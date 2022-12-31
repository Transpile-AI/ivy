# global
import ivy
from ivy.functional.frontends.numpy.func_wrapper import to_ivy_arrays_and_back
from ivy import asarray,issubclass,bool

@to_ivy_arrays_and_back
def all(
    a,
    axis=None,
    out=None,
    keepdims=False,
    *,
    where=True,
):
    ret = ivy.all(a, axis=axis, keepdims=keepdims, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@to_ivy_arrays_and_back
def any(
    a,
    axis=None,
    out=None,
    keepdims=False,
    *,
    where=True,
):
    ret = ivy.any(a, axis=axis, keepdims=keepdims, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@to_ivy_arrays_and_back
def isscalar(element):
    return (
        isinstance(element, int)
        or isinstance(element, bool)
        or isinstance(element, float)
    )

@to_ivy_arrays_and_back   
def iscomplex(element):
    ax = ivy.asarray(element)
    if issubclass(ax.dtype.type, ivy.complexfloating):
        return ax.imag != 0
    res = ivy.zeros(ax.shape, bool)
    return res[()]