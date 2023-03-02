# global

torch_scatter = None
from typing import Union, Optional, Sequence


import paddle

# local
import ivy
from ivy.utils.exceptions import IvyNotImplementedException
from . import backend_version

# Array API Standard #
# -------------------#

def min(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.min(x, axis=axis, keepdim=keepdims)


def max(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.max(x, axis=axis, keepdims=keepdims)


def mean(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.mean(x, axis=axis, keepdim=keepdims)


def _infer_dtype(dtype: paddle.dtype) -> paddle.dtype:
    raise IvyNotImplementedException()


def prod(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    dtype: Optional[paddle.dtype] = None,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.prod(x, axis=axis, keepdim=keepdims, dtype=dtype)


def std(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    correction: Union[int, float] = 0,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if axis is None:
        axis = list(range(len(x.shape)))
    if axis == ():
        return x
    axis = (axis,) if isinstance(axis, int) else tuple(axis)
    if correction == 0:
        return paddle.std(x, axis=axis, unbiased=False, keepdim=keepdims)
    elif correction == 1:
        return paddle.std(x, axis=axis, unbiased=True, keepdim=keepdims)
    size = 1
    for a in axis:
        size *= x.shape[a]
    if size - correction <= 0:
        ret = paddle.std(x, axis=axis, unbiased=False, keepdim=keepdims)
        ret = ivy.full(ret.shape, float("nan"), dtype=ret.dtype)
        return ret
    ret = paddle.mul(
        paddle.std(x, axis=axis, unbiased=False, keepdim=keepdims),
        (size / (size - correction)) ** 0.5,
    )
    return ret

def sum(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    dtype: Optional[paddle.dtype] = None,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.sum(x, axis=axis, dtype=dtype, keepdim=keepdims)


def var(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    correction: Union[int, float] = 0,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if axis is None:
        axis = list(range(len(x.shape)))
    if axis == ():
        return x
    axis = (axis,) if isinstance(axis, int) else tuple(axis)
    if correction == 0:
        return paddle.var(x, axis=axis, unbiased=False, keepdim=keepdims)
    elif correction == 1:
        return paddle.var(x, axis=axis, unbiased=True, keepdim=keepdims)
    size = 1
    for a in axis:
        size *= x.shape[a]
    if size - correction <= 0:
        ret = paddle.var(x, axis=axis, unbiased=False, keepdim=keepdims)
        ret = ivy.full(ret.shape, float("nan"), dtype=ret.dtype)
        return ret
    else:    
        ret = paddle.mul(
        paddle.var(x, axis=axis, unbiased=False, keepdim=keepdims),
        (size / (size - correction)) ** 0.5,
        )
    return ret
    


# Extra #
# ----- #

def cumprod(
    x: paddle.Tensor,
    /,
    *,
    axis: int = 0,
    exclusive: bool = False,
    reverse: bool = False,
    dtype: Optional[paddle.dtype] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
     if dtype is None:
        dtype = x.dtype
    if out is None:
        out = paddle.ones_like(x, dtype=dtype)
    if reverse:
        x = paddle.flip(x, axis=[axis])
        out = paddle.flip(out, axis=[axis])
    for i in range(1, x.shape[axis]):
        out = paddle.concat([out.slice(0, i, axis), paddle.multiply(x.slice(0, i, axis), out.slice(0, i, axis))], axis=axis)
    if exclusive:
        out = paddle.concat([paddle.ones_like(x.slice(0, 1, axis), dtype=dtype), out.slice(0, out.shape[axis] - 1, axis)], axis=axis)
    if reverse:
        out = paddle.flip(out, axis=[axis])
    return out


def cumsum(
    x: paddle.Tensor,
    axis: int = 0,
    exclusive: bool = False,
    reverse: bool = False,
    *,
    dtype: Optional[paddle.dtype] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def einsum(
    equation: str,
    *operands: paddle.Tensor,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()
