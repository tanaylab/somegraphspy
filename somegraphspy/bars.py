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
from .common import FigureConfiguration
from .common import Graph
from .common import NumbersVector
from .common import Stacking
from .common import StringsVector
from .common import ValuesOrientation
from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import _given
from .julia_import import jl
from .julia_import import register_jl_type

__all__ = [
    "BarsGraph",
    "BarsGraphConfiguration",
    "BarsGraphData",
    "SeriesBarsGraph",
    "SeriesBarsGraphConfiguration",
    "SeriesBarsGraphData",
    "bars_graph",
    "series_bars_graph",
]

#: The colors of a set of bars, either explicit color names or values to map through a palette.
ColorsVector = Union[NumbersVector, StringsVector]


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
    bars_colors: ColorsConfiguration
    #: The gap between the bars, as a fraction of the bar size.
    bars_gap: float
    #: The size of the annotations shown next to the bars.
    bars_annotations: AnnotationSize

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        value_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        value_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        values_orientation: Union[ValuesOrientation, DefaultValue] = DEFAULT,
        bars_colors: Union[ColorsConfiguration, DefaultValue] = DEFAULT,
        bars_gap: Union[float, DefaultValue] = DEFAULT,
        bars_annotations: Union[AnnotationSize, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.BarsGraphConfiguration(
                **_given(
                    figure=figure,
                    value_axis=value_axis,
                    value_bands=value_bands,
                    values_orientation=values_orientation,
                    bars_colors=bars_colors,
                    bars_gap=bars_gap,
                    bars_annotations=bars_annotations,
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
    #: The title of the axis listing the bars.
    bar_axis_title: Optional[str]
    #: The title of the axis showing the values.
    value_axis_title: Optional[str]
    #: The title of the bars colors legend.
    bars_colors_title: Optional[str]
    #: The value of each bar.
    bars_values: NumbersVector
    #: The name of each bar.
    bars_names: Optional[StringsVector]
    #: The color of each bar.
    bars_colors: Optional[ColorsVector]
    #: The hover text of each bar.
    bars_hovers: Optional[StringsVector]
    #: Override the offsets of the value bands.
    value_bands: BandsData
    #: Annotations shown next to the bars.
    bars_annotations: Sequence[AnnotationData]

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        bar_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        value_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        bars_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
        bars_values: Union[NumbersVector, DefaultValue] = DEFAULT,
        bars_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        bars_colors: Union[Optional[ColorsVector], DefaultValue] = DEFAULT,
        bars_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        value_bands: Union[BandsData, DefaultValue] = DEFAULT,
        bars_annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.BarsGraphData(
                **_given(
                    figure_title=figure_title,
                    bar_axis_title=bar_axis_title,
                    value_axis_title=value_axis_title,
                    bars_colors_title=bars_colors_title,
                    bars_values=bars_values,
                    bars_names=bars_names,
                    bars_colors=bars_colors,
                    bars_hovers=bars_hovers,
                    value_bands=value_bands,
                    bars_annotations=bars_annotations,
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


def bars_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    bar_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    value_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    bars_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
    bars_values: Union[NumbersVector, DefaultValue] = DEFAULT,
    bars_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    bars_colors: Union[Optional[ColorsVector], DefaultValue] = DEFAULT,
    bars_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    value_bands: Union[BandsData, DefaultValue] = DEFAULT,
    bars_annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
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
            bar_axis_title=bar_axis_title,
            value_axis_title=value_axis_title,
            bars_colors_title=bars_colors_title,
            bars_values=bars_values,
            bars_names=bars_names,
            bars_colors=bars_colors,
            bars_hovers=bars_hovers,
            value_bands=value_bands,
            bars_annotations=bars_annotations,
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
    #: The gap between the bars, as a fraction of the bar size.
    bars_gap: float
    #: The size of the annotations shown next to the bars.
    bars_annotations: AnnotationSize
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
        bars_gap: Union[float, DefaultValue] = DEFAULT,
        bars_annotations: Union[AnnotationSize, DefaultValue] = DEFAULT,
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
                    bars_gap=bars_gap,
                    bars_annotations=bars_annotations,
                    series_gap=series_gap,
                    stacking=stacking,
                    mirrored=mirrored,
                )
            )
        )


register_jl_type("SeriesBarsGraphConfiguration", SeriesBarsGraphConfiguration)


class SeriesBarsGraphData(AbstractGraphData):
    """
    The data of a graph showing multiple series of bars. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/bars.html#SomeGraphs.Bars.SeriesBarsGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The title of the axis listing the bars.
    bar_axis_title: Optional[str]
    #: The title of the axis showing the values.
    value_axis_title: Optional[str]
    #: The values of the bars of each series.
    series_bars_values: Sequence[NumbersVector]
    #: The name of each bar.
    bars_names: Optional[StringsVector]
    #: The hover text of each bar.
    bars_hovers: Optional[StringsVector]
    #: Annotations shown next to the bars.
    bars_annotations: Sequence[AnnotationData]
    #: The name of each series.
    series_names: Optional[StringsVector]
    #: The color of each series.
    series_colors: Optional[StringsVector]
    #: The hover text of each series.
    series_hovers: Optional[StringsVector]

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        bar_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        value_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        series_bars_values: Union[Sequence[NumbersVector], DefaultValue] = DEFAULT,
        bars_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        bars_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        bars_annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
        series_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        series_colors: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        series_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.SeriesBarsGraphData(
                **_given(
                    figure_title=figure_title,
                    bar_axis_title=bar_axis_title,
                    value_axis_title=value_axis_title,
                    series_bars_values=series_bars_values,
                    bars_names=bars_names,
                    bars_hovers=bars_hovers,
                    bars_annotations=bars_annotations,
                    series_names=series_names,
                    series_colors=series_colors,
                    series_hovers=series_hovers,
                )
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


def series_bars_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    bar_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    value_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    series_bars_values: Union[Sequence[NumbersVector], DefaultValue] = DEFAULT,
    bars_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    bars_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    bars_annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
    series_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    series_colors: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    series_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
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
            figure_title=figure_title,
            bar_axis_title=bar_axis_title,
            value_axis_title=value_axis_title,
            series_bars_values=series_bars_values,
            bars_names=bars_names,
            bars_hovers=bars_hovers,
            bars_annotations=bars_annotations,
            series_names=series_names,
            series_colors=series_colors,
            series_hovers=series_hovers,
        ),
        configuration=configuration,
    )
