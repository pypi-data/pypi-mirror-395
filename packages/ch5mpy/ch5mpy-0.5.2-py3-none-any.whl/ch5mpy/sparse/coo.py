from __future__ import annotations

import pickle
from typing import Any, cast, overload

import numpy as np
from scipy.sparse import coo_array

from ch5mpy import Group, H5Array, H5Dict, H5List
from ch5mpy.sparse._typing import INT_FLOAT
from ch5mpy.sparse.base import H5_sparse_array


class H5_coo_array(H5_sparse_array, coo_array):  # type: ignore[misc]
    """A sparse matrix in COOrdinate format created from hdf5 objects."""

    file: H5Dict[Any]
    coords: H5List[H5Array[np.integer[Any]]]
    data: H5Array[INT_FLOAT]

    # region magic methods
    @overload
    def __new__(cls, arg1: Group | H5Dict[Any], *args: Any, **kwargs: Any) -> H5_coo_array: ...
    @overload
    def __new__(cls, arg1: tuple[int, int], *args: Any, **kwargs: Any) -> coo_array: ...
    def __new__(cls, arg1: Any, *args: Any, **kwargs: Any) -> coo_array:
        if not isinstance(arg1, (Group, H5Dict)):
            return coo_array(arg1, *args, **kwargs)

        return super(H5_coo_array, cls).__new__(cls)

    def __init__(
        self,
        file: Group | H5Dict[Any],
    ):
        super().__init__(file)

        self.coords = self.file["coords"]
        self.data = self.file["data"]

    def __h5_write__(self, values: H5Dict[Any]) -> None:
        values["data"] = self.data
        values["coords"] = self.coords

    # endregion

    # region predicates
    @property
    def has_canonical_format(self) -> bool:
        return cast(bool, self.file.attrs["has_canonical_format"])

    # endregion

    # region class methods
    @classmethod
    def write(cls, file: Group | H5Dict[Any], matrix: coo_array) -> H5_coo_array:
        file = H5Dict(file)

        file["coords"] = matrix.coords
        file["data"] = matrix.data

        file.attributes.set(
            _shape=matrix._shape,
            has_canonical_format=matrix.has_canonical_format,
            __h5_type__="object",
            __h5_class__=np.void(pickle.dumps(H5_coo_array, protocol=pickle.HIGHEST_PROTOCOL)),
        )

        return H5_coo_array(file)

    # endregion
