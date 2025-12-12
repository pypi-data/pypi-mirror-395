# Ch5mpy

Pronounced "champy".
This library provides a set of helper tools for easily reading or writing even complex objects to h5 files using the h5py library. It implements wrappers around h5py objects providing APIs identical to regular Python lists and dicts and to numpy ndarrays.

See the complete documentation at https://ch5mpy.readthedocs.io/en/latest/ for more details.

## Description

Ch5mpy provides a set of abstractions over h5py's (https://docs.h5py.org/en/stable/) objects for handling them as more commonly used objects :
- H5Dict: an object behaving as regular Python dictionaries, for exploring Files and Groups.
- H5List: an object behaving as regular Python lists for storing any set of objects.
- H5Array: an object behaving as Numpy ndarrays for dealing effortlessly with Datasets while keeping the memory usage low. This works by applying numpy functions to small chunks of the whole Dataset at a time.
- AttributeManager: a dict-like object for accessing an h5 object's metadata.
- read/write utily functions for effortlessly storing any object to an h5 file.

Pickling has also been added to base h5 objects.

### Pickling
Ch5mpy provides Datasets, Groups and Files objects wrapping the h5py's equivalents to allow pickling. Those objects can be directly imported from `ch5mpy`:

```python
>>> from ch5mpy import File
>>> from ch5mpy import Group
>>> from ch5mpy import Dataset
```

The `H5Mode` enum lists valid modes for opening an h5 file:

```python
>>> from ch5mpy import H5Mode
```

```python
class H5Mode(str, Enum):
    READ = "r"  # Readonly, file must exist
    READ_WRITE = "r+"  # Read/write, file must exist
    WRITE_TRUNCATE = "w"  # Create file, truncate if exists
    WRITE = "w-"  # Create file, fail if exists
    READ_WRITE_CREATE = "a"  # Read/write if exists, create otherwise
```

### Attributes
Metadata on Datasets, Groups and Files can be obtained and modified through the `.attrs` attribute, returning an `AttributeManager` object. `AttributeManagers` behave like Python dictionaries for getting and setting any value.

```python
>>> from ch5mpy import File
>>> f = File('some/file.h5')
>>> f.attrs
AttributeManager{value: 1,
                 creation: '02/08/2021',
                 parent: None}
>>> f.attrs['value']
1
```

`AttributeManagers` correctly handle `None` values.

### H5Dict
An `H5Dict` allows to explore the content of an H5 File or Group as if it was a regular Python dict. Any value can be set in an `H5Dict`. However, keys in an `H5Dict` are not loaded into memory until they are directly requested. `Datasets` are wrapped and accessed as `H5Arrays` (see section [H5Arrays](#h5array)).

To create an `H5Dict`, a `File` or `Group` object must be provided as argument:

```python
>>> from ch5mpy import File
>>> from ch5mpy import H5Dict
>>> from ch5mpy import H5Mode
>>>
>>> dct = H5Dict(File("dict.h5", H5Mode.READ_WRITE))
>>> dct
H5Dict{
    a: 1, 
    b: H5Array([1, 2, 3], shape=(3,), dtype=int64), 
    c: {...}
}
```

Here, `dct` is an `H5Dict` with 3 keys `a, b and c` where :
- `a` maps to the value `1`
- `b` maps to a 1D Dataset 
- `c` maps to a sub H5Dict with keys and values not loaded yet

Alternatively, an `H5Dict` can be created directly from a path to an h5 file:

```python
>>> H5Dict.read("dict.h5")
H5Dict{
    a: 1, 
    b: H5Array([1, 2, 3], shape=(3,), dtype=int64), 
    c: {...}
}
```

### H5List
An `H5List` behave as regular Python lists, allowing to store and access any kind of object in an h5 file. `H5Lists` are usually created when regular lists are stored in an h5 file. 

As for [H5Dicts](#h5dict), `H5Lists` can be created by providing a `File` or by calling the `.read()` method:

```python
>>> from ch5mpy import File
>>> from ch5mpy import H5List
>>> from ch5mpy import H5Mode
>>>
>>> lst = H5List(File("backed_list.h5", H5Mode.READ_WRITE))
>>> lst
H5List[1.0, 2, '4.']
```

```python
class O_:
    def __init__(self, v: float):
        self._v = v

    def __repr__(self) -> str:
        return f"O({self._v})"
```

```python
>>> lst.append(O(5.0))
>>> lst
H5List[1.0, 2, '4.', O(5.0)]
```

`H5Lists` can store regular integers, floats and strings, but can also store any object (such as the `O` object at index 3 in this example).

### H5Array
`H5Arrays` wrap `Datasets` and implement numpy ndarrays' interface to behave as numpy ndarrays while controlling the amount of RAM used. The maximum amount of available RAM for performing operations can be set with the function `set_options(max_memory_usage=...)`, using suffixes `B`, `K`, `M` and `G` for expressing amounts in bytes.

H5Arrays can be created by passing a `Dataset` as argument. 

```python
>>> from ch5mpy import File
>>> from ch5mpy import H5Mode
>>> from ch5mpy import H5Array
>>> h5_array = H5Array(File("h5_arrays", H5Mode.READ_WRITE)["integers"])
>>> h5_array
H5Array([[0, 1, 2],
         [3, 4, 5],
         [6, 7, 8]], shape=(3, 3), dtype=int64)
>>> h5_array = H5Array(File("h5_arrays", H5Mode.READ_WRITE)["strings"])
>>> h5_array
H5Array(['blue', 'red', 'yellow'], shape=(3,), dtype='<U6')
```



Then, all usual numpy indexing and methods can be used. To keep the memory footprint small, those methods will be applied repeatedly on small chunks of the underlying Dataset.

To load an H5Array into memory as a numpy array, simply run :

```python
np.array(h5_array)
```

### Read/write utilities

#### Functions
To store any array-like object (object which could be converted to a numpy ndarray), functions `write_dataset()` and `write_datasets()` respectively allow to store one or many such objects.

To store any other object, call functions `write_object()` and `write_objects()`. 
To dertermine how the object will be stored in the h5 file, the following rules are applied:
- objects implementing the [Storing API](#storing-api) will be stored by calling the `__h5_write__()` function
- objects that can be converted to numpy arrays will be saved by calling `write_dataset()`
- numbers and strings will be stored directly 
- all other objects will be stored as binary data by first pickling them

#### Storing API
To define by hand how an object is stored and read from an h5 file, you can implement the `__h5_write__()` and `__h5_read__()` methods:

```python
class YourObject:
    ...

    def __h5_write__(self, values: ch5mpy.H5Dict[Any]) -> None: 
        ...

    @classmethod
    def __h5_read__(cls, values: ch5mpy.H5Dict[Any]) -> YourObject:
        ...
```

Both `__h5_write__()` and `__h5_read__()` receive as input an `H5Dict` in which to store or retreive your object. Please note that `__h5_read__()` is a classmethod, called as `YourObject.__h5_read__()` and which is responsible for both reading data from the `H5Dict` and reconstructing an instance of `YourObject`.

### Roadmap

Numpy methods to implement for `H5Arrays`:

Logic functions
- [x] np.all
- [x] np.any
- [x] np.isfinite
- [x] np.isinf
- [x] np.isnan
- [ ] np.isnat
- [x] np.isneginf
- [x] np.isposinf
- [ ] np.iscomplex
- [ ] np.iscomplexobj
- [ ] np.isfortran
- [ ] np.isreal
- [ ] np.isrealobj
- [ ] np.isscalar
- [x] np.logical_and
- [x] np.logical_or
- [x] np.logical_not
- [x] np.logical_xor
- [ ] np.allclose
- [ ] np.isclose
- [x] np.array_equal
- [ ] np.array_equiv
- [x] np.greater
- [x] np.greater_equal
- [x] np.less
- [x] np.less_equal
- [x] np.equal
- [x] np.not_equal

Binary operations
- [ ] np.bitwize_and
- [ ] np.bitwize_or
- [ ] np.bitwize_xor
- [ ] np.invert
- [ ] np.left_shift
- [ ] np.right_shift
- [ ] np.packbits
- [ ] np.unpackbits
- [ ] np.binary_repr

String operations
- [x] np.char.add
- [x] np.char.multiply
- [x] np.char.mod
- [ ] np.char.capitalize
- [ ] np.char.center
- [ ] np.char.decode
- [ ] np.char.encode
- [ ] np.char.expandtabs
- [ ] np.char.join
- [ ] np.char.ljust
- [ ] np.char.lower
- [ ] np.char.lstrip
- [ ] np.char.partition
- [ ] np.char.replace
- [ ] np.char.rjust
- [ ] np.char.rpartition
- [ ] np.char.rsplit
- [ ] np.char.rstrip
- [ ] np.char.split
- [ ] np.char.splitlines
- [ ] np.char.strip
- [ ] np.char.swapcase
- [ ] np.char.title
- [ ] np.char.translate
- [ ] np.char.upper
- [ ] np.char.zfill
- [x] np.char.equal
- [x] np.char.not_equal
- [x] np.char.greater_equal
- [x] np.char.less_equal
- [x] np.char.greater
- [x] np.char.less
- [ ] np.char.compare_chararrays
- [ ] np.char.count
- [ ] np.char.endswith
- [ ] np.char.find
- [ ] np.char.index
- [ ] np.char.isalpha
- [ ] np.char.isalnum
- [ ] np.char.isdecimal
- [ ] np.char.isdigit
- [ ] np.char.islower
- [ ] np.char.isnumeric
- [ ] np.char.isspace
- [ ] np.char.istitle
- [ ] np.char.isupper
- [ ] np.char.rfind
- [ ] np.char.rindex
- [ ] np.char.startswith
- [ ] np.char.str_len
- [ ] np.char.array
- [ ] np.char.asarray
- [ ] np.char.chararray

Mathematical functions
- [x] np.sin
- [x] np.cos
- [x] np.tan
- [x] np.arcsin
- [x] np.arccos
- [x] np.arctan
- [ ] np.hypot
- [ ] np.arctan2
- [ ] np.degrees
- [ ] np.radians
- [ ] np.unwrap
- [ ] np.deg2rad
- [ ] np.rad2deg
- [x] np.sinh
- [x] np.cosh
- [x] np.tanh
- [x] np.arcsinh
- [x] np.arccosh
- [x] np.arctanh
- [ ] np.around
- [ ] np.rint
- [ ] np.fix
- [x] np.floor
- [x] np.ceil
- [x] np.trunc
- [x] np.prod
- [x] np.sum
- [ ] np.nanprod
- [ ] np.nansum
- [ ] np.cumprod
- [x] np.cumsum
- [ ] np.nancumprod
- [ ] np.nancumsum
- [x] np.diff
- [ ] np.ediff1d
- [ ] np.gradient
- [ ] np.cross
- [ ] np.trapz
- [x] np.exp
- [x] np.expm1
- [x] np.exp2
- [x] np.log
- [x] np.log10
- [x] np.log2
- [x] np.log1p
- [ ] np.logaddexp
- [ ] np.logaddexp2
- [ ] np.i0
- [ ] np.sinc
- [ ] np.signbit
- [ ] np.copysign
- [ ] np.frexp
- [ ] np.ldexp
- [ ] np.nextafter
- [ ] np.spacing
- [ ] np.lcm
- [ ] np.gcd
- [x] np.add
- [ ] np.reciprocal
- [x] np.positive
- [x] np.negative
- [x] np.multiply
- [x] np.divide
- [x] np.power
- [x] np.subtract
- [x] np.true_divide
- [x] np.floor_divide
- [x] np.float_power
- [x] np.fmod
- [x] np.mod
- [ ] np.modf
- [ ] np.remainder
- [ ] np.divmod
- [ ] np.angle
- [ ] np.real
- [ ] np.imag
- [ ] np.conj
- [ ] np.conjugate
- [x] np.maximum
- [x] np.fmax
- [x] np.amax
- [ ] np.nanmax
- [x] np.minimum
- [x] np.fmin
- [x] np.amin
- [ ] np.nanmin
- [ ] np.convolve
- [ ] np.clip
- [x] np.sqrt
- [x] np.cbrt
- [x] np.square
- [x] np.absolute
- [x] np.fabs
- [x] np.sign
- [ ] np.heaviside
- [ ] np.nan_to_num
- [ ] np.real_if_close
- [ ] np.interp

Set routines
- [x] np.unique
- [x] np.in1d
- [ ] np.intersect1d
- [x] np.isin
- [ ] np.setdiff1d
- [ ] np.setxor1d
- [ ] np.union1d

Array creation routines
- [ ] np.empty
  - [x] ch5mpy.empty
- [ ] np.empty_like
- [ ] np.eye
- [ ] np.identity
- [ ] np.ones
  - [x] ch5mpy.ones
- [x] np.ones_like
- [ ] np.zeros
  - [x] ch5mpy.zeros
- [x] np.zeros_like
- [ ] np.full
  - [x] ch5mpy.full
- [ ] np.full_like
- [x] np.array
- [x] np.asarray
- [x] np.asanyarray
- [ ] np.ascontiguousarray
- [ ] np.asmatrix
- [x] np.copy
- [ ] np.frombuffer
- [ ] np.from_dlpack
- [ ] np.fromfile
- [ ] np.fromfunction
- [ ] np.fromiter
- [ ] np.fromstring
- [ ] np.loadtxt
- [ ] np.core.records.array
- [ ] np.core.records.fromarrays
- [ ] np.core.records.fromrecords
- [ ] np.core.records.fromstring
- [ ] np.core.records.fromfile
- [ ] np.core.defchararray.array
- [ ] np.core.defchararray.asarray
- [ ] np.arange
- [ ] np.linspace
- [ ] np.logspace
- [ ] np.geomspace
- [ ] np.meshgrid
- [ ] np.mgrid
- [ ] np.ogrid
- [ ] np.diag
- [ ] np.diagflat
- [ ] np.tri
- [ ] np.tril
- [ ] np.triu
- [ ] np.vander
- [ ] np.mat
- [ ] np.bmat

Array manipulation routines
- [ ] np.copyto
- [x] np.shape
- [ ] np.reshape
- [x] np.ravel
- [ ] np.ndarray.flat
- [ ] np.ndarray.flatten
- [ ] np.moveaxis
- [ ] np.rollaxis
- [ ] np.swapaxes
- [x] np.ndarray.T
- [x] np.transpose
- [ ] np.atleast_1d
- [ ] np.atleast_2d
- [ ] np.atleast_3d
- [ ] np.broadcast
- [ ] np.broadcast_to
- [x] np.broadcast_arrays
- [ ] np.expand_dims
- [ ] np.squeeze
- [ ] np.asarray
- [ ] np.asanyarray
- [ ] np.asmatrix
- [ ] np.asfarray
- [ ] np.asfortranarray
- [ ] np.ascontiguousarray
- [ ] np.asarray_chkfinite
- [ ] np.require
- [x] np.concatenate
- [ ] np.stack
- [ ] np.block
- [x] np.vstack
- [x] np.hstack
- [ ] np.dstack
- [ ] np.column_stack
- [ ] np.row_stack
- [x] np.split
- [ ] np.array_split
- [ ] np.dsplit
- [ ] np.hsplit
- [ ] np.vsplit
- [ ] np.tile
- [x] np.repeat
- [x] np.delete
- [x] np.insert
- [ ] np.append
- [ ] np.resize
- [ ] np.trim_zeros
- [x] np.unique
- [ ] np.flip
- [ ] np.fliplr
- [ ] np.flipud
- [ ] np.reshape
- [ ] np.roll
- [ ] np.rot90

Sorting, searching, and counting
- [ ] np.sort
- [ ] np.lexsort
- [ ] np.argsort
- [ ] np.ndarray.sort
- [ ] np.sort_complex
- [ ] np.partition
- [ ] np.argpartition
- [ ] np.argmax
- [ ] np.nanargmax
- [ ] np.argmin
- [ ] np.nanargmin
- [ ] np.argwhere
- [ ] np.nonzero
- [ ] np.flatnonzero
- [ ] np.where
- [x] np.searchsorted
- [ ] np.extract
- [ ] np.count_nonzero

Random
- [x] beta
- [x] binomial
- [x] bytes
- [x] chisquare
- [x] choice
- [x] dirichlet
- [x] exponential
- [x] f
- [x] gamma
- [x] get_state
- [x] geometric
- [x] gumbel
- [x] hypergeometric
- [x] laplace
- [x] logistic
- [x] lognormal
- [x] logseries
- [x] multinomial
- [x] multivariate_normal
- [x] negative_binomial
- [x] noncentral_chisquare
- [x] noncentral_f
- [x] normal
- [x] pareto
- [x] permutation
- [x] poisson
- [x] power
- [x] rand
- [x] randint
- [x] randn
- [x] random
- [x] random_integers
- [x] random_sample
- [x] rayleigh
- [x] seed
- [x] set_state
- [x] shuffle
- [x] standard_cauchy
- [x] standard_exponential
- [x] standard_gamma
- [x] standard_normal
- [x] standard_t
- [x] triangular
- [x] uniform
- [x] vonmises
- [x] wald
- [x] weibull
- [x] zipf

Misc
- [x] np.ndim
