# global
# local
import numpy as np
from hypothesis import strategies as st

import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_test


# Helpers #
# ------- #


@st.composite
def statistical_dtype_values(draw, *, function):
    large_abs_safety_factor = 2
    small_abs_safety_factor = 2
    if function in ["mean", "median", "std", "var"]:
        large_abs_safety_factor = 24
        small_abs_safety_factor = 24
    dtype, values, axis = draw(
        helpers.dtype_values_axis(
            available_dtypes=helpers.get_dtypes("float"),
            large_abs_safety_factor=large_abs_safety_factor,
            small_abs_safety_factor=small_abs_safety_factor,
            safety_factor_scale="log",
            min_num_dims=1,
            max_num_dims=5,
            min_dim_size=2,
            valid_axis=True,
            allow_neg_axes=False,
            min_axes_size=1,
        )
    )
    shape = values[0].shape
    size = values[0].size
    max_correction = np.min(shape)
    if function == "var" or function == "std":
        if size == 1:
            correction = 0
        elif isinstance(axis, int):
            correction = draw(
                helpers.ints(min_value=0, max_value=shape[axis] - 1)
                | helpers.floats(min_value=0, max_value=shape[axis] - 1)
            )
            return dtype, values, axis, correction
        else:
            correction = draw(
                helpers.ints(min_value=0, max_value=max_correction - 1)
                | helpers.floats(min_value=0, max_value=max_correction - 1)
            )
        return dtype, values, axis, correction

    if function == "quantile":
        q = draw(
            helpers.array_values(
                dtype=helpers.get_dtypes("float"),
                shape=helpers.get_shape(min_dim_size=1, max_num_dims=1, min_num_dims=1),
                min_value=0.0,
                max_value=1.0,
                exclude_max=False,
                exclude_min=False,
            )
        )

        interpolation_names = ["linear", "lower", "higher", "midpoint", "nearest"]
        interpolation = draw(
            helpers.lists(
                arg=st.sampled_from(interpolation_names), min_size=1, max_size=1
            )
        )
        return dtype, values, axis, interpolation, q

    return dtype, values, axis


# TODO: numpy does not support bfloat16
# TODO: put this function inside statistical_dtype_values if needed
@st.composite
def _statistical_dtype_xs_bins_range_axis_castable(draw, n: int = 2):
    available_dtypes = draw(helpers.get_dtypes(kind="float"))
    if "bfloat16" in available_dtypes:
        available_dtypes.remove("bfloat16")
    shape = draw(helpers.get_shape(min_num_dims=1, min_dim_size=2))
    dtype, values = draw(
        helpers.dtype_and_values(
            available_dtypes=available_dtypes,
            num_arrays=n,
            large_abs_safety_factor=2,
            small_abs_safety_factor=2,
            safety_factor_scale="log",
            shape=shape,
            shared_dtype=True,
        )
    )
    axis = draw(helpers.get_axis(shape=shape, force_int=True))
    dtype1, dtype2 = draw(helpers.get_castable_dtype(available_dtypes, dtype[0]))
    bins = draw(
        helpers.array_values(
            dtype=dtype1, min_value=0, shape=draw(helpers.get_shape(max_num_dims=1))
        )
    )
    range = (0, 0)
    if bins.size == 1:
        while range[0] == range[1]:
            range = (
                draw(
                    st.floats(
                        allow_nan=False, allow_infinity=False, allow_subnormal=False
                    )
                ),
                draw(
                    st.floats(
                        allow_nan=False, allow_infinity=False, allow_subnormal=False
                    )
                ),
            )
        range = sorted(range)
        return dtype1, values, int(bins), range, axis, dtype2
    else:
        bins = sorted(bins)
        range = None
        return dtype1, values, bins, range, axis, dtype2


@handle_test(
    fn_tree="functional.ivy.experimental.histogram",
    private_data_generated=_statistical_dtype_xs_bins_range_axis_castable(),
    extend_lower_interval=st.booleans(),
    extend_upper_interval=st.booleans(),
    density=st.booleans(),
)
def test_histogram(
    *,
    private_data_generated,
    extend_lower_interval,
    extend_upper_interval,
    density,
):
    input_dtype, values, bins, range, axis, castable = private_data_generated
    helpers.test_function(
        a=values[0],
        bins=bins,
        axis=axis,
        extend_lower_interval=extend_lower_interval,
        extend_upper_interval=extend_upper_interval,
        dtype=castable,
        range=range,
        weights=values[1],
        density=density,
        input_dtypes=input_dtype,
    )


@handle_test(
    fn_tree="functional.ivy.experimental.median",
    dtype_x_axis=statistical_dtype_values(function="median"),
    keep_dims=st.booleans(),
    test_gradients=st.just(False),
)
def test_median(
    *,
    dtype_x_axis,
    keep_dims,
    num_positional_args,
    as_variable,
    with_out,
    native_array,
    container_flags,
    instance_method,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=input_dtype,
        num_positional_args=num_positional_args,
        as_variable_flags=as_variable,
        with_out=with_out,
        native_array_flags=native_array,
        container_flags=container_flags,
        instance_method=instance_method,
        on_device=on_device,
        fw=backend_fw,
        fn_name=fn_name,
        input=x[0],
        axis=axis,
        keepdims=keep_dims,
    )


# nanmean
@handle_test(
    fn_tree="functional.ivy.experimental.nanmean",
    dtype_x_axis=statistical_dtype_values(function="nanmean"),
    keep_dims=st.booleans(),
    dtype=helpers.get_dtypes("float", full=False),
    test_gradients=st.just(False),
)
def test_nanmean(
    *,
    dtype_x_axis,
    keep_dims,
    dtype,
    test_flags,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=input_dtype,
        test_flags=test_flags,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        a=x[0],
        axis=axis,
        keepdims=keep_dims,
        dtype=dtype[0],
    )


# unravel_index
@st.composite
def max_value_as_shape_prod(draw):
    shape = draw(
        helpers.get_shape(
            min_num_dims=1,
            max_num_dims=5,
            min_dim_size=1,
            max_dim_size=5,
        )
    )
    dtype_and_x = draw(
        helpers.dtype_values_axis(
            available_dtypes=helpers.get_dtypes("integer"),
            min_value=0,
            max_value=np.prod(shape) - 1,
        )
    )
    return dtype_and_x, shape


@handle_test(
    fn_tree="functional.ivy.experimental.unravel_index",
    dtype_x_shape=max_value_as_shape_prod(),
    test_gradients=st.just(False),
)
def test_unravel_index(
    dtype_x_shape,
    test_flags,
    backend_fw,
    fn_name,
    ground_truth_backend,
):
    dtype_and_x, shape = dtype_x_shape
    input_dtype, x = dtype_and_x[0], dtype_and_x[1]
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=input_dtype,
        test_flags=test_flags,
        fw=backend_fw,
        fn_name=fn_name,
        indices=np.asarray(x[0], dtype=input_dtype[0]),
        shape=shape,
    )


# quantile


@handle_test(
    fn_tree="functional.ivy.experimental.quantile",
    dtype_and_x=statistical_dtype_values(function="quantile"),
    keep_dims=st.booleans(),
    num_positional_args=helpers.num_positional_args(fn_name="quantile"),
    test_gradients=st.just(False),
)
def test_quantile(
    *,
    dtype_and_x,
    keep_dims,
    as_variable,
    num_positional_args,
    native_array,
    container_flags,
    with_out,
    instance_method,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    input_dtype, x, axis, interpolation, q = dtype_and_x
    helpers.test_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container_flags,
        instance_method=instance_method,
        ground_truth_backend=ground_truth_backend,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        a=x[0],
        q=q,
        axis=axis,
        interpolation=interpolation[0],
        keepdims=keep_dims,
    )
