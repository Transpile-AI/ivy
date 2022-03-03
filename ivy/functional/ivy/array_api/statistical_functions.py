# global
from typing import Union, Optional, Tuple, List

# local
import ivy
from ivy.framework_handler import current_framework as _cur_framework


def var(x: Union[ivy.Array, ivy.NativeArray],
        axis: Optional[Union[int, Tuple[int], List[int]]] = None,
        correction: Union[int, float] = 0.0,
        keepdims: bool = False) \
        -> ivy.Array:
    """
    Calculates the variance of the input array x.
    :param x: input array
    :param axis: axis or axes along which variances must be computed. By default, the variance must be computed over the entire array
    :param correction: degrees of freedom adjustment
    :param keepdims: Default: False
    :return: The returned array must have the same data type as x.
    """
    return _cur_framework(x).var(x, axis, correction, keepdims)
