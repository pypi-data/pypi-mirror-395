from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

import ch5mpy


@runtime_checkable
class AnonymousArrayCreationFunc(Protocol):
    def __call__(self, name: str, loc: str | Path | ch5mpy.File | ch5mpy.Group) -> None: ...
