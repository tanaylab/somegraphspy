"""
Common data types for specifying graphs. See the Julia
`documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html>`__ for details.
"""

# The enum values are named exactly as they are in Julia, so they are not UPPER_CASE.
# pylint: disable=invalid-name

from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import numpy as np
from plotly.graph_objects import Figure  # type: ignore
from plotly.io import from_json  # type: ignore

from .julia_import import DEFAULT
from .julia_import import DefaultValue
from .julia_import import JlEnum
from .julia_import import JlObject
from .julia_import import _given
from .julia_import import jl
from .julia_import import register_jl_type

__all__ = [
    "AbstractGraphConfiguration",
    "AbstractGraphData",
    "AnnotationData",
    "AnnotationSize",
    "AutomaticColors",
    "AxisConfiguration",
    "BandConfiguration",
    "BandsConfiguration",
    "BandsData",
    "BoolsVector",
    "CategoricalColors",
    "ColorsConfiguration",
    "ContinuousColors",
    "FigureConfiguration",
    "Graph",
    "IntegersVector",
    "LineConfiguration",
    "LineStyle",
    "LogScale",
    "MarginsConfiguration",
    "NAMED_COLOR_SCALES",
    "NumbersMatrix",
    "NumbersVector",
    "Palette",
    "SizesConfiguration",
    "Stacking",
    "StringsMatrix",
    "StringsVector",
    "Validated",
    "ValuesOrientation",
    "categorical_palette",
]

#: A vector of numbers.
NumbersVector = Union[np.ndarray, Sequence[float]]

#: A vector of integers.
IntegersVector = Union[np.ndarray, Sequence[int]]

#: A vector of strings.
StringsVector = Union[np.ndarray, Sequence[str]]

#: A vector of booleans, used as a mask.
BoolsVector = Union[np.ndarray, Sequence[bool]]

#: A matrix of numbers. Entry ``matrix[row, column]`` is the same entry in Python and in Julia, whatever the memory
#: layout of the array is.
NumbersMatrix = np.ndarray

#: A matrix of strings. Entry ``matrix[row, column]`` is the same entry in Python and in Julia, whatever the memory
#: layout of the array is.
StringsMatrix = np.ndarray

#: A continuous colors palette, mapping numbers to colors. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.ContinuousColors>`__
#: for details.
ContinuousColors = Sequence[Tuple[float, str]]

#: A categorical colors palette, mapping string values to colors. An empty color means the entity will not be shown.
#: See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.CategoricalColors>`__
#: for details.
CategoricalColors = Mapping[str, str]

#: The names of the standard Plotly color scales that can be used as a ``palette``. See the Julia
#: `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.NAMED_COLOR_SCALES>`__
#: for details.
NAMED_COLOR_SCALES = sorted(str(name) for name in jl.keys(jl.SomeGraphs.NAMED_COLOR_SCALES))


class Validated(JlObject):
    """
    A common type for objects that support validation. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/validations.html#SomeGraphs.Validations.Validated>`__
    for details.
    """

    def validate(self, name: str = "value") -> None:
        """
        Validate the object, raising an exception describing the problem if it isn't valid.

        The ``name`` is used as the prefix of the path reported in the error message.
        """
        jl.SomeGraphs.validate(jl.SomeGraphs.ValidationContext(jl.Vector([name])), self.jl_obj)


class ValuesOrientation(JlEnum):
    """
    The orientation of the values axis. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.ValuesOrientation>`__
    for details.
    """

    #: Show the values in the horizontal (X) axis.
    HorizontalValues = "HorizontalValues"
    #: Show the values in the vertical (Y) axis.
    VerticalValues = "VerticalValues"


register_jl_type("ValuesOrientation", ValuesOrientation)


class LogScale(JlEnum):
    """
    The base of the logarithm used to scale an axis. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.LogScale>`__
    for details.
    """

    #: Scale the axis using a base 10 logarithm.
    Log10Scale = "Log10Scale"
    #: Scale the axis using a base 2 logarithm.
    Log2Scale = "Log2Scale"


register_jl_type("LogScale", LogScale)


class LineStyle(JlEnum):
    """
    The style of a line. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.LineStyle>`__
    for details.
    """

    #: Draw a solid line.
    SolidLine = "SolidLine"
    #: Draw a dashed line.
    DashLine = "DashLine"
    #: Draw a dotted line.
    DotLine = "DotLine"
    #: Draw a dash-dotted line.
    DashDotLine = "DashDotLine"


register_jl_type("LineStyle", LineStyle)


class Stacking(JlEnum):
    """
    How to stack multiple series on top of each other. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.Stacking>`__
    for details.
    """

    #: Stack the actual values.
    StackValues = "StackValues"
    #: Stack the fractions of the values out of the total.
    StackFractions = "StackFractions"


register_jl_type("Stacking", Stacking)


class AutomaticColors(JlObject):
    """
    A marker for the ``palette`` of a :py:obj:`ColorsConfiguration`, specifying that string color values are
    categorical keys whose colors are picked automatically. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.AutomaticColors>`__
    for details.
    """

    def __init__(self) -> None:
        super().__init__(jl.SomeGraphs.AutomaticColors())


register_jl_type("AutomaticColors", AutomaticColors)

#: The ways to specify how to color data: a named Plotly color scale, an explicit continuous or categorical palette, or
#: :py:obj:`AutomaticColors`.
Palette = Union[str, ContinuousColors, CategoricalColors, AutomaticColors]


class MarginsConfiguration(Validated):
    """
    Configure the margins of the graph, in pixels. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.MarginsConfiguration>`__
    for details.
    """

    #: The left margin.
    left: int
    #: The bottom margin.
    bottom: int
    #: The right margin.
    right: int
    #: The top margin.
    top: int

    def __init__(
        self,
        *,
        left: Union[int, DefaultValue] = DEFAULT,
        bottom: Union[int, DefaultValue] = DEFAULT,
        right: Union[int, DefaultValue] = DEFAULT,
        top: Union[int, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.MarginsConfiguration(**_given(left=left, bottom=bottom, right=right, top=top)))


register_jl_type("MarginsConfiguration", MarginsConfiguration)


class FigureConfiguration(Validated):
    """
    Configure the overall figure. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.FigureConfiguration>`__
    for details.
    """

    #: The margins around the graph.
    margins: MarginsConfiguration
    #: The width of the figure in pixels.
    width: Optional[int]
    #: The height of the figure in pixels.
    height: Optional[int]
    #: The name of the Plotly template to use.
    template: Optional[str]
    #: The color of the area behind the graph itself.
    background_color: str
    #: The color of the area around the graph.
    paper_color: str
    #: The horizontal offsets of the color scales, as fractions of the graph width.
    colors_scale_offsets: NumbersVector

    def __init__(
        self,
        *,
        margins: Union[MarginsConfiguration, DefaultValue] = DEFAULT,
        width: Union[Optional[int], DefaultValue] = DEFAULT,
        height: Union[Optional[int], DefaultValue] = DEFAULT,
        template: Union[Optional[str], DefaultValue] = DEFAULT,
        background_color: Union[str, DefaultValue] = DEFAULT,
        paper_color: Union[str, DefaultValue] = DEFAULT,
        colors_scale_offsets: Union[NumbersVector, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.FigureConfiguration(
                **_given(
                    margins=margins,
                    width=width,
                    height=height,
                    template=template,
                    background_color=background_color,
                    paper_color=paper_color,
                    colors_scale_offsets=colors_scale_offsets,
                )
            )
        )


register_jl_type("FigureConfiguration", FigureConfiguration)


class SizesConfiguration(Validated):
    """
    Configure how to scale data values into sizes (in pixels). See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.SizesConfiguration>`__
    for details.
    """

    #: Use this fixed size for everything, instead of scaling the data.
    fixed: Optional[float]
    #: The minimal data value to show.
    minimum: Optional[float]
    #: The maximal data value to show.
    maximum: Optional[float]
    #: Scale the data values by their logarithm.
    log_scale: bool
    #: Added to the data values before taking their logarithm.
    log_regularization: float
    #: The size of the smallest data value.
    smallest: float
    #: Added to the ``smallest`` size for the largest data value.
    span: float

    def __init__(
        self,
        *,
        fixed: Union[Optional[float], DefaultValue] = DEFAULT,
        minimum: Union[Optional[float], DefaultValue] = DEFAULT,
        maximum: Union[Optional[float], DefaultValue] = DEFAULT,
        log_scale: Union[bool, DefaultValue] = DEFAULT,
        log_regularization: Union[float, DefaultValue] = DEFAULT,
        smallest: Union[float, DefaultValue] = DEFAULT,
        span: Union[float, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.SizesConfiguration(
                **_given(
                    fixed=fixed,
                    minimum=minimum,
                    maximum=maximum,
                    log_scale=log_scale,
                    log_regularization=log_regularization,
                    smallest=smallest,
                    span=span,
                )
            )
        )


register_jl_type("SizesConfiguration", SizesConfiguration)


class AxisConfiguration(Validated):
    """
    Configure an axis of a graph. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.AxisConfiguration>`__
    for details.
    """

    #: The minimal value shown in the axis.
    minimum: Optional[float]
    #: The maximal value shown in the axis.
    maximum: Optional[float]
    #: Expand the axis range by this fraction of the data range.
    expand_fraction: float
    #: Scale the axis by a logarithm of this base.
    log_scale: Optional[LogScale]
    #: Added to the values before taking their logarithm.
    log_regularization: float
    #: Show the values as percents.
    percent: bool
    #: Show the tick labels.
    show_ticks: bool
    #: Rotate the tick labels by this angle, in degrees.
    ticks_angle: Optional[float]
    #: Show the grid lines.
    show_grid: bool
    #: The color of the grid lines.
    grid_color: str
    #: The title of the axis.
    title: Optional[str]

    def __init__(
        self,
        *,
        minimum: Union[Optional[float], DefaultValue] = DEFAULT,
        maximum: Union[Optional[float], DefaultValue] = DEFAULT,
        expand_fraction: Union[float, DefaultValue] = DEFAULT,
        log_scale: Union[Optional[LogScale], DefaultValue] = DEFAULT,
        log_regularization: Union[float, DefaultValue] = DEFAULT,
        percent: Union[bool, DefaultValue] = DEFAULT,
        show_ticks: Union[bool, DefaultValue] = DEFAULT,
        ticks_angle: Union[Optional[float], DefaultValue] = DEFAULT,
        show_grid: Union[bool, DefaultValue] = DEFAULT,
        grid_color: Union[str, DefaultValue] = DEFAULT,
        title: Union[Optional[str], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.AxisConfiguration(
                **_given(
                    minimum=minimum,
                    maximum=maximum,
                    expand_fraction=expand_fraction,
                    log_scale=log_scale,
                    log_regularization=log_regularization,
                    percent=percent,
                    show_ticks=show_ticks,
                    ticks_angle=ticks_angle,
                    show_grid=show_grid,
                    grid_color=grid_color,
                    title=title,
                )
            )
        )


register_jl_type("AxisConfiguration", AxisConfiguration)


class LineConfiguration(Validated):
    """
    Configure a line in a graph. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.LineConfiguration>`__
    for details.
    """

    #: The width of the line in pixels.
    width: Optional[float]
    #: The style of the line, or ``None`` not to show it at all.
    style: Optional[LineStyle]
    #: Fill the area below (or to the left of) the line.
    is_filled: bool
    #: The color of the line.
    color: Optional[str]

    def __init__(
        self,
        *,
        width: Union[Optional[float], DefaultValue] = DEFAULT,
        style: Union[Optional[LineStyle], DefaultValue] = DEFAULT,
        is_filled: Union[bool, DefaultValue] = DEFAULT,
        color: Union[Optional[str], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.LineConfiguration(**_given(width=width, style=style, is_filled=is_filled, color=color))
        )


register_jl_type("LineConfiguration", LineConfiguration)


class BandConfiguration(Validated):
    """
    Configure a single band in a graph. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.BandConfiguration>`__
    for details.
    """

    #: The offset of the band, or ``None`` not to show it at all.
    offset: Optional[float]
    #: How to draw the boundary line of the band.
    line: LineConfiguration

    def __init__(
        self,
        *,
        offset: Union[Optional[float], DefaultValue] = DEFAULT,
        line: Union[LineConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.BandConfiguration(**_given(offset=offset, line=line)))


register_jl_type("BandConfiguration", BandConfiguration)


class BandsConfiguration(Validated):
    """
    Configure the partition of a graph into low, middle and high regions. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.BandsConfiguration>`__
    for details.
    """

    #: The band separating the low region.
    low: BandConfiguration
    #: The band in the middle region.
    middle: BandConfiguration
    #: The band separating the high region.
    high: BandConfiguration

    def __init__(
        self,
        *,
        low: Union[BandConfiguration, DefaultValue] = DEFAULT,
        middle: Union[BandConfiguration, DefaultValue] = DEFAULT,
        high: Union[BandConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.BandsConfiguration(**_given(low=low, middle=middle, high=high)))


register_jl_type("BandsConfiguration", BandsConfiguration)


class BandsData(JlObject):
    """
    Override the band offsets specified in the configuration, when they depend on the data. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.BandsData>`__
    for details.
    """

    #: The offset of the band separating the low region.
    low_offset: Optional[float]
    #: The offset of the band in the middle region.
    middle_offset: Optional[float]
    #: The offset of the band separating the high region.
    high_offset: Optional[float]

    def __init__(
        self,
        *,
        low_offset: Union[Optional[float], DefaultValue] = DEFAULT,
        middle_offset: Union[Optional[float], DefaultValue] = DEFAULT,
        high_offset: Union[Optional[float], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.BandsData(
                **_given(low_offset=low_offset, middle_offset=middle_offset, high_offset=high_offset)
            )
        )


register_jl_type("BandsData", BandsData)


class ColorsConfiguration(Validated):
    """
    Configure how to color some data. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.ColorsConfiguration>`__
    for the (many) supported combinations of configuration and data.
    """

    #: How to map the colors data to actual colors.
    palette: Optional[Palette]
    #: Give all the entities this same color.
    fixed: Optional[str]
    #: How to scale the (numeric) colors data.
    axis: AxisConfiguration
    #: Show a legend (or a color scale) for the colors.
    show_legend: bool
    #: The title to use when showing the legend.
    title: Optional[str]

    def __init__(
        self,
        *,
        palette: Union[Optional[Palette], DefaultValue] = DEFAULT,
        fixed: Union[Optional[str], DefaultValue] = DEFAULT,
        axis: Union[AxisConfiguration, DefaultValue] = DEFAULT,
        show_legend: Union[bool, DefaultValue] = DEFAULT,
        title: Union[Optional[str], DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.ColorsConfiguration(
                **_given(palette=palette, fixed=fixed, axis=axis, show_legend=show_legend, title=title)
            )
        )


register_jl_type("ColorsConfiguration", ColorsConfiguration)


class AnnotationSize(Validated):
    """
    Configure the size of the annotations shown next to a graph. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.AnnotationSize>`__
    for details.
    """

    #: The size of each annotation, as a fraction of the graph size.
    size: float
    #: The gap between annotations, as a fraction of the graph size.
    gap: float

    def __init__(
        self,
        *,
        size: Union[float, DefaultValue] = DEFAULT,
        gap: Union[float, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(jl.SomeGraphs.AnnotationSize(**_given(size=size, gap=gap)))


register_jl_type("AnnotationSize", AnnotationSize)


class AnnotationData(Validated):
    """
    The data of a single annotation shown next to a graph. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.AnnotationData>`__
    for details.
    """

    #: The title of the annotation.
    title: Optional[str]
    #: A value per annotated entity, either numbers or category names.
    values: Union[NumbersVector, StringsVector]
    #: The hover text per annotated entity.
    hovers: Optional[StringsVector]
    #: How to color the annotation values.
    colors: ColorsConfiguration

    def __init__(
        self,
        *,
        title: Union[Optional[str], DefaultValue] = DEFAULT,
        values: Union[NumbersVector, StringsVector, DefaultValue] = DEFAULT,
        hovers: Union[Optional[StringsVector], DefaultValue] = DEFAULT,
        colors: Union[ColorsConfiguration, DefaultValue] = DEFAULT,
    ) -> None:
        super().__init__(
            jl.SomeGraphs.AnnotationData(**_given(title=title, values=values, hovers=hovers, colors=colors))
        )


register_jl_type("AnnotationData", AnnotationData)


class AbstractGraphConfiguration(Validated):
    """
    Specify how to display a graph, as much as possible independently of the data itself. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.AbstractGraphConfiguration>`__
    for details.
    """


class AbstractGraphData(Validated):
    """
    Specify what to display in a graph, as much as possible independently of how to display it. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.AbstractGraphData>`__
    for details.
    """


class Graph(Validated):
    """
    A combination of some :py:obj:`AbstractGraphData` and some :py:obj:`AbstractGraphConfiguration`. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.Graph>`__
    for details.
    """

    #: What to display.
    data: AbstractGraphData
    #: How to display it.
    configuration: AbstractGraphConfiguration

    @property
    def json(self) -> str:
        """
        Render the graph as a JSON string describing the Plotly figure. See the Julia
        `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/utilities.html#SomeGraphs.Utilities.graph_to_json>`__
        for details.
        """
        return str(jl.SomeGraphs.graph_to_json(self.jl_obj))

    @property
    def figure(self) -> Figure:
        """
        Render the graph as a ``plotly`` figure, which can be displayed and further manipulated using the normal
        ``plotly`` API.

        Simply evaluating the graph in a Jupyter notebook cell displays it, so this is only needed if you want the
        figure itself.
        """
        return from_json(self.json)

    def show(self) -> None:
        """
        Display the graph, opening it in a browser when not running in a notebook.
        """
        self.figure.show()

    def _repr_mimebundle_(self, include: Any = None, exclude: Any = None) -> Any:
        # This is how Jupyter notebook displays the graph when it is the value of a cell. Deliberately delegated to
        # ``plotly`` rather than implemented here, and deliberately not importing ``IPython``, so that nothing about
        # this costs anything (or even runs) outside a notebook.
        return self.figure._repr_mimebundle_(include, exclude)

    def save(self, output_file: str) -> None:
        """
        Save the graph to a file. The format is deduced from the suffix of the file name. See the Julia
        `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.save_graph>`__
        for details.

        Unlike the Plotly ``savefig`` function, this obeys the ``width`` and ``height`` of the figure configuration.
        Writing anything other than an ``html`` file starts a Kaleido process, which is slow the first time.
        """
        jl.SomeGraphs.save_graph(self.jl_obj, output_file)

    def flip_axes(self) -> "Graph":
        """
        Return a new graph with the axes flipped. See the Julia
        `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.flip_axes>`__
        for details.

        The returned graph shares storage with the original where possible.
        """
        return self.__class__.wrap_jl_object(jl.SomeGraphs.flip_axes(self.jl_obj))

    def flip_axes_in_place(self) -> "Graph":
        """
        Flip the axes of the graph in-place and return it. See the Julia
        `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.flip_axes!>`__
        for details.
        """
        return self.__class__.wrap_jl_object(jl.SomeGraphs.flip_axes_b(self.jl_obj))

    def validate(self, name: str = "graph") -> None:
        """
        Validate the graph, raising an exception describing the problem if it isn't valid.

        The ``name`` is used as the prefix of the path reported in the error message.
        """
        super().validate(name)


def categorical_palette(values: Union[StringsVector, Any], palette: Optional[str] = None) -> CategoricalColors:
    """
    Create a categorical colors palette assigning a distinct color to each of the ``values``. See the Julia
    `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/common.html#SomeGraphs.Common.categorical_palette>`__
    for details.
    """
    jl_values = jl.Vector(np.array([str(value) for value in values], dtype=str))
    if palette is None:
        jl_palette = jl.SomeGraphs.categorical_palette(jl_values)
    else:
        jl_palette = jl.SomeGraphs.categorical_palette(jl_values, palette)
    return {str(key): str(jl.getindex(jl_palette, key)) for key in jl.keys(jl_palette)}
