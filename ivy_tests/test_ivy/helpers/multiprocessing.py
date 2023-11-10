# global
import sys
import importlib

from ivy_tests.test_ivy.helpers.hypothesis_helpers.array_helpers import (
    array_helpers_dtype_info_helper,
)
from ivy_tests.test_ivy.helpers.hypothesis_helpers.dtype_helpers import (
    _get_type_dict_helper,
    cast_filter_helper,
)

# local
from .testing_helpers import (
    _get_supported_devices_dtypes_helper,
    _get_method_supported_devices_dtypes_helper,
    num_positional_args_helper,
)
from .function_testing import (
    test_function_backend_computation,
    test_function_ground_truth_computation,
    test_gradient_backend_computation,
    test_gradient_ground_truth_computation,
    _transpile_if_required_backend,
)
from ..pipeline.frontend.multiprocessing import (
    FrontendFunctionTestCaseRunnerMP,
    FrontendMethodTestCaseRunnerMP,
)
from ..pipeline.backend.multiprocessing import (
    BackendMethodTestCaseRunnerMP,
)

framework_path = "/opt/fw/"


def backend_proc(input_queue, output_queue):
    # first argument is going to be the framework and its path
    framework = input_queue.get()
    path = framework_path + framework
    sys.path.insert(1, path)
    framework = framework.split("/")[0]
    framework = importlib.import_module(framework)
    # if jax, do more stuff
    if framework.__name__ == "jax":
        framework.config.update("jax_enable_x64", True)
    while True:
        # subsequent arguments will be passed
        data = input_queue.get()
        if data[0] == "supported dtypes":
            # stage 1, calculating and returning supported dtypes
            # of each backend
            pass

            _, fn_module, fn_name, b = data
            output_queue.put(
                _get_supported_devices_dtypes_helper(b, fn_module, fn_name)
            )

        elif data[0] == "method supported dtypes":
            # again stage 1, calculating and returning supported dtypes
            _, method_name, class_module, class_name, backend_str = data
            # since class module is name, we will import it to make it a module
            class_module = importlib.import_module(class_module)
            organized_dtypes = _get_method_supported_devices_dtypes_helper(
                method_name, class_module, class_name, backend_str
            )
            output_queue.put(organized_dtypes)

        elif data[0] == "dtype_info_helper":
            _, backend, kind_dtype, dtype = data
            dtype_info = array_helpers_dtype_info_helper(backend, kind_dtype, dtype)
            output_queue.put(dtype_info)

        elif data[0] == "_get_type_dict_helper":
            _, framework, kind, is_frontend_test = data
            dtype_ret = _get_type_dict_helper(framework, kind, is_frontend_test)
            output_queue.put(dtype_ret)

        elif data[0] == "num_positional_args_helper":
            _, fn_name, framework = data
            dtype_ret = num_positional_args_helper(fn_name, framework)
            output_queue.put(dtype_ret)

        elif data[0] == "cast_filter_helper":
            _, d, dtype, x, current_backend = data
            dtype_ret = cast_filter_helper(d, dtype, x, current_backend)
            output_queue.put(dtype_ret)

        elif data[0] == "function_backend_computation":
            # it's the backend return computation
            _, fw, test_flags, all_as_kwargs_np, input_dtypes, on_device, fn_name = data
            (
                ret_from_target,
                ret_np_flat_from_target,
                ret_device,
                args_np,
                arg_np_arrays,
                arrays_args_indices,
                kwargs_np,
                arrays_kwargs_indices,
                kwarg_np_arrays,
                test_flags,
                input_dtypes,
            ) = test_function_backend_computation(
                fw, test_flags, all_as_kwargs_np, input_dtypes, on_device, fn_name
            )
            # ret_from_target to be none, because main process has
            # framework imports blocked
            output_queue.put(
                (
                    (None),
                    ret_np_flat_from_target,
                    ret_device,
                    args_np,
                    arg_np_arrays,
                    arrays_args_indices,
                    kwargs_np,
                    arrays_kwargs_indices,
                    kwarg_np_arrays,
                    test_flags,
                    input_dtypes,
                )
            )
        elif data[0] == "function_ground_truth_computation":
            # it's the ground_truth return computation
            (
                _,
                ground_truth_backend,
                on_device,
                args_np,
                arg_np_arrays,
                arrays_args_indices,
                kwargs_np,
                arrays_kwargs_indices,
                kwarg_np_arrays,
                input_dtypes,
                test_flags,
                fn_name,
            ) = data
            (
                ret_from_gt,
                ret_np_from_gt_flat,
                ret_from_gt_device,
                test_flags,
                fw_list,
            ) = test_function_ground_truth_computation(
                ground_truth_backend,
                on_device,
                args_np,
                arg_np_arrays,
                arrays_args_indices,
                kwargs_np,
                arrays_kwargs_indices,
                kwarg_np_arrays,
                input_dtypes,
                test_flags,
                fn_name,
            )
            # ret_from gt is none because main process has frameworks is None
            output_queue.put(
                (
                    (None),
                    ret_np_from_gt_flat,
                    ret_from_gt_device,
                    test_flags,
                    fw_list,
                )
            )
        elif data[0] == "gradient_backend_computation":
            # gradient testing , part where it uses the backend
            (
                _,
                backend_to_test,
                args_np,
                arg_np_vals,
                args_idxs,
                kwargs_np,
                kwarg_np_vals,
                kwargs_idxs,
                input_dtypes,
                test_flags,
                on_device,
                fn,
                test_trace,
                xs_grad_idxs,
                ret_grad_idxs,
            ) = data
            grads_np_flat = test_gradient_backend_computation(
                backend_to_test,
                args_np,
                arg_np_vals,
                args_idxs,
                kwargs_np,
                kwarg_np_vals,
                kwargs_idxs,
                input_dtypes,
                test_flags,
                on_device,
                fn,
                test_trace,
                xs_grad_idxs,
                ret_grad_idxs,
            )
            output_queue.put(grads_np_flat)

        elif data[0] == "gradient_ground_truth_computation":
            # gradient testing, part where it uses ground truth
            (
                _,
                ground_truth_backend,
                on_device,
                fn,
                input_dtypes,
                all_as_kwargs_np,
                args_np,
                arg_np_vals,
                args_idxs,
                kwargs_np,
                kwarg_np_vals,
                test_flags,
                kwargs_idxs,
                test_trace,
                xs_grad_idxs,
                ret_grad_idxs,
            ) = data
            grads_np_from_gt_flat = test_gradient_ground_truth_computation(
                ground_truth_backend,
                on_device,
                fn,
                input_dtypes,
                all_as_kwargs_np,
                args_np,
                arg_np_vals,
                args_idxs,
                kwargs_np,
                kwarg_np_vals,
                test_flags,
                kwargs_idxs,
                test_trace,
                xs_grad_idxs,
                ret_grad_idxs,
            )
            output_queue.put(grads_np_from_gt_flat)

        elif data[0] == "_method_backend":
            (
                _,
                class_name,
                method_name,
                backend_handler,
                ground_truth_backend,
                on_device,
                traced_fn,
                v_np,
                init_input_dtypes,
                method_input_dtypes,
                init_flags,
                method_flags,
                init_all_as_kwargs_np,
                method_all_as_kwargs_np,
            ) = data
            ret = BackendMethodTestCaseRunnerMP._run_target_helper(
                class_name,
                method_name,
                backend_handler,
                ground_truth_backend,
                on_device,
                traced_fn,
                v_np,
                init_input_dtypes,
                method_input_dtypes,
                init_flags,
                method_flags,
                init_all_as_kwargs_np,
                method_all_as_kwargs_np,
            )
            output_queue.put(ret)

        elif data[0] == "_method_ground_truth":
            (
                _,
                class_name,
                method_name,
                backend_handler,
                ground_truth_backend,
                on_device,
                traced_fn,
                v_np,
                init_input_dtypes,
                method_input_dtypes,
                init_flags,
                method_flags,
                init_all_as_kwargs_np,
                method_all_as_kwargs_np,
            ) = data
            ret = BackendMethodTestCaseRunnerMP._run_ground_truth_helper(
                class_name,
                method_name,
                backend_handler,
                ground_truth_backend,
                on_device,
                traced_fn,
                v_np,
                init_input_dtypes,
                method_input_dtypes,
                init_flags,
                method_flags,
                init_all_as_kwargs_np,
                method_all_as_kwargs_np,
            )
            output_queue.put(ret)

        elif data[0] == "_run_target_frontend_function":
            (
                _,
                fn_tree,
                test_flags,
                frontend,
                backend_handler,
                on_device,
                input_dtypes,
                test_arguments,
                backend_to_test,
                traced_fn,
            ) = data
            ret = FrontendFunctionTestCaseRunnerMP._run_target_helper(
                fn_tree,
                test_flags,
                frontend,
                backend_handler,
                on_device,
                input_dtypes,
                test_arguments,
                backend_to_test,
                traced_fn,
            )
            output_queue.put(ret)
        elif data[0] == "_run_target_frontend_method":
            (
                _,
                frontend_method_data,
                frontend,
                backend_handler,
                backend_to_test,
                on_device,
                init_flags,
                method_flags,
                init_all_as_kwargs_np,
                method_all_as_kwargs_np,
                init_with_v,
                method_with_v,
            ) = data
            ret = FrontendMethodTestCaseRunnerMP._run_target_helper(
                frontend_method_data,
                frontend,
                backend_handler,
                backend_to_test,
                on_device,
                init_flags,
                method_flags,
                init_all_as_kwargs_np,
                method_all_as_kwargs_np,
                init_with_v,
                method_with_v,
            )
            output_queue.put(ret)

        elif data[0] == "transpile_if_required_backend":
            _, backend, fn_name, args_np, kwargs_np = data
            _transpile_if_required_backend(backend, fn_name, args_np, kwargs_np)

        if not data:
            break
        # process the data


# TODO incomplete
def frontend_proc(input_queue, output_queue):
    # first argument is going to be the framework and its path
    framework = input_queue.get()
    sys.path.insert(1, f"{framework_path}{framework}")
    importlib.import_module(framework.split("/")[0])
    while True:
        # subsequent arguments will be passed
        data = input_queue.get()

        if data[0] == "_run_gt_frontend_function":
            (
                _,
                gt_fn_tree,
                fn_tree,
                test_flags,
                frontend,
                backend_handler,
                on_device,
                input_dtypes,
                test_arguments,
            ) = data
            ret = FrontendFunctionTestCaseRunnerMP._run_ground_truth_helper(
                gt_fn_tree,
                fn_tree,
                test_flags,
                frontend,
                backend_handler,
                on_device,
                input_dtypes,
                test_arguments,
            )
            output_queue.put(ret)

        elif data[0] == "_get_type_dict_helper":
            _, framework, kind, is_frontend_test = data
            dtype_ret = _get_type_dict_helper(framework, kind, is_frontend_test)
            output_queue.put((dtype_ret))
        elif data[0] == "_run_gt_frontend_method":
            (
                _,
                frontend_method_data,
                frontend,
                backend_handler,
                backend_to_test,
                on_device,
                init_flags,
                method_flags,
                init_all_as_kwargs_np,
                method_all_as_kwargs_np,
            ) = data
            ret = FrontendMethodTestCaseRunnerMP._run_ground_truth_method_helper(
                frontend_method_data,
                frontend,
                backend_handler,
                backend_to_test,
                on_device,
                init_flags,
                method_flags,
                init_all_as_kwargs_np,
                method_all_as_kwargs_np,
            )
            output_queue.put(ret)

        if not data:
            break
        # process the data
