# global
import os
import ivy
import pytest
import numpy as np

# local
from ivy_models.transformers.helpers import FeedForward, PreNorm
from ivy_models.transformers.perceiver_io import PerceiverIOSpec, PerceiverIO


# Helpers #
# --------#

def test_feedforward(dev_str, f, call):
    ivy.seed(0)
    feedforward = FeedForward(4, dev_str=dev_str)
    x = ivy.random_uniform(shape=(1, 3, 4), dev_str=dev_str)
    ret = feedforward(x)
    assert list(ret.shape) == [1, 3, 4]


def test_prenorm(dev_str, f, call):
    ivy.seed(0)
    att = ivy.MultiHeadAttention(4, dev_str=dev_str)
    prenorm = PreNorm(4, att, dev_str=dev_str)
    x = ivy.random_uniform(shape=(1, 3, 4), dev_str=dev_str)
    ret = prenorm(x)
    assert list(ret.shape) == [1, 3, 4]


# Perceiver IO #
# -------------#

@pytest.mark.parametrize(
    "batch_shape", [[1]])
@pytest.mark.parametrize(
    "img_dims", [[224, 224]])
@pytest.mark.parametrize(
    "queries_dim", [1024])
@pytest.mark.parametrize(
    "learn_query", [True])
@pytest.mark.parametrize(
    "load_weights", [True, False])
def test_perceiver_io_img_classification(dev_str, f, call, batch_shape, img_dims, queries_dim, learn_query,
                                         load_weights):
    # params
    input_dim = 3
    num_input_axes = 2
    output_dim = 10

    # inputs
    this_dir = os.path.dirname(os.path.realpath(__file__))
    img = ivy.array(np.load(os.path.join(this_dir, 'img.npy'))[None], dtype_str='float32', dev_str=dev_str)
    queries = None if learn_query else ivy.random_uniform(shape=batch_shape + [1, queries_dim], dev_str=dev_str)

    model = PerceiverIO(PerceiverIOSpec(input_dim=input_dim,
                                        num_input_axes=num_input_axes,
                                        output_dim=output_dim,
                                        queries_dim=queries_dim,
                                        learn_query=learn_query,
                                        query_shape=[1],
                                        max_fourier_freq=img_dims[0],
                                        num_fourier_freq_bands=64,
                                        device=dev_str))

    # maybe load weights
    if load_weights:
        this_dir = os.path.dirname(os.path.realpath(__file__))
        weight_fpath = os.path.join(this_dir, '../ivy_models/transformers/pretrained_weights/perceiver_io.pickled')
        v = ivy.Container.from_disk_as_pickled(weight_fpath).from_numpy()

        # try:
        #     assert model.v.num_arrays() == v.num_arrays()
        #     assert ivy.Container.identical_array_shapes([model.v, v])
        # except AssertionError:
        #     raise Exception(
        #         'model.v.size_ordered_arrays(): {}\n\n'
        #         'v.size_ordered_arrays(): {}\n\n'.format(
        #             model.v.size_ordered_arrays(), v.size_ordered_arrays()))

        # ToDo: incrementally update this restructuring, so that the loaded jax weights are converted
        v = v.restructure(
            {'perceiver_encoder/~/trainable_position_encoding/pos_embs': 'latents',

             'perceiver_encoder/~/cross_attention/layer_norm/scale': 'layers/v0/cross_att/norm/scale',
             'perceiver_encoder/~/cross_attention/layer_norm/offset': 'layers/v0/cross_att/norm/offset',

             'perceiver_encoder/~/cross_attention/layer_norm_1/scale': 'layers/v0/cross_att/norm_context/scale',
             'perceiver_encoder/~/cross_attention/layer_norm_1/offset': 'layers/v0/cross_att/norm_context/offset',

             'perceiver_encoder/~/cross_attention/attention/linear/w':
                 {'key_chain': 'layers/v0/cross_att/fn/to_q/w', 'pattern': 'a b -> b a'},
             'perceiver_encoder/~/cross_attention/attention/linear/b': 'layers/v0/cross_att/fn/to_q/b',

             'perceiver_encoder/~/cross_attention/attention/linear_1/w':
                 {'key_chain': 'layers/v0/cross_att/fn/to_kv/k/w', 'pattern': 'a b -> b a'},
             'perceiver_encoder/~/cross_attention/attention/linear_1/b': 'layers/v0/cross_att/fn/to_kv/k/b',

             'perceiver_encoder/~/cross_attention/attention/linear_2/w':
                 {'key_chain': 'layers/v0/cross_att/fn/to_kv/v/w', 'pattern': 'a b -> b a'},
             'perceiver_encoder/~/cross_attention/attention/linear_2/b': 'layers/v0/cross_att/fn/to_kv/v/b',

             'perceiver_encoder/~/cross_attention/attention/linear_3/w':
                 {'key_chain': 'layers/v0/cross_att/fn/to_out/submodules/v0/w', 'pattern': 'a b -> b a'},
             'perceiver_encoder/~/cross_attention/attention/linear_3/b':
                 'layers/v0/cross_att/fn/to_out/submodules/v0/b'},
            keep_orig=False)

        # layers.v0.cross_att.fn.to_out.submodules.v0

        # assert ivy.Container.identical_structure([model.v, v])

        model = PerceiverIO(PerceiverIOSpec(input_dim=input_dim,
                                            num_input_axes=num_input_axes,
                                            output_dim=output_dim,
                                            queries_dim=queries_dim,
                                            learn_query=learn_query,
                                            query_shape=[1],
                                            max_fourier_freq=img_dims[0],
                                            num_fourier_freq_bands=64,
                                            device=dev_str), v=v, with_partial_v=True)

        # expected submodule returns
        expected_submod_rets = ivy.Container()
        for dct in [{'val': 'LayerNorm_0', 'atol': 1e-6, 'rtol': 1e-6},
                    {'val': 'LayerNorm_1', 'atol': 1e-3},
                    {'val': 'Linear_0', 'atol': 1e-5},
                    {'val': 'Linear_1', 'atol': 1e-3},
                    {'val': 'Linear_2', 'atol': 1e-3},
                    {'val': 'Linear_3', 'atol': 1e-3}]:
            key = dct['val']
            dct['val'] = np.load(os.path.join(this_dir, key + '.npy'))
            expected_submod_rets[key] = dct

        # check submod returns
        output = model(img, queries=queries, expected_submod_rets=expected_submod_rets)

    else:

        # output
        output = model(img, queries=queries)

    # cardinality test
    assert output.shape == tuple(batch_shape + [1, output_dim])


@pytest.mark.parametrize(
    "batch_shape", [[3]])
@pytest.mark.parametrize(
    "img_dims", [[32, 32]])
@pytest.mark.parametrize(
    "queries_dim", [32])
@pytest.mark.parametrize(
    "learn_query", [True, False])
def test_perceiver_io_flow_prediction(dev_str, f, call, batch_shape, img_dims, queries_dim, learn_query):
    # params
    input_dim = 3
    num_input_axes = 3
    output_dim = 2

    # inputs
    img = ivy.random_uniform(shape=batch_shape + [2] + img_dims + [3], dev_str=dev_str)
    queries = ivy.random_uniform(shape=batch_shape + img_dims + [32], dev_str=dev_str)

    # model call
    model = PerceiverIO(PerceiverIOSpec(input_dim=input_dim,
                                        num_input_axes=num_input_axes,
                                        output_dim=output_dim,
                                        queries_dim=queries_dim,
                                        learn_query=learn_query,
                                        query_shape=img_dims,
                                        max_fourier_freq=img_dims[0],
                                        device=dev_str))

    # output
    output = model(img, queries=queries)

    # cardinality test
    assert output.shape == tuple(batch_shape + img_dims + [output_dim])
