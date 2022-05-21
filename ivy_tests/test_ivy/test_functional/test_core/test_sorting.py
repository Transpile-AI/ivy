"""Collection of tests for sorting functions."""

# global
from hypothesis import given, strategies as st
import numpy as np

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.numpy as ivy_np


# argsort
@given(
    array_shape=helpers.lists(
        st.integers(1, 5), min_size="num_dims", max_size="num_dims", size_bounds=[1, 5]
    ),
    dtype=st.sampled_from(ivy_np.valid_dtype_strs),
    data=st.data(),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 4),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_argsort(
    array_shape,
    dtype,
    data,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    # smoke for torch
    if fw == "torch" and dtype in ["uint16", "uint32", "uint64"]:
        return

    # we do not want any nans
    x = data.draw(
        helpers.nph.arrays(shape=array_shape, dtype=dtype).filter(
            lambda x: not np.any(np.isnan(x))
        )
    )

    ndim = len(x.shape)
    axis = data.draw(st.integers(-ndim, ndim - 1))
    descending = data.draw(st.booleans())
    stable = data.draw(st.booleans())

    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "argsort",
        x=x,
        axis=axis,
        descending=descending,
        stable=stable,
    )


# sort
@given(
    array_shape=helpers.lists(
        st.integers(1, 5), min_size="num_dims", max_size="num_dims", size_bounds=[1, 5]
    ),
    dtype=st.sampled_from(ivy_np.valid_dtype_strs),
    data=st.data(),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    num_positional_args=st.integers(0, 4),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_sort(
    array_shape,
    dtype,
    data,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    # smoke for torch
    if fw == "torch" and dtype in ["uint16", "uint32", "uint64"]:
        return

    # we do not want any nans
    x = data.draw(
        helpers.nph.arrays(shape=array_shape, dtype=dtype).filter(
            lambda x: not np.any(np.isnan(x))
        )
    )

    ndim = len(x.shape)
    axis = data.draw(st.integers(-ndim, ndim - 1))
    descending = data.draw(st.booleans())
    stable = data.draw(st.booleans())

    helpers.test_array_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "sort",
        x=x,
        axis=axis,
        descending=descending,
        stable=stable,
    )
