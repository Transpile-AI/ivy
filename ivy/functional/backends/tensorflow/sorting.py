# global
import tensorflow as tf
from typing import Union, Optional

# local
import ivy

def argsort(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    direction = "DESCENDING" if descending else "ASCENDING"
    x = tf.convert_to_tensor(x)
    is_bool = x.dtype.is_bool
    if is_bool:
        x = tf.cast(x, tf.int32)
    ret = tf.argsort(x, axis=axis, direction=direction, stable=stable)
    return tf.cast(ret, dtype=tf.int64)


def sort(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    axis: int = -1,
    descending: bool = False,
    stable: bool = True,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    # TODO: handle stable sort when it's supported in tensorflow
    # currently it supports only quicksort (unstable)
    direction = "DESCENDING" if descending else "ASCENDING"
    x = tf.convert_to_tensor(x)
    is_bool = x.dtype.is_bool
    if is_bool:
        x = tf.cast(x, tf.int32)
    ret = tf.sort(x, axis=axis, direction=direction)
    if is_bool:
        ret = tf.cast(ret, dtype=tf.bool)
    return ret


def searchsorted(
    x: Union[tf.Tensor, tf.Variable],
    v: Union[tf.Tensor, tf.Variable],
    /,
    *,
    side="left",
    sorter=None,
    ret_dtype=tf.int64,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    if ivy.as_native_dtype(ret_dtype) not in [tf.int32, tf.int64]:
        raise ValueError("only int32 and int64 are supported for ret_dtype.")
    if sorter is not None:
        x = tf.gather(x, sorter)
    return tf.searchsorted(x, v, side=side, out_type=ret_dtype)
