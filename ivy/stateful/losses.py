"""Collection of Ivy's losses as stateful classes."""

# local
import ivy
from ivy.stateful.module import Module


class LogPoissonLoss(Module):
    def __init__(
        self,
        *,
        compute_full_loss: bool = False,
        axis: int = -1,
        reduction: str = "none",
    ):
        self._compute_full_loss = compute_full_loss
        self._axis = axis
        self._reduction = reduction
        Module.__init__(self)

    def _forward(
        self, true, pred, *, compute_full_loss=None, axis=None, reduction=None
    ):
        """
        Perform forward pass of the Log Poisson Loss.

        true
            input array containing true labels.
        pred
            input array containing Predicted labels.
        compute_full_loss
            whether to compute the full loss. If false, a constant term is dropped
            in favor of more efficient optimization. Default: ``False``.
        axis
            the axis along which to compute the log-likelihood loss. If axis is ``-1``,
            the log-likelihood loss will be computed along the last dimension.
            Default: ``-1``.
        reduction
            ``'none'``: No reduction will be applied to the output.
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed. Default: ``'none'``.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The binary log-likelihood loss between the given distributions.
        """
        return ivy.log_poisson_loss(
            true,
            pred,
            compute_full_loss=ivy.default(compute_full_loss, self._compute_full_loss),
            axis=ivy.default(axis, self._axis),
            reduction=ivy.default(reduction, self._reduction),
        )


class CrossEntropyLoss(Module):
    def __init__(
        self,
        *,
        axis: int = -1,
        epsilon: float = 1e-7,
        reduction: str = "sum",
    ):
        self._axis = axis
        self._epsilon = epsilon
        self._reduction = reduction
        Module.__init__(self)

    def _forward(self, true, pred, *, axis=None, epsilon=None, reduction=None):
        """
        Perform forward pass of the Cross Entropy Loss.

        true
            input array containing true labels.
        pred
            input array containing Predicted labels.
        axis
            the axis along which to compute the cross-entropy loss. If axis is ``-1``,
            the cross-entropy loss will be computed along the last dimension.
            Default: ``-1``.
        epsilon
            small value to avoid division by zero. Default: ``1e-7``.
        reduction
            ``'none'``: No reduction will be applied to the output.
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed. Default: ``'sum'``.
        out
            optional output array, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The cross-entropy loss between the given distributions.
        """
        return ivy.cross_entropy(
            true,
            pred,
            axis=ivy.default(axis, self._axis),
            epsilon=ivy.default(epsilon, self._epsilon),
            reduction=ivy.default(reduction, self._reduction),
        )

class DiceLoss(Module):
    def __init__(self, smooth: float = 1.0, reduction: str = "mean"):
        self._smooth = smooth
        self._reduction = reduction
        Module.__init__(self)

    def _forward(self, true, pred, *, smooth=None, reduction=None):
        """
        Perform forward pass of the Dice Loss.

        true
            input array containing true labels.
        pred
            input array containing Predicted labels.
        smooth
            smoothing value to avoid division by zero in denominator. Default: ``1.0``.
        reduction
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed.
            ``'none'``: No reduction will be applied to the output. Default: ``'mean'``.

        Returns
        -------
        ret
            The Dice Loss between the given distributions.
        """
        return ivy.dice_loss(
            true,
            pred,
            smooth=ivy.default(smooth, self._smooth),
            reduction=ivy.default(reduction, self._reduction),
        )

