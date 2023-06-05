# global
import ivy
from ivy.functional.frontends.numpy.func_wrapper import to_ivy_arrays_and_back


@to_ivy_arrays_and_back
def argsort(
    x,
    /,
    *,
    axis=-1,
    kind=None,
    order=None,
):
    return ivy.argsort(x, axis=axis)


@to_ivy_arrays_and_back
def sort(a, axis=-1, kind=None, order=None):
    return ivy.sort(a, axis=axis)


@to_ivy_arrays_and_back
def msort(a):
    return ivy.msort(a)


@to_ivy_arrays_and_back
def sort_complex(a):
    return ivy.sort(a)


@to_ivy_arrays_and_back
def lexsort(keys, /, *, axis=-1):
    return ivy.lexsort(keys, axis=axis)


@to_ivy_arrays_and_back
def partition(a, kth, axis=-1, kind="introselect", order=None):
    indices = ivy.argsort(a, axis=axis)
    a = a[indices]
    if isinstance(kth, int):
        kth = [kth]
    index = ivy.argsort(a, axis=axis)
    partitions = ivy.split(index, ivy.searchsorted(ivy.sort(kth), index))
    sorted_partitions = [a[partition] for partition in partitions]
    return ivy.concat(sorted_partitions)
