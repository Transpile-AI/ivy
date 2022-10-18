# global
import ivy

from .. import versions
from ivy.func_wrapper import with_unsupported_dtypes

from ivy.functional.frontends.tensorflow import promote_types_of_tensorflow_inputs


def matrix_rank(a, tol=None, valiate_args=False, name=None):
    return ivy.matrix_rank(a, tol)


def det(input, name=None):
    return ivy.det(input)


def eigh(tensor, name=None):
    input_dtype = tensor.dtype
    input_tensor = ivy.astype(tensor, ivy.float32)
    output_tensor = ivy.eigh(input_tensor)
    output_tensor = ivy.astype(output_tensor, input_dtype)
    e = output_tensor[0]
    v = output_tensor[1]
    return e, v


def eigvalsh(tensor, name=None):
    return ivy.eigvalsh(tensor)


def solve(x, y):
    x, y = promote_types_of_tensorflow_inputs(x, y)
    return ivy.solve(x, y)


def logdet(matrix, name=None):
    return ivy.det(matrix).log()


logdet.supported_dtypes = ("float16", "float32", "float64")


def slogdet(input, name=None):
    return ivy.slogdet(input)


def cholesky_solve(chol, rhs, name=None):
    chol, rhs = promote_types_of_tensorflow_inputs(chol, rhs)
    y = ivy.solve(chol, rhs)
    return ivy.solve(ivy.matrix_transpose(chol), y)


def pinv(a, rcond=None, validate_args=False, name=None):
    return ivy.pinv(a, rcond)


def tensordot(a, b, axes, name=None):
    a, b = promote_types_of_tensorflow_inputs(a, b)
    return ivy.tensordot(a, b, axes)


@with_unsupported_dtypes(
    {"2.9.0 and below": ("float16", "bfloat16")}, versions["tensorflow"]
)
def eye(num_rows, num_columns=None, batch_shape=None, dtype=ivy.float32, name=None):
    return ivy.eye(num_rows, num_columns, batch_shape=batch_shape, dtype=dtype)


def norm(tensor, ord="euclidean", axis=None, keepdims=None, name=None):

    keepdims = keepdims or False

    # Check if it's a matrix norm
    if (type(axis) in [tuple, list]) and (len(axis) == 2):
        return ivy.matrix_norm(tensor, ord=ord, axis=axis, keepdims=keepdims)
    # Else resort to a vector norm
    return ivy.vector_norm(tensor, ord=ord, axis=axis, keepdims=keepdims)


norm.supported_dtypes = (
    "float32",
    "float64",
)


def normalize(tensor, ord="euclidean", axis=None, name=None):
    _norm = norm(tensor, ord=ord, axis=axis, keepdims=True)
    _norm = ivy.astype(_norm, ivy.dtype(tensor))
    normalized = ivy.divide(tensor, _norm)
    return normalized, _norm


normalize.supported_dtypes = (
    "float32",
    "float64",
)
