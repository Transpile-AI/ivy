# local
import ivy
import ivy.functional.frontends.torch as torch_frontend
from ivy.functional.frontends.torch.func_wrapper import to_ivy_arrays_and_back
from ivy.func_wrapper import with_unsupported_dtypes


@to_ivy_arrays_and_back
def diagonal(input, *, offset=0, dim1=-2, dim2=-1):
    return torch_frontend.diagonal(input, offset=offset, dim1=dim1, dim2=dim2)


@to_ivy_arrays_and_back
def inv(input, *, out=None):
    return ivy.inv(input, out=out)


@to_ivy_arrays_and_back
def pinv(input, *, atol=None, rtol=None, hermitian=False, out=None):
    if atol is None:
        return ivy.pinv(input, rtol=rtol, out=out)
    else:
        sigma = ivy.svdvals(input)[0]
        if rtol is None:
            rtol = atol / sigma
        else:
            if atol > rtol * sigma:
                rtol = atol / sigma

    return ivy.pinv(input, rtol=rtol, out=out)


@to_ivy_arrays_and_back
def det(input, *, out=None):
    return ivy.det(input, out=out)


@to_ivy_arrays_and_back
def eigvalsh(input, UPLO="L", *, out=None):
    return ivy.eigvalsh(input, UPLO=UPLO, out=out)


@to_ivy_arrays_and_back
def qr(input, mode="reduced", *, out=None):
    if mode == "reduced":
        ret = ivy.qr(input, mode="reduced")
    elif mode == "r":
        Q, R = ivy.qr(input, mode="r")
        Q = []
        ret = Q, R
    elif mode == "complete":
        ret = ivy.qr(input, mode="complete")
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


@to_ivy_arrays_and_back
def slogdet(input, *, out=None):
    return ivy.slogdet(input, out=out)


@to_ivy_arrays_and_back
def matrix_power(input, n, *, out=None):
    return ivy.matrix_power(input, n, out=out)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def cross(input, other, *, dim=-1, out=None):
    return torch_frontend.cross(input, other, dim, out=out)


@to_ivy_arrays_and_back
def matrix_rank(input, *, atol=None, rtol=None, hermitian=False, out=None):
    return ivy.astype(ivy.matrix_rank(input, atol=atol, rtol=rtol, out=out), ivy.int64)


@to_ivy_arrays_and_back
def cholesky(input, *, upper=False, out=None):
    return ivy.cholesky(input, upper=upper, out=out)


@to_ivy_arrays_and_back
def svd(input, /, *, full_matrices=True):
    return ivy.svd(input, compute_uv=True, full_matrices=full_matrices)


@to_ivy_arrays_and_back
def svdvals(input, *, out=None):
    return ivy.svdvals(input, out=out)


@to_ivy_arrays_and_back
def eig(input, *, out=None):
    return ivy.eig(input, out=out)
