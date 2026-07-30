"""
Utilities for test code.
"""

# pylint: disable=wildcard-import,unused-wildcard-import,missing-function-docstring
# flake8: noqa: F403,F405

from contextlib import contextmanager
from typing import Iterator
from typing import Never


@contextmanager
def assert_raises(expected: str) -> Iterator[Never]:
    try:
        yield  # type: ignore
        raise AssertionError("no exception was thrown")
    except Exception as exception:  # pylint: disable=broad-exception-caught
        actual = str(exception)
        if expected not in actual:
            raise exception
