# global
from ..random import *  # noqa: F401
import ivy
from ivy.func_wrapper import with_supported_dtypes
from ivy.functional.frontends.paddle.func_wrapper import (
    to_ivy_arrays_and_back,
)

from ivy.functional.frontends.paddle.random import normal
from ivy.functional.frontends.paddle.random import randint
# NOTE:
# Only inplace functions are to be added in this file.
# Please add non-inplace counterparts to `/frontends/paddle/random.py`.


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64")},
    "paddle",
)
@to_ivy_arrays_and_back
def exponential_(x, lam=1.0, name=None):
    return ivy.multiply(lam, ivy.exp(ivy.multiply(-lam, x)))


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64")},
    "paddle",
)
@to_ivy_arrays_and_back
def uniform_(x, min=-1.0, max=1.0, seed=0, name=None):
    x = ivy.array(x)
    return ivy.random_uniform(
        low=min, high=max, shape=x.shape, dtype=x.dtype, seed=seed
    )
    
def normal(x, mean=0.0, std=1.0, seed=0, name=None):
    x = ivy.array(x)
    return ivy.random_normal(mean=mean, stddev=std, shape=x.shape, dtype=x.dtype, seed=seed)


def randint(x, low=0, high=10, seed=0, name=None):
    x = ivy.array(x)
    return ivy.random.randint(low=low, high=high, shape=x.shape, dtype=x.dtype, seed=seed)