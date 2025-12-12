from __future__ import annotations

from typing import Any, Literal, TypeVar, cast, overload

import numpy as np
import numpy.typing as npt

import ch5mpy
import ch5mpy.indexing as ci
from ch5mpy import Dataset
from ch5mpy._typing import NP_FUNC, ONE_AXIS_SELECTOR, SELECTOR
from ch5mpy.array.array import as_array
from ch5mpy.array.flags import FlagDict
from ch5mpy.array.io import read_from_dataset, read_one_from_dataset, write_to_dataset
from ch5mpy.objects import DatasetWrapper

_T = TypeVar("_T", bound=np.generic, covariant=True)


class H5ArrayView(ch5mpy.H5Array[_T]):
    """A view on a H5Array."""

    # region magic methods
    def __init__(self, dset: Dataset[_T] | DatasetWrapper[_T], sel: ci.Selection, flags: FlagDict):
        super().__init__(dset)
        self._selection = sel
        self.flags = flags

    @overload
    def __getitem__(self, index: tuple[()]) -> ch5mpy.H5Array[_T]: ...  # type: ignore
    @overload
    def __getitem__(self, index: tuple[ONE_AXIS_SELECTOR, ONE_AXIS_SELECTOR, ONE_AXIS_SELECTOR]) -> _T: ...  # type: ignore
    @overload
    def __getitem__(self, index: SELECTOR | tuple[SELECTOR, ...]) -> H5ArrayView[_T]: ...
    def __getitem__(  # pyright: ignore[reportInconsistentOverload]
        self, index: tuple[()] | SELECTOR | tuple[SELECTOR, ...]
    ) -> _T | ch5mpy.H5Array[_T] | H5ArrayView[_T]:  # pyright: ignore[reportInconsistentOverload]
        selection = ci.Selection.from_selector(index, self.shape)

        if selection.is_empty:
            return H5ArrayView(dset=self._dset, sel=self._selection, flags=self.flags)

        selection = selection.cast_on(self._selection)

        if selection.is_empty:
            return ch5mpy.H5Array(self._dset)

        if selection.out_shape == ():
            return read_one_from_dataset(self._dset, selection, self.dtype)

        return H5ArrayView(dset=self._dset, sel=selection, flags=self.flags)

    def __setitem__(self, index: SELECTOR | tuple[SELECTOR, ...], value: Any) -> None:
        selection = ci.Selection.from_selector(index, self.shape)
        write_to_dataset(self._dset, as_array(value, self.dtype), selection.cast_on(self._selection))

    def __len__(self) -> int:
        return self.shape[0]

    def _inplace(self, func: NP_FUNC, value: Any) -> H5ArrayView[_T]:
        if np.issubdtype(self.dtype, str):
            raise TypeError("Cannot perform inplace operation on str H5Array.")

        # special case : 0D array
        if self.shape == ():
            self._dset[:] = func(self._dset[:], value)
            return self

        # general case : 1D+ array
        for index, chunk in self.iter_chunks():
            func(chunk, value, out=chunk)

            for dest_sel, _, source_sel in ci.Selection(index, self.shape).cast_on(self._selection).iter_indexers():
                self._dset.write_direct(chunk, source_sel=source_sel, dest_sel=dest_sel)

        return self

    # endregion

    # region interface
    def __array__(self, dtype: npt.DTypeLike | None = None, copy: bool | None = True) -> npt.NDArray[Any]:
        loading_array = np.empty(
            self._selection.out_shape,
            dtype or self.dtype,
        )
        read_from_dataset(self._dset, self._selection, loading_array)

        return loading_array.reshape(self.shape)

    # endregion

    # region attributes
    @property
    def shape(self) -> tuple[int, ...]:
        return self._selection.out_shape

    # endregion

    # region methods
    @overload
    def astype(self, dtype: npt.DTypeLike, copy: Literal[True], inplace: bool = ...) -> npt.NDArray[Any]: ...
    @overload
    def astype(self, dtype: npt.DTypeLike, copy: Literal[False] = False, inplace: bool = ...) -> H5ArrayView[Any]: ...
    @overload
    def astype(
        self, dtype: npt.DTypeLike, copy: bool = False, inplace: bool = ...
    ) -> npt.NDArray[Any] | H5ArrayView[Any]: ...

    def astype(
        self, dtype: npt.DTypeLike, copy: bool = False, inplace: bool = False
    ) -> npt.NDArray[Any] | H5ArrayView[Any]:
        """
        Cast an H5Array to a specified dtype.
        This does not perform a copy, it returns a wrapper around the underlying H5 dataset.
        """
        if inplace:
            raise TypeError("Cannot cast inplace a view of an H5Array.")

        if np.issubdtype(dtype, str) and (np.issubdtype(self._dset.dtype, str) or self._dset.dtype == object):
            casted_view = H5ArrayView(self._dset.asstr(), sel=self._selection, flags=self.flags)

        else:
            casted_view = H5ArrayView(self._dset.astype(dtype), sel=self._selection, flags=self.flags)

        if copy:
            return np.array(casted_view)
        return casted_view

    def maptype(self, otype: type[Any]) -> H5ArrayView[Any]:
        """
        Cast an H5Array to any object type.
        This extends H5Array.astype() to any type <T>, where it is required that an object <T> can be constructed as
        T(v) for any value <v> in the dataset.
        """
        return H5ArrayView(self._dset.maptype(otype), sel=self._selection, flags=self.flags)

    def read_direct(
        self,
        dest: npt.NDArray[_T],
        source_sel: tuple[int | slice, ...],
        dest_sel: tuple[int | slice, ...],
    ) -> None:
        if isinstance(self._dset, Dataset) and np.issubdtype(self.dtype, str):
            dataset: Dataset[_T] | DatasetWrapper[_T] = cast(DatasetWrapper[_T], self._dset.asstr())
        else:
            dataset = self._dset

        read_from_dataset(
            dataset,
            ci.Selection(
                (ci.as_indexer(sl, max=axis_shape) for sl, axis_shape in zip(source_sel, self.shape)),
                shape=self.shape,
            ).cast_on(self._selection),
            dest[dest_sel],
        )

    # endregion
