from typing import Union, Optional, Sequence
import mxnet as mx

from ivy.utils.exceptions import IvyNotImplementedException


def min(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def max(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def mean(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def prod(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    dtype: Optional[None] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def std(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    correction: Union[(int, float)] = 0.0,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def sum(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    dtype: Optional[None] = None,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def var(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: Optional[Union[(int, Sequence[int])]] = None,
    correction: Union[(int, float)] = 0.0,
    keepdims: bool = False,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def cumprod(
    x: Union[(None, mx.ndarray.NDArray)],
    /,
    *,
    axis: int = 0,
    exclusive: bool = False,
    reverse: bool = False,
    dtype: Optional[None] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def cumsum(
    x: Union[(None, mx.ndarray.NDArray)],
    axis: int = 0,
    exclusive: bool = False,
    reverse: bool = False,
    *,
    dtype: Optional[None] = None,
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()


def einsum(
    equation: str,
    *operands: Union[(None, mx.ndarray.NDArray)],
    out: Optional[Union[(None, mx.ndarray.NDArray)]] = None,
) -> Union[(None, mx.ndarray.NDArray)]:
    raise IvyNotImplementedException()
