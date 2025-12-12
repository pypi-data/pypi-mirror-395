from __future__ import annotations

from typing import Any

import numpy as np
from numpy import typing as npt


def _as_valid_dtype(arr: npt.NDArray[Any], dtype: np.dtype[Any]) -> npt.NDArray[Any]:
    if np.issubdtype(dtype, str):
        return arr.astype(str)

    return arr
