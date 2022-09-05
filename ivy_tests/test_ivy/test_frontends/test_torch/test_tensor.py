# global
import numpy as np
from hypothesis import given, strategies as st

# local
from ivy.functional.frontends.torch import Tensor
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.numpy as ivy_np
import ivy.functional.backends.torch as ivy_torch
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


# add
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=tuple(
            set(ivy_np.valid_float_dtypes).intersection(
                set(ivy_torch.valid_float_dtypes)
            )
        ),
        num_arrays=2,
        min_value=-1e04,
        max_value=1e04,
        allow_inf=False,
    ),
    alpha=st.floats(min_value=-1e06, max_value=1e06, allow_infinity=False),
    num_positional_args=helpers.num_positional_args(
        fn_name="functional.frontends.torch.Tensor.add",
    ),
)
def test_torch_add(
    dtype_and_x,
    alpha,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x
    helpers.test_frontend_array_instance_method(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        frontend_class=Tensor,
        fn_tree="add",
        rtol=1e-04,
        self=np.asarray(x[0], dtype=input_dtype[0]),
        other=np.asarray(x[1], dtype=input_dtype[1]),
        alpha=alpha,
        out=None,
    )


# reshape
@handle_cmd_line_args
@given(
    dtype_value_shape=helpers.dtype_and_values(
        available_dtypes=tuple(
            set(ivy_np.valid_float_dtypes).intersection(
                set(ivy_torch.valid_float_dtypes)
            ),
        ),
        ret_shape=True,
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.Tensor.reshape",
    ),
)
def test_torch_reshape(
    dtype_value_shape,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, value, shape = dtype_value_shape
    helpers.test_frontend_array_instance_method(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        frontend_class=Tensor,
        fn_tree="reshape",
        self=np.asarray(value, dtype=input_dtype),
        shape=shape,
    )
