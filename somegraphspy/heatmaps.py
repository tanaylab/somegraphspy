"""
Graphs showing a matrix of values as a heatmap. See the Julia
`documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html>`__ for details.
"""

# The enum values are named exactly as they are in Julia, so they are not UPPER_CASE.
# pylint: disable=invalid-name

from typing import Any
from typing import Optional
from typing import Sequence
from typing import Union

from .common import AbstractGraphConfiguration
from .common import AbstractGraphData
from .common import AnnotationData
from .common import AnnotationSize
from .common import ColorsConfiguration
from .common import FigureConfiguration
from .common import Graph
from .common import IntegersVector
from .common import LineConfiguration
from .common import NumbersMatrix
from .common import StringsMatrix
from .common import StringsVector
from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import JlEnum
from .julia_import import JlObject
from .julia_import import _from_julia
from .julia_import import _given
from .julia_import import jl
from .julia_import import register_jl_type

__all__ = [
    "HeatmapGraph",
    "HeatmapGraphConfiguration",
    "HeatmapGraphData",
    "HeatmapGraphOrder",
    "HeatmapLinkage",
    "HeatmapOrigin",
    "HeatmapReorder",
    "Order",
    "heatmap_graph",
]

#: An explicit order of the rows or columns. This is either a vector of (1-based) indices, or an opaque ``Hclust``
#: clustering taken from the :py:obj:`HeatmapGraphOrder` of a previously generated graph.
Order = Union[IntegersVector, Any]


class HeatmapReorder(JlEnum):
    """
    How to reorder the rows or columns of a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapReorder>`__
    for details.
    """

    #: Cluster the data the same way R does.
    RCompatibleHclust = "RCompatibleHclust"
    #: Cluster the data using an optimal ordering of the tree.
    OptimalHclust = "OptimalHclust"
    #: Cluster the data and reorder the tree.
    ReorderHclust = "ReorderHclust"
    #: Cluster the data and slant the tree.
    SlantedHclust = "SlantedHclust"
    #: Cluster the pre-squared data and slant the tree.
    SlantedPreSquaredHclust = "SlantedPreSquaredHclust"
    #: Slant the data without computing a clustering tree.
    SlantedOrder = "SlantedOrder"
    #: Slant the pre-squared data without computing a clustering tree.
    SlantedPreSquaredOrder = "SlantedPreSquaredOrder"
    #: Use the same order as the other dimension.
    SameOrder = "SameOrder"


register_jl_type("HeatmapReorder", HeatmapReorder)


class HeatmapLinkage(JlEnum):
    """
    The linkage used when clustering the rows or columns of a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapLinkage>`__
    for details.
    """

    #: Use the minimal distance between the clusters.
    SingleLinkage = "SingleLinkage"
    #: Use the average distance between the clusters.
    AverageLinkage = "AverageLinkage"
    #: Use the maximal distance between the clusters.
    CompleteLinkage = "CompleteLinkage"
    #: Use Ward's minimal variance.
    WardLinkage = "WardLinkage"
    #: Use Ward's minimal variance on the pre-squared data.
    WardPreSquaredLinkage = "WardPreSquaredLinkage"


register_jl_type("HeatmapLinkage", HeatmapLinkage)


class HeatmapOrigin(JlEnum):
    """
    Where the first entry of the heatmap matrix is shown. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapOrigin>`__
    for details.
    """

    #: Show the first entry at the top left.
    HeatmapTopLeft = "HeatmapTopLeft"
    #: Show the first entry at the top right.
    HeatmapTopRight = "HeatmapTopRight"
    #: Show the first entry at the bottom left.
    HeatmapBottomLeft = "HeatmapBottomLeft"
    #: Show the first entry at the bottom right.
    HeatmapBottomRight = "HeatmapBottomRight"


register_jl_type("HeatmapOrigin", HeatmapOrigin)


class HeatmapGraphOrder(JlObject):
    """
    The final order and clustering of the rows and the columns of a heatmap graph, as returned by the graph's
    ``order``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapGraphOrder>`__
    for details.

    The orders are always a permutation of the entries, so they can be fed as-is into the ``rows_order`` and
    ``columns_order`` of a :py:obj:`HeatmapGraphData` to show another graph in the same order.

    The ``rows_hclust`` and ``columns_hclust`` are Julia ``Hclust`` objects. There is no Python model for these, but
    they too can be fed back into the ``rows_order`` and ``columns_order`` of a :py:obj:`HeatmapGraphData`, which
    reuses both the order and the tree, so the other graph also shows the same dendogram.

    These describe the order of the data, not the order it is displayed in; applying the ``origin`` is up to whoever
    shows the graph.
    """

    #: The final (1-based) order of the rows; the identity if they weren't reordered at all.
    rows_order: IntegersVector
    #: The clustering of the rows, if one was computed.
    rows_hclust: Optional[Any]
    #: The final (1-based) order of the columns; the identity if they weren't reordered at all.
    columns_order: IntegersVector
    #: The clustering of the columns, if one was computed.
    columns_hclust: Optional[Any]


register_jl_type("HeatmapGraphOrder", HeatmapGraphOrder)


class HeatmapGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing a matrix of values as a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapGraphConfiguration>`__
    for details.

    Groups (and subgroups) constrain the clustering, and are separated by a gap. Each level is placed independently: a
    level specified by numbers is laid out in the order of these numbers, and a level specified by names is laid out by
    the clustering. The ``..._subgroups_gap`` defaults to ``None`` because the usual reason to specify subgroups is to
    constrain the clustering rather than to show gaps.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: The title of the horizontal axis.
    x_axis_title: Optional[str]
    #: The title of the vertical axis.
    y_axis_title: Optional[str]
    #: How to color the entries.
    entries_colors: ColorsConfiguration
    #: The size of the annotations shown next to the rows.
    rows_annotations: AnnotationSize
    #: The size of the annotations shown next to the columns.
    columns_annotations: AnnotationSize
    #: How to reorder the rows.
    rows_reorder: Optional[HeatmapReorder]
    #: How to reorder the columns.
    columns_reorder: Optional[HeatmapReorder]
    #: The linkage used when clustering the rows.
    rows_linkage: Optional[HeatmapLinkage]
    #: The linkage used when clustering the columns.
    columns_linkage: Optional[HeatmapLinkage]
    #: The distance metric used when clustering the rows, a Julia ``Distances.PreMetric``.
    rows_metric: Optional[Any]
    #: The distance metric used when clustering the columns, a Julia ``Distances.PreMetric``.
    columns_metric: Optional[Any]
    #: The gap between groups of rows, in entries.
    rows_groups_gap: Optional[int]
    #: The gap between groups of columns, in entries.
    columns_groups_gap: Optional[int]
    #: The gap between subgroups of rows, in entries.
    rows_subgroups_gap: Optional[int]
    #: The gap between subgroups of columns, in entries.
    columns_subgroups_gap: Optional[int]
    #: The size of the rows dendogram, as a fraction of the graph size.
    rows_dendogram_size: Optional[float]
    #: The size of the columns dendogram, as a fraction of the graph size.
    columns_dendogram_size: Optional[float]
    #: How to draw the rows dendogram.
    rows_dendogram_line: LineConfiguration
    #: How to draw the columns dendogram.
    columns_dendogram_line: LineConfiguration
    #: Where the first entry of the matrix is shown.
    origin: HeatmapOrigin
    #: Caches the computed order of the rows and the columns; access it through the graph's ``order``, and reset it
    #: with the graph's ``reset_order`` if anything it was computed from is changed after it was computed.
    final_order: Optional[HeatmapGraphOrder]

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        entries_colors: Union[ColorsConfiguration, DefaultValue] = DEFAULT,
        rows_annotations: Union[AnnotationSize, DefaultValue] = DEFAULT,
        columns_annotations: Union[AnnotationSize, DefaultValue] = DEFAULT,
        rows_reorder: Union[Optional[HeatmapReorder], DefaultValue] = DEFAULT,
        columns_reorder: Union[Optional[HeatmapReorder], DefaultValue] = DEFAULT,
        rows_linkage: Union[Optional[HeatmapLinkage], DefaultValue] = DEFAULT,
        columns_linkage: Union[Optional[HeatmapLinkage], DefaultValue] = DEFAULT,
        rows_metric: Union[Optional[Any], DefaultValue] = DEFAULT,
        columns_metric: Union[Optional[Any], DefaultValue] = DEFAULT,
        rows_groups_gap: Union[Optional[int], DefaultValue] = DEFAULT,
        columns_groups_gap: Union[Optional[int], DefaultValue] = DEFAULT,
        rows_subgroups_gap: Union[Optional[int], DefaultValue] = DEFAULT,
        columns_subgroups_gap: Union[Optional[int], DefaultValue] = DEFAULT,
        rows_dendogram_size: Union[Optional[float], DefaultValue] = DEFAULT,
        columns_dendogram_size: Union[Optional[float], DefaultValue] = DEFAULT,
        rows_dendogram_line: Union[LineConfiguration, DefaultValue] = DEFAULT,
        columns_dendogram_line: Union[LineConfiguration, DefaultValue] = DEFAULT,
        origin: Union[HeatmapOrigin, DefaultValue] = DEFAULT,
        final_order: Union[Optional[HeatmapGraphOrder], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapGraphConfiguration(
                **_given(
                    figure=figure,
                    x_axis_title=x_axis_title,
                    y_axis_title=y_axis_title,
                    entries_colors=entries_colors,
                    rows_annotations=rows_annotations,
                    columns_annotations=columns_annotations,
                    rows_reorder=rows_reorder,
                    columns_reorder=columns_reorder,
                    rows_linkage=rows_linkage,
                    columns_linkage=columns_linkage,
                    rows_metric=rows_metric,
                    columns_metric=columns_metric,
                    rows_groups_gap=rows_groups_gap,
                    columns_groups_gap=columns_groups_gap,
                    rows_subgroups_gap=rows_subgroups_gap,
                    columns_subgroups_gap=columns_subgroups_gap,
                    rows_dendogram_size=rows_dendogram_size,
                    columns_dendogram_size=columns_dendogram_size,
                    rows_dendogram_line=rows_dendogram_line,
                    columns_dendogram_line=columns_dendogram_line,
                    origin=origin,
                    final_order=final_order,
                )
            )
        )


register_jl_type("HeatmapGraphConfiguration", HeatmapGraphConfiguration)


class HeatmapGraphData(AbstractGraphData):
    """
    The data of a graph showing a matrix of values as a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The title of the horizontal axis.
    x_axis_title: Optional[str]
    #: The title of the vertical axis.
    y_axis_title: Optional[str]
    #: The title of the entries colors legend.
    entries_colors_title: Optional[str]
    #: The value of each entry, a row per row and a column per column.
    entries_values: Optional[NumbersMatrix]
    #: The name of each row.
    rows_names: Optional[StringsVector]
    #: The name of each column.
    columns_names: Optional[StringsVector]
    #: The hover text of each entry.
    entries_hovers: Optional[StringsMatrix]
    #: The hover text of each row.
    rows_hovers: Optional[StringsVector]
    #: The hover text of each column.
    columns_hovers: Optional[StringsVector]
    #: Annotations shown next to the rows.
    rows_annotations: Sequence[AnnotationData]
    #: Annotations shown next to the columns.
    columns_annotations: Sequence[AnnotationData]
    #: The features to cluster the rows by, instead of the entries values.
    rows_arrange_by: Optional[NumbersMatrix]
    #: The features to cluster the columns by, instead of the entries values.
    columns_arrange_by: Optional[NumbersMatrix]
    #: Force this order of the rows.
    rows_order: Optional[Order]
    #: Force this order of the columns.
    columns_order: Optional[Order]
    #: The group of each row.
    rows_groups: Optional[Union[StringsVector, IntegersVector]]
    #: The group of each column.
    columns_groups: Optional[Union[StringsVector, IntegersVector]]
    #: The subgroup of each row, nested in its group. A subgroup of one group is unrelated to the same subgroup of
    #: another group, so the subgroups need not be unique.
    rows_subgroups: Optional[Union[StringsVector, IntegersVector]]
    #: The subgroup of each column, nested in its group. A subgroup of one group is unrelated to the same subgroup of
    #: another group, so the subgroups need not be unique.
    columns_subgroups: Optional[Union[StringsVector, IntegersVector]]

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
        entries_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
        entries_values: Union[Optional[NumbersMatrix], DefaultValue] = DEFAULT,
        rows_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        columns_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        entries_hovers: Union[Optional[StringsMatrix], DefaultValue] = DEFAULT,
        rows_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        columns_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        rows_annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
        columns_annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
        rows_arrange_by: Union[Optional[NumbersMatrix], DefaultValue] = DEFAULT,
        columns_arrange_by: Union[Optional[NumbersMatrix], DefaultValue] = DEFAULT,
        rows_order: Union[Optional[Order], DefaultValue] = DEFAULT,
        columns_order: Union[Optional[Order], DefaultValue] = DEFAULT,
        rows_groups: Union[Optional[Union[StringsVector, IntegersVector]], DefaultValue] = DEFAULT,
        columns_groups: Union[Optional[Union[StringsVector, IntegersVector]], DefaultValue] = DEFAULT,
        rows_subgroups: Union[Optional[Union[StringsVector, IntegersVector]], DefaultValue] = DEFAULT,
        columns_subgroups: Union[Optional[Union[StringsVector, IntegersVector]], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapGraphData(
                **_given(
                    figure_title=figure_title,
                    x_axis_title=x_axis_title,
                    y_axis_title=y_axis_title,
                    entries_colors_title=entries_colors_title,
                    entries_values=entries_values,
                    rows_names=rows_names,
                    columns_names=columns_names,
                    entries_hovers=entries_hovers,
                    rows_hovers=rows_hovers,
                    columns_hovers=columns_hovers,
                    rows_annotations=rows_annotations,
                    columns_annotations=columns_annotations,
                    rows_arrange_by=rows_arrange_by,
                    columns_arrange_by=columns_arrange_by,
                    rows_order=rows_order,
                    columns_order=columns_order,
                    rows_groups=rows_groups,
                    columns_groups=columns_groups,
                    rows_subgroups=rows_subgroups,
                    columns_subgroups=columns_subgroups,
                )
            )
        )


register_jl_type("HeatmapGraphData", HeatmapGraphData)


class HeatmapGraph(Graph):
    """
    A graph visualizing a matrix of values as a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapGraph>`__
    for details.
    """

    #: What to display.
    data: HeatmapGraphData
    #: How to display it.
    configuration: HeatmapGraphConfiguration

    def __init__(
        self,
        *,
        data: Union[HeatmapGraphData, DefaultValue] = DEFAULT,
        configuration: Union[HeatmapGraphConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.HeatmapGraph(**_given(data=data, configuration=configuration)))

    @property
    def order(self) -> HeatmapGraphOrder:
        """
        The final order of the rows and the columns, and the trees they were clustered by, without rendering the graph.
        See the Julia
        `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.heatmap_order>`__
        for details.

        Use this to list the entries in the order they are shown, or to show several graphs in the same order by
        feeding it into the ``rows_order`` and ``columns_order`` of their data. The order is only computed
        once; showing the graph will reuse it, and vice versa.

        .. note::

            Nothing detects that the cached order went stale. Call :py:obj:`reset_order` if anything it was computed
            from is changed after it was computed - that is, the ``..._reorder``, ``..._linkage`` and ``..._metric``
            configuration, and the ``entries_values``, ``..._order``, ``..._arrange_by`` and ``..._groups`` data. The
            groups are easy to forget: they constrain the clustering, so saving the same graph twice, grouped
            differently each time, silently reuses the order of the first grouping unless the cache is reset in
            between.
        """
        return _from_julia(jl.SomeGraphs.heatmap_order(self.jl_obj))

    def reset_order(self) -> None:
        """
        Forget the cached :py:obj:`HeatmapGraphOrder`, so that asking for the graph's :py:obj:`order` (or showing it)
        will compute it again. Call this after changing anything the order was computed from. See the Julia
        `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.reset_order!>`__
        for details.
        """
        jl.SomeGraphs.reset_order_b(self.jl_obj)


def heatmap_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    x_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    y_axis_title: Union[Optional[str], DefaultValue] = DEFAULT,
    entries_colors_title: Union[Optional[str], DefaultValue] = DEFAULT,
    entries_values: Union[Optional[NumbersMatrix], DefaultValue] = DEFAULT,
    rows_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    columns_names: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    entries_hovers: Union[Optional[StringsMatrix], DefaultValue] = DEFAULT,
    rows_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    columns_hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
    rows_annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
    columns_annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
    rows_arrange_by: Union[Optional[NumbersMatrix], DefaultValue] = DEFAULT,
    columns_arrange_by: Union[Optional[NumbersMatrix], DefaultValue] = DEFAULT,
    rows_order: Union[Optional[Order], DefaultValue] = DEFAULT,
    columns_order: Union[Optional[Order], DefaultValue] = DEFAULT,
    rows_groups: Union[Optional[Union[StringsVector, IntegersVector]], DefaultValue] = DEFAULT,
    columns_groups: Union[Optional[Union[StringsVector, IntegersVector]], DefaultValue] = DEFAULT,
    rows_subgroups: Union[Optional[Union[StringsVector, IntegersVector]], DefaultValue] = DEFAULT,
    columns_subgroups: Union[Optional[Union[StringsVector, IntegersVector]], DefaultValue] = DEFAULT,
    configuration: Union[HeatmapGraphConfiguration, DefaultValue] = DEFAULT,
) -> HeatmapGraph:
    """
    Create a :py:obj:`HeatmapGraph` by specifying only the :py:obj:`HeatmapGraphData` fields (with an optional
    :py:obj:`HeatmapGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.heatmap_graph>`__
    for details.
    """
    return HeatmapGraph(
        data=HeatmapGraphData(
            figure_title=figure_title,
            x_axis_title=x_axis_title,
            y_axis_title=y_axis_title,
            entries_colors_title=entries_colors_title,
            entries_values=entries_values,
            rows_names=rows_names,
            columns_names=columns_names,
            entries_hovers=entries_hovers,
            rows_hovers=rows_hovers,
            columns_hovers=columns_hovers,
            rows_annotations=rows_annotations,
            columns_annotations=columns_annotations,
            rows_arrange_by=rows_arrange_by,
            columns_arrange_by=columns_arrange_by,
            rows_order=rows_order,
            columns_order=columns_order,
            rows_groups=rows_groups,
            columns_groups=columns_groups,
            rows_subgroups=rows_subgroups,
            columns_subgroups=columns_subgroups,
        ),
        configuration=configuration,
    )
