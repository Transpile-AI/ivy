import ivy

from hypothesis import given, assume, strategies as st
from ivy.functional.backends.numpy.data_type import dtype

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


# hann_window


@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric")
    ),
    # generate pereodic boolean
    peroidic=st.booleans(),
    dtype=helpers.get_dtypes("float", full=False, none=True),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.signal.hann_window"
    ),
)
def test_tensorflow_hann_window(
    dtype_and_x,
    dtype,
    periodic,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x

    # test if periodic is a boolean
    if periodic is not None:
        assume(isinstance(periodic, bool))

    as_variable, native_array = helpers.handle_where_and_array_bools(
        input_dtype=input_dtype,
        as_variable=as_variable,
        native_array=native_array,
    )
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_tree="hann_window",
        window_length=x[0],
        periodic=periodic,
        dtype=dtype[0],
    )
