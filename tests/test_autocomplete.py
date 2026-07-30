"""
Test that auto-completion works through the nested structures.

This is the whole point of wrapping the strongly typed Julia API, so it is worth a test of its own: a refactor that
replaces the declared fields with something else would still pass all the other tests.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,missing-function-docstring
# flake8: noqa: F403,F405

from typing import Sequence

import jedi  # type: ignore

import somegraphspy as sg


def _completions(code: str) -> Sequence[str]:
    return [completion.name for completion in jedi.Script(code="import somegraphspy as sg\n" + code).complete()]


def test_complete_the_fields_of_a_configuration() -> None:
    names = _completions("sg.PointsGraphConfiguration().")
    for name in ("figure", "x_axis", "y_axis", "points", "borders", "edges", "edges_over_points"):
        assert name in names


def test_complete_through_nested_fields() -> None:
    names = _completions("sg.PointsGraphConfiguration().figure.")
    for name in ("margins", "width", "height", "template", "background_color"):
        assert name in names

    names = _completions("sg.PointsGraphConfiguration().points.colors.axis.")
    for name in ("minimum", "maximum", "log_scale", "percent", "title"):
        assert name in names


def test_complete_the_fields_of_a_graph() -> None:
    names = _completions("sg.points_graph().")
    for name in ("data", "configuration", "figure", "json", "save", "show", "validate", "flip_axes"):
        assert name in names

    names = _completions("sg.points_graph().data.")
    for name in ("points_xs", "points_ys", "points_colors", "figure_title"):
        assert name in names


def test_complete_the_values_of_an_enum() -> None:
    names = _completions("sg.LineStyle.")
    for name in ("SolidLine", "DashLine", "DotLine", "DashDotLine"):
        assert name in names

    names = _completions("sg.DistributionStyle.")
    for name in ("CurveDistribution", "ViolinDistribution", "BoxDistribution", "CumulativeDistribution"):
        assert name in names


def test_dir_lists_the_fields_at_run_time() -> None:
    names = dir(sg.PointsGraphConfiguration())
    for name in ("figure", "x_axis", "edges_over_points"):
        assert name in names

    names = dir(sg.PointsGraphConfiguration().figure)
    for name in ("margins", "width", "height"):
        assert name in names


def test_the_enums_namespace_lists_all_the_enums() -> None:
    names = _completions("sg.enums.")
    for name in sg.enums.__all__:
        assert name in names

    # Typing a couple of letters is enough to get to the namespace.
    assert "enums" in _completions("sg.e")


def test_the_enums_namespace_holds_the_same_types() -> None:
    for name in sg.enums.__all__:
        assert getattr(sg.enums, name) is getattr(sg, name)
