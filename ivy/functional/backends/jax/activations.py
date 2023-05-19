"""Collection of Jax activation functions, wrapped to fit Ivy syntax and signature."""


# global


import jax
import jax.numpy as jnp
from typing import Optional, Union

# local
from ivy.func_wrapper import with_unsupported_dtypes
from . import backend_version
from ivy.functional.backends.jax import JaxArray



@with_unsupported_dtypes({"0.4.10 and below": ("complex",)}, backend_version)

def gelu(
    x: JaxArray,
    /,
    *,
    approximate: bool = False,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    return jax.nn.gelu(x, approximate)


def leaky_relu(
    x: JaxArray, /, *, alpha: float = 0.2, out: Optional[JaxArray] = None
) -> JaxArray:
    return jnp.asarray(jnp.where(x > 0, x, jnp.multiply(x, alpha)), x.dtype)


def relu(x: JaxArray, /, *, out: Optional[JaxArray] = None) -> JaxArray:
    return jnp.maximum(x, 0)


def sigmoid(x: JaxArray, /, *, out: Optional[JaxArray] = None) -> JaxArray:
    return 1 / (1 + jnp.exp(-x))


def softmax(
    x: JaxArray, /, *, axis: Optional[int] = None, out: Optional[JaxArray] = None
) -> JaxArray:
    if axis is None:
        axis = -1
    return jax.nn.softmax(x, axis)


def softplus(
    x: JaxArray,
    /,
    *,
    beta: Optional[Union[int, float]] = None,
    threshold: Optional[Union[int, float]] = None,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    if beta is not None and beta != 1:
        x_beta = x * beta
        res = (
            jnp.add(
                jnp.log1p(jnp.exp(-jnp.abs(x_beta))),
                jnp.maximum(x_beta, 0).astype(x.dtype),
            )
        ) / beta
    else:
        x_beta = x
        res = jnp.add(
            jnp.log1p(jnp.exp(-jnp.abs(x_beta))),
            jnp.maximum(x_beta, 0).astype(x.dtype),
        )
    if threshold is not None:
        return jnp.where(x_beta > threshold, x, res).astype(x.dtype)
    return res.astype(x.dtype)


def log_softmax(
    x: JaxArray, /, *, axis: Optional[int] = None, out: Optional[JaxArray] = None
):
    if axis is None:
        axis = -1
    return jax.nn.log_softmax(x, axis)


def mish(x: JaxArray, /, *, out: Optional[JaxArray] = None):
    return x * jnp.tanh(jax.nn.softplus(x))
