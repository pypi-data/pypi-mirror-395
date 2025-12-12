from importlib import metadata

import ch5mpy.dict
import ch5mpy.functions.random
from ch5mpy import indexing
from ch5mpy.array import H5Array
from ch5mpy.attributes import AttributeManager
from ch5mpy.dict import H5Dict
from ch5mpy.functions import AnonymousArrayCreationFunc, empty, full, ones, zeros
from ch5mpy.io import (
    read_object,
    store_dataset,
    write_dataset,
    write_datasets,
    write_object,
    write_objects,
)
from ch5mpy.list import H5List
from ch5mpy.names import H5Mode
from ch5mpy.np import arange_nd
from ch5mpy.objects import Dataset, File, Group
from ch5mpy.options import options, set_options
from ch5mpy.types import SupportsH5Read, SupportsH5ReadWrite, SupportsH5Write

random = ch5mpy.functions.random

__all__ = [
    "File",
    "Group",
    "Dataset",
    "H5Dict",
    "H5List",
    "H5Array",
    "AttributeManager",
    "store_dataset",
    "write_dataset",
    "write_datasets",
    "write_object",
    "write_objects",
    "read_object",
    "H5Mode",
    "arange_nd",
    "empty",
    "zeros",
    "ones",
    "full",
    "AnonymousArrayCreationFunc",
    "options",
    "set_options",
    "SupportsH5Write",
    "SupportsH5Read",
    "SupportsH5ReadWrite",
    "indexing",
]

__version__ = metadata.version("ch5mpy")
