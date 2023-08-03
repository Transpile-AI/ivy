from hypothesis import strategies as st
from typing import Callable, Any
from ivy_tests.test_ivy.helpers.decorators.base.function_decorator_base import (
    FunctionHandler,
)
from ivy_tests.test_ivy.helpers.test_parameter_flags import (
    build_backend_function_flags,
    BuiltInstanceStrategy,
    BuiltAsVariableStrategy,
    BuiltNativeArrayStrategy,
    BuiltGradientStrategy,
    BuiltContainerStrategy,
    BuiltWithOutStrategy,
    BuiltCompileStrategy,
)


class BackendFunctionHandler(FunctionHandler):
    def __init__(
        self,
        fn_tree: str,
        ground_truth_backend="tensorflow",
        num_positional_args=None,
        instance_method=BuiltInstanceStrategy,
        with_out=BuiltWithOutStrategy,
        test_gradients=BuiltGradientStrategy,
        test_compile=BuiltCompileStrategy,
        as_variable=BuiltAsVariableStrategy,
        native_arrays=BuiltNativeArrayStrategy,
        container_flags=BuiltContainerStrategy,
        **_given_kwargs
    ):
        # Changing the order of init vars will likely break things. Change with caution!
        self.fn_tree = self._append_ivy_to_fn_tree(fn_tree)
        self.ground_truth_backend = ground_truth_backend
        self._given_kwargs = _given_kwargs
        self.callable_fn = self.import_function(self.fn_tree)
        self._build_test_data()

        if num_positional_args is None:
            num_positional_args = self._build_num_positional_arguments_strategy()

        self.test_flags = build_backend_function_flags(
            ground_truth_backend=st.just(ground_truth_backend),
            num_positional_args=num_positional_args,
            instance_method=instance_method,
            with_out=with_out,
            test_gradients=test_gradients,
            test_compile=test_compile,
            as_variable=as_variable,
            native_arrays=native_arrays,
            container_flags=container_flags,
        )

    @property
    def possible_args(self):
        return {
            "ground_truth_backend": st.just(self.ground_truth_backend),
            "fn_name": st.just(self.test_data.fn_name),
            "test_data": self.test_data,
            "test_flags": self.test_flags,
        }

    def _add_test_attributes_to_test_function(self, fn: Callable[..., Any]):
        fn._is_ivy_backend_test = True
        fn.ground_truth_backend = self.ground_truth_backend
        fn.test_data = self.test_data
        return fn
