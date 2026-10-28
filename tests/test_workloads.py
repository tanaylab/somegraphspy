"""
Test the calls of a typical session, which ``SomeGraphsPy`` makes while it is precompiled.
"""

# pylint: disable=missing-function-docstring

from somegraphspy.workloads import run_workload


def test_run_workload() -> None:
    run_workload()
