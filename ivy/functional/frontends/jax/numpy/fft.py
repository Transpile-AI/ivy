# local
import ivy
from ivy.functional.frontends.jax.func_wrapper import to_ivy_arrays_and_back
from ivy.func_wrapper import with_unsupported_dtypes


@to_ivy_arrays_and_back
def fft(a, n=None, axis=-1, norm=None):
    if norm is None:
        norm = "backward"
    return ivy.fft(a, axis, norm=norm, n=n)


@to_ivy_arrays_and_back
def fft2(a, s=None, axes=(-2, -1), norm=None):
    if norm is None:
        norm = "backward"
    return ivy.array(ivy.fft2(a, s=s, dim=axes, norm=norm), dtype=ivy.dtype(a))


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.4.2 and below": ("float16", "bfloat16")}, "paddle")
def fftshift(x, axes=None, name=None):
    shape = x.shape

    if axes is None:
        axes = tuple(range(x.ndim))
        shifts = [(dim // 2) for dim in shape]
    elif isinstance(axes, int):
        shifts = shape[axes] // 2
    else:
        shifts = [shape[ax] // 2 for ax in axes]

    roll = ivy.roll(x, shifts, axis=axes)

    return roll


@to_ivy_arrays_and_back
def hfft(x, n=None, axis=-1, norm="backward"):
    """Compute the FFT of a signal that has Hermitian symmetry, resulting in a real
    spectrum."""
    # Determine the input shape and axis length
    input_shape = x.shape
    input_len = input_shape[axis]

    # Calculate n if not provided
    if n is None:
        n = 2 * (input_len - 1)

    # Perform the FFT along the specified axis
    result = ivy.fft(x, axis, n=n, norm=norm)

    return ivy.real(result)


@to_ivy_arrays_and_back
def ifft(a, n=None, axis=-1, norm=None):
    if norm is None:
        norm = "backward"
    return ivy.ifft(a, axis, norm=norm, n=n)
