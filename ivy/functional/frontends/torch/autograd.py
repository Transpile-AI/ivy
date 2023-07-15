# local
import ivy
import ivy.functional.frontends.torch as torch_frontend


def _add_grad(g_total, g):
    """Return g_total + g after checking None values."""
    if g is None:
        return g_total
    elif g_total is None:
        return g
    return g_total + g


def _tensors_to_tuple(tensors, outputs=None):
    if tensors is None:
        ret = tuple()
        for out in outputs:
            ret += (torch_frontend.ones_like(out),)
        return ret

    if isinstance(tensors, torch_frontend.Tensor):
        return (tensors,)
    return tuple(tensors)


def _grad_out_multiply(grad_out, jacobian_wrt_input):
    """
    return grad_out * jacobian_wrt_input after manipulating the shapes
    """
    output_shape = grad_out.shape
    input_num_dims = len(jacobian_wrt_input.shape) - len(output_shape)
    expanded_grad_out = grad_out.view(output_shape + (1,) * input_num_dims)
    sum_dims = tuple(range(len(output_shape)))
    new_grad_out = (expanded_grad_out * jacobian_wrt_input).sum(dim=sum_dims)
    return new_grad_out


def get_elemnt(nest, idx):
    ret = nest
    for i in idx:
        ret = ret[i]
    return ret


def _get_grad(output, input, grad_output):
    """Compute gradient of output w.r.t input."""

    # Case #1
    if output is input:
        return grad_output

    # Get inputs of the function that returned output
    func_inputs = output.func_inputs

    # Case #2
    # Reached end of graph. input & output are not connected
    if not func_inputs:
        return None

    # Case #3
    grads = None
    all_indices = ivy.all_nested_indices(func_inputs)
    for idx in all_indices:
        func_input = get_elemnt(func_inputs, idx)
        grad_wrt_input = get_elemnt(output.grads, idx)

        new_grad_out = _grad_out_multiply(grad_output, grad_wrt_input)
        grad = _get_grad(func_input, input, new_grad_out)
        grads = _add_grad(grads, grad)

    return grads


def _batched_get_grad(output, input, grad_output, batched):
    if batched:
        return torch_frontend.stack([_get_grad(output, input, g) for g in grad_output])
    return _get_grad(output, input, grad_output)


def grad(
    outputs,
    inputs,
    grad_outputs=None,
    retain_graph=None,
    create_graph=False,
    only_inputs=True,
    allow_unused=False,
    is_grads_batched=False,
):
    """Compute and return the sum of gradients of outputs with respect to each input."""
    inputs = _tensors_to_tuple(inputs)
    outputs = _tensors_to_tuple(outputs)
    grad_outputs = _tensors_to_tuple(grad_outputs, outputs)

    ret = []
    for input in inputs:
        if not input.requires_grad:
            raise RuntimeError("One of the input tensors does not require grad")

        grad_wrt_input = None
        for output, grad_output in zip(outputs, grad_outputs):
            if not output.requires_grad:
                raise RuntimeError("One of the output tensors does not require grad")

            g = _batched_get_grad(output, input, grad_output, is_grads_batched)
            grad_wrt_input = _add_grad(grad_wrt_input, g)

        if not allow_unused and grad_wrt_input is None:
            raise RuntimeError(
                "One of the differentiated Tensors appears to not have"
                " been used in the graph. Set allow_unused=True if this"
                " is the desired behavior."
            )
        ret += [grad_wrt_input]
    return tuple(ret)
