# global
import abc
from typing import Optional, Union

# local
import ivy


class _ArrayWithNormsExperimental(abc.ABC):
    def l2_normalize(
        self: ivy.Array,
        axis: Optional[int] = None,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """Normalizes the array to have unit L2 norm.

        Parameters
        ----------
        self
            Input array.
        axis
            Axis along which to normalize. If ``None``, the whole array
            is normalized.
        out
            optional output array, for writing the result to. It must have a
            shape that the inputs broadcast to.

        Returns
        -------
        ret
            The normalized array.

        Examples
        --------
        >>> x = ivy.array([[1., 2.], [3., 4.]])
        >>> x.l2_normalize(axis=1)
        ivy.array([[0.4472, 0.8944],
                   [0.6, 0.8]])
        """
        return ivy.l2_normalize(self, axis=axis, out=out)

    def batch_norm(
            self,
            mean: Union[ivy.NativeArray, ivy.Array],
            variance: Union[ivy.NativeArray, ivy.Array],
            /,
            *,
            offset: Optional[Union[ivy.NativeArray, ivy.Array]] = None,
            scale: Optional[Union[ivy.NativeArray, ivy.Array]] = None,
            training: bool = False,
            eps: float = 1e-5,
            momentum: float = 1e-1,
            out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.batch_norm. This method
        simply wraps the function, and so the docstring for ivy.batch_norm
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array of shape (N,C,S), where N is the batch dimension, C is the
            feature dimension and S corresponds to the following spatial dimensions.
        mean
            A mean array for the input's normalization.
        variance
            A variance array for the input's normalization.
        offset
            An offset array. If present, will be added to the normalized input.
        scale
            A scale array. If present, the scale is applied to the normalized input.
        training
            If true, calculate and use the mean and variance of `x`. Otherwise, use the
            provided `mean` and `variance`.
        eps
            A small float number to avoid dividing by 0.
        momentum
             The value used for the running_mean and running_var computation. Default value is 0.1.
        out
            Optional output array, for writing the result to.

        Returns
        -------
        ret
             Array containing the normalized, scaled, offset values.
        """
        return ivy.batch_norm(
            self._data,
            mean,
            variance,
            scale=scale,
            offset=offset,
            training=training,
            eps=eps,
            momentum=momentum,
            out=out,
        )

    def instance_norm(
        self,
        mean: Union[ivy.NativeArray, ivy.Array],
        variance: Union[ivy.NativeArray, ivy.Array],
        /,
        *,
        offset: Optional[Union[ivy.NativeArray, ivy.Array]] = None,
        scale: Optional[Union[ivy.NativeArray, ivy.Array]] = None,
        training: bool = False,
        eps: float = 1e-5,
        momentum: float = 1e-1,
        out: Optional[ivy.Array] = None,
    ):
        """
        ivy.Array instance method variant of ivy.instance_norm. This method
        simply wraps the function, and so the docstring for ivy.instance_norm
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            Input array of shape (N,C,S), where N is the batch dimension, C is the
            feature dimension and S corresponds to the following spatial dimensions.
        mean
            A mean array for the input's normalization.
        variance
            A variance array for the input's normalization.
        offset
            An offset array. If present, will be added to the normalized input.
        scale
            A scale array. If present, the scale is applied to the normalized input.
        training
            If true, calculate and use the mean and variance of `x`. Otherwise, use the
            provided `mean` and `variance`.
        eps
            A small float number to avoid dividing by 0.
        momentum
             The value used for the running_mean and running_var computation. Default value is 0.1.
        out
            Optional output array, for writing the result to.

        Returns
        -------
        ret
             Array containing the normalized, scaled, offset values.
        """
        return ivy.instance_norm(
            self._data,
            mean,
            variance,
            scale=scale,
            offset=offset,
            training=training,
            eps=eps,
            momentum=momentum,
            out=out,
        )

    def lp_normalize(
        self: ivy.Array,
        /,
        *,
        p: float = 2,
        axis: Optional[int] = None,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """Normalizes the array to have Lp norm.

        Parameters
        ----------
        self
            Input array.
        p
            p-norm to use for normalization.
        axis
            Axis along which to normalize. If ``None``, the whole array
            is normalized.
        out
            optional output array, for writing the result to. It must have a
            shape that the inputs broadcast to.

        Returns
        -------
        ret
            The normalized array.

        Examples
        --------
        >>> x = ivy.array([[1., 2.], [3., 4.]])
        >>> x.lp_normalize(p=2, axis=1)
        ivy.array([[0.4472, 0.8944],
               [0.6, 0.8]])
        """
        return ivy.lp_normalize(self, p=p, axis=axis, out=out)
