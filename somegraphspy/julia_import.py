"""
Import the Julia environment.

This imports the ``juliacall`` module to obtain a Julia run-time (as ``jl``), and uses it to import the
``SomeGraphs.jl`` Julia package.

How Julia is run, and which Julia is run, is left to ``juliacall``, and is configured by its own environment variables,
which must be set before importing anything that reaches Julia. This adds one thing to them: ``@default``.

By default ``juliacall`` has ``juliapkg`` install a Julia of its own, and an environment of its own, and populates that
environment with what each installed Python package declares in its ``juliapkg.json``. That is a reasonable default, and
it is not always what you want: if you use Julia yourself, it means a second copy of everything, which you cannot see
from a Julia prompt, and whose versions you do not choose.

``juliacall`` can be pointed at a Julia instead, through ``PYTHON_JULIACALL_EXE`` and ``PYTHON_JULIACALL_PROJECT``, but
it has no way to say "the Julia I already have": the first must be an executable and the second a directory which
exists. Setting either of them to ``@default`` here means exactly that - the ``julia`` in the path, and the environment
that Julia would use by itself, which it is asked for rather than being worked out from the depot and the version.
They are expanded before ``juliacall`` sees them, and are independent, so one may be ``@default`` while the other is
given explicitly.

Setting them is a deliberate act, so nothing is assumed if you do not. In particular ``PYTHON_JULIACALL_THREADS`` and
``PYTHON_JULIACALL_HANDLE_SIGNALS`` are left exactly as you set them: Julia runs on one thread unless you ask for more,
and asking for more without also setting the signal handling to ``yes`` is what makes it crash. ``juliacall`` warns
about that combination itself; this warns, once, about the single thread, which nothing else would tell you about.

Three packages provide this expansion: ``dafpy``, ``somegraphspy``, and ``metacellspy`` (transitively, through
``dafpy``). Importing any of them expands ``@default``, so the order does not matter. If ``juliacall`` is imported
before any of them, it sees ``@default`` itself, and rejects it as a path which does not exist, naming the variable it
could not use. That is why this is a value of a variable ``juliacall`` reads, rather than a variable of our own, which
it would silently ignore.

This code is based on the code from the ``pysr`` Python package, adapted to our needs. TODO: Much of this is replicated
in all our Python packages that invoke Julia.
"""

import os
import shutil
import sys
import warnings
from enum import Enum
from typing import Any
from typing import Mapping
from typing import MutableMapping
from typing import Sequence
from typing import Type
from typing import Union

import numpy as np

__all__ = ["jl", "jl_version", "DefaultValue", "DEFAULT", "JlEnum", "JlObject"]

# The value of ``PYTHON_JULIACALL_EXE`` or ``PYTHON_JULIACALL_PROJECT`` asking for the Julia you already have, rather
# than the one ``juliapkg`` would install for itself. Not exported: it has to be in the environment before anything
# which reaches Julia is imported, so by the time it could be read from here it would be too late to use.
_DEFAULT_JULIA = "@default"


def _default_julia_exe() -> str:
    """
    Return the path of the Julia which is in the path (for internal use).

    This is resolved to the real binary, because ``juliacall`` works out where Julia's system image is from the path of
    the executable it is given, and the directory holding ``juliaup``'s shim has no ``lib/julia`` beside it.
    """
    julia_exe = shutil.which("julia")
    if julia_exe is None:
        raise ValueError(f"PYTHON_JULIACALL_EXE={_DEFAULT_JULIA}: there is no julia in the path")
    return os.path.realpath(julia_exe)


def _default_julia_project(julia_exe: str) -> str:
    """
    Return the path of the default environment of some Julia (for internal use).

    Which environment that is depends on the depot, on the version, and on ``JULIA_PROJECT``, which conda sets to an
    environment named after the conda environment. It is therefore asked of that Julia rather than worked out here.
    """
    import subprocess  # pylint: disable=import-outside-toplevel

    try:
        return subprocess.run(
            [julia_exe, "-e", "print(dirname(Base.active_project()))"],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        ).stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exception:
        raise ValueError(
            f"PYTHON_JULIACALL_PROJECT={_DEFAULT_JULIA}: {julia_exe} did not report its default environment"
        ) from exception


# Expand the ``@default`` we accept in the two variables ``juliacall`` uses to locate Julia. It has no notion of "the
# Julia I already have": ``PYTHON_JULIACALL_EXE`` must be an executable and ``PYTHON_JULIACALL_PROJECT`` a directory
# which exists, and if neither is given then ``juliapkg`` installs a Julia and an environment of its own.
#
# This has to happen before ``juliacall`` is imported, since that is when it reads them. If something else imported it
# first, then it has already rejected ``@default`` as a path which does not exist - which is the point of using a value
# it cannot accept, rather than a variable of our own which it would silently ignore.
if os.environ.get("PYTHON_JULIACALL_EXE") == _DEFAULT_JULIA:
    os.environ["PYTHON_JULIACALL_EXE"] = _default_julia_exe()

if os.environ.get("PYTHON_JULIACALL_PROJECT") == _DEFAULT_JULIA:
    os.environ["PYTHON_JULIACALL_PROJECT"] = _default_julia_project(
        os.environ.get("PYTHON_JULIACALL_EXE") or _default_julia_exe()
    )

# How Julia is run is left as you set it. ``juliacall`` warns by itself when signal handling is unset and Julia has more
# than one thread, which is the combination that crashes; there is nobody to warn you that leaving both unset gives you
# a single-threaded Julia, so we do.
#
# Only when ``juliacall`` has not been imported yet, so this is said once even when several of ``dafpy``,
# ``somegraphspy`` and ``metacellspy`` are imported: the first of them ends by importing ``juliacall``, so the rest stay
# quiet. Recording it in the variable instead would not work - ``juliacall`` reads an empty value as an empty value, and
# refuses it.
if "juliacall" not in sys.modules and "PYTHON_JULIACALL_THREADS" not in os.environ:
    warnings.warn(
        "PYTHON_JULIACALL_THREADS is not set, so Julia will use a single thread. Set it to 'auto' to use the whole "
        "machine, and set PYTHON_JULIACALL_HANDLE_SIGNALS to 'yes' along with it, or Julia and Python will fight over "
        "signals and the process will die with a segfault."
    )

from juliacall import AnyValue  # type: ignore # isort: skip
from juliacall import Main  # type: ignore # isort: skip

#: The interface to the Julia run-time.
jl = Main


#: The version of Julia being used.
jl_version = (jl.VERSION.major, jl.VERSION.minor, jl.VERSION.patch)

# Everything is imported rather than ``using``, so no package's exports leak into Julia's ``Main``. This keeps
# ``Main`` clear for other Python packages that wrap Julia packages and are used in the same session.
for package in ("PythonCall", "SomeGraphs"):
    jl.seval("import " + package)

# Our own Julia code lives in a module of its own, for the same reason.
jl.seval("""
    module SomeGraphsPy

    using PythonCall

    function pyconvert_rule_jl_object(::Type{T}, x::Py) where {T}
        return PythonCall.pyconvert_return(pyconvert(T, x.jl_obj))
    end

    PythonCall.pyconvert_add_rule("somegraphspy.julia_import:JlObject", Any, pyconvert_rule_jl_object)

    # Build a vector of pairs of values, whose element type Julia infers from the (already converted) vectors. A list
    # of Python tuples would arrive as a ``PyList{Any}``, which Julia can't convert to a vector of tuples.
    function _tuples_vector(firsts::AbstractVector, seconds::AbstractVector)::AbstractVector
        return [(first, second) for (first, second) in zip(firsts, seconds)]
    end

    # Re-infer the element type of a vector whose entries are already Julia values. This turns the ``Vector{Any}`` we
    # get for a list of arrays or of objects into a properly typed vector.
    function _typed_vector(items::AbstractVector)::AbstractVector
        return [item for item in items]
    end

    # Classify an array by what its entries are, to pick the matching Python representation.
    function _array_kind(array::AbstractArray)::String
        element_type = eltype(array)
        if element_type <: Real
            return "numbers"
        elseif element_type <: AbstractString
            return "strings"
        else
            return "other"
        end
    end

    end  # module SomeGraphsPy
    """)


class JlEnum(Enum):
    """
    A Python base class for wrapping a Julia ``@enum`` type.

    The members are named exactly as the Julia values are, and their value is that name. Grouping them in a class (as
    opposed to listing them as separate constants) is what allows auto-completion to list the valid values of a field.
    """

    def __str__(self) -> str:
        return self.value


class DefaultValue:
    """
    A Python class for the value of a constructor parameter that was not specified.

    We can't use ``None`` for this because ``None`` is how one specifies Julia's ``nothing``, and not every field
    defaults to ``nothing`` (e.g., the ``rows_groups_gap`` of ``HeatmapGraphConfiguration`` defaults to ``1``).
    """


#: A Python value for a constructor parameter that was not specified, so the Julia default should be used instead.
DEFAULT = DefaultValue()

#: The Python class wrapping each of the Julia types, filled in by ``register_jl_type`` as the modules are imported.
PYTHON_CLASS_OF_JULIA_TYPE: MutableMapping[str, Union["Type[JlObject]", "Type[JlEnum]"]] = {}


def _to_julia(value: Any) -> Any:  # pylint: disable=too-many-return-statements
    # Anything not handled here is left to PythonCall, which converts it as needed for the (typed) Julia field.
    if isinstance(value, JlObject):
        return value.jl_obj

    if isinstance(value, JlEnum):
        return jl.getproperty(jl.SomeGraphs, jl.Symbol(value.value))

    # Strings have to go through ``numpy``; a plain Python list of them would arrive as a ``PyList{Any}``, which isn't
    # an ``AbstractVector{<:AbstractString}`` so Julia would reject it.
    if isinstance(value, np.ndarray) and value.dtype.type == np.str_:
        return jl.Vector(value)

    if isinstance(value, (list, tuple)) and len(value) > 0 and all(isinstance(entry, str) for entry in value):
        return jl.Vector(np.array(value, dtype=str))

    if isinstance(value, Mapping):
        return jl.Dict(jl.Vector([jl.Pair(key, _to_julia(entry)) for key, entry in value.items()]))

    if isinstance(value, (list, tuple)) and len(value) > 0 and all(_is_pair(entry) for entry in value):
        return jl.SomeGraphsPy._tuples_vector(
            jl.Vector([entry[0] for entry in value]), jl.Vector([entry[1] for entry in value])
        )

    if isinstance(value, (list, tuple)) and len(value) > 0:
        # A ``PyList{Any}`` is not an ``AbstractVector`` of anything specific, so Julia rejects it for a typed field.
        if all(isinstance(entry, (bool, int, float)) for entry in value):
            return np.array(value)
        return jl.SomeGraphsPy._typed_vector(jl.Vector([_to_julia(entry) for entry in value]))

    return value


def _is_pair(value: Any) -> bool:
    return isinstance(value, tuple) and len(value) == 2


def _from_julia(value: Any) -> Any:  # pylint: disable=too-many-return-statements
    if not isinstance(value, AnyValue):
        return value

    python_class = PYTHON_CLASS_OF_JULIA_TYPE.get(str(jl.nameof(jl.typeof(value))))
    if python_class is not None:
        if issubclass(python_class, JlEnum):
            return python_class(str(jl.string(value)))
        return python_class.wrap_jl_object(value)

    if bool(jl.isa(value, jl.AbstractDict)):
        return {str(key): _from_julia(jl.getindex(value, key)) for key in jl.keys(value)}

    if bool(jl.isa(value, jl.AbstractArray)):
        return _from_julia_array(value)

    if bool(jl.isa(value, jl.Tuple)):
        return tuple(_from_julia(entry) for entry in value)

    return value


def _from_julia_array(julia_array: Any) -> Any:
    # Only arrays of numbers and of strings become ``numpy`` arrays; anything else (a vector of vectors, of tuples, or
    # of wrapped objects) becomes a list, whose entries are converted individually.
    kind = str(jl.SomeGraphsPy._array_kind(julia_array))

    if kind == "numbers":
        return np.asarray(julia_array)

    if kind == "strings":
        return np.array([str(entry) for entry in julia_array], dtype=str)

    return [_from_julia(entry) for entry in julia_array]


def _given(**kwargs: Any) -> Mapping[str, Any]:
    """
    Collect the keyword arguments that were actually specified (for internal use).
    """
    return {name: _to_julia(value) for name, value in kwargs.items() if value is not DEFAULT}


class JlObject:
    """
    A Python base class for wrapping a Julia object.

    Reading a field returns the matching Julia field, wrapping it in the Python class of its type (if there is one) and
    converting Julia arrays to ``numpy`` arrays. Writing a field writes through to the Julia object, so Julia validates
    the value immediately. Nested objects are shared rather than copied, exactly as they are in Julia; that is, after
    ``configuration.figure = other.figure`` both configurations refer to the same figure configuration. Use ``copy`` if
    you need an independent one.
    """

    def __init__(self, jl_obj: Any) -> None:
        object.__setattr__(self, "jl_obj", jl_obj)

    def __getattr__(self, name: str) -> Any:
        # Only called for names that aren't real Python attributes, that is, for the (annotated) Julia fields. No Julia
        # field starts with an underscore, and Python (and IPython, when deciding how to display something) probes for
        # such names all the time, expecting an ``AttributeError`` rather than an error from Julia.
        if name.startswith("_"):
            raise AttributeError(name)
        try:
            return _from_julia(jl.getproperty(self.jl_obj, jl.Symbol(name)))
        except Exception as exception:  # pylint: disable=broad-exception-caught
            raise AttributeError(str(exception)) from None

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "jl_obj":
            object.__setattr__(self, name, value)
        else:
            # The Julia error is re-raised as a plain Python one holding just its text. Keeping the original would
            # keep the Julia exception object (and through it the Python value that caused it) alive in the traceback,
            # to be finalized only when the process exits, which crashes it.
            try:
                jl.setproperty_b(self.jl_obj, jl.Symbol(name), _to_julia(value))
            except Exception as exception:  # pylint: disable=broad-exception-caught
                raise RuntimeError(str(exception)) from None

    def __dir__(self) -> Sequence[str]:
        return sorted(set(super().__dir__()) | {str(field) for field in jl.fieldnames(jl.typeof(self.jl_obj))})

    def __str__(self) -> str:
        return str(jl.string(self.jl_obj))

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> Any:
        """
        Return an independent copy of the object, which shares nothing with the original.
        """
        return self.__class__.wrap_jl_object(jl.deepcopy(self.jl_obj))

    @classmethod
    def wrap_jl_object(cls, jl_obj: Any) -> Any:
        """
        Wrap a Julia object (for internal use).
        """
        instance = cls.__new__(cls)
        JlObject.__init__(instance, jl_obj)
        return instance


def register_jl_type(julia_type_name: str, python_class: Union[Type[JlObject], Type[JlEnum]]) -> None:
    """
    Associate a Julia type with the Python class that wraps it (for internal use).

    This is what allows reading a field of a wrapped object to return a wrapped object of the right class.
    """
    PYTHON_CLASS_OF_JULIA_TYPE[julia_type_name] = python_class
