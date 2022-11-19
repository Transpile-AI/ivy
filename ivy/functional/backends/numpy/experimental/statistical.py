from typing import Optional, Union, Tuple, Sequence
import numpy as np
import ivy


def median(
    input: np.ndarray,
    /,
    *,
    axis: Optional[Union[Tuple[int], int]] = None,
    keepdims: Optional[bool] = False,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.median(
        input,
        axis=axis,
        keepdims=keepdims,
        out=out,
    )


def nanmean(
    a: np.ndarray,
    /,
    *,
    axis: Optional[Union[int, Tuple[int]]] = None,
    keepdims: Optional[bool] = False,
    dtype: Optional[np.dtype] = None,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.nanmean(a, axis=axis, keepdims=keepdims, dtype=dtype, out=out)


nanmean_support_native_out = True


def unravel_index(
    indices: np.ndarray,
    shape: Tuple[int],
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.unravel_index(indices, shape)


def quantile(
    a: np.ndarray,
    q: Union[float, np.ndarray],
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    interpolation: str = 'linear',
    out : Optional[np.ndarray] = None 
) -> np.ndarray:
    a, q = ivy.promote_types_of_inputs(a, q)
    tuple(axis) if isinstance(axis, list) else axis
    return np.quantile(
        a,
        q,
        axis=axis,
        method=interpolation,
        keepdims=keepdims,
        out=out
    ).astype('float64')
