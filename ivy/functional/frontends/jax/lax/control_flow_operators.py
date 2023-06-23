# global
import ivy
from ivy.functional.frontends.jax.func_wrapper import to_ivy_arrays_and_back
from typing import Callable, Optional, List, Union
import numpy as np


@to_ivy_arrays_and_back
def cond(pred, true_fun, false_fun, *operands, operand=None, linear=None):
    if operand is not None:
        if operands:
            raise ivy.utils.exceptions.IvyException(
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
            raise ivy.utils.exceptions.IvyException(
                "if `operand` is passed, positional `operands` should not be passed"
            )
        operands = (operand,)

    index = max(index, 0)
    index = min(len(branches) - 1, index)
    return branches[index](*operands)


@to_ivy_arrays_and_back
def fori_loop(lower, upper, body_fun, init_val):
    if not (callable(body_fun)):
        raise ivy.exceptions.IvyException(
            "jax.lax.fori_loop: Argument body_fun should be callable."
        )
    val = init_val
    for i in range(lower, upper):
        val = body_fun(i, val)
    return val


@to_ivy_arrays_and_back
def while_loop(cond_fun, body_fun, init_val):
    if not (callable(body_fun) and callable(cond_fun)):
        raise ivy.exceptions.IvyException(
            "jax.lax.while_loop: Arguments body_fun and cond_fun should be callable."
        )
    val = init_val
    while cond_fun(val):
        val = body_fun(val)
    return val


# @to_ivy_arrays_and_back
# def scan(f, init, xs, length=None, reverse=False, unroll=1):
#     if xs is None:
#         xs = [None] * length
#     carry = init
#     ys = []
#     for x in xs:
#         carry, y = f(carry, x)
#         ys.append(y)
#     return carry, ivy.stack(ys)


# @to_ivy_arrays_and_back
# def scan(
#     f: Callable[[Carry, X], Tuple[Carry, Y]],
#     init: Carry,
#     xs: X,
#     length: Optional[int] = None,
#     reverse: bool = False,
#     unroll: int = 1,
# ) -> Tuple[Carry, Y]:
#     if xs is None:
#         xs = [None] * length

#     if reverse:
#         xs = xs[::-1]

#     carry = init
#     ys = []

#     for _ in range(unroll):
#         for x in xs:
#             carry, y = f(carry, x)
#             ys.append(y)

#     return carry, ivy.stack(ys)


# @to_ivy_arrays_and_back
# def scan(
#     f: Callable[[Carry, X], Tuple[Carry, Y]],
#     init: Carry,
#     xs: X,
#     length: Optional[int] = None,
#     reverse: bool = False,
#     unroll: int = 1,
# ) -> Tuple[Carry, Y]:
#     if xs is None:
#         xs = [None] * length

#     if reverse:
#         xs = xs[::-1]

#     carry = init
#     ys = []

#     if length is None:
#         length = len(xs[0]) if isinstance(xs[0], np.ndarray) else len(xs)

#     for _ in range(length):
#         for _ in range(unroll):
#             for x in xs:
#                 carry, y = f(carry, x)
#                 ys.append(y)

#     return carry, ivy.stack(ys)


# @to_ivy_arrays_and_back
# def scan(
#     f: Callable[[X], Y],
#     init: X,
#     xs: X,
#     length: Optional[int] = None,
#     reverse: bool = False,
#     unroll: int = 1,
# ) -> Y:
#     if xs is None:
#         xs = [None] * length

#     if reverse:
#         xs = xs[::-1]

#     ys = []

#     if length is None:
#         length = len(xs[0]) if isinstance(xs[0], np.ndarray) else len(xs)

#     for _ in range(length):
#         for _ in range(unroll):
#             for x in xs:
#                 y = f(x)
#                 ys.append(y)

#     return ivy.stack(ys)




# @to_ivy_arrays_and_back
# def scan(f, init, xs, length=None, reverse=False, unroll=1):
#     if xs is None:
#         xs = [None] * length

#     if reverse:
#         xs = xs[::-1]

#     ys = []

#     if length is None:
#         length = len(xs[0]) if isinstance(xs[0], ivy.ndarray) else len(xs)

#     for _ in range(length):
#         carry = init
#         for _ in range(unroll):
#             for x in xs:
#                 carry = f(x)
#                 ys.append(carry)

#     return ivy.stack(ys)


@to_ivy_arrays_and_back
def scan(f, init, xs, length=None, reverse=False, unroll=1):
    if length is None:
        length = len(xs[0]) if isinstance(xs[0], ivy.ndarray) else len(xs)

    if reverse:
        xs = xs[::-1]

    ys = []
    carry = init
    for x in xs:
        for _ in range(unroll):
            carry = f(carry)
            ys.append(carry)

    return ivy.stack(ys)
