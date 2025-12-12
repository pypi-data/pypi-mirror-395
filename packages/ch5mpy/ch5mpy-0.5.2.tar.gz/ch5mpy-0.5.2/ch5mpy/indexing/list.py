from __future__ import annotations

from typing import Any, override

import numpy as np
import numpy.typing as npt
from numpy._globals import _CopyMode

from ch5mpy.indexing.base import Indexer, as_indexer


class ListIndex(Indexer):
    # region magic methods
    def __init__(self, elements: npt.NDArray[np.int_], max: int):
        if not np.issubdtype(elements.dtype, np.integer):
            raise ValueError("Indexing elements should be integers.")
        if elements.ndim == 0:
            raise ValueError("Cannot build empty ListIndex, use EmptyList instead.")

        self._elements: npt.NDArray[np.int_] = np.array(elements)
        self._max: int = max

        self._elements[self._elements < 0] += max

        if len(self._elements) and (self._elements.min() < 0 or self._elements.max() >= max):
            raise IndexError(f"Selection {self._elements} is out of bounds for axis with size {max}.")

    @override
    def __repr__(self) -> str:
        flat_elements_repr = str(self._elements).replace("\n", "")
        return f"ListIndex({flat_elements_repr}, ndim={self.ndim} | {self._max})"

    def __getitem__(self, item: Indexer | tuple[Indexer, ...]) -> Indexer:
        if not isinstance(item, tuple):
            item = (item,)

        return as_indexer(self._elements[tuple(i.as_numpy_index() for i in item)], max=self._max)

    @override
    def __len__(self) -> int:
        return len(self._elements)

    @override
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ListIndex):
            return False

        return np.array_equal(self._elements, other._elements)

    @override
    def __array__(self, dtype: npt.DTypeLike | None = None, copy: bool | _CopyMode = True) -> npt.NDArray[Any]:
        if dtype is None:
            return self._elements

        return self._elements.astype(dtype, copy=copy)

    # endregion

    # region attributes
    @property
    @override
    def ndim(self) -> int:
        return self._elements.ndim

    @property
    def max(self) -> int:
        return self._max

    @property
    def shape(self) -> tuple[int, ...]:
        return self._elements.shape

    @property
    def size(self) -> int:
        return self._elements.size

    @property
    @override
    def is_whole_axis(self) -> bool:
        return np.array_equal(self._elements, np.arange(self._max))

    # endregion

    # region methods
    def as_array(self, sorted: bool = False, flattened: bool = False) -> npt.NDArray[np.int_]:
        elements = self._elements

        if flattened:
            elements = elements.flatten()

        if sorted:
            elements = np.sort(elements)

        return elements

    @override
    def as_numpy_index(self) -> npt.NDArray[np.int_]:
        return self.__array__()

    def squeeze(self) -> ListIndex:
        if self.size <= 1:
            return self

        return ListIndex(np.squeeze(self._elements), self._max)

    def expand_to_dim(self, n: int) -> ListIndex:
        if n < self.ndim:
            raise RuntimeError

        expanded_shape = (1,) * (n - self.ndim) + self.shape
        return ListIndex(self._elements.reshape(expanded_shape), self._max)

    def broadcast_to(self, shape: tuple[int, ...]) -> ListIndex:
        return ListIndex(np.broadcast_to(self._elements, shape), self._max)

    def reshape(self, shape: tuple[int, ...]) -> ListIndex:
        return ListIndex(self._elements.reshape(shape), self._max)

    def flatten(self) -> ListIndex:
        return ListIndex(self._elements.flatten(), self._max)

    # endregion
