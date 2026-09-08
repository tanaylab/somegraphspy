"""
Test the data source views: they reference the graph's own objects, hovers are added through them, and a Python source
function fills a graph the same way Julia would.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,missing-function-docstring
# flake8: noqa: F403,F405

from typing import Any
from typing import List
from typing import Sequence

import numpy as np

import somegraphspy as sg
from somegraphspy.julia_import import jl

_IS_SAME = jl.seval("(a, b) -> a === b")


def _is_same(left: Any, right: Any) -> bool:
    return bool(_IS_SAME(left.jl_obj, right.jl_obj))


def _hovers(entities: sg.EntitiesData) -> List[str]:
    hovers = entities.hovers
    assert hovers is not None
    return list(hovers)


def _values(values_data: sg.ValuesData) -> List[Any]:
    values = values_data.values
    assert values is not None
    return list(values)


def _points_graph() -> sg.PointsGraph:
    return sg.points_graph(x=sg.ValuesData(values=[1.0, 2.0, 3.0]), y=sg.ValuesData(values=[1.0, 4.0, 9.0]))


def test_views_reference_the_graph() -> None:
    graph = _points_graph()

    fields = graph.x_fields()
    assert isinstance(fields, sg.VectorFields)
    assert _is_same(fields.data.values, graph.data.x)
    assert _is_same(fields.data.entities, graph.data.points.entities)
    assert _is_same(fields.configuration.axis, graph.configuration.x_axis)

    fields = graph.points_colors_fields()
    assert _is_same(fields.data.values, graph.data.points.colors)
    assert _is_same(fields.data.entities, graph.data.points.entities)
    assert _is_same(fields.configuration.colors, graph.configuration.points.colors)
    assert _is_same(fields.configuration.axis, graph.configuration.points.colors.axis)

    fields = graph.points_sizes_fields()
    assert _is_same(fields.data.values, graph.data.points.sizes)
    assert _is_same(fields.configuration.sizes, graph.configuration.points.sizes)


def test_indexed_and_data_only_views() -> None:
    graph = sg.lines_graph(
        lines=[
            sg.LineData(x=sg.ValuesData(values=[1.0, 2.0]), y=sg.ValuesData(values=[1.0, 2.0])),
            sg.LineData(x=sg.ValuesData(values=[1.0, 3.0]), y=sg.ValuesData(values=[2.0, 4.0])),
        ]
    )
    fields = graph.x_fields(2)
    assert _is_same(fields.data.values, graph.data.lines[1].x)
    assert _is_same(fields.data.entities, graph.data.lines[1].points)

    bars = sg.bars_graph(values=sg.ValuesData(values=[1.0, 2.0]), names=sg.ValuesData(values=["a", "b"]))
    names = bars.names_fields()
    assert isinstance(names, sg.VectorDataFields)
    assert _is_same(names.values, bars.data.names)
    assert _is_same(names.entities, bars.data.bars)

    heatmap = sg.heatmap_graph(entries=sg.MatrixData(values=np.array([[1.0, 2.0], [3.0, 4.0]])))
    entries = heatmap.entries_fields()
    assert isinstance(entries, sg.MatrixFields)
    assert _is_same(entries.data.values, heatmap.data.entries)
    assert _is_same(entries.data.entities, heatmap.data.cells)
    assert _is_same(entries.configuration.colors, heatmap.configuration.entries.colors)


def test_add_structs() -> None:
    bars = sg.series_bars_graph(names=sg.ValuesData(values=["a", "b"]))

    series = sg.SeriesData(name="first", values=sg.ValuesData(values=[1.0, 2.0]))
    assert bars.add_series(series) == 1
    assert _is_same(bars.series_values_fields(1).data.values, series.values)
    assert bars.data.series[0].name == "first"

    assert bars.add_series() == 2
    bars.series_values_fields(2).data.values.values = [3.0, 4.0]
    assert _values(bars.data.series[1].values) == [3.0, 4.0]

    assert bars.add_annotation() == 1
    bars.annotations_fields(1).data.values.values = [1.0, 0.0]
    assert bars.add_annotation(sg.AnnotationData(values=sg.ValuesData(values=[0.0, 1.0]))) == 2
    assert len(bars.data.annotations) == 2
    bars.validate()

    lines = sg.lines_graph()
    assert lines.add_line(sg.LineData(name="first")) == 1
    assert lines.add_line() == 2
    lines.x_fields(2).data.values.values = [1.0, 2.0]
    assert _values(lines.data.lines[1].x) == [1.0, 2.0]

    distributions = sg.distributions_graph()
    assert distributions.add_distribution() == 1
    assert distributions.add_distribution(sg.DistributionData(name="second")) == 2
    assert distributions.data.distributions[1].name == "second"

    heatmap = sg.heatmap_graph(entries=sg.MatrixData(values=np.array([[1.0, 2.0], [3.0, 4.0]])))
    assert heatmap.add_rows_annotation() == 1
    assert heatmap.add_columns_annotation(sg.AnnotationData(values=sg.ValuesData(values=[1.0, 0.0]))) == 1
    heatmap.rows_annotations_fields(1).data.values.values = [0.0, 1.0]
    assert len(heatmap.data.rows.annotations) == 1
    assert len(heatmap.data.columns.annotations) == 1
    heatmap.validate()


def test_add_hovers() -> None:
    graph = _points_graph()
    entities = graph.data.points.entities
    entities.add_hovers(["a", "b", "c"])
    entities.add_hovers(["1", "2", "3"], title="N")
    assert _hovers(graph.data.points.entities) == ["a<br>N: 1", "b<br>N: 2", "c<br>N: 3"]

    # Hovers added through one view of the points are seen through all of them.
    graph.x_fields().data.entities.add_hovers(["x", "y", "z"], title="L")
    assert _hovers(graph.points_colors_fields().data.entities) == [
        "a<br>N: 1<br>L: x",
        "b<br>N: 2<br>L: y",
        "c<br>N: 3<br>L: z",
    ]

    try:
        entities.add_hovers(["too", "few"])
        raise AssertionError("hovers of the wrong size were accepted")
    except RuntimeError as exception:
        assert "invalid size of added hovers" in str(exception)


def test_add_matrix_hovers() -> None:
    heatmap = sg.heatmap_graph(entries=sg.MatrixData(values=np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])))
    heatmap.data.cells.add_hovers(np.array([["a", "b", "c"], ["d", "e", "f"]]), title="L")
    hovers = heatmap.data.cells.hovers
    assert hovers is not None
    assert hovers.shape == (2, 3)
    assert hovers[0, 2] == "L: c"
    assert hovers[1, 0] == "L: d"
    heatmap.validate()


def _source(fields: sg.VectorFields, values: Sequence[float], title: str) -> None:
    fields.data.values.values = values
    fields.data.values.title = title
    fields.data.entities.add_hovers([str(value) for value in values], title=title)


def test_python_source_function() -> None:
    graph = sg.points_graph()
    _source(graph.x_fields(), [1.0, 2.0, 3.0], "X")
    _source(graph.y_fields(), [1.0, 4.0, 9.0], "Y")
    _source(graph.points_colors_fields(), [0.0, 1.0, 2.0], "C")
    graph.validate()

    julia_json = jl.seval(
        "SomeGraphs.graph_to_json(SomeGraphs.points_graph(; "
        'x = SomeGraphs.ValuesData([1.0, 2.0, 3.0], "X"), '
        'y = SomeGraphs.ValuesData([1.0, 4.0, 9.0], "Y"), '
        "points = SomeGraphs.PointsData(; "
        'colors = SomeGraphs.ValuesData([0.0, 1.0, 2.0], "C"), '
        'entities = SomeGraphs.EntitiesData(; hovers = ["X: 1.0<br>Y: 1.0<br>C: 0.0", '
        '"X: 2.0<br>Y: 4.0<br>C: 1.0", "X: 3.0<br>Y: 9.0<br>C: 2.0"]))))'
    )
    assert graph.json == str(julia_json)
