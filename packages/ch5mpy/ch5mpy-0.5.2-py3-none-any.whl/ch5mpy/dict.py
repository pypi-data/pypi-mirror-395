from __future__ import annotations

from collections.abc import Iterable, KeysView, MutableMapping
from itertools import islice
from pathlib import Path
from types import TracebackType
from typing import Any, ItemsView, Iterator, TypeVar, Union, ValuesView, cast

import numpy as np
from h5py._hl.base import ItemsViewHDF5

from ch5mpy.array import H5Array
from ch5mpy.names import H5Mode
from ch5mpy.objects import AsStrWrapper, Dataset, File, Group, H5Object
from ch5mpy.options import _OPTIONS
from ch5mpy.types import SupportsH5ReadWrite

from . import io

_T = TypeVar("_T", bound=SupportsH5ReadWrite | H5Array[Any])

_NO_OBJECT = object()


def _get_in_memory(value: Any) -> Any:
    if isinstance(value, H5Dict):
        return value.copy()

    elif isinstance(value, (Dataset, AsStrWrapper)):
        return value[()]

    elif isinstance(value, (H5Object, H5Array)):
        return value.copy()

    return value


def _is_group(obj: Group | Dataset[Any]) -> bool:
    h5_type = obj.attrs.get("__h5_type__", "<UNKNOWN>")
    return isinstance(obj, Group) and h5_type not in ("object", "list")


def _get_group_repr(obj: Group | Dataset[Any]) -> str:
    return "{...}" if len(obj) else "{}"


def _get_repr(items: ItemsViewHDF5[str, Group | Dataset[Any]]) -> str:
    if not len(items):
        return "{}"

    if len(items) > 100:
        return (
            "{\n\t"
            + ",\n\t".join(
                [
                    f"{k}: "
                    + (
                        _get_group_repr(v)
                        if _is_group(v)
                        else repr(io.read_object(v, error="ignore")).replace("\n", "\n\t")
                    )
                    for k, v in islice(items, 0, 10)
                ]
            )
            + ",\n\t...,\n\t"
            + ",\n\t".join(
                [
                    f"{k}: "
                    + (
                        _get_group_repr(v)
                        if _is_group(v)
                        else repr(io.read_object(v, error="ignore")).replace("\n", "\n\t")
                    )
                    for k, v in islice(items, len(items) - 10, None)
                ]
            )
            + "}"
        )

    return (
        "{\n\t"
        + ",\n\t".join(
            [
                f"{k}: "
                + (
                    _get_group_repr(v)
                    if _is_group(v)
                    else repr(io.read_object(v, error="ignore")).replace("\n", "\n\t")
                )
                for k, v in items
            ]
        )
        + "\n}"
    )


def _get_note(annotation: str | None) -> str:
    return "" if annotation is None else f"[{annotation}]"


class H5DictValuesView(ValuesView[_T]):
    """Class for iterating over values in an H5Dict."""

    # region magic methods
    def __repr__(self) -> str:
        return f"{type(self).__name__}([{len(self)} values])"

    def __iter__(self) -> Iterator[_T]:
        return (
            io.read_object(v, error=_OPTIONS["error_mode"])
            for v in cast(Iterator[Union[Group, Dataset[Any]]], super().__iter__())
        )

    # endregion


class H5DictItemsView(ItemsView[str, _T]):
    """Class for iterating over items in an H5Dict."""

    # region magic methods
    def __repr__(self) -> str:
        return f"{type(self).__name__}([{len(self)} items])"

    def __iter__(self) -> Iterator[tuple[str, _T]]:
        return (
            (k, io.read_object(v, error=_OPTIONS["error_mode"]))
            for k, v in cast(Iterator[tuple[str, Union[Group, Dataset[Any]]]], super().__iter__())
        )

    # endregion


def _diff(a: Any, b: Any) -> bool:
    if a is _NO_OBJECT:
        return True

    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        if a.shape != b.shape:
            return True

    try:
        return bool(np.array(a != b).any())

    except Exception:
        return False


class H5Dict(H5Object, MutableMapping[str, _T]):
    """Class for managing dictionaries backed on h5 files."""

    # region magic methods
    def __init__(self, file: File | Group | H5Dict[Any], annotation: str | None = None):
        if isinstance(file, H5Dict):
            file = file.file

        super().__init__(file)
        self.annotation = annotation

    def __dir__(self) -> Iterable[str]:
        return dir(H5Dict) + list(self.keys())

    def __repr__(self) -> str:
        if self.is_closed:
            return "Closed H5Dict{}"

        return f"H5Dict{_get_note(self.annotation)}{_get_repr(self._file.items())}"

    def __getitem__(self, key: str) -> _T:
        return cast(_T, io.read_object(self._file[key], error=_OPTIONS["error_mode"]))

    def __matmul__(self, key: str) -> H5Dict[_T]:
        return io.read_object(  # type: ignore[no-any-return]
            self._file[key], error=_OPTIONS["error_mode"], read_object=False
        )

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        value_is_empty_dict = isinstance(value, dict) and value == {}

        if isinstance(value, (dict, H5Dict)) and key in self._file.keys() and isinstance(sub_dict := self[key], H5Dict):
            for self_key in sub_dict.keys():
                if self_key not in value.keys():
                    del sub_dict[self_key]

            for sub_key, sub_value in value.items():
                sub_dict[sub_key] = sub_value

        elif value_is_empty_dict or _diff(self.get(key, _NO_OBJECT), value):
            io.write_object(value, self, key, overwrite=True)

    def __delitem__(self, key: str) -> None:
        del self._file[key]

    def __getattr__(self, item: str) -> _T:
        if item not in self._file.keys():
            raise AttributeError

        return self.__getitem__(item)

    def __len__(self) -> int:
        return len(self._file.keys())

    def __iter__(self) -> Iterator[str]:
        return iter(self.keys())

    def __deepcopy__(self, _memo: dict[Any, Any]) -> dict[str, Any]:
        return self.copy()

    def __enter__(self) -> H5Dict[_T]:
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def __ior__(self, other: object) -> H5Dict[_T]:
        if not isinstance(other, dict):
            raise NotImplementedError

        for key, value in other.items():
            if key in self.keys():
                target = self[key]
                if isinstance(value, (dict, H5Dict)):
                    if isinstance(target, H5Dict):
                        target |= value
                        continue

                    else:
                        del self[key]

            self[key] = value

        return self

    # endregion

    # region
    @property
    def parent(self) -> H5Dict[_T] | None:
        if isinstance(self._file, File):
            return None
        return H5Dict(self._file.parent)

    # endregion

    # region class methods
    @classmethod
    def read(
        cls,
        path: str | Path | File | Group,
        name: str | None = None,
        mode: H5Mode = H5Mode.READ,
    ) -> H5Dict[Any]:
        file = File(Path(path).expanduser(), mode=mode) if isinstance(path, (str, Path)) else path

        if name is not None:
            file = file[name]

        return H5Dict(file)

    # endregion

    # region methods
    def keys(self) -> KeysView[str]:
        return self._file.keys()

    def values(self) -> H5DictValuesView[_T]:
        return H5DictValuesView(self._file)  # type: ignore[arg-type]

    def items(self) -> H5DictItemsView[_T]:
        return H5DictItemsView(self._file)  # type: ignore[arg-type]

    def get(self, key: str, default: Any = None) -> Any:
        res = self._file.get(key, default)

        if res is default:
            return default
        return io.read_object(res, error=_OPTIONS["error_mode"])

    def rename(self, name: str, new_name: str) -> None:
        if new_name.startswith(name):
            self._file.move(name, "__h5_TMP__")
            name = "__h5_TMP__"

        self._file.move(name, new_name)

    def copy(self) -> dict[str, Any]:
        """
        Build an in-memory copy of this H5Dict object.
        """
        return {k: _get_in_memory(v) for k, v in self.items()}

    # endregion
