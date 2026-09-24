"""
Data source views into the graphs. See the Julia
`documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html>`__ for details.

A view bundles the parts of a graph that one source of data fills: the values of one role, the entities they belong to,
and the configuration they are shown by. The views are obtained from a graph by its ``..._fields`` methods (e.g.,
``graph.x_axis_vector_fields()``), which mirror the Julia accessor functions. A source is any Python function writing
into a view. It works on any graph and any role that offers the same kind of view. The views hold no data of their own.
They reference the graph's own objects, so writing into them changes the graph.
"""

from typing import Any
from typing import Callable
from typing import Sequence
from typing import Union

from .common import AxisConfiguration
from .common import ColorsConfiguration
from .common import MatrixEntitiesData
from .common import MatrixValuesData
from .common import ScaleConfiguration
from .common import SizesConfiguration
from .common import VectorEntitiesData
from .common import VectorValuesData
from .julia_import import JlObject
from .julia_import import _from_julia
from .julia_import import _to_julia
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

#: A struct holding graph data with a value per entity. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.VectorDataLeaf>`__
#: for details.
VectorDataLeaf = Union[VectorValuesData, VectorEntitiesData]

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

#: Anything that may contain graph data: a view, or the data half of one. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.DataContainer>`__
#: for details.
DataContainer = Union[VectorFields, MatrixFields, VectorDataFields, MatrixDataFields]

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
