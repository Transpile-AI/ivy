# global
import numpy as np
import sys
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.numpy as ivy_np
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


@st.composite
def _solve_get_dtype_and_data(draw):
    batch = draw(st.integers(min_value=1, max_value=5))
    random_size = draw(st.integers(min_value=2, max_value=4))
    # shape = (batch, random_size, random_size)

    input_dtype = draw(
        st.shared(st.sampled_from(ivy_np.valid_float_dtypes), key="shared_dtype")
    )
    shape = (random_size, random_size)
    tmp = []
    for i in range(batch):
        tmp.append(
            draw(
                helpers.array_values(
                    dtype=input_dtype,
                    shape=shape,
                    min_value=-10,
                    max_value=10,
                ).filter(lambda x: np.linalg.cond(x) < 1 / sys.float_info.epsilon)
            )
        )

    data1 = (input_dtype, tmp)

    shape = (batch, random_size, draw(st.integers(min_value=2, max_value=4)))
    data2 = draw(
        helpers.dtype_and_values(
            available_dtypes=ivy_np.valid_float_dtypes,
            shape=shape,
            min_value=-10,
            max_value=10,
        )
    )

    return data1, data2


# solve
@handle_cmd_line_args
@given(
    dtype_and_x=_solve_get_dtype_and_data(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.numpy.solve"
    ),
)
def test_numpy_solve(
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):

    data1, data2 = dtype_and_x
    input_dtype1, x = data1
    input_dtype2, y = data2

    helpers.test_frontend_function(
        input_dtypes=[input_dtype1, input_dtype2],
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="numpy",
        fn_tree="linear_algebra.linalg.solve",
        x=np.asarray(x, dtype=input_dtype1),
        y=np.asarray(y, dtype=input_dtype2),
    )
