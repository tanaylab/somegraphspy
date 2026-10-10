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


def _hovers(entities: sg.VectorEntitiesData) -> List[str]:
    hovers = entities.hovers
    assert hovers is not None
    return list(hovers)


def _values(values_data: sg.VectorValuesData) -> List[Any]:
    values = values_data.vector
    assert values is not None
    return list(values)


def _points_graph() -> sg.PointsGraph:
    return sg.points_graph(x=sg.VectorValuesData(vector=[1.0, 2.0, 3.0]), y=sg.VectorValuesData(vector=[1.0, 4.0, 9.0]))


def test_views_reference_the_graph() -> None:
    graph = _points_graph()

    fields = graph.x_axis_vector_fields()
    assert isinstance(fields, sg.VectorFields)
    assert _is_same(fields.data.values, graph.data.x)
    assert _is_same(fields.data.entities, graph.data.points.entities)
    assert _is_same(fields.configuration.axis, graph.configuration.x_axis)

    fields = graph.points_colors_vector_fields()
    assert _is_same(fields.data.values, graph.data.points.colors)
    assert _is_same(fields.data.entities, graph.data.points.entities)
    assert _is_same(fields.configuration.colors, graph.configuration.points.colors)
    assert _is_same(fields.configuration.scale, graph.configuration.points.colors.scale)

    fields = graph.points_sizes_vector_fields()
    assert _is_same(fields.data.values, graph.data.points.sizes)
    assert _is_same(fields.configuration.sizes, graph.configuration.points.sizes)

    assert _is_same(graph.points_entities(), graph.data.points.entities)
    assert _is_same(graph.edges_entities(), graph.data.edges.entities)


def test_part_and_data_only_views() -> None:
    graph = sg.lines_graph(
        lines=[
            sg.LineData(x=sg.VectorValuesData(vector=[1.0, 2.0]), y=sg.VectorValuesData(vector=[1.0, 2.0])),
            sg.LineData(x=sg.VectorValuesData(vector=[1.0, 3.0]), y=sg.VectorValuesData(vector=[2.0, 4.0])),
        ]
    )
    part = graph.line_part_fields(2)
    assert isinstance(part, sg.PartFields)
    assert part.index == 2
    assert _is_same(part.data, graph.data.lines[1])
    assert _is_same(part.x.data.values, graph.data.lines[1].x)
    assert _is_same(part.y.data.values, graph.data.lines[1].y)
    assert _is_same(part.entities, graph.data.lines[1].points)
    assert _is_same(part.x.configuration.axis, graph.configuration.x_axis)

    heatmap = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=np.array([[1.0, 2.0], [3.0, 4.0]])))
    entries = heatmap.entries_matrix_fields()
    assert isinstance(entries, sg.MatrixFields)
    assert _is_same(entries.data.values, heatmap.data.entries)
    assert _is_same(entries.data.entities, heatmap.data.cells)
    assert _is_same(entries.data.rows_entities, heatmap.data.rows.entities)
    assert _is_same(entries.data.columns_entities, heatmap.data.columns.entities)
    assert _is_same(entries.configuration.colors, heatmap.configuration.entries.colors)
    assert _is_same(entries.configuration.scale, heatmap.configuration.entries.colors.scale)

    groups = heatmap.rows_groups_vector_data_fields()
    assert isinstance(groups, sg.VectorDataFields)
    assert _is_same(groups.values, heatmap.data.rows.arrangement.groups)
    assert _is_same(groups.entities, heatmap.data.rows.entities)
    assert _is_same(heatmap.rows_entities(), heatmap.data.rows.entities)
    assert _is_same(heatmap.rows_arrangement(), heatmap.data.rows.arrangement)
    assert _is_same(heatmap.columns_arrangement(), heatmap.data.columns.arrangement)

    side = heatmap.columns_side()
    assert isinstance(side, sg.HeatmapSide)
    assert not side.is_rows
    assert _is_same(side.data(), heatmap.data.columns)
    assert _is_same(side.configuration(), heatmap.configuration.columns)
    assert list(side.placement().order) == list(heatmap.placement.columns.order)

    visited: List[Any] = []
    sg.visit_data_sinks(visited.append, side)
    assert len(visited) == 2
    assert isinstance(visited[0], sg.VectorEntitiesData)
    assert isinstance(visited[1], sg.ArrangementData)
    assert _is_same(visited[1], heatmap.data.columns.arrangement)


def test_add_parts() -> None:
    bars = sg.series_bars_graph(bars=sg.VectorEntitiesData(names=["a", "b"]))

    series = sg.SeriesData(name="first", values=sg.VectorValuesData(vector=[1.0, 2.0]))
    part = bars.add_series(series)
    assert isinstance(part, sg.PartFields)
    assert part.index == 1
    assert part.name == "first"
    assert _is_same(part.values.data.values, series.values)
    assert _is_same(part.entities, series.bars)
    assert bars.data.series[0].name == "first"

    part = bars.add_series()
    assert part.index == 2
    part.values.data.values.vector = [3.0, 4.0]
    part.name = "second"
    assert _values(bars.data.series[1].values) == [3.0, 4.0]
    assert bars.data.series[1].name == "second"
    assert _is_same(bars.series_part_fields(2).data, bars.data.series[1])

    assert bars.add_annotation() == 1
    bars.annotations_colors_vector_fields(1).data.values.vector = [1.0, 0.0]
    assert bars.add_annotation(sg.AnnotationData(values=sg.VectorValuesData(vector=[0.0, 1.0]))) == 2
    assert len(bars.data.annotations) == 2
    assert _is_same(bars.bars_entities(), bars.data.bars)
    bars.validate()

    lines = sg.lines_graph()
    assert lines.add_line(sg.LineData(name="first")).index == 1
    part = lines.add_line()
    assert part.index == 2
    part.x.data.values.vector = [1.0, 2.0]
    assert _values(lines.data.lines[1].x) == [1.0, 2.0]

    distributions = sg.distributions_graph()
    assert distributions.add_distribution().index == 1
    part = distributions.add_distribution(sg.DistributionData(name="second"))
    assert part.index == 2
    assert distributions.data.distributions[1].name == "second"
    assert _is_same(part.values.data.values, distributions.data.distributions[1].values)

    heatmap = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=np.array([[1.0, 2.0], [3.0, 4.0]])))
    assert heatmap.add_rows_annotation() == 1
    assert heatmap.add_columns_annotation(sg.AnnotationData(values=sg.VectorValuesData(vector=[1.0, 0.0]))) == 1
    heatmap.rows_annotations_colors_vector_fields(1).data.values.vector = [0.0, 1.0]
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
    graph.x_axis_vector_fields().data.entities.add_hovers(["x", "y", "z"], title="L")
    assert _hovers(graph.points_colors_vector_fields().data.entities) == [
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
    heatmap = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])))
    heatmap.data.cells.add_hovers(np.array([["a", "b", "c"], ["d", "e", "f"]]), title="L")
    hovers = heatmap.data.cells.hovers
    assert hovers is not None
    assert hovers.shape == (2, 3)
    assert hovers[0, 2] == "L: c"
    assert hovers[1, 0] == "L: d"
    heatmap.validate()


def _source(fields: sg.VectorFields, values: Sequence[float], title: str) -> None:
    fields.data.values.vector = values
    fields.data.values.title = title
    fields.data.entities.add_hovers([str(value) for value in values], title=title)


def test_python_source_function() -> None:
    graph = sg.points_graph()
    _source(graph.x_axis_vector_fields(), [1.0, 2.0, 3.0], "X")
    _source(graph.y_axis_vector_fields(), [1.0, 4.0, 9.0], "Y")
    _source(graph.points_colors_vector_fields(), [0.0, 1.0, 2.0], "C")
    graph.validate()

    julia_json = jl.seval(
        "SomeGraphs.graph_to_json(SomeGraphs.points_graph(; "
        'x = SomeGraphs.VectorValuesData(; vector = [1.0, 2.0, 3.0], title = "X"), '
        'y = SomeGraphs.VectorValuesData(; vector = [1.0, 4.0, 9.0], title = "Y"), '
        "points = SomeGraphs.PointsData(; "
        'colors = SomeGraphs.VectorValuesData(; vector = [0.0, 1.0, 2.0], title = "C"), '
        'entities = SomeGraphs.VectorEntitiesData(; hovers = ["X: 1.0<br>Y: 1.0<br>C: 0.0", '
        '"X: 2.0<br>Y: 4.0<br>C: 1.0", "X: 3.0<br>Y: 9.0<br>C: 2.0"]))))'
    )
    assert graph.json == str(julia_json)


def test_visit_sinks() -> None:
    graph = _points_graph()

    visited: List[Any] = []
    sg.visit_data_sinks(visited.append, [graph.x_axis_vector_fields(), graph.data.points.colors])
    assert [type(sink) for sink in visited] == [sg.VectorValuesData, sg.VectorEntitiesData, sg.VectorValuesData]
    assert _is_same(visited[0], graph.data.x)
    assert _is_same(visited[1], graph.data.points.entities)
    assert _is_same(visited[2], graph.data.points.colors)

    visited = []
    sg.visit_configuration_sinks(visited.append, graph.points_colors_vector_fields())
    assert any(isinstance(sink, sg.ColorsConfiguration) for sink in visited)
    assert all(
        _is_same(sink, graph.configuration.points.colors)
        for sink in visited
        if isinstance(sink, sg.ColorsConfiguration)
    )


def test_visit_graph_parts() -> None:
    graph = _points_graph()

    visited: List[Any] = []
    sg.visit_graph_parts(visited.append, graph)
    assert isinstance(visited[0], sg.PointsGraph)
    assert any(_is_same(part, graph.data.points.colors) for part in visited)
    assert any(_is_same(part, graph.configuration.points.colors) for part in visited)
    assert not any(isinstance(part, sg.ScaleConfiguration) for part in visited)

    def show_legend(part: Any) -> None:
        if hasattr(part, "show_legend"):
            part.show_legend = True

    sg.visit_graph_parts(show_legend, graph)
    assert graph.configuration.points.colors.show_legend
    assert graph.configuration.edges.sizes.show_legend

    lines = sg.lines_graph()
    sg.visit_graph_parts(show_legend, lines)
    assert lines.configuration.show_legend


def _given_list(values: Any) -> List[Any]:
    assert values is not None
    return list(values)


def test_puts() -> None:
    graph = _points_graph()
    sg.put_vector_data(graph.x_axis_vector_fields(), np.array([5.0, 6.0, 7.0]), title="X")
    sg.put_vector_names_data(graph.points_entities(), ["a", "b", "c"])
    sg.put_vector_mask_data(graph.points_entities(), [True, False, True])
    sg.put_vector_order_data(graph.points_entities(), [3, 1, 2])
    assert _values(graph.data.x) == [5.0, 6.0, 7.0]
    assert _hovers(graph.data.points.entities) == ["X: 5.0", "X: 6.0", "X: 7.0"]
    assert _given_list(graph.data.points.entities.names) == ["a", "b", "c"]
    assert _given_list(graph.data.points.entities.mask) == [True, False, True]
    assert _given_list(graph.data.points.entities.order) == [3, 1, 2]

    heatmap = sg.heatmap_graph()
    sg.put_matrix_data(heatmap.entries_matrix_fields(), np.array([[1.0, 2.0], [3.0, 4.0]]), title="M")
    sg.put_matrix_names_data(heatmap.entries_matrix_fields(), ["r1", "r2"], ["c1", "c2"])
    matrix = heatmap.data.entries.matrix
    assert matrix is not None
    assert matrix[0, 1] == 2.0
    assert _given_list(heatmap.data.rows.entities.names) == ["r1", "r2"]
    assert _given_list(heatmap.data.columns.entities.names) == ["c1", "c2"]

    sg.put_vector_names_data(heatmap.rows_side(), ["s1", "s2"])
    assert _given_list(heatmap.data.rows.entities.names) == ["s1", "s2"]


def test_gets() -> None:
    graph = _points_graph()
    assert sg.get_vector_names_data(graph.points_colors_vector_fields()) is None
    sg.put_vector_names_data(graph.points_entities(), ["a", "b", "c"])
    assert _given_list(sg.get_vector_names_data(graph.points_colors_vector_fields())) == ["a", "b", "c"]

    heatmap = sg.heatmap_graph()
    assert sg.get_matrix_names_data(heatmap.entries_matrix_fields()) == (None, None)
    sg.put_matrix_names_data(heatmap.entries_matrix_fields(), ["r1", "r2"], ["c1", "c2"])
    name_per_row, name_per_column = sg.get_matrix_names_data(heatmap.entries_matrix_fields())
    assert _given_list(name_per_row) == ["r1", "r2"]
    assert _given_list(name_per_column) == ["c1", "c2"]


def test_fill_side() -> None:
    values = np.array([[0.0, 5.0, 1.0, 6.0], [0.0, 5.0, 1.0, 6.0]])
    base = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=values))
    base.data.columns.entities.names = ["A", "B", "C", "D"]
    base.data.columns.arrangement.subgroups.vector = ["P", "Q", "R", "S"]
    base.data.columns.arrangement.groups.vector = [1, 1, 2, 2]
    base.configuration.columns.order_source = sg.OrderSource.OptimalTreeReorder
    base.configuration.columns.dendogram_size = 0.1

    other = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=np.array([[9.0, 8.0, 7.0, 6.0], [5.0, 4.0, 3.0, 2.0]])))
    sg.fill_side(other.columns_side(), base.columns_side())
    other.validate()
    assert list(other.placement.columns.order) == list(base.placement.columns.order)
    assert _given_list(other.data.columns.entities.names) == ["A", "B", "C", "D"]
    assert _given_list(other.data.columns.arrangement.groups.vector) == [1, 1, 2, 2]
    assert other.data.columns.arrangement.subgroups.vector is None
    assert other.configuration.columns.order_source is None
    assert other.configuration.columns.dendogram_size == 0.1

    another = sg.heatmap_graph(entries=sg.MatrixValuesData(matrix=values))
    sg.fill_placement(another.columns_side(), base.placement.columns)
    assert list(another.placement.columns.order) == list(base.placement.columns.order)
