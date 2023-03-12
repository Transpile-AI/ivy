# global
from hypothesis import strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


@st.composite
def _extract_patches_helper(draw):
    sizes = [
        1,
        draw(st.integers(min_value=1, max_value=5)),
        draw(st.integers(min_value=1, max_value=5)),
        1,
    ]
    rates = [
        1,
        draw(st.integers(min_value=1, max_value=5)),
        draw(st.integers(min_value=1, max_value=5)),
        1,
    ]
    x_dim = []
    for i in range(1, 3):
        min_x = sizes[i] + (sizes[i] - 1) * (rates[i] - 1)
        x_dim.append(draw(st.integers(min_x, min_x + 5)))
    x_shape = [
        draw(st.integers(min_value=1, max_value=5)),
        *x_dim,
        draw(st.integers(min_value=1, max_value=5)),
    ]
    dtype_x = draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("numeric"),
            shape=x_shape,
        )
    )
    strides = [
        1,
        draw(st.integers(min_value=1, max_value=5)),
        draw(st.integers(min_value=1, max_value=5)),
        1,
    ]
    padding = draw(st.sampled_from(["VALID", "SAME"]))
    return dtype_x, sizes, strides, rates, padding


# extract_patches
@handle_frontend_test(
    fn_tree="tensorflow.image.extract_patches",
    dtype_values_and_other=_extract_patches_helper(),
    test_with_out=st.just(False),
)
def test_tensorflow_extract_patches(
    *,
    dtype_values_and_other,
    frontend,
    test_flags,
    fn_tree,
    on_device,
):
    (x_dtype, x), sizes, strides, rates, padding = dtype_values_and_other
    helpers.test_frontend_function(
        input_dtypes=x_dtype,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        images=x[0],
        sizes=sizes,
        strides=strides,
        rates=rates,
        padding=padding,
    )
