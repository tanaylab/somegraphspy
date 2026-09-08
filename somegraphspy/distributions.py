"""
Graphs showing distributions. See the Julia
`documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html>`__ for details.
"""

# The enum values are named exactly as they are in Julia, so they are not UPPER_CASE. The data classes mirror the Julia
# structures, which share fields, so the classes repeat each other.
# pylint: disable=invalid-name,duplicate-code

from typing import Optional
from typing import Sequence
from typing import Union

from .common import AbstractGraphConfiguration
from .common import AbstractGraphData
from .common import AxisConfiguration
from .common import BandsConfiguration
from .common import BandsData
from .common import EntitiesData
from .common import FigureConfiguration
from .common import Graph
from .common import IntegersVector
from .common import LineConfiguration
from .common import Validated
from .common import ValuesData
from .common import ValuesOrientation
from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import JlEnum
from .julia_import import JlObject
from .julia_import import _from_julia
from .julia_import import _given
from .julia_import import jl
from .julia_import import register_jl_type
from .sources import AxisFields

__all__ = [
    "DistributionConfiguration",
    "DistributionData",
    "DistributionGraph",
    "DistributionGraphConfiguration",
    "DistributionGraphData",
    "DistributionStyle",
    "DistributionsGraph",
    "DistributionsGraphConfiguration",
    "DistributionsGraphData",
    "distribution_graph",
    "distributions_graph",
]


class DistributionStyle(JlEnum):
    """
    The style used to show a distribution. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionStyle>`__
    for details.
    """

    #: Show the density of the distribution as a curve.
    CurveDistribution = "CurveDistribution"
    #: Show the density of the distribution as a symmetric violin.
    ViolinDistribution = "ViolinDistribution"
    #: Show the quantiles of the distribution as a box.
    BoxDistribution = "BoxDistribution"
    #: Show the quantiles of the distribution as a box, with the outlier values.
    BoxOutliersDistribution = "BoxOutliersDistribution"
    #: Show both a curve and a box.
    CurveBoxDistribution = "CurveBoxDistribution"
    #: Show both a violin and a box.
    ViolinBoxDistribution = "ViolinBoxDistribution"
    #: Show the distribution as a histogram.
    HistogramDistribution = "HistogramDistribution"
    #: Show the cumulative distribution.
    CumulativeDistribution = "CumulativeDistribution"


register_jl_type("DistributionStyle", DistributionStyle)


class DistributionConfiguration(Validated):
    """
    Configure how to show a distribution. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionConfiguration>`__
    for details.
    """

    #: Whether the values are shown in the vertical or the horizontal axis.
    values_orientation: ValuesOrientation
    #: The style used to show the distribution.
    style: DistributionStyle
    #: How to show the outline of the distribution.
    line: LineConfiguration
    #: Normalize the density (or the histogram counts).
    normalize: bool
    #: Show the cumulative distribution in descending order.
    cumulative_descending: bool

    def __init__(
        self,
        *,
        values_orientation: Union[ValuesOrientation, DefaultValue] = DEFAULT,
        style: Union[DistributionStyle, DefaultValue] = DEFAULT,
        line: Union[LineConfiguration, DefaultValue] = DEFAULT,
        normalize: Union[bool, DefaultValue] = DEFAULT,
        cumulative_descending: Union[bool, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.DistributionConfiguration(
                **_given(
                    values_orientation=values_orientation,
                    style=style,
                    line=line,
                    normalize=normalize,
                    cumulative_descending=cumulative_descending,
                )
            )
        )


register_jl_type("DistributionConfiguration", DistributionConfiguration)


class DistributionGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing a single distribution. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionGraphConfiguration>`__
    for details.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: How to show the distribution.
    distribution: DistributionConfiguration
    #: The axis showing the values.
    value_axis: AxisConfiguration
    #: Bands partitioning the graph by the value axis.
    value_bands: BandsConfiguration
    #: The axis showing the density.
    density_axis: AxisConfiguration
    #: Bands partitioning the graph by the cumulative axis.
    cumulative_bands: BandsConfiguration

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        distribution: Union[DistributionConfiguration, DefaultValue] = DEFAULT,
        value_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        value_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        density_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        cumulative_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.DistributionGraphConfiguration(
                **_given(
                    figure=figure,
                    distribution=distribution,
                    value_axis=value_axis,
                    value_bands=value_bands,
                    density_axis=density_axis,
                    cumulative_bands=cumulative_bands,
                )
            )
        )


register_jl_type("DistributionGraphConfiguration", DistributionGraphConfiguration)


class DistributionData(JlObject):
    """
    One distribution of a :py:obj:`DistributionGraphData` or a :py:obj:`DistributionsGraphData`. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionData>`__
    for details.
    """

    #: The values whose distribution is shown; their title is the value axis title.
    values: ValuesData
    #: The hovers and mask of the values.
    points: EntitiesData
    #: The name of the distribution.
    name: Optional[str]
    #: Prefixed to the hover of each value.
    hover: Optional[str]
    #: Whether to show the distribution at all (in a graph of multiple distributions).
    is_shown: bool
    #: The color of the distribution.
    color: Optional[str]

    def __init__(
        self,
        *,
        values: Union[ValuesData, DefaultValue] = DEFAULT,
        points: Union[EntitiesData, DefaultValue] = DEFAULT,
        name: Union[Optional[str], DefaultValue] = DEFAULT,
        hover: Union[Optional[str], DefaultValue] = DEFAULT,
        is_shown: Union[bool, DefaultValue] = DEFAULT,
        color: Union[Optional[str], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.DistributionData(
                **_given(values=values, points=points, name=name, hover=hover, is_shown=is_shown, color=color)
            )
        )


register_jl_type("DistributionData", DistributionData)


class DistributionGraphData(AbstractGraphData):
    """
    The data of a graph showing a single distribution. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The distribution to show.
    distribution: DistributionData
    #: Override the offsets of the value bands.
    value_bands: BandsData
    #: Override the offsets of the cumulative bands.
    cumulative_bands: BandsData

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        distribution: Union[DistributionData, DefaultValue] = DEFAULT,
        value_bands: Union[BandsData, DefaultValue] = DEFAULT,
        cumulative_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.DistributionGraphData(
                **_given(
                    figure_title=figure_title,
                    distribution=distribution,
                    value_bands=value_bands,
                    cumulative_bands=cumulative_bands,
                )
            )
        )


register_jl_type("DistributionGraphData", DistributionGraphData)


class DistributionGraph(Graph):
    """
    A graph visualizing a single distribution. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionGraph>`__
    for details.
    """

    #: What to display.
    data: DistributionGraphData
    #: How to display it.
    configuration: DistributionGraphConfiguration

    def __init__(
        self,
        *,
        data: Union[DistributionGraphData, DefaultValue] = DEFAULT,
        configuration: Union[DistributionGraphConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.DistributionGraph(**_given(data=data, configuration=configuration)))

    def distribution_values_fields(self) -> AxisFields:
        """
        The data source view of the values of the distribution, along the ``value_axis``.
        """
        return _from_julia(jl.SomeGraphs.distribution_values_fields(self.jl_obj))


def distribution_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    distribution: Union[DistributionData, DefaultValue] = DEFAULT,
    value_bands: Union[BandsData, DefaultValue] = DEFAULT,
    cumulative_bands: Union[BandsData, DefaultValue] = DEFAULT,
    configuration: Union[DistributionGraphConfiguration, DefaultValue] = DEFAULT,
) -> DistributionGraph:
    """
    Create a :py:obj:`DistributionGraph` by specifying only the :py:obj:`DistributionGraphData` fields (with an
    optional :py:obj:`DistributionGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.distribution_graph>`__
    for details.
    """
    return DistributionGraph(
        data=DistributionGraphData(
            figure_title=figure_title,
            distribution=distribution,
            value_bands=value_bands,
            cumulative_bands=cumulative_bands,
        ),
        configuration=configuration,
    )


class DistributionsGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing multiple distributions. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionsGraphConfiguration>`__
    for details.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: How to show each distribution.
    distribution: DistributionConfiguration
    #: The axis showing the values.
    value_axis: AxisConfiguration
    #: Bands partitioning the graph by the value axis.
    value_bands: BandsConfiguration
    #: The axis showing the density.
    density_axis: AxisConfiguration
    #: The axis listing the distributions.
    series_axis: AxisConfiguration
    #: The gap between the distributions, as a fraction of their size.
    distributions_gap: Optional[float]

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        distribution: Union[DistributionConfiguration, DefaultValue] = DEFAULT,
        value_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        value_bands: Union[BandsConfiguration, DefaultValue] = DEFAULT,
        density_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        series_axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        distributions_gap: Union[Optional[float], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.DistributionsGraphConfiguration(
                **_given(
                    figure=figure,
                    distribution=distribution,
                    value_axis=value_axis,
                    value_bands=value_bands,
                    density_axis=density_axis,
                    series_axis=series_axis,
                    distributions_gap=distributions_gap,
                )
            )
        )


register_jl_type("DistributionsGraphConfiguration", DistributionsGraphConfiguration)


class DistributionsGraphData(AbstractGraphData):
    """
    The data of a graph showing multiple distributions. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionsGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The distributions to show.
    distributions: Sequence[DistributionData]
    #: The (1-based) order to show the distributions in.
    order: Optional[IntegersVector]
    #: The title of the axis showing the density.
    density_axis_title: Optional[str]
    #: The title of the axis listing the distributions.
    series_axis_title: Optional[str]
    #: Override the offsets of the value bands.
    value_bands: BandsData

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        distributions: Union[Sequence[DistributionData], DefaultValue] = DEFAULT,
        order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
        density_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        series_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        value_bands: Union[BandsData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.DistributionsGraphData(
                **_given(
                    figure_title=figure_title,
                    distributions=distributions,
                    order=order,
                    density_axis_title=density_axis_title,
                    series_axis_title=series_axis_title,
                    value_bands=value_bands,
                )
            )
        )


register_jl_type("DistributionsGraphData", DistributionsGraphData)


class DistributionsGraph(Graph):
    """
    A graph visualizing multiple distributions. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.DistributionsGraph>`__
    for details.
    """

    #: What to display.
    data: DistributionsGraphData
    #: How to display it.
    configuration: DistributionsGraphConfiguration

    def __init__(
        self,
        *,
        data: Union[DistributionsGraphData, DefaultValue] = DEFAULT,
        configuration: Union[DistributionsGraphConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.DistributionsGraph(**_given(data=data, configuration=configuration)))

    def distributions_values_fields(self, index: int) -> AxisFields:
        """
        The data source view of the values of the (1-based) ``index`` distribution, along the (shared) ``value_axis``.
        """
        return _from_julia(jl.SomeGraphs.distributions_values_fields(self.jl_obj, index))


def distributions_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    distributions: Union[Sequence[DistributionData], DefaultValue] = DEFAULT,
    order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
    density_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    series_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    value_bands: Union[BandsData, DefaultValue] = DEFAULT,
    configuration: Union[DistributionsGraphConfiguration, DefaultValue] = DEFAULT,
) -> DistributionsGraph:
    """
    Create a :py:obj:`DistributionsGraph` by specifying only the :py:obj:`DistributionsGraphData` fields (with an
    optional :py:obj:`DistributionsGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/distributions.html#SomeGraphs.Distributions.distributions_graph>`__
    for details.
    """
    return DistributionsGraph(
        data=DistributionsGraphData(
            figure_title=figure_title,
            distributions=distributions,
            order=order,
            density_axis_title=density_axis_title,
            series_axis_title=series_axis_title,
            value_bands=value_bands,
        ),
        configuration=configuration,
    )
