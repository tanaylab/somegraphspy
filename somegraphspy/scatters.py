"""
Graphs showing scattered points and/or lines. See the Julia
`documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html>`__ for details.
"""

from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from .common import AbstractGraphConfiguration
from .common import AbstractGraphData
from .common import AxisConfiguration
from .common import BandsConfiguration
from .common import BandsData
from .common import BoolsVector
from .common import ColorsConfiguration
from .common import FigureConfiguration
from .common import Graph
from .common import IntegersVector
from .common import LineConfiguration
from .common import LineStyle
from .common import NumbersVector
from .common import SizesConfiguration
from .common import Stacking
from .common import StringsVector
from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import _given
from .julia_import import jl
from .julia_import import register_jl_type

__all__ = [
    "LineGraph",
    "LineGraphConfiguration",
    "LineGraphData",
    "LinesGraph",
    "LinesGraphConfiguration",
    "LinesGraphData",
    "PointsGraph",
    "PointsGraphConfiguration",
    "PointsGraphData",
    "ScattersConfiguration",
    "line_graph",
    "lines_graph",
    "points_density",
    "points_graph",
]

#: The colors of a set of points (or edges), either explicit color names or values to map through a palette.
ColorsVector = Union[NumbersVector, StringsVector]

#: The pairs of point indices to draw edges between. These are 1-based, as in Julia.
EdgesVector = Sequence[Tuple[int, int]]


class ScattersConfiguration(AbstractGraphConfiguration):
    """
    Configure points, borders or edges in a scatter graph. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.ScattersConfiguration>`__
    for details.
    """

    #: How to color the entities.
    colors: ColorsConfiguration
    #: How to size the entities.
    sizes: SizesConfiguration

    def __init__(
        self,
        *,
        colors: Union[ColorsConfiguration, DefaultValue] = DEFAULT,
        sizes: Union[SizesConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.ScattersConfiguration(**_given(colors=colors, sizes=sizes)))


register_jl_type("ScattersConfiguration", ScattersConfiguration)


class PointsGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing a scatter of points and/or edges. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.PointsGraphConfiguration>`__
    for details.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: The horizontal axis.
    x_axis: AxisConfiguration
    #: The vertical axis.
    y_axis: AxisConfiguration
    #: How to show the points.
    points: ScattersConfiguration
    #: How to show the borders drawn under the points.
    borders: ScattersConfiguration
    #: How to show the edges between points.
    edges: ScattersConfiguration
    #: The style of the edges.
    edges_style: LineStyle
    #: Draw the edges above the points.
    edges_over_points: bool
    #: Bands partitioning the graph by the horizontal axis.
    vertical_bands: BandsConfiguration
    #: Bands partitioning the graph by the vertical axis.
    horizontal_bands: BandsConfiguration
    #: Bands partitioning the graph parallel to the X = Y line.
    diagonal_bands: BandsConfiguration

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        x_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        y_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        points: Union[ScattersConfiguration, DefaultValue] = DEFAULT,
        borders: Union[ScattersConfiguration, DefaultValue] = DEFAULT,
        edges: Union[ScattersConfiguration, DefaultValue] = DEFAULT,
        edges_style: Union[LineStyle, DefaultValue] = DEFAULT,
        edges_over_points: Union[bool, DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.PointsGraphConfiguration(
                **_given(
                    figure=figure,
                    x_axis=x_axis,
                    y_axis=y_axis,
                    points=points,
                    borders=borders,
                    edges=edges,
                    edges_style=edges_style,
                    edges_over_points=edges_over_points,
                    vertical_bands=vertical_bands,
                    horizontal_bands=horizontal_bands,
                    diagonal_bands=diagonal_bands,
                )
            )
        )


register_jl_type("PointsGraphConfiguration", PointsGraphConfiguration)


class PointsGraphData(AbstractGraphData):
    """
    The data of a scatter graph of points. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.PointsGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The title of the horizontal axis.
    x_axis_title: Optional[str]
    #: The title of the vertical axis.
    y_axis_title: Optional[str]
    #: The title of the points colors legend.
    points_colors_title: Optional[str]
    #: The title of the borders colors legend.
    borders_colors_title: Optional[str]
    #: The title of the edges colors legend.
    edges_colors_title: Optional[str]
    #: The horizontal coordinate of each point.
    points_xs: NumbersVector
    #: The vertical coordinate of each point.
    points_ys: NumbersVector
    #: The diameter of each point, in pixels.
    points_sizes: Optional[NumbersVector]
    #: The color of each point.
    points_colors: Optional[ColorsVector]
    #: The hover text of each point.
    points_hovers: Optional[StringsVector]
    #: Which points to show.
    points_mask: Optional[BoolsVector]
    #: The order to draw the points in, controlling which are on top.
    points_order: Optional[IntegersVector]
    #: The color of the border of each point.
    borders_colors: Optional[ColorsVector]
    #: The size added to each point for its border, in pixels.
    borders_sizes: Optional[NumbersVector]
    #: Which borders to show.
    borders_mask: Optional[BoolsVector]
    #: The pairs of (1-based) point indices to draw edges between.
    edges_points: Optional[EdgesVector]
    #: The color of each edge.
    edges_colors: Optional[ColorsVector]
    #: The width of each edge, in pixels.
    edges_sizes: Optional[NumbersVector]
    #: The style of each edge.
    edges_styles: Optional[Sequence[LineStyle]]
    #: The hover text of each edge.
    edges_hovers: Optional[StringsVector]
    #: Which edges to show.
    edges_mask: Optional[BoolsVector]
    #: The order to draw the edges in, controlling which are on top.
    edges_order: Optional[IntegersVector]
    #: Override the offsets of the vertical bands.
    vertical_bands: BandsData
    #: Override the offsets of the horizontal bands.
    horizontal_bands: BandsData
    #: Override the offsets of the diagonal bands.
    diagonal_bands: BandsData

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        points_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
        borders_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
        edges_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
        points_xs: Union[NumbersVector, DefaultValue] = DEFAULT,
        points_ys: Union[NumbersVector, DefaultValue] = DEFAULT,
        points_sizes: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
        points_colors: Union[Optional[ColorsVector], DefaultValue] = DEFAULT,
        points_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        points_mask: Union[Optional[BoolsVector], DefaultValue] = DEFAULT,
        points_order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
        borders_colors: Union[Optional[ColorsVector], DefaultValue] = DEFAULT,
        borders_sizes: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
        borders_mask: Union[Optional[BoolsVector], DefaultValue] = DEFAULT,
        edges_points: Union[Optional[EdgesVector], DefaultValue] = DEFAULT,
        edges_colors: Union[Optional[ColorsVector], DefaultValue] = DEFAULT,
        edges_sizes: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
        edges_styles: Union[Optional[Sequence[LineStyle]], DefaultValue] = DEFAULT,
        edges_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        edges_mask: Union[Optional[BoolsVector], DefaultValue] = DEFAULT,
        edges_order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.PointsGraphData(
                **_given(
                    figure_title=figure_title,
                    x_axis_title=x_axis_title,
                    y_axis_title=y_axis_title,
                    points_colors_title=points_colors_title,
                    borders_colors_title=borders_colors_title,
                    edges_colors_title=edges_colors_title,
                    points_xs=points_xs,
                    points_ys=points_ys,
                    points_sizes=points_sizes,
                    points_colors=points_colors,
                    points_hovers=points_hovers,
                    points_mask=points_mask,
                    points_order=points_order,
                    borders_colors=borders_colors,
                    borders_sizes=borders_sizes,
                    borders_mask=borders_mask,
                    edges_points=edges_points,
                    edges_colors=edges_colors,
                    edges_sizes=edges_sizes,
                    edges_styles=edges_styles,
                    edges_hovers=edges_hovers,
                    edges_mask=edges_mask,
                    edges_order=edges_order,
                    vertical_bands=vertical_bands,
                    horizontal_bands=horizontal_bands,
                    diagonal_bands=diagonal_bands,
                )
            )
        )


register_jl_type("PointsGraphData", PointsGraphData)


class PointsGraph(Graph):
    """
    A graph visualizing scattered points (possibly with edges between them). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.PointsGraph>`__
    for details.
    """

    #: What to display.
    data: PointsGraphData
    #: How to display it.
    configuration: PointsGraphConfiguration

    def __init__(
        self,
        *,
        data: Union[PointsGraphData, DefaultValue] = DEFAULT,
        configuration: Union[PointsGraphConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.PointsGraph(**_given(data=data, configuration=configuration)))


def points_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    points_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
    borders_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
    edges_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
    points_xs: Union[NumbersVector, DefaultValue] = DEFAULT,
    points_ys: Union[NumbersVector, DefaultValue] = DEFAULT,
    points_sizes: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
    points_colors: Union[Optional[ColorsVector], DefaultValue] = DEFAULT,
    points_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    points_mask: Union[Optional[BoolsVector], DefaultValue] = DEFAULT,
    points_order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
    borders_colors: Union[Optional[ColorsVector], DefaultValue] = DEFAULT,
    borders_sizes: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
    borders_mask: Union[Optional[BoolsVector], DefaultValue] = DEFAULT,
    edges_points: Union[Optional[EdgesVector], DefaultValue] = DEFAULT,
    edges_colors: Union[Optional[ColorsVector], DefaultValue] = DEFAULT,
    edges_sizes: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
    edges_styles: Union[Optional[Sequence[LineStyle]], DefaultValue] = DEFAULT,
    edges_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    edges_mask: Union[Optional[BoolsVector], DefaultValue] = DEFAULT,
    edges_order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
    vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
    horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    configuration: Union[PointsGraphConfiguration, DefaultValue] = DEFAULT,
) -> PointsGraph:
    """
    Create a :py:obj:`PointsGraph` by specifying only the :py:obj:`PointsGraphData` fields (with an optional
    :py:obj:`PointsGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.points_graph>`__
    for details.
    """
    return PointsGraph(
        data=PointsGraphData(
            figure_title=figure_title,
            x_axis_title=x_axis_title,
            y_axis_title=y_axis_title,
            points_colors_title=points_colors_title,
            borders_colors_title=borders_colors_title,
            edges_colors_title=edges_colors_title,
            points_xs=points_xs,
            points_ys=points_ys,
            points_sizes=points_sizes,
            points_colors=points_colors,
            points_hovers=points_hovers,
            points_mask=points_mask,
            points_order=points_order,
            borders_colors=borders_colors,
            borders_sizes=borders_sizes,
            borders_mask=borders_mask,
            edges_points=edges_points,
            edges_colors=edges_colors,
            edges_sizes=edges_sizes,
            edges_styles=edges_styles,
            edges_hovers=edges_hovers,
            edges_mask=edges_mask,
            edges_order=edges_order,
            vertical_bands=vertical_bands,
            horizontal_bands=horizontal_bands,
            diagonal_bands=diagonal_bands,
        ),
        configuration=configuration,
    )


def points_density(points_xs: NumbersVector, points_ys: NumbersVector) -> NumbersVector:
    """
    Compute the density of the points, for coloring them. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.points_density>`__
    for details.
    """
    from .julia_import import _from_julia  # pylint: disable=import-outside-toplevel

    return _from_julia(jl.SomeGraphs.points_density(points_xs, points_ys))


class LineGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing a single line. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.LineGraphConfiguration>`__
    for details.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: The horizontal axis.
    x_axis: AxisConfiguration
    #: The vertical axis.
    y_axis: AxisConfiguration
    #: How to show the line.
    line: LineConfiguration
    #: Show a point at each of the line's coordinates.
    show_points: bool
    #: The diameter of the points, in pixels.
    points_size: Optional[float]
    #: The color of the points.
    points_color: Optional[str]
    #: Bands partitioning the graph by the horizontal axis.
    vertical_bands: BandsConfiguration
    #: Bands partitioning the graph by the vertical axis.
    horizontal_bands: BandsConfiguration
    #: Bands partitioning the graph parallel to the X = Y line.
    diagonal_bands: BandsConfiguration

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        x_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        y_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        line: Union[LineConfiguration, DefaultValue] = DEFAULT,
        show_points: Union[bool, DefaultValue] = DEFAULT,
        points_size: Union[Optional[float], DefaultValue] = DEFAULT,
        points_color: Union[Optional[str], DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.LineGraphConfiguration(
                **_given(
                    figure=figure,
                    x_axis=x_axis,
                    y_axis=y_axis,
                    line=line,
                    show_points=show_points,
                    points_size=points_size,
                    points_color=points_color,
                    vertical_bands=vertical_bands,
                    horizontal_bands=horizontal_bands,
                    diagonal_bands=diagonal_bands,
                )
            )
        )


register_jl_type("LineGraphConfiguration", LineGraphConfiguration)


class LineGraphData(AbstractGraphData):
    """
    The data of a graph showing a single line. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.LineGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The title of the horizontal axis.
    x_axis_title: Optional[str]
    #: The title of the vertical axis.
    y_axis_title: Optional[str]
    #: The horizontal coordinate of each point of the line.
    points_xs: NumbersVector
    #: The vertical coordinate of each point of the line.
    points_ys: NumbersVector
    #: The hover text of each point of the line.
    points_hovers: Optional[StringsVector]
    #: Override the offsets of the vertical bands.
    vertical_bands: BandsData
    #: Override the offsets of the horizontal bands.
    horizontal_bands: BandsData
    #: Override the offsets of the diagonal bands.
    diagonal_bands: BandsData

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        points_xs: Union[NumbersVector, DefaultValue] = DEFAULT,
        points_ys: Union[NumbersVector, DefaultValue] = DEFAULT,
        points_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.LineGraphData(
                **_given(
                    figure_title=figure_title,
                    x_axis_title=x_axis_title,
                    y_axis_title=y_axis_title,
                    points_xs=points_xs,
                    points_ys=points_ys,
                    points_hovers=points_hovers,
                    vertical_bands=vertical_bands,
                    horizontal_bands=horizontal_bands,
                    diagonal_bands=diagonal_bands,
                )
            )
        )


register_jl_type("LineGraphData", LineGraphData)


class LineGraph(Graph):
    """
    A graph visualizing a single line. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.LineGraph>`__
    for details.
    """

    #: What to display.
    data: LineGraphData
    #: How to display it.
    configuration: LineGraphConfiguration

    def __init__(
        self,
        *,
        data: Union[LineGraphData, DefaultValue] = DEFAULT,
        configuration: Union[LineGraphConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.LineGraph(**_given(data=data, configuration=configuration)))


def line_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    points_xs: Union[NumbersVector, DefaultValue] = DEFAULT,
    points_ys: Union[NumbersVector, DefaultValue] = DEFAULT,
    points_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
    horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    configuration: Union[LineGraphConfiguration, DefaultValue] = DEFAULT,
) -> LineGraph:
    """
    Create a :py:obj:`LineGraph` by specifying only the :py:obj:`LineGraphData` fields (with an optional
    :py:obj:`LineGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.line_graph>`__
    for details.
    """
    return LineGraph(
        data=LineGraphData(
            figure_title=figure_title,
            x_axis_title=x_axis_title,
            y_axis_title=y_axis_title,
            points_xs=points_xs,
            points_ys=points_ys,
            points_hovers=points_hovers,
            vertical_bands=vertical_bands,
            horizontal_bands=horizontal_bands,
            diagonal_bands=diagonal_bands,
        ),
        configuration=configuration,
    )


class LinesGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing multiple lines. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.LinesGraphConfiguration>`__
    for details.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: The horizontal axis.
    x_axis: AxisConfiguration
    #: The vertical axis.
    y_axis: AxisConfiguration
    #: How to show the lines.
    line: LineConfiguration
    #: Show a point at each of the lines' coordinates.
    show_points: bool
    #: The diameter of the points, in pixels.
    points_size: Optional[float]
    #: The color of the points.
    points_color: Optional[str]
    #: Bands partitioning the graph by the horizontal axis.
    vertical_bands: BandsConfiguration
    #: Bands partitioning the graph by the vertical axis.
    horizontal_bands: BandsConfiguration
    #: Bands partitioning the graph parallel to the X = Y line.
    diagonal_bands: BandsConfiguration
    #: Show a legend of the lines.
    show_legend: bool
    #: Stack the lines on top of each other.
    stacking: Optional[Stacking]

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        x_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        y_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        line: Union[LineConfiguration, DefaultValue] = DEFAULT,
        show_points: Union[bool, DefaultValue] = DEFAULT,
        points_size: Union[Optional[float], DefaultValue] = DEFAULT,
        points_color: Union[Optional[str], DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        show_legend: Union[bool, DefaultValue] = DEFAULT,
        stacking: Union[Optional[Stacking], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.LinesGraphConfiguration(
                **_given(
                    figure=figure,
                    x_axis=x_axis,
                    y_axis=y_axis,
                    line=line,
                    show_points=show_points,
                    points_size=points_size,
                    points_color=points_color,
                    vertical_bands=vertical_bands,
                    horizontal_bands=horizontal_bands,
                    diagonal_bands=diagonal_bands,
                    show_legend=show_legend,
                    stacking=stacking,
                )
            )
        )


register_jl_type("LinesGraphConfiguration", LinesGraphConfiguration)


class LinesGraphData(AbstractGraphData):
    """
    The data of a graph showing multiple lines. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.LinesGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The title of the horizontal axis.
    x_axis_title: Optional[str]
    #: The title of the vertical axis.
    y_axis_title: Optional[str]
    #: The title of each line, shown in the legend.
    lines_titles: Optional[StringsVector]
    #: The horizontal coordinates of the points of each line.
    lines_points_xs: Sequence[NumbersVector]
    #: The vertical coordinates of the points of each line.
    lines_points_ys: Sequence[NumbersVector]
    #: The diameter of the points of each line, in pixels.
    lines_points_sizes: Optional[NumbersVector]
    #: The color of the points of each line.
    lines_points_colors: Optional[StringsVector]
    #: The width of each line, in pixels.
    lines_widths: Optional[NumbersVector]
    #: The color of each line.
    lines_colors: Optional[StringsVector]
    #: The style of each line.
    lines_styles: Optional[Sequence[LineStyle]]
    #: The order to draw the lines in, controlling which are on top.
    lines_order: Optional[IntegersVector]
    #: Override the offsets of the vertical bands.
    vertical_bands: BandsData
    #: Override the offsets of the horizontal bands.
    horizontal_bands: BandsData
    #: Override the offsets of the diagonal bands.
    diagonal_bands: BandsData

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        lines_titles: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        lines_points_xs: Union[Sequence[NumbersVector], DefaultValue] = DEFAULT,
        lines_points_ys: Union[Sequence[NumbersVector], DefaultValue] = DEFAULT,
        lines_points_sizes: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
        lines_points_colors: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        lines_widths: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
        lines_colors: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        lines_styles: Union[Optional[Sequence[LineStyle]], DefaultValue] = DEFAULT,
        lines_order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.LinesGraphData(
                **_given(
                    figure_title=figure_title,
                    x_axis_title=x_axis_title,
                    y_axis_title=y_axis_title,
                    lines_titles=lines_titles,
                    lines_points_xs=lines_points_xs,
                    lines_points_ys=lines_points_ys,
                    lines_points_sizes=lines_points_sizes,
                    lines_points_colors=lines_points_colors,
                    lines_widths=lines_widths,
                    lines_colors=lines_colors,
                    lines_styles=lines_styles,
                    lines_order=lines_order,
                    vertical_bands=vertical_bands,
                    horizontal_bands=horizontal_bands,
                    diagonal_bands=diagonal_bands,
                )
            )
        )


register_jl_type("LinesGraphData", LinesGraphData)


class LinesGraph(Graph):
    """
    A graph visualizing multiple lines. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.LinesGraph>`__
    for details.
    """

    #: What to display.
    data: LinesGraphData
    #: How to display it.
    configuration: LinesGraphConfiguration

    def __init__(
        self,
        *,
        data: Union[LinesGraphData, DefaultValue] = DEFAULT,
        configuration: Union[LinesGraphConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.LinesGraph(**_given(data=data, configuration=configuration)))


def lines_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    lines_titles: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    lines_points_xs: Union[Sequence[NumbersVector], DefaultValue] = DEFAULT,
    lines_points_ys: Union[Sequence[NumbersVector], DefaultValue] = DEFAULT,
    lines_points_sizes: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
    lines_points_colors: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    lines_widths: Union[Optional[NumbersVector], DefaultValue] = DEFAULT,
    lines_colors: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    lines_styles: Union[Optional[Sequence[LineStyle]], DefaultValue] = DEFAULT,
    lines_order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
    vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
    horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    configuration: Union[LinesGraphConfiguration, DefaultValue] = DEFAULT,
) -> LinesGraph:
    """
    Create a :py:obj:`LinesGraph` by specifying only the :py:obj:`LinesGraphData` fields (with an optional
    :py:obj:`LinesGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.lines_graph>`__
    for details.
    """
    return LinesGraph(
        data=LinesGraphData(
            figure_title=figure_title,
            x_axis_title=x_axis_title,
            y_axis_title=y_axis_title,
            lines_titles=lines_titles,
            lines_points_xs=lines_points_xs,
            lines_points_ys=lines_points_ys,
            lines_points_sizes=lines_points_sizes,
            lines_points_colors=lines_points_colors,
            lines_widths=lines_widths,
            lines_colors=lines_colors,
            lines_styles=lines_styles,
            lines_order=lines_order,
            vertical_bands=vertical_bands,
            horizontal_bands=horizontal_bands,
            diagonal_bands=diagonal_bands,
        ),
        configuration=configuration,
    )
