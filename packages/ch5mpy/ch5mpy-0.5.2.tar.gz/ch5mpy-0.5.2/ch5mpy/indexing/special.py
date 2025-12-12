from __future__ import annotations

from typing import Any, NoReturn, override

import numpy as np
import numpy.typing as npt

from ch5mpy.indexing.base import Indexer


class NewAxisType(Indexer):
    # region magic methods
    def __new__(cls) -> NewAxisType:
        return NewAxis

    @override
    def __repr__(self) -> str:
        return "<NewAxis>"

    @override
    def __len__(self) -> int:
        return 1

    @override
    def __eq__(self, other: Any) -> bool:
        return other is NewAxis

    @override
    def __array__(self, dtype: npt.DTypeLike | None = None, copy: bool | None = True) -> npt.NDArray[Any]:
        raise TypeError

    # endregion

    # region attributes
    @property
    def shape(self) -> tuple[int, ...]:
        return (1,)

    @property
    @override
    def ndim(self) -> int:
        return 1

    @property
    @override
    def is_whole_axis(bool) -> NoReturn:
        raise RuntimeError

    # endregion

    # region methods
    @override
    def as_numpy_index(self) -> None:
        return None

    # endregion


NewAxis = object.__new__(NewAxisType)


class EmptyList(Indexer):
    # region magic methods
    def __init__(self, *, max: int, shape: tuple[int, ...] = (0,)):
        assert np.prod(shape) == 0
        self._shape: tuple[int, ...] = shape
        self._max: int = max

    @override
    def __repr__(self) -> str:
        return f"<EmptyList {self.shape}>"

    @override
    def __len__(self) -> int:
        return 0

    @override
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EmptyList):
            raise NotImplementedError

        return self._shape == other.shape

    def __getitem__(self, item: Indexer) -> EmptyList:
        arr = np.empty(self._shape)[item.as_numpy_index()]
        return EmptyList(shape=arr.shape, max=self._max)

    @override
    def __array__(self, dtype: npt.DTypeLike | None = None, copy: bool | None = True) -> npt.NDArray[Any]:
        return np.empty(self._shape, dtype=dtype)

    # endregion

    # region attributes
    @property
    def shape(self) -> tuple[int, ...]:
        return self._shape

    @property
    @override
    def ndim(self) -> int:
        return len(self._shape)

    @property
    @override
    def is_whole_axis(self) -> bool:
        return self._max == 0

    @property
    def max(self) -> int:
        return self._max

    # endregion

    # region methods
    def as_array(self) -> npt.NDArray[np.int_]:
        return self.__array__(dtype=np.int32)

    @override
    def as_numpy_index(self) -> npt.NDArray[np.int_]:
        return self.__array__(dtype=np.int32)

    # endregion


class PlaceHolderType:
    def __new__(cls) -> PlaceHolderType:
        return PLACEHOLDER

    @override
    def __repr__(self) -> str:
        return "<placeholder>"


PLACEHOLDER = object.__new__(PlaceHolderType)
