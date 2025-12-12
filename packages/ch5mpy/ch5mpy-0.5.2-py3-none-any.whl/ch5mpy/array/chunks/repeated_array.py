from __future__ import annotations

from itertools import zip_longest
from typing import TYPE_CHECKING, Any, Generator

import numpy as np
from numpy import typing as npt

from ch5mpy.array.chunks.utils import _as_valid_dtype

if TYPE_CHECKING:
    from ch5mpy import H5Array


def _as_range(s: slice) -> range:
    return range(s.start or 0, s.stop, s.step or 1)


def broadcastable(*shapes: tuple[int, ...]) -> bool:
    try:
        np.broadcast_shapes(*shapes)

    except ValueError:
        return False

    return True


def parse_index(
    item: tuple[slice, ...],
    base_shape: tuple[int, ...],
    repeated_shape: tuple[int, ...],
) -> Generator[list[int], None, None]:
    for index_i, base_shape_i, repeated_shape_i in zip_longest(item, base_shape, repeated_shape, fillvalue=None):
        if repeated_shape_i is None:
            raise RuntimeError

        if index_i is None:
            yield [0 for _ in range(repeated_shape_i)]

        elif base_shape_i == 1:
            yield [0 for _ in range(index_i.stop - index_i.start)]

        else:
            yield [i for i in _as_range(index_i)]


class RepeatedArray:
    # region magic methods
    def __init__(self, array: H5Array[Any] | npt.NDArray[Any], shape: tuple[int, ...]):
        if not broadcastable(array.shape, shape):
            raise ValueError(f"Cannot broadcast array with shape {array.shape} to {shape}.")

        if len(shape) < array.ndim:
            raise ValueError(f"Cannot reduce dimensions of {array.ndim}D array to {len(shape)}D.")

        self._array = array[(None,) * (len(shape) - array.ndim)]
        self._shape = shape

    def __repr__(self) -> str:
        return f"RepeatedArray({self._shape})"

    def __getitem__(self, item: slice | tuple[slice, ...]) -> H5Array[Any] | npt.NDArray[Any]:
        if isinstance(item, slice):
            item = (item,)

        return self._array[np.ix_(*parse_index(item, self._array.shape, self._shape))]

    # endregion

    # region attributes
    @property
    def shape(self) -> tuple[int, ...]:
        return self._shape

    @property
    def ndim(self) -> int:
        return len(self._shape)

    @property
    def dtype(self) -> np.dtype[Any]:
        return self._array.dtype

    @property
    def chunks(self) -> tuple[int, ...] | None:
        if type(self._array) == H5Array:  # noqa: E721
            return self._array.dset.chunks

        return None

    # endregion

    # region methods
    def read(
        self,
        out: npt.NDArray[Any],
        source_sel: tuple[int | slice, ...],
        dest_sel: tuple[int | slice, ...],
    ) -> npt.NDArray[Any]:
        # if isinstance(self._array, ch5mpy.H5Array):
        #     self._array.read_direct(out, source_sel=source_sel, dest_sel=dest_sel)

        # else:
        out[dest_sel] = self._array[source_sel]

        return _as_valid_dtype(out, self._array.dtype)[dest_sel]

    # endregion
