"""
Test using the package from a plain script, as opposed to from a Jupyter notebook.

This runs in a separate process on purpose. Displaying a graph in a notebook and saving it from a script take different
paths through ``plotly``, and only a real process proves the script one needs neither a notebook nor ``IPython``.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,missing-function-docstring
# flake8: noqa: F403,F405

import os
import subprocess
import sys

import somegraphspy

SCRIPT = """
import sys

import somegraphspy as sg

graph = sg.points_graph(points_xs=[1.0, 2.0, 3.0], points_ys=[1.0, 4.0, 9.0], figure_title="from a script")
graph.validate()
graph.save(sys.argv[1] + "/graph.html")
graph.save(sys.argv[1] + "/graph.png")

assert isinstance(graph.json, str)
assert "IPython" not in sys.modules, "importing the package dragged in IPython"
print("done")
"""


def test_run_from_a_script(tmp_path: object) -> None:
    directory = str(tmp_path)  # type: ignore
    script_path = directory + "/script.py"
    with open(script_path, "w", encoding="utf8") as file:
        file.write(SCRIPT)

    environment = dict(os.environ)
    package_root = os.path.dirname(os.path.dirname(os.path.abspath(somegraphspy.__file__)))
    environment["PYTHONPATH"] = package_root + os.pathsep + environment.get("PYTHONPATH", "")

    completed = subprocess.run(
        [sys.executable, script_path, directory],
        check=True,
        capture_output=True,
        text=True,
        timeout=900,
        env=environment,
    )

    assert "done" in completed.stdout
    assert os.path.getsize(directory + "/graph.html") > 0
    assert os.path.getsize(directory + "/graph.png") > 0
