# global
import ivy
from ivy.functional.frontends.jax.func_wrapper import to_ivy_arrays_and_back


@to_ivy_arrays_and_back
def cond(pred, true_fun, false_fun, *operands, operand=None, linear=None):
    if operand is not None:
        if operands:
            raise ivy.exceptions.IvyException(
                "if `operand` is passed, positional `operands` should not be passed"
            )
        operands = (operand,)

    if pred:
        return true_fun(*operands)
    return false_fun(*operands)


@to_ivy_arrays_and_back
def map(f, xs):
    return ivy.stack([f(x) for x in xs])


@to_ivy_arrays_and_back
def switch(index, branches, *operands, operand=None):
    if operand is not None:
        if operands:
            raise ivy.exceptions.IvyException(
                "if `operand` is passed, positional `operands` should not be passed"
            )
        operands = (operand,)

    index = max(index, 0)
    index = min(len(branches) - 1, index)
    return branches[index](*operands)


@to_ivy_arrays_and_back
def while_loop(cond_fun, body_fun, init_val):
    if not (callable(body_fun) and callable(cond_fun)):
        raise ivy.exceptions.IvyException(
            "lax.while_loop: body_fun and cond_fun arguments should be callable."
        )

    val = init_val

    while cond_fun(val):
        val = body_fun(val)
    return val
