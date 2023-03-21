# local
import ivy
from ivy.functional.frontends.numpy.func_wrapper import (
    to_ivy_arrays_and_back,
)
import sys


@to_ivy_arrays_and_back
def reshape(x, /, newshape, order="C"):
    return ivy.reshape(x, shape=newshape, order=order)


@to_ivy_arrays_and_back
def resize(x, /, newshape, refcheck=True):
    if refcheck:
        if sys.getrefcount(x) > 2:
            raise ValueError('cannot resize an array that has been referenced by another array this way.\
                             Put refcheck to be False ')

    x = ravel(x)

    total_size = 1
    for diff_size in newshape:
        total_size *= diff_size
        if diff_size < 0:
            raise ValueError('values must not be negative')
    
    if x.size == 0 or total_size == 0:
        return ivy.zeros_like(x)   
    
    repetition = -(-total_size//x.size)
    zeros = ivy.zeros((repetition * repetition),dtype=int)
    x = ivy.concat((x,zeros))[:total_size]
    # or
    # x = ivy.concat((x,) * repetition)[:total_size]
    return ivy.reshape(x,newshape=newshape,order="C")
    # return ivy.resize(x, newshape=newshape, refcheck=refcheck)



@to_ivy_arrays_and_back
def broadcast_to(array, shape, subok=False):
    return ivy.broadcast_to(array, shape)


@to_ivy_arrays_and_back
def ravel(a, order="C"):
    return ivy.reshape(a, shape=(-1,), order=order)


@to_ivy_arrays_and_back
def moveaxis(a, source, destination):
    return ivy.moveaxis(a, source, destination)
