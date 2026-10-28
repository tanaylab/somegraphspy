"""
Test the Julia environment set up by ``SomeGraphs``, and the delegation to the wrapped Julia objects.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,missing-function-docstring
# flake8: noqa: F403,F405

import copy
import json
import os
import tomllib
from typing import Any
from typing import Collection

import numpy as np
import pytest

import somegraphspy
from somegraphspy.julia_import import _GLUE_PROJECT_PATH
from somegraphspy.julia_import import DEFAULT
from somegraphspy.julia_import import JlObject
from somegraphspy.julia_import import _given
from somegraphspy.julia_import import _to_julia
from somegraphspy.julia_import import jl

#: Names exported by the Julia package we wrap. Importing (rather than ``using``) it keeps these out of ``Main``.
EXPORTED_NAMES = ("Graph", "PointsGraph", "graph_to_json", "points_graph", "save_graph", "validate")


def _configuration() -> JlObject:
    return JlObject(jl.SomeGraphs.PointsGraphConfiguration())


def test_wrapped_package_does_not_leak() -> None:
    assert jl.seval("isdefined(Main, :SomeGraphsPy)")
    for name in EXPORTED_NAMES:
        assert not jl.seval(f"isdefined(Main, :{name})"), f"the exported {name} leaked into Julia's Main"


def _glue_project() -> dict[str, Any]:
    with open(_GLUE_PROJECT_PATH, "rb") as file:
        return tomllib.load(file)


def test_glue_version_is_the_package_version() -> None:
    assert _glue_project()["version"] == somegraphspy.__version__


def _dependencies_of(package: str) -> Collection[str]:
    # The dependencies a Julia package's own ``Project.toml`` lists, if it is loaded in ``Main``.
    if not jl.seval(f"isdefined(Main, :{package})"):
        return ()
    directory = jl.seval(f"pkgdir({package})")
    if directory is None:
        return ()
    with open(os.path.join(str(directory), "Project.toml"), "rb") as file:
        return tomllib.load(file).get("deps", {})


def test_url_packages_are_glue_dependencies() -> None:
    # A package comes by URL when it is not registered. It is a dependency of SomeGraphsPy, or of one of SomeGraphsPy's
    # dependencies.
    with open(os.path.join(os.path.dirname(somegraphspy.__file__), "juliapkg.json"), encoding="utf8") as file:
        packages = json.load(file)["packages"]
    glue_packages = _glue_project()["deps"]
    for name, package in packages.items():
        if "url" in package and name != "SomeGraphsPy":
            assert name in glue_packages or any(
                name in _dependencies_of(glue_package) for glue_package in glue_packages
            ), f"the URL package {name} of juliapkg.json is not a dependency of SomeGraphsPy, nor of its dependencies"


def test_read_and_write_fields() -> None:
    configuration = _configuration()
    assert configuration.edges_over_points is True

    configuration.edges_over_points = False
    assert configuration.edges_over_points is False


def test_nested_fields_are_shared() -> None:
    configuration = _configuration()
    configuration.figure.width = 800
    assert configuration.figure.width == 800

    other = _configuration()
    other.figure = configuration.figure
    other.figure.width = 400
    assert configuration.figure.width == 400, "assignment should share the figure, exactly as it does in Julia"


def test_copy_is_independent() -> None:
    configuration = _configuration()
    configuration.figure.width = 800

    duplicate = configuration.copy()
    duplicate.figure.width = 400

    assert configuration.figure.width == 800
    assert duplicate.figure.width == 400


def test_julia_validates_written_fields() -> None:
    configuration = _configuration()
    try:
        configuration.edges_over_points = "not a boolean"
        raise AssertionError("Julia accepted an invalid field value")
    except Exception:  # pylint: disable=broad-exception-caught
        pass


def test_dir_lists_the_julia_fields() -> None:
    names = dir(_configuration())
    for name in ("figure", "x_axis", "y_axis", "points", "borders", "edges", "edges_over_points"):
        assert name in names


def test_default_is_not_none() -> None:
    assert _given(figure=DEFAULT, width=None, height=8) == {"width": None, "height": 8}


def test_default_repr() -> None:
    assert repr(DEFAULT) == "DEFAULT"


def test_copied_default_is_default() -> None:
    assert copy.copy(DEFAULT) is DEFAULT
    assert copy.deepcopy({"palette": DEFAULT})["palette"] is DEFAULT


def _is_julia_strings_vector(value: Any) -> bool:
    return bool(jl.seval("value -> value isa AbstractVector{<:AbstractString}")(value))  # NOT F-STRING


def test_to_julia_of_strings() -> None:
    for value in (np.array(["a", "b"], dtype=object), np.array([b"a", b"b"])):
        converted = _to_julia(value)
        assert _is_julia_strings_vector(converted), f"not a vector of strings: {value.dtype}"
        assert [str(entry) for entry in converted] == ["a", "b"]


def test_to_julia_of_pandas_strings() -> None:
    pd = pytest.importorskip("pandas")
    for value in (pd.Series(["a", "b"]), pd.Index(["a", "b"]), pd.Categorical(["a", "b"])):
        converted = _to_julia(value)
        assert _is_julia_strings_vector(converted), f"not a vector of strings: {type(value)}"
        assert [str(entry) for entry in converted] == ["a", "b"]


def test_to_julia_of_numbers() -> None:
    converted = _to_julia(np.array([1, 2], dtype=object))
    assert converted.dtype == np.int64
    assert list(converted) == [1, 2]


def test_to_julia_rejects_missing_strings() -> None:
    with pytest.raises(TypeError, match="entry 0 is a str and whose entry 1 is a NoneType"):
        _to_julia(np.array(["a", None], dtype=object))

    with pytest.raises(TypeError, match="an array of NoneType"):
        _to_julia(np.array([None, None], dtype=object))
