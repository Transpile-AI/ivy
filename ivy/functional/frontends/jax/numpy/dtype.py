# local
import ivy
from ivy.functional.frontends.jax.func_wrapper import to_ivy_arrays_and_back
from ivy.functional.frontends.jax.numpy import (
    jax_numpy_casting_table,
    promote_types_jax,
)
from ivy.functional.frontends.numpy import dtype as np_dtype


@to_ivy_arrays_and_back
def can_cast(from_, to, casting="safe"):
    """
    Returns True if casting betweer two dtypes is possible according to casting rules,
    False otherwise.
    """
    ivy.assertions.check_elem_in_list(
        casting,
        ["no", "equiv", "safe", "same_kind", "unsafe"],
        message="casting must be one of [no, equiv, safe, same_kind, unsafe]",
    )

    if ivy.is_array(from_):
        from_ = ivy.as_ivy_dtype(from_.dtype)
    elif isinstance(from_, (str, type)):
        from_ = ivy.as_ivy_dtype(from_)
    elif isinstance(from_, np_dtype):
        from_ = from_._ivy_dtype
    else:
        raise ivy.exceptions.IvyException(
            "from_ must be one of dtype, dtype specifier, scalar type, or array, "
        )

    if isinstance(to, (str, type)):
        to = ivy.as_ivy_dtype(to)
    elif isinstance(to, np_dtype):
        to = to._ivy_dtype
    else:
        raise ivy.exceptions.IvyException("to must be one of dtype, or dtype specifier")

    if casting == "no" or casting == "equiv":
        return from_ == to

    if casting == "safe":
        return to in jax_numpy_casting_table[from_]

    if casting == "same_kind":
        if from_ == to or "bool" in from_:
            return True
        elif ivy.is_int_dtype(from_) and ivy.is_float_dtype(to):
            return True
        elif ivy.is_float_dtype(from_) and ivy.is_float_dtype(to):
            if "bfloat" in from_ and "bfloat" in to:
                return True
            elif "bfloat" in from_ and "float16" in to:
                return False
            return True

        elif ivy.is_uint_dtype(from_) and (
            ivy.is_int_dtype(to) or ivy.is_float_dtype(to)
        ):
            return True
        elif (
            ivy.is_int_dtype(from_)
            and ivy.is_int_dtype(to)
            and not ivy.is_uint_dtype(to)
        ):
            return True
        else:
            return to in jax_numpy_casting_table[from_]
    if casting == "unsafe":
        return True
    return False


def promote_types(type1, type2, /):
    if isinstance(type1, np_dtype):
        type1 = type1._ivy_dtype
    if isinstance(type2, np_dtype):
        type2 = type2._ivy_dtype
    return np_dtype(promote_types_jax(type1, type2))
