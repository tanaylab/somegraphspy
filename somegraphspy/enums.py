"""
All the enumerated types, collected in one place so that auto-completion can list them.

Since ``configuration.edges_style = <TAB>`` does not offer the valid values (no IDE infers the type of the assignment
target), the practical way to discover them is ``somegraphspy.enums.<TAB>`` for the types, and then ``.<TAB>`` again
for the values of the chosen one. The same types are also available directly, e.g. ``somegraphspy.LineStyle``.
"""

from .common import LineStyle
from .common import LogScale
from .common import Stacking
from .common import ValuesOrientation
from .distributions import DistributionStyle
from .heatmaps import HeatmapLinkage
from .heatmaps import HeatmapOrigin
from .heatmaps import HeatmapReorder

__all__ = [
    "DistributionStyle",
    "HeatmapLinkage",
    "HeatmapOrigin",
    "HeatmapReorder",
    "LineStyle",
    "LogScale",
    "Stacking",
    "ValuesOrientation",
]
