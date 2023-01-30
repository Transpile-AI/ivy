import numpy as np
import ivy
from ivy.functional.frontends.numpy.func_wrapper import (
    to_ivy_arrays_and_back,
    from_zero_dim_arrays_to_scalar,
)



@to_ivy_arrays_and_back
@from_zero_dim_arrays_to_scalar
def quantile(a, q, axis=None, out=None, overwrite_input=False, method='linear', keepdims=False, *, interpolation=None):
    
    # handle axis
    if axis is None:
        axis = tuple(range(len(a.shape)))
    axis = (axis,) if isinstance(axis, int) else tuple(axis)

    # Handle if size is zero 
    if a.size == 0:
        return np.asarray(float("nan"))

    a = ivy.astype(a, ivy.float64)

    return ivy.quantile(a, q,  axis=axis, keepdims=keepdims , interpolation='linear', out=out)

@to_ivy_arrays_and_back
@from_zero_dim_arrays_to_scalar
def percentile(a, q, axis=None, out=None, overwrite_input=False, method='linear', keepdims=False, *, interpolation=None):
    ## samething as quantile, just need to change the quantile into a percentile 

    q /= 100
    
    # handle axis
    if axis is None:
        axis = tuple(range(len(a.shape)))
    axis = (axis,) if isinstance(axis, int) else tuple(axis)

    # Handle if size is zero 
    if a.size == 0:
        return np.asarray(float("nan"))

    a = ivy.astype(a, ivy.float64)

    return ivy.quantile(a, q,  axis=axis, keepdims=keepdims , interpolation='linear', out=out)

    








    


