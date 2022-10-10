# local
import ivy


def empty(
    size,
    *,
    out=None,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    pin_memory=False,
    memory_format=None
):
    ret = ivy.empty(shape=size, dtype=dtype, device=device, out=out)
    if requires_grad:
        return ivy.variable(ret)
    return ret


def full(
    size,
    fill_value,
    *,
    out=None,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=None
):
    ret = ivy.full(
        shape=size, fill_value=fill_value, dtype=dtype, device=device, out=out
    )
    if requires_grad:
        return ivy.variable(ret)
    return ret


def ones(size, *, out=None, dtype=None, device=None, requires_grad=False):
    ret = ivy.ones(shape=size, dtype=dtype, device=device, out=out)
    if requires_grad:
        return ivy.variable(ret)
    return ret


def ones_like_v_0p3p0_to_0p3p1(input, out=None):
    return ivy.ones_like(input, out=None)


def ones_like_v_0p4p0_and_above(
    input,
    *,
    dtype=None,
    layout=None,
    device=None,
    requires_grad=False,
    memory_format=None
):
    ret = ivy.ones_like(input, dtype=dtype, device=device)
    if requires_grad:
        return ivy.variable(ret)
    return ret


def zeros(size, *, out=None, dtype=None, device=None, requires_grad=False):
    ret = ivy.zeros(shape=size, dtype=dtype, device=device, out=out)
    if requires_grad:
        return ivy.variable(ret)
    return ret


def arange(start, end=None, step=1, *, dtype=None, device=None, requires_grad=False):
    ret = ivy.arange(start, end, step, dtype=dtype, device=device)
    if requires_grad:
        return ivy.variable(ret)
    return ret
