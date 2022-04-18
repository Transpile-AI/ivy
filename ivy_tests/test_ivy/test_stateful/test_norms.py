"""
Collection of tests for normalization layers
"""

# global

# local


# layer norm
# @pytest.mark.parametrize(
#     "x_n_ns_n_target", [
#         ([[1., 2., 3.], [4., 5., 6.]],
#          [3],
#          [[-1.2247356, 0., 1.2247356],
#           [-1.2247356, 0., 1.2247356]]),
#     ])
# @pytest.mark.parametrize(
#     "with_v", [True, False])
# @pytest.mark.parametrize(
#     "dtype", ['float32'])
# @pytest.mark.parametrize(
#     "tensor_fn", [ivy.array, helpers.var_fn])
# def test_layer_norm_layer(x_n_ns_n_target, with_v, dtype, tensor_fn, dev, compile_graph, call):
#     # smoke test
#     x, normalized_shape, target = x_n_ns_n_target
#     x = tensor_fn(x, dtype, dev)
#     target = tensor_fn(target, dtype, dev)
#     if with_v:
#         v = Container({'scale': ivy.variable(ivy.ones(normalized_shape)),
#                        'offset': ivy.variable(ivy.zeros(normalized_shape))})
#     else:
#         v = None
#     norm_layer = ivy.LayerNorm(normalized_shape, dev=dev, v=v)
#     ret = norm_layer(x)
#     # type test
#     assert ivy.is_array(ret)
#     # cardinality test
#     assert ret.shape == x.shape
#     # value test
#     if not with_v:
#         return
#     assert np.allclose(call(norm_layer, x), ivy.to_numpy(target))
#     # compilation test
#     if call in [helpers.torch_call]:
#         # this is not a backend implemented function
#         return
