from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import numpy as np
import numpy.typing as npt
from numpy._typing import _ArrayLikeInt_co

from ch5mpy.array.functions.implement import implements

if TYPE_CHECKING:
    from ch5mpy import H5Array


@implements(np.searchsorted)
def searchsorted(
    a: H5Array[Any], v: npt.ArrayLike, side: Literal["left", "right"] = "left", sorter: _ArrayLikeInt_co | None = None
) -> int | npt.NDArray[np.int64]:
    if not a.ndim == 1:
        raise ValueError("Array should be 1 dimensional")

    # TODO: find better implementation to avoid whole array copy
    return np.searchsorted(a.copy(), v, side, sorter)
