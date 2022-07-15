"""Collection of PyTorch activation functions, wrapped to fit Ivy syntax and
signature.
"""
from typing import Optional

# global
import numpy as np
import torch
import torch.nn

# local


def relu(x: torch.Tensor) -> torch.Tensor:
    return torch.relu(x)


def leaky_relu(
    x: torch.Tensor,
    alpha: Optional[float] = 0.2,
) -> torch.Tensor:
    return torch.nn.functional.leaky_relu(x, alpha)


def gelu(
    x: torch.Tensor,
    approximate: bool = True,
) -> torch.Tensor:
    if approximate:
       return 0.5 * x * (1 + torch.tanh(((2 / np.pi) ** 0.5) * (x + 0.044715 * x ** 3)))
    return torch.nn.functional.gelu(x)
   

def tanh(x: torch.Tensor, out: Optional[torch.Tensor] = None) -> torch.Tensor:
    return torch.tanh(x, out=out)


def sigmoid(x: torch.Tensor, out: Optional[torch.Tensor] = None) -> torch.Tensor:
    return torch.sigmoid(x, out=out)


def softmax(
    x: torch.Tensor, axis: Optional[int] = None
) -> torch.Tensor:
    exp_x = torch.exp(x)
    return exp_x / torch.sum(exp_x, axis, keepdims=True)


def softplus(x: torch.Tensor) -> torch.Tensor:
    return torch.nn.functional.softplus(x)
