# global
import paddle
from typing import Union, Optional, Sequence
from ivy.exceptions import IvyNotImplementedException


def all(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x = paddle.as_tensor(x).type(paddle.bool)
    if axis is None:
        num_dims = len(x.shape)
        axis = list(range(num_dims))
    if isinstance(axis, int):
        return paddle.all(x, dim=axis, keepdim=keepdims, out=out)
    dims = len(x.shape)
    axis = [i % dims for i in axis]
    axis.sort()
    for i, a in enumerate(axis):
        x = paddle.all(x, dim=a if keepdims else a - i, keepdim=keepdims, out=out)
    return x


all.support_native_out = True


def any(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


