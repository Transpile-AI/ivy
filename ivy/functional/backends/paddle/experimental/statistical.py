# global
from typing import Optional, Union, Tuple, Sequence
import paddle
import ivy.functional.backends.paddle as paddle_backend

# local
from ivy.func_wrapper import with_unsupported_device_and_dtypes
from . import backend_version


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": (
                "int8",
                "int16",
                "uint8",
                "float16",
                "complex64",
                "complex128",
                "bool",
            )
        }
    },
    backend_version,
)
def median(
    input: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[Tuple[int], int]] = None,
    keepdims: Optional[bool] = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    # keepdims is set to True because in versions up to 2.4.2
    # there was a problem when the axis was defined and it was the
    # only axis in the tensor so it needs to be handled manually

    ret_dtype = input.dtype
    if input.dtype not in [paddle.int32, paddle.int64, paddle.float32, paddle.float64]:
        if paddle.is_complex(input):
            ret = paddle.complex(
                paddle.median(input.real(), axis=axis, keepdim=True),
                paddle.median(input.imag(), axis=axis, keepdim=True),
            )
        else:
            ret = paddle.median(input.cast("float32"), axis=axis, keepdim=True)
    else:
        ret = paddle.median(input, axis=axis, keepdim=True)
    if not keepdims:
        ret = paddle_backend.squeeze(ret, axis=axis)
    # The following code is to simulate other frameworks
    # output shapes behaviour since min output dim is 1 in paddle
    if isinstance(axis, Sequence):
        if len(axis) == input.ndim:
            axis = None
    if (input.ndim == 1 or axis is None) and not keepdims:
        ret = ret.squeeze()
    return ret.astype(ret_dtype)


def nanmean(
    a: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[int, Tuple[int]]] = None,
    keepdims: Optional[bool] = False,
    dtype: Optional[paddle.dtype] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    ret_dtype = dtype if dtype is not None else a.dtype
    a = a.cast(
        ret_dtype
    )  # this is necessary to match other FWs behaviour which cast before calculation
    if a.dtype not in [paddle.int64, paddle.float32, paddle.float64]:
        if paddle.is_complex(a):
            ret = paddle.complex(
                paddle.nanmean(a.real(), axis=axis, keepdim=keepdims),
                paddle.nanmean(a.imag(), axis=axis, keepdim=keepdims),
            )
        else:
            ret = paddle.nanmean(a.cast("float32"), axis=axis, keepdim=keepdims)
    else:
        ret = paddle.nanmean(a, axis=axis, keepdim=keepdims)

    # The following code is to simulate other frameworks
    # output shapes behaviour since min output dim is 1 in paddle
    if isinstance(axis, Sequence):
        if len(axis) == a.ndim:
            axis = None
    if (a.ndim == 1 or axis is None) and not keepdims:
        ret = ret.squeeze()
    return ret.astype(ret_dtype)


def _compute_quantile(
    x, q, axis=None, keepdim=False, ignore_nan=False, interpolation="linear"
):
    # Validate x
    if not isinstance(x, paddle.Tensor):
        raise TypeError("input x should be a Tensor.")
    ret_dtype = x.dtype
    # Validate q
    if isinstance(q, (int, float)):
        q = [q]
    elif isinstance(q, (list, tuple)):
        if len(q) <= 0:
            raise ValueError("q should not be empty")
    elif isinstance(q, paddle.Tensor):
        q = q.tolist()
    else:
        raise TypeError("Type of q should be int, float, list or tuple.")

    # Validate axis
    dims = len(x.shape)
    out_shape = list(x.shape)
    if axis is None:
        x = paddle_backend.flatten(x)
        axis = 0
        out_shape = [1] * dims
    else:
        if isinstance(axis, (list, tuple)):
            if len(axis) <= 0:
                raise ValueError("axis should not be empty")
            axis_src, axis_dst = [], []
            for axis_single in axis:
                if not isinstance(axis_single, int) or not (
                    axis_single < dims and axis_single >= -dims
                ):
                    raise ValueError(
                        "Axis should be None, int, or a list, element should in "
                        "range [-rank(x), rank(x))."
                    )
                if axis_single < 0:
                    axis_single = axis_single + dims
                axis_src.append(axis_single)
                out_shape[axis_single] = 1
            axis_dst = list(range(-len(axis), 0))
            x = paddle_backend.moveaxis(x, axis_src, axis_dst)
            x = paddle_backend.flatten(x, axis_dst[0], axis_dst[-1])
            axis = axis_dst[0]
        else:
            if not isinstance(axis, int) or not (axis < dims and axis >= -dims):
                raise ValueError(
                    "Axis should be None, int, or a list, element should in "
                    "range [-rank(x), rank(x))."
                )
            if axis < 0:
                axis += dims
            out_shape[axis] = 1

    mask = paddle_backend.isnan(x)
    valid_counts = paddle_backend.sum(
        mask.logical_not(), axis=axis, keepdims=True, dtype="float64"
    )

    indices = []

    for q_num in q:
        if q_num < 0 or q_num > 1:
            raise ValueError("q should be in range [0, 1]")
        if paddle.in_dynamic_mode():
            q_num = paddle.to_tensor(q_num, dtype="float64")
        if ignore_nan:
            indices.append(q_num * (valid_counts - 1))
        else:
            index = q_num * (valid_counts - 1)
            last_index = x.shape[axis] - 1
            nums = paddle.full_like(index, fill_value=last_index)
            index = paddle_backend.where(mask.any(axis=axis, keepdim=True), nums, index)
            indices.append(index)
    sorted_tensor = paddle.sort(x, axis)

    outputs = []

    for index in indices:
        if interpolation not in ["linear", "lower", "higher", "midpoint", "nearest"]:
            raise ValueError(
                "interpolation must be 'linear', 'lower', 'higher', 'midpoint', "
                "or 'nearest'"
            )
        if interpolation == "lower":
            index = paddle.floor(index)
        elif interpolation == "higher":
            index = paddle.ceil(index)
        elif interpolation == "nearest":
            index = paddle.round(index)
        elif interpolation == "midpoint":
            index_floor = paddle.floor(index)
            index_ceil = paddle.ceil(index)
            index = (index_floor + index_ceil) / 2

        indices_below = paddle.floor(index).astype(paddle.int32)
        indices_upper = paddle.ceil(index).astype(paddle.int32)
        tensor_upper = paddle.take_along_axis(sorted_tensor, indices_upper, axis=axis)
        tensor_below = paddle.take_along_axis(sorted_tensor, indices_below, axis=axis)
        weights = index - indices_below.astype("float64")
        out = paddle.lerp(
            tensor_below.astype("float64"),
            tensor_upper.astype("float64"),
            weights,
        )
    if not keepdim:
        out = paddle.squeeze(out, axis=axis)
    else:
        out = out.reshape(out_shape)
    outputs.append(out)

    if len(q) > 1:
        outputs = paddle.stack(outputs, 0)
    else:
        outputs = outputs[0]

    return outputs.astype(ret_dtype)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": (
                "int8",
                "int16",
                "uint8",
                "float16",
                "complex64",
                "complex128",
            )
        }
    },
    backend_version,
)
def quantile(
    a: paddle.Tensor,
    q: Union[paddle.Tensor, float],
    /,
    *,
    axis: Optional[Union[Sequence[int], int]] = None,
    keepdims: Optional[bool] = False,
    interpolation: Optional[str] = "linear",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return _compute_quantile(
        x=a,
        q=q,
        axis=axis,
        keepdim=keepdims,
        interpolation=interpolation,
        ignore_nan=False,
    )


def corrcoef(
    x: paddle.Tensor,
    /,
    *,
    y: Optional[paddle.Tensor] = None,
    rowvar: Optional[bool] = True,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if y is None:
        xarr = x
    else:
        axis = 0 if rowvar else 1
        xarr = paddle.concat([x, y], axis=axis)
        xarr = xarr.T if not rowvar else xarr

        def cov(x, rowvar=True, ddof=True, fweights=None, aweights=None, name=None):
            if len(x.shape) > 2 or len(x.shape) < 1:
                raise ValueError(
                    "Input(x) only support N-D (1<=N<=2) tensor in cov, but received "
                    "length of Input(input) is %s."
                    % len(x.shape)
                )
            nx = x
            if len(x.shape) == 1:
                nx = x.reshape((1, -1))
            if not rowvar and nx.shape[0] != 1:
                nx = nx.t()
            w = None
            observation_num = nx.shape[1]
            if fweights is not None:
                w = fweights.astype(nx.dtype)
                if len(w.shape) > 1:
                    raise ValueError(
                        "Input(fweights) only support N-D (N<=1) tensor in cov, but"
                        " received shape of Input(input) is %s."
                        % len(fweights.shape)
                    )
                if fweights.shape[0] != observation_num:
                    raise ValueError(
                        "The number of Input(fweights) should equal to x's dim[1]: {},"
                        " but received size of Input(fweights) is {}.".format(
                            observation_num, fweights.shape[0]
                        )
                    )
                if fweights.min() < 0:
                    raise ValueError(
                        "The value of Input(fweights) cannot be negtive, but received "
                        "min of Input(fweights) is {}.".format(fweights.min())
                    )
                if not paddle.all(fweights == paddle.round(fweights.astype("float64"))):
                    raise ValueError("Input(fweights) must be integer ")

            if aweights is not None:
                aw = aweights.astype(nx.dtype)
                if len(aw.shape) > 1:
                    raise ValueError(
                        "Input(aweights) only support N-D (N<=1) tensor in cov, but"
                        " received length of Input(input) is %s."
                        % len(aweights.shape)
                    )

                if aweights.shape[0] != observation_num:
                    raise ValueError(
                        "The number of Input(aweights) should equal to x's dim[1]: {},"
                        " but received size of Input(aweights) is {}.".format(
                            observation_num, aweights.shape[0]
                        )
                    )
                if aweights.min() < 0:
                    raise ValueError(
                        "The value of Input(aweights) cannot be negtive, but received "
                        "min of Input(aweights) is {}.".format(aweights.min())
                    )
                if w is not None:
                    w = w * aw
                else:
                    w = aw

            w_sum = paddle.to_tensor(observation_num, dtype=nx.dtype)

            if fweights is not None or aweights is not None:
                w_sum = w.sum()
                if w_sum.item() == 0:
                    raise ValueError("The sum of weights is zero, can't be normalized.")

            if w is not None:
                nx_w = nx * w
                avg = (nx_w).sum(axis=1) / w_sum
            else:
                avg = nx.sum(axis=1) / w_sum
                nx_w = nx

            if w is not None and aweights is not None and ddof:
                norm_factor = w_sum - (w * aweights).sum() / w_sum
            else:
                norm_factor = w_sum - ddof
            if norm_factor <= 0:
                norm_factor = paddle.to_tensor(0.0, dtype=nx.dtype)
            nx = nx - avg.unsqueeze(1)

            if w is None:
                nx_t = nx.T
            else:
                nx_t = (nx * w).T

            xxt = paddle.mm(nx, nx_t.conj())
            cov = paddle.divide(xxt, norm_factor).squeeze()
            return cov

        if len(x.shape) > 2 or len(x.shape) < 1:
            raise ValueError(
                "Input(x) only support N-D (1<=N<=2) tensor in corrcoef, but received "
                "length of Input(input) is %s."
                % len(x.shape)
            )
        x = xarr
        rowvar = True
        c = cov(x, rowvar)
        if c.ndim == 0:
            # scalar covariance
            # nan if incorrect value (nan, inf, 0), 1 otherwise
            return c / c

        d = paddle.diag(c)

        if paddle.is_complex(d):
            d = d.real()
        stddev = paddle.sqrt(d)
        c /= stddev[:, None]
        c /= stddev[None, :]

        # Clip to [-1, 1].  This does not guarantee
        if paddle.is_complex(c):
            return paddle.complex(
                paddle.clip(c.real(), -1, 1), paddle.clip(c.imag(), -1, 1)
            )
        else:
            c = paddle.clip(c, -1, 1)

        return c


def histogram(
    a: paddle.Tensor,
    /,
    *,
    bins: Optional[Union[int, paddle.Tensor]] = None,
    axis: Optional[int] = None,
    extend_lower_interval: Optional[bool] = False,
    extend_upper_interval: Optional[bool] = False,
    dtype: Optional[paddle.Tensor] = None,
    range: Optional[Tuple[float]] = None,
    weights: Optional[paddle.Tensor] = None,
    density: Optional[bool] = False,
    out: Optional[paddle.Tensor] = None,
) -> Tuple[paddle.Tensor]:
    if range is None:
        min_range = 0
        max_range = 0
    else:
        min_range = range[0]
        max_range = range[1]
    return paddle.histogram(a, bins=bins, min=min_range, max=max_range)


def nanmedian(
    input: paddle.Tensor,
    /,
    *,
    axis: Optional[Union[Tuple[int], int]] = None,
    keepdims: Optional[bool] = False,
    dtype: Optional[paddle.dtype] = None,
    overwrite_input: Optional[bool] = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if input.dtype not in [paddle.int32, paddle.int64, paddle.float32, paddle.float64]:
        if dtype is None:
            dtype = input.dtype
        input = input.cast("float32")
        paddle.nanmedian(x=input, axis=axis, keepdim=keepdims).cast(dtype)
    return paddle.nanmedian(x=input, axis=axis, keepdim=keepdims).cast(dtype)


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": (
                "int8",
                "int16",
                "uint8",
                "float16",
                "complex64",
                "complex128",
                "bool",
            )
        }
    },
    backend_version,
)
def unravel_index(
    indices: paddle.Tensor,
    shape: Tuple[int],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if indices.ndim == 0:
        indices = indices.unsqueeze(0)
    coord = []
    indices = indices
    for dim in reversed(shape):
        coord.append((indices % dim).astype("int32"))
        indices = paddle.floor(indices / dim)

    return tuple(reversed(coord))


@with_unsupported_device_and_dtypes(
    {
        "2.4.2 and below": {
            "cpu": (
                "int8",
                "int16",
                "uint8",
                "float16",
                "float32",
                "float64",
                "complex64",
                "complex128",
                "bool",
            )
        }
    },
    backend_version,
)
def bincount(
    x: paddle.Tensor,
    /,
    *,
    weights: Optional[paddle.Tensor] = None,
    minlength: int = 0,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.bincount(x, weights=weights, minlength=minlength).cast(
        x.dtype if weights is None else weights.dtype
    )


def igamma(
    a: paddle.Tensor,
    /,
    *,
    x: paddle.Tensor,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    results = []
    for ai, xi in zip(a.flatten(), x.flatten()):
        ai = ai.astype("float64")
        xi = xi.astype("float64")

        def integrand(t):
            return paddle.exp(-t) * paddle.pow(t, ai - 1)

        intervals = paddle.linspace(0, xi, 10001).astype("float64")
        interval_width = xi / 10000
        values = integrand(intervals)
        integral = paddle.multiply((values[:-1] + values[1:]) / 2, interval_width)
        result = paddle.divide(paddle.sum(integral), paddle.exp(paddle.lgamma(ai)))
        results.append(result)

    return paddle.to_tensor(results, dtype="float32").reshape(a.shape)
