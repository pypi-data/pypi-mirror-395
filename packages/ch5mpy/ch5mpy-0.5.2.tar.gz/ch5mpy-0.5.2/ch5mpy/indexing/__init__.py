from typing import Union

from ch5mpy.indexing.base import Indexer, as_indexer, boolean_array_as_indexer
from ch5mpy.indexing.list import ListIndex
from ch5mpy.indexing.selection import Selection, get_indexer
from ch5mpy.indexing.single import SingleIndex
from ch5mpy.indexing.slice import FullSlice, map_slice
from ch5mpy.indexing.special import EmptyList, NewAxis, NewAxisType

LengthedIndexer = Union[ListIndex, FullSlice, EmptyList]

__all__ = [
    "Indexer",
    "Selection",
    "get_indexer",
    "boolean_array_as_indexer",
    "map_slice",
    "FullSlice",
    "ListIndex",
    "SingleIndex",
    "NewAxis",
    "NewAxisType",
    "as_indexer",
    "EmptyList",
]
