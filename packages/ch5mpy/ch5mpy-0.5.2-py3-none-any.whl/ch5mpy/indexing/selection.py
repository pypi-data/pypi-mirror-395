from __future__ import annotations

from dataclasses import dataclass
from itertools import chain, dropwhile, repeat, takewhile
from typing import Any, Generator, Iterable, Iterator, overload

import numpy as np
import numpy.typing as npt

from ch5mpy._typing import SELECTOR
from ch5mpy.indexing.base import Indexer, as_indexer, boolean_array_as_indexer
from ch5mpy.indexing.list import ListIndex
from ch5mpy.indexing.optimization import get_valid_indices
from ch5mpy.indexing.single import SingleIndex
from ch5mpy.indexing.slice import FullSlice
from ch5mpy.indexing.special import PLACEHOLDER, EmptyList, NewAxis, NewAxisType, PlaceHolderType
from ch5mpy.indexing.utils import takewhile_inclusive


@dataclass
class IndexedValue:
    value: Indexer
    idx: int


def get_indexer(
    obj: Indexer, sorted: bool = False, enforce_1d: bool = False, for_h5: bool = False
) -> int | npt.NDArray[np.int_] | slice | None:
    if isinstance(obj, NewAxisType):
        return None

    if isinstance(obj, (SingleIndex, FullSlice, EmptyList)):
        return obj.as_numpy_index()

    if isinstance(obj, ListIndex):
        if obj.size != 1:
            return obj.as_array(sorted=sorted, flattened=enforce_1d)

        if enforce_1d:
            return obj.squeeze().as_array().reshape((1,))

        if for_h5:
            return int(obj.squeeze().as_array()[()])

        return obj.squeeze().as_array()

    raise TypeError(f"Can't get indexer for {obj} with type '{type(obj)}'.")


def _compute_shape_empty_dset(
    indices: tuple[Indexer, ...], arr_shape: tuple[int, ...], new_axes: bool
) -> tuple[int, ...]:
    if new_axes and any(
        dropwhile(lambda x: x, reversed(list(dropwhile(lambda x: x, [x is NewAxis for x in indices]))))
    ):
        raise NotImplementedError("Cannot have new axis besides first and last indices yet.")

    shape: tuple[int, ...] = ()

    for index in indices:
        if index is NewAxis:
            if not new_axes:
                continue

            shape += (1,)
            continue

        if index.ndim > 0:
            shape += (len(index),)

    return shape + arr_shape[len(indices) :]


def _get_sorting_indices(i: Any) -> npt.NDArray[np.int_] | slice:
    if isinstance(i, np.ndarray):
        return np.unique(i.flatten(), return_inverse=True)[1]  # type: ignore[no-any-return]
    return slice(None)


def _as_indexers(indices: tuple[SELECTOR, ...], shape: tuple[int, ...]) -> Generator[Indexer, None, None]:
    if len([i for i in indices if i is not None]) > len(shape):
        raise IndexError(
            f"too many indices for H5Array, array is {len(shape)}-dimensional, but {len(indices)} were indexed"
        )

    shape_it = iter(shape)

    for index in indices:
        if index is None:
            yield NewAxis
            continue

        elif isinstance(index, (np.ndarray, list)):
            index = np.array(index)

            if index.dtype == np.bool_:
                for indexer in boolean_array_as_indexer(
                    index,  # type: ignore[arg-type]
                    tuple(next(shape_it) for _ in range(index.ndim)),
                ):
                    yield indexer

                continue

        yield as_indexer(index, next(shape_it))  # type: ignore[arg-type]


class Selection:
    __slots__ = "_indices", "_array_shape"

    # region magic methods
    def __init__(self, indices: Iterable[Indexer] | None, shape: tuple[int, ...], optimize: bool = True):
        if indices is None:
            self._indices: tuple[Indexer, ...] = ()
            return

        indices = tuple(indices)

        if len([i for i in indices if i is not NewAxis]) > len(shape):
            raise IndexError(f"Got too many indices ({len(indices)}) for shape {shape}.")

        it_indices = iter(indices)
        *_indices, first_list = takewhile_inclusive(lambda i: not isinstance(i, ListIndex), it_indices)

        largest_dim = 0 if first_list is None else max(i.ndim for i in indices if isinstance(i, ListIndex))
        self._indices = get_valid_indices(
            tuple(chain(_indices, () if first_list is None else (first_list.expand_to_dim(largest_dim),), it_indices)),
            optimize=optimize,
        )

        self._array_shape = shape

    def __repr__(self) -> str:
        return f"Selection{self._indices}\n         {self.in_shape} --> {self.out_shape}"

    @overload
    def __getitem__(self, item: int) -> Indexer: ...

    @overload
    def __getitem__(self, item: slice | Iterable[int]) -> Selection: ...

    def __getitem__(self, item: int | slice | Iterable[int]) -> Indexer | Selection:
        if isinstance(item, int):
            if item >= len(self._indices):
                if item >= len(self.out_shape):
                    raise IndexError(f"Index {item} is out of range for {self.out_shape} selection.")

                return FullSlice.whole_axis(self.out_shape[item])

            return self._indices[item]

        elif isinstance(item, slice):
            return Selection(self._indices[item], shape=self._array_shape)

        return Selection([e for i, e in enumerate(self._indices) if i in item], shape=self._array_shape)

    def __matmul__(self, item: slice | Iterable[int]) -> Selection:
        """Same as __getitem__ but without optimization"""
        if isinstance(item, slice):
            return Selection(self._indices[item], shape=self._array_shape, optimize=False)

        return Selection([e for i, e in enumerate(self._indices) if i in item], shape=self._array_shape, optimize=False)

    def __iter__(self) -> Iterator[Indexer]:
        return iter(self._indices)

    def __len__(self) -> int:
        return len(self._indices)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Selection):
            return False

        return (self._array_shape, self._indices) == (other._array_shape, other._indices)

    # endregion

    # region attributes
    @property
    def is_empty(self) -> bool:
        return len(self._indices) == 0

    @property
    def contains_empty_list(self) -> bool:
        return any(isinstance(e, EmptyList) for e in self._indices)

    @property
    def is_newaxis(self) -> npt.NDArray[np.bool_]:
        return np.array([x is NewAxis for x in self._indices], dtype=bool)

    @property
    def is_single(self) -> npt.NDArray[np.bool_]:
        return np.array([isinstance(x, SingleIndex) for x in self._indices], dtype=bool)

    @property
    def is_list(self) -> npt.NDArray[np.bool_]:
        return np.array([isinstance(x, (ListIndex, EmptyList)) for x in self._indices], dtype=bool)

    @property
    def is_slice(self) -> npt.NDArray[np.bool_]:
        return np.array([isinstance(x, FullSlice) for x in self._indices], dtype=bool)

    @property
    def in_shape(self) -> tuple[int, ...]:
        return self._array_shape

    @property
    def out_shape(self) -> tuple[int, ...]:
        if np.prod(self._array_shape) == 0:
            return _compute_shape_empty_dset(self._indices, self._array_shape, new_axes=True)

        len_end_shape = len(self._indices) - sum(self.is_newaxis)
        return self._min_shape(new_axes=True) + self._array_shape[len_end_shape:]

    @property
    def out_shape_squeezed(self) -> tuple[int, ...]:
        if np.prod(self.in_shape) == 0:
            shape = _compute_shape_empty_dset(self._indices, self._array_shape, new_axes=False)

        else:
            len_end_shape = len(self._indices) - sum(self.is_newaxis)
            shape = self._min_shape(new_axes=False) + self._array_shape[len_end_shape:]

        return tuple(
            s for s, is_list in zip(shape, chain(self.is_list | self.is_single, repeat(False))) if s != 1 or not is_list
        )

    # endregion

    # region methods
    @classmethod
    def from_selector(cls, indices: SELECTOR | tuple[SELECTOR, ...], shape: tuple[int, ...]) -> Selection:
        if not isinstance(indices, tuple):
            indices = (indices,)

        return Selection(_as_indexers(indices, shape), shape=shape)

    def get_indexers(
        self,
        sorted: bool = False,
        enforce_1d: bool = False,
        for_h5: bool = False,
    ) -> tuple[int | npt.NDArray[np.int_] | slice | None, ...]:
        """Get indexers for reading data in a h5py Dataset from a Selection.
        Args:
            sorted:
            enforce_1d:
            for_h5: skip new axes, transform lists of 1 element into single integer index
        """
        if for_h5:
            return tuple(
                get_indexer(i, sorted=sorted, enforce_1d=enforce_1d, for_h5=True)
                for i in self._indices
                if not isinstance(i, NewAxisType)
            )

        return tuple(get_indexer(i, sorted=sorted, enforce_1d=enforce_1d, for_h5=False) for i in self._indices)

    def _min_shape(self, new_axes: bool) -> tuple[int, ...]:
        last_slice_position = np.argwhere(self.is_slice)[-1, 0] if any(self.is_slice) else np.inf
        first_list_position = np.argmax(self.is_list) if any(self.is_list) else -1

        slice_indices_shape = tuple(len(s) for s in self._indices if isinstance(s, FullSlice))
        list_indices_shape = np.broadcast_shapes(
            *(lst.shape for lst in self._indices if isinstance(lst, (ListIndex, EmptyList)) and lst.ndim > 0)
        )

        if first_list_position < last_slice_position:
            min_shape = list_indices_shape + slice_indices_shape

        else:
            min_shape = slice_indices_shape + list_indices_shape

        if not new_axes:
            return min_shape

        if any(dropwhile(lambda x: x, reversed(list(dropwhile(lambda x: x, self.is_newaxis))))):
            raise NotImplementedError("Cannot have new axis besides first and last indices yet.")

        new_axes_before = tuple(1 for _ in takewhile(lambda x: x, self.is_newaxis))
        new_axes_after = tuple(1 for _ in takewhile(lambda x: x, reversed(self.is_newaxis[len(new_axes_before) :])))

        return new_axes_before + min_shape + new_axes_after

    def cast_on(self, previous_selection: Selection) -> Selection:
        if np.prod(previous_selection.out_shape) and self.in_shape != previous_selection.out_shape:
            raise ValueError(f"Cannot cast {self._array_shape} selection on {previous_selection.out_shape} selection.")

        if self.is_empty:
            return previous_selection

        if previous_selection.is_empty:
            return self

        previous_indices_queue = Queue(previous_selection._indices)
        self_indices_queue = Queue(self._indices)

        casted_selection: list[Indexer | PlaceHolderType] = [PLACEHOLDER] * len(previous_selection)

        while len(previous_indices_queue):
            if not len(self_indices_queue):
                one_previous_sel_element, idx = previous_indices_queue.next_one()
                casted_selection[idx] = one_previous_sel_element
                continue

            previous_sel_element = previous_indices_queue.next_all()

            if isinstance(previous_sel_element, IndexedValue):
                if isinstance(previous_sel_element.value, SingleIndex):
                    casted_selection[previous_sel_element.idx] = previous_sel_element.value
                    continue

                self_sel_element, _ = self_indices_queue.next_one()

                if isinstance(previous_sel_element.value, (FullSlice, EmptyList)):
                    casted_selection[previous_sel_element.idx] = previous_sel_element.value[self_sel_element]
                    continue

                assert isinstance(previous_sel_element.value, NewAxisType)
                if self_sel_element.as_numpy_index() != 0:
                    raise IndexError

                del casted_selection[previous_sel_element.idx]
                del previous_indices_queue[previous_sel_element.idx]

            else:
                self_sel_elements = tuple(e for (e, _) in self_indices_queue.next_n(previous_sel_element[0].value.ndim))

                for iv in previous_sel_element:
                    assert isinstance(iv.value, ListIndex)

                    casted_selection[iv.idx] = iv.value[self_sel_elements]

        casted_selection.extend(self_indices_queue)

        assert all(isinstance(e, Indexer) for e in casted_selection)

        sel = Selection(casted_selection, shape=previous_selection.in_shape)  # type: ignore[arg-type]

        if not sel.contains_empty_list and (sel.in_shape, sel.out_shape) != (
            previous_selection.in_shape,
            self.out_shape,
        ):
            raise RuntimeError("Selection casting failed: could not maintain shape consistency.")

        return sel

    def _get_loading_sel(self, extra_before: int = 0, extra_after: int = 0) -> tuple[int | slice, ...]:
        if extra_before == 0 and extra_after == 0 and not any(i is NewAxis for i in self._indices):
            return ()

        before = tuple(0 for _ in takewhile(lambda x: x is NewAxis, self._indices)) + (0,) * extra_before
        middle = tuple(
            slice(None)
            for i in takewhile(lambda x: x is not NewAxis, self._indices[len(before) :])
            if not isinstance(i, SingleIndex)
        )
        after = (
            tuple(0 for _ in takewhile(lambda x: x is NewAxis, self._indices[len(before) :][::-1])) + (0,) * extra_after
        )

        return before + middle + after

    def _get_loading_sel_iter(self, it: Iterator[int], list_indices: list[int]) -> Generator[int | slice, None, None]:
        yield from (0 for _ in takewhile(lambda i: i is NewAxis, self._indices))

        indices_it = enumerate(dropwhile(lambda i: i is NewAxis, self._indices))

        for _, s in dropwhile(lambda i_s: i_s[0] is NewAxis, zip(self._indices, self.out_shape)):
            if s == 1:
                yield 0

            else:
                idx, _ = next(indices_it)

                if idx in list_indices:
                    try:
                        yield next(it)
                    except StopIteration:
                        break

                else:
                    yield slice(None)

    def iter_indexers(
        self, can_reorder: bool = True
    ) -> Generator[
        tuple[
            tuple[int | npt.NDArray[np.int_] | slice | None, ...],
            slice | npt.NDArray[np.int_],
            tuple[int | npt.NDArray[np.int_] | slice, ...],
        ],
        None,
        tuple[npt.NDArray[np.int_] | slice, ...] | None,
    ]:
        list_indices = [idx for idx, i in enumerate(self._indices) if isinstance(i, ListIndex)]

        # short indexing ------------------------------------------------------
        if not len(list_indices):
            yield (
                self.get_indexers(for_h5=True),
                slice(None),
                self._get_loading_sel(),
            )
            return None

        if len(list_indices) == 1:
            list_ = self._indices[list_indices[0]]
            assert isinstance(list_, ListIndex)

            unique_list, inverse = np.unique(list_, return_inverse=True)

            already_sorted = np.array_equal(list_.as_array(sorted=True), list_.as_array())
            already_unique = len(unique_list) == len(list_)

            if can_reorder or already_sorted:
                if list_.ndim == 1:
                    indices = self.get_indexers(sorted=True, enforce_1d=True)

                    if already_unique:
                        yield (
                            indices,
                            slice(None),
                            self._get_loading_sel(),
                        )

                    else:
                        indices = indices[: list_indices[0]] + (unique_list,) + indices[list_indices[0] + 1 :]
                        yield (
                            indices,
                            inverse,
                            self._get_loading_sel(),
                        )
                        already_sorted = True

                elif list_.squeeze().ndim == 1:
                    extra_before = len(tuple(takewhile(lambda x: x == 1, list_.shape[:-1])))
                    extra_after = len(tuple(takewhile(lambda x: x, list_.shape[extra_before + 1 :][::-1])))

                    yield (
                        self.get_indexers(sorted=True, enforce_1d=True),
                        slice(None),
                        self._get_loading_sel(extra_before, extra_after),
                    )

                else:
                    raise NotImplementedError
                    # for idx, list_e in enumerate(list_.as_array(sorted=True)):
                    #     dataset_sel = tuple(
                    #         list_e if i == list_indices[0] else get_indexer(e, for_h5=True)
                    #         for i, e in enumerate(self._indices)
                    #     )
                    #     loading_sel = tuple(0 for s in self.out_shape if s == 1) + (idx,)

                    #     yield dataset_sel, loading_sel

                if not already_sorted:
                    sel_it = chain(self.get_indexers(for_h5=True), repeat(slice(None)))
                    return tuple(slice(None) if s == 1 else _get_sorting_indices(next(sel_it)) for s in self.out_shape)

                return None

        # long indexing -------------------------------------------------------
        if not self.out_shape_squeezed:
            yield (self.get_indexers(for_h5=True), slice(None), ())
            return None

        indices_dataset = [
            a.flatten() for a in np.broadcast_arrays(*(idx for i, idx in enumerate(self._indices) if i in list_indices))
        ]
        indices_loading = [i.flatten() for i in np.indices(self.out_shape_squeezed[: len(list_indices)])]

        for index_dataset, index_loading in zip(
            (iter(di) for di in zip(*indices_dataset)), (iter(li) for li in zip(*indices_loading))
        ):
            dataset_sel = tuple(
                next(index_dataset) if i in list_indices else get_indexer(e, for_h5=True)
                for i, e in enumerate(self._indices)
                if e is not NewAxis
            )
            loading_sel = tuple(self._get_loading_sel_iter(index_loading, list_indices))

            yield dataset_sel, slice(None), loading_sel

        return None

    # endregion


class Queue:
    # region magic methods
    def __init__(self, elements: Iterable[Indexer]):
        self._elements = list(elements)
        self._indices = list(range(len(self._elements)))

        self._broadcast_shape = np.broadcast_shapes(*[li.shape for li in self._elements if isinstance(li, ListIndex)])

    def __repr__(self) -> str:
        return f"Queue({self._elements})"

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self) -> Iterator[Indexer]:
        return iter(self._elements)

    def __delitem__(self, index: int) -> None:
        if not len(self._indices):
            return

        if self._indices[0] <= index:
            raise ValueError

        self._indices = [i - 1 for i in self._indices]

    # endregion

    # region methods
    def next_one(self) -> tuple[Indexer, int]:
        if not len(self._elements):
            raise IndexError

        return self._elements.pop(0), self._indices.pop(0)

    def next_n(self, n: int) -> tuple[tuple[Indexer, int], ...]:
        if not len(self._elements):
            raise IndexError

        if (
            n == 1
            and len(self._elements) >= 2
            and isinstance(self._elements[0], FullSlice)
            and isinstance(self._elements[1], (ListIndex, EmptyList))
        ):
            return ((self._elements.pop(0), self._indices.pop(0)), (NewAxis, -1))

        return tuple((self._elements.pop(0), self._indices.pop(0)) for _ in range(min(n, len(self._elements))))

    def next_all(self) -> IndexedValue | tuple[IndexedValue, ...]:
        if not len(self._elements):
            raise IndexError

        if not isinstance(self._elements[0], ListIndex):
            return IndexedValue(self._elements.pop(0), self._indices.pop(0))

        lists = tuple(
            IndexedValue(e.broadcast_to(self._broadcast_shape), i)
            for e, i in zip(self._elements, self._indices)
            if isinstance(e, ListIndex)
        )

        self._indices = [i for e, i in zip(self._elements, self._indices) if not isinstance(e, ListIndex)]
        self._elements = [e for e in self._elements if not isinstance(e, ListIndex)]

        return tuple(li for li in lists)

    # endregion
