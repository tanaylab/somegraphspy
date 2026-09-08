"""
Graphs showing bars. See the Julia
`documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html>`__ for details.
"""

from typing import Optional
from typing import Sequence
from typing import Union

from .common import AbstractGraphConfiguration
from .common import AbstractGraphData
from .common import AnnotationData
from .common import AnnotationSize
from .common import AxisConfiguration
from .common import BandsConfiguration
from .common import BandsData
from .common import ColorsConfiguration
from .common import EntitiesData
from .common import FigureConfiguration
from .common import Graph
from .common import Stacking
from .common import Validated
from .common import ValuesData
from .common import ValuesOrientation
from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import JlObject
from .julia_import import _from_julia
from .julia_import import _given
from .julia_import import jl
from .julia_import import register_jl_type
from .sources import AxisFields
from .sources import ColorsFields
from .sources import VectorDataFields

__all__ = [
    "BarsConfiguration",
    "BarsGraph",
    "BarsGraphConfiguration",
    "BarsGraphData",
    "SeriesBarsGraph",
    "SeriesBarsGraphConfiguration",
    "SeriesBarsGraphData",
    "SeriesData",
    "bars_graph",
    "series_bars_graph",
]


class BarsConfiguration(Validated):
    """
    Configure the bars of a bars graph. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.BarsConfiguration>`__
    for details.
    """

    #: The gap between the bars, as a fraction of the total graph size.
    gap: float

    def __init__(self, *, gap: Union[float, DefaultValue] = DEFAULT) -> None:
        super().__init__(jl.SomeGraphs.BarsConfiguration(**_given(gap=gap)))


register_jl_type("BarsConfiguration", BarsConfiguration)


class BarsGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing a single series of bars. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.BarsGraphConfiguration>`__
    for details.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: The axis showing the values of the bars.
    value_axis: AxisConfiguration
    #: Bands partitioning the graph by the value axis.
    value_bands: BandsConfiguration
    #: Whether the values are shown in the vertical or the horizontal axis.
    values_orientation: ValuesOrientation
    #: How to color the bars.
    colors: ColorsConfiguration
    #: How to show the bars.
    bars: BarsConfiguration
    #: The size of the annotations shown next to the bars.
    annotations: AnnotationSize

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        value_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        value_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        values_orientation: Union[ValuesOrientation, DefaultValue] = DEFAULT,
        colors: Union[ColorsConfiguration, DefaultValue] = DEFAULT,
        bars: Union[BarsConfiguration, DefaultValue] = DEFAULT,
        annotations: Union[AnnotationSize, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.BarsGraphConfiguration(
                **_given(
                    figure=figure,
                    value_axis=value_axis,
                    value_bands=value_bands,
                    values_orientation=values_orientation,
                    colors=colors,
                    bars=bars,
                    annotations=annotations,
                )
            )
        )


register_jl_type("BarsGraphConfiguration", BarsGraphConfiguration)


class BarsGraphData(AbstractGraphData):
    """
    The data of a graph showing a single series of bars. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.BarsGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The value of each bar; their title is the value axis title.
    values: ValuesData
    #: The name of each bar; their title is the bar axis title.
    names: ValuesData
    #: The hovers and mask of the bars.
    bars: EntitiesData
    #: The color of each bar; their title is the legend title.
    colors: ValuesData
    #: Annotations shown next to the bars.
    annotations: Sequence[AnnotationData]
    #: Override the offsets of the value bands.
    value_bands: BandsData

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        values: Union[ValuesData, DefaultValue] = DEFAULT,
        names: Union[ValuesData, DefaultValue] = DEFAULT,
        bars: Union[EntitiesData, DefaultValue] = DEFAULT,
        colors: Union[ValuesData, DefaultValue] = DEFAULT,
        annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
        value_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.BarsGraphData(
                **_given(
                    figure_title=figure_title,
                    values=values,
                    names=names,
                    bars=bars,
                    colors=colors,
                    annotations=annotations,
                    value_bands=value_bands,
                )
            )
        )


register_jl_type("BarsGraphData", BarsGraphData)


class BarsGraph(Graph):
    """
    A graph visualizing a single series of bars. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.BarsGraph>`__
    for details.
    """

    #: What to display.
    data: BarsGraphData
    #: How to display it.
    configuration: BarsGraphConfiguration

    def __init__(
        self,
        *,
        data: Union[BarsGraphData, DefaultValue] = DEFAULT,
        configuration: Union[BarsGraphConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.BarsGraph(**_given(data=data, configuration=configuration)))

    def values_fields(self) -> AxisFields:
        """
        The data source view of the values of the bars, along the ``value_axis``.
        """
        return _from_julia(jl.SomeGraphs.values_fields(self.jl_obj))

    def colors_fields(self) -> ColorsFields:
        """
        The data source view of the colors of the bars.
        """
        return _from_julia(jl.SomeGraphs.colors_fields(self.jl_obj))

    def names_fields(self) -> VectorDataFields:
        """
        The data source view of the names of the bars; their title is the title of the bars axis.
        """
        return _from_julia(jl.SomeGraphs.names_fields(self.jl_obj))

    def annotations_fields(self, index: int) -> ColorsFields:
        """
        The data source view of the (1-based) ``index`` annotation of the bars, which shares the entities of the bars.
        """
        return _from_julia(jl.SomeGraphs.annotations_fields(self.jl_obj, index))


def bars_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    values: Union[ValuesData, DefaultValue] = DEFAULT,
    names: Union[ValuesData, DefaultValue] = DEFAULT,
    bars: Union[EntitiesData, DefaultValue] = DEFAULT,
    colors: Union[ValuesData, DefaultValue] = DEFAULT,
    annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
    value_bands: Union[BandsData, DefaultValue] = DEFAULT,
    configuration: Union[BarsGraphConfiguration, DefaultValue] = DEFAULT,
) -> BarsGraph:
    """
    Create a :py:obj:`BarsGraph` by specifying only the :py:obj:`BarsGraphData` fields (with an optional
    :py:obj:`BarsGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.bars_graph>`__
    for details.
    """
    return BarsGraph(
        data=BarsGraphData(
            figure_title=figure_title,
            values=values,
            names=names,
            bars=bars,
            colors=colors,
            annotations=annotations,
            value_bands=value_bands,
        ),
        configuration=configuration,
    )


class SeriesBarsGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing multiple series of bars. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.SeriesBarsGraphConfiguration>`__
    for details.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: The axis showing the values of the bars.
    value_axis: AxisConfiguration
    #: Whether the values are shown in the vertical or the horizontal axis.
    values_orientation: ValuesOrientation
    #: How to show the bars.
    bars: BarsConfiguration
    #: The size of the annotations shown next to the bars.
    annotations: AnnotationSize
    #: The gap between the series of each bar, as a fraction of the bar size.
    series_gap: Optional[float]
    #: Stack the series on top of each other.
    stacking: Optional[Stacking]
    #: Show the series in pairs, the 1st of each pair growing away from the bar axis in the opposite direction.
    mirrored: bool

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        value_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        values_orientation: Union[ValuesOrientation, DefaultValue] = DEFAULT,
        bars: Union[BarsConfiguration, DefaultValue] = DEFAULT,
        annotations: Union[AnnotationSize, DefaultValue] = DEFAULT,
        series_gap: Union[Optional[float], DefaultValue] = DEFAULT,
        stacking: Union[Optional[Stacking], DefaultValue] = DEFAULT,
        mirrored: Union[bool, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.SeriesBarsGraphConfiguration(
                **_given(
                    figure=figure,
                    value_axis=value_axis,
                    values_orientation=values_orientation,
                    bars=bars,
                    annotations=annotations,
                    series_gap=series_gap,
                    stacking=stacking,
                    mirrored=mirrored,
                )
            )
        )


register_jl_type("SeriesBarsGraphConfiguration", SeriesBarsGraphConfiguration)


class SeriesData(JlObject):
    """
    One series of a :py:obj:`SeriesBarsGraphData`. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.SeriesData>`__
    for details.
    """

    #: The value of each bar of the series; their title is the value axis title shared by all the series.
    values: ValuesData
    #: The hovers and mask of the bars of this series alone.
    bars: EntitiesData
    #: The name of the series.
    name: Optional[str]
    #: Prefixed to the hover of each bar of the series.
    hover: Optional[str]
    #: The color of all the bars of the series.
    color: Optional[str]

    def __init__(
        self,
        *,
        values: Union[ValuesData, DefaultValue] = DEFAULT,
        bars: Union[EntitiesData, DefaultValue] = DEFAULT,
        name: Union[Optional[str], DefaultValue] = DEFAULT,
        hover: Union[Optional[str], DefaultValue] = DEFAULT,
        color: Union[Optional[str], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.SeriesData(**_given(values=values, bars=bars, name=name, hover=hover, color=color))
        )


register_jl_type("SeriesData", SeriesData)


class SeriesBarsGraphData(AbstractGraphData):
    """
    The data of a graph showing multiple series of bars. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.SeriesBarsGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The series of bars.
    series: Sequence[SeriesData]
    #: The name of each bar; their title is the bar axis title.
    names: ValuesData
    #: The hovers and mask of the bars, shared by all the series.
    bars: EntitiesData
    #: Annotations shown next to the bars.
    annotations: Sequence[AnnotationData]

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        series: Union[Sequence[SeriesData], DefaultValue] = DEFAULT,
        names: Union[ValuesData, DefaultValue] = DEFAULT,
        bars: Union[EntitiesData, DefaultValue] = DEFAULT,
        annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.SeriesBarsGraphData(
                **_given(figure_title=figure_title, series=series, names=names, bars=bars, annotations=annotations)
            )
        )


register_jl_type("SeriesBarsGraphData", SeriesBarsGraphData)


class SeriesBarsGraph(Graph):
    """
    A graph visualizing multiple series of bars. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.SeriesBarsGraph>`__
    for details.
    """

    #: What to display.
    data: SeriesBarsGraphData
    #: How to display it.
    configuration: SeriesBarsGraphConfiguration

    def __init__(
        self,
        *,
        data: Union[SeriesBarsGraphData, DefaultValue] = DEFAULT,
        configuration: Union[SeriesBarsGraphConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.SeriesBarsGraph(**_given(data=data, configuration=configuration)))

    def series_values_fields(self, index: int) -> AxisFields:
        """
        The data source view of the values of the (1-based) ``index`` series, along the (shared) ``value_axis``. The
        entities are the bars of the series alone.
        """
        return _from_julia(jl.SomeGraphs.series_values_fields(self.jl_obj, index))

    def names_fields(self) -> VectorDataFields:
        """
        The data source view of the names of the bars (shared by all the series); their title is the title of the bars
        axis.
        """
        return _from_julia(jl.SomeGraphs.names_fields(self.jl_obj))

    def annotations_fields(self, index: int) -> ColorsFields:
        """
        The data source view of the (1-based) ``index`` annotation of the bars, which shares the entities of the bars
        (the ones shared by all the series).
        """
        return _from_julia(jl.SomeGraphs.annotations_fields(self.jl_obj, index))


def series_bars_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    series: Union[Sequence[SeriesData], DefaultValue] = DEFAULT,
    names: Union[ValuesData, DefaultValue] = DEFAULT,
    bars: Union[EntitiesData, DefaultValue] = DEFAULT,
    annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
    configuration: Union[SeriesBarsGraphConfiguration, DefaultValue] = DEFAULT,
) -> SeriesBarsGraph:
    """
    Create a :py:obj:`SeriesBarsGraph` by specifying only the :py:obj:`SeriesBarsGraphData` fields (with an optional
    :py:obj:`SeriesBarsGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.series_bars_graph>`__
    for details.
    """
    return SeriesBarsGraph(
        data=SeriesBarsGraphData(
            figure_title=figure_title, series=series, names=names, bars=bars, annotations=annotations
        ),
        configuration=configuration,
    )
