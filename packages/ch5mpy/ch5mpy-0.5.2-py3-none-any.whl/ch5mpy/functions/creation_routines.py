from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

import ch5mpy


class ArrayCreationFunc:
    # region magic methods
    def __init__(self, name: str):
        self._name = name

    def __repr__(self) -> str:
        return f"<function ch5mpy.{self._name} at {hex(id(self))}>"

    def __call__(
        self,
        shape: int | tuple[int, ...],
        fill_value: Any,
        loc: str | Path | ch5mpy.File | ch5mpy.Group,
        name: str,
        *,
        dtype: npt.DTypeLike = np.float64,
        chunks: bool | tuple[int, ...] = True,
        maxshape: int | tuple[int | None, ...] | None = None,
    ) -> ch5mpy.H5Array[Any]:
        shape = shape if isinstance(shape, tuple) else (shape,)

        if not isinstance(loc, ch5mpy.Group):
            loc = ch5mpy.File(loc, mode=ch5mpy.H5Mode.READ_WRITE_CREATE)

        dset = ch5mpy.store_dataset(
            None, loc, name, shape=shape, dtype=dtype, chunks=chunks, maxshape=maxshape, fill_value=fill_value
        )

        return ch5mpy.H5Array(dset)

    def defer(
        self,
        shape: int | tuple[int, ...],
        fill_value: Any,
        dtype: npt.DTypeLike = np.float64,
        chunks: bool | tuple[int, ...] = True,
        maxshape: int | tuple[int | None, ...] | None = None,
    ) -> partial[ch5mpy.H5Array[Any]]:
        return partial(self.__call__, shape=shape, fill_value=fill_value, dtype=dtype, chunks=chunks, maxshape=maxshape)

    # endregion


class ArrayCreationFuncWithFill(ArrayCreationFunc):
    # region magic methods
    def __init__(self, name: str, fill_value: Any):
        super().__init__(name)
        self._fill_value = fill_value

    def __call__(  # type: ignore[override]
        self,
        shape: int | tuple[int, ...],
        loc: str | Path | ch5mpy.File | ch5mpy.Group,
        name: str,
        *,
        dtype: npt.DTypeLike = np.float64,
        chunks: bool | tuple[int, ...] = True,
        maxshape: int | tuple[int | None, ...] | None = None,
    ) -> ch5mpy.H5Array[Any]:
        return super().__call__(
            loc=loc, name=name, shape=shape, fill_value=self._fill_value, dtype=dtype, chunks=chunks, maxshape=maxshape
        )

    # endregion

    # region methods
    def defer(  # type: ignore[override]
        self,
        shape: int | tuple[int, ...],
        dtype: npt.DTypeLike = np.float64,
        chunks: bool | tuple[int, ...] = True,
        maxshape: int | tuple[int | None, ...] | None = None,
    ) -> partial[ch5mpy.H5Array[Any]]:
        return partial(self.__call__, shape=shape, dtype=dtype, chunks=chunks, maxshape=maxshape)

    # endregion


full = ArrayCreationFunc("full")
empty = ArrayCreationFuncWithFill("empty", None)
zeros = ArrayCreationFuncWithFill("zeros", 0)
ones = ArrayCreationFuncWithFill("ones", 1)
