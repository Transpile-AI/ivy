# global
import torch as torch

backend_version = {"version": torch.__version__.split("+")[0]}

from .activations import *
from .converters import *
from .creation import *
from .data_type import *
from .device import *
from .elementwise import *
from .general import *
from .gradients import *
from .layers import *
from .linear_algebra import *
from .manipulation import *
from .norms import *
from .random import *
from .searching import *
from .set import *
from .sorting import *
from .sparse_array import *
from .statistical import *
from .utility import *
