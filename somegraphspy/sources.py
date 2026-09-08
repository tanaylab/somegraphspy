"""
Data source views into the graphs. See the Julia
`documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html>`__ for details.

A view bundles the parts of a graph that one source of data fills: the values of one role, the entities they belong to,
and the configuration they are shown by. The views are obtained from a graph by its ``..._fields`` methods (e.g.,
``graph.x_fields()``), which mirror the Julia accessor functions. A source is any Python function writing into a view.
It works on any graph and any role that offers the same kind of view. The views hold no data of their own. They
reference the graph's own objects, so writing into them changes the graph.
"""

from typing import Union

from .common import AxisConfiguration
from .common import ColorsConfiguration
from .common import EntitiesData
from .common import MatrixData
from .common import MatrixEntitiesData
from .common import SizesConfiguration
from .common import ValuesData
from .julia_import import JlObject
from .julia_import import register_jl_type

__all__ = [
    "AxisConfigurationFields",
    "AxisFields",
    "ColorsConfigurationFields",
    "ColorsFields",
    "MatrixConfigurationFields",
    "MatrixDataFields",
    "MatrixFields",
    "SizesConfigurationFields",
    "SizesFields",
    "VectorDataFields",
    "VectorFields",
]


class VectorDataFields(JlObject):
    """
    The data half of a data source view: the values of one role of a graph and the entities these values belong to. See
    the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.VectorDataFields>`__
    for details.

    A source which only writes values, a title and hovers takes one of these. The ``data`` of every
    :py:obj:`VectorFields` is one, and so is a view of a role that has no configuration (the names of the bars, the
    groups of the rows of a heatmap), so such a source applies to all of them alike.
    """

    #: The values of the role.
    values: ValuesData
    #: The entities the values belong to (shared with the other roles of the same entities).
    entities: EntitiesData


register_jl_type("VectorDataFields", VectorDataFields)


class MatrixDataFields(JlObject):
    """
    The data half of a :py:obj:`MatrixFields` data source view: the entries of a heatmap and its cells. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.MatrixDataFields>`__
    for details.
    """

    #: The values of the entries.
    values: MatrixData
    #: The cells the values belong to.
    entities: MatrixEntitiesData


register_jl_type("MatrixDataFields", MatrixDataFields)


class AxisConfigurationFields(JlObject):
    """
    The configuration half of an :py:obj:`AxisFields` data source view. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.AxisConfigurationFields>`__
    for details.
    """

    #: The axis the values are shown along.
    axis: AxisConfiguration


register_jl_type("AxisConfigurationFields", AxisConfigurationFields)


class ColorsConfigurationFields(JlObject):
    """
    The configuration half of a :py:obj:`ColorsFields` data source view. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.ColorsConfigurationFields>`__
    for details.
    """

    #: The axis of the colors configuration, which scales the values.
    axis: AxisConfiguration
    #: How the values are colored.
    colors: ColorsConfiguration


register_jl_type("ColorsConfigurationFields", ColorsConfigurationFields)


class SizesConfigurationFields(JlObject):
    """
    The configuration half of a :py:obj:`SizesFields` data source view. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.SizesConfigurationFields>`__
    for details.
    """

    #: The axis of the sizes configuration, which scales the values.
    axis: AxisConfiguration
    #: How the values are sized.
    sizes: SizesConfiguration


register_jl_type("SizesConfigurationFields", SizesConfigurationFields)


class MatrixConfigurationFields(JlObject):
    """
    The configuration half of a :py:obj:`MatrixFields` data source view. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/sources.html#SomeGraphs.Sources.MatrixConfigurationFields>`__
    for details.
    """

    #: The axis of the colors configuration, which scales the entries.
    axis: AxisConfiguration
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
    view this is: an :py:obj:`AxisConfigurationFields` for values shown along an axis (:py:obj:`AxisFields`), a
    :py:obj:`ColorsConfigurationFields` for values shown as colors (:py:obj:`ColorsFields`), or a
    :py:obj:`SizesConfigurationFields` for values shown as sizes (:py:obj:`SizesFields`). All three have an ``axis``.
    """

    #: The values of the role and the entities they belong to.
    data: VectorDataFields
    #: How the values are shown.
    configuration: Union[AxisConfigurationFields, ColorsConfigurationFields, SizesConfigurationFields]


register_jl_type("VectorFields", VectorFields)

#: A :py:obj:`VectorFields` view of values shown along an axis; its ``configuration`` is an
#: :py:obj:`AxisConfigurationFields`.
AxisFields = VectorFields

#: A :py:obj:`VectorFields` view of values shown as colors; its ``configuration`` is a
#: :py:obj:`ColorsConfigurationFields`.
ColorsFields = VectorFields

#: A :py:obj:`VectorFields` view of values shown as sizes; its ``configuration`` is a
#: :py:obj:`SizesConfigurationFields`.
SizesFields = VectorFields


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
