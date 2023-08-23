# local
import ivy
from ivy.func_wrapper import with_supported_dtypes
from ivy.functional.frontends.paddle.func_wrapper import to_ivy_arrays_and_back
from ivy.functional.frontends.torch.nn.functional.pooling_functions import (
    _broadcast_pooling_helper,
)
from ivy.func_wrapper import with_unsupported_dtypes


@to_ivy_arrays_and_back
@with_supported_dtypes({"2.5.0 and below": ("float32", "float64")}, "paddle")
def avg_pool2d(
    x,
    kernel_size,
    stride=None,
    padding=0,
    ceil_mode=False,
    exclusive=True,
    divisor_override=None,
    data_format="NCHW",
    name=None,
):
    kernel_size = _broadcast_pooling_helper(kernel_size, "2d", name="kernel_size")
    stride = _broadcast_pooling_helper(stride, "2d", name="stride")
    padding = _broadcast_pooling_helper(padding, "2d", name="padding")
    kernel_pads = list(zip(kernel_size, padding))

    # Padding should be less than or equal to half of kernel size
    if not all([pad <= kernel / 2 for kernel, pad in kernel_pads]):
        raise ValueError(
            "pad should be smaller than or equal to half of kernel size, "
            f"but got padding={padding}, kernel_size={kernel_size}. "
        )

    # Figure out padding string
    if all([pad == ivy.ceil((kernel - 1) / 2) for kernel, pad in kernel_pads]):
        padding = "SAME"
    else:
        padding = "VALID"

    count_include_pad = False if exclusive else True
    return ivy.avg_pool2d(
        x,
        kernel_size,
        stride,
        padding,
        data_format=data_format,
        count_include_pad=count_include_pad,
        ceil_mode=ceil_mode,
        divisor_override=divisor_override,
    )


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.5.0 and below": ("float16", "bfloat16")}, "paddle")
def avg_pool1d(
    x, kernel_size, stride=None, padding=0, exclusive=True, ceil_mode=False, name=None
):
    data_format = "NCL"
    exclusive = not exclusive

    return ivy.avg_pool1d(
        x,
        kernel_size,
        stride,
        padding,
        count_include_pad=exclusive,
        ceil_mode=ceil_mode,
        data_format=data_format,
    )



@to_ivy_arrays_and_back
@with_supported_dtypes({"2.5.0 and below": ("float32", "float64")}, "paddle")
def max_pool2d(
    x,
    kernel_size,
    stride=None,
    padding=0,
    ceil_mode=False,
    data_format="NCHW",
    name=None,
):
    kernel_size = _broadcast_pooling_helper(kernel_size, "2d", name="kernel_size")
    stride = _broadcast_pooling_helper(stride, "2d", name="stride")
    padding = _broadcast_pooling_helper(padding, "2d", name="padding")

    # Padding should be less than or equal to half of kernel size
    kernel_pads = list(zip(kernel_size, padding))
    if not all([pad <= kernel / 2 for kernel, pad in kernel_pads]):
        raise ValueError(
            "pad should be smaller than or equal to half of kernel size, "
            f"but got padding={padding}, kernel_size={kernel_size}. "
        )

    # Figure out padding string
    if all([pad == ivy.ceil((kernel - 1) / 2) for kernel, pad in kernel_pads]):
        padding = "SAME"
    else:
        padding = "VALID"

    return ivy.max_pool2d(
        x,
        kernel_size,
        stride,
        padding,
        data_format=data_format,
        ceil_mode=ceil_mode,
    )


@to_ivy_arrays_and_back
@with_unsupported_dtypes({"2.5.0 and below": ("float16", "bfloat16")}, "paddle")
def max_pool1d(
    x, kernel_size, stride=None, padding=0, ceil_mode=False, name=None
):
    data_format = "NCL"

    return ivy.max_pool1d(
        x,
        kernel_size,
        stride,
        padding,
        data_format=data_format,
        ceil_mode=ceil_mode,
    )


from pooling import avg_pool2d, max_pool2d, avg_pool1d, max_pool1d

# Create an example input tensor
input_tensor = ivy.array([[
    [[1.0, 2.0, 3.0, 4.0],
     [5.0, 6.0, 7.0, 8.0],
     [9.0, 10.0, 11.0, 12.0],
     [13.0, 14.0, 15.0, 16.0]]
]])

# Perform average pooling on the input tensor
avg_pool_output = avg_pool2d(input_tensor, kernel_size=(2, 2), stride=(2, 2))

# Perform max pooling on the input tensor
max_pool_output = max_pool2d(input_tensor, kernel_size=(2, 2), stride=(2, 2))

print("Input Tensor:")
print(input_tensor)

print("\nAverage Pooling Output:")
print(avg_pool_output)

print("\nMax Pooling Output:")
print(max_pool_output)

#lets se how this works