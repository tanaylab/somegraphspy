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
from .common import ArrangementData
from .common import ColorsConfiguration
from .common import FigureConfiguration
from .common import Graph
from .common import IntegersVector
from .common import LineConfiguration
from .common import MatrixEntitiesData
from .common import MatrixValuesData
from .common import Validated
from .common import VectorEntitiesData
from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import JlEnum
from .julia_import import JlObject
from .julia_import import _from_julia
from .julia_import import _given
from .julia_import import _optional_jl_obj
from .julia_import import jl
from .julia_import import register_jl_type
from .sources import ColorsVectorFields
from .sources import HeatmapSide
from .sources import MatrixFields
from .sources import VectorDataFields

__all__ = [
    "EntriesConfiguration",
    "HeatmapGraph",
    "HeatmapGraphConfiguration",
    "HeatmapGraphData",
    "HeatmapGraphPlacement",
    "HeatmapLinkage",
    "HeatmapOrigin",
    "HeatmapSideConfiguration",
    "HeatmapSideData",
    "OrderSource",
    "SidePlacement",
    "TreeSource",
    "heatmap_graph",
]


class TreeSource(JlEnum):
    """
    Where the tree of a heatmap side comes from. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.TreeSource>`__
    for details.
    """

    #: The ``hclust`` of the arrangement.
    GivenTree = "GivenTree"
    #: Cluster the data.
    ClusteredTree = "ClusteredTree"
    #: Build a tree around the target order, so its leaves are exactly that order.
    OrderTree = "OrderTree"
    #: The tree of the other side.
    SameTree = "SameTree"


register_jl_type("TreeSource", TreeSource)


class OrderSource(JlEnum):
    """
    Where the order of a heatmap side comes from. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.OrderSource>`__
    for details.
    """

    #: The leaves of the given tree, as they are.
    GivenTreeOrder = "GivenTreeOrder"
    #: The leaves of the tree after reordering its branches using the (better) Bar-Joseph method.
    OptimalTreeReorder = "OptimalTreeReorder"
    #: The leaves of the tree after reordering its branches in the same (bad) way that R does.
    RCompatibleTreeReorder = "RCompatibleTreeReorder"
    #: The ``order`` of the entities.
    GivenOrder = "GivenOrder"
    #: The entries as they are.
    EntryOrder = "EntryOrder"
    #: Slant the data.
    SlantedOrder = "SlantedOrder"
    #: Slant the pre-squared data.
    SlantedPreSquaredOrder = "SlantedPreSquaredOrder"
    #: The order of the other side.
    SameOrder = "SameOrder"


register_jl_type("OrderSource", OrderSource)


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


class SidePlacement(JlObject):
    """
    Where the entries of one side of a heatmap were put: their final order, and the tree they were put by, if one was
    needed. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.SidePlacement>`__
    for details.

    The order is always a permutation of all the entries (hidden ones included), so it can be fed as-is into the
    ``order`` of the ``entities`` of a side of a :py:obj:`HeatmapGraphData` to show another graph in the same order.

    The ``hclust`` is a Julia ``Hclust`` object. There is no Python model for these, but it too can be fed back into the
    ``hclust`` of the :py:obj:`ArrangementData` of a side of a :py:obj:`HeatmapGraphData`, which reuses both the order
    and the tree, so the other graph also shows the same dendogram.

    These describe the order of the data, not the order it is displayed in; applying the ``origin`` and skipping the
    hidden entries is up to whoever shows the graph.
    """

    #: The final (1-based) order of the entries; the identity if they weren't reordered at all.
    order: IntegersVector
    #: The tree of the entries, if one was needed.
    hclust: Optional[Any]


register_jl_type("SidePlacement", SidePlacement)


class HeatmapGraphPlacement(JlObject):
    """
    The computed :py:obj:`SidePlacement` of the rows and of the columns of a heatmap graph, as returned by the graph's
    ``placement``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapGraphPlacement>`__
    for details.
    """

    #: The placement of the rows.
    rows: SidePlacement
    #: The placement of the columns.
    columns: SidePlacement


register_jl_type("HeatmapGraphPlacement", HeatmapGraphPlacement)


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


class HeatmapSideConfiguration(Validated):
    """
    Configure one side (the rows or the columns) of a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapSideConfiguration>`__
    for details.

    Groups (and subgroups) constrain the clustering, and are separated by a gap. Each level is placed independently: a
    level specified by numbers is laid out in the order of these numbers, and a level specified by names is laid out by
    the clustering. The ``subgroups_gap`` defaults to ``None`` because the usual reason to specify subgroups is to
    constrain the clustering rather than to show gaps.
    """

    #: The title of the axis.
    title: Optional[str]
    #: Show the tick labels (the names of the entries).
    show_ticks: bool
    #: Rotate the tick labels by this angle, in degrees.
    ticks_angle: Optional[float]
    #: The size of the annotations shown next to the entries.
    annotations: AnnotationSize
    #: Where the tree of the entries comes from, if one is needed; by default, inferred from what is given.
    tree_source: Optional[TreeSource]
    #: Where the order of the entries comes from; by default, inferred from what is given.
    order_source: Optional[OrderSource]
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
    #: Cap the total size of all the gaps to this fraction of the axis.
    total_gaps_fraction: Optional[float]
    #: The size of the dendogram, as a fraction of the graph size.
    dendogram_size: Optional[float]
    #: How to draw the dendogram.
    dendogram_line: LineConfiguration

    def __init__(
        self,
        *,
        title: Union[Optional[str], DefaultValue] = DEFAULT,
        show_ticks: Union[bool, DefaultValue] = DEFAULT,
        ticks_angle: Union[Optional[float], DefaultValue] = DEFAULT,
        annotations: Union[AnnotationSize, DefaultValue] = DEFAULT,
        tree_source: Union[Optional[TreeSource], DefaultValue] = DEFAULT,
        order_source: Union[Optional[OrderSource], DefaultValue] = DEFAULT,
        linkage: Union[Optional[HeatmapLinkage], DefaultValue] = DEFAULT,
        metric: Union[Optional[Any], DefaultValue] = DEFAULT,
        include_hidden: Union[bool, DefaultValue] = DEFAULT,
        groups_gap: Union[Optional[int], DefaultValue] = DEFAULT,
        subgroups_gap: Union[Optional[int], DefaultValue] = DEFAULT,
        total_gaps_fraction: Union[Optional[float], DefaultValue] = DEFAULT,
        dendogram_size: Union[Optional[float], DefaultValue] = DEFAULT,
        dendogram_line: Union[LineConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapSideConfiguration(
                **_given(
                    title=title,
                    show_ticks=show_ticks,
                    ticks_angle=ticks_angle,
                    annotations=annotations,
                    tree_source=tree_source,
                    order_source=order_source,
                    linkage=linkage,
                    metric=metric,
                    include_hidden=include_hidden,
                    groups_gap=groups_gap,
                    subgroups_gap=subgroups_gap,
                    total_gaps_fraction=total_gaps_fraction,
                    dendogram_size=dendogram_size,
                    dendogram_line=dendogram_line,
                )
            )
        )


register_jl_type("HeatmapSideConfiguration", HeatmapSideConfiguration)


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
    rows: HeatmapSideConfiguration
    #: How to show the columns.
    columns: HeatmapSideConfiguration
    #: Where the first entry of the matrix is shown.
    origin: HeatmapOrigin
    #: Caches the computed placement of the rows and the columns; access it through the graph's ``placement``, and
    #: reset it with the graph's ``reset_placement`` if anything it was computed from is changed after it was computed.
    final_placement: Optional[HeatmapGraphPlacement]

    def __init__(
        self,
        *,
        figure: Union[FigureConfiguration, DefaultValue] = DEFAULT,
        entries: Union[EntriesConfiguration, DefaultValue] = DEFAULT,
        rows: Union[HeatmapSideConfiguration, DefaultValue] = DEFAULT,
        columns: Union[HeatmapSideConfiguration, DefaultValue] = DEFAULT,
        origin: Union[HeatmapOrigin, DefaultValue] = DEFAULT,
        final_placement: Union[Optional[HeatmapGraphPlacement], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapGraphConfiguration(
                **_given(
                    figure=figure,
                    entries=entries,
                    rows=rows,
                    columns=columns,
                    origin=origin,
                    final_placement=final_placement,
                )
            )
        )


register_jl_type("HeatmapGraphConfiguration", HeatmapGraphConfiguration)


class HeatmapSideData(JlObject):
    """
    The data of one side (the rows or the columns) of a :py:obj:`HeatmapGraphData`. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapSideData>`__
    for details.
    """

    #: The names (shown as the tick labels), hovers, mask and order of the entries.
    entities: VectorEntitiesData
    #: What else the entries are arranged by.
    arrangement: ArrangementData
    #: Annotations shown next to the entries.
    annotations: Sequence[AnnotationData]
    #: The (1-based) order to show the annotations in.
    annotations_order: Optional[IntegersVector]

    def __init__(
        self,
        *,
        entities: Union[VectorEntitiesData, DefaultValue] = DEFAULT,
        arrangement: Union[ArrangementData, DefaultValue] = DEFAULT,
        annotations: Union[Sequence[AnnotationData], DefaultValue] = DEFAULT,
        annotations_order: Union[Optional[IntegersVector], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.HeatmapSideData(
                **_given(
                    entities=entities,
                    arrangement=arrangement,
                    annotations=annotations,
                    annotations_order=annotations_order,
                )
            )
        )


register_jl_type("HeatmapSideData", HeatmapSideData)


class HeatmapGraphData(AbstractGraphData):
    """
    The data of a graph showing a matrix of values as a heatmap. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.HeatmapGraphData>`__
    for details.
    """

    #: The title of the figure.
    figure_title: Optional[str]
    #: The value of each entry, a row per row and a column per column; their title is the colors legend title.
    entries: MatrixValuesData
    #: The hovers of the entries.
    cells: MatrixEntitiesData
    #: The data of the rows.
    rows: HeatmapSideData
    #: The data of the columns.
    columns: HeatmapSideData

    def __init__(
        self,
        *,
        figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
        entries: Union[MatrixValuesData, DefaultValue] = DEFAULT,
        cells: Union[MatrixEntitiesData, DefaultValue] = DEFAULT,
        rows: Union[HeatmapSideData, DefaultValue] = DEFAULT,
        columns: Union[HeatmapSideData, DefaultValue] = DEFAULT,
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
    def placement(self) -> HeatmapGraphPlacement:
        """
        The final order of the rows and the columns, and the trees they were placed by, without rendering the graph.
        See the Julia
        `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.heatmap_placement>`__
        for details.

        Use this to list the entries in the order they are shown, or to show several graphs in the same order by
        feeding it into the ``order`` of the ``entities`` of the ``rows`` and ``columns`` of their data. The placement
        is only computed once. Showing the graph will reuse it, and vice versa.

        .. note::

            Nothing detects that the cached placement went stale. Call :py:obj:`reset_placement` if anything it was
            computed from is changed after it was computed - that is, the ``tree_source``, ``order_source``,
            ``linkage``, ``metric``, ``dendogram_size`` and ``include_hidden`` of the sides configuration, and the
            ``entries.values``, the ``order`` of the sides entities and their ``arrangement``. The groups are easy to
            forget: they constrain the clustering, so saving the same graph twice, grouped differently each time,
            silently reuses the placement of the first grouping unless the cache is reset in between.
        """
        return _from_julia(jl.SomeGraphs.heatmap_placement(self.jl_obj))

    def reset_placement(self) -> None:
        """
        Forget the cached :py:obj:`HeatmapGraphPlacement`, so that asking for the graph's :py:obj:`placement` (or
        showing it) will compute it again. Call this after changing anything the placement was computed from. See the
        Julia
        `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/heatmaps.html#SomeGraphs.Heatmaps.reset_placement!>`__
        for details.
        """
        jl.SomeGraphs.reset_placement_b(self.jl_obj)

    def entries_matrix_fields(self) -> MatrixFields:
        """
        The data source view of the entries of the heatmap, colored by the ``entries.colors``.
        """
        return _from_julia(jl.SomeGraphs.entries_matrix_fields(self.jl_obj))

    def rows_groups_vector_data_fields(self) -> VectorDataFields:
        """
        The data source view of the groups of the rows.
        """
        return _from_julia(jl.SomeGraphs.rows_groups_vector_data_fields(self.jl_obj))

    def rows_subgroups_vector_data_fields(self) -> VectorDataFields:
        """
        The data source view of the subgroups of the rows.
        """
        return _from_julia(jl.SomeGraphs.rows_subgroups_vector_data_fields(self.jl_obj))

    def columns_groups_vector_data_fields(self) -> VectorDataFields:
        """
        The data source view of the groups of the columns.
        """
        return _from_julia(jl.SomeGraphs.columns_groups_vector_data_fields(self.jl_obj))

    def columns_subgroups_vector_data_fields(self) -> VectorDataFields:
        """
        The data source view of the subgroups of the columns.
        """
        return _from_julia(jl.SomeGraphs.columns_subgroups_vector_data_fields(self.jl_obj))

    def rows_annotations_colors_vector_fields(self, index: int) -> ColorsVectorFields:
        """
        The data source view of the (1-based) ``index`` annotation of the rows, which shares the entities of the rows.
        """
        return _from_julia(jl.SomeGraphs.rows_annotations_colors_vector_fields(self.jl_obj, index))

    def columns_annotations_colors_vector_fields(self, index: int) -> ColorsVectorFields:
        """
        The data source view of the (1-based) ``index`` annotation of the columns, which shares the entities of the
        columns.
        """
        return _from_julia(jl.SomeGraphs.columns_annotations_colors_vector_fields(self.jl_obj, index))

    def rows_entities(self) -> VectorEntitiesData:
        """
        The entities of the rows, shared by all their roles.
        """
        return _from_julia(jl.SomeGraphs.rows_entities(self.jl_obj))

    def columns_entities(self) -> VectorEntitiesData:
        """
        The entities of the columns, shared by all their roles.
        """
        return _from_julia(jl.SomeGraphs.columns_entities(self.jl_obj))

    def rows_arrangement(self) -> ArrangementData:
        """
        The arrangement of the rows.
        """
        return _from_julia(jl.SomeGraphs.rows_arrangement(self.jl_obj))

    def columns_arrangement(self) -> ArrangementData:
        """
        The arrangement of the columns.
        """
        return _from_julia(jl.SomeGraphs.columns_arrangement(self.jl_obj))

    def rows_side(self) -> HeatmapSide:
        """
        The rows side: its data, configuration and placement.
        """
        return _from_julia(jl.SomeGraphs.rows_side(self.jl_obj))

    def columns_side(self) -> HeatmapSide:
        """
        The columns side: its data, configuration and placement.
        """
        return _from_julia(jl.SomeGraphs.columns_side(self.jl_obj))

    def add_rows_annotation(self, annotation: Optional[AnnotationData] = None) -> int:
        """
        Append an ``annotation`` of the rows (by default, an empty one) and return its (1-based) index, for
        :py:obj:`rows_annotations_colors_vector_fields`.
        """
        return int(jl.SomeGraphs.add_rows_annotation_b(self.jl_obj, *_optional_jl_obj(annotation)))

    def add_columns_annotation(self, annotation: Optional[AnnotationData] = None) -> int:
        """
        Append an ``annotation`` of the columns (by default, an empty one) and return its (1-based) index, for
        :py:obj:`columns_annotations_colors_vector_fields`.
        """
        return int(jl.SomeGraphs.add_columns_annotation_b(self.jl_obj, *_optional_jl_obj(annotation)))


def heatmap_graph(
    *,
    figure_title: Union[Optional[str], DefaultValue] = DEFAULT,
    entries: Union[MatrixValuesData, DefaultValue] = DEFAULT,
    cells: Union[MatrixEntitiesData, DefaultValue] = DEFAULT,
    rows: Union[HeatmapSideData, DefaultValue] = DEFAULT,
    columns: Union[HeatmapSideData, DefaultValue] = DEFAULT,
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
