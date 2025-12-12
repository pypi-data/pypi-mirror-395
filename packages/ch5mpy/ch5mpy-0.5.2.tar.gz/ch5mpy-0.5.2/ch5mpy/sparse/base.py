from abc import ABC, abstractmethod
from typing import Any, Self

from scipy.sparse._base import sparray

from ch5mpy import Group, H5Dict


class H5_sparse_array(ABC, sparray):  # type: ignore[misc]
    # region magic methods
    @abstractmethod
    def __init__(
        self,
        file: Group | H5Dict[Any],
    ):
        self.file: H5Dict[Any] = H5Dict(file)

    def __repr__(self) -> str:
        return str("<H5 " + super().__repr__()[1:])

    @classmethod
    def __h5_read__(cls, values: H5Dict[Any]) -> Self:
        return cls(values)

    @abstractmethod
    def __h5_write__(self, values: H5Dict[Any]) -> None: ...

    # endregion

    # region attributes
    @property
    def _shape(self) -> tuple[int, int]:
        return tuple(self.file.attributes["_shape"])

    @property
    def shape(self) -> tuple[int, int]:
        return self._shape

    @shape.setter
    def shape(self, value: tuple[int, int]) -> None:
        self.file.attributes.set(_shape=value)

    # endregion

    # region class methods
    @classmethod
    def read(cls, file: Group | H5Dict[Any]) -> Self:
        return cls(file)

    @classmethod
    @abstractmethod
    def write(cls, file: Group | H5Dict[Any], matrix: sparray) -> Self: ...

    # endregion
