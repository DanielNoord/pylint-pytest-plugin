"""Test for setting __tracebackhide__ within a test function."""


import pytest  # [unused-import]


def assert_something() -> None:
    """My test."""
    __tracebackhide__ = True
    __tracebackhide__ = lambda x: isinstance(x, str)
