from __future__ import annotations

from functools import partial
from numbers import Number
from typing import TYPE_CHECKING, Any, Iterable

import numpy as np
import numpy.typing as npt
from numpy import _NoValue as NoValue  # type: ignore[attr-defined]

from ch5mpy._typing import NP_FUNC
from ch5mpy.array.functions.apply import ApplyOperation, apply, apply_everywhere
from ch5mpy.array.functions.implement import implements, register

if TYPE_CHECKING:
    from ch5mpy import H5Array


# ufuncs ----------------------------------------------------------------------
def H5_ufunc(
    a: H5Array[Any],
    out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None,
    *,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
    dtype: npt.DTypeLike | None = None,
    np_ufunc: NP_FUNC,
) -> Any:
    return apply(
        partial(np_ufunc, dtype=dtype),
        ApplyOperation.set,
        a,
        out=None if out is None else out[0],
        dtype=dtype,
        initial=NoValue,
        where=where,
        default_0D_output=False,
    )


_IMPLEMENTED_UFUNCS: tuple[NP_FUNC, ...] = (
    np.sin,
    np.cos,
    np.tan,
    np.arcsin,
    np.arccos,
    np.arctan,
    np.sinh,
    np.cosh,
    np.tanh,
    np.arcsinh,
    np.arccosh,
    np.arctanh,
    np.floor,
    np.ceil,
    np.trunc,
    np.exp,
    np.expm1,
    np.exp2,
    np.log,
    np.log10,
    np.log2,
    np.log1p,
    np.positive,
    np.negative,
    np.sqrt,
    np.cbrt,
    np.square,
    np.absolute,
    np.fabs,
    np.sign,
)

for ufunc in _IMPLEMENTED_UFUNCS:
    register(partial(H5_ufunc, np_ufunc=ufunc), ufunc)


@implements(np.isfinite)
def isfinite(
    a: H5Array[Any],
    out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None,
    *,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> Any:
    return apply(
        partial(np.isfinite),
        ApplyOperation.set,
        a,
        out=None if out is None else out[0],
        dtype=bool,
        initial=NoValue,
        where=where,
        default_0D_output=False,
    )


@implements(np.isinf)
def isinf(
    a: H5Array[Any],
    out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None,
    *,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> Any:
    return apply(
        partial(np.isinf),
        ApplyOperation.set,
        a,
        out=None if out is None else out[0],
        dtype=bool,
        initial=NoValue,
        where=where,
        default_0D_output=False,
    )


@implements(np.isnan)
def isnan(
    a: H5Array[Any],
    out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None,
    *,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> Any:
    return apply(
        partial(np.isnan),
        ApplyOperation.set,
        a,
        out=None if out is None else out[0],
        dtype=bool,
        initial=NoValue,
        where=where,
        default_0D_output=False,
    )


@implements(np.isneginf)
def isneginf(a: H5Array[Any], out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None) -> Any:
    return apply_everywhere(
        partial(np.isneginf),
        ApplyOperation.set,
        a,
        out=None if out is None else out[0],
        dtype=bool,
        initial=NoValue,
        default_0D_output=False,
    )


@implements(np.isposinf)
def isposinf(a: H5Array[Any], out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None) -> Any:
    return apply_everywhere(
        partial(np.isposinf),
        ApplyOperation.set,
        a,
        out=None if out is None else out[0],
        dtype=bool,
        initial=NoValue,
        default_0D_output=False,
    )


# numpy functions -------------------------------------------------------------
@implements(np.prod)
def prod(
    a: H5Array[Any],
    axis: int | Iterable[int] | tuple[int] | None = None,
    dtype: npt.DTypeLike | None = None,
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    keepdims: bool = False,
    initial: int | float | complex | NoValue = NoValue,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> Any:
    initial = 1 if initial is NoValue else initial

    return apply(
        partial(np.prod, keepdims=keepdims, dtype=dtype, axis=axis),
        ApplyOperation.imul,
        a,
        out,
        dtype=dtype,
        initial=initial,
        where=where,
    )


@implements(np.sum)
def sum_(
    a: H5Array[Any],
    axis: int | Iterable[int] | tuple[int] | None = None,
    dtype: npt.DTypeLike | None = None,
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    keepdims: bool = False,
    initial: int | float | complex | NoValue = NoValue,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> Any:
    initial = 0 if initial is NoValue else initial

    return apply(
        partial(np.sum, keepdims=keepdims, dtype=dtype, axis=axis),
        ApplyOperation.iadd,
        a,
        out,
        dtype=dtype,
        initial=initial,
        where=where,
    )


@implements(np.mean)
def mean(
    a: H5Array[Any],
    axis: int | Iterable[int] | tuple[int] | None = None,
    dtype: npt.DTypeLike | None = None,
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    keepdims: bool = False,
    *,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> Any:
    s = sum_(a, axis, dtype, out, keepdims, where=where)

    if where == NoValue:
        where = True

    n = np.broadcast_to(where, a.shape).sum(axis=axis)  # type: ignore[arg-type]
    return np.divide(s, n, out, where=where)  # type: ignore[arg-type]


@implements(np.amax, np.max)
def amax(
    a: H5Array[Any],
    axis: int | Iterable[Any] | tuple[int] | None = None,
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    keepdims: bool = False,
    initial: Number | NoValue = NoValue,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> npt.NDArray[np.number[Any]] | np.number[Any]:
    return apply(  # type: ignore[no-any-return]
        partial(np.amax, keepdims=keepdims, axis=axis),
        ApplyOperation.set,
        a,
        out,
        dtype=None,
        initial=initial,
        where=where,
    )


@implements(np.amin, np.min)
def amin(
    a: H5Array[Any],
    axis: int | Iterable[Any] | tuple[int] | None = None,
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    keepdims: bool = False,
    initial: Number | NoValue = NoValue,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> npt.NDArray[np.number[Any]] | np.number[Any]:
    return apply(  # type: ignore[no-any-return]
        partial(np.amin, keepdims=keepdims, axis=axis),
        ApplyOperation.set,
        a,
        out,
        dtype=None,
        initial=initial,
        where=where,
    )


@implements(np.all)
def all_(
    a: H5Array[Any],
    axis: int | Iterable[Any] | tuple[int] | None = None,
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    keepdims: bool = False,
    *,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> npt.NDArray[Any] | bool:
    return apply(  # type: ignore[no-any-return]
        partial(np.all, keepdims=keepdims, axis=axis),
        ApplyOperation.iand,
        a,
        out,
        dtype=bool,
        initial=True,
        where=where,
    )


@implements(np.any)
def any_(
    a: H5Array[Any],
    axis: int | Iterable[Any] | tuple[int] | None = None,
    out: H5Array[Any] | npt.NDArray[Any] | None = None,
    keepdims: bool = False,
    *,
    where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
) -> npt.NDArray[Any] | bool:
    return apply(  # type: ignore[no-any-return]
        partial(np.any, keepdims=keepdims, axis=axis),
        ApplyOperation.ior,
        a,
        out,
        dtype=bool,
        initial=False,
        where=where,
    )


@implements(np.cumsum)
def cumsum(
    a: H5Array[Any], axis: int | None = None, dtype: npt.DTypeLike = None, out: npt.NDArray[Any] | None = None
) -> npt.NDArray[Any]:
    # TODO: find better implementation to avoid whole array copy
    return np.cumsum(a.copy(), axis=axis, dtype=dtype, out=out)


@implements(np.diff)
def diff(
    a: H5Array[Any],
    n: int = 1,
    axis: int = -1,
    prepend: npt.NDArray[Any] | NoValue = NoValue,
    append: npt.NDArray[Any] | NoValue = NoValue,
) -> npt.NDArray[Any] | H5Array[Any]:
    if a.ndim != 1 or axis not in (0, -1):
        raise NotImplementedError

    if n == 0:
        return a

    if n > 1:
        raise NotImplementedError

    prepend = np.array([], dtype=a.dtype) if prepend == NoValue else np.atleast_1d(prepend).astype(a.dtype)
    append = np.array([], dtype=a.dtype) if append == NoValue else np.atleast_1d(append).astype(a.dtype)

    output_array = np.empty(len(a) + len(prepend) + len(append) - 1, dtype=a.dtype)

    for index, chunk_start, chunk_end in a[:-1].iter_chunks_with(a[1:]):
        output_array[len(prepend) : len(prepend) + len(a)][index] = chunk_end - chunk_start

    output_array[: len(prepend)] = np.diff(np.r_[prepend, a[0]])
    output_array[len(prepend) + len(a) - 1 :] = np.diff(np.r_[a[-1], append])

    return output_array


@implements(np.ediff1d)
def ediff1d(
    ary: H5Array[Any], to_end: npt.ArrayLike | None = None, to_begin: npt.ArrayLike | None = None
) -> npt.NDArray[Any]:
    if ary.ndim > 1:
        return np.diff(ary.flatten(), prepend=to_begin or NoValue, append=to_end or NoValue)

    return np.diff(ary, prepend=to_begin or NoValue, append=to_end or NoValue)
