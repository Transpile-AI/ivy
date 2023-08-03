# global
# from hypothesis import strategies as st


# local
# TODO: uncomment after frontend is not required
#  to be set as backend in test_frontend_function

# import ivy_tests.test_ivy.helpers as helpers
# from ivy_tests.test_ivy.helpers import handle_frontend_test
#
# #dropout2d
# @handle_frontend_test(
#     fn_tree="mindspore.ops.function.nn_func.dropout2d",
#     d_type_and_x=helpers.dtype_and_values(
#         available_dtypes=helpers.get_dtypes("valid"),
#         num_arrays=1,
#         shared_dtype=True,
#         min_value=2,
#         max_value=5,
#         min_dim_size=4,
#         shape=(
#             st.integers(min_value=2, max_value=10),
#             4,
#             st.integers(min_value=12, max_value=64),
#             st.integers(min_value=12, max_value=64),
#         ),
#     ),
#     p=st.floats(min_value=0.0, max_value=1.0),
#     training=st.booleans(),
# )
# def test_mindspore_dropout2d(
#     *,
#     d_type_and_x,
#     p,
#     training,
#     on_device,
#     fn_tree,
#     frontend,
#     test_flags,
# ):
#     dtype, x = d_type_and_x
#     helpers.test_frontend_function(
#         input_dtypes=dtype,
#         frontend=frontend,
#         test_flags=test_flags,
#         fn_tree=fn_tree,
#         on_device=on_device,
#         input=x[0],
#         p=p,
#         training=training,
#     )


# selu
# @handle_frontend_test(
#     fn_tree="mindspore.ops.function.nn_func.selu",
#     dtype_and_x=helpers.dtype_and_values(
#         available_dtypes=helpers.get_dtypes("valid"),
#         safety_factor_scale="log",
#         small_abs_safety_factor=20,
#     ),
# )
# def test_mindspore_selu(
#     *,
#     dtype_and_x,
#     on_device,
#     fn_tree,
#     frontend,
#     test_flags,
# ):
#     input_dtype, x = dtype_and_x
#     helpers.test_frontend_function(
#         input_dtypes=input_dtype,
#         frontend=frontend,
#         test_flags=test_flags,
#         fn_tree=fn_tree,
#         on_device=on_device,
#         x=x[0],
#     )

# @handle_frontend_test(
#     fn_tree="mindspore.ops.function.nn_func.interpolate",
#     dtype_and_x=helpers.dtype_and_values(
#         available_dtypes=helpers.get_dtypes("valid"),
#         num_arrays=1,
#         shared_dtype=True,
#         min_value=2,
#         max_value=5,
#         min_dim_size=4,
#         shape=(
#             st.integers(min_value=2, max_value=10),
#             4,
#             st.integers(min_value=12, max_value=64),
#             st.integers(min_value=12, max_value=64),
#         ),
#     ),
#     mode=st.sampled_from(
#         [
#             "nearest",
#             "linear",
#             "bilinear",
#             "bicubic",
#             "trilinear",
#             "area",
#             "nearest-exact",
#         ]
#     ),
#     align_corners=st.booleans(),
#     recompute_scale_factor=st.booleans(),
#     size=st.one_of(
#         st.integers(min_value=1, max_value=10),
#         st.tuples(st.integers(min_value=1, max_value=10)),
#         st.lists(st.integers(min_value=1, max_value=10), min_size=3, max_size=3),
#     )
#     | None,
#     scale_factor=st.one_of(
#         st.floats(min_value=0.1, max_value=2.0),
#         st.tuples(st.floats(min_value=0.1, max_value=2.0)),
#         st.lists(st.floats(min_value=0.1, max_value=2.0), min_size=3, max_size=3),
#     )
#     | None,
# )
# def test_mindspore_interpolate(
#     *,
#     dtype_and_x,
#     size,
#     scale_factor,
#     mode,
#     align_corners,
#     recompute_scale_factor,
#     on_device,
#     fn_tree,
#     frontend,
#     test_flags,
# ):
#     dtype, x = dtype_and_x

#     if size is None and scale_factor is None:
#         raise ValueError(
#             "Both 'size' and 'scale_factor' cannot be None."
#             "Please provide a valid value for either 'size' or 'scale_factor'."
#         )

#     if not recompute_scale_factor:
#         if size is not None:
#             scale_factor = None
#         elif scale_factor is not None:
#             size = None

#     helpers.test_frontend_function(
#         input_dtypes=dtype,
#         frontend=frontend,
#         test_flags=test_flags,
#         fn_tree=fn_tree,
#         on_device=on_device,
#         input=x[0],
#         size=size,
#         scale_factor=scale_factor,
#         mode=mode,
#         align_corners=align_corners,
#         recompute_scale_factor=recompute_scale_factor,
#     )
