import inspect
from ivy_tests.test_ivy.helpers.structs import ParametersInfo

from abc import abstractproperty
from ivy_tests.test_ivy.helpers.decorators.base.decorator_base import HandlerBase
from ivy_tests.test_ivy.helpers.pipeline_helper import update_backend
from ivy_tests.test_ivy.helpers.available_frameworks import available_frameworks
from ivy_tests.test_ivy.helpers.decorators.strategies import (
    num_positional_args_from_dict,
)


class MethodHandlerBase(HandlerBase):
    @abstractproperty
    def init_tree():
        pass

    @abstractproperty
    def method_tree():
        pass

    def _build_parameter_info(self, fn):
        total = num_positional_only = num_keyword_only = 0
        # TODO refactor out
        for param in inspect.signature(fn).parameters.values():
            if param.name == "self":
                continue
            total += 1
            if param.kind == param.POSITIONAL_ONLY:
                num_positional_only += 1
            elif param.kind == param.KEYWORD_ONLY:
                num_keyword_only += 1
            elif param.kind == param.VAR_KEYWORD:
                num_keyword_only += 1
        return ParametersInfo(
            total=total,
            positional_only=num_positional_only,
            keyword_only=num_keyword_only,
        )

    def _build_parameters_info_dict_from_function(self, function_tree):
        ret = {}

        for framework in available_frameworks:
            method = self._import_function(function_tree, framework)
            parameter_info = self._build_parameter_info(method)
            ret[framework] = parameter_info

        return ret

    def _build_parameters_info_dict_from_method(self, method_tree):
        ret = {}

        for framework in available_frameworks:
            method = self._import_method(method_tree, framework)
            parameter_info = self._build_parameter_info(method)
            ret[framework] = parameter_info

        return ret

    def _build_num_positional_arguments_strategy_from_function(self, method_tree: str):
        dict_for_num_pos_strategy = self._build_parameters_info_dict_from_function(
            method_tree
        )
        return num_positional_args_from_dict(dict_for_num_pos_strategy)

    def _build_num_positional_arguments_strategy_from_method(self, method_tree: str):
        dict_for_num_pos_strategy = self._build_parameters_info_dict_from_method(
            method_tree
        )
        return num_positional_args_from_dict(dict_for_num_pos_strategy)

    def _partition_method_tree(self, method_tree: str):
        class_module_and_name, _, method_name = method_tree.rpartition(".")
        class_module, _, class_name = class_module_and_name.rpartition(".")
        return class_module, class_name, method_name

    def _import_method(self, method_tree: str, framework: str):
        class_module, class_name, method_name = self._partition_method_tree(method_tree)
        with update_backend(framework) as ivy_backend:
            module = ivy_backend.utils.dynamic_import.import_module(class_module)
            cls = getattr(module, class_name)
            method = getattr(cls, method_name)
        return method

    def _import_function(self, function_tree: str, framework: str):
        function_module_tree, _, function_name = function_tree.rpartition(".")
        with update_backend(framework) as ivy_backend:
            module = ivy_backend.utils.dynamic_import.import_module(
                function_module_tree
            )
            fn = getattr(module, function_name)
        return fn

    def _build_supported_devices_dtypes(self):
        supported_device_dtypes = {}
        for backend_str in available_frameworks:
            with update_backend(backend_str) as backend:
                method = self._import_method(self.method_tree, backend_str)
                devices_and_dtypes = backend.function_supported_devices_and_dtypes(
                    method
                )
                organized_dtypes = {}
                for device in devices_and_dtypes.keys():
                    organized_dtypes[device] = self._partition_dtypes_into_kinds(
                        backend_str, devices_and_dtypes[device]
                    )
                supported_device_dtypes[backend_str] = organized_dtypes
        return supported_device_dtypes
