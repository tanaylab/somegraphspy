"""
Import the Julia environment.

This provides additional functionality on top of ``juliapkg`` (which automatically downloads Julia packages for us). It
will import the ``juliacall`` module to create a Julia environment (as ``jl``), and uses it to import the
``SomeGraphs.jl`` Julia package.

You can control the behavior using the following environment variables:

* ``PYTHON_JULIACALL_HANDLE_SIGNALS`` (by default, ``yes``). This is needed to avoid segfaults when calling
  Julia from Python.

* ``PYTHON_JULIACALL_THREADS`` (by default, ``auto``). By default Julia will use all the threads available
  in the machine. On machines with hyper-threading you may want to specify only half the number of threads (that is,
  just have one thread per physical core) as that should provide better performance for compute-intensive (as opposed to
  IO-intensive) code.

* ``PYTHON_JULIACALL_OPTLEVEL`` (by default, ``3``).

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

__all__ = ["jl", "jl_version", "DefaultValue", "DEFAULT", "JlEnum", "JlObject", "use_default_julia_environment"]

# Check if JuliaCall is already loaded. If not, setup sensible defaults. If it was loaded manually, warn the user about
# the relevant environment variables.
if "juliacall" not in sys.modules:
    # TODO: Remove these when juliapkg lets you specify this.
    for k, default in (
        ("PYTHON_JULIACALL_HANDLE_SIGNALS", "yes"),
        ("PYTHON_JULIACALL_THREADS", "auto"),
        ("PYTHON_JULIACALL_OPTLEVEL", "3"),
    ):
        os.environ[k] = os.environ.get(k, default)

    # When using the default Julia environment (the default), point juliacall directly at the default Julia binary and
    # its global package environment, bypassing juliapkg. Otherwise juliapkg populates its own isolated project and
    # re-installs everything, which fails for locally-developed packages (e.g., SomeGraphs) that aren't in the
    # General registry. juliacall honors ``PYTHON_JULIACALL_EXE`` and ``PYTHON_JULIACALL_PROJECT`` only when both are
    # set, so we compute both and set them together.
    if os.environ.get("PYTHON_JULIACALL_USE_DEFAULT_ENVIRONMENT", "yes") == "yes" and (
        "PYTHON_JULIACALL_EXE" not in os.environ and "PYTHON_JULIACALL_PROJECT" not in os.environ
    ):
        import subprocess  # pylint: disable=import-outside-toplevel

        # Resolve the juliaup shim to the real binary; juliacall derives the system image location from the executable
        # path, and the shim directory has no ``lib/julia``.
        julia_exe = shutil.which("julia")
        if julia_exe is not None:
            julia_exe = os.path.realpath(julia_exe)

            # The default environment path is ``~/.julia/environments/v<MAJOR>.<MINOR>``, so we query the Julia binary
            # for its version to construct the path.
            try:
                julia_version_output = subprocess.run(
                    [julia_exe, "--version"],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                ).stdout
                # Output looks like: "julia version 1.12.5"
                julia_ver_tokens = julia_version_output.strip().split()
                julia_semver = julia_ver_tokens[-1].split(".")
                julia_minor_env = f"v{julia_semver[0]}.{julia_semver[1]}"  # pylint: disable=invalid-name
                julia_depot = os.environ.get("JULIA_DEPOT_PATH", os.path.join(os.path.expanduser("~"), ".julia")).split(
                    os.pathsep
                )[0]
                os.environ["PYTHON_JULIACALL_EXE"] = julia_exe
                os.environ["PYTHON_JULIACALL_PROJECT"] = os.path.join(julia_depot, "environments", julia_minor_env)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError, IndexError):
                pass

if os.environ.get("PYTHON_JULIACALL_PROPER_IMPORT", "") == "":
    # Required to avoid segfaults (https://juliapy.github.io/PythonCall.jl/dev/faq/)
    if os.environ.get("PYTHON_JULIACALL_HANDLE_SIGNALS", "yes") != "yes":
        warnings.warn(
            "PYTHON_JULIACALL_HANDLE_SIGNALS environment variable is set to something other than 'yes'. "
            "You will experience segfaults if running with multithreading."
        )

    if os.environ.get("PYTHON_JULIACALL_THREADS", "auto") != "auto":
        warnings.warn(
            "PYTHON_JULIACALL_THREADS environment variable is set to something other than 'auto', "
            "You may wish to set it to 'auto' for full use of your CPU."
        )

# Only the first Python package to import Julia records itself here, so importing several of them (in any order) does
# not lose the marker that the environment variables above were already dealt with.
if os.environ.get("PYTHON_JULIACALL_PROPER_IMPORT", "") == "":
    os.environ["PYTHON_JULIACALL_PROPER_IMPORT"] = "somegraphspy"

from juliacall import AnyValue  # type: ignore # isort: skip
from juliacall import Main  # type: ignore # isort: skip

#: The interface to the Julia run-time.
jl = Main


def use_default_julia_environment() -> None:
    """
    Force JuliaCall to use your default environment (whatever that is). By default JuliaCall creates its own separate
    independent environment, which means that it re-downloads and re-installs all the dependency packages there.
    This is nice if you don't otherwise use Julia and/or don't care about the wasted disk space and initial installation
    time and manual control over package versions. It sucks if you do otherwise use Julia, and/or you want manual
    control over the version of some of the packages (e.g., if you are actively developing them). You would think
    there would a built-in method for doing this in JuliaCall, right?

    To make this easier (and trigger it before actually importing packages), you can set the
    ``PYTHON_JULIACALL_USE_DEFAULT_ENVIRONMENT`` environment variable to ``yes``, and then ``import somegraphspy`` will
    call ``use_default_julia_environment`` for you. Sigh.
    """
    default_env = jl.seval('joinpath(DEPOT_PATH[1], "environments", "v$(VERSION.major).$(VERSION.minor)")')
    jl.seval('using Pkg; Pkg.activate("' + default_env + '")')


if os.environ.get("PYTHON_JULIACALL_USE_DEFAULT_ENVIRONMENT", "yes") == "yes":
    use_default_julia_environment()

#: The version of Julia being used.
jl_version = (jl.VERSION.major, jl.VERSION.minor, jl.VERSION.patch)

jl.seval("using Pkg")

# Everything is imported rather than ``using``, so no package's exports leak into Julia's ``Main``. This keeps
# ``Main`` clear for other Python packages that wrap Julia packages and are used in the same session.
for package in ("PythonCall", "SomeGraphs"):
    if jl.seval('Base.find_package("' + package + '")') is None:
        jl.seval('Pkg.add("' + package + '")')
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
