from __future__ import annotations

import pickle
from typing import Any, Literal, cast

import numpy as np

import ch5mpy
import ch5mpy.dict
from ch5mpy.objects import Dataset, Group
from ch5mpy.types import SupportsH5Read


def _handle_read_error(
    error: BaseException, data: Group, error_mode: Literal["ignore", "raise"]
) -> ch5mpy.dict.H5Dict[Any]:
    if error_mode == "raise":
        raise error

    else:
        return ch5mpy.dict.H5Dict(data, annotation=f"Failed reading object: {error}")


def read_object(
    data: Dataset[Any] | Group,
    error: Literal["ignore", "raise"] = "raise",
    read_object: bool = True,
) -> Any:
    """Read an object from a .h5 file"""
    if not isinstance(data, (Dataset, Group)):
        raise ValueError(f"Cannot read object from '{type(data)}'.")

    if not data.file.id.valid:
        raise OSError("Cannot read data from closed file.")

    if isinstance(data, Group):
        h5_type = data.attrs.get("__h5_type__", "<UNKNOWN>")
        if h5_type == "list":
            return ch5mpy.H5List(data)

        if not read_object or h5_type != "object":
            return ch5mpy.dict.H5Dict(data)

        h5_class = data.attrs.get("__h5_class__", None)
        if h5_class is None:
            return _handle_read_error(ValueError("Cannot read object with unknown class."), data, error)

        try:
            data_class = pickle.loads(h5_class)
        except ModuleNotFoundError as e:
            return _handle_read_error(e, data, error)

        if not issubclass(data_class, SupportsH5Read):
            return _handle_read_error(
                ValueError(
                    f"Don't know how to read {data_class} since it does not implement the '__h5_read__' method."
                ),
                data,
                error,
            )

        try:
            return data_class.__h5_read__(ch5mpy.dict.H5Dict(data))

        except Exception as e:
            return _handle_read_error(e, data, error)

    if data.ndim == 0:
        if np.issubdtype(data.dtype, np.void):
            return pickle.loads(data[()])  # type: ignore[arg-type]

        if data.dtype == object:
            return cast(bytes, data[()]).decode()

        return data[()]

    return ch5mpy.H5Array(data)
