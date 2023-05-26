# TODO rename file
import ivy
from typing import Callable


class WithBackendContext:
    def __init__(self, backend) -> None:
        self.backend = backend

    def __enter__(self):
        return ivy.with_backend(self.backend, cached=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


# update_backend: Callable = ivy.utils.backend.ContextManager
update_backend: Callable = WithBackendContext
