# global
import abc
from typing import List

# local
import ivy


class NestedArray(abc.ABC):
    """
    Base class for nested array objects.
    """

    def __init__(self, data, dtype, device, internal=False):
        if not internal:
            raise RuntimeError(
                "NestedArray is an abstract class "
                "and should not be instantiated directly."
                "Please use one of the factory methods instead"
            )
        self._data = data
        self._shape = self._genearate_shape()
        self._dtype = dtype
        self._device = device
        self._pre_repr = "ivy."

    def _genearate_shape(
        self,
    ):
        final_shape = [len(self._data)]
        shapes = list()
        ndims = list()
        for arr in self._data:
            shapes.append(arr.shape)
            ndims.append(arr.ndim)
        if ndims.count(ndims[0]) != len(ndims):
            raise RuntimeError(
                "All arrays in a nested array must have the same number of dimensions."
            )
        for i in range(ndims[0]):
            same_shape = True
            current_shape = shapes[0][i]
            for j in range(final_shape[0]):
                if shapes[j][i] != current_shape:
                    same_shape = False
                    break
            if same_shape:
                final_shape.append(current_shape)
            else:
                final_shape.append(None)
        return final_shape

    @classmethod
    def nested_array(cls, data, dtype=None, device=None):
        dtype = ivy.default_dtype(dtype=dtype, item=data)
        if ivy.is_ivy_array(data):
            data = [data]
        elif isinstance(data, (list, tuple)) or ivy.is_native_array(data):
            data = ivy.to_ivy(data)
        # TODo: add support for nested arrays
        # ToDo: adjust dtype and device with nested_map
        else:
            raise TypeError(
                "Input data must be ivy.Array, ivy.NativeArray"
                " or a list of either, got: {}".format(type(data))
            )
        return cls(data, dtype, device, internal=True)

    # Properties #
    # ---------- #

    @property
    def data(self) -> ivy.NativeArray:
        """The native array being wrapped in self."""
        return self._data

    @property
    def dtype(self) -> ivy.Dtype:
        """Data type of the array elements"""
        return self._dtype

    @property
    def device(self) -> ivy.Device:
        """Hardware device the array data resides on."""
        return self._device

    @property
    def shape(self) -> List:
        """Array dimensions."""
        return self._shape

    @property
    def ndim(self) -> int:
        """Number of array dimensions (axes)."""
        return len(tuple(self._shape))

    # Built-ins #
    # ----------#

    def __repr__(self):
        arrays_repr = "\t"
        for i in range(self.ndim - 1):
            arrays_repr += repr(self._data[i]) + "\n\t"
        arrays_repr += repr(self._data[-1])
        return self._pre_repr + self.__class__.__name__ + "([\n" + arrays_repr + "\n])"
