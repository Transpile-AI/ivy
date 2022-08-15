# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.numpy as ivy_np
import ivy.functional.backends.torch as ivy_torch


# composite the generation of ints of valid dtypes and tuple(int)
# that shares the same size as input shape
@st.composite
def _roll_helper(draw):
    return draw(
        helpers.ints()
        | helpers.get_axis(
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="shape"),
        ret_tuple=True,
          ),
    )


# roll
@given(
    dtype_and_values=helpers.dtype_and_values(
        available_dtypes=tuple(
            set(ivy_np.valid_float_dtypes).intersection(
                set(ivy_torch.valid_float_dtypes))
        ),
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="shape"),
    ),
    shift=_roll_helper(),
    dims=helpers.get_axis(
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="shape"),
        allow_none=True,
    ),
    as_variable=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.roll"
    ),
    native_array=st.booleans(),
)
def test_torch_roll(
    dtype_and_values,
    shifts,
    dims,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, value = dtype_and_values
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="roll",
        input=np.asarray(value, dtype=input_dtype),
        shifts=shifts,
        dims=dims,
    )
