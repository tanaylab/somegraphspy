"""
Test creating each of the graph types.

Each graph is built twice, once through the Python wrappers and once directly in Julia, and the resulting figures are
compared. This verifies the wrappers pass every value through unchanged, without restating what the Julia tests already
cover.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,missing-function-docstring
# flake8: noqa: F403,F405

from typing import Any
from typing import List

import numpy as np
import plotly.graph_objects as go  # type: ignore
import pytest
import scipy.cluster.hierarchy as sch  # type: ignore

import somegraphspy as sg
from somegraphspy.julia_import import jl

#: A Julia module for evaluating the Julia code with the ``SomeGraphs`` names in scope, without leaking them into ``Main``.
_JULIA_TESTS = jl.seval("module SomeGraphsPyTests; using SomeGraphs; end")

#: A Python graph and the Julia code building the identical graph.
GRAPHS = {
    "points": (
        sg.points_graph(
            x=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]),
            y=sg.VectorValuesData(vector=[1.0, 4.0, 9.0]),
            figure_title="t",
        ),
        'points_graph(; x = VectorValuesData([1.0, 2.0, 3.0]), y = VectorValuesData([1.0, 4.0, 9.0]), figure_title = "t")',
    ),
    "points_box": (
        sg.points_graph(
            x=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]),
            y=sg.VectorValuesData(vector=[1.0, 4.0, 9.0]),
            selection=sg.SelectionData(box=(1.5, 3.0, 2.0, 9.0)),
        ),
        "points_graph(; x = VectorValuesData([1.0, 2.0, 3.0]), y = VectorValuesData([1.0, 4.0, 9.0]), "
        "selection = SelectionData(; box = (1.5, 3.0, 2.0, 9.0)))",
    ),
    "points_polygon": (
        sg.points_graph(
            x=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]),
            y=sg.VectorValuesData(vector=[1.0, 4.0, 9.0]),
            selection=sg.SelectionData(polygon=[(1.0, 0.0), (3.0, 5.0), (2.0, 10.0)]),
        ),
        "points_graph(; x = VectorValuesData([1.0, 2.0, 3.0]), y = VectorValuesData([1.0, 4.0, 9.0]), "
        "selection = SelectionData(; polygon = [(1.0, 0.0), (3.0, 5.0), (2.0, 10.0)]))",
    ),
    "line": (
        sg.line_graph(x=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]), y=sg.VectorValuesData(vector=[1.0, 4.0, 9.0])),
        "line_graph(; x = VectorValuesData([1.0, 2.0, 3.0]), y = VectorValuesData([1.0, 4.0, 9.0]))",
    ),
    "lines": (
        sg.lines_graph(
            lines=[
                sg.LineData(x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0, 2.0])),
                sg.LineData(x=sg.VectorValuesData(vector=[1.0, 3.0]), y=sg.VectorValuesData(vector=[2.0, 4.0])),
            ]
        ),
        "lines_graph(; lines = [LineData(; x = VectorValuesData([1.0, 2.0]), y = VectorValuesData([1.0, 2.0])), "
        "LineData(; x = VectorValuesData([1.0, 3.0]), y = VectorValuesData([2.0, 4.0]))])",
    ),
    "bars": (
        sg.bars_graph(
            values=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]), bars=sg.VectorEntitiesData(names=["a", "b", "c"])
        ),
        'bars_graph(; values = VectorValuesData([1.0, 2.0, 3.0]), bars = VectorEntitiesData(; names = ["a", "b", "c"]))',
    ),
    "series_bars": (
        sg.series_bars_graph(
            series=[
                sg.SeriesData(values=sg.VectorValuesData(vector=[1.0, 2.0])),
                sg.SeriesData(values=sg.VectorValuesData(vector=[3.0, 4.0])),
            ],
            bars=sg.VectorEntitiesData(names=["a", "b"]),
        ),
        "series_bars_graph(; series = [SeriesData(; values = VectorValuesData([1.0, 2.0])), "
        'SeriesData(; values = VectorValuesData([3.0, 4.0]))], bars = VectorEntitiesData(; names = ["a", "b"]))',
    ),
    "series_bars_hovers": (
        sg.series_bars_graph(
            series=[
                sg.SeriesData(
                    values=sg.VectorValuesData(vector=[1.0, 2.0]), bars=sg.VectorEntitiesData(hovers=["a1", "b1"])
                ),
                sg.SeriesData(
                    values=sg.VectorValuesData(vector=[3.0, 4.0]), bars=sg.VectorEntitiesData(hovers=["a2", "b2"])
                ),
            ],
            bars=sg.VectorEntitiesData(names=["a", "b"]),
        ),
        "series_bars_graph(; series = ["
        'SeriesData(; values = VectorValuesData([1.0, 2.0]), bars = VectorEntitiesData(; hovers = ["a1", "b1"])), '
        'SeriesData(; values = VectorValuesData([3.0, 4.0]), bars = VectorEntitiesData(; hovers = ["a2", "b2"]))], '
        'bars = VectorEntitiesData(; names = ["a", "b"]))',
    ),
    "distribution": (
        sg.distribution_graph(
            distribution=sg.DistributionData(values=sg.VectorValuesData(vector=[0.0, 0.0, 1.0, 1.0, 1.0, 3.0]))
        ),
        "distribution_graph(; distribution = DistributionData(; values = VectorValuesData([0.0, 0.0, 1.0, 1.0, 1.0, 3.0])))",
    ),
    "distributions": (
        sg.distributions_graph(
            distributions=[
                sg.DistributionData(values=sg.VectorValuesData(vector=[0.0, 1.0, 1.0, 2.0])),
                sg.DistributionData(values=sg.VectorValuesData(vector=[1.0, 2.0, 2.0, 3.0])),
            ]
        ),
        "distributions_graph(; distributions = [DistributionData(; values = VectorValuesData([0.0, 1.0, 1.0, 2.0])), "
        "DistributionData(; values = VectorValuesData([1.0, 2.0, 2.0, 3.0]))])",
    ),
    "heatmap": (
        sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))),
        "heatmap_graph(; entries = MatrixValuesData([1.0 2.0 3.0; 4.0 5.0 6.0]))",
    ),
}


def _julia_json(julia_code: str) -> str:
    return str(_JULIA_TESTS.seval("graph_to_json(" + julia_code + ")"))


def _values(values_data: sg.VectorValuesData) -> List[Any]:
    values = values_data.vector
    assert values is not None
    return list(values)


@pytest.mark.parametrize("name", sorted(GRAPHS.keys()))
def test_graph_matches_julia(name: str) -> None:
    graph, julia_code = GRAPHS[name]
    graph.validate()
    assert graph.json == _julia_json(julia_code)


def test_heatmap_matrix_is_not_transposed() -> None:
    values = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    graph = sg.heatmap_graph(
        entries=sg.MatrixValuesData(matrix=values),
        rows=sg.HeatmapSideData(entities=sg.VectorEntitiesData(names=["r1", "r2"])),
        columns=sg.HeatmapSideData(entities=sg.VectorEntitiesData(names=["c1", "c2", "c3"])),
    )
    graph.validate()

    read_back = graph.data.entries.matrix
    assert read_back is not None
    assert read_back.shape == values.shape
    assert read_back[0, 2] == values[0, 2]


def test_configuration_is_shared_with_the_graph() -> None:
    configuration = sg.PointsGraphConfiguration()
    graph = sg.points_graph(
        x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0, 2.0]), configuration=configuration
    )

    configuration.figure.width = 700
    assert graph.configuration.figure.width == 700


def test_flip_axes() -> None:
    graph = sg.points_graph(
        x=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]), y=sg.VectorValuesData(vector=[4.0, 5.0, 6.0])
    )

    flipped = graph.flip_axes()
    assert _values(flipped.data.x) == [4.0, 5.0, 6.0]
    assert _values(graph.data.x) == [1.0, 2.0, 3.0]

    graph.flip_axes_in_place()
    assert _values(graph.data.x) == [4.0, 5.0, 6.0]


def test_enums_round_trip() -> None:
    configuration = sg.PointsGraphConfiguration(edges_style=sg.LineStyle.DashLine)
    assert configuration.edges_style == sg.LineStyle.DashLine
    assert configuration.edges_style != sg.LineStyle.SolidLine

    configuration.x_axis.scale.log_base = sg.LogBase.Log2Base
    assert configuration.x_axis.scale.log_base == sg.LogBase.Log2Base

    assert [member.name for member in sg.LineStyle] == ["SolidLine", "DashLine", "DotLine", "DashDotLine"]
    assert str(sg.LineStyle.DashLine) == "DashLine"


def test_none_clears_a_non_nothing_default() -> None:
    assert sg.HeatmapSideConfiguration().groups_gap == 1
    assert sg.HeatmapSideConfiguration(groups_gap=None).groups_gap is None
    assert sg.DistributionsGraphConfiguration(distributions_gap=None).distributions_gap is None


def test_annotations() -> None:
    graph = sg.heatmap_graph(
        entries=sg.MatrixValuesData(matrix=np.array([[1.0, 2.0], [3.0, 4.0]])),
        rows=sg.HeatmapSideData(
            annotations=[
                sg.AnnotationData(
                    values=sg.VectorValuesData(vector=["x", "y"], title="kind"),
                    colors=sg.ColorsConfiguration(palette={"x": "red", "y": "green"}),
                )
            ]
        ),
    )
    graph.validate()
    assert len(graph.data.rows.annotations) == 1
    assert graph.data.rows.annotations[0].values.title == "kind"
    assert _values(graph.data.rows.annotations[0].values) == ["x", "y"]


def test_heatmap_layout() -> None:
    # Columns 1 and 3 are close, as are 2 and 4, so a clustering pairs them and puts the close 2 and 3 side by side.
    values = np.array([[0.0, 5.0, 1.0, 6.0], [0.0, 5.0, 1.0, 6.0]])
    graph = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=values))
    assert graph.configuration.columns.tree_source is None
    assert graph.configuration.columns.order_source is None

    graph.configuration.columns.order_source = sg.OrderSource.OptimalTreeReorder
    assert graph.configuration.columns.order_source == sg.OrderSource.OptimalTreeReorder
    clustered_order = list(graph.placement.columns.order)
    assert clustered_order in ([1, 3, 2, 4], [4, 2, 3, 1])
    tree = graph.placement.columns.hclust
    assert tree is not None

    # The order and the tree of one graph lay out another.
    other_graph = sg.heatmap_graph(
        entries=sg.MatrixValuesData(matrix=values),
        columns=sg.HeatmapSideData(
            entities=sg.VectorEntitiesData(order=clustered_order), arrangement=sg.ArrangementData(hclust=tree)
        ),
    )
    other_graph.validate()
    other_order = other_graph.data.columns.entities.order
    assert other_order is not None
    assert list(other_order) == clustered_order
    assert other_graph.data.columns.arrangement.hclust is not None
    assert list(other_graph.placement.columns.order) == clustered_order

    other_graph.configuration.columns.tree_source = sg.TreeSource.ClusteredTree
    other_graph.reset_placement()
    try:
        other_graph.validate()
        raise AssertionError("an invalid graph was accepted")
    except Exception as exception:  # pylint: disable=broad-exception-caught
        assert "arrangement.hclust" in str(exception)


def test_linkage_matrix() -> None:
    values = np.array([[0.0, 5.0, 1.0, 6.0, 2.0], [0.0, 5.0, 1.0, 6.0, 3.0]])

    # A tree computed by Julia is a valid SciPy tree, whose leaves are the order the graph is shown in.
    graph = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=values))
    graph.configuration.columns.order_source = sg.OrderSource.OptimalTreeReorder
    julia_tree = graph.placement.columns.hclust
    assert isinstance(julia_tree, np.ndarray)
    assert julia_tree.shape == (4, 4)
    assert sch.is_valid_linkage(julia_tree)
    assert list(sch.leaves_list(julia_tree) + 1) == list(graph.placement.columns.order)

    # A tree computed by SciPy lays out a graph in the order of its leaves, and comes back as it was given.
    scipy_tree = sch.linkage(values.T, method="average")
    expected_order = list(sch.leaves_list(scipy_tree) + 1)

    other = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=values))
    other.data.columns.arrangement.hclust = scipy_tree
    assert list(other.placement.columns.order) == expected_order
    assert np.array_equal(other.data.columns.arrangement.hclust, scipy_tree)

    arranged = sg.heatmap_graph(
        entries=sg.MatrixValuesData(matrix=values),
        columns=sg.HeatmapSideData(arrangement=sg.ArrangementData(hclust=scipy_tree)),
    )
    assert list(arranged.placement.columns.order) == expected_order

    put = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=values))
    sg.put_vector_tree_data(put.columns_side(), scipy_tree)
    assert list(put.placement.columns.order) == expected_order

    # A tree which crosses back and forth is the same tree.
    other.data.columns.arrangement.hclust = julia_tree
    assert np.array_equal(other.data.columns.arrangement.hclust, julia_tree)

    other.data.columns.arrangement.hclust = None
    assert other.data.columns.arrangement.hclust is None


def test_points_order() -> None:
    graph = sg.points_graph(
        x=sg.VectorValuesData(vector=[1.0, 2.0]),
        y=sg.VectorValuesData(vector=[1.0, 2.0]),
        points=sg.PointsData(entities=sg.VectorEntitiesData(order=[2, 1])),
    )
    graph.validate()
    order = graph.data.points.entities.order
    assert order is not None
    assert list(order) == [2, 1]


def test_selection_round_trip() -> None:
    graph = sg.points_graph(x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0, 2.0]))
    graph.data.selection.box = (0.5, 1.5, 0.5, 1.5)
    graph.validate()
    assert graph.data.selection.box == (0.5, 1.5, 0.5, 1.5)
    graph.data.selection.box = None
    graph.data.selection.polygon = [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0)]
    graph.validate()
    assert graph.data.selection.polygon == [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0)]


def test_invalid_graph_is_rejected() -> None:
    graph = sg.points_graph(x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0]))
    try:
        graph.validate()
        raise AssertionError("an invalid graph was accepted")
    except Exception as exception:  # pylint: disable=broad-exception-caught
        assert "y.vector" in str(exception)


def test_save_html(tmp_path: object) -> None:
    graph = sg.points_graph(x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0, 2.0]))
    path = str(tmp_path) + "/graph.html"  # type: ignore
    graph.save(path)
    with open(path, "r", encoding="utf8") as file:
        assert "plotly" in file.read()


def test_save_png(tmp_path: object) -> None:
    graph = sg.points_graph(x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0, 2.0]))
    path = str(tmp_path) + "/graph.png"  # type: ignore
    graph.save(path)
    with open(path, "rb") as file:
        assert file.read(8) == b"\x89PNG\r\n\x1a\n"


def test_figure_is_a_plotly_figure() -> None:
    configuration = sg.PointsGraphConfiguration(figure=sg.FigureConfiguration(width=800))
    graph = sg.points_graph(
        x=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]),
        y=sg.VectorValuesData(vector=[1.0, 4.0, 9.0]),
        figure_title="t",
        configuration=configuration,
    )

    figure = graph.figure
    assert isinstance(figure, go.Figure)
    assert len(figure.data) == 1
    assert len(figure.data[0].x) == 3
    assert figure.layout.width == 800
    assert figure.layout.title.text == "t"


def test_palette_order_is_legend_order() -> None:
    configuration = sg.PointsGraphConfiguration()
    configuration.points.colors.palette = {"c": "red", "a": "green", "b": "blue"}
    configuration.points.colors.show_legend = True
    graph = sg.points_graph(
        x=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]),
        y=sg.VectorValuesData(vector=[1.0, 4.0, 9.0]),
        points=sg.PointsData(colors=sg.VectorValuesData(vector=["a", "b", "c"])),
        configuration=configuration,
    )
    assert [trace.name for trace in graph.figure.data if trace.name in ("a", "b", "c")] == ["c", "a", "b"]


def test_repr_mimebundle() -> None:
    graph = sg.points_graph(x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0, 2.0]))
    # Outside a notebook ``plotly`` has no renderer set up, so this is empty rather than absent.
    assert graph._repr_mimebundle_() is not None


def test_missing_attributes_raise_attribute_error() -> None:
    graph = sg.points_graph(x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0, 2.0]))
    # IPython probes for such names to decide how to display a value, and expects an ``AttributeError``.
    for name in ("_ipython_canary_method_should_not_exist_", "_repr_html_", "no_such_field"):
        try:
            getattr(graph, name)
            raise AssertionError(f"accessing {name} did not raise")
        except AttributeError:
            pass
