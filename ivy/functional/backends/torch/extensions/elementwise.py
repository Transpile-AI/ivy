from typing import Optional, Union, Tuple, Literal, List, Sequence
from numbers import Number
import ivy
from ivy.functional.ivy.extensions import (
    _verify_coo_components,
    _verify_csr_components,
    _is_data_not_indices_values_and_shape,
    _is_coo_not_csr,
)
from ivy.functional.backends.torch.elementwise import _cast_for_unary_op
import torch
import math


def lcm(
    x1: torch.Tensor,
    x2: torch.Tensor,
    /,
    *,
    dtype: Optional[torch.dtype] = None,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.abs(torch.lcm(x1, x2, out=out))


lcm.support_native_out = True


def fmod(
    x1: torch.Tensor,
    x2: torch.Tensor,
    /,
    *,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.fmod(x1, x2, out=None)


fmod.support_native_out = True
fmod.unsupported_dtypes = ("bfloat16",)


def fmax(
    x1: torch.Tensor,
    x2: torch.Tensor,
    /,
    *,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.fmax(x1, x2, out=None)


fmax.support_native_out = True


def sinc(x: torch.Tensor, /, *, out: Optional[torch.Tensor] = None) -> torch.Tensor:
    x = _cast_for_unary_op(x)
    return torch.sinc(x, out=out)


sinc.support_native_out = True
sinc.unsupported_dtypes = ("float16",)
