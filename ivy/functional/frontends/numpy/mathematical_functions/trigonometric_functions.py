# global
import ivy

# local
from ivy.func_wrapper import from_zero_dim_arrays_to_float
from ivy.functional.frontends.numpy.func_wrapper import to_ivy_arrays_and_back


@from_zero_dim_arrays_to_float
@to_ivy_arrays_and_back
def cos(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="k",
    dtype=None,
    subok=True,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.cos(x, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@from_zero_dim_arrays_to_float
@to_ivy_arrays_and_back
def sin(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="k",
    dtype=None,
    subok=True,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.sin(x, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@from_zero_dim_arrays_to_float
@to_ivy_arrays_and_back
def tan(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.tan(x, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@from_zero_dim_arrays_to_float
@to_ivy_arrays_and_back
def arcsin(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.asin(x, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@from_zero_dim_arrays_to_float
@to_ivy_arrays_and_back
def arccos(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.acos(x, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@from_zero_dim_arrays_to_float
@to_ivy_arrays_and_back
def arctan(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.atan(x, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@from_zero_dim_arrays_to_float
@to_ivy_arrays_and_back
def deg2rad(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
    signature=None,
    extobj=None,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.deg2rad(x, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret


@from_zero_dim_arrays_to_float
@to_ivy_arrays_and_back
def rad2deg(
    x,
    /,
    out=None,
    *,
    where=True,
    casting="same_kind",
    order="K",
    dtype=None,
    subok=True,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.rad2deg(x, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret
