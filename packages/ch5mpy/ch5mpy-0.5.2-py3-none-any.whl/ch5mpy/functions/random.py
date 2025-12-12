from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

import ch5mpy
from ch5mpy.functions.creation_routines import ArrayCreationFunc
from ch5mpy.indexing import map_slice


class ArrayCreationFuncRandom(ArrayCreationFunc):
    # region magic methods
    def __init__(self, name: str, random_func: Any):
        super().__init__(name)
        self._random_func = random_func

    def __call__(  # type: ignore[override]
        self,
        *dims: int,
        loc: str | Path | ch5mpy.File | ch5mpy.Group,
        name: str,
        dtype: npt.DTypeLike = np.float64,
        chunks: bool | tuple[int, ...] = True,
        maxshape: int | tuple[int | None, ...] | None = None,
    ) -> ch5mpy.H5Array[Any]:
        arr = super().__call__(dims, None, loc, name, dtype=dtype, chunks=chunks, maxshape=maxshape)

        for index, chunk in arr.iter_chunks():
            chunk = self._random_func(*chunk.shape)

            arr.dset.write_direct(
                chunk,
                source_sel=map_slice(index, shift_to_zero=True),
                dest_sel=map_slice(index),
            )

        return arr

    # endregion

    # region methods
    def anonymous(
        self,
        *dims: int,
        dtype: npt.DTypeLike = np.float64,
        chunks: bool | tuple[int, ...] = True,
        maxshape: int | tuple[int | None, ...] | None = None,
    ) -> partial[ch5mpy.H5Array[Any]]:
        return partial(self.__call__, *dims, dtype=dtype, chunks=chunks, maxshape=maxshape)

    # endregion


beta = ArrayCreationFuncRandom("beta", np.random.beta)
binomial = ArrayCreationFuncRandom("binomial", np.random.binomial)
bytes = ArrayCreationFuncRandom("bytes", np.random.bytes)
chisquare = ArrayCreationFuncRandom("chisquare", np.random.chisquare)
choice = ArrayCreationFuncRandom("choice", np.random.choice)
dirichlet = ArrayCreationFuncRandom("dirichlet", np.random.dirichlet)
exponential = ArrayCreationFuncRandom("exponential", np.random.exponential)
f = ArrayCreationFuncRandom("f", np.random.f)
gamma = ArrayCreationFuncRandom("gamma", np.random.gamma)
get_state = ArrayCreationFuncRandom("get_state", np.random.get_state)
geometric = ArrayCreationFuncRandom("geometric", np.random.geometric)
gumbel = ArrayCreationFuncRandom("gumbel", np.random.gumbel)
hypergeometric = ArrayCreationFuncRandom("hypergeometric", np.random.hypergeometric)
laplace = ArrayCreationFuncRandom("laplace", np.random.laplace)
logistic = ArrayCreationFuncRandom("logistic", np.random.logistic)
lognormal = ArrayCreationFuncRandom("lognormal", np.random.lognormal)
logseries = ArrayCreationFuncRandom("logseries", np.random.logseries)
multinomial = ArrayCreationFuncRandom("multinomial", np.random.multinomial)
multivariate_normal = ArrayCreationFuncRandom("multivariate_normal", np.random.multivariate_normal)
negative_binomial = ArrayCreationFuncRandom("negative_binomial", np.random.negative_binomial)
noncentral_chisquare = ArrayCreationFuncRandom("noncentral_chisquare", np.random.noncentral_chisquare)
noncentral_f = ArrayCreationFuncRandom("noncentral_f", np.random.noncentral_f)
normal = ArrayCreationFuncRandom("normal", np.random.normal)
pareto = ArrayCreationFuncRandom("pareto", np.random.pareto)
permutation = ArrayCreationFuncRandom("permutation", np.random.permutation)
poisson = ArrayCreationFuncRandom("poisson", np.random.poisson)
power = ArrayCreationFuncRandom("power", np.random.power)
rand = ArrayCreationFuncRandom("rand", np.random.rand)
randint = ArrayCreationFuncRandom("randint", np.random.randint)
randn = ArrayCreationFuncRandom("randn", np.random.randn)
random = ArrayCreationFuncRandom("random", np.random.random)
random_integers = ArrayCreationFuncRandom("random_integers", np.random.random_integers)
random_sample = ArrayCreationFuncRandom("random_sample", np.random.random_sample)
rayleigh = ArrayCreationFuncRandom("rayleigh", np.random.rayleigh)
seed = ArrayCreationFuncRandom("seed", np.random.seed)
set_state = ArrayCreationFuncRandom("set_state", np.random.set_state)
shuffle = ArrayCreationFuncRandom("shuffle", np.random.shuffle)
standard_cauchy = ArrayCreationFuncRandom("standard_cauchy", np.random.standard_cauchy)
standard_exponential = ArrayCreationFuncRandom("standard_exponential", np.random.standard_exponential)
standard_gamma = ArrayCreationFuncRandom("standard_gamma", np.random.standard_gamma)
standard_normal = ArrayCreationFuncRandom("standard_normal", np.random.standard_normal)
standard_t = ArrayCreationFuncRandom("standard_t", np.random.standard_t)
triangular = ArrayCreationFuncRandom("triangular", np.random.triangular)
uniform = ArrayCreationFuncRandom("uniform", np.random.uniform)
vonmises = ArrayCreationFuncRandom("vonmises", np.random.vonmises)
wald = ArrayCreationFuncRandom("wald", np.random.wald)
weibull = ArrayCreationFuncRandom("weibull", np.random.weibull)
zipf = ArrayCreationFuncRandom("zipf", np.random.zipf)
