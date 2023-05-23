import pytest

from ivy_tests.test_ivy.helpers import globals as test_globals


@pytest.fixture(autouse=True)
def run_around_tests(request, on_device, backend_fw, frontend, compile_graph, implicit):
    if not hasattr(request.function, "test_data"):
        return

    try:
        test_globals.setup_frontend_test(
            request.function.test_data, frontend, backend_fw, on_device
        )
    except Exception as e:
        test_globals.teardown_frontend_test()
        raise RuntimeError(f"Setting up test for {request.function} failed.") from e
    yield
    test_globals.teardown_frontend_test()
