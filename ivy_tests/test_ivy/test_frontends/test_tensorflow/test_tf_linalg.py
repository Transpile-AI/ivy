# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.tensorflow as ivy_tf


@st.composite
def _det_arrays(draw):
    arbitrary_dims = draw(st.lists(st.integers(min_value=1)))
    m = draw(st.integers(min_value=1, max_value=100))
    shape = (*arbitrary_dims, m, m)
    return draw(
        helpers.dtype_and_values(
            available_dtypes=ivy_tf.valid_float_dtypes,
            shape=shape,
        )
    )


@given(
    dtype_and_input=_det_arrays(),
    as_variable=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.tensorflow.det"
    ),
    native_array=st.booleans(),
)
def test_tensorflow_det(
    dtype_and_input, as_variable, num_positional_args, native_array, fw
):
    input_dtype, x = dtype_and_input
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="tensorflow",
        fn_name="linalg.det",
        rtol=1e-5,
        test_values=False,
        input=np.asarray(x, dtype=input_dtype),
    )
