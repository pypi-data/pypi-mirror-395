from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from ch5mpy.names import H5Mode
from ch5mpy.objects.group import File, Group

if TYPE_CHECKING:
    from ch5mpy.attributes import AttributeManager


class H5Object(ABC):
    """Base class for H5 objects."""

    # region magic methods
    def __init__(self, file: File | Group):
        assert isinstance(file, (File, Group))

        self._file = file

    # endregion

    # region class methods
    @classmethod
    @abstractmethod
    def read(cls, path: str | Path | File | Group, name: str = "", mode: H5Mode = H5Mode.READ) -> H5Object:
        """
        Read an H5 object from a file.

        Args:
            path: Either a path to the .h5 file or an open ch5mpy.File or
                ch5mpy.Group object.
            name: The group member name inside the .h5 file to use.
            mode: The mode for opening the .h5 file if not already open.
        """
        pass

    # endregion

    # region attributes
    @property
    def file(self) -> Group:
        return self._file

    @property
    def filename(self) -> str:
        return self._file.file.filename

    @property
    def mode(self) -> Literal[H5Mode.READ, H5Mode.READ_WRITE]:
        return self._file.file.mode

    @property
    def attributes(self) -> AttributeManager:
        return self._file.attrs

    # endregion

    # region predicates
    @property
    def is_closed(self) -> bool:
        """Is the file (this H5 object wraps) closed ?"""
        return not self._file.id.valid

    # endregion

    # region methods
    def close(self) -> None:
        """Close the file this H5 object wraps."""
        self._file.file.close()

    @abstractmethod
    def copy(self) -> Any:
        """Build an in-memory copy of this H5 object."""
        pass

    # endregion
