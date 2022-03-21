"""
Collection of PyTorch general functions, wrapped to fit Ivy syntax and signature.
"""

# global
import ivy
import numpy as np
torch_scatter = None
import math as _math
import torch as torch
from operator import mul
from torch.types import Number
from functools import reduce as _reduce
from ivy.functional.backends.torch import linspace
from typing import List, Dict, Optional, Union


# local
from ivy.functional.ivy.old import default_dtype
from ivy.functional.ivy.device import default_device
from ivy.functional.backends.torch.device import dev_from_str, _callable_dev


def is_array(x, exclusive=False):
    if isinstance(x, torch.Tensor):
        if exclusive and x.requires_grad:
            return False
        return True
    return False


def copy_array(x):
    return x.clone()


def array_equal(x0, x1):
    return torch.equal(x0, x1)


def to_numpy(x) -> np.ndarray:
    if isinstance(x, np.ndarray) or isinstance(x, (float, int, bool)):
        return x
    elif torch.is_tensor(x):
        return x.detach().cpu().numpy()
    raise ValueError('Expected a pytroch tensor.')


def to_scalar(x) -> Union[float, int, bool]:
    if isinstance(x, (float, int)):
        return x
    return x.item()


def to_list(x):
    if isinstance(x, np.ndarray):
        return x.tolist()
    elif torch.is_tensor(x):
        return x.detach().cpu().tolist()
    raise ValueError('Expected a pytroch tensor.')


def floormod(x, y):
    return x % y


def unstack(x, axis: int, keepdims: bool = False) -> List[torch.Tensor]:
    if x.shape == ():
        return [x]
    ret = list(torch.unbind(x, axis))
    if keepdims:
        return [r.unsqueeze(axis) for r in ret]
    return ret


def container_types():
    return []


def inplace_update(x, val):
    x.data = val
    return x


inplace_arrays_supported = lambda: True
inplace_variables_supported = lambda: True



def inplace_decrement(x, val):
    x.data -= val
    return x


def inplace_increment(x, val):
    x.data += val
    return x


def cumsum(x, axis: int = 0):
    return torch.cumsum(x, axis)


def cumprod(x, axis: int = 0, exclusive: bool = False):
    if exclusive:
        x = torch.transpose(x, axis, -1)
        x = torch.cat((torch.ones_like(x[..., -1:]), x[..., :-1]), -1)
        res = torch.cumprod(x, -1)
        return torch.transpose(res, axis, -1)
    return torch.cumprod(x, axis)
