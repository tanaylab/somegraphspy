"""
Data source views into the graphs. See the Julia
`documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html>`__ for details.

A view bundles the parts of a graph that one source of data fills: the values of one role, the entities they belong to,
and the configuration they are shown by. The views are obtained from a graph by its ``..._fields`` methods (e.g.,
``graph.x_axis_vector_fields()``), which mirror the Julia accessor functions. A source is any Python function writing
into a view. It works on any graph and any role that offers the same kind of view. The views hold no data of their own.
They reference the graph's own objects, so writing into them changes the graph.
"""

from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Optional
from typing import Sequence
from typing import Union

if TYPE_CHECKING:
    from .heatmaps import HeatmapSideConfiguration
    from .heatmaps import HeatmapSideData

from .common import ArrangementData
from .common import AxisConfiguration
from .common import BoolsVector
from .common import ColorsConfiguration
from .common import Graph
from .common import IntegersVector
from .common import LinkageMatrix
from .common import MatrixEntitiesData
from .common import MatrixValuesData
from .common import NumbersMatrix
from .common import NumbersVector
from .common import ScaleConfiguration
from .common import SidePlacement
from .common import SizesConfiguration
from .common import StringsVector
from .common import VectorEntitiesData
from .common import VectorValuesData
from .julia_import import JlObject
from .julia_import import _from_julia
from .julia_import import _given
from .julia_import import _to_julia
from .julia_import import _tree_to_julia
from .julia_import import jl
from .julia_import import register_jl_type

__all__ = [
    "AnyContainer",
    "AnyLeaf",
    "AnySink",
    "AxisConfigurationFields",
    "AxisVectorFields",
    "ColorsConfigurationFields",
    "ColorsVectorFields",
    "ConfigurationContainer",
    "ConfigurationLeaf",
    "ConfigurationSink",
    "DataContainer",
    "DataLeaf",
    "DataSink",
    "HeatmapSide",
    "MatrixConfigurationFields",
    "MatrixDataFields",
    "MatrixDataLeaf",
    "MatrixDataSinks",
    "MatrixFields",
    "PartFields",
    "Sinks",
    "SizesConfigurationFields",
    "SizesVectorFields",
    "VectorDataFields",
    "VectorDataLeaf",
    "VectorDataSinks",
    "VectorFields",
    "fill_annotations",
    "fill_arrangement",
    "fill_configuration",
    "fill_entities",
    "fill_placement",
    "fill_side",
    "put_matrix_data",
    "put_matrix_names_data",
    "put_vector_data",
    "put_vector_mask_data",
    "put_vector_names_data",
    "put_vector_order_data",
    "put_vector_tree_data",
    "visit_configuration_sinks",
    "visit_data_sinks",
]


class VectorDataFields(JlObject):
    """
    The data half of a data source view: the values of one role of a graph and the entities these values belong to. See
    the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.VectorDataFields>`__
    for details.

    A source which only writes values, a title and hovers takes one of these. The ``data`` of every
    :py:obj:`VectorFields` is one, and so is a view of a role that has no configuration (the groups of the rows of a
    heatmap), so such a source applies to all of them alike.
    """

    #: The values of the role.
    values: VectorValuesData
    #: The entities the values belong to (shared with the other roles of the same entities).
    entities: VectorEntitiesData


register_jl_type("VectorDataFields", VectorDataFields)


class MatrixDataFields(JlObject):
    """
    The data half of a :py:obj:`MatrixFields` data source view: the entries of a heatmap, its cells, and the entities of
    each of its two axes. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.MatrixDataFields>`__
    for details.
    """

    #: The values of the entries.
    values: MatrixValuesData
    #: The cells the values belong to.
    entities: MatrixEntitiesData
    #: The rows the values are indexed by (shared with the other roles of the rows).
    rows_entities: VectorEntitiesData
    #: The columns the values are indexed by (shared with the other roles of the columns).
    columns_entities: VectorEntitiesData


register_jl_type("MatrixDataFields", MatrixDataFields)


class AxisConfigurationFields(JlObject):
    """
    The configuration half of an :py:obj:`AxisVectorFields` data source view. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.AxisConfigurationFields>`__
    for details.
    """

    #: The axis the values are shown along.
    axis: AxisConfiguration


register_jl_type("AxisConfigurationFields", AxisConfigurationFields)


class ColorsConfigurationFields(JlObject):
    """
    The configuration half of a :py:obj:`ColorsVectorFields` data source view. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.ColorsConfigurationFields>`__
    for details.
    """

    #: The scale of the colors configuration, which scales the values.
    scale: ScaleConfiguration
    #: How the values are colored.
    colors: ColorsConfiguration


register_jl_type("ColorsConfigurationFields", ColorsConfigurationFields)


class SizesConfigurationFields(JlObject):
    """
    The configuration half of a :py:obj:`SizesVectorFields` data source view. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.SizesConfigurationFields>`__
    for details.
    """

    #: The scale of the sizes configuration, which scales the values.
    scale: ScaleConfiguration
    #: How the values are sized.
    sizes: SizesConfiguration


register_jl_type("SizesConfigurationFields", SizesConfigurationFields)


class MatrixConfigurationFields(JlObject):
    """
    The configuration half of a :py:obj:`MatrixFields` data source view. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.MatrixConfigurationFields>`__
    for details.
    """

    #: The scale of the colors configuration, which scales the entries.
    scale: ScaleConfiguration
    #: How the entries are colored.
    colors: ColorsConfiguration


register_jl_type("MatrixConfigurationFields", MatrixConfigurationFields)


class VectorFields(JlObject):
    """
    A data source view of one role of a graph whose entities are a vector: the ``data`` and the ``configuration``. See
    the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.VectorFields>`__
    for details.

    A function writing into such a view fills the role from some source of data, and works the same on the X
    coordinates of points, the values of bars, the colors of either, and so on. The ``configuration`` says what kind of
    view this is: an :py:obj:`AxisConfigurationFields` for values shown along an axis (:py:obj:`AxisVectorFields`), a
    :py:obj:`ColorsConfigurationFields` for values shown as colors (:py:obj:`ColorsVectorFields`), or a
    :py:obj:`SizesConfigurationFields` for values shown as sizes (:py:obj:`SizesVectorFields`).
    """

    #: The values of the role and the entities they belong to.
    data: VectorDataFields
    #: How the values are shown.
    configuration: Union[AxisConfigurationFields, ColorsConfigurationFields, SizesConfigurationFields]


register_jl_type("VectorFields", VectorFields)

#: A :py:obj:`VectorFields` view of values shown along an axis; its ``configuration`` is an
#: :py:obj:`AxisConfigurationFields`.
AxisVectorFields = VectorFields

#: A :py:obj:`VectorFields` view of values shown as colors; its ``configuration`` is a
#: :py:obj:`ColorsConfigurationFields`.
ColorsVectorFields = VectorFields

#: A :py:obj:`VectorFields` view of values shown as sizes; its ``configuration`` is a
#: :py:obj:`SizesConfigurationFields`.
SizesVectorFields = VectorFields


class PartFields(JlObject):
    """
    A data source view of one part of a graph built from several such parts (a series of bars, a line, a distribution),
    identified by its (1-based) ``index`` in the ``graph``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.PartFields>`__
    for details.

    The fields of the part's ``data`` (its ``name``, ``hover``, ``color``, ...) are also fields of the view, and so is
    its ``entities``, whatever the part calls them (the ``bars`` of a series, the ``points`` of a line). The roles of
    the part are :py:obj:`AxisVectorFields` views along the matching axis of the graph: the ``values`` of a series of
    bars or a distribution, the ``x`` and ``y`` of a line.
    """

    #: The graph the part belongs to.
    graph: Any
    #: The (1-based) index of the part in the graph.
    index: int
    #: The part itself (a ``SeriesData``, a ``LineData``, a ``DistributionData``).
    data: Any
    #: The entities of the part, shared by all its roles.
    entities: VectorEntitiesData
    #: The view of the values of the part (of a series of bars or a distribution).
    values: AxisVectorFields
    #: The view of the X coordinates of the part (of a line).
    x: AxisVectorFields
    #: The view of the Y coordinates of the part (of a line).
    y: AxisVectorFields


register_jl_type("PartFields", PartFields)


class MatrixFields(JlObject):
    """
    A data source view of the entries of a graph whose entities are arranged in rows and columns (a heatmap), shown as
    colors. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.MatrixFields>`__
    for details.
    """

    #: The values of the entries and the cells they belong to.
    data: MatrixDataFields
    #: How the entries are colored.
    configuration: MatrixConfigurationFields


register_jl_type("MatrixFields", MatrixFields)


class HeatmapSide(JlObject):
    """
    One side (the rows or the columns) of a heatmap graph, as returned by its ``rows_side`` and ``columns_side``. It
    stands for the side's data, configuration and computed placement. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.HeatmapSide>`__
    for details.

    As a sink, it reaches the entities and the arrangement of the side.
    """

    #: The heatmap graph the side belongs to.
    graph: Graph
    #: Whether this is the rows side (rather than the columns side).
    is_rows: bool

    def data(self) -> "HeatmapSideData":
        """
        The data of the side: the entities, the arrangement and the annotations of its entries.
        """
        return _from_julia(jl.SomeGraphs.side_data(self.jl_obj))

    def configuration(self) -> "HeatmapSideConfiguration":
        """
        The configuration of the side.
        """
        return _from_julia(jl.SomeGraphs.side_configuration(self.jl_obj))

    def placement(self) -> SidePlacement:
        """
        The computed placement of the side: the final order of its entries, and the tree they were placed by, if one
        was needed.
        """
        return _from_julia(jl.SomeGraphs.side_placement(self.jl_obj))


register_jl_type("HeatmapSide", HeatmapSide)

#: A struct holding graph data with a value per entity. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.VectorDataLeaf>`__
#: for details.
VectorDataLeaf = Union[VectorValuesData, VectorEntitiesData, ArrangementData]

#: A struct holding graph data with a value per row per column. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.MatrixDataLeaf>`__
#: for details.
MatrixDataLeaf = Union[MatrixValuesData, MatrixEntitiesData]

#: A struct holding graph data. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.DataLeaf>`__
#: for details.
DataLeaf = Union[VectorDataLeaf, MatrixDataLeaf]

#: A struct holding graph configuration. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.ConfigurationLeaf>`__
#: for details.
ConfigurationLeaf = Union[AxisConfiguration, ScaleConfiguration, ColorsConfiguration, SizesConfiguration]

#: A :py:obj:`DataLeaf` or a :py:obj:`ConfigurationLeaf`. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.AnyLeaf>`__
#: for details.
AnyLeaf = Union[DataLeaf, ConfigurationLeaf]

#: Anything that may contain graph data: a view, the data half of one, or a side of a heatmap. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.DataContainer>`__
#: for details.
DataContainer = Union[VectorFields, MatrixFields, VectorDataFields, MatrixDataFields, HeatmapSide]

#: Anything that may contain graph configuration: a view, or the configuration half of one. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.ConfigurationContainer>`__
#: for details.
ConfigurationContainer = Union[
    VectorFields, MatrixFields, AxisConfigurationFields, ColorsConfigurationFields, SizesConfigurationFields
]

#: A :py:obj:`DataContainer` or a :py:obj:`ConfigurationContainer`. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.AnyContainer>`__
#: for details.
AnyContainer = Union[DataContainer, ConfigurationContainer]

#: One struct a data source writes data into. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.DataSink>`__
#: for details.
DataSink = Union[DataContainer, DataLeaf]

#: One struct a data source writes configuration into. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.ConfigurationSink>`__
#: for details.
ConfigurationSink = Union[ConfigurationContainer, ConfigurationLeaf]

#: Any one struct a data source writes into. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.AnySink>`__
#: for details.
AnySink = Union[AnyContainer, AnyLeaf]

#: What a data source accepts: one :py:obj:`AnySink`, or a sequence of them. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.Sinks>`__
#: for details.
Sinks = Union[AnySink, Sequence[AnySink]]

#: What a data source writing a value per entity accepts: every :py:obj:`Sinks` but a :py:obj:`MatrixDataLeaf`. See the
#: Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.VectorDataSinks>`__
#: for details.
VectorDataSinks = Union[AnyContainer, ConfigurationLeaf, VectorDataLeaf, Sequence[AnySink]]

#: What a data source writing a value per row per column accepts: every :py:obj:`Sinks` but a :py:obj:`VectorDataLeaf`.
#: See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.MatrixDataSinks>`__
#: for details.
MatrixDataSinks = Union[AnyContainer, ConfigurationLeaf, MatrixDataLeaf, Sequence[AnySink]]


def visit_data_sinks(visitor: Callable[[Any], None], sinks: Sinks) -> None:
    """
    Call the ``visitor`` on each data struct among the ``sinks`` (and inside the views among them), once each. See the
    Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.visit_data_sinks>`__
    for details.
    """
    jl.SomeGraphsPy._visit_data_sinks(lambda sink: visitor(_from_julia(sink)), _to_julia(sinks))


def visit_configuration_sinks(visitor: Callable[[Any], None], sinks: Sinks) -> None:
    """
    Call the ``visitor`` on each configuration struct among the ``sinks`` (and inside the views among them), once each.
    See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.visit_configuration_sinks>`__
    for details.
    """
    jl.SomeGraphsPy._visit_configuration_sinks(lambda sink: visitor(_from_julia(sink)), _to_julia(sinks))


def put_vector_data(
    sinks: VectorDataSinks,
    value_per_entry: Union[NumbersVector, StringsVector, BoolsVector],
    *,
    title: Optional[str] = None,
) -> None:
    """
    Put a ``value_per_entry`` into the ``sinks``: as the values of a role, and as a hover line on the entities. See the
    Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.put_vector_data!>`__
    for details.
    """
    jl.SomeGraphs.put_vector_data_b(_to_julia(sinks), _to_julia(value_per_entry), **_given(title=title))


def put_vector_names_data(sinks: VectorDataSinks, name_per_entry: StringsVector) -> None:
    """
    Name the entities of the ``sinks`` after the ``name_per_entry``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.put_vector_names_data!>`__
    for details.
    """
    jl.SomeGraphs.put_vector_names_data_b(_to_julia(sinks), _to_julia(name_per_entry))


def put_vector_mask_data(sinks: VectorDataSinks, is_shown_per_entry: BoolsVector) -> None:
    """
    Hide the entities of the ``sinks`` which are not shown by the ``is_shown_per_entry`` mask. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.put_vector_mask_data!>`__
    for details.
    """
    jl.SomeGraphs.put_vector_mask_data_b(_to_julia(sinks), _to_julia(is_shown_per_entry))


def put_vector_order_data(sinks: VectorDataSinks, order: IntegersVector) -> None:
    """
    Give the entities of the ``sinks`` the ``order`` (a permutation of their 1-based indices). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.put_vector_order_data!>`__
    for details.
    """
    jl.SomeGraphs.put_vector_order_data_b(_to_julia(sinks), _to_julia(order))


def put_matrix_data(
    sinks: MatrixDataSinks, value_per_row_per_column: NumbersMatrix, *, title: Optional[str] = None
) -> None:
    """
    Put a ``value_per_row_per_column`` into the ``sinks``: as the values of the entries, and as a hover line on each
    entry. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.put_matrix_data!>`__
    for details.
    """
    jl.SomeGraphs.put_matrix_data_b(_to_julia(sinks), _to_julia(value_per_row_per_column), **_given(title=title))


def put_matrix_names_data(sinks: MatrixDataSinks, name_per_row: StringsVector, name_per_column: StringsVector) -> None:
    """
    Name the rows and the columns of the ``sinks`` after the ``name_per_row`` and the ``name_per_column``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.put_matrix_names_data!>`__
    for details.
    """
    jl.SomeGraphs.put_matrix_names_data_b(_to_julia(sinks), _to_julia(name_per_row), _to_julia(name_per_column))


def put_vector_tree_data(sinks: VectorDataSinks, hclust: Optional[LinkageMatrix]) -> None:
    """
    Give the arrangement of the ``sinks`` (that is, of the heatmap sides among them) the ``hclust`` tree of its
    entries. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.put_vector_tree_data!>`__
    for details.
    """
    jl.SomeGraphs.put_vector_tree_data_b(_to_julia(sinks), _tree_to_julia(hclust))


def fill_entities(sinks: VectorDataSinks, source: Union[HeatmapSide, VectorEntitiesData]) -> None:
    """
    Fill the entities of the ``sinks`` with a copy of the names, hovers, mask and order of the entities of the
    ``source``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.fill_entities!>`__
    for details.
    """
    jl.SomeGraphs.fill_entities_b(_to_julia(sinks), _to_julia(source))


def fill_arrangement(sinks: VectorDataSinks, source: Union[HeatmapSide, ArrangementData]) -> None:
    """
    Fill the arrangement of the ``sinks`` with a copy of the tree, groups, subgroups and ``arrange_by`` matrix of the
    arrangement of the ``source``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.fill_arrangement!>`__
    for details.
    """
    jl.SomeGraphs.fill_arrangement_b(_to_julia(sinks), _to_julia(source))


def fill_annotations(target: HeatmapSide, source: HeatmapSide) -> None:
    """
    Fill the annotations of the ``target`` side with a copy of the annotations of the ``source`` side. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.fill_annotations!>`__
    for details.
    """
    jl.SomeGraphs.fill_annotations_b(target.jl_obj, source.jl_obj)


def fill_configuration(target: HeatmapSide, source: HeatmapSide) -> None:
    """
    Fill the configuration of the ``target`` side with a copy of the configuration of the ``source`` side. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.fill_configuration!>`__
    for details.
    """
    jl.SomeGraphs.fill_configuration_b(target.jl_obj, source.jl_obj)


def fill_placement(target: HeatmapSide, source: Union[HeatmapSide, SidePlacement]) -> None:
    """
    Fill the ``target`` side with the computed placement of the ``source``: its final order and its tree (if any). The
    ``target`` is then placed exactly as the ``source`` was. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.fill_placement!>`__
    for details.

    Unlike the other fills, this does not copy an input of the graph. It turns what the inputs of the ``source``
    computed into inputs of the ``target``, so it also clears the inputs of the ``target`` which then have no effect:
    the ``tree_source``, ``order_source``, ``linkage`` and ``metric`` of its configuration, the ``arrange_by`` of its
    arrangement, and its groups and subgroups which are not drawn as gaps.
    """
    jl.SomeGraphs.fill_placement_b(target.jl_obj, source.jl_obj)


def fill_side(target: HeatmapSide, source: HeatmapSide) -> None:
    """
    Fill the ``target`` side with a copy of everything about the ``source`` side: its entities, arrangement,
    annotations and configuration, then its computed placement (see :py:obj:`fill_placement`, which is not a plain
    copy). This lays out the ``target`` exactly as the ``source``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.fill_side!>`__
    for details.
    """
    jl.SomeGraphs.fill_side_b(target.jl_obj, source.jl_obj)
