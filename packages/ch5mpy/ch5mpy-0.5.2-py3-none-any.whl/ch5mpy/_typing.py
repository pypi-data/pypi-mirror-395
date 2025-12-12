from __future__ import annotations

from types import EllipsisType
from typing import Any, Callable, Iterable, SupportsIndex, Union

from numpy._typing import _ArrayLikeInt_co

ONE_AXIS_SELECTOR = Union[
    int,
    bool,
    SupportsIndex,
]

PARTIAL_SELECTOR = Union[
    None,
    EllipsisType,
    slice,
    range,
    Iterable[int],
    Iterable[bool],
    _ArrayLikeInt_co,
]

SELECTOR = Union[ONE_AXIS_SELECTOR, PARTIAL_SELECTOR]

NP_FUNC = Callable[..., Any]
H5_FUNC = Callable[..., Any]
