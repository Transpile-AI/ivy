import ivy
from ivy.functional.ivy.extensions import (
    _verify_coo_components,
    _verify_csr_components,
    _is_data_not_indices_values_and_shape,
    _is_coo_not_csr,
)
import tensorflow as tf
import logging


def is_native_sparse_array(x):
    return isinstance(x, tf.SparseTensor)


def native_sparse_array(
    data=None,
    *,
    coo_indices=None,
    csr_crow_indices=None,
    csr_col_indices=None,
    values=None,
    dense_shape=None
):
    if _is_data_not_indices_values_and_shape(
        data, coo_indices, csr_crow_indices, csr_col_indices, values, dense_shape
    ):
        ivy.assertions.check_true(
            ivy.is_native_sparse_array(data), message="not a sparse array"
        )
        return data
    elif _is_coo_not_csr(
        coo_indices, csr_crow_indices, csr_col_indices, values, dense_shape
    ):
        _verify_coo_components(
            indices=coo_indices, values=values, dense_shape=dense_shape
        )
        return tf.SparseTensor(
            indices=coo_indices, values=values, dense_shape=dense_shape
        )
    else:
        _verify_csr_components(
            crow_indices=csr_crow_indices,
            col_indices=csr_col_indices,
            values=values,
            dense_shape=dense_shape,
        )
        logging.warning(
            "Tensorflow does not support CSR sparse array natively. None is returned."
        )
        return None


def native_sparse_array_to_indices_values_and_shape(x):
    if isinstance(x, tf.SparseTensor):
        return x.indices, x.values, x.dense_shape
    raise ivy.exceptions.IvyException("not a SparseTensor")

    
@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
def conv_transpose(
    x: Union[tf.Tensor, tf.Variable],
    filters: Union[int, float],
    strides: Union[int, float],
    padding: Union[int, float],
    output_shape: Optional[Union[ivy.Shape, ivy.NativeShape]] = None,
    data_format: str = "NCDHW",
    dilations: int = 1,
    /,
    *,
    dtype: tf.Dtype,
    device: str,
    out: [Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.experimental.numpy.conv_transpose(
        x, filters, strides, padding, output_shape, data_format, dilations, dtype=dtype
    )
