from typing import Optional, Union, Tuple, List
import numpy as np
import numpy.typing as npt

import ivy
from ivy import promote_types_of_inputs
from ivy.functional.backends.numpy.helpers import _scalar_output_to_0d_array
from ivy.func_wrapper import with_unsupported_dtypes
from . import backend_version


@_scalar_output_to_0d_array
@with_unsupported_dtypes({"1.23.0 and below": ("bfloat16",)}, backend_version)
def sinc(x: np.ndarray, /, *, out: Optional[np.ndarray] = None) -> np.ndarray:
    return np.sinc(x).astype(x.dtype)


@_scalar_output_to_0d_array
def lcm(
    x1: np.ndarray,
    x2: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    x1, x2 = promote_types_of_inputs(x1, x2)
    return np.abs(
        np.lcm(
            x1,
            x2,
            out=out,
        )
    )


lcm.support_native_out = True


@_scalar_output_to_0d_array
def fmod(
    x1: np.ndarray,
    x2: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    x1, x2 = promote_types_of_inputs(x1, x2)
    return np.fmod(
        x1,
        x2,
        out=None,
    )


fmod.support_native_out = True


@_scalar_output_to_0d_array
def fmax(
    x1: np.ndarray,
    x2: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    x1, x2 = promote_types_of_inputs(x1, x2)
    return np.fmax(
        x1,
        x2,
        out=None,
        where=True,
        casting="same_kind",
        order="K",
        dtype=None,
        subok=True,
    )


fmax.support_native_out = True


@_scalar_output_to_0d_array
def fmin(
    x1: np.ndarray,
    x2: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    x1, x2 = promote_types_of_inputs(x1, x2)
    return np.fmin(
        x1,
        x2,
        out=None,
        where=True,
        casting="same_kind",
        order="K",
        dtype=None,
        subok=True,
    )


fmin.support_native_out = True


@_scalar_output_to_0d_array
def trapz(
    y: np.ndarray,
    /,
    *,
    x: Optional[np.ndarray] = None,
    dx: Optional[float] = 1.0,
    axis: Optional[int] = -1,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.trapz(y, x=x, dx=dx, axis=axis)


trapz.support_native_out = False


@_scalar_output_to_0d_array
def float_power(
    x1: Union[np.ndarray, float, list, tuple],
    x2: Union[np.ndarray, float, list, tuple],
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    x1, x2 = promote_types_of_inputs(x1, x2)
    return np.float_power(x1, x2, out=out)


float_power.support_native_out = True


def exp2(
    x: Union[np.ndarray, float, list, tuple],
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.exp2(x, out=out)


exp2.support_native_out = True


@_scalar_output_to_0d_array
def copysign(
    x1: npt.ArrayLike,
    x2: npt.ArrayLike,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    x1, x2 = promote_types_of_inputs(x1, x2)
    if not ivy.is_float_dtype(x1):
        x1 = x1.astype(ivy.default_float_dtype(as_native=True))
        x2 = x2.astype(ivy.default_float_dtype(as_native=True))
    return np.copysign(x1, x2, out=out)


copysign.support_native_out = True


@_scalar_output_to_0d_array
def count_nonzero(
    a: np.ndarray,
    /,
    *,
    axis: Optional[Union[int, Tuple[int, ...]]] = None,
    keepdims: Optional[bool] = False,
    dtype: Optional[np.dtype] = None,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    if isinstance(axis, list):
        axis = tuple(axis)
    ret = np.count_nonzero(a, axis=axis, keepdims=keepdims)
    if np.isscalar(ret):
        return np.array(ret, dtype=dtype)
    return ret.astype(dtype)


count_nonzero.support_native_out = False


def nansum(
    x: np.ndarray,
    /,
    *,
    axis: Optional[Union[Tuple[int, ...], int]] = None,
    dtype: Optional[np.dtype] = None,
    keepdims: Optional[bool] = False,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    if isinstance(axis, list):
        axis = tuple(axis)
    return np.nansum(x, axis=axis, dtype=dtype, keepdims=keepdims, out=out)


nansum.support_native_out = True


def gcd(
    x1: Union[np.ndarray, int, list, tuple],
    x2: Union[np.ndarray, float, list, tuple],
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    x1, x2 = promote_types_of_inputs(x1, x2)
    return np.gcd(x1, x2, out=out)


gcd.support_native_out = True


def isclose(
    a: np.ndarray,
    b: np.ndarray,
    /,
    *,
    rtol: Optional[float] = 1e-05,
    atol: Optional[float] = 1e-08,
    equal_nan: Optional[bool] = False,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    ret = np.isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)
    if np.isscalar(ret):
        return np.array(ret, dtype=np.bool)
    return ret


isclose.support_native_out = False


def angle(
    z: np.ndarray,
    /,
    *,
    deg: Optional[bool] = False,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:

    return np.angle(z, deg=deg)


angle.support_native_out = False


def imag(
    val: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:

    return np.imag(val)


imag.support_native_out = False


def nan_to_num(
    x: np.ndarray,
    /,
    *,
    copy: Optional[bool] = True,
    nan: Optional[Union[float, int]] = 0.0,
    posinf: Optional[Union[float, int]] = None,
    neginf: Optional[Union[float, int]] = None,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.nan_to_num(x, copy=copy, nan=nan, posinf=posinf, neginf=neginf)


nan_to_num.support_native_out = False


def logaddexp2(
    x1: Union[np.ndarray, int, list, tuple],
    x2: Union[np.ndarray, int, list, tuple],
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    x1, x2 = promote_types_of_inputs(x1, x2)
    if not ivy.is_float_dtype(x1):
        x1 = x1.astype(ivy.default_float_dtype(as_native=True))
        x2 = x2.astype(ivy.default_float_dtype(as_native=True))
    return np.logaddexp2(x1, x2, out=out)


logaddexp2.support_native_out = True


def signbit(
    x: Union[np.ndarray, float, int, list, tuple],
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.signbit(x, out=out)


signbit.support_native_out = True


def hypot(
    x1: np.ndarray,
    x2: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.hypot(x1, x2)


def diff(
    x: Union[np.ndarray, list, tuple],
    /,
    *,
    n: int = 1,
    axis: int = -1,
    prepend: Optional[Union[np.ndarray, int, float, list, tuple]] = None,
    append: Optional[Union[np.ndarray, int, float, list, tuple]] = None,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    prepend = prepend if prepend is not None else np._NoValue
    append = append if append is not None else np._NoValue
    return np.diff(x, n=n, axis=axis, prepend=prepend, append=append)


diff.support_native_out = False


@_scalar_output_to_0d_array
def allclose(
    x1: np.ndarray,
    x2: np.ndarray,
    /,
    *,
    rtol: Optional[float] = 1e-05,
    atol: Optional[float] = 1e-08,
    equal_nan: Optional[bool] = False,
    out: Optional[np.ndarray] = None,
) -> bool:
    return np.allclose(x1, x2, rtol=rtol, atol=atol, equal_nan=equal_nan)


allclose.support_native_out = False


def fix(
    x: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.fix(x, out=out)


fix.support_native_out = True


def nextafter(
    x1: np.ndarray,
    x2: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    return np.nextafter(x1, x2)


nextafter.support_natvie_out = True


def zeta(
    x: np.ndarray,
    q: np.ndarray,
    /,
    *,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    temp = np.logical_and(np.greater(x, 0), np.equal(np.remainder(x, 2), 0))
    temp = np.logical_and(temp, np.less_equal(q, 0))
    temp = np.logical_and(temp, np.equal(np.remainder(q, 1), 0))
    inf_indices = np.logical_or(temp, np.equal(x, 1))
    temp = np.logical_and(np.not_equal(np.remainder(x, 2), 0), np.greater(x, 1))
    temp = np.logical_and(temp, np.less_equal(q, 0))
    nan_indices = np.logical_or(temp, np.less(x, 1))
    n, res = 1, 1 / q**x
    while n < 10000:
        term = 1 / (q + n) ** x
        n, res = n + 1, res + term
    ret = np.round(res, decimals=4)
    ret[nan_indices] = np.nan
    ret[inf_indices] = np.inf
    return ret


zeta.support_native_out = False


def gradient(
    x: np.ndarray,
    /,
    *,
    spacing: Optional[Union[int, list, tuple]] = 1,
    axis: Optional[Union[int, list, tuple]] = None,
    edge_order: Optional[int] = 1,
) -> Union[np.ndarray, List[np.ndarray]]:
    if type(spacing) in (int, float):
        return np.gradient(x, spacing, axis=axis, edge_order=edge_order)
    return np.gradient(x, *spacing, axis=axis, edge_order=edge_order)


def xlogy(
    x: np.ndarray, y: np.ndarray, /, *, out: Optional[np.ndarray] = None
) -> np.ndarray:
    x, y = promote_types_of_inputs(x, y)
    if (x == 0).all():
        return 0.0
    else:
        return x * np.log(y)


def real(x: np.ndarray, /, *, out: Optional[np.ndarray] = None) -> np.ndarray:
    return np.real(x)
