# global
from typing import Union, Optional

import paddle
import ivy.functional.backends.paddle as paddle_backend
import ivy
from ivy import promote_types_of_inputs
from ivy.func_wrapper import (
    with_unsupported_device_and_dtypes,
    with_supported_dtypes,
    with_unsupported_dtypes,
)

# local
from . import backend_version


def _elementwise_helper(x1, x2):
    x1, x2 = ivy.promote_types_of_inputs(x1, x2)
    x1, x2 = paddle_backend.broadcast_arrays(x1, x2)
    return x1, x2, x1.dtype


@with_unsupported_dtypes(
    {"2.5.1 and below": ("int8", "uint8", "float16", "bool", "bfloat16")},
    backend_version,
)
def add(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    alpha: Optional[Union[int, float]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if alpha not in (1, None):
        x2 = paddle_backend.multiply(x2, alpha)
        x1, x2 = ivy.promote_types_of_inputs(x1, x2)
    return paddle.add(x1, x2).astype(ret_dtype)


def bitwise_xor(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.bitwise_xor(x1, x2)


@with_supported_dtypes({"2.5.1 and below": ("float",)}, backend_version)
def expm1(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    return paddle.expm1(x)


def bitwise_invert(
    x: Union[int, bool, paddle.Tensor], /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.bitwise_not(x)


@with_unsupported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": (
                "int8",
                "int16",
                "uint8",
                "complex64",
                "complex128",
                "bool",
            )
        }
    },
    backend_version,
)
def isfinite(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.isfinite(x)


def isinf(
    x: paddle.Tensor,
    /,
    *,
    detect_positive: bool = True,
    detect_negative: bool = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if detect_negative and detect_positive:
        return paddle.isinf(x)

    if detect_negative:
        return paddle_backend.equal(x, float("-inf"))

    if detect_positive:
        return paddle_backend.equal(x, float("inf"))

    return paddle.zeros(shape=x.shape, dtype=bool)


def equal(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    diff = paddle_backend.subtract(x1, x2)
    ret = paddle_backend.logical_and(
        paddle_backend.less_equal(diff, 0), paddle_backend.greater_equal(diff, 0)
    )
    # ret result is sufficient for all cases except where the value is +/-INF of NaN
    return paddle_backend.where(
        paddle_backend.isnan(diff),
        ~paddle_backend.logical_or(paddle_backend.isnan(x1), paddle_backend.isnan(x2)),
        ret,
    )


@with_unsupported_dtypes(
    {"2.5.1 and below": ("int8", "int16", "bfloat16", "unsigned", "float16")},
    backend_version,
)
def less_equal(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if paddle.is_complex(x1):
        if paddle.is_complex(x1):
            real = paddle.less_equal(x1.real(), x2.real())
            imag = paddle.less_equal(x1.imag(), x2.imag())
            return paddle_backend.logical_and(real, imag)

    return paddle.less_equal(x1, x2)


def bitwise_and(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.bitwise_and(x1, x2)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def ceil(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.complex(paddle.ceil(x.real()), paddle.ceil(x.imag()))
    return paddle.ceil(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def floor(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.complex(paddle.floor(x.real()), paddle.floor(x.imag()))
    return paddle.floor(x)


@with_supported_dtypes({"2.5.1 and below": "float"}, backend_version)
def asin(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    return paddle.asin(x)


@with_supported_dtypes({"2.5.1 and below": "float"}, backend_version)
def asinh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    return paddle.asinh(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def sign(
    x: paddle.Tensor,
    /,
    *,
    np_variant: Optional[bool] = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.sgn(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def sqrt(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    """Calculate the square root with type handling."""
    if paddle.is_complex(x):
        angle = paddle.angle(x)
        return paddle.complex(
            paddle.cos(angle / 2), paddle.sin(angle / 2)
        ) * paddle.sqrt(paddle.abs(x))

    return paddle.sqrt(x)


@with_supported_dtypes({"2.5.1 and below": "float"}, backend_version)
def cosh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    return paddle.cosh(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def log10(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        base = paddle.to_tensor(10.0).squeeze()
        return paddle_backend.divide(
            paddle_backend.log(x), paddle_backend.log(base)
        ).astype(x.dtype)
    return paddle.log10(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def log2(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        base = paddle.to_tensor(2.0).squeeze()
        return paddle_backend.divide(
            paddle_backend.log(x), paddle_backend.log(base)
        ).astype(x.dtype)
    return paddle.log2(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def log1p(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.complex(paddle.log1p(paddle.abs(x)), paddle.angle(x + 1))
    return paddle.log1p(x)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "float",
            "int32",
            "int64",
            "complex",
        )
    },
    backend_version,
)
def isnan(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.logical_or(paddle.isnan(x.real()), paddle.isnan(x.imag()))
    return paddle.isnan(x)


@with_unsupported_dtypes(
    {
        "2.5.1 and below": (
            "int16",
            "int8",
            "uint8",
            "uint32",
            "uint64",
        )
    },
    backend_version,
)
def less(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if paddle.is_complex(x1):
        real = paddle.less_than(x1.real(), x2.real())
        imag = paddle.less_than(x1.imag(), x2.imag())
        return logical_and(real, imag)

    return paddle.less_than(x1, x2)


def multiply(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.multiply(x1, x2).astype(ret_dtype)


@with_supported_dtypes({"2.5.1 and below": "float"}, backend_version)
def cos(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    return paddle.cos(x)


@with_unsupported_dtypes(
    {"2.5.1 and below": ("uint",)},
    backend_version,
)
def logical_not(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.logical_and(
            paddle.logical_not(x.real()), paddle.logical_not(x.imag())
        )
    return paddle.logical_not(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64", "int32", "int64")}, backend_version
)
def divide(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return (x1 / x2).astype(ret_dtype)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "int32", "int64")},
    backend_version,
)
def fmin(
    x1: paddle.Tensor,
    x2: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if x1.dtype != x2.dtype:
        x1, x2 = promote_types_of_inputs(x1, x2)
    return paddle.fmin(x1, x2)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "bool",
            "float",
            "int32",
            "int64",
            "complex",
        )
    },
    backend_version,
)
def greater(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if paddle.is_complex(x1):
        if paddle.is_complex(x1):
            real = paddle.greater_than(x1.real(), x2.real())
            imag = paddle.greater_than(x1.imag(), x2.imag())
            return paddle.logical_and(real, imag)
    return paddle.greater_than(x1, x2)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "bool",
            "float",
            "int32",
            "int64",
            "complex",
        )
    },
    backend_version,
)
def greater_equal(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if paddle.is_complex(x1):
        if paddle.is_complex(x1):
            real = paddle.greater_equal(x1.real(), x2.real())
            imag = paddle.greater_equal(x1.imag(), x2.imag())
            return paddle.logical_and(real, imag)
    return paddle.greater_equal(x1, x2)


@with_supported_dtypes({"2.5.1 and below": ("float", "complex")}, backend_version)
def acos(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        # From https://github.com/python/cpython/blob/39ef93edb9802dccdb6555d4209ac2e60875a011/Modules/cmathmodule.c#L178 # noqa
        s1 = paddle_backend.sqrt(1 - x)
        s2 = paddle_backend.sqrt(1 + x)
        return paddle.complex(
            2.0 * paddle.atan2(s1.real(), s2.real()),
            paddle.asinh(s2.real() * s1.imag() - s2.imag() * s1.real()),
        )
    return paddle.acos(x)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "bool",
            "int8",
            "int16",
            "in32",
            "in64",
            "float",
        )
    },
    backend_version,
)
def logical_xor(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.logical_xor(x1, x2)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "bool",
            "int8",
            "int16",
            "in32",
            "in64",
            "float",
        )
    },
    backend_version,
)
def logical_and(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.logical_and(x1, x2)


@with_unsupported_dtypes(
    {"2.5.1 and below": ("uint",)},
    backend_version,
)
def logical_or(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if paddle.is_complex(x1):
        return paddle.logical_or(
            paddle.logical_or(x1.real(), x2.real()),
            paddle.logical_or(x1.imag(), x2.imag()),
        )
    return paddle.logical_or(x1, x2)


@with_supported_dtypes({"2.5.1 and below": ("float", "complex")}, backend_version)
def acosh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        # From https://github.com/python/cpython/blob/39ef93edb9802dccdb6555d4209ac2e60875a011/Modules/cmathmodule.c#L221 # noqa
        s1 = paddle_backend.sqrt(paddle.complex(x.real() - 1, x.imag()))
        s2 = paddle_backend.sqrt(paddle.complex(x.real() + 1, x.imag()))
        return paddle.complex(
            paddle.asinh(s1.real() * s2.real() + s1.imag() * s2.imag()),
            2.0 * paddle.atan2(s1.imag(), s2.real()),
        )
    return paddle.acosh(x)


@with_supported_dtypes({"2.5.1 and below": ("float", "complex")}, backend_version)
def sin(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        re = x.real()
        im = x.imag()
        return paddle.complex(
            paddle.sin(re) * paddle.cosh(im), paddle.cos(re) * paddle.sinh(im)
        )
    return paddle.sin(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64", "int8", "int16", "int32", "int64")},
    backend_version,
)
def negative(
    x: Union[float, paddle.Tensor], /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.neg(x)


def not_equal(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.logical_not(paddle_backend.equal(x1, x2))


@with_supported_dtypes(
    {"2.5.1 and below": ("bfloat16", "float", "complex")},
    backend_version,
)
def tanh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        tanh_a = paddle.tanh(paddle.real(x))
        tan_b = paddle.tan(paddle.imag(x))
        return (tanh_a + 1j * tan_b) / (1 + 1j * (tanh_a * tan_b))
    return paddle.tanh(x)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "uint8",
            "int8",
            "int32",
            "int64",
            "float32",
            "float64",
            "float16",
            "bfloat16",
        )
    },
    backend_version,
)
def floor_divide(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.floor_divide(x1, x2)


@with_supported_dtypes(
    {"2.5.1 and below": ("bool", "uint8", "int8", "int16", "int32", "int64")},
    backend_version,
)
def bitwise_or(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.bitwise_or(x1, x2)


@with_supported_dtypes({"2.5.1 and below": ("float", "complex")}, backend_version)
def sinh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        re = x.real()
        im = x.imag()
        return paddle.complex(
            paddle.sinh(re) * paddle.cos(im), paddle.cosh(re) * paddle.sin(im)
        )
    return paddle.sinh(x)


def positive(
    x: Union[float, paddle.Tensor], /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if not isinstance(x, paddle.Tensor):
        x = paddle.to_tensor(
            x, dtype=ivy.default_dtype(item=x, as_native=True)
        ).squeeze()
    return x.clone()


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "int32",
            "int64",
            "float",
            "complex",
        )
    },
    backend_version,
)
def square(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.square(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "int32", "int64", "complex")},
    backend_version,
)
def pow(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if paddle.is_complex(x1):
        # https://math.stackexchange.com/questions/476968/complex-power-of-a-complex-number
        r = paddle.abs(x1)
        theta = paddle.angle(x1)
        power = x2 * paddle.complex(paddle.log(r), theta)
        result = paddle.exp(power.real()) * paddle.complex(
            paddle.cos(power.imag()), paddle.sin(power.imag())
        )
        return result
    return paddle.pow(x1, x2)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def round(
    x: paddle.Tensor, /, *, decimals: int = 0, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    def _np_round(x):
        # this is a logic to mimic np.round behaviour
        # which rounds odd numbers up and even numbers down at limits like 0.5

        one = paddle.to_tensor(1, dtype="int64")

        # check if the number is even or odd
        is_even = paddle.bitwise_and(paddle_backend.trunc(x).astype("int64"), one) == 0

        # round the number to the nearest integer
        round_x = paddle.sign(x) * paddle.where(
            is_even, paddle.floor(x.abs()), paddle.ceil(x.abs())
        )

        # if the number was rounded up from an even number
        #   round the number down to the nearest even number
        return paddle.where(
            paddle.logical_and(
                paddle.bitwise_and(round_x.astype("int64"), one) == 1.0,
                is_even,
            ),
            round_x - 1.0,
            round_x,
        )

    if paddle.is_complex(x):
        return paddle.complex(
            _np_round(x.real(), decimals), _np_round(x.imag(), decimals)
        )
    return _np_round(x, decimals).astype(x.dtype)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def trunc(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.complex(paddle.trunc(x.real()), paddle.trunc(x.imag()))
    return paddle.trunc(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float64", "float32")},
    backend_version,
)
def trapz(
    y: paddle.Tensor,
    /,
    *,
    x: Optional[paddle.Tensor] = None,
    dx: Optional[float] = 1.0,
    axis: Optional[int] = -1,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if x is None:
        d = dx
    else:
        if x.ndim == 1:
            d = paddle.diff(x)
            # reshape to correct shape
            shape = [1] * y.ndim
            shape[axis] = d.shape[0]
            d = d.reshape(shape)
        else:
            d = paddle.diff(x, axis=axis)

    slice1 = [slice(None)] * y.ndim
    slice2 = [slice(None)] * y.ndim

    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)

    with ivy.ArrayMode(False):
        if y.shape[axis] < 2:
            return ivy.zeros_like(ivy.squeeze(y, axis=axis))
        ret = ivy.sum(
            ivy.divide(
                ivy.multiply(
                    d,
                    ivy.add(
                        ivy.get_item(y, tuple(slice1)), ivy.get_item(y, tuple(slice2))
                    ),
                ),
                2.0,
            ),
            axis=axis,
        )

    return ret


def abs(
    x: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if not isinstance(x, paddle.Tensor):
        x = paddle.to_tensor(x, dtype=ivy.default_dtype(item=x)).squeeze()
    return paddle.abs(x)


@with_unsupported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("float16",)}}, backend_version
)
def logaddexp(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    amax = paddle_backend.maximum(x1, x2)
    return amax + paddle_backend.log(
        paddle_backend.exp(x1 - amax) + paddle_backend.exp(x2 - amax)
    ).astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("float16",)}}, backend_version
)
def logaddexp2(
    x1: Union[paddle.Tensor, float, list, tuple],
    x2: Union[paddle.Tensor, float, list, tuple],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    with ivy.ArrayMode(False):
        return ivy.log2(ivy.exp2(x1) + ivy.exp2(x2))


@with_unsupported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": (
                "int8",
                "int16",
                "int32",
                "int64",
                "uint8",
                "float16",
                "float32",
                "float64",
                "bool",
            )
        }
    },
    backend_version,
)
def real(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    return paddle.real(x)


@with_supported_dtypes({"2.5.1 and below": ("float", "complex")}, backend_version)
def tan(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        tanh_ix = paddle_backend.tanh(paddle.complex(-x.imag(), x.real()))
        return paddle.complex(tanh_ix.imag(), -tanh_ix.real())
    return paddle.tan(x)


@with_supported_dtypes({"2.5.1 and below": ("float", "complex")}, backend_version)
def atan(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if x.dtype in [paddle.complex64, paddle.complex128]:
        atanh_iz = paddle_backend.atanh(paddle.complex(-x.imag(), x.real()))
        return paddle.complex(atanh_iz.imag(), -atanh_iz.real())
    return paddle.atan(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("int32", "int64", "float")},
    backend_version,
)
def atan2(
    x1: paddle.Tensor, x2: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.atan2(x1, x2).astype(ret_dtype)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "complex")},
    backend_version,
)
def log(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.complex(paddle.log(paddle.abs(x)), paddle.angle(x))
    return paddle.log(x)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "int32",
            "int64",
            "float",
            "complex",
        )
    },
    backend_version,
)
def exp(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    return paddle.exp(x)


def exp2(
    x: Union[paddle.Tensor, float, list, tuple],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    with ivy.ArrayMode(False):
        return ivy.pow(2, x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64", "int32", "int64")}, backend_version
)
def subtract(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    alpha: Optional[Union[int, float]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if alpha not in (1, None):
        x2 = paddle_backend.multiply(x2, alpha)
        x1, x2 = ivy.promote_types_of_inputs(x1, x2)
    return paddle.subtract(x1, x2).astype(ret_dtype)


@with_supported_dtypes(
    {"2.5.1 and below": ("float", "int32", "int64")},
    backend_version,
)
def remainder(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    modulus: bool = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if not modulus:
        res = paddle_backend.divide(x1, x2)
        res_floored = paddle_backend.where(
            paddle_backend.greater_equal(res, 0.0),
            paddle_backend.floor(res),
            paddle_backend.ceil(res),
        )
        diff = paddle_backend.subtract(res, res_floored).astype(res.dtype)
        return paddle_backend.round(paddle_backend.multiply(diff, x2)).astype(x1.dtype)

    return paddle.remainder(x1, x2).astype(ret_dtype)


@with_supported_dtypes({"2.5.1 and below": ("float", "complex")}, backend_version)
def atanh(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    if paddle.is_complex(x):
        return 0.5 * (paddle_backend.log(1 + x) - paddle_backend.log(1 - x))
    return paddle.atanh(x)


def bitwise_right_shift(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.floor(x1.astype("float64") / 2 ** x2.astype("float64")).astype(
        ret_dtype
    )


def bitwise_left_shift(
    x1: Union[int, bool, paddle.Tensor],
    x2: Union[int, bool, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    return paddle.floor(x1.astype("float64") * 2 ** x2.astype("float64")).astype(
        ret_dtype
    )


# Extra #
# ------#


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64")},
    backend_version,
)
def erf(x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None) -> paddle.Tensor:
    return paddle.erf(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64", "int32", "int64", "complex")},
    backend_version,
)
def minimum(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    use_where: bool = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if paddle.is_complex(x1):
        use_where = True

    if use_where:
        return paddle_backend.where(paddle_backend.less_equal(x1, x2), x1, x2).astype(
            ret_dtype
        )

    return paddle.minimum(x1, x2).astype(ret_dtype)


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64", "int32", "int64", "complex")},
    backend_version,
)
def maximum(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    use_where: bool = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    if paddle.is_complex(x1):
        use_where = True
    if use_where:
        return paddle_backend.where(
            paddle_backend.greater_equal(x1, x2), x1, x2
        ).astype(ret_dtype)
    return paddle.maximum(x1, x2).astype(ret_dtype)


@with_supported_dtypes({"2.5.1 and below": "float"}, backend_version)
def reciprocal(
    x: Union[float, paddle.Tensor], /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.reciprocal(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64", "int32", "int64")}, backend_version
)
def deg2rad(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.deg2rad(x)


@with_supported_dtypes(
    {"2.5.1 and below": ("float32", "float64", "int32", "int64")}, backend_version
)
def rad2deg(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    return paddle.rad2deg(x)


def trunc_divide(
    x1: Union[float, paddle.Tensor],
    x2: Union[float, paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle_backend.trunc(paddle_backend.divide(x1, x2))


def isreal(
    x: paddle.Tensor, /, *, out: Optional[paddle.Tensor] = None
) -> paddle.Tensor:
    if paddle.is_complex(x):
        return paddle.logical_not(x.imag().astype(bool))
    else:
        return paddle.ones_like(x, dtype="bool")


def fmod(
    x1: paddle.Tensor,
    x2: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2, ret_dtype = _elementwise_helper(x1, x2)
    res = paddle_backend.remainder(paddle_backend.abs(x1), paddle_backend.abs(x2))
    return paddle_backend.where(paddle_backend.less(x1, 0), -res, res)


@with_supported_dtypes({"2.5.1 and below": ("int32", "int64")}, backend_version)
def lcm(
    x1: paddle.Tensor,
    x2: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.lcm(x1, x2)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "float",
            "complex",
        ),
    },
    backend_version,
)
def angle(
    input: paddle.Tensor,
    /,
    *,
    deg: Optional[bool] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    result = paddle.angle(input)
    if deg:
        result = paddle.rad2deg(result)
    return result


@with_supported_dtypes({"2.5.1 and below": ("int32", "int64")}, backend_version)
def gcd(
    x1: Union[paddle.Tensor, int, list, tuple],
    x2: Union[paddle.Tensor, float, list, tuple],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    x1, x2 = promote_types_of_inputs(x1, x2)
    return paddle.gcd(x1, x2)


@with_supported_dtypes({"2.5.1 and below": "complex"}, backend_version)
def imag(
    val: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.imag(val)


def nan_to_num(
    x: paddle.Tensor,
    /,
    *,
    copy: Optional[bool] = True,
    nan: Optional[Union[float, int]] = 0.0,
    posinf: Optional[Union[float, int]] = None,
    neginf: Optional[Union[float, int]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    with ivy.ArrayMode(False):
        if ivy.is_int_dtype(x):
            if posinf is None:
                posinf = ivy.iinfo(x).max
            if neginf is None:
                neginf = ivy.iinfo(x).min
        elif ivy.is_float_dtype(x) or ivy.is_complex_dtype(x):
            if posinf is None:
                posinf = ivy.finfo(x).max
            if neginf is None:
                neginf = ivy.finfo(x).min
        ret = ivy.where(ivy.isnan(x), paddle.to_tensor(nan, dtype=x.dtype), x)
        ret = ivy.where(
            ivy.logical_and(ivy.isinf(ret), ret > 0),
            paddle.to_tensor(posinf, dtype=x.dtype),
            ret,
        )
        ret = ivy.where(
            ivy.logical_and(ivy.isinf(ret), ret < 0),
            paddle.to_tensor(neginf, dtype=x.dtype),
            ret,
        )
        if copy:
            return ret.clone()
        else:
            x = ret
            return x
