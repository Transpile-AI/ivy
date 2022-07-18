# for review
# global
import abc
from typing import Optional, Union

# local
import ivy

# ToDo: implement all methods here as public instance methods


# noinspection PyUnresolvedReferences
class ArrayWithElementwise(abc.ABC):
    def abs(self: ivy.Array, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.abs. This method simply wraps the
        function, and so the docstring for ivy.abs also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the absolute value of each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = ivy.array([2.6, -6.6, 1.6, -0])
        >>> y = x.abs()
        >>> print(y)
        ivy.array([ 2.6, 6.6, 1.6, 0.])
        """
        return ivy.abs(self, out=out)

    def acosh(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.acosh. This method simply wraps the
        function, and so the docstring for ivy.acosh also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent the area of a hyperbolic sector.
            Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse hyperbolic cosine
            of each element in ``self``.
            The returned array must have the same data type as ``self``.
        """
        return ivy.acosh(self._data, out=out)

    def acos(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.acos. This method simply wraps the
        function, and so the docstring for ivy.acos also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse cosine of each element in ``self``.
            The  returned array must have the same data type as ``self``.
        """
        return ivy.acos(self._data, out=out)

    def add(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.add. This method simply wraps the
        function, and so the docstring for ivy.add also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a numeric data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise sums. The returned array must have a
            data type determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = ivy.array([1, 2, 3])
        >>> y = ivy.array([4, 5, 6])
        >>> z = x.add(y)
        >>> print(z)
        ivy.array([5, 7, 9])
        """
        return ivy.add(self._data, x2, out=out)

    def asin(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.asin. This method simply wraps the
        function, and so the docstring for ivy.asin also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse sine of each element in ``self``. The
            returned array must have the same data type as ``self``.
        """
        return ivy.asin(self._data, out=out)

    def asinh(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.asinh. This method simply wraps the
        function, and so the docstring for ivy.asinh also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent the area of a hyperbolic sector.
            Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse hyperbolic sine of each element in ``self``.
            The returned array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = ivy.array([-1., 0., 3.])
        >>> y = x.asinh()
        >>> print(y)
        ivy.array([-0.881,  0.   ,  1.82 ])
        """
        return ivy.asinh(self._data, out=out)

    def atan(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.atan. This method simply wraps the
        function, and so the docstring for ivy.atan also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse tangent of each element in ``self``. The
            returned array must have the same data type as ``self``.
        """
        return ivy.atan(self._data, out=out)

    def atan2(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.atan2. This method simply wraps the
        function, and so the docstring for ivy.atan2 also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            first input array corresponding to the y-coordinates.
            Should have a real-valued floating-point data type.
        x2
            second input array corresponding to the x-coordinates.
            Must be compatible with ``self``(see :ref:`broadcasting`).
            Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse tangent of the quotient ``self/x2``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.
        """
        return ivy.atan2(self._data, x2, out=out)

    def atanh(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.atanh. This method simply wraps the
        function, and so the docstring for ivy.atanh also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent the area of a hyperbolic sector.
            Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the inverse hyperbolic tangent of each element
            in ``self``. The returned array must have a floating-point data type
            determined by :ref:`type-promotion`.
        """
        return ivy.atanh(self._data, out=out)

    def bitwise_and(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.bitwise_and.
        This method simply wraps the function, and so the docstring for
        ivy.bitwise_and also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined by :ref:`type-promotion`.
        """
        return ivy.bitwise_and(self._data, x2, out=out)

    def bitwise_left_shift(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.bitwise_left_shift.
        This method simply wraps the function, and so the docstring for
        ivy.bitwise_left_shift also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined by :ref:`type-promotion`.
        """
        return ivy.bitwise_left_shift(self._data, x2, out=out)

    def bitwise_invert(
        self: ivy.Array, *, out: Optional[ivy.Array] = None
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.bitwise_invert.
        This method simply wraps the function, and so the docstring
        for ivy.bitiwse_invert also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have the same data type as ``self``.
        """
        return ivy.bitwise_invert(self._data, out=out)

    def bitwise_or(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.bitwise_or. This method simply
        wraps the function, and so the docstring for ivy.bitwise_or also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = ivy.array([1, 2, 3])
        >>> y = ivy.array([4, 5, 6])
        >>> z = x.bitwise_or(y)
        >>> print(z)
        ivy.array([5, 7, 7])
        """
        return ivy.bitwise_or(self._data, x2, out=out)

    def bitwise_right_shift(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.bitwise_right_shift.
        This method simply wraps the function, and so the docstring
        for ivy.bitwise_right_shift also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`). Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.
        """
        return ivy.bitwise_right_shift(self._data, x2, out=out)

    def bitwise_xor(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.bitwise_xor.
        This method simply wraps the function, and so the docstring
        for ivy.bitwise_xor also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have an integer or boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have an integer or boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.
        """
        return ivy.bitwise_xor(self._data, x2, out=out)

    def ceil(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.ceil.
        This method simply wraps the function, and so the docstring for
        ivy.ceil also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rounded result for each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = ivy.array([5.5, -2.5, 1.5, -0])
        >>> y = x.ceil()
        >>> print(y)
        ivy.array([ 6., -2.,  2.,  0.])
        """
        return ivy.ceil(self._data, out=out)

    def cos(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.cos. This method simply wraps the
        function, and so the docstring for ivy.cos also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array whose elements are each expressed in radians. Should have a
            floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the cosine of each element in ``self``. The returned
            array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        With :code:`ivy.Array` input:

        >>> x = ivy.array([1., 0., 2.,])
        >>> y = x.cos()
        >>> print(y)
        ivy.array([0.54, 1., -0.416])

        >>> x = ivy.array([-3., 0., 3.])
        >>> y = ivy.zeros(3)
        >>> ivy.cos(x, out=y)
        >>> print(y)
        ivy.array([-0.99,  1.  , -0.99])
        """
        return ivy.cos(self._data, out=out)

    def cosh(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.cosh. This method simply wraps
        the function, and so the docstring for ivy.cosh also applies to this
        method with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent a hyperbolic angle.
            Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the hyperbolic cosine of each element in ``self``.
            The returned array must have a floating-point data type determined by
            :ref:`type-promotion`.
        """
        return ivy.cosh(self._data, out=out)

    def divide(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.divide. This method simply
        wraps the function, and so the docstring for ivy.divide also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array. Should have a real-valued data type.
        x2
            divisor input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.
        """
        return ivy.divide(self._data, x2, out=out)

    def equal(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.equal.
        This method simply wraps the function, and so the docstring for
        ivy.equal also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            May have any data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.
        """
        return ivy.equal(self._data, x2, out=out)

    def exp(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.exp. This method simply
        wraps the function, and so the docstring for ivy.exp also applies
        to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated exponential function result for
            each element in ``self``. The returned array must have a floating-point
            data type determined by :ref:`type-promotion`.
        """
        return ivy.exp(self._data, out=out)

    def expm1(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.expm1. This method simply wraps
        the function, and so the docstring for ivy.expm1 also applies to this
        method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.
        """
        return ivy.expm1(self._data, out=out)

    def floor(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.floor. This method simply wraps
        the function, and so the docstring for ivy.floor also applies to this
        method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rounded result for each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = ivy.array([5.5, -2.5, 1.5, -0])
        >>> y = x.floor()
        >>> print(y)
        ivy.array([ 5., -3.,  1.,  0.])
        """
        return ivy.floor(self._data, out=out)

    def floor_divide(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.floor_divide.
        This method simply wraps the function, and so the docstring for ivy.floor_divide
        also applies to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array. Should have a real-valued data type.
        x2
            divisor input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined
            by :ref:`type-promotion`.
        """
        return ivy.floor_divide(self._data, x2, out=out)

    def greater(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.greater.
        This method simply wraps the function, and so the docstring for
        ivy.greater also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array must
            have a data type of ``bool``.
        """
        return ivy.greater(self._data, x2, out=out)

    def greater_equal(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.greater_equal.
        This method simply wraps the function, and so the docstring for
        ivy.greater_equal also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.
        """
        return ivy.greater_equal(self._data, x2, out=out)

    def isfinite(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.isfinite.
        This method simply wraps the function, and so the docstring
        for ivy.isfinite also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing test results. An element ``out_i`` is ``True``
            if ``self_i`` is finite and ``False`` otherwise.
            The returned array must have a data type of ``bool``.
        """
        return ivy.isfinite(self._data, out=out)

    def isinf(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.isinf. This method simply wraps
        the function, and so the docstring for ivy.isinf also applies to this
        method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing test results. An element ``out_i`` is ``True``
            if ``self_i`` is either positive or negative infinity and ``False``
            otherwise. The returned array must have a data type of ``bool``.
        """
        return ivy.isinf(self._data, out=out)

    def isnan(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.isnan. This method simply wraps
        the function, and so the docstring for ivy.isnan also applies to this
        method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing test results. An element ``out_i`` is ``True``
            if ``self_i`` is ``NaN`` and ``False`` otherwise.
            The returned array should have a data type of ``bool``.
        """
        return ivy.isnan(self._data, out=out)

    def less(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.less. This method simply wraps
        the function, and so the docstring for ivy.less also applies to this
        method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.
        """
        return ivy.less(self._data, x2, out=out)

    def less_equal(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.less_equal.
        This method simply wraps the function, and so the docstring
        for ivy.less_equal also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.
        """
        return ivy.less_equal(self._data, x2, out=out)

    def log(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.log. This method simply wraps the
        function, and so the docstring for ivy.log also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.
        """
        return ivy.log(self._data, out=out)

    def log1p(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.log1p.
        This method simply wraps the function, and so the docstring
        for ivy.log1p also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have a real-valued floating-point data
            type determined by :ref:`type-promotion`.
        """
        return ivy.log1p(self._data, out=out)

    def log2(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.log2.
        This method simply wraps the function, and so the docstring for
        ivy.log2 also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated base ``2`` logarithm for each element
            in ``self``. The returned array must have a real-valued floating-point
            data type determined by :ref:`type-promotion`.
        """
        return ivy.log2(self._data, out=out)

    def log10(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.log10. This method simply wraps the
        function, and so the docstring for ivy.log10 also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated base ``10`` logarithm for each element
            in ``self``. The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.
        """
        return ivy.log10(self._data, out=out)

    def logaddexp(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.logaddexp.
        This method simply wraps the function, and so the docstring for
        ivy.logaddexp also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a real-valued floating-point data
            type determined by :ref:`type-promotion`.
        """
        return ivy.logaddexp(self._data, x2, out=out)

    def logical_and(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.logical_and.
        This method simply wraps the function, and so the docstring for
        ivy.logical_and also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.
        """
        return ivy.logical_and(self._data, x2, out=out)

    def logical_not(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.logical_not.
        This method simply wraps the function, and so the docstring
        for ivy.logical_not also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a boolean data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type of ``bool``.
        """
        return ivy.logical_not(self._data, out=out)

    def logical_or(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.logical_or.
        This method simply wraps the function, and so the docstring for
        ivy.logical_or also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a boolean data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.
        """
        return ivy.logical_or(self._data, x2, out=out)

    def logical_xor(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.logical_xor.
        This method simply wraps the function, and so the docstring
        for ivy.logical_xor also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a boolean data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned array
            must have a data type of ``bool``.
        """
        return ivy.logical_xor(self._data, x2, out=out)

    def multiply(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.multiply.
        This method simply wraps the function, and so the docstring for ivy.multiply
         also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise products. The returned array
            must have a data type determined by :ref:`type-promotion`.
        """
        return ivy.multiply(self._data, x2, out=out)

    def negative(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.negative.
        This method simply wraps the function, and so the docstring
        for ivy.negative also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have the same data type as ``self``.
        """
        return ivy.negative(self._data, out=out)

    def not_equal(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.not_equal.
        This method simply wraps the function, and so the docstring
        for ivy.not_equal also applies to this method with minimal changes.

        Parameters
        ----------
        self
            first input array. May have any data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results. The returned
            array must have a data type of ``bool``.
        """
        return ivy.not_equal(self._data, x2, out=out)

    def positive(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.positive.
        This method simply wraps the function, and so the docstring
        for ivy.positive also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``.
            The returned array must have the same data type as ``self``.
        """
        return ivy.positive(self._data, out=out)

    def pow(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.pow. This method simply wraps the
        function, and so the docstring for ivy.pow also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            first input array whose elements correspond to the exponentiation base.
            Should have a real-valued data type.
        x2
            second input array whose elements correspond to the exponentiation
            exponent. Must be compatible with ``self`` (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            The returned array must have a data type determined by :ref:`type-promotion`.
        """
        return ivy.pow(self._data, x2, out=out)

    def remainder(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.remainder.
        This method simply wraps the function, and so the docstring
        for ivy.remainder also applies to this method with minimal changes.

        Parameters
        ----------
        self
            dividend input array. Should have a real-valued data type.
        x2
            divisor input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise results.
            Each element-wise result must have the same sign as the respective
            element ``x2_i``. The returned array must have a data type
            determined by :ref:`type-promotion`.
        """
        return ivy.remainder(self._data, x2, out=out)

    def round(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.round. This method simply wraps the
        function, and so the docstring for ivy.round also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rounded result for each element in ``self``.
            The returned array must have the same data type as ``self``.
        """
        return ivy.round(self._data, out=out)

    def sign(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.sign. This method simply wraps the
        function, and so the docstring for ivy.sign also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a numeric data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the evaluated result for each element in ``self``. The
            returned array must have the same data type as ``self``.

        Examples
        --------
        >>> x = ivy.array([5.7, -7.1, 0, -0, 6.8])
        >>> y = x.sign()
        >>> print(y)
        ivy.array([ 1., -1.,  0.,  0.,  1.])

        >>> x = ivy.array([-94.2, 256.0, 0.0001, -0.0001, 36.6])
        >>> y = x.sign()
        >>> print(y)
        ivy.array([-1.,  1.,  1., -1.,  1.])

        >>> x = ivy.array([[ -1., -67.,  0.,  15.5,  1.], [3, -45, 24.7, -678.5, 32.8]])
        >>> y = x.sign()
        >>> print(y)
        ivy.array([[-1., -1.,  0.,  1.,  1.],
        [ 1., -1.,  1., -1.,  1.]])
        """
        return ivy.sign(self._data, out=out)

    def sin(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.sin. This method simply wraps the
        function, and so the docstring for ivy.sin also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array whose elements are each expressed in radians. Should have a
            floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the sine of each element in ``self``. The returned
            array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = ivy.array([0., 1., 2., 3.])
        >>> y = x.sin()
        >>> print(y)
        ivy.array([0., 0.841, 0.909, 0.141])
        """
        return ivy.sin(self._data, out=out)

    def sinh(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.sinh. This method simply wraps the
        function, and so the docstring for ivy.sinh also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent a hyperbolic angle.
            Should have a floating-point data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the hyperbolic sine of each element in ``self``. The
            returned array must have a floating-point data type determined by
            :ref:`type-promotion`.

        Examples
        --------
        >>> x = ivy.array([1., 2., 3.])
        >>> print(x.sinh())
            ivy.array([1.18, 3.63, 10.])

        >>> x = ivy.array([0.23, 3., -1.2])
        >>> y = ivy.zeros(3)
        >>> print(x.sinh(out=y))
            ivy.array([0.232, 10., -1.51])
        """
        return ivy.sinh(self._data, out=out)

    def square(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.square.
        This method simply wraps the function, and so the docstring
        for ivy.square also applies to this method with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the square of each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.
        """
        return ivy.square(self._data, out=out)

    def sqrt(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.sqrt. This method simply wraps the
        function, and so the docstring for ivy.sqrt also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued floating-point data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the square root of each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.
        """
        return ivy.sqrt(self._data, out=out)

    def subtract(
        self: ivy.Array,
        x2: Union[ivy.Array, ivy.NativeArray],
        *,
        out: Optional[ivy.Array] = None,
    ) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.subtract.
        This method simply wraps the function, and so the docstring
        for ivy.subtract also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            first input array. Should have a real-valued data type.
        x2
            second input array. Must be compatible with ``self``
            (see :ref:`broadcasting`).
            Should have a real-valued data type.
        out
            optional output array, for writing the result to. It must have a shape that
            the inputs broadcast to.

        Returns
        -------
        ret
            an array containing the element-wise differences. The returned array
            must have a data type determined by :ref:`type-promotion`.
        """
        return ivy.subtract(self._data, x2, out=out)

    def tan(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.tan. This method simply wraps the
        function, and so the docstring for ivy.tan also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array whose elements are expressed in radians. Should have a
            floating-point data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the tangent of each element in ``self``.
            The return must have a floating-point data type determined
            by :ref:`type-promotion`.

        Examples
        --------
        >>> x = ivy.array([0., 1., 2.])
        >>> y = x.tan()
        >>> print(y)
        ivy.array([0., 1.56, -2.19])
        """
        return ivy.tan(self._data, out=out)

    def tanh(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.tanh. This method simply wraps the
        function, and so the docstring for ivy.tanh also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array whose elements each represent a hyperbolic angle.
            Should have a real-valued floating-point data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the hyperbolic tangent of each element in ``self``.
            The returned array must have a real-valued floating-point data type
            determined by :ref:`type-promotion`.

        Examples
        --------
        >>> x = ivy.array([0., 1., 2.])
        >>> y = x.tanh()
        >>> print(y)
        ivy.array([0., 0.762, 0.964])
        """
        return ivy.tanh(self._data, out=out)

    def trunc(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.trunc. This method simply wraps the
        function, and so the docstring for ivy.trunc also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array. Should have a real-valued data type.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the rounded result for each element in ``self``.
            The returned array must have the same data type as ``self``.
        """
        return ivy.trunc(self._data, out=out)

    def erf(self: ivy.Array, *, out: Optional[ivy.Array] = None) -> ivy.Array:
        """
        ivy.Array instance method variant of ivy.erf. This method simply wraps the
        function, and so the docstring for ivy.erf also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input array to compute exponential for.
        out
            optional output, for writing the result to. It must have a shape that the
            inputs broadcast to.

        Returns
        -------
        ret
            an array containing the Gauss error of ``self``.
        """
        return ivy.erf(self._data, out=out)
