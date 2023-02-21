# global
from hypothesis import strategies as st, assume

# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test
from ivy_tests.test_ivy.test_functional.test_experimental.test_core.test_manipulation import (  # noqa
    _get_split_locations,
)


# hsplit
@handle_frontend_test(
    fn_tree="numpy.hsplit",
    dtype_value=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"),
        shape=st.shared(helpers.get_shape(min_num_dims=1), key="value_shape"),
    ),
    indices_or_sections=_get_split_locations(min_num_dims=1, axis=1),
    test_with_out=st.just(False),
)
def test_numpy_hsplit(
    *,
    dtype_value,
    indices_or_sections,
    on_device,
    fn_tree,
    frontend,
    test_flags,
):
    input_dtype, value = dtype_value
    # TODO: remove the assumption when these bugfixes are merged and version-pinned
    # https://github.com/tensorflow/tensorflow/pull/59523
    # https://github.com/google/jax/pull/14275
    assume(
        not (
            len(value[0].shape) == 1
            and ivy.current_backend_str() in ("tensorflow", "jax")
        )
    )
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        ary=value[0],
        indices_or_sections=indices_or_sections,
    )
