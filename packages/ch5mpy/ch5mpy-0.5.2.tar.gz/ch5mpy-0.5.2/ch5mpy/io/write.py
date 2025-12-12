from __future__ import annotations

import pickle
from numbers import Number
from typing import TYPE_CHECKING, Any, Mapping

import numpy as np
import numpy.typing as npt
from h5py import string_dtype
from tqdm.auto import tqdm

import ch5mpy
from ch5mpy.functions import AnonymousArrayCreationFunc
from ch5mpy.objects import Dataset, File, Group
from ch5mpy.types import SupportsH5Write
from ch5mpy.utils import is_sequence

if TYPE_CHECKING:
    from ch5mpy import H5Array


def store_dataset(
    array: npt.NDArray[Any] | H5Array[Any] | None,
    loc: Group | File,
    name: str,
    shape: tuple[int, ...] | None = None,
    dtype: npt.DTypeLike | None = None,
    chunks: bool | tuple[int, ...] = True,
    maxshape: int | tuple[int | None, ...] | None = None,
    fill_value: Any = None,
) -> Dataset[Any]:
    """Store a dataset."""
    if not loc.file.id.valid:
        raise OSError("Cannot write data to closed file.")

    if dtype is None:
        if array is not None:
            dtype = array.dtype

    if isinstance(dtype, type):
        str_dtype = str(dtype().dtype)
    else:
        str_dtype = str(dtype)

    if np.issubdtype(dtype, np.str_):
        array = None if array is None else array.astype("O")
        dtype = string_dtype()

    if array is not None:
        if shape is None:
            shape = array.shape

        elif shape != array.shape:
            raise ValueError("array's shape does not match the shape parameter.")

    elif shape is None:
        raise ValueError("At least one of `array` or `shape` must be provided.")

    if chunks:
        if chunks is True:  # literally `True`, not a tuple
            # FIXME : causes huge lag
            # parsed_chunks = (get_size(ch5mpy.H5Array.MAX_MEM_USAGE),) + (1,) * (len(shape) - 1)
            pass

        parsed_chunks = chunks

        if maxshape is None:
            maxshape = (None,) * len(shape)

    else:
        parsed_chunks = None

    dset = loc.create_dataset(
        name,
        data=array,
        shape=shape,
        dtype=dtype,
        chunks=parsed_chunks,
        maxshape=maxshape,
        fillvalue=fill_value,
    )
    dset.attrs["dtype"] = str_dtype

    return dset


def _has_dataset_attributes(obj: Any) -> bool:
    return hasattr(obj, "shape") and hasattr(obj, "dtype")


def write_dataset(
    obj: Any,
    loc: Group | File | ch5mpy.H5Dict[Any],
    name: str,
    *,
    chunks: bool | tuple[int, ...] = True,
    maxshape: tuple[int, ...] | None = None,
) -> ch5mpy.H5Array[Any]:
    """Write an array-like object to a H5 dataset."""
    if isinstance(loc, ch5mpy.H5Dict):
        loc = loc.file

    # cast to np.array if needed (to get shape and dtype)
    array = np.array(obj) if not _has_dataset_attributes(obj) else obj
    if array.dtype == object:
        array = array.astype(str)

        if array.dtype == object:
            array = np.array(array).astype(str)

        if array.dtype == object:
            raise ValueError("Array casting to string has failed repeatedly.")

    if name in loc.keys():
        if loc[name] is array:
            # this exact dataset is already stored > do nothing
            return ch5mpy.H5Array(loc[name])

        if loc[name].shape == array.shape and loc[name].dtype == array.dtype:
            # a similar array already exists > simply copy the data
            loc[name][()] = array
            return ch5mpy.H5Array(loc[name])

        # a different array was stored, delete it before storing the new array
        del loc[name]

    return ch5mpy.H5Array(store_dataset(array, loc, name, chunks=chunks, maxshape=maxshape))


def write_datasets(
    loc: Group | File | ch5mpy.H5Dict[Any],
    *,
    chunks: bool | tuple[int, ...] = True,
    maxshape: tuple[int, ...] | None = None,
    **kwargs: Any,
) -> None:
    """Write multiple array-like objects to H5 datasets."""
    for name, obj in kwargs.items():
        write_dataset(obj, loc, name, chunks=chunks, maxshape=maxshape)


def write_object(
    obj: Any,
    loc: Group | File | ch5mpy.H5Dict[Any],
    name: str,
    *,
    chunks: bool | tuple[int, ...] = True,
    maxshape: tuple[int, ...] | None = None,
    overwrite: bool = False,
    progress: tqdm[Any] | None = None,
) -> ch5mpy.H5Dict[Any]:
    """Write any object to a H5 file."""
    if isinstance(loc, ch5mpy.H5Dict):
        loc = loc.file

    if isinstance(obj, SupportsH5Write):
        group = loc.create_group(name, overwrite=overwrite, track_order=True) if name else loc
        obj.__h5_write__(ch5mpy.H5Dict(group))
        group.attrs["__h5_type__"] = "object"
        group.attrs["__h5_class__"] = np.void(pickle.dumps(type(obj), protocol=pickle.HIGHEST_PROTOCOL))

    elif isinstance(obj, AnonymousArrayCreationFunc):
        obj(name=name, loc=loc)

    elif isinstance(obj, Mapping):
        group = loc.create_group(name, overwrite=overwrite, track_order=True) if name else loc
        write_objects(group, **obj, chunks=chunks, maxshape=maxshape, progress=progress)

    elif is_sequence(obj):
        write_dataset(obj, loc, name, chunks=chunks, maxshape=maxshape)

    elif isinstance(obj, (Number, str)):
        name = name or "/"

        if name in loc and overwrite:
            del loc[name]

        loc[name] = obj

    else:
        name = name or "/"

        loc[name] = np.void(pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL))
        loc[name].attrs["__h5_type__"] = "pickle"

    if progress is not None:
        progress.update()

    return ch5mpy.H5Dict(loc) @ name if name else ch5mpy.H5Dict(loc)


def write_objects(
    loc: Group | File | ch5mpy.H5Dict[Any],
    *,
    chunks: bool | tuple[int, ...] = True,
    maxshape: tuple[int, ...] | None = None,
    overwrite: bool = False,
    progress: tqdm[Any] | None = None,
    **kwargs: SupportsH5Write | H5Array[Any],
) -> None:
    """Write multiple objects of any type to a H5 file."""
    for name, obj in kwargs.items():
        write_object(
            obj,
            loc,
            name,
            chunks=chunks,
            maxshape=maxshape,
            overwrite=overwrite,
            progress=progress,
        )
