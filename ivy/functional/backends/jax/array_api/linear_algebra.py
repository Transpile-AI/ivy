# global
import jax.numpy as jnp
from typing import Union, Optional, Tuple, Literal
from collections import namedtuple

# local
from ivy import inf
from ivy.functional.backends.jax import JaxArray
import ivy as _ivy


# noinspection PyUnusedLocal,PyShadowingBuiltins
def vector_norm(x: JaxArray,
                axis: Optional[Union[int, Tuple[int]]] = None, 
                keepdims: bool = False,
                ord: Union[int, float, Literal[inf, -inf]] = 2)\
        -> JaxArray:

    if axis is None:
        jnp_normalized_vector = jnp.linalg.norm(jnp.ravel(x), ord, axis, keepdims)
    else:
        jnp_normalized_vector = jnp.linalg.norm(x, ord, axis, keepdims)

    if jnp_normalized_vector.shape == ():
        return jnp.expand_dims(jnp_normalized_vector, 0)
    return jnp_normalized_vector

def svd(x:JaxArray,full_matrices: bool = True) -> Union[JaxArray, Tuple[JaxArray,...]]:
    results=namedtuple("svd", "U S Vh")
    results=jnp.linalg.svd(x, full_matrices=full_matrices)
    return results