from typing import Optional, Union, Tuple, Sequence
import ivy
from ivy.func_wrapper import (
    handle_out_argument,
    to_native_arrays_and_back,
    handle_nestable,
    infer_dtype,
)
from ivy.utils.exceptions import handle_exceptions

@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def histogramdd(
        a: Union[ivy.Array, ivy.NativeArray],
        /,
        *,
        bins: Optional[Union[Tuple[int], int]] = 10,
        range: Optional[Tuple[float]] = None,
        weights: Optional[Union[ivy.Array, ivy.NativeArray]] = None,
        density: Optional[bool] = False
) -> ivy.Array:
    """
    Compute the histogramdd of the NxD array ``a``.
    .. note::
        Given bins = [c0, ..., cK], defining intervals I0 = [c0, c1), I1 = [c1, c2),
        ..., I_{K-1} = [c_{K-1}, cK].
    Parameters
    ----------
    a
        input array.
    bins
        if ``bins`` is an int, it defines the number of equal-width bins in the given
        range.
        if ``bins`` is an array, it defines a monotonically increasing array of bin
        edges, including the rightmost edge, allowing for non-uniform bin widths.
    range
        the lower and upper range of the bins. The first element of the range must be
        less than or equal to the second.
    weights
        each value in ``a`` only contributes its associated weight towards the bin count
        (instead of 1). Must be of the same shape as a.
    density
        if True, the result is the value of the probability density function at the
        bin, normalized such that the integral over the range of bins is 1.
    Returns
    -------
    ret
        a tuple containing the values of the histogramdd and the bin edges.
    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.
    Examples
    --------
    With :class:`ivy.Array` input:
    >>> x = ivy.array([0, 0, 1, 1,2,2,2],[1,1,1,1,2,2])
    >>> y = ivy.array([0., 0.5, 1., 1.5, 2.])
    >>> z = ivy.histogramdd(x, bins=y)
    >>> print(z)
    (ivy.array([1, 0, 1, 1]), ivy.array([0. , 0.5, 1. , 1.5, 2. ]))
    >>> x = ivy.array([[1.1, 2.2, 3.3],
    ...                [4.4, 5.5, .6]])
    >>> bins = 4
    >>> range = (0., 5.)
    >>> dtype = ivy.int32
    >>> y = ivy.histogramdd(x, bins=bins, range=range, dtype=dtype)
    >>> print(y)
    (ivy.array([0, 0, 0, 0]), ivy.array([0.   , 0.125, 0.25 , 0.375, 0.5  ]))
    >>> x = ivy.array([[1.1, 2.2, 3.3],
    ...                [-4.4, -5.5, -6.6]])
    >>> y = ivy.array([0., 1., 2., 3., 4., 5.])
    >>> weights = ivy.array([[1., 1., 1.], [1., 1., 1.]])
    >>> z = ivy.histogramdd(
    >>>                     x,
    >>>                     bins=y,
    >>>                     weights=weights)
    >>> print(z)
    (ivy.array([[0., 3.],
    [1., 0.],
    [1., 0.],
    [1., 0.],
    [0., 0.]]), ivy.array([0., 1., 2., 3., 4., 5.]))
    >>> x = ivy.Container(a=ivy.array([0., 1., 2.]), b=ivy.array([3., 4., 5.]))
    >>> y = ivy.array([0., 1., 2., 3., 4., 5.])
    >>> z = ivy.histogramdd(x, bins=y, dtype=dtype)
    >>> print(z.a)
    >>> print(z.b)
    (ivy.array([1, 1, 1, 0, 0]), ivy.array([0., 1., 2., 3., 4., 5.]))
    (ivy.array([0, 0, 0, 1, 2]), ivy.array([0., 1., 2., 3., 4., 5.]))
    """
    return ivy.current_backend(a).histogramdd(
        a,
        bins=bins,
        range=range,
        weights=weights,
        density=density
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def median(
    input: ivy.Array,
    /,
    *,
    axis: Optional[Union[Tuple[int], int]] = None,
    keepdims: Optional[bool] = False,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Compute the median along the specified axis.

    Parameters
    ----------
    input
        Input array.
    axis
        Axis or axes along which the medians are computed. The default is to compute
        the median along a flattened version of the array.
    keepdims
        If this is set to True, the axes which are reduced are left in the result
        as dimensions with size one.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        The median of the array elements.

    Functional Examples
    -------------------
    >>> a = ivy.array([[10, 7, 4], [3, 2, 1]])
    >>> ivy.median(a)
    3.5
    >>> ivy.median(a, axis=0)
    ivy.array([6.5, 4.5, 2.5])
    """
    return ivy.current_backend().median(input, axis=axis, keepdims=keepdims, out=out)


@to_native_arrays_and_back
@infer_dtype
@handle_out_argument
@handle_nestable
@handle_exceptions
def nanmean(
    a: ivy.Array,
    /,
    *,
    axis: Optional[Union[Tuple[int], int]] = None,
    keepdims: Optional[bool] = False,
    dtype: Optional[Union[ivy.Dtype, ivy.NativeDtype]] = None,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Computes the mean of all non-NaN elements along the specified dimensions.

    Parameters
    ----------
    a
        Input array.
    axis
        Axis or axes along which the means are computed.
        The default is to compute the mean of the flattened array.
    keepdims
        If this is set to True, the axes which are reduced are left in the result
        as dimensions with size one. With this option, the result will broadcast
        correctly against the original a. If the value is anything but the default,
        then keepdims will be passed through to the mean or sum methods of sub-classes
        of ndarray. If the sub-classes methods does not implement keepdims any
        exceptions will be raised.
    dtype
        The desired data type of returned tensor. Default is None.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        The nanmean of the array elements.

    Functional Examples
    -------------------
    >>> a = ivy.array([[1, ivy.nan], [3, 4]])
    >>> ivy.nanmean(a)
    2.6666666666666665
    >>> ivy.nanmean(a, axis=0)
    ivy.array([2.,  4.])
    """
    return ivy.current_backend(a).nanmean(
        a, axis=axis, keepdims=keepdims, dtype=dtype, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def unravel_index(
    indices: ivy.Array,
    shape: Tuple[int],
    /,
    *,
    out: Optional[ivy.Array] = None,
) -> Tuple:
    """Converts a flat index or array of flat indices
    into a tuple of coordinate arrays.

    Parameters
    ----------
    indices
        Input array.
    shape
        The shape of the array to use for unraveling indices.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Tuple with arrays of type int32 that have the same shape as the indices array.

    Functional Examples
    -------------------
    >>> indices = ivy.array([22, 41, 37])
    >>> ivy.unravel_index(indices, (7,6))
    (ivy.array([3, 6, 6]), ivy.array([4, 5, 1]))
    """
    return ivy.current_backend(indices).unravel_index(indices, shape, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def quantile(
    a: ivy.Array,
    q: Union[ivy.Array, float],
    /,
    *,
    axis: Optional[Union[Sequence[int], int]] = None,
    keepdims: Optional[bool] = False,
    interpolation: Optional[str] = "linear",
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Compute the q-th quantile of the data along the specified axis.

    Parameters
    ----------
    a
        Input array.
    q
        Quantile or sequence of quantiles to compute, which must be
        between 0 and 1 inclusive.
    axis
        Axis or axes along which the quantiles are computed. The default
        is to compute the quantile(s) along a flattened version of the array.
    keepdims
        If this is set to True, the axes which are reduced are left in the result
        as dimensions with size one. With this option, the result will broadcast
        correctly against the original array a.
    interpolation
        {'nearest', 'linear', 'lower', 'higher', 'midpoint'}. Default value: 'linear'.
        This specifies the interpolation method to use when the desired quantile lies
        between two data points i < j:
        - linear: i + (j - i) * fraction, where fraction is the fractional part of the
        index surrounded by i and j.
        - lower: i.
        - higher: j.
        - nearest: i or j, whichever is nearest.
        - midpoint: (i + j) / 2. linear and midpoint interpolation do not work with
        integer dtypes.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        A (rank(q) + N - len(axis)) dimensional array of same dtype as a, or, if axis
        is None, a rank(q) array. The first rank(q) dimensions index quantiles for
        different values of q.

    Examples
    --------
    >>> a = ivy.array([[10., 7., 4.], [3., 2., 1.]])
    >>> q = ivy.array(0.5)
    >>> ivy.quantile(a, q)
    ivy.array(3.5)

    >>> a = ivy.array([[10., 7., 4.], [3., 2., 1.]])
    >>> q = 0.5
    >>> ivy.quantile(a, q)
    ivy.array(3.5)

    >>> ivy.quantile(a, q, axis=0)
    ivy.array([6.5, 4.5, 2.5])

    >>> ivy.quantile(a, q, axis=1)
    ivy.array([7.,  2.])

    >>> ivy.quantile(a, q, axis=1, keepdims=True)
    ivy.array([[7.],[2.]])

    >>> a = ivy.array([1., 2., 3., 4.])
    >>> q = ivy.array([0.3, 0.7])
    >>> ivy.quantile(a, q, interpolation='lower')
    ivy.array([1., 3.])
    """
    return ivy.current_backend(a).quantile(
        a, q, axis=axis, keepdims=keepdims, interpolation=interpolation, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def corrcoef(
    x: ivy.Array,
    /,
    *,
    y: Optional[ivy.Array] = None,
    rowvar: Optional[bool] = True,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    return ivy.current_backend().corrcoef(x, y=y, rowvar=rowvar, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def nanmedian(
    input: ivy.Array,
    /,
    *,
    axis: Optional[Union[Tuple[int], int]] = None,
    keepdims: Optional[bool] = False,
    overwrite_input: Optional[bool] = False,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """ivy.Array instance method variant of ivy.nanmedian. This method simply 
    wraps the function, and so the docstring for ivy.nanmedian also applies to
    this method with minimal changes.

    Parameters
    ----------
    self
        Input array.
    axis
        Axis or axes along which the means are computed.
        The default is to compute the mean of the flattened array.
    keepdims
        If this is set to True, the axes which are reduced are left in the result
        as dimensions with size one. With this option, the result will broadcast
        correctly against the original a. If the value is anything but the default,
        then keepdims will be passed through to the mean or sum methods of
        sub-classes of ndarray. If the sub-classes methods does not implement
        keepdims any exceptions will be raised.
    overwrite_input
        If True, then allow use of memory of input array a for calculations.
        The input array will be modified by the call to median. This will
        save memory when you do not need to preserve the contents of the input array.
        Treat the input as undefined, but it will probably be fully or partially sorted.
        Default is False. If overwrite_input is True and a is not already an ndarray,
        an error will be raised.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        A new array holding the result. If the input contains integers

    Examples
    --------
    >>> a = ivy.Array([[10.0, ivy.nan, 4], [3, 2, 1]])
    >>> a.nanmedian(a)
        3.0
    >>> a.nanmedian(a, axis=0)
        array([6.5, 2. , 2.5])
    """

    return ivy.current_backend().nanmedian(
        input, axis=axis, keepdims=keepdims, overwrite_input=overwrite_input, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def bincount(
    x: ivy.Array,
    /,
    *,
    weights: Optional[ivy.Array] = None,
    minlength: Optional[int] = 0,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    return ivy.current_backend(x).bincount(
        x, weights=weights, minlength=minlength, out=out
    )
