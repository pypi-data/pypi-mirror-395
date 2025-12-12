from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Any, overload

import numpy as np

if TYPE_CHECKING:
    from ch5mpy import H5Array


@overload
def _get3(arr: None) -> None: ...


@overload
def _get3(arr: H5Array[Any] | Number | str) -> list[Any]: ...


def _get3(arr: H5Array[Any] | Number | str | None) -> list[Any] | None:
    """Get the first (and last) 3 elements in a set <arr>."""
    if arr is None:
        return None

    if isinstance(arr, (Number, str)):
        return [arr]

    if len(arr) <= 6:
        return list(arr)

    return list(arr[[0, 1, 2]]) + [None] + list(arr[[-3, -2, -1]])


def _str(e: Any) -> str:
    if e is None:
        return "..."

    if not isinstance(e, np.generic):
        return repr(e)

    if np.issubdtype(e.dtype, str):
        return "'" + str(e) + "'"

    return str(e)


def _print3(lst: list[Any] | None, end: str = "\n", before: str = "", sep: str = ",") -> str:
    """Print the first (and last) 3 elements in"""
    if lst is None:
        return f"{before}...{end}"

    return f"{before}[{(sep + ' ').join(map(_str, lst))}]{end}"


def _get_padding(padding: int, before: str | None = None, padding_skip_first: bool = False) -> str:
    """Get the actual needed amount of padding, given that head strings might have been pasted before."""
    if padding_skip_first:
        return ""

    if before is None:
        return " " * padding

    return " " * (padding - len(before))


def _print_dataset_core(
    arr: H5Array[Any] | None,
    padding: int,
    padding_skip_first: bool,
    before: str,
    end: str,
    sep: str,
) -> str:
    # exit condition : array is 1D and can be printed
    if arr is None or arr.ndim <= 1:
        return _print3(_get3(arr), before=before, end=end, sep=sep)

    # recursive calls
    rows = _get3(arr)
    spacer = "," + "\n" * (arr.ndim - 1)

    return (
        spacer.join(
            [
                _print_dataset_core(
                    rows[0],
                    padding=padding,
                    padding_skip_first=True,
                    before=_get_padding(padding, before, padding_skip_first) + before + "[",
                    end="",
                    sep=sep,
                )
            ]
            + [
                _print_dataset_core(
                    sub_arr,
                    padding=padding,
                    padding_skip_first=False,
                    before=_get_padding(padding + len(before) + 1),
                    end="",
                    sep=sep,
                )
                for sub_arr in rows[1:-1]
            ]
            + (
                [
                    _print_dataset_core(
                        rows[-1],
                        padding=padding,
                        padding_skip_first=False,
                        before=_get_padding(padding + len(before) + 1),
                        end="",
                        sep=sep,
                    )
                ]
                if len(rows) > 1
                else []
            )
        )
        + "]"
    )


def print_dataset(
    arr: H5Array[Any],
    padding: int = 0,
    padding_skip_first: bool = False,
    before: str | None = None,
    after: str | None = None,
    end: str = "\n",
    sep: str = ",",
) -> str:
    if arr.size == 0:
        array_repr = "[]"

    elif arr.ndim == 0:
        array_repr = f"{arr[()]}"

    else:
        array_repr = _print_dataset_core(
            arr,
            padding=padding,
            padding_skip_first=padding_skip_first,
            before="",
            end="",
            sep=sep,
        )

    before = "" if before is None else before
    after = "" if after is None else after

    return f"{before}{array_repr}{after}{end}"
