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
from .common import EntitiesData
from .common import FigureConfiguration
from .common import Graph
from .common import IntegersVector
from .common import LineConfiguration
from .common import MatrixData
from .common import MatrixEntitiesData
from .common import NumbersMatrix
from .common import Validated
from .common import ValuesData
from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import JlEnum
from .julia_import import JlObject
from .julia_import import _from_julia
from .julia_import import _given
from .julia_import import _optional_jl_obj
from .julia_import import jl
from .julia_import import register_jl_type
from .sources import ColorsFields
from .sources import MatrixFields
from .sources import VectorDataFields

__all__ = [
    "EntriesConfiguration",
    "HeatmapAxisConfiguration",
    "HeatmapAxisData",
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

    The orders are always a permutation of all the entries (hidden ones included), so they can be fed as-is into the
    ``order`` of the ``rows`` and ``columns`` of a :py:obj:`HeatmapGraphData` to show another graph in the same order.

    The ``rows_hclust`` and ``columns_hclust`` are Julia ``Hclust`` objects. There is no Python model for these, but
    they too can be fed back into the ``order`` of the ``rows`` and ``columns`` of a :py:obj:`HeatmapGraphData`, which
    reuses both the order and the tree, so the other graph also shows the same dendogram.

    These describe the order of the data, not the order it is displayed in; applying the ``origin`` and skipping the
    hidden entries is up to whoever shows the graph.
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


class EntriesConfiguration(Validated):
    """
    Configure the entries of a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.EntriesConfiguration>`__
    for details.
    """

    #: How to color the entries (only continuous palettes are supported).
    colors: ColorsConfiguration

    def __init__(self, *, colors: Union[ColorsConfiguration, DefaultValue] = DEFAULT) -> None:
        super().__init__(jl.SomeGraphs.EntriesConfiguration(**_given(colors=colors)))


register_jl_type("EntriesConfiguration", EntriesConfiguration)


class HeatmapAxisConfiguration(Validated):
    """
    Configure one axis (the rows or the columns) of a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapAxisConfiguration>`__
    for details.

    Groups (and subgroups) constrain the clustering, and are separated by a gap. Each level is placed independently: a
    level specified by numbers is laid out in the order of these numbers, and a level specified by names is laid out by
    the clustering. The ``subgroups_gap`` defaults to ``None`` because the usual reason to specify subgroups is to
    constrain the clustering rather than to show gaps.
    """

    #: The title of the axis.
    title: Optional[str]
    #: The size of the annotations shown next to the axis.
    annotations: AnnotationSize
    #: How to reorder the entries.
    reorder: Optional[HeatmapReorder]
    #: The linkage used when clustering the entries.
    linkage: Optional[HeatmapLinkage]
    #: The distance metric used when clustering the entries, a Julia ``Distances.PreMetric``.
    metric: Optional[Any]
    #: Whether entries hidden by the mask take part in a computed clustering.
    include_hidden: bool
    #: The gap between groups of entries, in entries.
    groups_gap: Optional[int]
    #: The gap between subgroups of entries, in entries.
    subgroups_gap: Optional[int]
    #: The size of the dendogram, as a fraction of the graph size.
    dendogram_size: Optional[float]
    #: How to draw the dendogram.
    dendogram_line: LineConfiguration

    def __init__(
        self,
        *,
        title: Union[Optional[str], DefaultValue] = DEFAULT,
        annotations: Union[AnnotationSize, DefaultValue] = DEFAULT,
        reorder: Union[Optional[HeatmapReorder], DefaultValue] = DEFAULT,
        linkage: Union[Optional[HeatmapLinkage], DefaultValue] = DEFAULT,
        metric: Union[Optional[Any], DefaultValue] = DEFAULT,
        include_hidden: Union[bool, DefaultValue] = DEFAULT,
        groups_gap: Union[Optional[int], DefaultValue] = DEFAULT,
        subgroups_gap: Union[Optional[int], DefaultValue] = DEFAULT,
        dendogram_size: Union[Optional[float], DefaultValue] = DEFAULT,
        dendogram_line: Union[LineConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapAxisConfiguration(
                **_given(
                    title=title,
                    annotations=annotations,
                    reorder=reorder,
                    linkage=linkage,
                    metric=metric,
                    include_hidden=include_hidden,
                    groups_gap=groups_gap,
                    subgroups_gap=subgroups_gap,
                    dendogram_size=dendogram_size,
                    dendogram_line=dendogram_line,
                )
            )
        )


register_jl_type("HeatmapAxisConfiguration", HeatmapAxisConfiguration)


class HeatmapGraphConfiguration(AbstractGraphConfiguration):
    """
    Configure a graph showing a matrix of values as a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapGraphConfiguration>`__
    for details.
    """

    #: How to size the overall figure.
    figure: FigureConfiguration
    #: How to show the entries.
    entries: EntriesConfiguration
    #: How to show the rows.
    rows: HeatmapAxisConfiguration
    #: How to show the columns.
    columns: HeatmapAxisConfiguration
    #: Where the first entry of the matrix is shown.
    origin: HeatmapOrigin
    #: Caches the computed order of the rows and the columns; access it through the graph's ``order``, and reset it
    #: with the graph's ``reset_order`` if anything it was computed from is changed after it was computed.
    final_order: Optional[HeatmapGraphOrder]

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        entries: Union[EntriesConfiguration, DefaultValue] = DEFAULT,
        rows: Union[HeatmapAxisConfiguration, DefaultValue] = DEFAULT,
        columns: Union[HeatmapAxisConfiguration, DefaultValue] = DEFAULT,
        origin: Union[HeatmapOrigin, DefaultValue] = DEFAULT,
        final_order: Union[Optional[HeatmapGraphOrder], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapGraphConfiguration(
                **_given(
                    figure=figure, entries=entries, rows=rows, columns=columns, origin=origin, final_order=final_order
                )
            )
        )


register_jl_type("HeatmapGraphConfiguration", HeatmapGraphConfiguration)


class HeatmapAxisData(JlObject):
    """
    The data of one axis (the rows or the columns) of a :py:obj:`HeatmapGraphData`. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapAxisData>`__
    for details.
    """

    #: The name of each entry, shown as the tick labels; their title is the axis title.
    names: ValuesData
    #: The hovers and mask of the entries.
    entities: EntitiesData
    #: Force this order of the entries.
    order: Optional[Order]
    #: The group of each entry, either numbers or names. The groups have no title.
    groups: ValuesData
    #: The subgroup of each entry, nested in its group. A subgroup of one group is unrelated to the same subgroup of
    #: another group, so the subgroups need not be unique. The subgroups have no title.
    subgroups: ValuesData
    #: The features to cluster the entries by, instead of the entries values.
    arrange_by: Optional[NumbersMatrix]
    #: Annotations shown next to the axis.
    annotations: Sequence[AnnotationData]

    def __init__(
        self,
        *,
        names: Union[ValuesData, DefaultValue] = DEFAULT,
        entities: Union[EntitiesData, DefaultValue] = DEFAULT,
        order: Union[Optional[Order], DefaultValue] = DEFAULT,
        groups: Union[ValuesData, DefaultValue] = DEFAULT,
        subgroups: Union[ValuesData, DefaultValue] = DEFAULT,
        arrange_by: Union[Optional[NumbersMatrix], DefaultValue] = DEFAULT,
        annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapAxisData(
                **_given(
                    names=names,
                    entities=entities,
                    order=order,
                    groups=groups,
                    subgroups=subgroups,
                    arrange_by=arrange_by,
                    annotations=annotations,
                )
            )
        )


register_jl_type("HeatmapAxisData", HeatmapAxisData)


class HeatmapGraphData(AbstractGraphData):
    """
    The data of a graph showing a matrix of values as a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The value of each entry, a row per row and a column per column; their title is the colors legend title.
    entries: MatrixData
    #: The hovers and mask of the entries.
    cells: MatrixEntitiesData
    #: The data of the rows.
    rows: HeatmapAxisData
    #: The data of the columns.
    columns: HeatmapAxisData

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        entries: Union[MatrixData, DefaultValue] = DEFAULT,
        cells: Union[MatrixEntitiesData, DefaultValue] = DEFAULT,
        rows: Union[HeatmapAxisData, DefaultValue] = DEFAULT,
        columns: Union[HeatmapAxisData, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapGraphData(
                **_given(figure_title=figure_title, entries=entries, cells=cells, rows=rows, columns=columns)
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
        feeding it into the ``order`` of the ``rows`` and ``columns`` of their data. The order is only computed once.
        Showing the graph will reuse it, and vice versa.

        .. note::

            Nothing detects that the cached order went stale. Call :py:obj:`reset_order` if anything it was computed
            from is changed after it was computed - that is, the ``reorder``, ``linkage``, ``metric`` and
            ``include_hidden`` of the axes configuration, and the ``entries.values`` and the ``order``, ``arrange_by``,
            ``groups`` and ``subgroups`` of the axes data. The groups are easy to forget: they constrain the clustering,
            so saving the same graph twice, grouped differently each time, silently reuses the order of the first
            grouping unless the cache is reset in between.
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

    def entries_fields(self) -> MatrixFields:
        """
        The data source view of the entries of the heatmap, colored by the ``entries.colors``.
        """
        return _from_julia(jl.SomeGraphs.entries_fields(self.jl_obj))

    def rows_names_fields(self) -> VectorDataFields:
        """
        The data source view of the names of the rows; their title is the title of the rows axis.
        """
        return _from_julia(jl.SomeGraphs.rows_names_fields(self.jl_obj))

    def columns_names_fields(self) -> VectorDataFields:
        """
        The data source view of the names of the columns; their title is the title of the columns axis.
        """
        return _from_julia(jl.SomeGraphs.columns_names_fields(self.jl_obj))

    def rows_groups_fields(self) -> VectorDataFields:
        """
        The data source view of the groups of the rows.
        """
        return _from_julia(jl.SomeGraphs.rows_groups_fields(self.jl_obj))

    def rows_subgroups_fields(self) -> VectorDataFields:
        """
        The data source view of the subgroups of the rows.
        """
        return _from_julia(jl.SomeGraphs.rows_subgroups_fields(self.jl_obj))

    def columns_groups_fields(self) -> VectorDataFields:
        """
        The data source view of the groups of the columns.
        """
        return _from_julia(jl.SomeGraphs.columns_groups_fields(self.jl_obj))

    def columns_subgroups_fields(self) -> VectorDataFields:
        """
        The data source view of the subgroups of the columns.
        """
        return _from_julia(jl.SomeGraphs.columns_subgroups_fields(self.jl_obj))

    def rows_annotations_fields(self, index: int) -> ColorsFields:
        """
        The data source view of the (1-based) ``index`` annotation of the rows, which shares the entities of the rows.
        """
        return _from_julia(jl.SomeGraphs.rows_annotations_fields(self.jl_obj, index))

    def columns_annotations_fields(self, index: int) -> ColorsFields:
        """
        The data source view of the (1-based) ``index`` annotation of the columns, which shares the entities of the
        columns.
        """
        return _from_julia(jl.SomeGraphs.columns_annotations_fields(self.jl_obj, index))

    def add_rows_annotation(self, annotation: Optional[AnnotationData] = None) -> int:
        """
        Append an ``annotation`` of the rows (by default, an empty one) and return its (1-based) index, for
        :py:obj:`rows_annotations_fields`.
        """
        return int(jl.SomeGraphs.add_rows_annotation_b(self.jl_obj, *_optional_jl_obj(annotation)))

    def add_columns_annotation(self, annotation: Optional[AnnotationData] = None) -> int:
        """
        Append an ``annotation`` of the columns (by default, an empty one) and return its (1-based) index, for
        :py:obj:`columns_annotations_fields`.
        """
        return int(jl.SomeGraphs.add_columns_annotation_b(self.jl_obj, *_optional_jl_obj(annotation)))


def heatmap_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    entries: Union[MatrixData, DefaultValue] = DEFAULT,
    cells: Union[MatrixEntitiesData, DefaultValue] = DEFAULT,
    rows: Union[HeatmapAxisData, DefaultValue] = DEFAULT,
    columns: Union[HeatmapAxisData, DefaultValue] = DEFAULT,
    configuration: Union[HeatmapGraphConfiguration, DefaultValue] = DEFAULT,
) -> HeatmapGraph:
    """
    Create a :py:obj:`HeatmapGraph` by specifying only the :py:obj:`HeatmapGraphData` fields (with an optional
    :py:obj:`HeatmapGraphConfiguration`). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.heatmap_graph>`__
    for details.
    """
    return HeatmapGraph(
        data=HeatmapGraphData(figure_title=figure_title, entries=entries, cells=cells, rows=rows, columns=columns),
        configuration=configuration,
    )
