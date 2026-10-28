"""
Test recording what Julia compiles while our public functions run.
"""

# pylint: disable=missing-function-docstring

import json
import os
import subprocess
import sys
from textwrap import dedent

from somegraphspy.compile_tracing import SWITCH
from somegraphspy.compile_tracing import report

# A graph of ``int8`` values, which no workload makes, so Julia compiles for it. The second, same graph compiles nothing.
SESSION = dedent("""
    import numpy as np
    import somegraphspy as sg

    values = np.array([1, 2, 3], dtype="int8")
    sg.points_graph(x=sg.VectorValuesData(vector=values), y=sg.VectorValuesData(vector=values)).figure
    sg.points_graph(x=sg.VectorValuesData(vector=values), y=sg.VectorValuesData(vector=values)).figure
    """)


def test_compile_tracing(tmp_path) -> None:
    subprocess.run([sys.executable, "-c", SESSION], env=dict(os.environ, **{SWITCH: str(tmp_path)}), check=True)

    names = os.listdir(tmp_path)
    assert any(name.endswith(".trace.jl") for name in names)
    records_names = [name for name in names if name.endswith(".compiles.jsonl")]
    assert len(records_names) == 1

    with open(tmp_path / records_names[0], encoding="utf8") as file:
        entries = [json.loads(line) for line in file]
    assert entries
    assert all(entry["callable"].startswith("somegraphspy.") for entry in entries)
    assert any(entry["call_site"] == "<string>:6" and entry["compiled"] for entry in entries)
    assert not any(entry["call_site"] == "<string>:7" for entry in entries)

    text = report(str(tmp_path))
    assert entries[0]["callable"] in text
    assert "SomeGraphs:" in text.split("for their Workloads", 1)[1]
