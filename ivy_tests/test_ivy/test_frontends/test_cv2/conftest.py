import pytest


@pytest.fixture(scope="session")
def frontend():
    return "cv2"
