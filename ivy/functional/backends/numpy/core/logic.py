"""
Collection of Numpy logic functions, wrapped to fit Ivy syntax and signature.
"""

# global
import numpy as _np

logical_and = _np.logical_and
logical_or = _np.logical_or


def logical_not(x: _np.ndarray) -> _np.ndarray:
    return _np.logical_not(x)
