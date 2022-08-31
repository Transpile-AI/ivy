import ivy
from ivy.func_wrapper import from_zero_dim_arrays_to_float


@from_zero_dim_arrays_to_float
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
         signature=None,
         extobj=None,
):
    if dtype:
        x = ivy.astype(ivy.array(x), ivy.as_ivy_dtype(dtype))
    ret = ivy.multiply(ivy.divide(x, ivy.pi), 180, out=out)
    if ivy.is_array(where):
        ret = ivy.where(where, ret, ivy.default(out, ivy.zeros_like(ret)), out=out)
    return ret
