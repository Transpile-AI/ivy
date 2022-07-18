"""Collection of Numpy random functions, wrapped to fit Ivy syntax and signature."""

# global
import numpy as np
from typing import Optional, Union, Tuple, Sequence
import ivy

# localf


# Extra #
# ------#


def random_uniform(
    low: Union[float] = 0.0,
    high: Union[float] = 1.0,
    shape: Optional[Union[int, Tuple[int, ...]]] = None,
    *,
    device: str,
    dtype = None,
) -> np.ndarray:

    if isinstance(low, (np.ndarray, ivy.Array)):
        low = float(low)
    if isinstance(low, tuple):
        low = float(low[0])
    if isinstance(high, (np.ndarray, ivy.Array)):
        high = float(high)
    if isinstance(high, tuple):
        high = float(high[0])

    if isinstance(shape, (np.ndarray, ivy.Array)):
        if shape.size <= 1:
            shape = int(shape)
        else:
            new_shape = []
            for i in shape:
                new_shape.append(int(i))
            shape = new_shape

    #return np.asarray(np.random.uniform(low, high, shape), dtype=dtype)
    return np.random.uniform(low, high, shape)


def random_normal(
    mean: float = 0.0,
    std: float = 1.0,
    shape: Optional[Union[int, Tuple[int, ...]]] = None,
    *,
    device: str,
) -> np.ndarray:
    return np.asarray(np.random.normal(mean, std, shape))


def multinomial(
    population_size: int,
    num_samples: int,
    batch_size: int = 1,
    probs: Optional[np.ndarray] = None,
    replace=True,
    *,
    device: str,
    out: Optional[np.ndarray] = None,
) -> np.ndarray:
    if probs is None:
        probs = (
            np.ones(
                (
                    batch_size,
                    population_size,
                )
            )
            / population_size
        )
    orig_probs_shape = list(probs.shape)
    num_classes = orig_probs_shape[-1]
    probs_flat = np.reshape(probs, (-1, orig_probs_shape[-1]))
    probs_flat = probs_flat / np.sum(
        probs_flat, -1, keepdims=True, dtype="float64", out=out
    )
    probs_stack = np.split(probs_flat, probs_flat.shape[0])
    samples_stack = [
        np.random.choice(num_classes, num_samples, replace, p=prob[0])
        for prob in probs_stack
    ]
    samples_flat = np.stack(samples_stack, out=out)
    return np.asarray(np.reshape(samples_flat, orig_probs_shape[:-1] + [num_samples]))


def randint(
    low: int, high: int, shape: Union[int, Sequence[int]], *, device: str
) -> np.ndarray:
    return np.random.randint(low, high, shape)


def seed(seed_value: int = 0) -> None:
    np.random.seed(seed_value)


def shuffle(x: np.ndarray) -> np.ndarray:
    return np.random.permutation(x)
