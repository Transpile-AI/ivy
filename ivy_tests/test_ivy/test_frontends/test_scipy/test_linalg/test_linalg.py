# TODO: uncomment after frontend is not required
# # global
# from hypothesis import strategies as st

# # local
# import ivy_tests.test_ivy.helpers as helpers
# from ivy_tests.test_ivy.helpers import handle_frontend_test


# # tril
# @handle_frontend_test(
#     fn_tree="scipy.linalg.tril",
#     dtype_and_x=helpers.dtype_and_values(
#         available_dtypes=helpers.get_dtypes("numeric"),
#         num_arrays=1,
#         min_num_dims=2,
#         max_num_dims=5,
#         min_dim_size=1,
#         max_dim_size=5,
#     ),
#     k=helpers.ints(min_value=-10, max_value=10),
#     test_with_out=st.just(False),
# )
# def test_scipy_tril(
#     dtype_and_x,
#     k,
#     frontend,
#     test_flags,
#     fn_tree,
#     on_device,
# ):
#     dtype, x = dtype_and_x
#     helpers.test_frontend_function(
#         input_dtypes=dtype,
#         frontend=frontend,
#         test_flags=test_flags,
#         fn_tree=fn_tree,
#         on_device=on_device,
#         m=x[0],
#         k=k,
#     )


# # triu
# @handle_frontend_test(
#     fn_tree="jax.scipy.triu",
#     dtype_and_x=helpers.dtype_and_values(
#         available_dtypes=helpers.get_dtypes("numeric"),
#         num_arrays=1,
#         min_num_dims=2,
#         max_num_dims=5,
#         min_dim_size=1,
#         max_dim_size=5,
#     ),
#     k=helpers.ints(min_value=-10, max_value=10),
#     test_with_out=st.just(False),
# )
# def test_scipy_triu(
#     dtype_and_x,
#     k,
#     test_flags,
#     frontend,
#     fn_tree,
#     on_device,
# ):
#     dtype, x = dtype_and_x
#     helpers.test_frontend_function(
#         input_dtypes=dtype,
#         frontend=frontend,
#         test_flags=test_flags,
#         fn_tree=fn_tree,
#         on_device=on_device,
#         m=x[0],
#         k=k,
#     )
