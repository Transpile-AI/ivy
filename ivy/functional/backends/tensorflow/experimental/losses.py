import tensorflow as tf
import math
from typing import Optional
from ivy.func_wrapper import (
    with_unsupported_dtypes,
    with_supported_device_and_dtypes,
)
from . import backend_version


@with_unsupported_dtypes({"2.14.0 and below": "bool"}, backend_version)
def huber_loss(
    input: tf.Tensor,
    target: tf.Tensor,
    /,
    *,
    delta: Optional[float] = 1.0,
    reduction: Optional[str] = "mean",
) -> tf.Tensor:
    abs_diff = tf.abs(input - target)
    quadratic_loss = 0.5 * (abs_diff**2)
    linear_loss = delta * (abs_diff - 0.5 * delta)
    loss = tf.where(abs_diff <= delta, quadratic_loss, linear_loss)

    if reduction == "sum":
        return tf.sum(loss)
    elif reduction == "mean":
        return tf.mean(loss)
    else:
        return loss


@with_unsupported_dtypes({"2.14.0 and below": "bool"}, backend_version)
def smooth_l1_loss(
    input: tf.Tensor,
    target: tf.Tensor,
    /,
    *,
    beta: Optional[float] = 1.0,
    reduction: Optional[str] = "mean",
) -> tf.Tensor:
    diff = tf.abs(input - target)
    loss = tf.where(diff < beta, 0.5 * diff**2 / beta, diff - 0.5 * beta)

    if reduction == "mean":
        return tf.reduce_mean(loss)
    elif reduction == "sum":
        return tf.reduce_sum(loss)
    else:
        return loss


@with_unsupported_dtypes({"2.14.0 and below": "bool"}, backend_version)
def soft_margin_loss(
    input: tf.Tensor,
    target: tf.Tensor,
    /,
    *,
    reduction: Optional[str] = "mean",
) -> tf.Tensor:
    loss = tf.reduce_sum(tf.math.log1p(tf.exp(-input * target))) / tf.size(input)

    if reduction == "sum":
        return tf.reduce_sum(loss)
    elif reduction == "mean":
        return tf.reduce_mean(loss)
    else:
        return loss


def _apply_loss_reduction(loss: tf.Tensor, reduction: str, axis=None) -> tf.Tensor:
    if reduction == "sum":
        return tf.math.reduce_sum(loss, axis=axis)
    elif reduction == "mean":
        return tf.reduce_mean(loss, axis=axis)
    else:  # reduction == "none"
        return loss


def _validate_poisson_nll_params(
    input,
    label,
    epsilon,
    reduction,
    allowed_dtypes=[tf.float32, tf.float64],
):
    # Validate dtypes
    for parameter, name in zip([input, label], ["input", "label"]):
        if parameter.dtype not in allowed_dtypes:
            raise ValueError(
                "The dtype of '%s' in poisson_nll_loss should be one of %s, but"
                " received %s." % (name, allowed_dtypes, parameter.dtype)
            )

    # Validate epsilon
    if epsilon <= 0:
        raise ValueError(
            "The value of `epsilon` in poisson_nll_loss should be positive, but"
            " received %f, which is not allowed" % epsilon
        )

    # Validate reduction
    if reduction not in ["sum", "mean", "none"]:
        raise ValueError(
            "The value of 'reduction' in poisson_nll_loss should be 'sum', 'mean' or"
            " 'none', but received %s, which is not allowed." % reduction
        )

    # Validate shape
    if input.shape != label.shape:
        raise ValueError(
            "The shape of 'input' (%s) must be the same as the shape of 'label' (%s)."
            % (input.shape, label.shape)
        )

    return True


@with_supported_device_and_dtypes(
    {
        "2.14.0 and below": {
            "cpu": ("float32", "float64"),
            "gpu": ("float32", "float64"),
        }
    },
    backend_version,
)
def poisson_nll_loss(
    input: tf.Tensor,
    target: tf.Tensor,
    *,
    log_input: bool = True,
    full: bool = False,
    eps: float = 1e-8,
    reduction: str = "mean",
) -> tf.Tensor:
    input_tensor = tf.constant(input, dtype=input.dtype)
    target_tensor = tf.constant(target, dtype=input.dtype)

    _validate_poisson_nll_params(input_tensor, target_tensor, eps, reduction)
    if log_input:
        loss = tf.math.exp(input_tensor) - target_tensor * input_tensor
    else:
        loss = input_tensor - target_tensor * tf.math.log(input_tensor + eps)
    if full:
        point_five = tf.constant(0.5, dtype=target_tensor.dtype)
        two_pi = tf.constant(2 * math.pi, dtype=target_tensor.dtype)

        stirling_approx = (
            (target_tensor * tf.math.log(target_tensor))
            - target_tensor
            + (point_five * tf.math.log(two_pi * target_tensor))
        )
        zeros = tf.zeros_like(target_tensor, dtype=target_tensor.dtype)
        ones = tf.ones_like(target_tensor, dtype=target_tensor.dtype)
        cond = tf.math.logical_and(target_tensor >= zeros, target_tensor <= ones)
        loss = loss + tf.where(cond, zeros, stirling_approx)
    return _apply_loss_reduction(loss, reduction)


@with_supported_device_and_dtypes(
    {
        "2.14.0 and below": {
            "cpu": ("float32", "float64"),
            "gpu": ("float32", "float64"),
        }
    },
    backend_version,
)
def multilabel_margin_loss(
    input: tf.Tensor,
    target: tf.Tensor,
    /,
    *,
    reduction: str = "none",
    margin: float = 1.0,
) -> tf.Tensor:
    """
    Compute the multilabel margin loss.

    Parameters
    ----------
    input : tf.Tensor
        The input tensor.
    target : tf.Tensor
        The target tensor.
    reduction : str, optional
        The reduction method for the loss, by default "none".
    margin : float, optional
        The margin value for the loss, by default 1.0.

    Returns
    -------
    tf.Tensor
        The computed loss tensor.
    """
    input_tensor = tf.convert_to_tensor(input, dtype=input.dtype)
    target_tensor = tf.convert_to_tensor(target, dtype=input.dtype)

    if input.shape != target.shape:
        raise ValueError("Input and target tensors must have matching shapes.")

    loss = tf.reduce_sum(
        tf.maximum(0.0, margin - (input_tensor[target_tensor] - input_tensor))
    ) / tf.cast(tf.size(input_tensor), tf.float32)

    if reduction not in ["none", "sum", "mean"]:
        raise ValueError(
            "Invalid reduction value. Allowed values are 'none', 'sum', 'mean'."
        )

    return _apply_loss_reduction(loss, reduction=reduction)
