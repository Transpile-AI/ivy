# global
import numpy as _np
from typing import Tuple, Union

# local
from ivy import dtype_from_str, default_dtype

def min(x: _np.ndarray,
        axis: Union[int, Tuple[int]] = None,
        keepdims: bool = False) \
        -> _np.ndarray:
    return _np.amin(a = x, axis = axis, keepdims = keepdims)

def prod(x: _np.ndarray,
         axis: Union[int, Tuple[int]] = None,
         dtype: _np.dtype = None,
         keepdims: bool = False)\
        -> _np.ndarray:
    if x.dtype == _np.int8:
        dtype = _np.int32
    return _np.prod(a=x,axis=axis,dtype=dtype,keepdims=keepdims)