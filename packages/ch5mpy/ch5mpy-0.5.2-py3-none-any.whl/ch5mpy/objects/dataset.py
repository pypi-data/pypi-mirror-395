from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Collection
from typing import Any, Generic, Literal, TypeVar, cast, override

import h5py
import numpy as np
import numpy.typing as npt
from h5py.h5t import check_string_dtype
from numpy._typing import _ArrayLikeInt_co  # pyright: ignore[reportPrivateUsage]

import ch5mpy
from ch5mpy._typing import SELECTOR
from ch5mpy.attributes import AttributeManager
from ch5mpy.objects.pickle import PickleableH5Object
from ch5mpy.utils import NAN_PACKED

_T = TypeVar("_T", bound=np.generic)
_WT = TypeVar("_WT", bound=np.generic, covariant=True)
ENCODING = Literal["ascii", "utf-8"]
ERROR_METHOD = Literal[
    "backslashreplace",
    "ignore",
    "namereplace",
    "strict",
    "replace",
    "xmlcharrefreplace",
]


class DatasetWrapper(ABC, Generic[_WT]):
    """Base class to wrap Datasets."""

    # region magic methods
    def __init__(self, dset: Dataset[Any]):
        self._dset: Dataset[Any] = dset

    @abstractmethod
    def __getitem__(self, item: SELECTOR | tuple[SELECTOR, ...]) -> Any:
        pass

    def __setitem__(self, item: SELECTOR, value: Any) -> None:
        raise NotImplementedError

    def __getattr__(self, attr: str) -> Any:
        # If method/attribute is not defined here, pass the call to the wrapped dataset.
        return getattr(self._dset, attr)

    def __len__(self) -> int:
        return len(self._dset)

    # endregion

    # region numpy interface
    def __array__(self, dtype: npt.DTypeLike | None = None, copy: bool | None = True) -> npt.NDArray[Any]:
        if dtype is None:
            return np.array(self[()])

        return np.array(self[()]).astype(dtype)

    # endregion

    # region attributes
    @property
    @abstractmethod
    def dtype(self) -> np.dtype[Any]:
        pass

    @property
    def size(self) -> int:
        return self._dset.size

    @property
    def attrs(self) -> AttributeManager:
        return self._dset.attrs

    # endregion

    # region methods
    def read_direct(
        self,
        dest: npt.NDArray[Any],
        source_sel: tuple[int | slice | Collection[int], ...] | None = None,
        dest_sel: tuple[int | slice | Collection[int], ...] | None = None,
        expand_sel: _ArrayLikeInt_co | slice | None = None,
    ) -> None:
        source_sel = () if source_sel is None else source_sel
        dest_sel = () if dest_sel is None else dest_sel

        if expand_sel is None or isinstance(expand_sel, slice) and expand_sel == slice(None):
            dest[dest_sel] = self[source_sel]
        else:
            dest[dest_sel] = np.atleast_1d(self[source_sel])[expand_sel]

    # endregion


class AsStrWrapper(DatasetWrapper[np.str_]):
    """Wrapper to decode strings on reading the dataset"""

    # region magic methods
    @override
    def __getitem__(self, args: SELECTOR | tuple[SELECTOR, ...]) -> npt.NDArray[np.str_] | np.str_:
        subset = self._dset[args]

        if isinstance(subset, bytes):
            if subset == NAN_PACKED:
                return np.str_("nan")
            return np.str_(subset.decode())

        subset[np.where(subset == NAN_PACKED)] = b"nan"
        return np.array(subset, dtype=str)

    @override
    def __repr__(self) -> str:
        dset_name = "anonymous" if self._dset.name is None else self._dset.name[1:]
        return f'<HDF5 AsStrWrapper "{dset_name}": shape {self._dset.shape}">'

    # endregion

    # region attributes
    @property
    @override
    def dtype(self) -> np.dtype[np.str_]:
        str_dset = self._dset.asstr()[:]

        if isinstance(str_dset, np.ndarray):
            return str_dset.dtype

        return np.dtype(f"<U{len(str_dset)}")

    # endregion


class AsDtypeWrapper(DatasetWrapper[_WT]):
    """Wrapper to cast elements in a dataset as another numpy dtype."""

    # region magic methods
    def __init__(self, dset: Dataset[Any], dtype: npt.DTypeLike):
        super().__init__(dset)
        self._dtype: np.dtype[Any] = np.dtype(dtype)

    @override
    def __repr__(self) -> str:
        return f'<HDF5 AsDtypeWrapper "{self._dset.name[1:]}": shape {self._dset.shape}, dtype "{self._dtype}">'

    @override
    def __getitem__(self, args: SELECTOR | tuple[SELECTOR, ...]) -> npt.NDArray[Any] | Any:
        subset = self._dset[args]

        if np.isscalar(subset):
            return self._dtype.type(subset)  # type: ignore[arg-type]

        return np.array(subset, dtype=self._dtype)

    # endregion

    # region attributes
    @property
    @override
    def dtype(self) -> np.dtype[Any]:
        if np.issubdtype(self._dtype, str):
            # special case of str casting (todo: should find a better way of finding out the dtype)
            return self._dset[:].astype(str).dtype

        return self._dtype

    # endregion


class AsObjectWrapper(DatasetWrapper[_WT]):
    """Wrapper to map any object type to elements in a dataset."""

    # region magic methods
    def __init__(self, dset: Dataset[Any], otype: type[_WT]):
        super().__init__(dset)
        self._otype: type[_WT] = otype

    @override
    def __repr__(self) -> str:
        return (
            f'<HDF5 AsObjectWrapper "{self._dset.name[1:]}": shape {self._dset.shape}, otype "{self._otype.__name__}">'
        )

    @override
    def __getitem__(self, args: SELECTOR | tuple[SELECTOR, ...]) -> npt.NDArray[np.object_] | _WT:
        subset = self._dset[args]

        if np.isscalar(subset):
            return self._otype(subset)

        subset = cast(npt.NDArray[Any], subset)
        return np.array(list(map(self._otype, subset.flat)), dtype=np.object_).reshape(subset.shape)

    # endregion

    # region attributes
    @property
    @override
    def dtype(self) -> np.dtype[np.object_]:
        return np.dtype("O")

    @property
    def otype(self) -> type[_WT]:
        return self._otype

    # endregion


class Dataset(PickleableH5Object, h5py.Dataset, Generic[_T]):
    """A subclass of h5py.Dataset that implements pickling."""

    # region magic methods
    @override
    def __getitem__(
        self,
        arg: SELECTOR | tuple[SELECTOR, ...],
        new_dtype: npt.DTypeLike | None = None,
    ) -> _T | npt.NDArray[_T]:
        return super().__getitem__(arg, new_dtype)  # type: ignore[no-any-return]

    @override
    def __setitem__(self, arg: SELECTOR | tuple[SELECTOR, ...], val: Any) -> None:
        super().__setitem__(arg, val)

    # endregion

    # region attributes
    @property
    @override
    def file(self) -> ch5mpy.File:
        with h5py._objects.phil:  # type: ignore[attr-defined]
            return ch5mpy.File(self.id)

    @property
    def attributes(self) -> AttributeManager:
        return self.file.attrs

    @property
    @override
    def dtype(self) -> np.dtype[_T]:
        return self.id.dtype  # type: ignore[return-value]

    @property
    @override
    def attrs(self) -> AttributeManager:  # type: ignore[override]
        return AttributeManager(super().attrs)

    # endregion

    # region methods
    def asstr(self, encoding: ENCODING | None = None, errors: ERROR_METHOD = "strict") -> AsStrWrapper:  # type: ignore[override]
        """
        Get a wrapper to read string data as Python strings:

        The parameters have the same meaning as in `bytes.decode()`.
        If `encoding` is unspecified, it will use the encoding in the HDF5
        datatype (either ascii or utf-8).
        """
        string_info = check_string_dtype(self.dtype)
        if string_info is None:
            raise TypeError("dset.asstr() can only be used on datasets with an HDF5 string datatype")

        self_ = cast(Dataset[np.bytes_], self)
        return AsStrWrapper(self_)

    @override
    def astype(self, dtype: npt.DTypeLike) -> AsDtypeWrapper[np.generic]:  # type: ignore[override]
        return AsDtypeWrapper(self, dtype)

    def maptype(self, otype: type[Any]) -> AsObjectWrapper[Any]:
        # noinspection PyTypeChecker
        return AsObjectWrapper(self, otype)

    @override
    def read_direct(
        self,
        dest: npt.NDArray[Any],
        source_sel: tuple[int | slice | Collection[int], ...] | None = None,
        dest_sel: tuple[int | slice | Collection[int], ...] | None = None,
        expand_sel: _ArrayLikeInt_co | slice | None = None,
    ) -> None:
        # FIXME: find better way (here we have to load data to RAM before writing to dest)
        source_sel = () if source_sel is None else source_sel
        dest_sel = () if dest_sel is None else dest_sel

        if expand_sel is None or isinstance(expand_sel, slice) and expand_sel == slice(None):
            dest[dest_sel] = self[source_sel]
        else:
            dest[dest_sel] = np.atleast_1d(self[source_sel])[expand_sel]

    @override
    def write_direct(
        self,
        source: npt.NDArray[Any],
        source_sel: tuple[int | slice | Collection[int] | None, ...] | None = None,
        dest_sel: tuple[int | slice | Collection[int] | None, ...] | None = None,
    ) -> None:
        if not source.flags.carray:
            # ensure 'C' memory layout
            source = source.copy()

        if is_empty_selection(dest_sel):
            # empty selection : skip write operation
            return

        super().write_direct(handle_nan(source, self.dtype), source_sel=source_sel, dest_sel=dest_sel)

    # endregion


def is_empty_selection(sel: tuple[int | slice | Collection[int] | None, ...] | None) -> bool:
    if sel is None:
        return False

    if isinstance(sel, tuple) and len(sel) == 0:
        return False

    return not any(sel_len(s) for s in sel)


def sel_len(sel: int | slice | Collection[int] | None) -> int:
    if sel is None or isinstance(sel, (int, np.integer, slice)):
        return 1

    return len(sel)


def handle_nan(source: npt.NDArray[Any], dest_dtype: np.dtype[Any]) -> npt.NDArray[Any]:
    if np.issubdtype(dest_dtype, np.integer):
        if source.dtype.kind in "fc" and np.any(np.isnan(source)):
            raise ValueError("cannot convert float NaN to integer")

    if np.issubdtype(dest_dtype, np.object_):
        if source.ndim == 0:
            if source[()] is np.nan:
                return np.array(NAN_PACKED, dtype=object)

        else:
            is_nan = np.array([e is np.nan for e in source.ravel()], dtype=bool).reshape(source.shape)
            source[is_nan] = NAN_PACKED
            return source

    return source
