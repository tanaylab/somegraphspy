somegraphspy 0.2.0 - Generate graphs (using Plotly)
===================================================

`SomeGraphs.jl <https://github.com/tanaylab/SomeGraphs.jl>`_ is a Julia package which generates a specific set of graph
types, using Plotly. Graphs are specified using strongly typed data and configuration structures, whose fields are as
high-level as possible and as orthogonal to each other as possible. This package (``somegraphspy``) is a wrapper around
the Julia package that allows generating such graphs from Python, using the
`JuliaCall <https://github.com/JuliaPy/PythonCall.jl>`_ package.

Installation
------------

Just ``pip install somegraphspy``, like installing any other Python package.

Usage
-----

The Python package provides the same API as the Julia package, with the following modifications:

- Each Julia data or configuration structure is wrapped by a Python class of the same name, with the same fields. The
  fields are declared with their types, so auto-completion in Jupyter notebook (or any IDE) will guide you through the
  nested structures.

- The Python classes hold no data of their own; they delegate to the Julia object. Writing a field writes through to
  Julia, which validates it immediately, and nested objects are shared rather than copied, exactly as they are in
  Julia.

- Constructor parameters default to ``DEFAULT`` rather than to ``None``, so that ``None`` can be passed to explicitly
  mean Julia's ``nothing``. Some fields have a default which isn't ``nothing``, so this is the only way to clear them.

- Functions which take the graph as their 1st parameter are exposed as member functions (e.g., write
  ``graph.save("foo.png")`` in Python instead of ``save_graph(graph, "foo.png")`` in Julia). There is no ``!`` suffix
  for functions that modify the data (e.g., write ``graph.flip_axes_in_place()`` instead of ``flip_axes!(graph)``).

- Matrices are passed as ``numpy`` arrays and need no transposing: ``matrix[row, column]`` in Python is the same entry
  as ``matrix[row, column]`` in Julia, whatever the memory layout of the array is.

- Accessing ``graph.figure`` returns a ``plotly.graph_objects.Figure``. Simply evaluating the graph in a Jupyter
  notebook cell will display it. Outside a notebook, call ``graph.show()`` to open it in a browser.

See the `Python v0.2.0 documentation <https://tanaylab.github.io/somegraphspy/v0.2.0/html/index.html>`_ and the
`Julia v0.2.0 documentation <https://tanaylab.github.io/SomeGraphs.jl/v0.2.0/index.html>`_ for details.

Status
------

Version 0.2.0 is an alpha release, tracking version 0.2.0 of the Julia package. Everything is subject to change based
on user feedback (so don't be shy). Comments, bug reports and PRs are welcome!

License (MIT)
-------------

Copyright © 2025 Weizmann Institute of Science

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
