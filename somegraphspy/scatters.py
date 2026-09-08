"""
Scatter graphs: points and lines. See the Julia
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
from .common import EntitiesData
from .common import FigureConfiguration
from .common import Graph
from .common import IntegersVector
from .common import LineConfiguration
from .common import LineStyle
from .common import NumbersVector
from .common import SizesConfiguration
from .common import Stacking
from .common import ValuesData
from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import JlObject
from .julia_import import _from_julia
from .julia_import import _given
from .julia_import import _optional_jl_obj
from .julia_import import jl
from .julia_import import register_jl_type
from .sources import AxisFields
from .sources import ColorsFields
from .sources import SizesFields

__all__ = [
    "BordersData",
    "EdgesData",
    "LineData",
    "LineGraph",
    "LineGraphConfiguration",
    "LineGraphData",
    "LinesGraph",
    "LinesGraphConfiguration",
    "LinesGraphData",
    "PointsData",
    "PointsGraph",
    "PointsGraphConfiguration",
    "PointsGraphData",
    "ScattersConfiguration",
    "line_graph",
    "lines_graph",
    "points_density",
    "points_graph",
]

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


class PointsData(JlObject):
    """
    The per-point data of a :py:obj:`PointsGraphData`. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.PointsData>`__
    for details.
    """

    #: The color of each point; their title is the legend title.
    colors: ValuesData
    #: The size of each point.
    sizes: ValuesData
    #: The hovers and mask of the points.
    entities: EntitiesData
    #: The (1-based) order to draw the points in, controlling which are on top.
    order: Optional[IntegersVector]

    def __init__(
        self,
        *,
        colors: Union[ValuesData, DefaultValue] = DEFAULT,
        sizes: Union[ValuesData, DefaultValue] = DEFAULT,
        entities: Union[EntitiesData, DefaultValue] = DEFAULT,
        order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.PointsData(**_given(colors=colors, sizes=sizes, entities=entities, order=order)))


register_jl_type("PointsData", PointsData)


class BordersData(JlObject):
    """
    The per-point data of the borders of a :py:obj:`PointsGraphData`. The borders share the hovers and order of the
    points. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.BordersData>`__
    for details.
    """

    #: The color of the border of each point; their title is the legend title.
    colors: ValuesData
    #: The size added to each point for its border.
    sizes: ValuesData
    #: Which borders to show.
    mask: Optional[BoolsVector]

    def __init__(
        self,
        *,
        colors: Union[ValuesData, DefaultValue] = DEFAULT,
        sizes: Union[ValuesData, DefaultValue] = DEFAULT,
        mask: Union[Optional[BoolsVector], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.BordersData(**_given(colors=colors, sizes=sizes, mask=mask)))


register_jl_type("BordersData", BordersData)


class EdgesData(JlObject):
    """
    The per-edge data of a :py:obj:`PointsGraphData`. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.EdgesData>`__
    for details.
    """

    #: The pairs of (1-based) point indices to draw edges between.
    points: Optional[EdgesVector]
    #: The color of each edge; their title is the legend title.
    colors: ValuesData
    #: The width of each edge.
    sizes: ValuesData
    #: The style of each edge.
    styles: Optional[Sequence[LineStyle]]
    #: The hovers and mask of the edges.
    entities: EntitiesData
    #: The (1-based) order to draw the edges in, controlling which are on top.
    order: Optional[IntegersVector]

    def __init__(
        self,
        *,
        points: Union[Optional[EdgesVector], DefaultValue] = DEFAULT,
        colors: Union[ValuesData, DefaultValue] = DEFAULT,
        sizes: Union[ValuesData, DefaultValue] = DEFAULT,
        styles: Union[Optional[Sequence[LineStyle]], DefaultValue] = DEFAULT,
        entities: Union[EntitiesData, DefaultValue] = DEFAULT,
        order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.EdgesData(
                **_given(points=points, colors=colors, sizes=sizes, styles=styles, entities=entities, order=order)
            )
        )


register_jl_type("EdgesData", EdgesData)


class PointsGraphData(AbstractGraphData):
    """
    The data of a scatter graph of points. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.PointsGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The horizontal coordinate of each point; their title is the horizontal axis title.
    x: ValuesData
    #: The vertical coordinate of each point; their title is the vertical axis title.
    y: ValuesData
    #: The colors, sizes, hovers, mask and order of the points.
    points: PointsData
    #: The colors, sizes and mask of the borders of the points.
    borders: BordersData
    #: The edges between the points.
    edges: EdgesData
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
        x: Union[ValuesData, DefaultValue] = DEFAULT,
        y: Union[ValuesData, DefaultValue] = DEFAULT,
        points: Union[PointsData, DefaultValue] = DEFAULT,
        borders: Union[BordersData, DefaultValue] = DEFAULT,
        edges: Union[EdgesData, DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.PointsGraphData(
                **_given(
                    figure_title=figure_title,
                    x=x,
                    y=y,
                    points=points,
                    borders=borders,
                    edges=edges,
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

    def x_fields(self) -> AxisFields:
        """
        The data source view of the X coordinates of the points, along the ``x_axis``.
        """
        return _from_julia(jl.SomeGraphs.x_fields(self.jl_obj))

    def y_fields(self) -> AxisFields:
        """
        The data source view of the Y coordinates of the points, along the ``y_axis``.
        """
        return _from_julia(jl.SomeGraphs.y_fields(self.jl_obj))

    def points_colors_fields(self) -> ColorsFields:
        """
        The data source view of the colors of the points.
        """
        return _from_julia(jl.SomeGraphs.points_colors_fields(self.jl_obj))

    def points_sizes_fields(self) -> SizesFields:
        """
        The data source view of the sizes of the points.
        """
        return _from_julia(jl.SomeGraphs.points_sizes_fields(self.jl_obj))

    def borders_colors_fields(self) -> ColorsFields:
        """
        The data source view of the colors of the borders of the points, which share the entities of the points.
        """
        return _from_julia(jl.SomeGraphs.borders_colors_fields(self.jl_obj))

    def borders_sizes_fields(self) -> SizesFields:
        """
        The data source view of the sizes of the borders of the points, which share the entities of the points.
        """
        return _from_julia(jl.SomeGraphs.borders_sizes_fields(self.jl_obj))

    def edges_colors_fields(self) -> ColorsFields:
        """
        The data source view of the colors of the edges.
        """
        return _from_julia(jl.SomeGraphs.edges_colors_fields(self.jl_obj))

    def edges_sizes_fields(self) -> SizesFields:
        """
        The data source view of the sizes (widths) of the edges.
        """
        return _from_julia(jl.SomeGraphs.edges_sizes_fields(self.jl_obj))


def points_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    x: Union[ValuesData, DefaultValue] = DEFAULT,
    y: Union[ValuesData, DefaultValue] = DEFAULT,
    points: Union[PointsData, DefaultValue] = DEFAULT,
    borders: Union[BordersData, DefaultValue] = DEFAULT,
    edges: Union[EdgesData, DefaultValue] = DEFAULT,
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
            x=x,
            y=y,
            points=points,
            borders=borders,
            edges=edges,
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
    #: The horizontal coordinate of each point of the line; their title is the horizontal axis title.
    x: ValuesData
    #: The vertical coordinate of each point of the line; their title is the vertical axis title.
    y: ValuesData
    #: The hovers and mask of the points of the line.
    points: EntitiesData
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
        x: Union[ValuesData, DefaultValue] = DEFAULT,
        y: Union[ValuesData, DefaultValue] = DEFAULT,
        points: Union[EntitiesData, DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.LineGraphData(
                **_given(
                    figure_title=figure_title,
                    x=x,
                    y=y,
                    points=points,
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

    def x_fields(self) -> AxisFields:
        """
        The data source view of the X coordinates of the points of the line, along the ``x_axis``.
        """
        return _from_julia(jl.SomeGraphs.x_fields(self.jl_obj))

    def y_fields(self) -> AxisFields:
        """
        The data source view of the Y coordinates of the points of the line, along the ``y_axis``.
        """
        return _from_julia(jl.SomeGraphs.y_fields(self.jl_obj))


def line_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    x: Union[ValuesData, DefaultValue] = DEFAULT,
    y: Union[ValuesData, DefaultValue] = DEFAULT,
    points: Union[EntitiesData, DefaultValue] = DEFAULT,
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
            x=x,
            y=y,
            points=points,
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


class LineData(JlObject):
    """
    One line of a :py:obj:`LinesGraphData`. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.LineData>`__
    for details.
    """

    #: The horizontal coordinate of each point of the line; their title is the horizontal axis title.
    x: ValuesData
    #: The vertical coordinate of each point of the line; their title is the vertical axis title.
    y: ValuesData
    #: The hovers and mask of the points of the line.
    points: EntitiesData
    #: The name of the line, shown in the legend.
    name: Optional[str]
    #: Prefixed to the hover of each point of the line.
    hover: Optional[str]
    #: Whether to show the line at all.
    is_shown: bool
    #: The color of the line.
    color: Optional[str]
    #: The width of the line, in pixels.
    width: Optional[float]
    #: The style of the line.
    style: Optional[LineStyle]
    #: The diameter of the points of the line, in pixels.
    points_size: Optional[float]
    #: The color of the points of the line.
    points_color: Optional[str]

    def __init__(
        self,
        *,
        x: Union[ValuesData, DefaultValue] = DEFAULT,
        y: Union[ValuesData, DefaultValue] = DEFAULT,
        points: Union[EntitiesData, DefaultValue] = DEFAULT,
        name: Union[Optional[str], DefaultValue] = DEFAULT,
        hover: Union[Optional[str], DefaultValue] = DEFAULT,
        is_shown: Union[bool, DefaultValue] = DEFAULT,
        color: Union[Optional[str], DefaultValue] = DEFAULT,
        width: Union[Optional[float], DefaultValue] = DEFAULT,
        style: Union[Optional[LineStyle], DefaultValue] = DEFAULT,
        points_size: Union[Optional[float], DefaultValue] = DEFAULT,
        points_color: Union[Optional[str], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.LineData(
                **_given(
                    x=x,
                    y=y,
                    points=points,
                    name=name,
                    hover=hover,
                    is_shown=is_shown,
                    color=color,
                    width=width,
                    style=style,
                    points_size=points_size,
                    points_color=points_color,
                )
            )
        )


register_jl_type("LineData", LineData)


class LinesGraphData(AbstractGraphData):
    """
    The data of a graph showing multiple lines. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/scatters.html#SomeGraphs.Scatters.LinesGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The lines to show.
    lines: Sequence[LineData]
    #: The (1-based) order to draw the lines in, controlling which are on top.
    order: Optional[IntegersVector]
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
        lines: Union[Sequence[LineData], DefaultValue] = DEFAULT,
        order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
        vertical_bands: Union[BandsData, DefaultValue] = DEFAULT,
        horizontal_bands: Union[BandsData, DefaultValue] = DEFAULT,
        diagonal_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.LinesGraphData(
                **_given(
                    figure_title=figure_title,
                    lines=lines,
                    order=order,
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

    def x_fields(self, index: int) -> AxisFields:
        """
        The data source view of the X coordinates of the points of the (1-based) ``index`` line, along the (shared)
        ``x_axis``.
        """
        return _from_julia(jl.SomeGraphs.x_fields(self.jl_obj, index))

    def y_fields(self, index: int) -> AxisFields:
        """
        The data source view of the Y coordinates of the points of the (1-based) ``index`` line, along the (shared)
        ``y_axis``.
        """
        return _from_julia(jl.SomeGraphs.y_fields(self.jl_obj, index))

    def add_line(self, line: Optional[LineData] = None) -> int:
        """
        Append a ``line`` (by default, an empty one) and return its (1-based) index, for :py:obj:`x_fields` and
        :py:obj:`y_fields`. Whatever the line leaves at its defaults can be set later, through the views or directly.
        """
        return int(jl.SomeGraphs.add_line_b(self.jl_obj, *_optional_jl_obj(line)))


def lines_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    lines: Union[Sequence[LineData], DefaultValue] = DEFAULT,
    order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
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
            lines=lines,
            order=order,
            vertical_bands=vertical_bands,
            horizontal_bands=horizontal_bands,
            diagonal_bands=diagonal_bands,
        ),
        configuration=configuration,
    )
