"""
Collection of tests for module converters
"""

# global
import pytest
import torch.nn
import haiku as hk
import jax.numpy as jnp

# local
import ivy
import ivy_tests.helpers as helpers


class TorchModule(torch.nn.Module):
    def __init__(self, in_size, out_size, dev_str='cpu', hidden_size=64):
        super(TorchModule, self).__init__()
        self._linear0 = torch.nn.Linear(in_size, hidden_size)
        self._linear1 = torch.nn.Linear(hidden_size, hidden_size)
        self._linear2 = torch.nn.Linear(hidden_size, out_size)

    def forward(self, x):
        x = x.unsqueeze(0)
        x = torch.tanh(self._linear0(x))
        x = torch.tanh(self._linear1(x))
        return torch.tanh(self._linear2(x))[0]


class HaikuModule(hk.Module):
    def __init__(self, in_size, out_size, dev_str='cpu', hidden_size=64):
        super(HaikuModule, self).__init__()
        self._linear0 = hk.Linear(hidden_size)
        self._linear1 = hk.Linear(hidden_size)
        self._linear2 = hk.Linear(out_size)

    def __call__(self, x):
        x = jnp.expand_dims(x, 0)
        x = jnp.tanh(self._linear0(x))
        x = jnp.tanh(self._linear1(x))
        return jnp.tanh(self._linear2(x))[0]


NATIVE_MODULES = {'torch': TorchModule,
                  'jax': HaikuModule}


# to_ivy_module
@pytest.mark.parametrize(
    "bs_ic_oc", [([1, 2], 4, 5)])
@pytest.mark.parametrize(
    "from_class_and_args", [True, False])
def test_to_ivy_module(bs_ic_oc, from_class_and_args, dev_str, call):
    # smoke test
    if call not in [helpers.torch_call, helpers.jnp_call]:
        # Currently only implemented for PyTorch
        pytest.skip()
    batch_shape, input_channels, output_channels = bs_ic_oc
    x = ivy.cast(ivy.linspace(ivy.zeros(batch_shape), ivy.ones(batch_shape), input_channels), 'float32')
    natvie_module_class = NATIVE_MODULES[ivy.current_framework_str()]
    if from_class_and_args:
        ivy_module = ivy.to_ivy_module(native_module_class=natvie_module_class,
                                       args=[input_channels, output_channels],
                                       dev_strs=[dev_str])
    else:
        if call is helpers.jnp_call:
            def forward_fn(*a, **kw):
                model = natvie_module_class(input_channels, output_channels)
                return model(*a, **kw)
            native_module = hk.transform(forward_fn)
        else:
            native_module = natvie_module_class(input_channels, output_channels)
        ivy_module = ivy.to_ivy_module(native_module, dev_strs=[dev_str])

    def loss_fn(v_=None):
        out = ivy_module(x, v=v_)
        return ivy.reduce_mean(out)[0]

    # train
    loss_tm1 = 1e12
    loss = None
    grads = None
    loss_fn()  # for on-call mode
    for i in range(10):
        loss, grads = ivy.execute_with_gradients(loss_fn, ivy_module.v)
        ivy_module.v = ivy.gradient_descent_update(ivy_module.v, grads, 1e-3)
        assert loss < loss_tm1
        loss_tm1 = loss

    # type test
    assert ivy.is_array(loss)
    assert isinstance(grads, ivy.Container)
    # cardinality test
    if call is helpers.mx_call:
        # mxnet slicing cannot reduce dimension to zero
        assert loss.shape == (1,)
    else:
        assert loss.shape == ()
    # value test
    assert (abs(grads).reduce_max() > 0).all_true()
