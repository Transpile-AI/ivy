from typing import (
    Optional,
    Union,
    Tuple,
    Iterable,
    Callable,
    Literal,
    Sequence,
    Generator,
)
from numbers import Number
import ivy
from ivy.func_wrapper import (
    handle_out_argument,
    to_native_arrays_and_back,
    handle_nestable,
    integer_arrays_to_float,
)
from ivy.exceptions import handle_exceptions


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def flatten(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    start_dim: Optional[int] = 0,
    end_dim: Optional[int] = -1,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Flattens input by reshaping it into a one-dimensional tensor.
        If start_dim or end_dim are passed, only dimensions starting
        with start_dim and ending with end_dim are flattened.
        The order of elements in input is unchanged.

    Parameters
    ----------
    x
        input array to flatten.
    start_dim
        first dim to flatten. If not set, defaults to 0.
    end_dim
        last dim to flatten. If not set, defaults to -1.

    Returns
    -------
    ret
        the flattened array over the specified dimensions.

    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/API_specification/generated/signatures.manipulation_functions.concat.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`ivy.Array` input:

    >>> x = np.array([1,2], [3,4])
    >>> ivy.flatten(x)
    ivy.array([1, 2, 3, 4])

    >>> x = np.array(
        [[[[ 5,  5,  0,  6],
         [17, 15, 11, 16],
         [ 6,  3, 13, 12]],

        [[ 6, 18, 10,  4],
         [ 5,  1, 17,  3],
         [14, 14, 18,  6]]],


       [[[12,  0,  1, 13],
         [ 8,  7,  0,  3],
         [19, 12,  6, 17]],

        [[ 4, 15,  6, 15],
         [ 0,  5, 17,  9],
         [ 9,  3,  6, 19]]],


       [[[17, 13, 11, 16],
         [ 4, 18, 17,  4],
         [10, 10,  9,  1]],

        [[19, 17, 13, 10],
         [ 4, 19, 16, 17],
         [ 2, 12,  8, 14]]]]
         )
    >>> ivy.flatten(x, start_dim = 1, end_dim = 2)
    ivy.array(
        [[[ 5,  5,  0,  6],
          [17, 15, 11, 16],
          [ 6,  3, 13, 12],
          [ 6, 18, 10,  4],
          [ 5,  1, 17,  3],
          [14, 14, 18,  6]],

         [[12,  0,  1, 13],
          [ 8,  7,  0,  3],
          [19, 12,  6, 17],
          [ 4, 15,  6, 15],
          [ 0,  5, 17,  9],
          [ 9,  3,  6, 19]],

         [[17, 13, 11, 16],
          [ 4, 18, 17,  4],
          [10, 10,  9,  1],
          [19, 17, 13, 10],
          [ 4, 19, 16, 17],
          [ 2, 12,  8, 14]]]))
    """
    if start_dim == end_dim and len(x.shape) != 0:
        return x
    if start_dim not in range(-len(x.shape), len(x.shape)):
        raise IndexError(
            f"Dimension out of range (expected to be in range of\
            {[-len(x.shape), len(x.shape) - 1]}, but got {start_dim}"
        )
    if end_dim not in range(-len(x.shape), len(x.shape)):
        raise IndexError(
            f"Dimension out of range (expected to be in range of\
            {[-len(x.shape), len(x.shape) - 1]}, but got {end_dim}"
        )
    if start_dim < 0:
        start_dim = len(x.shape) + start_dim
    if end_dim < 0:
        end_dim = len(x.shape) + end_dim
    c = 1
    for i in range(start_dim, end_dim + 1):
        c *= x.shape[i]
    lst = [c]
    if start_dim != 0:
        for i in range(0, start_dim):
            lst.insert(i, x.shape[i])
    for i in range(end_dim + 1, len(x.shape)):
        lst.insert(i, x.shape[i])
    return ivy.reshape(x, tuple(lst))


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def vorbis_window(
    window_length: Union[ivy.Array, ivy.NativeArray],
    *,
    dtype: Optional[Union[ivy.Dtype, ivy.NativeDtype]] = None,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns an array that contains a vorbis power complementary window
    of size window_length.

    Parameters
    ----------
    window_length
        the length of the vorbis window.
    dtype
        data type of the returned array. By default float32.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Input array with the vorbis window.

    Examples
    --------
    >>> ivy.vorbis_window(3)
    ivy.array([0.38268346, 1. , 0.38268352])

    >>> ivy.vorbis_window(5)
    ivy.array([0.14943586, 0.8563191 , 1. , 0.8563191, 0.14943568])
    """
    return ivy.current_backend().vorbis_window(window_length, dtype=dtype, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def hann_window(
    window_length: int,
    periodic: Optional[bool] = True,
    dtype: Optional[Union[ivy.Dtype, ivy.NativeDtype]] = None,
    *,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Generate a Hann window. The Hanning window
    is a taper formed by using a weighted cosine.

    Parameters
    ----------
    window_length
        the size of the returned window.
    periodic
        If True, returns a window to be used as periodic function.
        If False, return a symmetric window.
    dtype
        The data type to produce. Must be a floating point type.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        The array containing the window.

    Functional Examples
    -------------------
    >>> ivy.hann_window(4, True)
    ivy.array([0. , 0.5, 1. , 0.5])

    >>> ivy.hann_window(7, False)
    ivy.array([0.  , 0.25, 0.75, 1.  , 0.75, 0.25, 0.  ])

    """
    return ivy.current_backend().hann_window(
        window_length, periodic, dtype=dtype, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
def max_pool2d(
    x: Union[ivy.Array, ivy.NativeArray],
    kernel: Union[int, Tuple[int], Tuple[int, int]],
    strides: Union[int, Tuple[int], Tuple[int, int]],
    padding: str,
    /,
    *,
    data_format: str = "NHWC",
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Computes a 2-D max pool given 4-D input x.

    Parameters
    ----------
    x
        Input image *[batch_size,h,w,d_in]*.
    kernel
        Size of the kernel i.e., the sliding window for each
        dimension of input. *[h,w]*.
    strides
        The stride of the sliding window for each dimension of input.
    padding
        SAME" or "VALID" indicating the algorithm, or list
        indicating the per-dimensio paddings.
    data_format
        NHWC" or "NCHW". Defaults to "NHWC".
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        The result of the pooling operation.

    Both the description and the type hints above assumes an array input
    for simplicity, but this function is *nestable*, and therefore
    also accepts :class:`ivy.Container` instances in place of any of
    the arguments.

    Examples
    --------
    >>> x = ivy.arange(12).reshape((2, 1, 3, 2))
    >>> print(ivy.max_pool2d(x, (2, 2), (1, 1), 'SAME'))
    ivy.array([[[[ 2,  3],
     [ 4,  5],
     [ 4,  5]]],
    [[[ 8,  9],
     [10, 11],
     [10, 11]]]])

    >>> x = ivy.arange(48).reshape((2, 4, 3, 2))
    >>> print(ivy.max_pool2d(x, 3, 1, 'VALID'))
    ivy.array([[[[16, 17]],
    [[22, 23]]],
    [[[40, 41]],
    [[46, 47]]]])
    """
    return ivy.current_backend(x).max_pool2d(x, kernel, strides, padding, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def kaiser_window(
    window_length: int,
    periodic: bool = True,
    beta: float = 12.0,
    *,
    dtype: Optional[Union[ivy.Array, ivy.NativeArray]] = None,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Computes the Kaiser window with window length window_length and shape beta

    Parameters
    ----------
    window_length
        an int defining the length of the window.
    periodic
        If True, returns a periodic window suitable for use in spectral analysis.
        If False, returns a symmetric window suitable for use in filter design.
    beta
        a float used as shape parameter for the window.
    dtype
        data type of the returned array.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        The array containing the window.

    Examples
    --------
    >>> ivy.kaiser_window(5)
    ivy.array([5.2773e-05, 1.0172e-01, 7.9294e-01, 7.9294e-01, 1.0172e-01]])
    >>> ivy.kaiser_window(5, True, 5)
    ivy.array([0.0367, 0.4149, 0.9138, 0.9138, 0.4149])
    >>> ivy.kaiser_window(5, False, 5)
    ivy.array([0.0367, 0.5529, 1.0000, 0.5529, 0.0367])
    """
    return ivy.current_backend().kaiser_window(
        window_length, periodic, beta, dtype=dtype, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
def moveaxis(
    a: Union[ivy.Array, ivy.NativeArray],
    source: Union[int, Sequence[int]],
    destination: Union[int, Sequence[int]],
    /,
    *,
    out: Optional[Union[ivy.Array, ivy.NativeArray]] = None,
) -> Union[ivy.Array, ivy.NativeArray]:
    """Move axes of an array to new positions..

    Parameters
    ----------
    a
        The array whose axes should be reordered.
    source
        Original positions of the axes to move. These must be unique.
    destination
        Destination positions for each of the original axes.
        These must also be unique.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Array with moved axes. This array is a view of the input array.

    Examples
    --------
    With :class:`ivy.Array` input:
    >>> x = ivy.zeros((3, 4, 5))
    >>> ivy.moveaxis(x, 0, -1).shape
    (4, 5, 3)
    >>> ivy.moveaxis(x, -1, 0).shape
    (5, 3, 4)
    """
    return ivy.current_backend().moveaxis(a, source, destination, out=out)


@handle_exceptions
def ndenumerate(
    input: Iterable,
) -> Generator:
    """Multidimensional index iterator.

    Parameters
    ----------
    input
        Input array to iterate over.

    Returns
    -------
    ret
        An iterator yielding pairs of array coordinates and values.

    Examples
    --------
    >>> a = ivy.array([[1, 2], [3, 4]])
    >>> for index, x in ivy.ndenumerate(a):
    >>>     print(index, x)
    (0, 0) 1
    (0, 1) 2
    (1, 0) 3
    (1, 1) 4
    """

    def _ndenumerate(input, t=None):
        if t is None:
            t = ()
        if not hasattr(input, "__iter__"):
            yield t, input
        else:
            for i, v in enumerate(input):
                yield from _ndenumerate(v, t + (i,))

    return _ndenumerate(input)


@handle_exceptions
def ndindex(
    shape: Tuple,
) -> Generator:
    """Multidimensional index iterator.

    Parameters
    ----------
    shape
        The shape of the array to iterate over.

    Returns
    -------
    ret
        An iterator yielding array coordinates.

    Examples
    --------
    >>> a = ivy.array([[1, 2], [3, 4]])
    >>> for index in ivy.ndindex(a):
    >>>     print(index)
    (0, 0)
    (0, 1)
    (1, 0)
    (1, 1)
    """

    def _iter_product(*args, repeat=1):
        pools = [tuple(pool) for pool in args] * repeat
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)

    args = []
    for s in range(len(shape)):
        args += [range(shape[s])]
    return _iter_product(*args)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def pad(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    pad_width: Union[Iterable[Tuple[int]], int],
    *,
    mode: Optional[
        Union[
            Literal[
                "constant",
                "edge",
                "linear_ramp",
                "maximum",
                "mean",
                "median",
                "minimum",
                "reflect",
                "symmetric",
                "wrap",
                "empty",
            ],
            Callable,
        ]
    ] = "constant",
    stat_length: Optional[Union[Iterable[Tuple[int]], int]] = None,
    constant_values: Optional[Union[Iterable[Tuple[Number]], Number]] = 0,
    end_values: Optional[Union[Iterable[Tuple[Number]], Number]] = 0,
    reflect_type: Optional[Literal["even", "odd"]] = "even",
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Pads an array.

    Parameters
    ----------
    x
        Input array to pad.
    pad_width
        Number of values padded to the edges of each axis.
         - ((before_1, after_1), … (before_N, after_N)) yields unique pad widths
           for each axis.
         - ((before, after),) yields same before and after pad for each axis.
         - (pad,) or int is a shortcut for before = after = pad width for all axes.
    mode
        One of the following string values or a user supplied function.
             - "constant": Pads with a constant value.
             - "edge": Pads with the edge values of array.
             - "linear_ramp": Pads with the linear ramp between end_value
               and the array edge value.
             - "maximum": Pads with the maximum value of all or part of the vector
               along each axis.
             - "mean": Pads with the mean value of all or part of the vector along
               each axis.
             - "median": Pads with the median value of all or part of the vector
               along each axis.
             - "minimum": Pads with the minimum value of all or part of the vector
               along each axis.
             - "reflect": Pads with the reflection mirrored on the first and last
               values of the vector along each axis.
             - "symmetric": Pads with the reflection of the vector mirrored along
               the edge of the array.
             - "wrap": Pads with the wrap of the vector along the axis.
               The first values are used to pad the end and the end values are used
               to pad the beginning.
             - "empty": Pads with undefined values.
             - <function>: Pads with a user-defined padding function.
                 The padding function should modify a rank 1 array in-place.
                 It has the following signature:
                 padding_func(vector, iaxis_pad_width, iaxis, kwargs), where:
                     - vector is
                       A rank 1 array already padded with zeros. Padded values are
                       vector[:iaxis_pad_width[0]] and vector[-iaxis_pad_width[1]:].
                     - iaxis_pad_width is
                       A 2-tuple of ints, where iaxis_pad_width[0] represents the
                       number of values padded at the beginning of vector and
                       iaxis_pad_width[1] represents the number of values padded
                       at the end of vector.
                     - iaxis is
                       The axis currently being calculated.
                     - kwargs is
                       A dict of any keyword arguments the function requires.
    stat_length
        Used in "maximum", "mean", "median", and "minimum".
        Number of values at edge of each axis used to calculate the statistic value.
         - ((before_1, after_1), … (before_N, after_N)) yields unique statistic
           lengths for each axis.
         - ((before, after),) yields same before and after statistic lengths for
           each axis.
         - (stat_length,) or int is a shortcut for before = after = statistic length
           for all axes.
         - None uses the entire axis.
    constant_values
        Used in "constant". The values to set the padded values for each axis.
         - ((before_1, after_1), ... (before_N, after_N)) yields unique pad constants
           for each axis.
         - ((before, after),) yields same before and after constants for each axis.
         - (constant,) or constant is a shortcut for before = after = constant for
           all axes.
    end_values
        Used in "linear_ramp". The values used for the ending value of the linear_ramp
        and that will form the edge of the padded array.
         - ((before_1, after_1), ... (before_N, after_N)) yields unique end values
           for each axis.
         - ((before, after),) yields same before and after end values for each axis.
         - (constant,) or constant is a shortcut for before = after = constant for
           all axes.
    reflect_type
        Used in "reflect", and "symmetric". The "even" style is the default with an
        unaltered reflection around the edge value. For the "odd" style, the extended
        part of the array is created by subtracting the reflected values from two
        times the edge value.
    out
        optional output array, for writing the result to. It must have a shape that
        the inputs broadcast to.

    Returns
    -------
    ret
        Padded array of rank equal to x with shape increased according to pad_width.


    Both the description and the type hints above assume an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`ivy.Array` input:

    >>> x = ivy.array([[1, 2, 3], [4, 5, 6]])
    >>> padding = ivy.array([(1, 1), (2, 2)])
    >>> y = ivy.pad(x, padding, mode="constant")
    >>> print(y)
    ivy.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 2, 3, 0, 0],
               [0, 0, 4, 5, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]])

    >>> x = ivy.array([[1, 2, 3], [4, 5, 6]])
    >>> padding = ivy.array([(1, 1), (2, 2)])
    >>> y = ivy.pad(x, padding, mode="reflect")
    >>> print(y)
    ivy.array([[6, 5, 4, 5, 6, 5, 4],
               [3, 2, 1, 2, 3, 2, 1],
               [6, 5, 4, 5, 6, 5, 4],
               [3, 2, 1, 2, 3, 2, 1]])

    >>> x = ivy.array([[1, 2, 3], [4, 5, 6]])
    >>> padding = ivy.array([(1, 1), (2, 2)])
    >>> y = ivy.pad(x, padding, mode="symmetric")
    >>> print(y)
    ivy.array([[2, 1, 1, 2, 3, 3, 2],
               [2, 1, 1, 2, 3, 3, 2],
               [5, 4, 4, 5, 6, 6, 5],
               [5, 4, 4, 5, 6, 6, 5]])

    With :class:`ivy.NativeArray` input:

    >>> x = ivy.native_array([[1, 2, 3], [4, 5, 6]])
    >>> padding = ivy.array([(1, 1), (2, 2)])
    >>> y = ivy.pad(x, padding, mode="constant", constant_values=7)
    >>> print(y)
    ivy.array([[7, 7, 7, 7, 7, 7, 7],
               [7, 7, 1, 2, 3, 7, 7],
               [7, 7, 4, 5, 6, 7, 7],
               [7, 7, 7, 7, 7, 7, 7]])

    With :class:`ivy.Container` input:

    >>> x = ivy.Container(a=ivy.array([0., 1., 2.]), b=ivy.array([0., 1., 2.]))
    >>> padding = ivy.array([(1, 1)])
    >>> y = ivy.pad(x, padding, mode="constant")
    >>> print(y)
    {
        a: ivy.array([0., 0., 1., 2., 0.]),
        b: ivy.array([0., 0., 1., 2., 0.])
    }
    """
    return ivy.current_backend(x).pad(
        x,
        pad_width,
        mode=mode,
        stat_length=stat_length,
        constant_values=constant_values,
        end_values=end_values,
        reflect_type=reflect_type,
        out=out,
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
def heaviside(
    x1: Union[ivy.Array, ivy.NativeArray],
    x2: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Computes the Heaviside step function for each element in x1.

    Parameters
    ----------
    x1
        input array.
    x2
        values to use where x1 is zero.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        output array with element-wise Heaviside step function of x1.
        This is a scalar if both x1 and x2 are scalars.

    Examples
    --------
    With :class:`ivy.Array` input:

    >>> x1 = ivy.array([-1.5, 0, 2.0])
    >>> x2 = ivy.array([0.5])
    >>> ivy.heaviside(x1, x2)
    ivy.array([0.0000, 0.5000, 1.0000])

    >>> x1 = ivy.array([-1.5, 0, 2.0])
    >>> x2 = ivy.array([1.2, -2.0, 3.5])
    >>> ivy.heaviside(x1, x2)
    ivy.array([0., -2., 1.])
    """
    return ivy.current_backend().heaviside(x1, x2, out=out)


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
@handle_out_argument
@handle_nestable
def flipud(
    m: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    out: Optional[Union[ivy.Array, ivy.NativeArray]] = None,
) -> Union[ivy.Array, ivy.NativeArray]:
    """Flip array in the up/down direction.
    Flip the entries in each column in the up/down direction.
    Rows are preserved, but appear in a different order than before.

    Parameters
    ----------
    m
        The array to be flipped.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Array corresponding to input array with elements
        order reversed along axis 0.

    Examples
    --------
    >>> m = ivy.diag([1, 2, 3])
    >>> ivy.flipud(m)
    ivy.array([[ 0.,  0.,  3.],
        [ 0.,  2.,  0.],
        [ 1.,  0.,  0.]])
    """
    return ivy.current_backend().flipud(m, out=out)
