from __future__ import annotations

import pickle
from typing import Any, cast, overload

import numpy as np
import numpy.typing as npt
from scipy.sparse import csr_array

from ch5mpy import Group
from ch5mpy.array import H5Array
from ch5mpy.dict import H5Dict
from ch5mpy.sparse._typing import INT_FLOAT
from ch5mpy.sparse.base import H5_sparse_array


class H5_csr_array(H5_sparse_array, csr_array):  # type: ignore[misc]
    """Compressed Sparse Row matrix created from hdf5 objects."""

    file: H5Dict[Any]
    data: H5Array[INT_FLOAT]
    indices: H5Array[np.integer[Any]]
    indptr: H5Array[np.integer[Any]]

    # region magic methods
    @overload
    def __new__(cls, arg1: Group | H5Dict[Any], *args: Any, **kwargs: Any) -> H5_csr_array: ...
    @overload
    def __new__(cls, arg1: tuple[int, int], *args: Any, **kwargs: Any) -> csr_array: ...
    def __new__(cls, arg1: Any, *args: Any, **kwargs: Any) -> csr_array:
        if not isinstance(arg1, (Group, H5Dict)):
            return csr_array(arg1, *args, **kwargs)

        return super(H5_csr_array, cls).__new__(cls)

    def __init__(
        self,
        file: Group | H5Dict[Any],
    ):
        super().__init__(file)

        self.data = self.file["data"]
        self.indices = self.file["indices"]
        self.indptr = self.file["indptr"]

    def __h5_write__(self, values: H5Dict[Any]) -> None:
        values["data"] = self.data
        values["indices"] = self.indices
        values["indptr"] = self.indptr

        values.attributes["_shape"] = self.shape

    # endregion

    # region class methods
    @classmethod
    def write(cls, file: Group | H5Dict[Any], matrix: csr_array) -> H5_csr_array:
        file = H5Dict(file)

        file["data"] = matrix.data
        file["indices"] = matrix.indices
        file["indptr"] = matrix.indptr

        file.attributes.set(
            _shape=matrix.shape,
            __h5_type__="object",
            __h5_class__=np.void(pickle.dumps(H5_csr_array, protocol=pickle.HIGHEST_PROTOCOL)),
        )

        return H5_csr_array(file)

    # endregion

    # region methods
    def _insert_many(
        self, i: npt.NDArray[np.integer[Any]], j: npt.NDArray[np.integer[Any]], x: npt.NDArray[INT_FLOAT]
    ) -> None:
        """Inserts new nonzero at each (i, j) with value x

        Here (i,j) index major and minor respectively.
        i, j and x must be non-empty, 1d arrays.
        Inserts each major group (e.g. all entries per row) at a time.
        Maintains has_sorted_indices property.
        """
        if self.has_sorted_indices:
            # convert i and j indices to a single ij array of complex values so that when we sort ij, i is used as
            # primary key and j as secondary
            sorted_indices = np.argsort(i + 1j * j)
            i = i[sorted_indices]
            j = j[sorted_indices]
            x = x[sorted_indices]

            ui, ui_idx = np.unique(i, return_index=True)

            split_indices = np.split(self.indices, cast(H5Array[np.int64], self.indptr[1:-1]))
            split_j = np.split(j, ui_idx[1:])

            indptr_diff = np.zeros(max(ui[-1] + 1, len(self.indptr) - 1), dtype=np.int64)
            indptr_diff[: len(self.indptr) - 1] = np.diff(self.indptr)
            n_items_before_line = np.r_[0, np.cumsum(indptr_diff)]

            def searchsorted(ix: int, jx: npt.NDArray[np.int64]) -> npt.NDArray[np.int64]:
                indices = np.searchsorted(split_indices[ix], jx) if ix < len(split_indices) else np.arange(len(jx))
                return cast(npt.NDArray[np.int64], indices + n_items_before_line[ix])

            insert_indices = np.concatenate([searchsorted(ix, jx) for ix, jx in zip(ui, split_j)])

            np.insert(self.data, insert_indices, x)
            np.insert(self.indices, insert_indices, j)

            indptr_diff[ui] += [len(s) for s in split_j]
            self.indptr.overwrite(np.cumsum(np.r_[0, indptr_diff]))

            self.shape = (max(self.shape[0], len(self.indptr) - 1)), max(self.shape[1], np.max(self.indices))

        else:
            raise NotImplementedError

    # endregion
