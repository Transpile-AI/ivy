"""
Collection of runtime tests for unified gradients functions
"""

DIM = int(1e4)


# global
import os
import random

# local
import ivy.core.general as ivy_gen
import ivy.core.gradients as ivy_grad
this_file_dir = os.path.dirname(os.path.realpath(__file__))
import with_time_logs.ivy.core.gradients as ivy_grad_w_time

from ivy.backends import jax as _ivy_jnp, torch as _ivy_torch, mxnet as _ivy_mxnet, numpy as _ivy_np, \
    tensorflow as _ivy_tf

from with_time_logs.ivy import torch as _ivy_torch_w_time
from with_time_logs.ivy import tensorflow as _ivy_tf_w_time
from with_time_logs.ivy import mxnet as _ivy_mxnet_w_time
from with_time_logs.ivy import jax as _ivy_jnp_w_time
from with_time_logs.ivy import numpy as _ivy_np_w_time

LIB_DICT = {_ivy_torch: _ivy_torch_w_time,
            _ivy_tf: _ivy_tf_w_time,
            _ivy_mxnet: _ivy_mxnet_w_time,
            _ivy_jnp: _ivy_jnp_w_time,
            _ivy_np: _ivy_np_w_time}

# local
import ivy_tests.helpers as helpers
from test_runtime.utils import append_to_file, log_time, write_times, TIMES_DICT


def test_variable():

    fname = os.path.join(this_file_dir, 'runtime_analysis/{}/gradients/variable.txt'.format(DIM))
    if os.path.exists(fname):
        os.remove(fname)
    for lib, call in [(l, c) for l, c in helpers.calls if c not in [helpers.tf_graph_call, helpers.mx_graph_call]]:

        time_lib = LIB_DICT[lib]

        append_to_file(fname, '{}'.format(lib))

        x0 = ivy_gen.tensor([random.uniform(0, 1) for _ in range(DIM)], f=lib)

        ivy_grad.variable(x0, f=lib)
        ivy_grad_w_time.variable(x0, f=time_lib)
        TIMES_DICT.clear()

        for _ in range(100):

            log_time(fname, 'tb0')
            ivy_grad_w_time.variable(x0, f=time_lib)
            log_time(fname, 'tb4', time_at_start=True)

            log_time(fname, 'tt0')
            ivy_grad.variable(x0, f=lib)
            log_time(fname, 'tt1', time_at_start=True)

        write_times()

    append_to_file(fname, 'end of analysis')


def test_execute_with_gradients():

    fname = os.path.join(this_file_dir, 'runtime_analysis/{}/gradients/execute_with_gradients.txt'.format(DIM))
    if os.path.exists(fname):
        os.remove(fname)
    for lib, call in [(l, c) for l, c in helpers.calls if c not in [helpers.tf_graph_call, helpers.mx_graph_call]]:

        time_lib = LIB_DICT[lib]

        append_to_file(fname, '{}'.format(lib))

        x0 = ivy_gen.tensor([random.uniform(0, 1) for _ in range(DIM)], f=lib)
        func = lambda xs_in: (xs_in[0] * xs_in[0])[0]
        xs = [ivy_grad.variable(x0)]

        ivy_grad.execute_with_gradients(func, xs, f=lib)
        ivy_grad_w_time.execute_with_gradients(func, xs, f=time_lib)
        TIMES_DICT.clear()

        for _ in range(100):

            log_time(fname, 'tb0')
            ivy_grad_w_time.execute_with_gradients(func, xs, f=time_lib)
            log_time(fname, 'tb4', time_at_start=True)

            log_time(fname, 'tt0')
            ivy_grad.execute_with_gradients(func, xs, f=lib)
            log_time(fname, 'tt1', time_at_start=True)

        write_times()

    append_to_file(fname, 'end of analysis')


def test_gradient_descent_update():

    fname = os.path.join(this_file_dir, 'runtime_analysis/{}/gradients/gradient_descent_update.txt'.format(DIM))
    if os.path.exists(fname):
        os.remove(fname)
    for lib, call in [(l, c) for l, c in helpers.calls if c not in [helpers.tf_graph_call, helpers.mx_graph_call]]:

        time_lib = LIB_DICT[lib]

        append_to_file(fname, '{}'.format(lib))

        x0 = ivy_gen.tensor([random.uniform(0, 1) for _ in range(DIM)], f=lib)
        x1 = ivy_gen.tensor([random.uniform(0, 1) for _ in range(DIM)], f=lib)
        ws = [ivy_grad.variable(x0)]
        dcdws = [x1]

        ivy_grad.gradient_descent_update(ws, dcdws, 0.1, f=lib)
        ivy_grad_w_time.gradient_descent_update(ws, dcdws, 0.1, f=time_lib)
        TIMES_DICT.clear()

        for _ in range(100):

            log_time(fname, 'tb0')
            ivy_grad_w_time.gradient_descent_update(ws, dcdws, 0.1, f=time_lib)
            log_time(fname, 'tb4', time_at_start=True)

            log_time(fname, 'tt0')
            ivy_grad.gradient_descent_update(ws, dcdws, 0.1, f=lib)
            log_time(fname, 'tt1', time_at_start=True)

        write_times()

    append_to_file(fname, 'end of analysis')


def test_stop_gradient():

    fname = os.path.join(this_file_dir, 'runtime_analysis/{}/gradients/stop_gradient.txt'.format(DIM))
    if os.path.exists(fname):
        os.remove(fname)
    for lib, call in [(l, c) for l, c in helpers.calls if c not in [helpers.tf_graph_call, helpers.mx_graph_call]]:

        time_lib = LIB_DICT[lib]

        append_to_file(fname, '{}'.format(lib))

        x0 = ivy_gen.tensor([random.uniform(0, 1) for _ in range(DIM)], f=lib)

        ivy_grad.stop_gradient(x0, f=lib)
        ivy_grad_w_time.stop_gradient(x0, f=time_lib)
        TIMES_DICT.clear()

        for _ in range(100):

            log_time(fname, 'tb0')
            ivy_grad_w_time.stop_gradient(x0, f=time_lib)
            log_time(fname, 'tb4', time_at_start=True)

            log_time(fname, 'tt0')
            ivy_grad.stop_gradient(x0, f=lib)
            log_time(fname, 'tt1', time_at_start=True)

        write_times()

    append_to_file(fname, 'end of analysis')
