# global
import ivy


def matrix_rank(a, tol=None, valiate_args=False, name=None):
    return ivy.matrix_rank(a, tol)


def det(input, name=None):
    return ivy.det(input)


det.unsupported_dtypes = ("float16", "bfloat16")


def eigvalsh(tensor, name=None):
    return ivy.eigvalsh(tensor)


eigvalsh.unsupported_dtypes = ("float16", "bfloat16")


def solve(x, y):
    return ivy.solve(x, y)


solve.unsupported_dtypes = ("float16", "bfloat16")


def slogdet(input, name=None):
    return ivy.slogdet(input)


def pinv(a, rcond=None, validate_args=False, name=None):
    return ivy.pinv(a, rcond=rcond)


def qr(input, full_matrices=False, name=None):
    if full_matrices is False:
        return ivy.qr(input, mode="reduced")
    return ivy.qr(input, mode="complete")


qr.unsupported_dtypes = ("float16", "bfloat16")


def svd(tensor, full_matrices=False, compute_uv=True, name=None):
    return ivy.svd(tensor, full_matrices=full_matrices)


svd.unsupported_dtypes = ("float16", "bfloat16")


def cholesky_solve(chol, rhs, name=None):
    y = ivy.solve(chol, rhs)
    return ivy.solve(ivy.matrix_transpose(chol), y)


cholesky_solve.unsupported_dtypes = ("float16", "bfloat16")


def trace(a, offset=0, axis1=0, axis2=1, dtype=None):
    return ivy.trace(a, offset=offset)


def tensordot(x, y, axes, name=None):
    return ivy.tensordot(x, y, axes)


tensordot.supported_dtypes = ("float32", "float64")
