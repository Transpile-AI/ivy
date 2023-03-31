# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


# fft
@handle_frontend_test(
    fn_tree="jax.numpy.fft.fft",
    dtype_and_x=helpers.dtype_and_values(available_dtypes=helpers.get_dtypes("float"),
                                         array_api_dtypes=True,
                                         shape=helpers.ints(min_value=2).
                                         map(lambda x: tuple([x, ])))
    .filter(
        lambda x: "bfloat16" not in x[0]
        and "float16" not in x[0]
    )
)
def test_jax_numpy_fft(
    dtype_and_x,
    frontend,
    fn_tree,
    test_flags,
    on_device
):
    input_dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=True,
        a=x[0]
    )
