from __future__ import annotations

from enum import Enum


class H5Mode(str, Enum):
    """
    READ (r) : Readonly, file must exist
    READ_WRITE (r+) : Read/write, file must exist
    WRITE_TRUNCATE (w) : Create file, truncate if exists
    WRITE (w-) : Create file, fail if exists
    READ_WRITE_CREATE (a) : Read/write if exists, create otherwise
    """

    READ = "r"  # Readonly, file must exist
    READ_WRITE = "r+"  # Read/write, file must exist
    WRITE_TRUNCATE = "w"  # Create file, truncate if exists
    WRITE = "w-"  # Create file, fail if exists
    READ_WRITE_CREATE = "a"  # Read/write if exists, create otherwise

    @staticmethod
    def has_write_intent(mode: H5Mode) -> bool:
        return mode in (H5Mode.READ_WRITE, H5Mode.READ_WRITE_CREATE, H5Mode.WRITE, H5Mode.WRITE_TRUNCATE)
