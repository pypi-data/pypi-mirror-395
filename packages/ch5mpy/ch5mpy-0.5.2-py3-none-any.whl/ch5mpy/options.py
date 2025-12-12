from contextlib import contextmanager
from typing import Generator, Literal, TypedDict, cast

from ch5mpy.memory_size import MemorySize, as_memorysize


class _OptionsDict(TypedDict):
    error_mode: Literal["raise", "ignore"]
    max_memory_usage: MemorySize


_OPTIONS = _OptionsDict(error_mode="ignore", max_memory_usage=MemorySize(250, "M"))


def _check_error_mode(error_mode: str) -> Literal["raise", "ignore"]:
    if error_mode not in ("raise", "ignore"):
        raise ValueError("'error_mode' must be 'raise' or 'ignore'.")
    return cast(Literal["raise", "ignore"], error_mode)


def set_options(error_mode: Literal["raise", "ignore"] | None = None, max_memory: int | str | None = None) -> None:
    if error_mode is not None:
        _OPTIONS["error_mode"] = _check_error_mode(error_mode)

    if max_memory is not None:
        _OPTIONS["max_memory_usage"] = as_memorysize(max_memory)


@contextmanager
def options(
    error_mode: Literal["raise", "ignore"] | None = None, max_memory: int | str | None = None
) -> Generator[None, None, None]:
    _current_options = _OptionsDict(
        error_mode=_OPTIONS["error_mode"], max_memory_usage=_OPTIONS["max_memory_usage"].copy()
    )

    if error_mode is not None:
        _OPTIONS["error_mode"] = _check_error_mode(error_mode)

    if max_memory is not None:
        _OPTIONS["max_memory_usage"] = as_memorysize(max_memory)

    yield

    _OPTIONS["error_mode"] = _current_options["error_mode"]
    _OPTIONS["max_memory_usage"] = _current_options["max_memory_usage"]
