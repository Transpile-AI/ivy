from typing import Union, Optional, Sequence, Tuple, List
from numbers import Number


def moveaxis(
    a: Union[(None, tf.Variable)],
    source: Union[(int, Sequence[int])],
    destination: Union[(int, Sequence[int])],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.moveaxis Not Implemented")


def heaviside(
    x1: Union[(None, tf.Variable)],
    x2: Union[(None, tf.Variable)],
    /,
    *,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.heaviside Not Implemented")


def flipud(
    m: Union[(None, tf.Variable)],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.flipud Not Implemented")


def vstack(
    arrays: Union[(Sequence[None], Sequence[tf.Variable])],
    /,
    *,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.vstack Not Implemented")


def hstack(
    arrays: Union[(Sequence[None], Sequence[tf.Variable])],
    /,
    *,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.hstack Not Implemented")


def rot90(
    m: Union[(None, tf.Variable)],
    /,
    *,
    copy: Optional[bool] = None,
    k: int = 1,
    axes: Tuple[(int, int)] = (0, 1),
    out: Union[(None, tf.Variable)] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.rot90 Not Implemented")


def top_k(
    x: None,
    k: int,
    /,
    *,
    axis: int = (-1),
    largest: bool = True,
    out: Optional[Tuple[(None, None)]] = None,
) -> Tuple[(None, None)]:
    raise NotImplementedError("mxnet.top_k Not Implemented")


def fliplr(
    m: Union[(None, tf.Variable)],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.fliplr Not Implemented")


def i0(
    x: Union[(None, tf.Variable)],
    /,
    *,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.i0 Not Implemented")


def vsplit(
    ary: Union[(None, tf.Variable)],
    indices_or_sections: Union[(int, Tuple[(int, ...)])],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[Union[(None, tf.Variable)]]:
    raise NotImplementedError("mxnet.vsplit Not Implemented")


def dsplit(
    ary: Union[(None, tf.Variable)],
    indices_or_sections: Union[(int, Tuple[(int, ...)])],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[Union[(None, tf.Variable)]]:
    raise NotImplementedError("mxnet.dsplit Not Implemented")


def atleast_1d(
    *arys: Union[(None, tf.Variable, bool, Number)], copy: Optional[bool] = None
) -> List[Union[(None, tf.Variable)]]:
    raise NotImplementedError("mxnet.atleast_1d Not Implemented")


def dstack(
    arrays: Union[(Sequence[None], Sequence[tf.Variable])],
    /,
    *,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.dstack Not Implemented")


def atleast_2d(
    *arys: Union[(None, tf.Variable)], copy: Optional[bool] = None
) -> List[Union[(None, tf.Variable)]]:
    raise NotImplementedError("mxnet.atleast_2d Not Implemented")


def atleast_3d(
    *arys: Union[(None, tf.Variable, bool, Number)], copy: Optional[bool] = None
) -> List[Union[(None, tf.Variable)]]:
    raise NotImplementedError("mxnet.atleast_3d Not Implemented")


def take_along_axis(
    arr: Union[(None, tf.Variable)],
    indices: Union[(None, tf.Variable)],
    axis: int,
    /,
    *,
    mode: str = "fill",
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.take_along_axis Not Implemented")


def hsplit(
    ary: Union[(None, tf.Variable)],
    indices_or_sections: Union[(int, Tuple[(int, ...)])],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[Union[(None, tf.Variable)]]:
    raise NotImplementedError("mxnet.hsplit Not Implemented")


def broadcast_shapes(*shapes: Union[(List[int], List[Tuple])]) -> Tuple[(int, ...)]:
    raise NotImplementedError("mxnet.broadcast_shapes Not Implemented")


def expand(
    x: Union[(None, tf.Variable)],
    shape: Union[(List[int], List[Tuple])],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.expand Not Implemented")


def concat_from_sequence(
    input_sequence: Union[(Tuple[None], List[None])],
    /,
    *,
    new_axis: int = 0,
    axis: int = 0,
    out: Optional[Union[(None, tf.Variable)]] = None,
) -> Union[(None, tf.Variable)]:
    raise NotImplementedError("mxnet.concat_from_sequence Not Implemented")
