# global
from hypothesis import strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


# cross_entropy
@handle_frontend_test(
    fn_tree="torch.nn.functional.cross_entropy",
    dtype_and_input=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        allow_inf=False,
        min_num_dims=2,
        max_num_dims=2,
        min_dim_size=1,
    ),
    dtype_and_target=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0.0,
        max_value=1.0,
        allow_inf=False,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    dtype_and_weights=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        allow_inf=False,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    size_average=st.booleans(),
    reduce=st.booleans(),
    reduction=st.sampled_from(["mean", "none", "sum"]),
    label_smoothing=helpers.floats(min_value=0, max_value=0.49),
)
def test_torch_cross_entropy(
    *,
    dtype_and_input,
    dtype_and_target,
    dtype_and_weights,
    size_average,
    reduce,
    reduction,
    label_smoothing,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    inputs_dtype, input = dtype_and_input
    target_dtype, target = dtype_and_target
    weights_dtype, weights = dtype_and_weights
    helpers.test_frontend_function(
        input_dtypes=inputs_dtype + target_dtype + weights_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=input[0],
        target=target[0],
        weight=weights[0].reshape(-1),
        size_average=size_average,
        reduce=reduce,
        reduction=reduction,
        label_smoothing=label_smoothing,
    )


# binary_cross_entropy
@handle_frontend_test(
    fn_tree="torch.nn.functional.binary_cross_entropy",
    dtype_and_true=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0.0,
        max_value=1.0,
        large_abs_safety_factor=2,
        small_abs_safety_factor=2,
        safety_factor_scale="linear",
        allow_inf=False,
        exclude_min=True,
        exclude_max=True,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    dtype_and_pred=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=1.0013580322265625e-05,
        max_value=1.0,
        large_abs_safety_factor=2,
        small_abs_safety_factor=2,
        safety_factor_scale="linear",
        allow_inf=False,
        exclude_min=True,
        exclude_max=True,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    dtype_and_weight=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=1.0013580322265625e-05,
        max_value=1.0,
        allow_inf=False,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    size_average=st.booleans(),
    reduce=st.booleans(),
    reduction=st.sampled_from(["mean", "none", "sum", None]),
)
def test_torch_binary_cross_entropy(
    *,
    dtype_and_true,
    dtype_and_pred,
    dtype_and_weight,
    size_average,
    reduce,
    reduction,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    pred_dtype, pred = dtype_and_pred
    true_dtype, true = dtype_and_true
    weight_dtype, weight = dtype_and_weight
    helpers.test_frontend_function(
        input_dtypes=[pred_dtype[0], true_dtype[0], weight_dtype[0]],
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        input=pred[0],
        target=true[0],
        weight=weight[0],
        size_average=size_average,
        reduce=reduce,
        reduction=reduction,
    )
