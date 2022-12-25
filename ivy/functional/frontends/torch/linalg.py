# local
import ivy
import ivy.functional.frontends.torch as torch_frontend
from ivy.functional.frontends.torch.func_wrapper import to_ivy_arrays_and_back
from ivy.func_wrapper import with_unsupported_dtypes


@to_ivy_arrays_and_back
def diagonal(A, *, offset=0, dim1=-2, dim2=-1):
    return torch_frontend.diagonal(A, offset=offset, dim1=dim1, dim2=dim2)


@to_ivy_arrays_and_back
def inv(input, *, out=None):
    return ivy.inv(input, out=out)


@to_ivy_arrays_and_back
def pinv(input, *, atol=None, rtol=None, hermitian=False, out=None):
    # TODO: add handling for hermitian once complex numbers are supported
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
    # TODO: add handling for out
    return ivy.slogdet(input)


@to_ivy_arrays_and_back
def matrix_power(input, n, *, out=None):
    return ivy.matrix_power(input, n, out=out)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16",)}, "torch")
def cross(input, other, *, dim=-1, out=None):
    return torch_frontend.cross(input, other, dim, out=out)


@to_ivy_arrays_and_back
def matrix_rank(input, *, atol=None, rtol=None, hermitian=False, out=None):
    # TODO: add handling for hermitian once complex numbers are supported
    return ivy.astype(ivy.matrix_rank(input, atol=atol, rtol=rtol, out=out), ivy.int64)


@to_ivy_arrays_and_back
def cholesky(input, *, upper=False, out=None):
    return ivy.cholesky(input, upper=upper, out=out)


@to_ivy_arrays_and_back
def svd(A, /, *, full_matrices=True, driver=None, out=None):
    # TODO: add handling for driver and out
    return ivy.svd(A, compute_uv=True, full_matrices=full_matrices)


@to_ivy_arrays_and_back
def svdvals(A, *, driver=None, out=None):
    # TODO: add handling for driver
    return ivy.svdvals(A, out=out)


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"1.11.0 and below": ("float16", "bfloat16")}, "torch")
def tensorinv(input, ind=2, *, out=None):
    not_invertible = "Reshaped tensor is not invertible"
    prod_cond = "Tensor shape must satisfy prod(A.shape[:ind]) == prod(A.shape[ind:])"
    input_shape = ivy.shape(input)
    if ind > 0:
        shape_ind_end = input_shape[:ind]
        shape_ind_start = input_shape[ind:]
        prod_ind_end = 1
        prod_ind_start = 1
        for i in shape_ind_start:
            prod_ind_start *= i
        for j in shape_ind_end:
            prod_ind_end *= j
        if prod_ind_end == prod_ind_start:
            inverse_shape = shape_ind_start + shape_ind_end
            input = ivy.reshape(input, shape=(prod_ind_end, -1))
            inverse_shape_tuple = tuple([*inverse_shape])
            if len(ivy.shape(input)) > 1 and (ivy.inv(input)).any():
            # TODO: replace ivy.inv(input) with ivy.linalg.cond or torch.linalg.cond
                inverse_tensor = ivy.inv(input)
            else:
                ret = ivy.reshape(input, shape=inverse_shape_tuple, out=out)
                return ret if ivy.inv(ret) else not_invertible
        else:
            raise ValueError(f'{prod_cond} or {not_invertible}.')
    else:
        raise ValueError("Expected a strictly positive integer for 'ind'")
    return ivy.reshape(inverse_tensor, shape=inverse_shape_tuple, out=out)
