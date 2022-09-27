# global

# local
import ivy
import ivy.functional.frontends.numpy as np_frontend


class ndarray:
    def __init__(self, data):
        if ivy.is_native_array(data):
            data = ivy.Array(data)
        self.data = data

    # Instance Methoods #
    # -------------------#

    # Add argmax #
    def argmax(
        self,
        /,
        *,
        axis=None,
        out=None,
        keepdims=False,
    ):
        
        return np_frontend.argmax(
            self.data, 
            axis=axis,
            out=out,
            keepdims=keepdims,
        )

    def reshape(self, shape, order="C"):
        return np_frontend.reshape(self.data, shape)

    def add(
        self,
        value,
    ):
        return np_frontend.add(
            self.data,
            value,
        )
