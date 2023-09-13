import os
from types import ModuleType, FunctionType
import logging
import importlib
from typing import Callable

import ivy
from ivy.func_wrapper import _wrap_function
from ivy.utils.exceptions import IvyException


_backends_subpackage_path = "ivy.functional.backends"
_sub_backend_dict: dict[str, str] = dict()
_backend_to_sub_backends_dict: dict[str, list] = dict()
_available_sub_backends_implementations_dict: dict[str, dict[str, list]] = dict()


def _detect_sub_backends_dynamically():
    for backend in os.listdir(
        os.path.join(
            ivy.__path__[0].rpartition(os.path.sep)[0],  # type: ignore
            _backends_subpackage_path.replace(".", os.path.sep),
        )
    ):
        if not backend[0].isalpha():
            continue

        sub_backends_dir = os.path.join(
            ivy.__path__[0].rpartition(os.path.sep)[0],
            _backends_subpackage_path.replace(".", os.path.sep),
            backend,
            "sub_backends",
        )
        for sub_backend in os.listdir(sub_backends_dir):
            if not sub_backend[0].isalpha():
                continue
            _sub_backend_dict[sub_backend] = (
                f"{_backends_subpackage_path}.{backend}.sub_backends.{sub_backend}"
            )
            try:
                _backend_to_sub_backends_dict[backend].append(sub_backend)
            except KeyError:
                _backend_to_sub_backends_dict[backend] = [sub_backend]


_detect_sub_backends_dynamically()


def _get_all_sub_backends():
    result = []
    for v in _backend_to_sub_backends_dict.values():
        result.extend(v)
    return result


_all_sub_backends = _get_all_sub_backends()


original_backend_dict = None


def set_sub_backend(sub_backend_str: str):
    if ivy.backend == "":
        logging.warning("You must set a backend first")
        return

    if ivy.current_backend_str() not in _backend_to_sub_backends_dict.keys():
        logging.warning(
            f"backend {ivy.current_backend_str()} does not have any"
            " supported sub_backends"
        )
        return

    if sub_backend_str not in _all_sub_backends:
        raise IvyException(
            "sub_backend must be one from"
            f" {_backend_to_sub_backends_dict[ivy.current_backend_str()]}"
        )

    if sub_backend_str not in _backend_to_sub_backends_dict[ivy.current_backend_str()]:
        logging.warning(
            f"{ivy.current_backend_str()} does not support"
            f" {sub_backend_str} as a sub_backend"
        )
        return

    if sub_backend_str in ivy.current_sub_backends():
        return

    global original_backend_dict
    if original_backend_dict is None:
        original_backend_dict = ivy.__dict__.copy()
    sub_backend = ivy.utils.dynamic_import.import_module(
        _sub_backend_dict[sub_backend_str]
    )
    _set_sub_backend_as_ivy(ivy.__dict__.copy(), ivy, sub_backend)
    ivy.current_backend().sub_backends._current_sub_backends.append(sub_backend_str)


# this is very similar to _set_backend_as_ivy in handler.py, with a minor change
def _set_sub_backend_as_ivy(
    original: dict, target: ModuleType, sub_backend: ModuleType
):
    backend_str = ivy.current_backend_str()
    for k, v in original.items():
        if k not in sub_backend.__dict__ and not k.startswith("__"):
            target.__dict__[k] = v
        if (
            k in sub_backend.__dict__
            and not k.startswith("__")
            and isinstance(v, FunctionType)
        ):
            target.__dict__[k] = _wrap_function(
                key=k, to_wrap=sub_backend.__dict__[k], original=v, compositional=False
            )
        elif (
            k in sub_backend.__dict__
            and not k.startswith("__")
            and isinstance(v, ModuleType)
        ):
            # we are creating a module to avoid inplace updating
            # the sub_backends dict's modules, this happens when
            # unsetting the sub_backend as we partially update the modules
            mod = ModuleType(k)
            mod.__name__ = v.__name__
            mod.__file__ = v.__file__
            target.__dict__[k] = mod
        if (
            isinstance(v, ModuleType)
            and "ivy.functional." in v.__name__
            and os.path.join("{}", "__init__.py").format(backend_str) not in v.__file__
            and k in sub_backend.__dict__
        ):
            _set_sub_backend_as_ivy(
                v.__dict__,
                target.__dict__[k],
                sub_backend.__dict__[k],
            )


def unset_sub_backend(sub_backend_str: str):
    if sub_backend_str not in ivy.current_sub_backends():
        return
    global original_backend_dict

    # The sub-backend is cached so this is fast
    sub_backend = ivy.utils.dynamic_import.import_module(
        _sub_backend_dict[sub_backend_str]
    )
    _unset_sub_backend_from_ivy(
        original_backend_dict, ivy, sub_backend, sub_backend.name
    )
    ivy.current_backend().sub_backends._current_sub_backends.remove(sub_backend_str)


def _unset_sub_backend_from_ivy(
    original: dict, target: ModuleType, sub_backend: ModuleType, sub_backend_str: str
):
    backend_str = ivy.current_backend_str()
    for k, v in sub_backend.__dict__.items():
        if k in target.__dict__:
            if (
                isinstance(v, FunctionType)
                and sub_backend_str in f"sub_backends.{sub_backend_str}" in v.__module__
            ):
                target.__dict__[k] = original[k]
            if (
                isinstance(v, ModuleType)
                and "ivy.functional." in v.__name__
                and os.path.join("{}", "__init__.py").format(backend_str)
                not in v.__file__
            ):
                _unset_sub_backend_from_ivy(
                    original[k].__dict__,
                    target.__dict__[k],
                    sub_backend.__dict__[k],
                    sub_backend_str,
                )


def clear_sub_backends():
    if ivy.current_sub_backends():
        ivy.__dict__.update(original_backend_dict)
        ivy.current_backend().sub_backends._current_sub_backends = []


# This is only used in set_backend in handler.py
def _clear_current_sub_backends():
    global original_backend_dict
    original_backend_dict = None
    if ivy.current_sub_backends():
        ivy.current_backend().sub_backends._current_sub_backends = []


# this is overwritten when setting a backend
def available_sub_backends():
    for k, v in _backend_to_sub_backends_dict.items():
        print(f"backend: {k} supports sub_backends: {v}")


def find_available_sub_backends(sub_backends_loc):
    available_sub_backends = []
    for sub_backend in os.listdir(sub_backends_loc):
        if sub_backend.startswith("__") or not os.path.isdir(
            os.path.join(sub_backends_loc, sub_backend)
        ):
            continue

        elif importlib.util.find_spec(sub_backend):
            available_sub_backends.append(sub_backend)

    return available_sub_backends


def _find_available_sub_backend_implementations(sub_backends):
    result = dict()
    for sub in sub_backends:
        sub_backend = ivy.utils.dynamic_import.import_module(_sub_backend_dict[sub])
        for k, v in sub_backend.__dict__.items():
            if isinstance(v, Callable) and not k.startswith("__"):
                result[k] = result.get(k, []) + [sub]

    return result


def available_sub_backend_implementations(obj: str) -> list:
    """
    Return whether a sub-backend implementation is available for `obj`.

    Parameters
    ----------
    obj : str
        the object for which to check if a sub-backend implementation is available.

    Returns
    -------
    ret : list
        a list of sub-backend implementations available for `obj`.

    Examples
    --------
    >>> import ivy
    >>> ivy.set_backend('torch')
    >>> ivy.available_sub_backend_implementations("scaled_dot_product_attention")
    ['xformers']
    >>> ivy.set_backend('numpy')
    >>> ivy.available_sub_backend_implementations("scaled_dot_product_attention")
    []
    """
    obj = _check_callable(obj)
    sub_backends = ivy.current_backend().available_sub_backends()
    if not sub_backends:
        return []
    if not _sub_backends_implementations_already_verified():
        _verify_sub_backends_implementations(sub_backends)
    return _available_implementations_for(obj)


def _check_callable(obj):
    if isinstance(obj, str):
        obj = getattr(ivy, obj)
    if not callable(obj):
        raise TypeError(
            "The argument `obj` must be a callable or a string representing a callable"
        )
    return obj


def _sub_backends_implementations_already_verified():
    return (
        ivy.current_backend_str() in _available_sub_backends_implementations_dict.keys()
    )


def _verify_sub_backends_implementations(sub_backends):
    _available_sub_backends_implementations_dict[ivy.current_backend_str()] = (
        _find_available_sub_backend_implementations(sub_backends)
    )


def _available_implementations_for(obj):
    return _available_sub_backends_implementations_dict[ivy.current_backend_str()].get(
        obj.__name__, []
    )
