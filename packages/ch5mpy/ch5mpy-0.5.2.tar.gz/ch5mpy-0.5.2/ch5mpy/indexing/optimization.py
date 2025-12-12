from itertools import chain
from typing import cast

import numpy as np

from ch5mpy.indexing.base import Indexer
from ch5mpy.indexing.list import ListIndex
from ch5mpy.indexing.single import SingleIndex
from ch5mpy.indexing.slice import FullSlice
from ch5mpy.indexing.special import EmptyList, NewAxis
from ch5mpy.indexing.utils import takewhile_inclusive


class Vector:
    # region magic methods
    def __init__(self, index: ListIndex):
        self._index = index
        self._max = index.max

    def __repr__(self) -> str:
        return f"Vector({self._index})"

    # endregion

    # region methods
    def try_as_slice(self) -> FullSlice | None:
        array = self._index.as_array(flattened=True)
        array[array < 0] += self._index.max

        if not len(array):
            return None

        if len(array) == 1:
            return FullSlice.one(array[0], max=self._index.max)

        steps = np.ediff1d(array)

        # check all steps are equal and > 0
        if steps[0] <= 0 or np.any(steps != steps[0]):
            return None

        return FullSlice(array[0], array[-1] + steps[0], steps[0], max=self._index.max)

    def drop_axes(self, n: int) -> ListIndex:
        n = min(self._index.ndim - 1, n)

        return cast(ListIndex, self._index[(SingleIndex(0, max=self._max),) * n])

    # endregion


class VectorEnsembl:
    # region magic methods
    def __init__(self, vectors: tuple[Vector, ...]):
        self._vectors = vectors

    # endregion

    # region methods
    def convert(self) -> tuple[FullSlice | ListIndex, ...]:
        converted_vectors: tuple[FullSlice | ListIndex, ...] = ()
        can_convert = True
        drop_n_axes = 0

        for vector in self._vectors:
            if can_convert:
                converted = vector.try_as_slice()
                if converted is None:
                    can_convert = False
                    converted_vectors += (vector.drop_axes(drop_n_axes),)

                else:
                    drop_n_axes += 1
                    converted_vectors += (converted,)

            else:
                converted_vectors += (vector.drop_axes(drop_n_axes),)

        return converted_vectors

    # endregion


def get_valid_indices(indices: tuple[Indexer, ...], optimize: bool) -> tuple[Indexer, ...]:
    if not len(indices):
        return ()

    if any(isinstance(i, EmptyList) for i in indices):
        # make sure shapes are broadcastable
        np.broadcast_shapes(*(lst.shape for lst in indices if isinstance(lst, (ListIndex, EmptyList)) and lst.ndim > 0))

    if not optimize:
        return indices

    if _gets_whole_dataset(indices):
        return ()

    if any(isinstance(i, ListIndex) for i in indices) and all(isinstance(i, (FullSlice, ListIndex)) for i in indices):
        indices = _optimize_indices(indices)

    if _gets_whole_dataset(indices):
        return ()

    return _drop_whole_axes(indices)


def _gets_whole_dataset(indices: tuple[Indexer, ...]) -> bool:
    return all(isinstance(i, (FullSlice, ListIndex)) and i.is_whole_axis for i in indices)


def _drop_whole_axes(indices: tuple[Indexer, ...]) -> tuple[Indexer, ...]:
    drop = 0
    rev_indices = list(indices[::-1])

    for idx, i in enumerate(rev_indices):
        if isinstance(i, FullSlice) and i.is_whole_axis:
            drop += 1

        elif isinstance(i, ListIndex) and i.squeeze().is_whole_axis:
            if len(rev_indices) == (idx + 1):
                drop += 1
                continue

            next_index = rev_indices[idx + 1]

            if not isinstance(next_index, ListIndex) or next_index.ndim == 1:
                drop += 1

            elif next_index.ndim == 2 and next_index.shape[1] == 1:
                rev_indices[idx + 1] = next_index.flatten()
                drop += 1

            else:
                break

        else:
            break

    return tuple(rev_indices[drop:][::-1])


def _convert_lists_to_slices(indices: tuple[ListIndex, ...]) -> tuple[Indexer, ...]:
    """
    From indexing arrays, return (if possible) the tuple of slices that would lead to the same indexing since indexing
    from slices leads to much fewer read operations.
    Also, return the number of NewAxes to add before and after the tuple of slices so as to maintain the resulting
    array's dimensions.

    This is effectively the inverse of the numpy.ix_ function, with indexing arrays converted to slices.
    """
    if len(indices) == 1 and len(indices[0]) == 1:
        return indices

    ndim = max(i.ndim for i in indices)

    if len(indices) > ndim:
        raise ValueError

    shapes = np.array([i.expand_to_dim(ndim).shape for i in indices])

    start = ndim - len(indices)
    end = start + len(indices)
    extra_before, square, extra_after = np.split(shapes, [start, end], axis=1)

    square[np.diag_indices(len(indices))] = 1

    if np.any(extra_before != 1) or np.any(square != 1) or np.any(extra_after != 1):
        raise ValueError

    slices = VectorEnsembl(tuple(Vector(i) for i in indices)).convert()

    return (NewAxis,) * extra_before.shape[1] + slices + (NewAxis,) * extra_after.shape[1]


def _optimize_indices(indices: tuple[Indexer, ...]) -> tuple[Indexer, ...]:
    list_indices, lists = zip(*((idx, i) for idx, i in enumerate(indices) if isinstance(i, ListIndex)))

    try:
        lists = _convert_lists_to_slices(lists)
    except ValueError:
        pass

    it_optimized_lists = iter(lists)

    return tuple(
        chain.from_iterable(
            (i,) if idx not in list_indices else takewhile_inclusive(lambda e: e is NewAxis, it_optimized_lists)
            for idx, i in enumerate(indices)
        )
    )
