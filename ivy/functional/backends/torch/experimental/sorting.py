# global
import torch
from typing import Optional, Union


# msort
def msort(
    a: Union[torch.Tensor, list, tuple], /, *, out: Optional[torch.Tensor] = None
) -> torch.Tensor:
    return torch.msort(a, out=out)


msort_support_native_out = True


# lexsort
def lexsort(
    keys: torch.Tensor,
    /,
    *,
    axis: int = -1,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    size = keys.size(dim=0)
    result = torch.argsort(keys[0], dim=axis, stable=True)
    if size == 1:
        return result
    for i in range(1, size):
        key = keys[i]
        ind = key[result]
        temp = torch.argsort(ind, dim=axis, stable=True)
        result = result[temp]
    return result


lexsort_support_native_out = False
