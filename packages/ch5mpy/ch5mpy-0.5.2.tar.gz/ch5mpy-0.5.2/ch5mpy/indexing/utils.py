from typing import Any, Callable, Generator, Iterable


def takewhile_inclusive(predicate: Callable[[Any], bool], it: Iterable[Any]) -> Generator[Any, None, None]:
    while True:
        e = next(it, None)  # type: ignore[call-overload]
        yield e

        if e is None or not predicate(e):
            break


def positive_slice_index(value: int, max: int) -> int:
    return value if value >= 0 else max + value
