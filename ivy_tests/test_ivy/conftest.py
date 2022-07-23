# global
import os
import pytest
from typing import Dict, Union, Tuple
from hypothesis import settings

settings.register_profile("default", max_examples=5, deadline=None)
settings.load_profile("default")

# local
from ivy_tests.test_ivy import helpers
from ivy import clear_backend_stack, DefaultDevice


FW_STRS = ["numpy", "jax", "tensorflow", "torch", "mxnet"]


TEST_BACKENDS: Dict[str, callable] = {
    "numpy": lambda: helpers.get_ivy_numpy(),
    "jax": lambda: helpers.get_ivy_jax(),
    "tensorflow": lambda: helpers.get_ivy_tensorflow(),
    "torch": lambda: helpers.get_ivy_torch(),
    "mxnet": lambda: helpers.get_ivy_mxnet(),
}
TEST_CALL_METHODS: Dict[str, callable] = {
    "numpy": helpers.np_call,
    "jax": helpers.jnp_call,
    "tensorflow": helpers.tf_call,
    "torch": helpers.torch_call,
    "mxnet": helpers.mx_call,
}
global CONFIG_DICT
CONFIG_DICT: Dict[str, Union[Tuple[bool, bool], None, bool]] = {
    "as-variable": None,
    "native-array": None,
    "with-out": None,
    "nestable": None,
    "instance-method": None,
}
MAP_BOOL_FLAGS: Dict[str, bool] = {
    "true": True,
    "false": False,
}

if "ARRAY_API_TESTS_MODULE" not in os.environ:
    os.environ["ARRAY_API_TESTS_MODULE"] = "ivy.functional.backends.numpy"


@pytest.fixture(autouse=True)
def run_around_tests(device, f, compile_graph, implicit, call, fw):
    if "gpu" in device and call is helpers.np_call:
        # Numpy does not support GPU
        pytest.skip()
    clear_backend_stack()
    with f.use:
        with DefaultDevice(device):
            yield


def pytest_generate_tests(metafunc):

    # device
    raw_value = metafunc.config.getoption("--device")
    if raw_value == "all":
        devices = ["cpu", "gpu:0", "tpu:0"]
    else:
        devices = raw_value.split(",")

    # framework
    raw_value = metafunc.config.getoption("--backend")
    if raw_value == "all":
        backend_strs = TEST_BACKENDS.keys()
    else:
        backend_strs = raw_value.split(",")

    # compile_graph
    raw_value = metafunc.config.getoption("--compile_graph")
    if raw_value == "both":
        compile_modes = [True, False]
    elif raw_value == "true":
        compile_modes = [True]
    else:
        compile_modes = [False]

    # implicit
    raw_value = metafunc.config.getoption("--with_implicit")
    if raw_value == "true":
        implicit_modes = [True, False]
    else:
        implicit_modes = [False]

    # create test configs
    configs = list()
    for backend_str in backend_strs:
        for device in devices:
            for compile_graph in compile_modes:
                for implicit in implicit_modes:
                    configs.append(
                        (
                            device,
                            TEST_BACKENDS[backend_str](),
                            compile_graph,
                            implicit,
                            TEST_CALL_METHODS[backend_str],
                            backend_str,
                        )
                    )

    metafunc.parametrize("device,f,compile_graph,implicit,call,fw", configs)


@pytest.fixture(scope="session")
def get_command_line_flags(request) -> Dict[str, bool]:

    a_v_f_s = request.config.getoption("--skip-variable-testing")
    n_f_s = request.config.getoption("--skip-native-array-testing")
    o_f_s = request.config.getoption("--skip-out-testing")
    n_s = request.config.getoption("--skip-nestable-testing")
    i_m_f_s = request.config.getoption("--skip-instance-method-testing")

    a_v_f_w = request.config.getoption("--with-variable-testing")
    n_f_w = request.config.getoption("--with-native-array-testing")
    o_f_w = request.config.getoption("--with-out-testing")
    n_w = request.config.getoption("--with-nestable-testing")
    i_m_f_w = request.config.getoption("--with-instance-method-testing")

    # mapping command line arguments, first element of the tuple is
    # the --skip flag, and the second is the --with flag
    CONFIG_DICT["as-variable"] = (MAP_BOOL_FLAGS[a_v_f_s], MAP_BOOL_FLAGS[a_v_f_w])
    CONFIG_DICT["native-array"] = (MAP_BOOL_FLAGS[n_f_s], MAP_BOOL_FLAGS[n_f_w])
    CONFIG_DICT["with-out"] = (MAP_BOOL_FLAGS[o_f_s], MAP_BOOL_FLAGS[o_f_w])
    CONFIG_DICT["nestable"] = (MAP_BOOL_FLAGS[n_s], MAP_BOOL_FLAGS[n_w])
    CONFIG_DICT["instance-method"] = (MAP_BOOL_FLAGS[i_m_f_s], MAP_BOOL_FLAGS[i_m_f_w])

    # final mapping for hypothesis value generation
    for k, v in CONFIG_DICT.items():
        # when both flags are true
        if v[0] and v[1]:
            raise Exception(
                f"--skip-{k}--testing and --with-{k}--testing flags cannot be tested together"
            )
        # skipping a test
        if v[0]:
            CONFIG_DICT[k] = False
        # extra testing
        if v[1]:
            CONFIG_DICT[k] = True
        # default
        if not v[0] ^ v[1]:
            CONFIG_DICT[k] = None

    return CONFIG_DICT


def pytest_addoption(parser):
    parser.addoption("--device", action="store", default="cpu")
    parser.addoption("--backend", action="store", default="jax,numpy,tensorflow,torch")
    parser.addoption("--compile_graph", action="store", default="true")
    parser.addoption("--with_implicit", action="store", default="false")

    parser.addoption("--skip-variable-testing", action="store", default="true")
    parser.addoption("--skip-native-array-testing", action="store", default="false")
    parser.addoption("--skip-out-testing", action="store", default="true")
    parser.addoption("--skip-nestable-testing", action="store", default="false")
    parser.addoption("--skip-instance-method-testing", action="store", default="true")

    parser.addoption("--with-variable-testing", action="store", default="false")
    parser.addoption("--with-native-array-testing", action="store", default="true")
    parser.addoption("--with-out-testing", action="store", default="false")
    parser.addoption("--with-nestable-testing", action="store", default="true")
    parser.addoption("--with-instance-method-testing", action="store", default="false")
