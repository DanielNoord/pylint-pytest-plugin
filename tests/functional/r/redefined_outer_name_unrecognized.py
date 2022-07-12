"""Test for redefined-outer-name for fixtures that are unrecognizable."""

from typing import Any

import pytest  # [unused-import]


# This is mostly a test to increase coverage and show we handle weird decorators
@lambda x: x
def my_second_fixture() -> None:
    """A second fixture."""
    return None


def test_something_else(
    my_second_fixture: Any,  # [redefined-outer-name]
) -> None:
    """Test some fixtures."""
    assert not my_second_fixture
