# local
import ivy
from ivy.func_wrapper import with_unsupported_dtypes
from ivy.functional.frontends.torch.func_wrapper import to_ivy_arrays_and_back


def _compute_threshold(input, threshold, value, inplace):
    ret = ivy.where(ivy.greater(input, threshold), input, value)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


def _compute_elu(input, alpha=1.0, inplace=False):
    prod = ivy.multiply(
        alpha,
        ivy.subtract(ivy.exp(input), 1),
    )
    ret = ivy.where(ivy.greater(input, 0), input, prod)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


def _selu_with_inplace(input, inplace=False):
    alpha = 1.6732632423543772848170429916717
    scale = 1.0507009873554804934193349852946
    prod = ivy.multiply(
        alpha,
        ivy.subtract(
            ivy.exp(input),
            1,
        ),
    )
    min_ = ivy.multiply(
        scale,
        ivy.minimum(0, prod),
    )
    max_ = ivy.multiply(
        scale,
        ivy.maximum(0, input),
    )
    ret = ivy.add(min_, max_)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


def _rrelu(input, lower=1.0 / 8, upper=1.0 / 3, training=False, inplace=False):
    if training:
        # alpha = ivy.random_uniform(low=lower, high=upper)
        # ToDo implement alpha correctly after fixing ivy.random_uniform
        pass
    else:
        alpha = (lower + upper) / 2
    ret = ivy.subtract(
        ivy.relu(input), ivy.multiply(alpha, ivy.relu(ivy.negative(input)))
    )
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def sigmoid(input):
    return ivy.sigmoid(input)


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def leaky_relu(input, negative_slope=0.01, inplace=False):
    ret = ivy.leaky_relu(input, alpha=negative_slope)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def softmax(input, dim=None, _stacklevel=3, dtype=None):
    if dtype:
        input = ivy.astype(ivy.array(input), ivy.as_ivy_dtype(dtype))
    return ivy.softmax(input, axis=dim)


@to_ivy_arrays_and_back
@with_unsupported_dtypes(
    {
        "1.11.0 and below": (
            "float16",
            "bfloat16",
        )
    },
    "torch",
)
def gelu(
    input,
):  # , *, approximate="none"): ToDo: approximate is added in in PyTorch 1.12.1
    # if approximate == "none":
    # approximate = False
    # else:
    # approximate = True
    return ivy.gelu(input, approximate=False)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def tanh(input):
    return ivy.tanh(input)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def softmin(input, dim=None, dtype=None):
    if dtype:
        input = ivy.astype(ivy.array(input), ivy.as_ivy_dtype(dtype))
    return ivy.softmax(-input, axis=dim)


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def threshold(input, threshold, value, inplace=False):
    return _compute_threshold(input, threshold, value, inplace)


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def threshold_(input, threshold, value):
    return _compute_threshold(input, threshold, value, inplace=True)


def relu6(input, inplace=False):
    ret = ivy.relu6(input)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


def elu(input, alpha=1.0, inplace=False):
    out = input if inplace else None
    return ivy.elu(input, alpha=alpha, out=out)


def elu_(input, alpha=1.0):
    return ivy.elu(input, alpha=alpha, out=input)


def celu(input, alpha=1.0, inplace=False):
    out = input if inplace else None
    return ivy.celu(input, alpha=alpha, out=out)


def mish(input, inplace=False):
    ret = ivy.multiply(
        input,
        ivy.tanh(ivy.softplus(input)),
    )
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
def relu(input, inplace=False):
    ret = ivy.relu(input)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


def relu_(input):
    ret = ivy.relu(input)
    ivy.inplace_update(input, ret)
    return input


def selu(input, inplace=False):
    out = input if inplace else None
    return ivy.selu(input, out=out)


@to_ivy_arrays_and_back
def prelu(input, weight):
    return ivy.add(ivy.maximum(0, input), ivy.multiply(weight, ivy.minimum(0, input)))


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def rrelu(input, lower=1.0 / 8, upper=1.0 / 3, training=False, inplace=False):
    return _rrelu(input, lower, upper, training, inplace)


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def rrelu_(input, lower=1.0 / 8, upper=1.0 / 3, training=False):
    return _rrelu(input, lower, upper, training, inplace=True)


@to_ivy_arrays_and_back
def hardshrink(input, lambd=0.5):
    mask = ivy.logical_or(ivy.greater(input, lambd), ivy.less(input, -lambd))
    return ivy.where(mask, input, 0.0)


@to_ivy_arrays_and_back
def softshrink(input, lambd=0.5):
    low = ivy.where(ivy.less(input, -lambd), ivy.add(input, lambd), 0)
    up = ivy.where(ivy.greater(input, lambd), ivy.subtract(input, lambd), 0)
    return ivy.add(low, up)


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def silu(input, inplace=False):
    out = input if inplace else None
    return ivy.silu(input, out=out)


@to_ivy_arrays_and_back
def glu(input, dim=-1):
    return ivy.glu(input, axis=dim)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def log_softmax(input, dim=None, _stacklevel=3, dtype=None):
    if dtype:
        input = ivy.astype(ivy.array(input), ivy.as_ivy_dtype(dtype))
    if dim is None:
        dim = -1
    return ivy.log_softmax(input, axis=dim)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def tanhshrink(input):
    return ivy.subtract(input, ivy.tanh(input))


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def leaky_relu_(input, negative_slope=0.01):
    ret = ivy.leaky_relu(input, alpha=negative_slope)
    ivy.inplace_update(input, ret)
    return input


@to_ivy_arrays_and_back
def hardswish(input, inplace=False):
    out = input if inplace else None
    return ivy.hard_silu(input, out=out)


@to_ivy_arrays_and_back
def hardsigmoid(input, inplace=False):
    out = input if inplace else None
    return ivy.hard_sigmoid(input, out=out)


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def hardtanh(input, min_val=-1.0, max_val=1.0, inplace=False):
    less = ivy.where(ivy.less(input, min_val), min_val, input)
    ret = ivy.where(ivy.greater(input, max_val), max_val, less).astype(input.dtype)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def hardtanh_(input, min_val=-1.0, max_val=1.0):
    less = ivy.where(ivy.less(input, min_val), min_val, input)
    ret = ivy.where(ivy.greater(input, max_val), max_val, less).astype(input.dtype)
    ivy.inplace_update(input, ret)
    return input


@to_ivy_arrays_and_back
def normalize(input, p=2.0, dim=1, eps=1e-12, out=None):
    abs_square = ivy.pow(ivy.abs(input), p)
    sum_ = ivy.sum(abs_square, axis=dim, keepdims=True)
    pnorm_res = ivy.pow(sum_, 1.0 / p)
    max_ = ivy.maximum(pnorm_res, eps)
    return ivy.divide(input, max_, out=out)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def layer_norm(input, normalized_shape, weight=None, bias=None, eps=1e-05):
    shape = ivy.shape(input)
    if isinstance(normalized_shape, int) and normalized_shape == shape[-1]:
        axis = [-1]
    else:
        assert normalized_shape == shape[-len(normalized_shape) :]
        axis = list(range(len(shape) - len(normalized_shape), len(shape)))
    return ivy.layer_norm(input, axis, scale=weight, b=bias, epsilon=eps)


@to_ivy_arrays_and_back
@with_unsupported_dtypes(
    {
        "1.11.0 and below": (
            "float16",
            "bfloat16",
        )
    },
    "torch",
)
def softplus(input, beta=1, threshold=20):
    return ivy.softplus(input, beta=beta, threshold=threshold)


@to_ivy_arrays_and_back
def softsign(input):
    return ivy.softsign(input)


@to_ivy_arrays_and_back
def logsigmoid(input):
    return ivy.log_sigmoid(input)


@to_ivy_arrays_and_back
@with_unsupported_dtypes(
    {
        "1.11.0 and below": (
            "float16",
            "bfloat16",
        )
    },
    "torch",
)
def group_norm(input, num_groups, weight=None, bias=None, eps=1e-05):
    shape = ivy.shape(input)
    assert shape[1] % num_groups == 0
    groups = shape[1] // num_groups
    num_dims = ivy.get_num_dims(input)
    expand_dims = (
        [0, *range(2, num_dims)] if weight is not None and num_dims > 2 else [0]
    )
    ret = ivy.concat(
        [
            ivy.layer_norm(
                input[:, i * groups : (i + 1) * groups, ...],
                list(range(1, num_dims)),
                scale=ivy.expand_dims(
                    weight[i * groups : (i + 1) * groups], axis=expand_dims
                )
                if weight is not None
                else None,
                b=ivy.expand_dims(bias[i * groups : (i + 1) * groups], axis=expand_dims)
                if bias is not None
                else None,
                epsilon=eps,
            )
            for i in range(num_groups)
        ],
        axis=1,
    )

    return ret


@with_unsupported_dtypes(
    {
        "1.11.0 and below": (
            "bfloat16",
            "float16",
        )
    },
    "torch",
)
@to_ivy_arrays_and_back
def batch_norm(
    input,
    running_mean,
    running_var,
    weight=None,
    bias=None,
    training=False,
    momentum=0.1,
    eps=1e-5,
):
    # momentum is not practically used in the functional api
    return ivy.batch_norm(
        input,
        running_mean,
        running_var,
        offset=bias,
        scale=weight,
        training=training,
        eps=eps,
    )
