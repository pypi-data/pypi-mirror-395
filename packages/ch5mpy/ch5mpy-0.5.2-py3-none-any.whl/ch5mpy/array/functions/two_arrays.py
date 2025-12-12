from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Any, Iterable

import numpy as np
import numpy.typing as npt

import ch5mpy
from ch5mpy.array.functions.apply import apply_2, ensure_h5array_first, str_apply_2
from ch5mpy.array.functions.implement import implements

if TYPE_CHECKING:
    from ch5mpy import H5Array


@implements(np.array_equal)
def array_equal(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    equal_nan: bool = False,
) -> bool:
    x1, x2, *_ = ensure_h5array_first(x1, x2)

    # case 0D
    if isinstance(x2, Number):
        if x1.ndim:
            return False

        return np.array_equal(x1, x2, equal_nan=equal_nan)  # type: ignore[arg-type]

    # case nD
    if not isinstance(x2, (np.ndarray, ch5mpy.H5Array)):
        x2 = np.array(x2)

    if x1.shape != x2.shape:
        return False

    for _, chunk_x1, chunk_x2 in x1.iter_chunks_with(x2):
        if not np.array_equal(chunk_x1, chunk_x2):
            return False

    return True


@implements(np.greater)
def greater(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.greater,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=False,
    )


@implements(np.char.greater)
def str_greater(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.greater, x1, x2)


@implements(np.greater_equal)
def greater_equal(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.greater_equal,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=False,
    )


@implements(np.char.greater_equal)
def str_greater_equal(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.greater_equal, x1, x2)


@implements(np.less)
def less(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.less,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=False,
    )


@implements(np.char.less)
def str_less(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.less, x1, x2)


@implements(np.less_equal)
def less_equal(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.less_equal,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=False,
    )


@implements(np.char.less_equal)
def str_less_equal(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.less_equal, x1, x2)


@implements(np.equal)
def equal(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.equal,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=False,
    )


@implements(np.char.equal)
def str_equal(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.equal, x1, x2)


@implements(np.not_equal)
def not_equal(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.not_equal,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=False,
    )


@implements(np.char.not_equal)
def str_not_equal(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.not_equal, x1, x2)


@implements(np.add)
def add(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.add,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.char.add)
def str_add(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.add, x1, x2)


@implements(np.multiply)
def multiply(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.multiply,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.char.multiply)
def str_multiply(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.multiply, x1, x2)


@implements(np.divide)
def divide(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.divide,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.power)
def power(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.power,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.subtract)
def subtract(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.subtract,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.true_divide)
def true_divide(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.true_divide,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.floor_divide)
def floor_divide(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.floor_divide,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.float_power)
def float_power(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.float_power,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.fmod)
def fmod(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.fmod,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.mod)
def mod(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.mod,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.char.mod)
def str_mod(x1: str | npt.NDArray[np.str_] | Iterable[str] | H5Array[np.str_], x2: Any) -> Any:
    return str_apply_2(np.char.mod, x1, x2)


@implements(np.maximum)
def maximum(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.maximum,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.fmax)
def fmax(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.fmax,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.minimum)
def minimum(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.minimum,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.fmin)
def fmin(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    return apply_2(
        np.fmin,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.logical_and)
def logical_and(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.logical_and,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.logical_or)
def logical_or(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.logical_or,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.logical_not)
def logical_not(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.logical_not,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )


@implements(np.logical_xor)
def logical_xor(
    x1: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    x2: npt.NDArray[Any] | Iterable[Any] | Number | H5Array[Any],
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    where: npt.NDArray[np.bool_] | Iterable[bool] | bool | int = True,
    dtype: npt.DTypeLike | None = None,
) -> Any:
    if dtype is None:
        dtype = bool

    return apply_2(
        np.logical_xor,
        x1,
        x2,
        out=out,
        dtype=dtype,
        where=where,
        default=x1,
    )
