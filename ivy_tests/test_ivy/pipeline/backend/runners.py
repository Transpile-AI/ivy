import numpy as np
import inspect
import copy
from ivy_tests.test_ivy.pipeline.base.runners import (
    TestCaseRunner,
    TestCaseSubRunner,
    TestCaseSubRunnerResult,
    TestArgumentsSearchResult,
)


class FunctionTestCaseSubRunner(TestCaseSubRunner):
    def __init__(
        self, fn_name, backend_handler, backend, device, input_dtypes, test_flags
    ):
        self.fn_name = fn_name
        self._backend_handler = backend_handler
        self.backend = backend
        self.on_device = device
        self.__ivy = self._backend_handler.set_backend(backend)
        self.test_flags = test_flags
        self.input_dtypes = input_dtypes

    @property
    def backend_handler(self):
        return self._backend_handler

    @property
    def _ivy(self):
        return self.__ivy

    def _search_args(self, test_arguments):
        # split the arguments into their positional and keyword components
        args_np, kwargs_np = self._split_args_to_args_and_kwargs(
            num_positional_args=self.test_flags.num_positional_args,
            test_arguments=test_arguments,
        )

        # Extract all arrays from the arguments and keyword arguments
        arg_np_arrays, arrays_args_indices, n_args_arrays = self._get_nested_np_arrays(
            args_np
        )
        kwarg_np_arrays, arrays_kwargs_indices, n_kwargs_arrays = (
            self._get_nested_np_arrays(kwargs_np)
        )

        total_num_arrays = n_args_arrays + n_kwargs_arrays
        args_result = TestArgumentsSearchResult(
            args_np, arg_np_arrays, arrays_args_indices
        )
        kwargs_result = TestArgumentsSearchResult(
            kwargs_np, kwarg_np_arrays, arrays_kwargs_indices
        )
        return args_result, kwargs_result, total_num_arrays

    def _preprocess_flags(self, total_num_arrays):
        # Make all array-specific test flags and dtypes equal in length
        if len(self.input_dtypes) < total_num_arrays:
            self.input_dtypes = [self.input_dtypes[0] for _ in range(total_num_arrays)]
        if len(self.test_flags.as_variable) < total_num_arrays:
            self.test_flags.as_variable = [
                self.test_flags.as_variable[0] for _ in range(total_num_arrays)
            ]
        if len(self.test_flags.native_arrays) < total_num_arrays:
            self.test_flags.native_arrays = [
                self.test_flags.native_arrays[0] for _ in range(total_num_arrays)
            ]
        if len(self.test_flags.container) < total_num_arrays:
            self.test_flags.container = [
                self.test_flags.container[0] for _ in range(total_num_arrays)
            ]
        # Update variable flags to be compatible with float dtype and with_out args
        self.test_flags.as_variable = [
            v if self._ivy.is_float_dtype(d) and not self.test_flags.with_out else False
            for v, d in zip(self.test_flags.as_variable, self.input_dtypes)
        ]

        # TODO this is not ideal, modifying Hypothesis generated value
        # May result in weird bugs. Should instead update strategies to
        # Not generate this in first place.
        # update instance_method flag to only be considered if the
        self.test_flags.instance_method = self.test_flags.instance_method and (
            not self.test_flags.native_arrays[0] or self.test_flags.container[0]
        )
        return self.test_flags

    def _preprocess_args(
        self,
        args_result: TestArgumentsSearchResult,
        kwargs_result: TestArgumentsSearchResult,
    ):
        """
        Create arguments and keyword-arguments for the function to test.

        Returns
        -------
        Backend specific arguments, keyword-arguments
        """
        ret = []
        for result, start_index_of_arguments in zip(
            [args_result, kwargs_result], [0, len(args_result.values)]
        ):
            temp = self._ivy.copy_nest(result.original, to_mutable=False)
            self._ivy.set_nest_at_indices(
                temp,
                result.indices,
                self.test_flags.apply_flags(
                    result.values,
                    self.input_dtypes,
                    start_index_of_arguments,
                    backend=self.backend,
                    on_device=self.on_device,
                ),
            )
            ret.append(temp)
        return ret[0], ret[1]

    def _call_function(self, args, kwargs):
        instance = None
        if self.test_flags.instance_method:
            array_or_container_mask = [
                (not native_flag) or container_flag
                for native_flag, container_flag in zip(
                    self.test_flags.native_arrays, self.test_flags.container
                )
            ]

            # Boolean mask for args and kwargs True if an entry's
            # test Array flag is True or test Container flag is true
            args_instance_mask = array_or_container_mask[
                : self.test_flags.num_positional_args
            ]
            kwargs_instance_mask = array_or_container_mask[
                self.test_flags.num_positional_args :
            ]

            if any(args_instance_mask):
                instance, args = _find_instance_in_args(
                    self.backend, args, arrays_args_indices, args_instance_mask
                )
            else:
                instance, kwargs = _find_instance_in_args(
                    self.backend, kwargs, arrays_kwargs_indices, kwargs_instance_mask
                )

            if self.test_flags.test_compile:
                target_fn = lambda instance, *args, **kwargs: instance.__getattribute__(
                    self.fn_name
                )(*args, **kwargs)
                args = [instance, *args]
            else:
                target_fn = instance.__getattribute__(self.fn_name)
        else:
            target_fn = self._ivy.__dict__[self.fn_name]

        # Make copy of arguments for functions that might use inplace update by default
        copy_kwargs = copy.deepcopy(kwargs)
        copy_args = copy.deepcopy(args)

        ret_from_target, ret_np_flat_from_target = get_ret_and_flattened_np_array(
            self.backend,
            target_fn,
            *copy_args,
            test_compile=self.test_flags.test_compile,
            **copy_kwargs,
        )

        # TODO move from here to assertions
        assert self._ivy.nested_map(
            ret_from_target,
            lambda x: self._ivy.is_ivy_array(x) if self._ivy.is_array(x) else True,
        ), "Ivy function returned non-ivy arrays: {}".format(ret_from_target)

        # TODO should be moved outside of get_results
        # Assert indices of return if the indices of the out array provided
        if self.test_flags.with_out and not self.test_flags.test_compile:
            test_ret = (
                ret_from_target[getattr(self._ivy.__dict__[self.fn_name], "out_index")]
                if hasattr(self._ivy.__dict__[self.fn_name], "out_index")
                else ret_from_target
            )
            out = self._ivy.nested_map(
                test_ret, self._ivy.zeros_like, to_mutable=True, include_derived=True
            )
            if self.test_flags.instance_method:
                ret_from_target, ret_np_flat_from_target = (
                    get_ret_and_flattened_np_array(
                        self.backend,
                        instance.__getattribute__(self.fn_name),
                        *args,
                        **kwargs,
                        out=out,
                    )
                )
            else:
                ret_from_target, ret_np_flat_from_target = (
                    get_ret_and_flattened_np_array(
                        self.backend,
                        self._ivy.__dict__[self.fn_name],
                        *args,
                        **kwargs,
                        out=out,
                    )
                )
            test_ret = (
                ret_from_target[getattr(self.ivy.__dict__[self.fn_name], "out_index")]
                if hasattr(self._ivy.__dict__[self.fn_name], "out_index")
                else ret_from_target
            )
            assert not self._ivy.nested_any(
                self._ivy.nested_multi_map(lambda x, _: x[0] is x[1], [test_ret, out]),
                lambda x: not x,
            ), "the array in out argument does not contain same value as the returned"
            if not max(self.test_flags.container) and self._ivy.native_inplace_support:
                # these backends do not always support native inplace updates
                assert not self._ivy.nested_any(
                    self._ivy.nested_multi_map(
                        lambda x, _: x[0].data is x[1].data, [test_ret, out]
                    ),
                    lambda x: not x,
                ), (
                    "the array in out argument does not contain same value as the"
                    " returned"
                )
        ret_device = (
            self._ivy.dev(ret_from_target)
            if self._ivy.is_array(ret_from_target)
            else None
        )
        return (
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
        )

    def get_results(self, test_arguments):
        args_result, kwargs_result, total_num_arrays = self._search_args(test_arguments)
        self._preprocess_flags(total_num_arrays)
        args, kwargs = self._preprocess_args(args_result, kwargs_result)

        # If function doesn't have an out argument but an out argument is given
        # or a test with out flag is True
        if (
            "out" in kwargs or self.test_flags.with_out
        ) and "out" not in inspect.signature(
            getattr(self._ivy, self.fn_name)
        ).parameters:
            raise Exception(f"Function {self.fn_name} does not have an out parameter")

        return self._call_function(args, kwargs)


class BackendTestCaseRunner(TestCaseRunner):
    def __init__(
        self,
        backend_handler,
        fn_name,
        backend_to_test,
        ground_truth_backend,
        on_device,
        rtol,
        atol,
    ):
        self.fn_name = fn_name
        self.backend_handler = backend_handler
        self.backend_to_test = backend_to_test
        self.grond_truth_backend = ground_truth_backend
        self.on_device = on_device
        self.rtol = rtol
        self.atol = atol

    def _assert_type(self, target_type, ground_truth_type):
        assert target_type == ground_truth_type

    def _assert_dtype(self, target_dtype, ground_truth_dtype):
        assert target_dtype == ground_truth_dtype

    def _assert_device(self, target_device, ground_truth_device):
        assert target_device == ground_truth_device, (
            f"ground truth backend ({self.ground_truth_backend}) returned array on"
            f" device {ground_truth_device} but target backend ({self.backend_to_test})"
            f" returned array on device {target_device}"
        )

    def _assert_equal_elements(self, target_elements, ground_truth_elements):
        assert np.allclose(
            np.nan_to_num(target_elements),
            np.nan_to_num(ground_truth_elements),
            rtol=self.rtol,
            atol=self.atol,
        ), (
            f" the results from backend {self.backend_to_test} "
            f"and ground truth framework {self.ground_truth_backend} "
            f"do not match\n {target_elements}!={ground_truth_elements} \n\n"
        )

    def _run_target(self, input_dtypes, test_arguments, test_flags):
        sub_runner_target = FunctionTestCaseSubRunner(
            self.fn_name,
            self.backend_handler,
            self.backend_to_test,
            self.on_device,
            input_dtypes,
            test_flags,
        )
        sub_runner_target.get_results(test_arguments)
        sub_runner_target.exit()

    def _run_ground_truth(self, input_dtypes, test_arguments, test_flags):
        pass

    def run(self, input_dtypes, test_arguments, test_flags):
        target_results: TestCaseSubRunnerResult = self._run_target(
            input_dtypes, test_arguments, test_flags
        )
        ground_truth_results: TestCaseSubRunnerResult = self._run_ground_truth(
            input_dtypes, test_arguments, test_flags
        )

        self._assert_dtype(target_results.dtype, ground_truth_results.dtype)
        self._assert_type(target_results.type, ground_truth_results.type)
        self._assert_device(target_results.device, ground_truth_results.device)
        self._assert_equal_elements(
            target_results.flatten_elements_np, ground_truth_results.flatten_elements_np
        )
