"""
Make the calls of a typical session (for internal use).

The Julia package ``SomeGraphsPy`` runs this while it is precompiled, so the code these calls compile is cached, and a
session does not compile it again. It is not part of the API, so the package does not import it.
"""

import numpy as np

from .bars import SeriesData
from .bars import bars_graph
from .bars import series_bars_graph
from .common import MatrixValuesData
from .common import VectorEntitiesData
from .common import VectorValuesData
from .distributions import DistributionData
from .distributions import distribution_graph
from .distributions import distributions_graph
from .heatmaps import heatmap_graph
from .scatters import LineData
from .scatters import line_graph
from .scatters import lines_graph
from .scatters import points_graph

__all__ = ["run_workload"]


def run_workload() -> None:
    """
    Make the calls of a typical session, building and showing a small graph of each kind (for internal use).
    """
    values = np.array([1.0, 2.0, 3.0], dtype="float32")
    graphs = [
        points_graph(x=VectorValuesData(vector=values), y=VectorValuesData(vector=[1.0, 4.0, 9.0])),
        line_graph(x=VectorValuesData(vector=[1.0, 2.0, 3.0]), y=VectorValuesData(vector=values)),
        lines_graph(
            lines=[
                LineData(x=VectorValuesData(vector=[1.0, 2.0]), y=VectorValuesData(vector=[1.0, 2.0])),
                LineData(x=VectorValuesData(vector=[1.0, 3.0]), y=VectorValuesData(vector=[2.0, 4.0])),
            ]
        ),
        bars_graph(values=VectorValuesData(vector=values), bars=VectorEntitiesData(names=["a", "b", "c"])),
        series_bars_graph(
            series=[
                SeriesData(values=VectorValuesData(vector=[1.0, 2.0])),
                SeriesData(values=VectorValuesData(vector=[3.0, 4.0])),
            ],
            bars=VectorEntitiesData(names=["a", "b"]),
        ),
        distribution_graph(distribution=DistributionData(values=VectorValuesData(vector=values))),
        distributions_graph(
            distributions=[
                DistributionData(values=VectorValuesData(vector=[0.0, 1.0, 1.0, 2.0])),
                DistributionData(values=VectorValuesData(vector=[1.0, 2.0, 2.0, 3.0])),
            ]
        ),
        heatmap_graph(entries=MatrixValuesData(matrix=np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype="float32"))),
    ]
    for graph in graphs:
        graph.validate()
        _ = graph.json
        _ = graph.figure
