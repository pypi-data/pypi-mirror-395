from __future__ import annotations

from enum import Enum, auto
from functools import partial
from numbers import Number
from typing import TYPE_CHECKING, Any, Callable, Iterable, cast

import numpy as np
import numpy.typing as npt
from numpy import _NoValue as NoValue  # type: ignore[attr-defined]

import ch5mpy
from ch5mpy._typing import NP_FUNC
from ch5mpy.array.chunks.iter import iter_chunks_2
from ch5mpy.indexing import FullSlice, SingleIndex, map_slice

if TYPE_CHECKING:
    from ch5mpy import H5Array


class ApplyOperation(Enum):
    set = auto()
    iadd = auto()
    imul = auto()
    iand = auto()
    ior = auto()


def ensure_h5array_first(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
) -> tuple[
    H5Array[Any],
    npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    Callable[[npt.NDArray[Any] | H5Array[Any], npt.NDArray[Any] | H5Array[Any]], npt.NDArray[Any] | H5Array[Any]],
    Callable[[npt.NDArray[Any] | H5Array[Any], npt.NDArray[Any] | H5Array[Any]], npt.NDArray[Any] | H5Array[Any]],
]:
    """One of x1, x2 must be an H5Array. Returns x1, x2 (maybe swapped such that the first returned array is guaranteed
    to be an H5Array).
    Also return getter functions swapping arrays back in the order they were passed to this function if needed."""
    if not isinstance(x1, ch5mpy.H5Array):
        return cast(ch5mpy.H5Array[Any], x2), x1, lambda _, x2: x2, lambda x1, _: x1

    return x1, x2, lambda x1, _: x1, lambda _, x2: x2


class MaskWhere:
    def __init__(
        self,
        where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue,
        shape: tuple[int, ...],
    ):
        # TODO : make memory efficient (avoid broadcast and compute on the fly)
        self._where = None if where in (True, NoValue) else np.broadcast_to(where, shape)  # type: ignore[arg-type]

    def __repr__(self) -> str:
        return f"MaskWhere({self._where})"

    def __getitem__(self, item: tuple[Any, ...] | slice) -> npt.NDArray[np.bool_] | None:
        if self._where is None:
            return None

        return self._where[item]


def _get_output_array(
    out: H5Array[Any] | npt.NDArray[Any] | None,
    shape: tuple[int, ...],
    axis: tuple[int, ...],
    keepdims: bool,
    dtype: npt.DTypeLike | None,
    initial: int | float | complex | NoValue,
) -> H5Array[Any] | npt.NDArray[Any]:
    if keepdims:
        expected_shape = tuple(s if i not in axis else 1 for i, s in enumerate(shape))

    else:
        expected_shape = tuple(s for i, s in enumerate(shape) if i not in axis)

    if out is not None:
        ndim = len(expected_shape)
        if out.ndim != ndim:
            raise ValueError(f"Output array has the wrong number of dimensions: Found {out.ndim} but expected {ndim}")

        if out.shape != expected_shape:
            raise ValueError(f"Output array has the wrong shape: Found {out.shape} but expected {expected_shape}")

        if initial is not NoValue:
            out[()] = initial

        return out

    if initial is NoValue:
        return np.empty(shape=expected_shape, dtype=dtype)

    return np.full(shape=expected_shape, fill_value=initial, dtype=dtype)


def _get_output_array_2(
    out: H5Array[Any] | npt.NDArray[Any] | None,
    a_shape: tuple[int, ...],
    b_shape: tuple[int, ...],
    dtype: npt.DTypeLike | None,
    default: Any,
) -> H5Array[Any] | npt.NDArray[Any]:
    expected_shape = np.broadcast_shapes(a_shape, b_shape)

    if out is not None:
        ndim = len(expected_shape)
        if out.ndim != ndim:
            raise ValueError(f"Output array has the wrong number of dimensions: Found {out.ndim} but expected {ndim}")

        if out.shape != expected_shape:
            raise ValueError(f"Output array has the wrong shape: Found {out.shape} but expected {expected_shape}")

        return out

    if default is None:
        return np.empty(shape=expected_shape, dtype=dtype)

    return np.full(shape=expected_shape, fill_value=default, dtype=dtype)


def _as_tuple(
    axis: int | Iterable[int] | tuple[int, ...] | None,
    ndim: int,
    default_0D_output: bool,
) -> tuple[int, ...]:
    if axis is None:
        return tuple(range(ndim)) if default_0D_output else ()

    elif not isinstance(axis, Iterable):
        return (axis,)

    return tuple(axis)


def _get_indices(
    index: tuple[SingleIndex | FullSlice, ...],
    axis: tuple[int, ...],
    where_compute: MaskWhere,
    where_output: MaskWhere,
    output_ndim: int,
) -> tuple[npt.NDArray[np.bool_] | None, tuple[slice, ...], npt.NDArray[np.bool_] | None]:
    # compute on whole array at once
    if len(index) == 1 and isinstance(index[0], FullSlice) and index[0].is_whole_axis:
        return where_compute[:], (), where_output[index]

    where_to_compute = where_compute[map_slice(index)]

    # 0D output array (no chunk selection, no where selection)
    if output_ndim == 0:
        return where_to_compute, (), None

    # nD output array
    selected_index = map_slice(tuple(e for i, e in enumerate(index) if i not in axis))
    return where_to_compute, selected_index, where_output[selected_index]


def _apply_operation(
    operation: ApplyOperation,
    dest: H5Array[Any] | npt.NDArray[Any],
    chunk_selection: tuple[slice, ...] | tuple[()],
    where_to_output: npt.NDArray[np.bool_] | None,
    values: npt.NDArray[Any],
) -> None:
    if values.ndim == 0:
        values = values[()]

    if operation is ApplyOperation.set:
        if dest.ndim == 0:
            dest[()] = values

        else:
            dest[chunk_selection][where_to_output] = values[where_to_output]

    elif operation is ApplyOperation.iadd:
        if dest.ndim == 0:
            dest[()] = values + dest[()]

        else:
            dest[chunk_selection][where_to_output] += values[where_to_output]

    elif operation is ApplyOperation.imul:
        if dest.ndim == 0:
            dest *= values  # type: ignore[assignment]

        else:
            dest[chunk_selection][where_to_output] *= values[where_to_output]

    elif operation is ApplyOperation.iand:
        if dest.ndim == 0:
            dest &= values  # type: ignore[assignment]

        else:
            dest[chunk_selection][where_to_output] &= values[where_to_output]

    elif operation is ApplyOperation.ior:
        if dest.ndim == 0:
            dest |= values  # type: ignore[assignment]

        else:
            dest[chunk_selection][where_to_output] |= values[where_to_output]

    else:
        raise NotImplementedError(f"Do not know how to apply operation '{operation}'")


def apply(
    func: partial[NP_FUNC],
    operation: ApplyOperation,
    a: H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None,
    *,
    dtype: npt.DTypeLike | None,
    initial: int | float | complex | NoValue,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue,
    default_0D_output: bool = True,
) -> Any:
    dtype = a.dtype if dtype is None else dtype
    axis = _as_tuple(func.keywords.get("axis", None), a.ndim, default_0D_output)
    output_array = _get_output_array(out, a.shape, axis, func.keywords.get("keepdims", False), dtype, initial)

    if where is not False:
        where_compute = MaskWhere(where, a.shape)
        where_output = MaskWhere(where, output_array.shape)

        for index, chunk in a.iter_chunks(keepdims=True):
            where_to_compute, chunk_selection, where_to_output = _get_indices(
                index, axis, where_compute, where_output, output_array.ndim
            )
            result = np.array(
                func(chunk, where=True if where_to_compute is None else where_to_compute),
                dtype=output_array.dtype,
            )
            _apply_operation(operation, output_array, chunk_selection, where_to_output, result)

    if out is None and output_array.ndim == 0:
        return output_array[()]

    return output_array


def apply_everywhere(
    func: partial[NP_FUNC],
    operation: ApplyOperation,
    a: H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None,
    *,
    dtype: npt.DTypeLike | None,
    initial: int | float | complex | NoValue,
    default_0D_output: bool = True,
) -> Any:
    dtype = a.dtype if dtype is None else dtype
    axis = _as_tuple(func.keywords.get("axis", None), a.ndim, default_0D_output)
    output_array = _get_output_array(out, a.shape, axis, func.keywords.get("keepdims", False), dtype, initial)

    where_compute = MaskWhere(True, a.shape)
    where_output = MaskWhere(True, output_array.shape)

    for index, chunk in a.iter_chunks(keepdims=True):
        _, chunk_selection, where_to_output = _get_indices(index, axis, where_compute, where_output, output_array.ndim)
        result = np.array(func(chunk), dtype=output_array.dtype)
        _apply_operation(operation, output_array, chunk_selection, where_to_output, result)

    if out is None and output_array.ndim == 0:
        return output_array[()]

    return output_array


def _get_str_dtype(
    a: npt.NDArray[np.str_] | H5Array[np.str_],
    b: npt.NDArray[Any] | H5Array[Any],
    func: NP_FUNC,
) -> np.dtype[Any]:
    assert np.issubdtype(a.dtype, str)

    if func == np.char.multiply:
        assert np.issubdtype(b.dtype, np.number)
        return np.dtype(f"<U{a.dtype.itemsize // 4 * max(b)}")

    if func == np.char.add:
        assert np.issubdtype(b.dtype, str)
        return np.dtype(f"<U{(a.dtype.itemsize + b.dtype.itemsize) // 4}")

    elif func in (
        np.char.greater,
        np.char.greater_equal,
        np.char.less,
        np.char.less_equal,
        np.char.equal,
        np.char.not_equal,
    ):
        return np.dtype(bool)

    raise NotImplementedError


def str_apply_2(
    func: NP_FUNC,
    a: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_],
    b: Any,
) -> npt.NDArray[Any] | H5Array[Any] | bool:
    a_arr = a if isinstance(a, (np.ndarray, ch5mpy.H5Array)) else np.array(a, dtype=str)
    b_arr = b if isinstance(b, (np.ndarray, ch5mpy.H5Array)) else np.array(b)

    if b_arr.dtype == object:
        b_arr = b_arr.astype(str)

    output_array = _get_output_array_2(None, a_arr.shape, b_arr.shape, _get_str_dtype(a_arr, b_arr, func), None)

    if not np.issubdtype(b_arr.dtype, str):
        try:
            return {np.char.equal: False, np.char.not_equal: True}[func]

        except KeyError:
            raise TypeError(f"'{func}' not supported between arrays with dtypes {a_arr.dtype} and {b_arr.dtype}.")

    for index, chunk_x1, chunk_x2 in iter_chunks_2(a_arr, b_arr):
        output_array[map_slice(index)] = func(chunk_x1, chunk_x2)

    return output_array


num_to_str_ufunc: dict[NP_FUNC, NP_FUNC] = {
    np.add: np.char.add,
    np.multiply: np.char.multiply,
    np.greater: np.char.greater,
    np.greater_equal: np.char.greater_equal,
    np.less: np.char.less,
    np.less_equal: np.char.less_equal,
    np.equal: np.char.equal,
    np.not_equal: np.char.not_equal,
}


def apply_2(
    func: NP_FUNC,
    a: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    b: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    *,
    out: H5Array[Any] | npt.NDArray[Any] | None,
    default: Any,
    dtype: npt.DTypeLike | None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | int | bool,
) -> Any:
    h5, maybe_not_h5, get_a, get_b = ensure_h5array_first(a, b)

    # if h5array is a str H5Array (got here because the operators ==, +, *, ... were used), pass to str_apply_2()
    if np.issubdtype(h5.dtype, str):
        assert out is None and where is True
        return str_apply_2(num_to_str_ufunc[func], a, b)  # type: ignore[arg-type]

    # operation on regular H5Arrays
    if not isinstance(maybe_not_h5, (np.ndarray, ch5mpy.H5Array)):
        maybe_not_h5 = np.array(maybe_not_h5)

    output_array = _get_output_array_2(out, h5.shape, maybe_not_h5.shape, dtype, default)

    if where is not False:
        where_compute = MaskWhere(where, get_a(h5, maybe_not_h5).shape)
        where_output = MaskWhere(where, output_array.shape)

        for index, chunk_x1, chunk_x2 in iter_chunks_2(get_a(h5, maybe_not_h5), get_b(h5, maybe_not_h5)):
            where_to_compute, chunk_selection, where_to_output = _get_indices(
                index, (), where_compute, where_output, output_array.ndim
            )
            result = np.array(
                func(
                    chunk_x1,
                    chunk_x2,
                    where=True if where_to_compute is None else where_to_compute,
                ),
                dtype=output_array.dtype,
            )
            _apply_operation(
                ApplyOperation.set,
                output_array,
                chunk_selection,
                where_to_output,
                result,
            )

    if out is None and output_array.ndim == 0:
        return output_array[()]

    return output_array
