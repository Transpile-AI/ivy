import ivy


def relu(x):
    return ivy.relu(x)


relu.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def relu6(x):
    res = ivy.minimum(ivy.maximum(x, 0.0), 6.0)

    dtype = ivy.as_ivy_dtype(ivy.asarray(x).dtype)
    if "float" in dtype:
        return res.astype(dtype)

    return ivy.astype(res, "float64")


relu6.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def soft_sign(x):
    ret = x / (ivy.abs(x) + 1)

    dtype = ivy.as_ivy_dtype(ivy.asarray(x).dtype)
    if "float" not in dtype:
        if "64" in dtype[-2:]:
            dtype = "float64"
        else:
            dtype = "float32"

    return ivy.astype(ret, dtype)


soft_sign.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def silu(x):
    return x * sigmoid(x)


soft_sign.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def leaky_relu(x, negative_slope=0.01):
    return ivy.leaky_relu(x, alpha=negative_slope)


leaky_relu.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def gelu(x, approximate=True):
    return ivy.gelu(x, approximate=approximate)


gelu.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def sigmoid(x):
    return ivy.sigmoid(x)


sigmoid.unsupported_dtypes = {"torch": ("float16", "bfloat16")}


def one_hot(x, num_classes, *, device=None, out=None):
    return ivy.one_hot(x, num_classes, device=device, out=out)


def softmax(x, /, *, axis=None):
    return ivy.softmax(x, axis=axis)


def softplus(x):
    return ivy.softplus(x)
