"""
Record what Julia compiles while our public functions run (for internal use).

Set ``METACELLS_TRACE_COMPILE`` to a directory before importing any of our packages to enable this. Each process then
writes two files there. ``<pid>.trace.jl`` is Julia's own compile trace. ``<pid>.compiles.jsonl`` holds one JSON line
per outermost call of a public function which compiled something. Each line says which function was called, with what
kind of arguments, from where, and what Julia compiled for it. Calls which compiled nothing are not written.

To summarize the records of a directory, run ``python -m dafpy.compile_tracing <directory>``, or
``python -m somegraphspy.compile_tracing <directory>`` where only ``somegraphspy`` is installed. What it lists is what the
precompiled workloads do not cover yet. It lists it twice. First per call of our Python packages, for their
``workloads.py``, which serves Python users. Then per method of our Julia packages, with Python types as Julia ones, for
their ``Workloads`` module, which serves Julia users.

``dafpy`` and ``somegraphspy`` each hold an identical copy of this module, since neither depends on the other.
"""

import functools
import inspect
import json
import os
import re
import sys
import threading
import warnings
from collections import defaultdict
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

__all__ = ["configure_julia", "wrap_package", "report"]

#: The environment variable which enables this, naming the directory to write to.
SWITCH = "METACELLS_TRACE_COMPILE"

# Our packages. A call site is the first frame of the stack which is outside all of them.
OUR_PACKAGES = ("dafpy", "somegraphspy", "metacellspy", "metacellsgraphspy", "metacellswidgets")

# The methods of a class which are wrapped beside its public ones, since some of our API goes through them (e.g.,
# ``daf["@ cell : age"]``, or constructing a wrapper of a Julia value).
WRAPPED_DUNDERS = ("__init__", "__getitem__", "__setitem__", "__contains__", "__call__")

# A call which compiled for less than this, and wrote no trace lines, is taken to have compiled nothing.
MIN_COMPILE_SECONDS = 0.001

# Our Julia packages. A compiled method belongs to the first of these its line names, for that package's workload.
OUR_JULIA_PACKAGES = ("MetacellsGraphs", "Metacells", "SomeGraphs", "DataAxesFormats", "TanayLabUtilities")

# PythonCall's wrappers of Python values, and the Julia types a Julia user would pass instead.
JULIA_TYPE_OF_PYTHON_TYPE = (
    (re.compile(r"PythonCall\.PyArray\{([^{},]+), ([0-9]+), [^{}]*\}"), r"Array{\1, \2}"),  # NOT F-STRING
    (re.compile(r"PythonCall\.PyList\{([^{}]+)\}"), r"Vector{\1}"),  # NOT F-STRING
    (re.compile(r"PythonCall\.PyDict\{([^{},]+), ([^{}]+)\}"), r"Dict{\1, \2}"),  # NOT F-STRING
    (re.compile(r"PythonCall\.Py\b"), "Py"),
)

# A line of Julia's compile trace, when it is written with its timing.
TRACE_LINE = re.compile(r"^#=\s*([0-9.]+) ms =# (precompile\(.*\))( # recompile)?$")

# Whether a call of a wrapped function is in progress in this thread, so only the outermost call is recorded.
STATE = threading.local()

# The Julia function which returns the total compile time so far, created when the package is wrapped.
COMPILE_SECONDS: List[Any] = []


def trace_directory() -> Optional[str]:
    """
    The directory to write to, if tracing is enabled (for internal use).
    """
    return os.environ.get(SWITCH) or None


def trace_path(directory: str) -> str:
    """
    The path of Julia's compile trace of this process (for internal use).
    """
    return os.path.join(directory, f"{os.getpid()}.trace.jl")


def records_path(directory: str) -> str:
    """
    The path of the records of this process (for internal use).
    """
    return os.path.join(directory, f"{os.getpid()}.compiles.jsonl")


def configure_julia() -> None:
    """
    If tracing is enabled, make Julia write its compile trace (for internal use).

    This must be called before ``juliacall`` is imported, since that is when it reads how to start Julia.
    """
    directory = trace_directory()
    if directory is None:
        return

    if "juliacall" in sys.modules:
        if os.environ.get("PYTHON_JULIACALL_TRACE_COMPILE") != trace_path(directory):
            warnings.warn(
                f"{SWITCH} is set, but Julia was started before any of our packages was imported, so nothing is traced"
            )
        return

    os.makedirs(directory, exist_ok=True)
    os.environ["PYTHON_JULIACALL_TRACE_COMPILE"] = trace_path(directory)
    os.environ["PYTHON_JULIACALL_TRACE_COMPILE_TIMING"] = "yes"


def is_tracing() -> bool:
    """
    Whether Julia writes the compile trace this records from (for internal use).
    """
    directory = trace_directory()
    return directory is not None and os.environ.get("PYTHON_JULIACALL_TRACE_COMPILE") == trace_path(directory)


def wrap_package(package_name: str) -> None:
    """
    If tracing is enabled, wrap the public functions of a package so each records what Julia compiles while it runs
    (for internal use).

    This wraps the functions each module of the package lists in its ``__all__``, and the public methods of the classes
    it lists there. A wrapped function replaces the original everywhere in the package that names it.
    """
    if not is_tracing():
        return

    from juliacall import Main  # type: ignore # pylint: disable=import-outside-toplevel

    Main.seval("Base.cumulative_compile_timing(true)")
    COMPILE_SECONDS.append(Main.seval("() -> sum(Base.cumulative_compile_time_ns()) / 1e9"))
    COMPILE_SECONDS[0]()

    modules = [
        module
        for name, module in list(sys.modules.items())
        if (name == package_name or name.startswith(package_name + ".")) and name != __name__
    ]

    wrapper_of_function: Dict[int, Callable] = {}
    for module in modules:
        for name in getattr(module, "__all__", []):
            value = getattr(module, name, None)
            if inspect.isfunction(value) and id(value) not in wrapper_of_function:
                wrapper_of_function[id(value)] = wrapped(value)
            elif inspect.isclass(value) and value.__module__.startswith(package_name):
                wrap_class(value)

    for module in modules:
        for name, value in list(vars(module).items()):
            wrapper = wrapper_of_function.get(id(value))
            if wrapper is not None:
                setattr(module, name, wrapper)


def wrap_class(cls: type) -> None:
    """
    Wrap the public methods of a class in place (for internal use).
    """
    for name, value in list(vars(cls).items()):
        if name.startswith("_") and name not in WRAPPED_DUNDERS:
            continue
        if isinstance(value, staticmethod):
            setattr(cls, name, staticmethod(wrapped(value.__func__)))
        elif isinstance(value, classmethod):
            setattr(cls, name, classmethod(wrapped(value.__func__)))
        elif inspect.isfunction(value) and not getattr(value, "__wrapped_for_tracing__", False):
            setattr(cls, name, wrapped(value))


def wrapped(function: Callable) -> Callable:
    """
    A wrapper of a function which records what Julia compiles while it runs, if it is the outermost wrapped call
    (for internal use).
    """

    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if getattr(STATE, "is_in_call", False):
            return function(*args, **kwargs)

        directory = trace_directory()
        assert directory is not None
        STATE.is_in_call = True
        offset = trace_size(directory)
        compile_seconds = COMPILE_SECONDS[0]()
        try:
            return function(*args, **kwargs)
        finally:
            STATE.is_in_call = False
            record(
                directory,
                function,
                args=args,
                kwargs=kwargs,
                offset=offset,
                compile_seconds=float(COMPILE_SECONDS[0]() - compile_seconds),
            )

    setattr(wrapper, "__wrapped_for_tracing__", True)
    return wrapper


def trace_size(directory: str) -> int:
    """
    The size of Julia's compile trace so far (for internal use).
    """
    path = trace_path(directory)
    return os.path.getsize(path) if os.path.exists(path) else 0


def record(
    directory: str,
    function: Callable,
    *,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    offset: int,
    compile_seconds: float,
) -> None:
    """
    Write the record of a call, if it compiled anything (for internal use).
    """
    path = trace_path(directory)
    if not os.path.exists(path):
        return
    with open(path, encoding="utf8") as file:
        file.seek(offset)
        trace = file.read()

    compiled = []
    for line in trace.splitlines():
        match = TRACE_LINE.match(line)
        if match is not None:
            compiled.append(
                {
                    "milliseconds": float(match.group(1)),
                    "statement": match.group(2),
                    "is_recompile": match.group(3) is not None,
                }
            )
    if not compiled and compile_seconds < MIN_COMPILE_SECONDS:
        return

    entry = {
        "callable": f"{function.__module__}.{function.__qualname__}",
        "arguments": arguments_summary(function, args, kwargs),
        "call_site": call_site(),
        "compile_seconds": round(compile_seconds, 4),
        "compiled": compiled,
    }
    with open(records_path(directory), "a", encoding="utf8") as file:
        file.write(json.dumps(entry) + "\n")


def arguments_summary(function: Callable, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Dict[str, str]:
    """
    A short description of the kind of each argument of a call (for internal use).
    """
    try:
        bound = inspect.signature(function).bind_partial(*args, **kwargs)
    except (TypeError, ValueError):
        return {"*args": ", ".join(value_summary(value) for value in args)}
    return {name: value_summary(value) for name, value in bound.arguments.items()}


def value_summary(value: Any) -> str:
    """
    A short description of the kind of a value, which says what Julia compiles for (for internal use).
    """
    type_name = type(value).__name__
    if hasattr(value, "jl_obj"):
        from juliacall import Main  # type: ignore # pylint: disable=import-outside-toplevel

        return f"{type_name}({Main.nameof(Main.typeof(value.jl_obj))})"
    if hasattr(value, "dtypes") and hasattr(value, "shape") and not hasattr(value, "dtype"):
        return f"{type_name}[{value.shape}]"
    if hasattr(value, "dtype") and hasattr(value, "shape"):
        return f"{type_name}[{value.dtype}, {value.shape}]"
    if isinstance(value, (list, tuple, set)):
        element_types = sorted({type(element).__name__ for element in value})
        return f"{type_name}[{', '.join(element_types)}, {len(value)}]"
    if isinstance(value, dict):
        return f"dict[{len(value)}]"
    return type_name


def call_site() -> str:
    """
    The file and line of the first frame of the stack which is outside our packages (for internal use).
    """
    our_directories = [
        os.path.dirname(module.__file__)
        for name in OUR_PACKAGES
        if (module := sys.modules.get(name)) is not None and module.__file__ is not None
    ]
    frame = sys._getframe(1)  # pylint: disable=protected-access
    while frame is not None:
        filename = frame.f_code.co_filename
        if not any(filename.startswith(directory) for directory in our_directories):
            return f"{filename}:{frame.f_lineno}"
        frame = frame.f_back  # type: ignore
    return "?"


def report(directory: str) -> str:
    """
    Summarize the records of a directory, per called function, most compile time first (for internal use).
    """
    calls: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for name in sorted(os.listdir(directory)):
        if name.endswith(".compiles.jsonl"):
            with open(os.path.join(directory, name), encoding="utf8") as file:
                for line in file:
                    entry = json.loads(line)
                    calls[entry["callable"]].append(entry)

    lines = ["What compiled in each call of our Python packages (for their workloads.py):"]
    for callable_name, entries in sorted(calls.items(), key=lambda item: -total_compile_seconds(item[1])):
        lines += callable_report(callable_name, entries)
    lines += ["", "What compiled of each of our Julia packages, with Python types as Julia ones (for their Workloads):"]
    lines += julia_report(calls)
    return "\n".join(lines)


def julia_report(calls: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    """
    The lines of the report about the methods of each of our Julia packages, for Julia users (for internal use).
    """
    milliseconds_of_statement_of_package: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for entries in calls.values():
        for entry in entries:
            for compiled in entry["compiled"]:
                statement = julia_statement(compiled["statement"])
                package = None if statement is None else julia_package(statement)
                if statement is not None and package is not None:
                    milliseconds_of_statement_of_package[package][statement] += compiled["milliseconds"]

    lines = []
    for package in OUR_JULIA_PACKAGES:
        milliseconds_of_statement = milliseconds_of_statement_of_package.get(package)
        if milliseconds_of_statement:
            lines.append(f"{package}:")
            for statement, milliseconds in sorted(milliseconds_of_statement.items(), key=lambda item: -item[1]):
                lines.append(f"    {milliseconds:8.1f} ms {statement}")
    return lines


def julia_statement(statement: str) -> Optional[str]:
    """
    A compiled method as a Julia user would need it, with Python types as Julia ones, or ``None`` if only Python needs
    it (for internal use).
    """
    if statement.startswith("precompile(Tuple{typeof(PythonCall."):  # NOT F-STRING
        return None
    for pattern, replacement in JULIA_TYPE_OF_PYTHON_TYPE:
        statement = pattern.sub(replacement, statement)
    return statement


def julia_package(statement: str) -> Optional[str]:
    """
    The first of our Julia packages a compiled method names, if any (for internal use).
    """
    for package in OUR_JULIA_PACKAGES:
        if f"{package}." in statement:
            return package
    return None


def total_compile_seconds(entries: List[Dict[str, Any]]) -> float:
    """
    The total compile time of some records (for internal use).
    """
    return sum(entry["compile_seconds"] for entry in entries)


def callable_report(callable_name: str, entries: List[Dict[str, Any]]) -> List[str]:
    """
    The lines of the report about the records of one called function (for internal use).
    """
    lines = [f"{callable_name}: {len(entries)} calls compiled {total_compile_seconds(entries):.2f} s"]
    for arguments in sorted({json.dumps(entry["arguments"], sort_keys=True) for entry in entries}):
        lines.append(f"    arguments: {arguments}")
    for site in sorted({entry["call_site"] for entry in entries}):
        lines.append(f"    called from: {site}")
    milliseconds_of_statement: Dict[str, float] = defaultdict(float)
    recompiled_statements = set()
    for entry in entries:
        for compiled in entry["compiled"]:
            milliseconds_of_statement[compiled["statement"]] += compiled["milliseconds"]
            if compiled["is_recompile"]:
                recompiled_statements.add(compiled["statement"])
    for statement, milliseconds in sorted(milliseconds_of_statement.items(), key=lambda item: -item[1]):
        # A recompile was cached, but a package this session loaded made it invalid. So it needs a workload of a package
        # built with that package loaded too, rather than one more call where it was cached.
        recompile = " # recompile" if statement in recompiled_statements else ""
        lines.append(f"    {milliseconds:8.1f} ms {statement}{recompile}")
    return lines


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Usage: python -m {__package__}.compile_tracing <directory>")
    print(report(sys.argv[1]))
