from __future__ import annotations

from typing import Any, Generator, TypeVar, cast

import numpy as np
from numpy import typing as npt

from ch5mpy.indexing.selection import Selection
from ch5mpy.objects import Dataset, DatasetWrapper
from ch5mpy.utils import NAN_PACKED

_DT = TypeVar("_DT", bound=np.generic)


class IterWithFinalReordering:
    def __init__(self, gen: Generator[Any, Any, Any]):
        self.gen = gen
        self.final_reordering: tuple[npt.NDArray[np.int_] | slice, ...] | None = None

    def __iter__(self) -> Generator[Any, Any, Any]:
        self.final_reordering = yield from self.gen


def read_from_dataset(
    dataset: Dataset[_DT] | DatasetWrapper[_DT],
    selection: Selection,
    loading_array: npt.NDArray[_DT],
) -> None:
    if not dataset.size:
        if loading_array.size:
            raise ValueError("Reading from empty dataset.")
        return

    if not loading_array.size:
        return

    indexers = IterWithFinalReordering(selection.iter_indexers())
    for dataset_idx, dataset_expand_idx, loading_array_idx in indexers:
        # TODO : would be nice to be able to pass an array with random order in `dest_sel`
        dataset.read_direct(
            loading_array, source_sel=dataset_idx, dest_sel=loading_array_idx, expand_sel=dataset_expand_idx
        )

    if indexers.final_reordering is not None:
        loading_array[:] = loading_array[indexers.final_reordering]

    if loading_array.ndim == 0:
        if loading_array == NAN_PACKED:
            loading_array[()] = np.nan

    else:
        pass
        # is_nan = np.where(loading_array == NAN_PACKED)
        # if is_nan[0].size:
        #     loading_array[is_nan] = np.nan


def read_one_from_dataset(
    dataset: Dataset[_DT] | DatasetWrapper[_DT],
    selection: Selection,
    dtype: np.dtype[_DT],
) -> _DT:
    loading_array = np.empty((), dtype=dtype)
    read_from_dataset(dataset, selection, loading_array)
    return cast(_DT, loading_array[()])


def write_to_dataset(
    dataset: Dataset[_DT] | DatasetWrapper[_DT],
    values: npt.NDArray[_DT],
    selection: Selection,
) -> None:
    selection_shape = selection.out_shape

    if values.size == np.prod(selection_shape) and values.shape != selection_shape:
        values = values.reshape(selection_shape)

    for dataset_idx, _, array_idx in selection.iter_indexers(can_reorder=False):
        dataset.write_direct(values, source_sel=array_idx, dest_sel=dataset_idx)
