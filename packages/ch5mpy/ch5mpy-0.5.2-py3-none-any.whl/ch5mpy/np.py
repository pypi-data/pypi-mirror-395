from __future__ import annotations

from numbers import Number
from typing import Any

import numpy as np
import numpy.typing as npt


def arange_nd(
    shape: tuple[int, ...],
    start: Number | None = None,
    step: Number | None = None,
    dtype: npt.DTypeLike | None = None,
) -> npt.NDArray[Any]:
    start_ = 0 if start is None else start
    stop = np.prod(shape) + start_  # type: ignore[call-overload]

    return np.arange(start=start_, stop=stop, step=step, dtype=dtype).reshape(shape)
