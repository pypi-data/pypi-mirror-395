from __future__ import annotations

from collections.abc import Collection, Iterable, Iterator
from itertools import zip_longest
from pathlib import Path
from typing import Any, Generic, TypeVar, cast, override

import numpy as np

from ch5mpy.array import H5Array
from ch5mpy.dict import H5Dict
from ch5mpy.functions.types import AnonymousArrayCreationFunc
from ch5mpy.io import read_object, write_object, write_objects
from ch5mpy.names import H5Mode
from ch5mpy.objects import File, Group, H5Object
from ch5mpy.types import SupportsH5ReadWrite

_T = TypeVar("_T", bound=SupportsH5ReadWrite | H5Array[Any])


def _get_group(file: File | Group, name: str) -> tuple[File | Group, str]:
    lst = name.rsplit("/", 1)

    if len(lst) == 1:
        return file, lst[0]

    return file.require_group(lst[0]), lst[1]


def deferred_H5List(values: Collection[Any]) -> AnonymousArrayCreationFunc:
    def inner(name: str, loc: str | Path | File | Group) -> None:
        H5List.write(list(values), loc, name)

    return inner


class H5List(H5Object, Generic[_T]):
    """Class for managing lists backed on h5 files."""

    # region magic methods
    def __init__(self, file: File | Group):
        super().__init__(file)
        self._iter_index: int = 0

    @override
    def __repr__(self) -> str:
        if self.is_closed:
            return "Closed H5List[...]"

        if len(self) > 6:
            return f"H5List[{self[0]}, {self[1]}, {self[2]}, ..., {self[-3]}, {self[-2]}, {self[-1]}]"

        return f"H5List[{', '.join([str(e) if isinstance(e, np.generic) else repr(e) for e in self])}]"

    def __len__(self) -> int:
        return len(self._file.keys())

    def __getitem__(self, item: int) -> _T:
        if item < 0:
            item = len(self) + item

        return cast(_T, read_object(self._file[str(item)]))

    def __iter__(self) -> Iterator[_T]:
        self._iter_index = 0
        return self

    def __next__(self) -> _T:
        if self._iter_index >= len(self):
            raise StopIteration

        obj = cast(_T, read_object(self._file[str(self._iter_index)]))
        self._iter_index += 1

        return obj

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Iterable):
            return False

        for self_i, other_i in zip_longest(self, other):
            if self_i != other_i:
                return False

        return True

    def __delitem__(self, key: int) -> None:
        if key < 0:
            key = len(self) + key

        del self._file[str(key)]

        for old_key in range(key + 1, len(self) + 1):
            self._file.move(str(old_key), str(old_key - 1))

    # endregion

    # region class methods
    @classmethod
    @override
    def read(cls, path: str | Path | File | Group, name: str = "", mode: H5Mode = H5Mode.READ) -> H5List[Any]:
        if isinstance(path, (str, Path)):
            path = File(path, mode=mode)

        src = path[name]

        if not isinstance(src, Group):
            raise ValueError(f"Cannot read H5List from '{type(src)}' object, should be a 'Group'.")

        src_type = src.attrs.get("__h5_type__", "")

        if src_type != "list":
            raise ValueError(f"Cannot read H5List from Group marked as type '{src_type}', should be 'list'.")

        return H5List(src)

    @classmethod
    def write(cls, lst: list[Any], path: str | Path | File | Group, name: str) -> H5List[Any]:
        """
        Write a list to a .h5 file as a H5List.

        Args:
            lst: a list to write.
            path: Either a path to the .h5 file or an open ch5mpy.File or
                ch5mpy.Group object.
            name: The group member name inside the .h5 file to use.
        """
        if isinstance(path, (str, Path)):
            path = File(path, mode=H5Mode.READ_WRITE)

        if path.file.mode == H5Mode.READ:
            raise ValueError("Cannot write to h5 file open in 'r' mode.")

        dest, group_name = _get_group(path, name)

        if group_name in dest.keys():
            raise ValueError(f"An object with name '{group_name}' already exists.")

        dest = dest.create_group(group_name)
        dest.attrs["__h5_type__"] = "list"

        write_objects(
            dest,
            chunks=True,
            maxshape=None,
            overwrite=False,
            progress=None,
            **dict(map(lambda x: (str(x[0]), x[1]), enumerate(lst))),
        )

        return H5List(dest)

    @classmethod
    def defer(cls, values: Collection[Any] = ()) -> AnonymousArrayCreationFunc:
        return deferred_H5List(values)

    # endregion

    # region methods
    @override
    def copy(self) -> Any:
        return [e for e in self]

    def to_dict(self) -> H5Dict[_T]:
        return H5Dict(self._file)

    def append(self, value: Any) -> None:
        write_object(value, self._file, str(len(self)), chunks=True)

    # endregion
