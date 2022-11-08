from hypothesis import given
# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


# split
@handle_cmd_line_args
@given(
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.numpy.split"
    ),
    dtype_and_x=helpers.dtype_and_values(
        dtype_i=helpers.get_dtypes("numeric", full=False, none=True),
        dtype_ar=helpers.get_dtypes("numeric", full=False, none=True),
        dtype_ax=helpers.get_dtypes("numeric", full=False, none=True),
        dtype_id=helpers.get_dtypes("numeric", full=False, none=True),
    ),
)
def test_numpy_split(
    as_variable,
    dtype_and_x,
    num_positional_args,
):
    indices_or_sections, ary, axis, input_dtypes = dtype_and_x
    helpers.test_frontend_function(
        as_variable_flags=as_variable,
        input_dtypes=input_dtypes,
        with_out=False,
        num_positional_args=num_positional_args,
        frontend="numpy",
        fn_tree="split",
        ary=ary[0],
        axis=axis,
        indices_or_sections=indices_or_sections[0],
    )
