# global
import sys
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


# qr
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float", index=1, full=True),
        min_num_dims=2,
        max_num_dims=2,
        min_dim_size=2,
        max_dim_size=5,
        min_value=2,
        max_value=5,
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.jax.lax.linalg.qr"
    ),
    full_matrices=st.booleans(),
)
def test_jax_qr(
    dtype_and_x,
    full_matrices,
    as_variable,
    native_array,
    num_positional_args,
    fw,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=[dtype],
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="jax",
        fn_tree="lax.linalg.qr",
        rtol=1e-02,
        x=np.array(x, dtype=dtype),
        full_matrices=full_matrices
    )