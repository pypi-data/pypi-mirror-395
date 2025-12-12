from __future__ import annotations

from typing import Any, Literal, override

import numpy as np
import numpy.typing as npt

from ch5mpy.indexing.base import Indexer


class SingleIndex(Indexer):
    __slots__: tuple[str, ...] = "_index", "_max"

    # region magic methods
    def __init__(self, index: int, max: int):
        if max <= index:
            raise IndexError(f"Selection {index} is out of bounds for axis with size {max}.")

        self._index: int = index
        self._max: int = max

    @override
    def __repr__(self) -> str:
        return f"SingleIndex({self._index} | {self._max})"

    @override
    def __len__(self) -> int:
        return 1

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SingleIndex):
            return False

        return self._index == other._index

    @override
    def __array__(self, dtype: npt.DTypeLike | None = None, copy: bool | None = True) -> npt.NDArray[Any]:
        return np.array(self._index, dtype=None)

    # endregion

    # region attributes
    @property
    @override
    def ndim(self) -> Literal[0]:
        return 0

    @property
    @override
    def is_whole_axis(self) -> bool:
        return self._max == 1

    @property
    def max(self) -> int:
        return self._max

    # endregion

    # region methods
    @override
    def as_numpy_index(self) -> int:
        return self._index

    def as_slice(self) -> slice:
        return slice(self._index, self._index + 1)

    # endregion
