# global
import copy
import inspect
import logging
from typing import Callable, Dict
import functools

import tensorflow as tf

# local
import ivy
import ivy.functional.frontends.tensorflow as frontend


def _tf_frontend_array_to_ivy(x):
    if isinstance(x, frontend.EagerTensor):
        return x.data
    return x


def ivy_array_to_tensorflow(x):
    if isinstance(x, ivy.Array) or ivy.is_native_array(x):
        return frontend.EagerTensor(x.data)
    return x


def _tf_array_to_ivy_array(x):
    if isinstance(x, tf.Tensor):
        return ivy.array(x)
    return x


def _to_ivy_array(x):
    return _tf_frontend_array_to_ivy(_tf_array_to_ivy_array(x))


def _has_nans(x):
    if isinstance(x, ivy.Container):
        return x.has_nans()
    elif isinstance(x, ivy.Array) or ivy.is_native_array(x):
        return ivy.isnan(x).any()
    elif isinstance(x, tuple):
        return any(_has_nans(xi) for xi in x)
    else:
        return False


def inputs_to_ivy_arrays(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        """
        Converts all `TensorFlow.Tensor` instances in both the positional and keyword
        arguments into `ivy.Array` instances, and then calls the function with the
        updated arguments.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with ivy arrays passed in the arguments.
        """
        has_out = False
        out = None
        if "out" in kwargs:
            out = kwargs["out"]
            del kwargs["out"]
            has_out = True

        # convert all arrays in the inputs to ivy.Array instances
        ivy_args = ivy.nested_map(args, _to_ivy_array, include_derived=True)
        ivy_kwargs = ivy.nested_map(kwargs, _to_ivy_array, include_derived=True)
        if has_out:
            ivy_kwargs["out"] = out
        return fn(*ivy_args, **ivy_kwargs)

    new_fn.inputs_to_ivy_arrays = True
    return new_fn


def outputs_to_tensorflow_array(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        """
        Calls the function, and then converts all `tensorflow.Tensor` instances in
        the function return into `ivy.Array` instances.

        Parameters
        ----------
        args
            The arguments to be passed to the function.

        kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
            The return of the function, with ivy arrays as tensorflow.Tensor arrays.
        """
        # call unmodified function
        ret = fn(*args, **kwargs)

        # convert all arrays in the return to `frontend.Tensorflow.tensor` instances
        return ivy.nested_map(
            ret, ivy_array_to_tensorflow, include_derived={tuple: True}
        )

    new_fn.outputs_to_tensorflow_array = True
    return new_fn


def to_ivy_arrays_and_back(fn: Callable) -> Callable:
    return outputs_to_tensorflow_array(inputs_to_ivy_arrays(fn))


# update kwargs dictionary keys helper
def update_kwarg_keys(kwargs: Dict, to_update: Dict) -> Dict:
    """A helper function for updating the key-word only arguments dictionary.

    Parameters
    ----------
    kwargs
        A dictionary containing key-word only arguments to be updated.

    to_update
        The dictionary containing keys to update from raw_ops function the mapping
        is raw_ops argument name against corresponding tf_frontend argument name.

    Returns
    -------
    ret
        An updated dictionary with new keyword mapping
    """
    updated_kwargs = copy.deepcopy(kwargs)
    for key, val in to_update.items():
        for k in kwargs.keys():
            if key == k:
                temp_key = updated_kwargs[k]
                del updated_kwargs[k]
                updated_kwargs[val] = temp_key
    return updated_kwargs


def map_raw_ops_alias(alias: callable, kwargs_to_update: Dict = None) -> callable:
    """
    Mapping the raw_ops function with its respective frontend alias function,
    as the implementations of raw_ops is way similar to that of frontend functions,
    except that only arguments are passed as key-word only in raw_ops functions.

    Parameters
    ----------
    alias:
        The frontend function that is being referenced to as an alias to the
        current raw_ops function.
    kwargs_to_update:
        A dictionary containing key-word args to update to conform with a given
        raw_ops function

    Returns
    -------
    ret
        A decorated tf_frontend function to alias a given raw_ops function.
        Only accepting key-word only arguments.
    """

    def _wrap_raw_ops_alias(fn: callable, kw_update: Dict) -> callable:
        # removing decorators from frontend function
        fn = inspect.unwrap(fn)

        def _wraped_fn(**kwargs):
            # update kwargs dictionary keys
            if kw_update:
                kwargs = update_kwarg_keys(kwargs, kw_update)
            return fn(**kwargs)

        return _wraped_fn

    return _wrap_raw_ops_alias(alias, kwargs_to_update)


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
        # skip the check if the current nan policy is `nothing``
        if ivy.get_nan_policy() == "nothing":
            return fn(*args, **kwargs)

        # check all args and kwards for presence of nans
        result = ivy.nested_any(args, _has_nans) or ivy.nested_any(
            kwargs, _has_nans)

        if result:
            # handle nans based on the selected policy
            if ivy.get_nan_policy() == "raise_exception":
                raise ivy.exceptions.IvyException(
                    "Nans are not allowed in `raise_exception` policy.")
            elif ivy.get_nan_policy() == "warns":
                logging.warning("Nans are present in the input.")
        
        return fn(*args, **kwargs)

    new_fn.handle_nans = True
    return new_fn
