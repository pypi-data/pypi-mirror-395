from __future__ import annotations

from collections.abc import Collection, Sequence
from typing import Any, TypeGuard


def is_sequence(obj: Any) -> TypeGuard[Sequence[Any]]:
    """Is the object a sequence of objects ? (excluding strings and byte objects.)"""
    return (
        isinstance(obj, Collection)
        and hasattr(obj, "__getitem__")
        and not isinstance(obj, (str, bytes, bytearray, memoryview))
    )


NAN_PACKED = b"\x01\x01\xc0\x7f"  # special representation of a nan suited for storage in hdf5 datasets
# null bytes \x00 cause errors but nan can be represented as s111 1111 1100 0000 xxxx xxxx xxxx xxxx
#                                                             7    f    c    0    x    x    x    x
