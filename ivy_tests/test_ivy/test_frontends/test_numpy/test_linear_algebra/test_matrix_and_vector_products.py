# global
from hypothesis import strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy_tests.test_ivy.test_frontends.test_numpy.helpers as np_frontend_helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test
from ivy_tests.test_ivy.test_functional.test_core.test_linalg import (
    _get_first_matrix_and_dtype,
    _get_second_matrix_and_dtype,
    _get_dtype_value1_value2_axis_for_tensordot,
)




@st.composite
def _get_dtype_value1_value2_axis_for_cross(
    draw,
    available_dtypes,
    min_value=None,
    max_value=None,
    allow_inf=False,
    exclude_min=False,
    exclude_max=False,
    min_num_dims=1,
    max_num_dims=10,
    min_dim_size=1,
    max_dim_size=3,
):
    shape = draw(
        helpers.get_shape(
            allow_none=False,
            min_num_dims=min_num_dims,
            max_num_dims=max_num_dims,
            min_dim_size=min_dim_size,
            max_dim_size=max_dim_size,
        )
    )
    axisa = draw(helpers.ints(min_value=1, max_value=len(shape)))
    axisb = draw(helpers.ints(min_value=1, max_value=len(shape)))
    axisc = draw(helpers.ints(min_value=1, max_value=len(shape)))
    axis = draw(helpers.ints(min_value=1, max_value=len(shape)))
    dtype = draw(st.sampled_from(draw(available_dtypes)))

    values = []
    for i in range(2):
        values.append(
            draw(
                helpers.array_values(
                    dtype=dtype,
                    shape=shape,
                    min_value=min_value,
                    max_value=max_value,
                    allow_inf=allow_inf,
                    exclude_min=exclude_min,
                    exclude_max=exclude_max,
                    large_abs_safety_factor=72,
                    small_abs_safety_factor=72,
                    safety_factor_scale="log",
                )
            )
        )

    value1, value2 = values[0], values[1]
    if not isinstance(axis, list):
        value2 = value2.transpose(
            [k for k in range(len(shape) - axis, len(shape))]
            + [k for k in range(0, len(shape) - axis)]
        )
    return [dtype], value1, value2, axisa, axisb, axisc, axis


# outer
@handle_frontend_test(
    fn_tree="numpy.outer",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_value=-10,
        max_value=10,
        num_arrays=2,
        min_num_dims=1,
        max_num_dims=1,
        shared_dtype=True,
    ),
)
def test_numpy_outer(
    dtype_and_x,
    frontend,
    test_flags,
    fn_tree,
    on_device,
):
    input_dtypes, xs = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        a=xs[0],
        b=xs[1],
    )


# inner
@handle_frontend_test(
    fn_tree="numpy.inner",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_value=-10,
        max_value=10,
        num_arrays=2,
        shared_dtype=True,
    ),
    test_with_out=st.just(False),
)
def test_numpy_inner(
    dtype_and_x,
    frontend,
    test_flags,
    fn_tree,
    on_device,
):
    input_dtypes, xs = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtypes,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        a=xs[0],
        b=xs[1],
    )


# cross
@handle_frontend_test(
    fn_tree="numpy.cross",
    dtype_x1_x2_axis=_get_dtype_value1_value2_axis_for_cross(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=3,
        max_dim_size=3,
        min_value=-1e5,
        max_value=1e5,
        abs_smallest_val=0.01,
        safety_factor_scale="log",
    ),
)
def test_cross(
    *,
    dtype_x1_x2_axis,
    test_flags,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    dtype, x1, x2, axisa, axisb, axisc, axis = dtype_x1_x2_axis
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=dtype,
        test_flags=test_flags,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        rtol_=1e-1,
        atol_=1e-1,
        x1=x1,
        x2=x2,
        axisa=axisa,
        axisb=axisb,
        axisc=axisc,
        axis=axis,
    )


# matmul
@handle_frontend_test(
    fn_tree="numpy.matmul",
    dtypes_values_casting=np_frontend_helpers.dtypes_values_casting_dtype(
        arr_func=[_get_first_matrix_and_dtype, _get_second_matrix_and_dtype],
        get_dtypes_kind="numeric",
    ),
    number_positional_args=np_frontend_helpers.get_num_positional_args_ufunc(
        fn_name="matmul"
    ),
)
def test_numpy_matmul(
    dtypes_values_casting,
    frontend,
    test_flags,
    fn_tree,
    on_device,
):
    dtypes, x, casting, dtype = dtypes_values_casting
    helpers.test_frontend_function(
        input_dtypes=dtypes,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        x1=x[0],
        x2=x[1],
        out=None,
        casting=casting,
        order="K",
        dtype=dtype,
        # The arguments below are currently unused.
        # subok=True,
    )


# matrix_power
@handle_frontend_test(
    fn_tree="numpy.linalg.matrix_power",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0,
        max_value=50,
        shape=helpers.ints(min_value=2, max_value=8).map(lambda x: tuple([x, x])),
    ),
    n=helpers.ints(min_value=1, max_value=8),
    test_with_out=st.just(False),
)
def test_numpy_matrix_power(
    dtype_and_x,
    n,
    frontend,
    test_flags,
    fn_tree,
    on_device,
):
    dtype, x = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtype,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        a=x[0],
        n=n,
    )


# tensordot
@handle_frontend_test(
    fn_tree="numpy.tensordot",
    dtype_values_and_axes=_get_dtype_value1_value2_axis_for_tensordot(
        helpers.get_dtypes(kind="numeric")
    ),
    test_with_out=st.just(False),
)
def test_numpy_tensordot(
    dtype_values_and_axes,
    frontend,
    test_flags,
    fn_tree,
):
    dtype, a, b, axes = dtype_values_and_axes
    helpers.test_frontend_function(
        input_dtypes=dtype,
        frontend=frontend,
        test_flags=test_flags,
        fn_tree=fn_tree,
        a=a,
        b=b,
        axes=axes,
    )


# kron
@handle_frontend_test(
    fn_tree="numpy.kron",
    dtype_and_x=helpers.dtype_and_values(
        num_arrays=2,
        allow_inf=True,
        allow_nan=True,
        shared_dtype=True,
    ),
)
def test_numpy_kron(
    *,
    dtype_and_x,
    frontend,
    fn_tree,
    on_device,
    test_flags,
):
    dtypes, xs = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=dtypes,
        frontend=frontend,
        fn_tree=fn_tree,
        on_device=on_device,
        test_flags=test_flags,
        a=xs[0],
        b=xs[1],
    )
