"""
Test creating each of the graph types.

Each graph is built twice, once through the Python wrappers and once directly in Julia, and the resulting figures are
compared. This verifies the wrappers pass every value through unchanged, without restating what the Julia tests already
cover.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,missing-function-docstring
# flake8: noqa: F403,F405

import numpy as np
import plotly.graph_objects as go  # type: ignore
import pytest

import somegraphspy as sg
from somegraphspy.julia_import import jl

#: A Python graph and the Julia code building the identical graph.
GRAPHS = {
    "points": (
        sg.points_graph(points_xs=[1.0, 2.0, 3.0], points_ys=[1.0, 4.0, 9.0], figure_title="t"),
        'points_graph(; points_xs = [1.0, 2.0, 3.0], points_ys = [1.0, 4.0, 9.0], figure_title = "t")',
    ),
    "line": (
        sg.line_graph(points_xs=[1.0, 2.0, 3.0], points_ys=[1.0, 4.0, 9.0]),
        "line_graph(; points_xs = [1.0, 2.0, 3.0], points_ys = [1.0, 4.0, 9.0])",
    ),
    "lines": (
        sg.lines_graph(lines_points_xs=[[1.0, 2.0], [1.0, 3.0]], lines_points_ys=[[1.0, 2.0], [2.0, 4.0]]),
        "lines_graph(; lines_points_xs = [[1.0, 2.0], [1.0, 3.0]], lines_points_ys = [[1.0, 2.0], [2.0, 4.0]])",
    ),
    "bars": (
        sg.bars_graph(bars_values=[1.0, 2.0, 3.0], bars_names=["a", "b", "c"]),
        'bars_graph(; bars_values = [1.0, 2.0, 3.0], bars_names = ["a", "b", "c"])',
    ),
    "series_bars": (
        sg.series_bars_graph(series_bars_values=[[1.0, 2.0], [3.0, 4.0]], bars_names=["a", "b"]),
        'series_bars_graph(; series_bars_values = [[1.0, 2.0], [3.0, 4.0]], bars_names = ["a", "b"])',
    ),
    "distribution": (
        sg.distribution_graph(distribution_values=[0.0, 0.0, 1.0, 1.0, 1.0, 3.0]),
        "distribution_graph(; distribution_values = [0.0, 0.0, 1.0, 1.0, 1.0, 3.0])",
    ),
    "distributions": (
        sg.distributions_graph(distributions_values=[[0.0, 1.0, 1.0, 2.0], [1.0, 2.0, 2.0, 3.0]]),
        "distributions_graph(; distributions_values = [[0.0, 1.0, 1.0, 2.0], [1.0, 2.0, 2.0, 3.0]])",
    ),
    "heatmap": (
        sg.heatmap_graph(entries_values=np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])),
        "heatmap_graph(; entries_values = [1.0 2.0 3.0; 4.0 5.0 6.0])",
    ),
}


def _julia_json(julia_code: str) -> str:
    return str(jl.seval("SomeGraphs.graph_to_json(SomeGraphs." + julia_code + ")"))


@pytest.mark.parametrize("name", sorted(GRAPHS.keys()))
def test_graph_matches_julia(name: str) -> None:
    graph, julia_code = GRAPHS[name]
    graph.validate()
    assert graph.json == _julia_json(julia_code)


def test_heatmap_matrix_is_not_transposed() -> None:
    values = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    graph = sg.heatmap_graph(entries_values=values, rows_names=["r1", "r2"], columns_names=["c1", "c2", "c3"])
    graph.validate()

    read_back = graph.data.entries_values
    assert read_back is not None
    assert read_back.shape == values.shape
    assert read_back[0, 2] == values[0, 2]


def test_configuration_is_shared_with_the_graph() -> None:
    configuration = sg.PointsGraphConfiguration()
    graph = sg.points_graph(points_xs=[1.0, 2.0], points_ys=[1.0, 2.0], configuration=configuration)

    configuration.figure.width = 700
    assert graph.configuration.figure.width == 700


def test_flip_axes() -> None:
    graph = sg.points_graph(points_xs=[1.0, 2.0, 3.0], points_ys=[4.0, 5.0, 6.0])

    flipped = graph.flip_axes()
    assert list(flipped.data.points_xs) == [4.0, 5.0, 6.0]
    assert list(graph.data.points_xs) == [1.0, 2.0, 3.0]

    graph.flip_axes_in_place()
    assert list(graph.data.points_xs) == [4.0, 5.0, 6.0]


def test_enums_round_trip() -> None:
    configuration = sg.PointsGraphConfiguration(edges_style=sg.LineStyle.DashLine)
    assert configuration.edges_style == sg.LineStyle.DashLine
    assert configuration.edges_style != sg.LineStyle.SolidLine

    configuration.x_axis.log_scale = sg.LogScale.Log2Scale
    assert configuration.x_axis.log_scale == sg.LogScale.Log2Scale

    assert [member.name for member in sg.LineStyle] == ["SolidLine", "DashLine", "DotLine", "DashDotLine"]
    assert str(sg.LineStyle.DashLine) == "DashLine"


def test_none_clears_a_non_nothing_default() -> None:
    assert sg.HeatmapGraphConfiguration().rows_groups_gap == 1
    assert sg.HeatmapGraphConfiguration(rows_groups_gap=None).rows_groups_gap is None
    assert sg.DistributionsGraphConfiguration(distributions_gap=None).distributions_gap is None


def test_annotations() -> None:
    graph = sg.heatmap_graph(
        entries_values=np.array([[1.0, 2.0], [3.0, 4.0]]),
        rows_annotations=[
            sg.AnnotationData(
                title="kind",
                values=["x", "y"],
                colors=sg.ColorsConfiguration(palette={"x": "red", "y": "green"}),
            )
        ],
    )
    graph.validate()
    assert len(graph.data.rows_annotations) == 1
    assert graph.data.rows_annotations[0].title == "kind"
    assert list(graph.data.rows_annotations[0].values) == ["x", "y"]


def test_invalid_graph_is_rejected() -> None:
    graph = sg.points_graph(points_xs=[1.0, 2.0], points_ys=[1.0])
    try:
        graph.validate()
        raise AssertionError("an invalid graph was accepted")
    except Exception as exception:  # pylint: disable=broad-exception-caught
        assert "points_ys" in str(exception)


def test_save_html(tmp_path: object) -> None:
    graph = sg.points_graph(points_xs=[1.0, 2.0], points_ys=[1.0, 2.0])
    path = str(tmp_path) + "/graph.html"  # type: ignore
    graph.save(path)
    with open(path, "r", encoding="utf8") as file:
        assert "plotly" in file.read()


def test_save_png(tmp_path: object) -> None:
    graph = sg.points_graph(points_xs=[1.0, 2.0], points_ys=[1.0, 2.0])
    path = str(tmp_path) + "/graph.png"  # type: ignore
    graph.save(path)
    with open(path, "rb") as file:
        assert file.read(8) == b"\x89PNG\r\n\x1a\n"


def test_figure_is_a_plotly_figure() -> None:
    configuration = sg.PointsGraphConfiguration(figure=sg.FigureConfiguration(width=800))
    graph = sg.points_graph(
        points_xs=[1.0, 2.0, 3.0], points_ys=[1.0, 4.0, 9.0], figure_title="t", configuration=configuration
    )

    figure = graph.figure
    assert isinstance(figure, go.Figure)
    assert len(figure.data) == 1
    assert len(figure.data[0].x) == 3
    assert figure.layout.width == 800
    assert figure.layout.title.text == "t"


def test_repr_mimebundle() -> None:
    graph = sg.points_graph(points_xs=[1.0, 2.0], points_ys=[1.0, 2.0])
    # Outside a notebook ``plotly`` has no renderer set up, so this is empty rather than absent.
    assert graph._repr_mimebundle_() is not None


def test_missing_attributes_raise_attribute_error() -> None:
    graph = sg.points_graph(points_xs=[1.0, 2.0], points_ys=[1.0, 2.0])
    # IPython probes for such names to decide how to display a value, and expects an ``AttributeError``.
    for name in ("_ipython_canary_method_should_not_exist_", "_repr_html_", "no_such_field"):
        try:
            getattr(graph, name)
            raise AssertionError(f"accessing {name} did not raise")
        except AttributeError:
            pass
