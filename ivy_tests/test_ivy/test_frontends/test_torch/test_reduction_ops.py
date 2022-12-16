# global
from hypothesis import strategies as st

import ivy

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test
from ivy_tests.test_ivy.test_functional.test_core.test_statistical import (
    statistical_dtype_values,
)


@handle_frontend_test(
    fn_tree="torch.dist",
    dtype_and_input=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        num_arrays=2,
        shared_dtype=True,
        allow_inf=False,
    ),
    p=helpers.floats(min_value=1.0, max_value=10.0),
)
def test_torch_dist(
    *,
    dtype_and_input,
    p,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, input = dtype_and_input
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=input[0],
        other=input[1],
        p=p,
    )


@handle_frontend_test(
    fn_tree="torch.argmax",
    dtype_input_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        force_int_axis=True,
        min_num_dims=1,
        min_axis=-1,
        max_axis=0,
    ),
    keepdims=st.booleans(),
)
def test_torch_argmax(
    *,
    dtype_input_axis,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_input_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.argmin",
    dtype_input_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        force_int_axis=True,
        min_num_dims=1,
        min_axis=-1,
        max_axis=0,
    ),
    keepdims=st.booleans(),
)
def test_torch_argmin(
    *,
    dtype_input_axis,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_input_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.amax",
    dtype_input_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        min_axis=-1,
        max_axis=0,
    ),
    keepdims=st.booleans(),
)
def test_torch_amax(
    *,
    dtype_input_axis,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_input_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.amin",
    dtype_input_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        min_axis=-1,
        max_axis=0,
    ),
    keepdims=st.booleans(),
)
def test_torch_amin(
    *,
    dtype_input_axis,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_input_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.all",
    dtype_input_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        allow_inf=False,
    ),
    keepdims=st.booleans(),
)
def test_torch_all(
    *,
    dtype_input_axis,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_input_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.any",
    dtype_input_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("valid"),
        min_axis=-1,
        max_axis=0,
        min_num_dims=1,
        allow_inf=False,
    ),
    keepdims=st.booleans(),
)
def test_torch_any(
    *,
    dtype_input_axis,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_input_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.sum",
    dtype_and_x=statistical_dtype_values(function="sum"),
    keepdims=st.booleans(),
)
def test_torch_sum(
    *,
    dtype_and_x,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.mean",
    dtype_and_x=statistical_dtype_values(function="mean"),
    keepdims=st.booleans(),
)
def test_torch_mean(
    *,
    dtype_and_x,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        rtol=1e-04,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.nanmean",
    dtype_and_x=statistical_dtype_values(function="nanmean"),
    keepdims=st.booleans(),
)
def test_torch_nanmean(
    *,
    dtype_and_x,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.std",
    dtype_and_x=statistical_dtype_values(function="std"),
    keepdims=st.booleans(),
)
def test_torch_std(
    *,
    dtype_and_x,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis, correction = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        unbiased=bool(correction),
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.prod",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        max_num_dims=5,
        valid_axis=True,
        allow_neg_axes=False,
        max_axes_size=1,
        force_int_axis=True,
    ),
    dtype=helpers.get_dtypes("numeric", none=True, full=False),
    keepdims=st.booleans(),
)
def test_torch_prod(
    *,
    dtype_x_axis,
    dtype,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        dtype=dtype[0],
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.var",
    dtype_and_x=statistical_dtype_values(function="var"),
    keepdims=st.booleans(),
)
def test_torch_var(
    *,
    dtype_and_x,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis, correction = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        unbiased=bool(correction),
        keepdim=keepdims,
    )


# ToDo, fails for TensorFlow backend, tf.reduce_min doesn't support bool
# ToDo, fails for torch backend, tf.argmin_cpu doesn't support bool
@handle_frontend_test(
    fn_tree="torch.argmin",
    dtype_input_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        valid_axis=True,
        force_int_axis=True,
    ),
    keepdim=st.booleans(),
)
def test_torch_min(
    *,
    dtype_input_axis,
    keepdim,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_input_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdim,
    )


# moveaxis
@handle_frontend_test(
    fn_tree="torch.moveaxis",
    dtype_and_a=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=-100,
        max_value=100,
        shape=st.shared(
            helpers.get_shape(
                min_num_dims=1,
                max_num_dims=3,
                min_dim_size=1,
                max_dim_size=3,
            ),
            key="a_s_d",
        ),
    ),
    source=helpers.get_axis(
        allow_none=False,
        unique=True,
        shape=st.shared(
            helpers.get_shape(
                min_num_dims=1,
                max_num_dims=3,
                min_dim_size=1,
                max_dim_size=3,
            ),
            key="a_s_d",
        ),
        min_size=1,
        force_int=True,
    ),
    destination=helpers.get_axis(
        allow_none=False,
        unique=True,
        shape=st.shared(
            helpers.get_shape(
                min_num_dims=1,
                max_num_dims=3,
                min_dim_size=1,
                max_dim_size=3,
            ),
            key="a_s_d",
        ),
        min_size=1,
        force_int=True,
    ),
)
def test_torch_moveaxis(
    *,
    dtype_and_a,
    source,
    destination,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, a = dtype_and_a
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=a[0],
        source=source,
        destination=destination,
    )


@handle_frontend_test(
    fn_tree="torch.max",
    dtype_input_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        valid_axis=True,
        force_int_axis=True,
    ),
    keepdim=st.booleans(),
)
def test_torch_max(
    *,
    dtype_input_axis,
    keepdim,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis = dtype_input_axis
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        keepdim=keepdim,
    )


@handle_frontend_test(
    fn_tree="torch.std_mean",
    dtype_and_x=statistical_dtype_values(function="std_mean"),
    keepdims=st.booleans(),
)
def test_torch_std_mean(
    *,
    dtype_and_x,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x, axis, correction = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=x[0],
        dim=axis,
        unbiased=bool(correction),
        keepdim=keepdims,
    )


@handle_frontend_test(
    fn_tree="torch.unique",
    dtype_and_values=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("integer"),
        min_num_dims=1,
        shape=st.shared(
            helpers.get_shape(
                min_num_dims=1,
                max_num_dims=5,
                min_dim_size=1,
                max_dim_size=5,
            ),
            key="shape",
        ),
    ).filter(lambda x: "bfloat16" not in x[0] and "float16" not in x[0]),
    sorted=st.booleans(),
    return_inverse=st.booleans(),
    return_counts=st.booleans(),
)
def test_torch_unique(
    *,
    dtype_and_values,
    sorted,
    return_inverse,
    return_counts,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    input_dtype, x = dtype_and_values
    ret, ret_gt = helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=False,
        input=x[0],
        sorted=sorted,
        return_inverse=return_inverse,
        return_counts=return_counts,
        dim=None,
    )

    ivy.set_backend(frontend)

    def _sort_inverse_indices(unique_values):
        _inverse_indices = ivy.zeros_like(x[0])
        for idx, val in enumerate(unique_values):
            _inverse_indices[x[0] == val] = idx

        return _inverse_indices

    def _sort_output_tuple(unique_tuple):
        values_sorted_idx = ivy.argsort(unique_tuple[0])
        output = [ivy.take_along_axis(unique_tuple[0], values_sorted_idx, -1)]

        for idx in range(1, len(unique_tuple)):
            item = unique_tuple[idx]

            if values_sorted_idx.shape == item.shape:
                output.append(ivy.take_along_axis(item, values_sorted_idx, -1))
            else:
                output.append(_sort_inverse_indices(output[0]))

        return tuple(output)

    assert len(ret) == len(ret_gt)

    x[0] = ivy.array(x[0])
    ret = [ivy.array(r) for r in ret]
    ret_gt = [ivy.array(r) for r in ret_gt]

    if not sorted:
        # manually sort both tuples so to check their equality
        ret = _sort_output_tuple(ret)
        ret_gt = _sort_output_tuple(ret_gt)

    for i in range(len(ret)):
        helpers.assert_same_type_and_shape([ret[i], ret_gt[i]])
        helpers.assert_all_close(ret[i], ret_gt[i])

    ivy.unset_backend()
