# local
import ivy


def cat(tensors, dim=0, *, out=None):
    return ivy.concat(tensors, axis=dim, out=out)


def concat(tensors, dim=0, *, out=None):
    return ivy.concat(tensors, axis=dim, out=out)


def permute(input, dims):
    return ivy.permute_dims(input, axes=dims)


def swapdims(input, dim0, dim1):
    return ivy.swapaxes(input, dim0, dim1)


swapdims.unsupported_dtypes = (
    "uint16",
    "uint32",
    "uint64",
)


def transpose(input, dim0, dim1):
    return ivy.swapaxes(input, dim0, dim1)


def reshape(input, shape):
    return ivy.reshape(input, shape)


def stack(tensors, dim=0, *, out=None):
     return ivy.stack(tensors, axis=dim, out=out)


def movedim(input, source, destination):
    """
    If either dimension input is a tuple, 
    loop over both tuples and swap input tensor's axes individually in the correct order
    """
    if isinstance(source, tuple) or isinstance(destination, tuple):
        assert len(source) == len(destination), "if either dimension input is a tuple"\
                                                ", their size must match"
        map = {}
        for i, j in zip(source, destination):
            if i in map:
                i = map[i]
            if j in map:
                j = map[j]
            input = ivy.swapaxes(input, i, j)
            map[i] = j
            map[j] = i
        return input

    return ivy.swapaxes(input, source, destination)
