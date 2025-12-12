from __future__ import annotations

from collections.abc import Iterable, Sequence
from itertools import repeat
from typing import TYPE_CHECKING, Any, Literal, SupportsIndex, cast

import numpy as np
import numpy.typing as npt
from numpy._typing import _ArrayLikeInt_co  # pyright: ignore[reportPrivateUsage]

import ch5mpy
from ch5mpy._typing import NP_FUNC
from ch5mpy.array.functions.apply import ensure_h5array_first
from ch5mpy.array.functions.implement import implements

if TYPE_CHECKING:
    from ch5mpy import H5Array


CastingKind = Literal["no", "equiv", "safe", "same_kind", "unsafe"]
_NAN_PLACEHOLDER = object()
_NUMPY_VERSION = tuple(map(int, np.__version__.split(".")))


@implements(np.unique)
def unique(
    ar: H5Array[Any],
    return_index: bool = False,
    return_inverse: bool = False,
    return_counts: bool = False,
    axis: int | None = None,
    *,
    equal_nan: bool = True,
) -> (
    npt.NDArray[Any]
    | tuple[npt.NDArray[Any], npt.NDArray[np.int_]]
    | tuple[npt.NDArray[Any], npt.NDArray[np.int_], npt.NDArray[np.int_]]
    | tuple[
        npt.NDArray[Any],
        npt.NDArray[np.int_],
        npt.NDArray[np.int_],
        npt.NDArray[np.int_],
    ]
):
    if return_inverse:
        raise NotImplementedError

    if axis is not None:
        raise NotImplementedError

    unique = np.array([])
    index = np.array([])
    counts: dict[Any, int] = {}
    index_offset = 0

    for _, chunk in ar.iter_chunks():
        unique_chunk, index_chunk, counts_chunk = np.unique(
            chunk, return_index=True, return_counts=True, equal_nan=equal_nan
        )

        unique_concat = np.concatenate((unique, unique_chunk))
        index_concat = np.concatenate((index, index_chunk + index_offset))

        for u, c in zip(unique_chunk, counts_chunk):
            if isinstance(u, float) and np.isnan(u):
                u = _NAN_PLACEHOLDER
            counts[u] = counts.setdefault(u, 0) + c

        unique, i = np.unique(unique_concat, return_index=True, equal_nan=equal_nan)
        index = index_concat[i]

        index_offset += chunk.size

    to_return: tuple[npt.NDArray[Any], ...] = (unique,)
    if return_index:
        to_return += (index,)
    if return_counts:
        counts_array = np.array([counts[u] for u in unique if not np.isnan(u)])
        if _NAN_PLACEHOLDER in counts:
            if equal_nan:
                counts_array = np.concatenate((counts_array, np.array([counts[_NAN_PLACEHOLDER]])))

            else:
                counts_array = np.concatenate(
                    (
                        counts_array,
                        np.array([1 for _ in range(counts[_NAN_PLACEHOLDER])]),
                    )
                )

        to_return += (counts_array,)

    if len(to_return) == 1:
        return to_return[0]
    return to_return  # pyright: ignore[reportReturnType]


def _in_chunk(
    chunk_1: npt.NDArray[Any],
    chunk_2: npt.NDArray[Any],
    res: npt.NDArray[Any],
    invert: bool,
    func: NP_FUNC,
) -> npt.NDArray[np.bool_]:
    if invert:
        return np.logical_and(res, func(chunk_1, chunk_2, invert=True))

    else:
        return np.logical_or(res, func(chunk_1, chunk_2))


@implements(np.in1d)
def in1d(ar1: Any, ar2: Any, invert: bool = False) -> npt.NDArray[np.bool_]:
    # cast arrays as either np.arrays or H5Arrays
    if not isinstance(ar1, (np.ndarray, ch5mpy.H5Array)):
        ar1 = np.array(ar1)

    if not isinstance(ar2, (np.ndarray, ch5mpy.H5Array)):
        ar2 = np.array(ar2)

    # prepare output
    if invert:
        res = np.ones(ar1.size, dtype=bool)
    else:
        res = np.zeros(ar1.size, dtype=bool)

    # case np.array in H5Array
    if type(ar1) == np.ndarray:  # noqa: E721
        ar2 = cast(ch5mpy.H5Array[Any], ar2)

        for _, chunk in ar2.iter_chunks():
            res = _in_chunk(ar1, chunk, res, invert=invert, func=np.in1d)

    else:
        ar1 = cast(ch5mpy.H5Array[Any], ar1)
        index_offset = 0

        # case H5Array in np.array
        if type(ar2) == np.ndarray:  # noqa: E721
            for _, chunk in ar1.iter_chunks():
                index = slice(index_offset, index_offset + chunk.size)
                index_offset += chunk.size
                res[index] = _in_chunk(chunk, ar2, res[index], invert=invert, func=np.in1d)

        # case H5Array in H5Array
        else:
            ar2 = cast(ch5mpy.H5Array[Any], ar2)

            for _, chunk_1 in ar1.iter_chunks():
                index = slice(index_offset, index_offset + chunk_1.size)
                index_offset += chunk_1.size

                for _, chunk_2 in ar2.iter_chunks():
                    res[index] = _in_chunk(chunk_1, chunk_2, res[index], invert=invert, func=np.in1d)

    return res


@implements(np.isin)
def isin(element: Any, test_elements: Any, invert: bool = False) -> npt.NDArray[np.bool_]:
    # cast arrays as either np.arrays or H5Arrays
    if not isinstance(element, (np.ndarray, ch5mpy.H5Array)):
        element = np.array(element)

    if not isinstance(test_elements, (np.ndarray, ch5mpy.H5Array)):
        test_elements = np.array(test_elements)

    # prepare output
    if invert:
        res = np.ones_like(element, dtype=bool)
    else:
        res = np.zeros_like(element, dtype=bool)

    # case np.array in H5Array
    if type(element) == np.ndarray:  # noqa: E721
        test_elements = cast(ch5mpy.H5Array[Any], test_elements)

        for _, chunk in test_elements.iter_chunks():
            res = _in_chunk(element, chunk, res, invert=invert, func=np.isin)

    else:
        element = cast(ch5mpy.H5Array[Any], element)

        # case H5Array in np.array
        if type(test_elements) == np.ndarray:  # noqa: E721
            for index, chunk in element.iter_chunks():
                res[index] = _in_chunk(chunk, test_elements, res[index], invert=invert, func=np.isin)

        # case H5Array in H5Array
        else:
            test_elements = cast(ch5mpy.H5Array[Any], test_elements)

            for index_elem, chunk_elem in element.iter_chunks():
                for _, chunk_test in test_elements.iter_chunks():
                    res[index_elem] = _in_chunk(
                        chunk_elem,
                        chunk_test,
                        res[index_elem],
                        invert=invert,
                        func=np.isin,
                    )

    return res


@implements(np.concatenate)
def concatenate(
    arrays: H5Array[Any] | tuple[H5Array[Any] | npt.NDArray[Any], ...],
    axis: int | None = 0,
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    dtype: npt.DTypeLike | None = None,
) -> npt.NDArray[Any]:
    if out is None:
        if isinstance(arrays, ch5mpy.H5Array):
            return np.concatenate(np.array(arrays), axis=axis, dtype=dtype)

        else:
            return np.concatenate(tuple(map(np.array, arrays)), axis=axis, dtype=dtype)

    else:
        raise NotImplementedError


if _NUMPY_VERSION >= (1, 24, 0):

    @implements(np.hstack)
    def hstack(
        tup: Iterable[H5Array[Any] | npt.NDArray[Any]],
        *,
        dtype: npt.DTypeLike | None = None,
        casting: CastingKind = "same_kind",
    ) -> npt.NDArray[Any]:
        return np.hstack([np.array(a) for a in tup], dtype=dtype, casting=casting)

else:

    @implements(np.hstack)
    def hstack(tup: Iterable[H5Array[Any] | npt.NDArray[Any]]) -> npt.NDArray[Any]:
        return np.hstack([np.array(a) for a in tup])


@implements(np.vstack)
def vstack(
    tup: Iterable[H5Array[Any] | npt.NDArray[Any]],
    *,
    dtype: npt.DTypeLike | None = None,
    casting: CastingKind = "same_kind",
) -> npt.NDArray[Any]:
    return np.vstack(tuple(map(np.array, tup)), dtype=dtype, casting=casting)


@implements(np.repeat)
def repeat_(a: H5Array[Any], repeats: _ArrayLikeInt_co, axis: SupportsIndex | None = None) -> npt.NDArray[Any]:
    # FIXME: custom implementation to be more memory efficient (avoid importing a into RAM)
    return np.repeat(np.array(a), repeats, axis)


@implements(np.sort)
def sort(
    a: H5Array[Any],
    axis: int | None = -1,
    kind: Literal["quicksort", "mergesort", "heapsort", "stable"] | None = None,
    order: str | Sequence[str] | None = None,
) -> npt.NDArray[Any]:
    return np.sort(np.array(a), axis, kind, order)


@implements(np.insert)
def insert(
    arr: H5Array[Any],
    obj: int | slice | Sequence[int],
    values: npt.ArrayLike,
    axis: int | None = None,
) -> H5Array[Any]:
    r"""/!\ Happens `in place` !"""
    if arr.ndim > 1 and axis is None:
        raise NotImplementedError

    if axis is None:
        axis = 0

    if isinstance(obj, slice):
        raise NotImplementedError

    indexer = np.atleast_1d(obj)
    values = np.atleast_1d(values)

    out_of_bounds = indexer > arr.shape[axis]
    if np.any(out_of_bounds):
        raise IndexError(
            f"Index {tuple(indexer[out_of_bounds])} is out of bounds for axis {axis} with size {arr.shape[axis]}."
        )

    indexer[indexer < 0] += arr.shape[axis]

    if len(indexer) == 1:
        values = np.broadcast_to(values, (len(indexer), len(np.atleast_1d(values))))

    elif indexer.shape != values.shape:
        raise ValueError(f"Cannot set {indexer.shape} values from {values.shape} data.")

    # resize the array to insert extra columns at the end
    # matrix | 0 1 2 3 4 |
    #   ==>  | 0 1 2 3 4 . |
    arr.expand(len(indexer), axis=axis)

    prefix = (slice(None),) * axis
    indexer_sort_indices = np.argsort(indexer)[::-1]
    for index, value in zip(
        indexer[indexer_sort_indices],
        values[indexer_sort_indices],
    ):
        if index < (arr.shape[axis] - 1):
            # transfer data one row to the right, starting from the column after `obj` and insert values at `obj`
            # matrix | 0 1 2 3 4 . | with `obj` = 2
            #   ==>  | 0 1 . 2 3 4 |
            index_dest = prefix + (slice(index + 1, None),)
            index_source = prefix + (slice(index, -1),)
            arr[index_dest] = arr[index_source]

        # matrix | 0 1 . 2 3 4 |
        #   ==>  | 0 1 v 2 3 4 |
        arr[prefix + (index,)] = value

    return arr


@implements(np.delete)
def delete(arr: H5Array[Any], obj: int | slice | Sequence[int], axis: int | None = None) -> H5Array[Any]:
    if arr.ndim > 1 and axis is None:
        raise NotImplementedError

    if axis is None:
        axis = 0

    if not isinstance(obj, (int, np.integer)):
        raise NotImplementedError

    if obj > arr.shape[axis]:
        raise IndexError(f"Index {obj} is out of bounds for axis {axis} with size {arr.shape[axis]}.")

    elif obj < 0:
        obj = obj + arr.shape[axis]

    prefix = (slice(None),) * axis
    if obj < (arr.shape[axis] - 1):
        # transfer data one row to the left, starting from the column after the one to delete
        # matrix | 0 1 2 3 4 | with index of the column to delete = 2
        #   ==>  | 0 1 3 4 . |
        index_dest = prefix + (slice(obj, -1),)
        index_source = prefix + (slice(obj + 1, None),)
        arr[index_dest] = arr[index_source]

    # resize the arrays to drop the extra column at the end
    # matrix | 0 1 3 4 . |
    #   ==>  | 0 1 3 4 |
    arr.contract(1, axis=axis)

    return arr


@implements(np.atleast_1d)
def atleast_1d(arr: H5Array[Any]) -> H5Array[Any]:
    if arr.ndim >= 1:
        return arr
    return arr[None]


@implements(np.ravel)
def ravel(arr: H5Array[Any], order: Literal["C", "F", "A", "K"] = "C") -> npt.NDArray[Any]:
    return np.ravel(np.array(arr), order=order)


@implements(np.take)
def take(
    arr: H5Array[Any],
    indices: _ArrayLikeInt_co,
    axis: SupportsIndex | None = None,
    out: npt.NDArray[Any] | None = None,
    mode: Literal["raise", "wrap", "clip"] = "raise",
) -> npt.NDArray[Any]:
    if out is None:
        out = np.empty_like(indices, dtype=arr.dtype)

    if not out.size:
        return out

    if axis is not None:
        out[:] = arr[tuple(repeat(slice(None), int(axis))) + (indices,)]

    else:
        out[:] = arr[np.unravel_index(indices, arr.shape)]

    return out


@implements(np.copyto)
def copyto(
    dst: H5Array[Any],
    src: npt.ArrayLike,
    casting: Literal["no", "equiv", "safe", "same_kind", "unsafe"] = "same_kind",
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | bool = True,
) -> None:
    src = np.asanyarray(src)

    if not np.can_cast(src.dtype, dst.dtype, casting):
        raise TypeError(f"Cannot cast array data from {src.dtype} to {src.dtype} according to rule '{casting}'.")

    dst[()] = np.broadcast_to(src, dst.shape)


@implements(np.may_share_memory)
def may_share_memory(a: H5Array[Any] | npt.NDArray[Any], b: H5Array[Any] | npt.NDArray[Any]) -> bool:
    h5, maybe_not_h5, *_ = ensure_h5array_first(a, b)

    if not isinstance(maybe_not_h5, ch5mpy.H5Array):
        return False

    if h5._dset is maybe_not_h5._dset:  # pyright: ignore[reportPrivateUsage]
        return True

    return False


@implements(np.transpose)
def transpose(a: H5Array[Any], axes: tuple[int, ...] | list[int] | None = None) -> H5Array[Any]:
    if a.ndim < 2:
        return a
    if axes is None:
        axes = list(reversed(range(a.ndim)))
    reshapers = [(slice(None),) + (None,) * i for i in reversed(axes)]
    indexers = tuple(np.arange(i)[r] for i, r in zip(a.shape, reshapers))
    return a[indexers]


@implements(np.append)
def append(arr: H5Array[Any], values: npt.ArrayLike, axis: int | None = None) -> npt.NDArray[Any]:
    # FIXME:  implement concatenation of views of H5Arrays to return an H5Array
    return np.append(np.asarray(arr), np.asarray(values), axis)


@implements(np.split)
def split(
    arr: H5Array[Any], indices_or_sections: int | npt.NDArray[np.integer[Any]], axis: int = 0
) -> list[H5Array[Any]]:
    indices_or_sections = np.atleast_1d(indices_or_sections)

    return [
        arr[(slice(None),) * axis + (slice(i, j),)]
        for i, j in zip(np.r_[0, indices_or_sections], np.r_[indices_or_sections, len(arr)])
    ]


@implements(np.broadcast_arrays)
def broadcast_arrays(*args: npt.ArrayLike, subok: bool = False) -> tuple[npt.NDArray[Any] | H5Array[Any], ...]:
    broadcast_shape = np.broadcast_shapes(*(np.shape(arr) for arr in args))

    for arr in args:
        if isinstance(arr, ch5mpy.H5Array) and broadcast_shape != arr.shape:
            raise NotImplementedError

    return tuple(  # pyright: ignore[reportUnknownVariableType]
        arr if isinstance(arr, ch5mpy.H5Array) else np.broadcast_to(arr, broadcast_shape, subok=subok) for arr in args
    )


@implements(np.shape)
def shape(a: H5Array[Any]) -> tuple[int, ...]:
    return a.shape
