from __future__ import annotations

from typing import Literal, cast

_SIZES = {"B": 1, "K": 1024, "M": 1024 * 1024, "G": 1024 * 1024 * 1024}


class MemorySize:
    def __init__(self, value: int, unit: Literal["B", "K", "M", "G"]) -> None:
        if value <= 0:
            raise ValueError(f"Got invalid size ({value} <= 0).")

        self._value = value
        self._unit = unit

    def get(self) -> int:
        return self._value * _SIZES[self._unit]

    def copy(self) -> MemorySize:
        return MemorySize(self._value, self._unit)


def as_memorysize(size: int | str) -> MemorySize:
    if isinstance(size, int):
        return MemorySize(size, "B")

    elif size[-1] in _SIZES and size[:-1].lstrip("-").isdigit():
        return MemorySize(int(size[:-1]), cast(Literal["B", "K", "M", "G"], size[-1]))

    elif size.isdigit():
        return MemorySize(int(size), "B")

    raise ValueError(f"Unrecognized size '{size}'")
