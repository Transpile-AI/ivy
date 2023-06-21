# local
import ivy
from ivy.func_wrapper import with_unsupported_dtypes, with_supported_dtypes
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
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def sigmoid(input):
    return ivy.sigmoid(input)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def leaky_relu(input, negative_slope=0.01, inplace=False):
    ret = ivy.leaky_relu(input, alpha=negative_slope)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def softmax(input, dim=None, _stacklevel=3, dtype=None):
    if dtype:
        input = ivy.astype(ivy.array(input), ivy.as_ivy_dtype(dtype))
    return ivy.softmax(input, axis=dim)


@to_ivy_arrays_and_back
@with_unsupported_dtypes(
    {
        "2.0.1 and below": (
            "float16",
            "bfloat16",
        )
    },
    "torch",
)
def gelu(input, *, approximate="none"):
    if approximate == "none":
        return ivy.gelu(input, approximate=False)
    elif approximate == "tanh":
        return ivy.gelu(input, approximate=True)
    else:
        raise ivy.utils.exceptions.IvyException(
            "`approximate` argument must be either 'none' or 'tanh'."
        )


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def tanh(input):
    return ivy.tanh(input)


@to_ivy_arrays_and_back
@with_unsupported_dtypes(
    {
        "2.0.1 and below": (
            "float16",
            "bfloat16",
        )
    },
    "torch",
)
def logsigmoid(input):
    return ivy.logsigmoid(input)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def softmin(input, dim=None, dtype=None):
    if dtype:
        input = ivy.astype(ivy.array(input), ivy.as_ivy_dtype(dtype))
    return ivy.softmax(-input, axis=dim)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def threshold(input, threshold, value, inplace=False):
    return _compute_threshold(input, threshold, value, inplace)


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def threshold_(input, threshold, value):
    return _compute_threshold(input, threshold, value, inplace=True)


@to_ivy_arrays_and_back
def relu6(input, inplace=False):
    ret = ivy.relu6(input)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
def elu(input, alpha=1.0, inplace=False):
    return _compute_elu(input, alpha, inplace=inplace)


def elu_(input, alpha=1.0):
    return _compute_elu(input, alpha, inplace=True)


@to_ivy_arrays_and_back
def celu(input, alpha=1.0, inplace=False):
    prod = ivy.multiply(
        alpha,
        ivy.subtract(
            ivy.exp(ivy.divide(input, alpha)),
            1,
        ),
    )
    ret = ivy.add(
        ivy.maximum(0, input),
        ivy.minimum(0, prod),
    )
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
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


@to_ivy_arrays_and_back
def selu(input, inplace=False):
    ret = ivy.selu(input)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
def prelu(input, weight):
    return ivy.add(ivy.maximum(0, input), ivy.multiply(weight, ivy.minimum(0, input)))


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def rrelu(input, lower=1.0 / 8, upper=1.0 / 3, training=False, inplace=False):
    return _rrelu(input, lower, upper, training, inplace)


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def rrelu_(input, lower=1.0 / 8, upper=1.0 / 3, training=False):
    return _rrelu(input, lower, upper, training, inplace=True)


@to_ivy_arrays_and_back
def hardshrink(input, lambd=0.5):
    mask = ivy.logical_or(ivy.greater(input, lambd), ivy.less(input, -lambd))
    return ivy.where(mask, input, 0.0)


@to_ivy_arrays_and_back
def softsign(input):
    return ivy.divide(input, ivy.add(1, ivy.abs(input)))


@to_ivy_arrays_and_back
def softshrink(input, lambd=0.5):
    low = ivy.where(ivy.less(input, -lambd), ivy.add(input, lambd), 0)
    up = ivy.where(ivy.greater(input, lambd), ivy.subtract(input, lambd), 0)
    return ivy.add(low, up)


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
@to_ivy_arrays_and_back
def silu(input, inplace=False):
    ret = ivy.multiply(input, ivy.sigmoid(input))
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
def glu(input, dim=-1):
    a, b = ivy.split(input, num_or_size_splits=2, axis=dim)
    return ivy.multiply(a, ivy.sigmoid(b))


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def log_softmax(input, dim=None, _stacklevel=3, dtype=None):
    if dtype:
        input = ivy.astype(ivy.array(input), ivy.as_ivy_dtype(dtype))
    if dim is None:
        dim = -1
    return ivy.log_softmax(input, axis=dim)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def tanhshrink(input):
    return ivy.subtract(input, ivy.tanh(input))


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def leaky_relu_(input, negative_slope=0.01):
    ret = ivy.leaky_relu(input, alpha=negative_slope)
    ivy.inplace_update(input, ret)
    return input


@to_ivy_arrays_and_back
def hardswish(input, inplace=False):
    relu6_val = ivy.relu6(ivy.add(input, 3))
    ret = ivy.multiply(input, ivy.divide(relu6_val, 6))
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
def hardsigmoid(input, inplace=False):
    ret = ivy.divide(ivy.minimum(ivy.maximum(ivy.add(input, 3), 0), 6), 6)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
def hardtanh(input, min_val=-1.0, max_val=1.0, inplace=False):
    less = ivy.where(ivy.less(input, min_val), min_val, input)
    ret = ivy.where(ivy.greater(input, max_val), max_val, less).astype(input.dtype)
    if inplace:
        ivy.inplace_update(input, ret)
        return input
    return ret


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, "torch")
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
@with_unsupported_dtypes(
    {
        "2.0.1 and below": (
            "float16",
            "bfloat16",
        )
    },
    "torch",
)
def softplus(input, beta=1, threshold=20):
    return ivy.softplus(input, beta=beta, threshold=threshold)


@to_ivy_arrays_and_back
@with_supported_dtypes({"2.0.1 and below": ("float32", "float64")}, "torch")
def multi_head_attention_forward(
    query,
    key,
    value,
    embed_dim_to_check,
    num_heads,
    in_proj_weight,
    in_proj_bias,
    bias_k,
    bias_v,
    add_zero_attn,
    dropout_p,
    out_proj_weight,
    out_proj_bias,
    training=True,
    key_padding_mask=None,
    need_weights=True,
    attn_mask=None,
    use_separate_proj_weight=False,
    q_proj_weight=None,
    k_proj_weight=None,
    v_proj_weight=None,
    static_k=None,
    static_v=None,
    average_attn_weights=True,
    is_causal=False,
):
    # q/k/v shape: (seq_len, batch_size, embed_dim)
    seq_len, batch_size, embed_dim = query.shape
    assert embed_dim == embed_dim_to_check, \
        f"was expecting embedding dimension of {embed_dim_to_check}, but got {embed_dim}"
    assert key.shape == value.shape

    head_dim = embed_dim // num_heads
    assert head_dim * num_heads == embed_dim, "embed_dim needs to be divisible by heads"
    scale = ivy.sqrt(head_dim)

    if use_separate_proj_weight:
        assert key.shape[:2] == value.shape[:2], \
            f"key's sequence and batch dims {key.shape[:2]} do not match value's {value.shape[:2]}"
    else:
        assert key.shape == value.shape, f"key shape {key.shape} does not match value shape {value.shape}"
    
    if is_causal and key_padding_mask is None and not need_weights:
        mask = ivy.tril(ivy.ones((seq_len, seq_len), dtype=query.dtype), k=0)
        attn_mask = ivy.zeros((seq_len, seq_len), dtype=query.dtype)
        attn_mask = ivy.where(mask == 0., float("-inf"), 0)

    if in_proj_bias is None:
        q_bias, k_bias, v_bias = None, None, None
    else:
        q_bias, k_bias, v_bias = ivy.split(in_proj_bias, num_or_size_splits=3)

    if not use_separate_proj_weight:
        q_proj_weight, k_proj_weight, v_proj_weight = ivy.split(in_proj_weight, num_or_size_splits=3)

    q = ivy.linear(query, q_proj_weight, bias=q_bias)
    k = ivy.linear(key, k_proj_weight, bias=k_bias)
    v = ivy.linear(value, v_proj_weight, bias=v_bias)

    if bias_k is not None and bias_v is not None:
        assert static_k is None, "bias cannot be added to static key."
        assert static_v is None, "bias cannot be added to static value."
        k = ivy.concat([k, ivy.tile(bias_k, (1, batch_size, 1))])
        v = ivy.concat([v, ivy.tile(bias_v, (1, batch_size, 1))])
        if attn_mask is not None:
            attn_mask = ivy.concat([attn_mask, ivy.zeros((attn_mask.shape[0], 1), dtype=attn_mask.dtype)], axis=1)
        if key_padding_mask is not None:
            key_padding_mask = ivy.concat(
                [key_padding_mask, ivy.zeros((key_padding_mask.shape[0], 1), dtype=key_padding_mask.dtype).bool()],
                axis=1
            )

    q = ivy.swapaxes(q.reshape((q.shape[0], batch_size * num_heads, head_dim)), 0, 1)
    
    if static_k is None:
        k = ivy.swapaxes(k.reshape((k.shape[0], batch_size * num_heads, head_dim)), 0, 1)
    else:
        assert static_k.shape[0] == batch_size * num_heads, \
            f"expecting static_k.shape[0] of {batch_size * num_heads}, but got {static_k.shape[0]}"
        assert static_k.shape[2] == head_dim, \
            f"expecting static_k.shape[2] of {head_dim}, but got {static_k.shape[2]}"
        k = static_k
    
    if static_v is None:
        v = ivy.swapaxes(v.reshape((v.shape[0], batch_size * num_heads, head_dim)), 0, 1)
    else:
        assert static_v.shape[0] == batch_size * num_heads, \
            f"expecting static_v.shape[0] of {batch_size * num_heads}, but got {static_v.shape[0]}"
        assert static_v.shape[2] == head_dim, \
            f"expecting static_v.shape[2] of {head_dim}, but got {static_v.shape[2]}"
        v = static_v

    # TODO add_zero_attn doesn't work for all cases 
    # fix this and add test cases (by changing to add_zero_attn=st.booleans())
    if add_zero_attn:
        zero_attn_shape = (batch_size * num_heads, 1, head_dim)
        k = ivy.concat([k, ivy.zeros(zero_attn_shape, dtype=k.dtype)], axis=1)
        v = ivy.concat([v, ivy.zeros(zero_attn_shape, dtype=v.dtype)], axis=1)
        if attn_mask is not None:
            attn_mask = ivy.pad(attn_mask, [(0, 0), (0, 1)])
        if key_padding_mask is not None:
            key_padding_mask = ivy.pad(key_padding_mask, [(0, 0), (0, 1)])

    src_len = k.shape[1]
    attn_weights = ivy.matmul(q, ivy.swapaxes(k, 1, 2))
    assert list(attn_weights.shape) == [batch_size * num_heads, seq_len, src_len]

    attn_weights = attn_weights / scale

    if attn_mask is not None:
        attn_mask = ivy.expand_dims(attn_mask, axis=0)
        attn_weights += attn_mask

    if key_padding_mask is not None:    
        key_padding_mask = ivy.expand_dims(ivy.expand_dims(key_padding_mask, axis=1), axis=2)
        attn_weights = attn_weights.reshape((batch_size, num_heads, seq_len, src_len))
        attn_weights = ivy.where(
            key_padding_mask < 0.,
            float("-inf"),
            attn_weights
        )
        attn_weights = attn_weights.reshape((batch_size * num_heads, seq_len, src_len))

    attn_weights = ivy.softmax(attn_weights, axis=-1)
    attn_weights = ivy.dropout(attn_weights, dropout_p, training=training)

    attn_output = ivy.matmul(attn_weights, v)
    assert list(attn_output.shape) == [batch_size * num_heads, seq_len, head_dim]
    attn_output = ivy.swapaxes(attn_output, 0, 1).reshape((seq_len, batch_size, embed_dim))
    attn_output = ivy.linear(attn_output, out_proj_weight, bias=out_proj_bias)

    if need_weights:
        attn_weights = attn_weights.reshape((batch_size, num_heads, seq_len, src_len))
        if average_attn_weights:
            attn_weights = ivy.sum(attn_weights, axis=1) / num_heads
        return (attn_output, attn_weights)
    else:
        return (attn_output,)
