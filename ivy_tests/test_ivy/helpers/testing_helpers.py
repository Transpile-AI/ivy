# general
import importlib
import inspect
from hypothesis import given, strategies as st

# local
import ivy
from ivy_tests.test_ivy import conftest as cfg  # TODO temporary
from .hypothesis_helpers import number_helpers as nh
from .globals import TestData


cmd_line_args = (
    "with_out",
    "instance_method",
    "test_gradients",
)
cmd_line_args_lists = (
    "as_variable",
    "native_array",
    "container",
)


@st.composite
def num_positional_args(draw, *, fn_name: str = None):
    """Draws an integers randomly from the minimum and maximum number of positional
    arguments a given function can take.

    Parameters
    ----------
    draw
        special function that draws data randomly (but is reproducible) from a given
        data-set (ex. list).
    fn_name
        name of the function.

    Returns
    -------
    A strategy that can be used in the @given hypothesis decorator.

    Examples
    --------
    @given(
        num_positional_args=num_positional_args(fn_name="floor_divide")
    )
    @given(
        num_positional_args=num_positional_args(fn_name="add")
    )
    """
    num_positional_only = 0
    num_keyword_only = 0
    total = 0
    fn = None
    for i, fn_name_key in enumerate(fn_name.split(".")):
        if i == 0:
            fn = ivy.__dict__[fn_name_key]
        else:
            fn = fn.__dict__[fn_name_key]
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
    return draw(
        nh.ints(min_value=num_positional_only, max_value=(total - num_keyword_only))
    )


@st.composite
def num_positional_args_from_fn(draw, *, fn: str = None):
    """Draws an integers randomly from the minimum and maximum number of positional
    arguments a given function can take.

    Parameters
    ----------
    draw
        special function that draws data randomly (but is reproducible) from a given
        data-set (ex. list).
    fn
        name of the function.

    Returns
    -------
    A strategy that can be used in the @given hypothesis decorator.

    Examples
    --------
    @given(
        num_positional_args=num_positional_args_from_fn(fn="floor_divide")
    )
    @given(
        num_positional_args=num_positional_args_from_fn(fn="add")
    )
    """
    num_positional_only = 0
    num_keyword_only = 0
    total = 0
    for param in inspect.signature(fn).parameters.values():
        total += 1
        if param.kind == param.POSITIONAL_ONLY:
            num_positional_only += 1
        elif param.kind == param.KEYWORD_ONLY:
            num_keyword_only += 1
        elif param.kind == param.VAR_KEYWORD:
            num_keyword_only += 1
    return draw(
        nh.ints(min_value=num_positional_only, max_value=(total - num_keyword_only))
    )


# Decorators helpers


def _import_fn(fn_tree: str):
    """
    Imports a function from function tree string
    Parameters
    ----------
    fn_tree
        Full function tree without "ivy" root
        example: "functional.backends.jax.creation.arange".
    Returns
    -------
    Returns fn_name, imported module, callable function
    """
    split_index = fn_tree.rfind(".")
    fn_name = fn_tree[split_index + 1 :]
    module_to_import = fn_tree[:split_index]
    mod = importlib.import_module(module_to_import)
    callable_fn = mod.__dict__[fn_name]
    return callable_fn, fn_name, module_to_import


def _generate_shared_test_flags(_given_kwargs: dict, fn_tree: str, fn: callable):
    """
    Generates flags that all tests use.
    Returns
    -------

    """
    _given_kwargs["num_positional_args"] = num_positional_args(fn_name=fn_tree)
    for flag_key, flag_value in cfg.GENERAL_CONFIG_DICT.items():
        _given_kwargs[flag_key] = st.just(flag_value)
    for flag in cfg.UNSET_TEST_CONFIG_LISTS:
        _given_kwargs[flag] = st.lists(st.booleans(), min_size=1, max_size=1)
    for flag in cfg.UNSET_TEST_CONFIG_SINGLE:
        _given_kwargs[flag] = st.booleans()
        # Override with_out to be compatible
    for k in inspect.signature(fn).parameters.keys():
        if k.endswith("out"):
            break
    else:
        _given_kwargs["with_out"] = st.just(False)
    return _given_kwargs


def _get_supported_devices_dtypes(fn_name: str, fn_module: str):
    supported_device_dtypes = {}
    backends = ["numpy", "jax", "tensorflow", "torch"]  # TODO temporary
    for b in backends:  # ToDo can optimize this ?
        ivy.set_backend(b)
        _tmp_mod = importlib.import_module(fn_module)
        _fn = _tmp_mod.__dict__[fn_name]
        supported_device_dtypes[b] = ivy.function_supported_devices_and_dtypes(_fn)
        ivy.unset_backend()
    return supported_device_dtypes


# Decorators


def handle_test(*, fn_tree: str, **_given_kwargs):
    fn_tree = "ivy.functional.ivy." + fn_tree
    callable_fn, fn_name, fn_mod = _import_fn(fn_tree)
    is_hypothesis_test = len(_given_kwargs) != 0
    # TODO add support for flexible kwargs based on the function itself.
    if is_hypothesis_test:
        _given_kwargs = _generate_shared_test_flags(_given_kwargs, fn_tree, callable_fn)
    supported_device_dtypes = _get_supported_devices_dtypes(fn_name, fn_mod)

    def test_wrapper(test_fn):
        # No Hypothesis @given is used
        if is_hypothesis_test:

            def wrapped_test(*args, **kwargs):
                __tracebackhide__ = True
                wrapped_hypothesis_test = given(**_given_kwargs)(test_fn)
                return wrapped_hypothesis_test(fn_tree=fn_name, *args, **kwargs)

        else:
            wrapped_test = test_fn

        wrapped_test.test_data = TestData(
            test_fn=wrapped_test,
            fn_tree=fn_tree,
            fn_name=fn_name,
            supported_device_dtypes=supported_device_dtypes,
        )

        return wrapped_test

    return test_wrapper


def handle_frontend_test(*, fn_tree: str, **_given_kwargs):
    fn_tree = "ivy.functional.frontends." + fn_tree
    callable_fn, fn_name, fn_mod = _import_fn(fn_tree)
    is_hypothesis_test = len(_given_kwargs) != 0
    if is_hypothesis_test:
        _given_kwargs = _generate_shared_test_flags(_given_kwargs, fn_tree, callable_fn)
    supported_device_dtypes = _get_supported_devices_dtypes(fn_name, fn_mod)

    def test_wrapper(test_fn):
        if is_hypothesis_test:

            def wrapped_test(fixt_frontend_str, *args, **kwargs):
                __tracebackhide__ = True
                wrapped_hypothesis_test = given(**_given_kwargs)(test_fn)
                return wrapped_hypothesis_test(
                    fn_tree=fn_tree, frontend=fixt_frontend_str, *args, **kwargs
                )

        else:
            wrapped_test = test_fn

        wrapped_test.test_data = TestData(
            test_fn=wrapped_test,
            fn_tree=fn_tree,
            fn_name=fn_name,
            supported_device_dtypes=supported_device_dtypes,
        )

        return wrapped_test

    return test_wrapper


@st.composite
def seed(draw):
    return draw(st.integers(min_value=0, max_value=2**8 - 1))
