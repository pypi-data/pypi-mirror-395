from __future__ import annotations

from collections.abc import Collection, Iterator
from numbers import Number
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    SupportsIndex,
    TypeVar,
    cast,
    overload,
    override,
)

import numpy as np
import numpy.lib.mixins
import numpy.typing as npt
from numpy._typing import _ArrayLikeInt_co  # pyright: ignore[reportPrivateUsage]

import ch5mpy.io
from ch5mpy._typing import (
    NP_FUNC,
    ONE_AXIS_SELECTOR,
    SELECTOR,
)
from ch5mpy.array import repr
from ch5mpy.array.chunks.iter import ChunkIterator, PairedChunkIterator
from ch5mpy.array.flags import FlagDict
from ch5mpy.array.functions import HANDLED_FUNCTIONS
from ch5mpy.array.io import read_one_from_dataset, write_to_dataset
from ch5mpy.indexing import Selection, map_slice
from ch5mpy.names import H5Mode
from ch5mpy.objects import Dataset, DatasetWrapper, File, Group, H5Object
from ch5mpy.options import _OPTIONS  # pyright: ignore[reportPrivateUsage]
from ch5mpy.utils import NAN_PACKED

if TYPE_CHECKING:
    from ch5mpy.array.view import H5ArrayView
    from ch5mpy.attributes import AttributeManager


_T = TypeVar("_T", bound=np.generic, covariant=True)


def as_array(values: Any, dtype: np.dtype[Any]) -> npt.NDArray[Any]:
    # FIXME : work on H5Arrays directly instead of converting to np.array
    if np.issubdtype(dtype, str):
        return np.array(values, dtype=bytes)

    try:
        return np.array(values, dtype=dtype)

    except ValueError:
        raise ValueError(f"Couldn't set value of type {type(values)} in H5Array of type {dtype}.")


def as_python_scalar(value: np.number[Any]) -> int | float:
    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        return float(value)

    raise TypeError(f"Cannot convert {type(value)} to Python scalar.")


def _dtype_repr(dset: Dataset[Any] | DatasetWrapper[Any]) -> str:
    if np.issubdtype(dset.dtype, np.str_):
        return f"'{dset.dtype}'"

    return str(dset.dtype)


class H5Array(Collection[_T], H5Object, numpy.lib.mixins.NDArrayOperatorsMixin):
    """Wrapper around Dataset objects to interface with numpy's API."""

    __class__ = np.ndarray  # pyright: ignore[reportAssignmentType, reportUnannotatedClassAttribute, reportIncompatibleMethodOverride]

    # region magic methods
    def __init__(self, dset: Dataset[_T] | DatasetWrapper[_T] | H5Array[_T], flags: FlagDict | None = None):
        if isinstance(dset, H5Array):
            self._dset: Dataset[_T] | DatasetWrapper[_T] = dset.dset
            super().__init__(dset.dset.file)
            return

        if not isinstance(dset, (Dataset, DatasetWrapper)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Object of type '{type(dset)}' is not supported by H5Array.")  # pyright: ignore[reportUnreachable]

        if isinstance(dset, Dataset) and np.issubdtype(np.dtype(str(dset.attrs.get("dtype", "O"))), str):
            self._dset = dset.asstr()  # pyright: ignore[reportAttributeAccessIssue]

        else:
            self._dset = dset

        self.flags: FlagDict = flags if isinstance(flags, FlagDict) else FlagDict(self._dset)

        super().__init__(self._dset.file)

    @override
    def __repr__(self) -> str:
        return (
            f"H5Array({repr.print_dataset(self, end='', padding=8, padding_skip_first=True)}, "
            f"shape={self.shape}, dtype={_dtype_repr(self._dset)})"
        )

    @override
    def __str__(self) -> str:
        return repr.print_dataset(self, sep="")

    @overload
    def __getitem__(self, index: tuple[()]) -> H5Array[_T]: ...
    @overload
    def __getitem__(self, index: tuple[ONE_AXIS_SELECTOR, ONE_AXIS_SELECTOR, ONE_AXIS_SELECTOR]) -> _T: ...
    @overload
    def __getitem__(self, index: SELECTOR | tuple[SELECTOR, ...]) -> H5ArrayView[_T]: ...
    def __getitem__(self, index: tuple[()] | SELECTOR | tuple[SELECTOR, ...]) -> _T | H5Array[_T] | H5ArrayView[_T]:
        from ch5mpy.array.view import H5ArrayView

        selection = Selection.from_selector(index, self._dset.shape)

        if selection.is_empty:
            return H5Array(dset=self._dset, flags=self.flags)

        elif selection.out_shape == ():
            return read_one_from_dataset(self._dset, selection, self.dtype)

        else:
            return H5ArrayView(dset=self._dset, sel=selection, flags=self.flags)

    def __setitem__(self, index: SELECTOR | tuple[SELECTOR, ...], value: Any) -> None:
        if not self.flags.writeable:
            raise ValueError("assignment destination is read-only")

        selection = Selection.from_selector(index, self.shape)
        write_to_dataset(self._dset, as_array(value, self.dtype), selection)

    @override
    def __len__(self) -> int:
        return len(self._dset)

    @override
    def __iter__(self) -> Iterator[_T | npt.NDArray[_T] | H5Array[_T] | H5ArrayView[_T]]:  # type: ignore[override]
        for i in range(self.shape[0]):
            yield self[i]

    @override
    def __contains__(self, item: Any) -> bool:
        for _, chunk in self.iter_chunks():
            if item in chunk:
                return True

        return False

    def _inplace(self, func: NP_FUNC, value: Any) -> H5Array[_T]:
        if not self.flags.writeable:
            raise ValueError("assignment destination is read-only")

        if np.issubdtype(self.dtype, str):
            raise TypeError("Cannot perform inplace operation on str H5Array.")

        # special case : 0D array
        if self.shape == ():
            self._dset[:] = func(self._dset[:], value)
            return self

        # general case : 1D+ array
        for index, chunk in self.iter_chunks():
            func(chunk, value, out=chunk)

            # write back result into array
            self.dset.write_direct(
                chunk,
                source_sel=map_slice(index, shift_to_zero=True),
                dest_sel=map_slice(index),
            )

        return self

    @override
    def __add__(self, other: Any) -> Number | str | npt.NDArray[Any]:
        return np.array(self) + other  # type: ignore[no-any-return]

    @override
    def __iadd__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.add, other)

    @override
    def __sub__(self, other: Any) -> Number | str | npt.NDArray[Any]:
        return np.array(self) - other  # type: ignore[no-any-return]

    @override
    def __isub__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.subtract, other)

    @override
    def __mul__(self, other: Any) -> Number | str | npt.NDArray[Any]:
        return np.array(self) * other  # type: ignore[no-any-return]

    @override
    def __imul__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.multiply, other)

    @override
    def __truediv__(self, other: Any) -> Number | str | npt.NDArray[Any]:
        return np.array(self) / other  # type: ignore[no-any-return]

    @override
    def __itruediv__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.divide, other)

    @override
    def __mod__(self, other: Any) -> Number | str | npt.NDArray[Any]:
        return np.array(self) % other  # type: ignore[no-any-return]

    @override
    def __imod__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.mod, other)

    @override
    def __pow__(self, other: Any) -> Number | str | npt.NDArray[Any]:
        return np.array(self) ** other  # type: ignore[no-any-return]

    @override
    def __ipow__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.power, other)

    @override
    def __or__(self, other: Any) -> Number | npt.NDArray[Any]:
        return np.array(self) | other  # type: ignore[no-any-return]

    @override
    def __ior__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.logical_or, other)

    @override
    def __and__(self, other: Any) -> Number | npt.NDArray[Any]:
        return np.array(self) & other  # type: ignore[no-any-return]

    @override
    def __iand__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.logical_and, other)

    @override
    def __invert__(self) -> Number | npt.NDArray[Any]:
        return ~np.array(self)

    @override
    def __xor__(self, other: Any) -> Number | npt.NDArray[Any]:
        return np.array(self) ^ other  # type: ignore[no-any-return]

    @override
    def __ixor__(self, other: Any) -> H5Array[_T]:
        return self._inplace(np.logical_xor, other)

    def __int__(self) -> int:
        if self.size == 1:
            return int(np.array(self))

        raise TypeError("Only size-1 H5Arrays can bon converted to Python scalars.")

    def __float__(self) -> float:
        if self.size == 1:
            return float(np.array(self))

        raise TypeError("Only size-1 H5Arrays can be converted to Python scalars.")

    @override
    def __hash__(self) -> int:
        return hash(np.array(self._dset).data.tobytes())

    def __index__(self) -> int:
        return int(self)

    # endregion

    # region interface
    def __array__(self, dtype: npt.DTypeLike | None = None, copy: bool | None = True) -> npt.NDArray[Any]:
        array = np.array(self._dset)

        # is_nan = np.where(array == NAN_PACKED)
        # if is_nan[0].size:
        #     array[np.where(array == NAN_PACKED)] = np.nan

        if dtype is None:
            return array

        return array.astype(dtype)

    @override
    def __array_ufunc__(self, ufunc: NP_FUNC, method: str, *inputs: Any, **kwargs: Any) -> Any:
        if method == "__call__":
            if ufunc not in HANDLED_FUNCTIONS:
                return NotImplemented

            return HANDLED_FUNCTIONS[ufunc](*inputs, **kwargs)

        else:
            raise NotImplementedError

    def __array_function__(
        self,
        func: NP_FUNC,
        types: tuple[type, ...],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        del types

        if func not in HANDLED_FUNCTIONS:
            return NotImplemented

        return HANDLED_FUNCTIONS[func](*args, **kwargs)

    # endregion

    # region class methods
    @classmethod
    @override
    def read(cls, path: str | Path | File | Group, name: str | None = None, mode: H5Mode = H5Mode.READ) -> H5Array[Any]:
        file = File(path, mode=mode) if isinstance(path, (str, Path)) else path

        if name is None:
            dset = next(iter(file.values()))
            assert isinstance(dset, Dataset)
            return H5Array(dset)

        return H5Array(file[name])

    # endregion

    # region predicates
    @property
    def is_chunked(self) -> bool:
        return self._dset.chunks is not None

    # endregion

    # region attributes
    @property
    def dset(self) -> Dataset[_T] | DatasetWrapper[_T]:
        return self._dset

    @property
    def chunk_size(self) -> int:
        """Get the size of a chunk (i.e. the nb of elements that can be read/written at a time)."""
        return _OPTIONS["max_memory_usage"].get() // self._dset.dtype.itemsize

    @property
    def shape(self) -> tuple[int, ...]:
        return self._dset.shape

    @property
    def dtype(self) -> np.dtype[_T]:
        return self._dset.dtype

    @property
    def ndim(self) -> int:
        return len(self.shape)

    @property
    def size(self) -> int:
        return int(np.prod(self.shape))

    @property
    @override
    def attributes(self) -> AttributeManager:
        return self._dset.attrs

    @property
    def flat(self) -> np.flatiter[npt.NDArray[_T]]:
        return np.array(self).flat

    @property
    def T(self) -> H5Array[_T]:
        return cast(H5Array[_T], np.transpose(self))  # pyright: ignore[reportInvalidCast]

    # endregion

    # region methods
    def _resize(self, amount: int, axis: int | tuple[int, ...] | None = None) -> None:
        if not self.flags.writeable:
            raise ValueError("assignment destination is read-only")

        if amount == 0:
            return

        if axis is None:
            axis = 0

        if isinstance(axis, int):
            self._dset.resize(self.shape[axis] + amount, axis=axis)

        else:
            self._dset.resize([s + amount if i in axis else s for i, s in enumerate(self.shape)])

    def expand(self, amount: int, axis: int | tuple[int, ...] | None = None) -> None:
        """
        Resize an H5Array by adding `amount` elements along the selected axis.

        Raises:
            TypeError: if the H5Array does not wrap a chunked Dataset.
        """
        self._resize(amount, axis)

    def contract(self, amount: int, axis: int | tuple[int, ...] | None = None) -> None:
        """
        Resize an H5Array by removing `amount` elements along the selected axis.

        Raises:
            TypeError: if the H5Array does not wrap a chunked Dataset.
        """
        self._resize(-amount, axis)

    @overload
    def astype(self, dtype: npt.DTypeLike, copy: Literal[True], inplace: bool = ...) -> npt.NDArray[Any]: ...
    @overload
    def astype(self, dtype: npt.DTypeLike, copy: Literal[False], inplace: bool = ...) -> H5Array[Any]: ...
    @overload
    def astype(
        self, dtype: npt.DTypeLike, copy: bool = False, inplace: bool = False
    ) -> npt.NDArray[Any] | H5Array[Any]: ...

    def astype(
        self, dtype: npt.DTypeLike, copy: bool = False, inplace: bool = False
    ) -> npt.NDArray[Any] | H5Array[Any]:
        """
        Cast an H5Array to a specified dtype.

        Args:
            dtype: data-type to which the array is cast.
            copy: if set to False, astype() does not perform a copy but returns a wrapper around the underlying H5 dataset
            inplace: perform the type casting and write the result to the hdf5 file.
        """
        if np.issubdtype(dtype, str) and (np.issubdtype(self._dset.dtype, str) or self._dset.dtype == object):
            new_dset = self._dset.asstr()

        else:
            new_dset = self._dset.astype(dtype)

        if inplace:
            file, name = self._dset.file, self._dset.name
            del file[name]

            # FIXME : conversion to np happens anyway but might be expensive, could we save data without conversion ?
            ch5mpy.io.write_dataset(np.array(new_dset), file, name, chunks=new_dset.chunks, maxshape=new_dset.maxshape)

            if file[name].dtype == object:
                self._dset = file[name].asstr()

            else:
                self._dset = file[name]

        if copy:
            return np.array(new_dset)
        return H5Array(new_dset)

    def maptype(self, otype: type[Any]) -> H5Array[Any]:
        """
        Cast an H5Array to any object type.
        This extends H5Array.astype() to any type <T>, where it is required that an object <T> can be constructed as
        T(v) for any value <v> in the dataset.
        """
        return H5Array(self._dset.maptype(otype))

    def iter_chunks(self, keepdims: bool = False) -> ChunkIterator:
        return ChunkIterator(self, keepdims)

    def iter_chunks_with(self, other: npt.NDArray[Any] | H5Array[Any], keepdims: bool = False) -> PairedChunkIterator:
        return PairedChunkIterator(self, other, keepdims)

    def read_direct(
        self,
        dest: npt.NDArray[_T],
        source_sel: tuple[int | slice, ...],
        dest_sel: tuple[int | slice, ...],
    ) -> None:
        dset = self._dset.asstr() if np.issubdtype(self.dtype, str) else self._dset
        dset.read_direct(dest, source_sel=source_sel, dest_sel=dest_sel)

    def overwrite(self, values: npt.NDArray[_T]) -> None:
        if not self.flags.writeable:
            raise ValueError("assignment destination is read-only")

        if not self.ndim == 1:
            raise NotImplementedError

        if not self.ndim == values.ndim:
            raise ValueError(f"Cannot overwrite {self.ndim}D H5Array with {values.ndim}D values")

        self.expand(len(values) - len(self))
        self[:] = values

    @override
    def copy(self) -> npt.NDArray[_T]:
        return np.copy(self)

    def min(self, axis: int | tuple[int, ...] | None = None) -> _T | npt.NDArray[_T]:
        return np.min(self, axis=axis)  # type: ignore[no-any-return]

    def max(self, axis: int | tuple[int, ...] | None = None) -> _T | npt.NDArray[_T]:
        return np.max(self, axis=axis)  # type: ignore[no-any-return]

    def mean(self, axis: int | tuple[int, ...] | None = None) -> Any | npt.NDArray[Any]:
        return np.mean(self, axis=axis)

    def sum(
        self, axis: int | tuple[int, ...] | None = None, out: npt.NDArray[Any] | None = None
    ) -> _T | npt.NDArray[_T]:
        return np.sum(self, axis=axis, out=out)

    def ravel(self, order: Literal["C", "F", "A", "K"] = "C") -> npt.NDArray[_T]:
        return np.ravel(self, order=order)

    def flatten(self, order: Literal["C", "F", "A", "K"] = "C") -> npt.NDArray[_T]:
        return np.array(self).flatten(order=order)

    def take(
        self,
        indices: _ArrayLikeInt_co,
        axis: SupportsIndex | None = None,
        mode: Literal["raise", "wrap", "clip"] = "raise",
    ) -> npt.NDArray[_T]:
        return np.take(self, indices, axis=axis, mode=mode)

    def item(self, *args: int) -> int | float:
        if args == () and self._dset.size != 1:
            raise ValueError("can only convert an H5Array of size 1 to a Python scalar")

        for a in args:
            assert isinstance(a, (int, np.integer))

        return as_python_scalar(cast(np.number[Any], self.__getitem__(args)))  # pyright: ignore[reportInvalidCast]

    def tolist(self) -> list[Any]:
        return cast(list[Any], self.copy().tolist())

    def view(self, dtype: npt.DTypeLike | None = None) -> H5ArrayView[_T]:
        if dtype is None:
            return self[:]

        return self.astype(dtype, copy=False)[:]

    # endregion
