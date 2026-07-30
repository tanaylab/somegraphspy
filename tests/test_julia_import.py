"""
Test the Julia environment set up by ``SomeGraphs``, and the delegation to the wrapped Julia objects.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,missing-function-docstring
# flake8: noqa: F403,F405

from somegraphspy.julia_import import DEFAULT
from somegraphspy.julia_import import JlObject
from somegraphspy.julia_import import _given
from somegraphspy.julia_import import jl

#: Names exported by the Julia package we wrap. Importing (rather than ``using``) it keeps these out of ``Main``.
EXPORTED_NAMES = ("Graph", "PointsGraph", "graph_to_json", "points_graph", "save_graph", "validate")


def _configuration() -> JlObject:
    return JlObject(jl.SomeGraphs.PointsGraphConfiguration())


def test_wrapped_package_does_not_leak() -> None:
    assert jl.seval("isdefined(Main, :SomeGraphsPy)")
    for name in EXPORTED_NAMES:
        assert not jl.seval(f"isdefined(Main, :{name})"), f"the exported {name} leaked into Julia's Main"


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
