from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, Self, runtime_checkable

if TYPE_CHECKING:
    from ch5mpy.dict import H5Dict


@runtime_checkable
class SupportsH5Write(Protocol):
    def __h5_write__(self, values: H5Dict[Any]) -> None: ...


@runtime_checkable
class SupportsH5Read(Protocol):
    @classmethod
    def __h5_read__(cls, values: H5Dict[Any]) -> Self: ...


class SupportsH5ReadWrite(Protocol):
    def __h5_write__(self, values: H5Dict[Any]) -> None: ...

    @classmethod
    def __h5_read__(cls, values: H5Dict[Any]) -> Self: ...
