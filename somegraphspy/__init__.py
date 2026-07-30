"""
Generate graphs (using Plotly).

This is a thin wrapper for the ``SomeGraphs.jl`` Julia package, with the following adaptations:

* Each Julia data or configuration structure is wrapped by a Python class of the same name, whose fields are the same
  as the Julia fields. Since the fields are declared (with their types), auto-completion in Jupyter notebook (or any
  IDE) will guide you through the nested structures, which is the point of the strongly typed API.

* The Python classes hold no data of their own; they delegate to the Julia object. Reading a field returns the current
  Julia value and writing a field writes through to Julia, which validates it immediately. In particular, nested
  objects are shared rather than copied, exactly as they are in Julia; use ``copy`` if you need an independent one.

* Constructor parameters default to ``DEFAULT`` rather than to ``None``, so that ``None`` can be passed to explicitly
  mean Julia's ``nothing``. This matters because some fields have a default which isn't ``nothing`` (e.g., the
  ``rows_groups_gap`` of ``HeatmapGraphConfiguration`` is ``1``), so ``rows_groups_gap = None`` is the only way to ask
  for no gap at all.

* In Julia, the API is defined as a set of functions which take the graph as the 1st parameter. In Python, these are
  member functions of the graph classes (e.g., Julia's ``save_graph(graph, "foo.png")`` becomes Python's
  ``graph.save("foo.png")``). Python doesn't support the ``!`` trailing character in function names (to indicate
  modifying the object), so Julia's ``flip_axes!(graph)`` becomes Python's ``graph.flip_axes_in_place()``.

* Matrices are passed as ``numpy`` arrays, and need no transposing: ``matrix[row, column]`` in Python is the same entry
  as ``matrix[row, column]`` in Julia, whatever the memory layout of the array is. The layout only affects efficiency,
  never the results.

* Accessing ``graph.figure`` returns a ``plotly.graph_objects.Figure``, which Jupyter notebook knows how to display.
  Simply evaluating the graph in a cell will display it. Outside a notebook, call ``graph.show()`` to open the graph in
  a browser, or ``graph.save(path)`` to write it to a file.

Otherwise, the API works "just the same" :-) The documentation therefore mostly just links to the relevant entry in the
Julia `documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/index.html>`__.
"""

__author__ = "Oren Ben-Kiki"
__email__ = "oren@ben-kiki.org"
__version__ = "0.2.0"

# pylint: disable=wildcard-import,unused-wildcard-import

from .julia_import import *  # isort: skip
from .common import *  # isort: skip
from .distributions import *  # isort: skip
from .scatters import *  # isort: skip
from .bars import *  # isort: skip
from .heatmaps import *  # isort: skip
from . import enums  # isort: skip
from .enums import *  # isort: skip
