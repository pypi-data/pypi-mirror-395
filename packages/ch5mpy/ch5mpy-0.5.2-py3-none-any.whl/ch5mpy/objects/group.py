from __future__ import annotations

from typing import Any, Collection, Literal, cast

import h5py
import numpy.typing as npt
from h5py._hl.base import ItemsViewHDF5, ValuesViewHDF5

from ch5mpy.attributes import AttributeManager
from ch5mpy.names import H5Mode
from ch5mpy.objects.dataset import Dataset
from ch5mpy.objects.pickle import PickleableH5Object


def _h5py_wrap_type(obj: Any) -> Any:
    """Produce our objects instead of h5py default objects"""
    if isinstance(obj, h5py.Dataset):
        return Dataset(obj.id)
    elif isinstance(obj, h5py.File):
        return File(obj.id)
    elif isinstance(obj, h5py.Group):
        return Group(obj.id)
    elif isinstance(obj, h5py.Datatype):
        return obj  # Not supported for pickling yet. Haven't really thought about it
    else:
        return obj  # Just return, since we want to wrap h5py.Group.get too


class Group(PickleableH5Object, h5py.Group):
    """
    A subclass of h5py.Group that implements pickling, and to create new groups and datasets
    of the right type (i.e. the ones defined in this module).
    """

    # region magic methods
    def __getitem__(self, name: str | bytes) -> Any:  # type: ignore[override]
        return self._wrap(h5py.Group.__getitem__(self, name))  # type: ignore[index]

    # endregion

    # region attributes
    @property
    def attrs(self) -> AttributeManager:  # type: ignore[override]
        return AttributeManager(super().attrs)

    @property
    def file(self) -> File:
        with h5py._objects.phil:  # type: ignore[attr-defined]
            return File(self.id)

    @property
    def parent(self) -> Group:
        return Group(super().parent.id)

    # endregion

    # region methods
    def _wrap(self, obj: Any) -> Any:
        """Wrap an object accessed in this group with our custom classes."""
        obj = _h5py_wrap_type(obj)

        # If it is a group or dataset copy the current file info in
        if isinstance(obj, Group) or isinstance(obj, Dataset):
            obj.file_info = self.file_info

        return obj

    def get(self, name: str, default: Any = None, getclass: bool = False, getlink: bool = False) -> Any:
        """Retrieve an item or other information.

        "name" given only:
            Return the item, or "default" if it doesn't exist

        "getclass" is True:
            Return the class of object (Group, Dataset, etc.), or "default"
            if nothing with that name exists

        "getlink" is True:
            Return HardLink, SoftLink or ExternalLink instances.  Return
            "default" if nothing with that name exists.

        "getlink" and "getclass" are True:
            Return HardLink, SoftLink and ExternalLink classes.  Return
            "default" if nothing with that name exists.

        Example:

        >>> cls = group.get('foo', getclass=True)
        >>> if cls == SoftLink:
        """
        if not getclass and not getlink:
            return self._wrap(h5py.Group.get(self, name, default))  # type: ignore[arg-type]

        return h5py.Group.get(self, name, default, getclass, getlink)  # type: ignore[call-overload]

    def require_group(self, name: str) -> Group:
        """
        Return a group, creating it if it doesn't exist.

        TypeError is raised if something with that name already exists that
        isn't a group.
        """
        return cast(Group, super().require_group(name))

    def values(self) -> ValuesViewHDF5[Group | Dataset[Any]]:  # type: ignore[override]
        return super().values()  # type: ignore[return-value]

    def items(self) -> ItemsViewHDF5[str, Group | Dataset[Any]]:  # type: ignore[override]
        return super().items()  # type: ignore[return-value]

    def create_group(self, name: str, track_order: bool | None = None, overwrite: bool = False) -> Group:
        """
        Create and return a new subgroup.

        Args:
            name: may be absolute or relative. Fails if the target name already exists.
            track_order: Track dataset/group/attribute creation order under this group if True. If None use global
                default h5.get_config().track_order.
            overwrite: overwrite group if it already exists ?
        """
        if overwrite and name in self.keys():
            del self[name]

        group = super().create_group(name, track_order=track_order)
        return cast(Group, self._wrap(group))

    def create_dataset(
        self,
        name: str | None,
        shape: int | tuple[()] | tuple[int | None, ...] | None = None,
        dtype: npt.DTypeLike | None = None,
        data: Collection[Any] | None = None,
        **kwds: Any,
    ) -> Dataset[Any]:
        """
        Create and return a new Dataset.

        Args:
            name: Name of the dataset (absolute or relative). Provide None to make an anonymous dataset.
            shape: Dataset shape. Use "()" for scalar datasets. Required if "data" isn't provided.
            dtype: Numpy dtype or string. If omitted, dtype('f') will be used. Required if "data" isn't provided;
                otherwise, overrides data array's dtype.
            data: Provide data to initialize the dataset. If used, you can omit shape and dtype arguments.
            kwds: other arguments to pass to the dataset creation function.
        """
        group = super().create_dataset(name, shape=shape, dtype=dtype, data=data, **kwds)
        return cast(Dataset[Any], self._wrap(group))

    # endregion


class File(Group, h5py.File):
    """A subclass of h5py.File that implements pickling."""

    # region magic methods
    def __init__(self, *args: Any, **kwargs: Any):
        # Store args and kwargs for pickling
        self.init_args = args
        self.init_kwargs = kwargs

    def __new__(cls, *args: Any, **kwargs: Any) -> File:
        """Create a new File object with the h5 open function."""
        with h5py._objects.phil:  # type: ignore[attr-defined]
            self = super().__new__(cls)
            h5py.File.__init__(self, *args, **kwargs)

            return self

    def __getstate__(self) -> None:
        pass

    def __getnewargs_ex__(self) -> tuple[tuple[Any, ...], dict[str, Any]]:
        kwargs = self.init_kwargs.copy()

        if len(self.init_args) > 1 and self.init_args[1] == "w":
            return (self.init_args[0], "r+", *self.init_args[2:]), kwargs

        return self.init_args, kwargs

    def __enter__(self) -> File:
        return super().__enter__()  # type: ignore[return-value]

    # endregion

    # region attributes
    @property
    def mode(self) -> Literal[H5Mode.READ, H5Mode.READ_WRITE]:  # type: ignore[override]
        return H5Mode(super().mode)  # type: ignore[return-value]

    @property
    def file_info(self) -> File:
        return self

    # endregion
