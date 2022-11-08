# global
import functools
import logging
from typing import Callable

import torch

# local
import ivy
import ivy.functional.frontends.torch as torch_frontend


def _from_torch_frontend_tensor_to_ivy_array(x):
    if isinstance(x, torch_frontend.Tensor):
        return x.data
    return x


def _from_ivy_array_to_torch_frontend_tensor(x, nested=False, include_derived=None):
    if nested:
        return ivy.nested_map(
            x, _from_ivy_array_to_torch_frontend_tensor, include_derived
        )
    elif isinstance(x, ivy.Array) or ivy.is_native_array(x):
        return torch_frontend.Tensor(x)
    return x


def _from_torch_tensor_to_ivy_array(x):
    if isinstance(x, torch.Tensor):
        return ivy.array(x)
    return x


def _to_ivy_array(x):
    return _from_torch_frontend_tensor_to_ivy_array(_from_torch_tensor_to_ivy_array(x))


def _is_nan(x):
    if isinstance(x, ivy.Array) or ivy.is_native_array(x):
        return ivy.isnan(x).any().item()
    else:
        return False


def inputs_to_ivy_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        """
        Converts all `Tensor` instances in both the positional and keyword
        arguments into `ivy.Array` instances, and then calls the function with the
        updated arguments.
        """
        # Remove out argument if present in kwargs
        has_out = False
        out = None
        if "out" in kwargs:
            out = kwargs["out"]
            del kwargs["out"]
            has_out = True
        # convert all input arrays to ivy.Array instances
        new_args = ivy.nested_map(
            args,
            _to_ivy_array,
            include_derived={tuple: True},
        )
        new_kwargs = ivy.nested_map(
            kwargs,
            _to_ivy_array,
            include_derived={tuple: True},
        )
        # add the original out argument back to the keyword arguments
        if has_out:
            new_kwargs["out"] = out
        return fn(*new_args, **new_kwargs)

    return new_fn


def outputs_to_frontend_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        """
        Calls the function, and then converts all `ivy.Array` instances returned
        by the function into `Tensor` instances.
        """
        # call unmodified function
        ret = fn(*args, **kwargs)
        # convert all arrays in the return to `torch_frontend.Tensor` instances
        return _from_ivy_array_to_torch_frontend_tensor(
            ret, nested=True, include_derived={tuple: True}
        )

    return new_fn


def to_ivy_arrays_and_back(fn: Callable) -> Callable:
    """
    Wraps `fn` so that input arrays are all converted to `ivy.Array` instances
    and return arrays are all converted to `Tensor` instances.
    """
    return outputs_to_frontend_arrays(inputs_to_ivy_arrays(fn))


def handle_nans(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        """
        Checks for the existence of nans in all arrays in the `args`
        and `kwargs`. The presence of nans is then handled depending
        on the enabled `nan_policy`.

        Following policies apply:
        raise_exception: raises an exception in case nans are present
        warns: warns a user in case nans are present
        nothing: does nothing

        Parameters
        ----------
        args
            The arguments to be passed to the function.
        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with handling of inputs based
            on the selected `nan_policy`.
        """
        # check all args and kwards for presence of nans
        args_nans = ivy.nested_map(args, _is_nan, include_derived={tuple: True})
        kwargs_nans = ivy.nested_map(
            kwargs, _is_nan, include_derived={tuple: True}
        )
        if type(args_nans) is dict:
            args_result = any(list(args_nans.values()))
        else:
            args_result = any(list(args_nans))
        
        if type(kwargs_nans) is dict:
            kwargs_result = any(list(kwargs_nans.values()))
        else:
            kwargs_result = any(list(kwargs_nans))

        if args_result or kwargs_result:
            # handle nans based on the selected policy
            if ivy.get_nan_policy() == "raise_exception":
                raise ivy.exceptions.IvyException(
                    "Nans are not allowed in `raise_exception` policy.")
            elif ivy.get_nan_policy() == "warns":
                logging.warning("Nans are present in the input.")
        
        return fn(*args, **kwargs)

    new_fn.handle_nans = True
    return new_fn
