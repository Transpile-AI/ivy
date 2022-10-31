from hypothesis import given, assume, strategies as st
import ivy_tests.test_array_api.array_api_tests.hypothesis_helpers as hypothesis_helpers
# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


# pixel_shuffle
@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0,
        min_num_dims=4,
        max_num_dims=4,
        min_dim_size=1,
    ),
    factor=st.integers(min_value=1),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.nn.functional.pixel_shuffle"
    ),
)
def test_torch_pixel_shuffle(
    dtype_and_x,
    factor,
    as_variable,
    num_positional_args,
    native_array,
):
    input_dtype, x = dtype_and_x
    input = x[0]
    assume(ivy.shape(input)[1] % (factor**2) == 0)
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend="torch",
        fn_tree="nn.functional.pixel_shuffle",
        input=input,
        upscale_factor=factor,
    )


@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0,
        min_num_dims=4,
        max_num_dims=4,
        min_dim_size=1,
    ),
    factor=st.integers(min_value=1),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.nn.functional.pixel_unshuffle"
    ),
)
def test_torch_pixel_unshuffle(
    dtype_and_x,
    factor,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
):
    input_dtype, x = dtype_and_x
    input = x[0]
    assume((ivy.shape(input)[2] % factor == 0) & (ivy.shape(input)[3] % factor == 0))
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend="torch",
        fn_tree="nn.functional.pixel_unshuffle",
        input=input,
        downscale_factor=factor,
    )


@st.composite
def _pad_helper(draw):
    # 'constant', 'reflect', 'replicate', 'circular'
    mode = draw(st.sampled_from(['replicate']))
    min_v = 1
    max_v = 5
    if mode != 'constant':
        min_v = 3
        if mode == 'reflect':
            max_v = 4
    dtype, input, shape = draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("numeric"),
            ret_shape=True,
            min_num_dims=min_v,
            max_num_dims=max_v,
            min_value=-1e05,
            max_value=1e05
        )
    )
    m = len(shape)
    padding = draw(hypothesis_helpers.tuples(
        st.tuples(
            st.integers(min_value=0, max_value=1),
            st.integers(min_value=0, max_value=1),
        ),
        min_size=m,
        max_size=m,
    ))
    if type(padding[0]) is tuple:
        padding = sum(padding, ())
    if type(padding) is tuple: 
        if (len(padding) == 1):
            padding = padding[0]
    if mode == 'constant':
        value = draw(helpers.ints(min_value=0, max_value=4))
    else:
        value = None
    return dtype, input[0], padding, value, mode


@handle_cmd_line_args
@given(
    dtype_and_input_and_other=_pad_helper(),
)
def test_torch_pad(
    *,
    dtype_and_input_and_other,
    as_variable,
    with_out,
    native_array,
):
    dtype, input, padding, value, mode = dtype_and_input_and_other
    if mode == 'constant':
        helpers.test_frontend_function(
            input_dtypes=dtype,
            as_variable_flags=as_variable,
            with_out=with_out,
            num_positional_args=2,
            native_array_flags=native_array,
            frontend="torch",
            fn_tree="nn.functional.pad",
            input=input,
            padding=padding,
            mode=mode,
            value=value,
        )
    else:
        helpers.test_frontend_function(
            input_dtypes=dtype,
            as_variable_flags=as_variable,
            with_out=with_out,
            num_positional_args=2,
            native_array_flags=native_array,
            frontend="torch",
            fn_tree="nn.functional.pad",
            input=input,
            padding=padding,
            mode=mode,
        )
