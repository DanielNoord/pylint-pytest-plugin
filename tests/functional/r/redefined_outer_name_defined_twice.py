"""Test for redefined-outer-name for fixtures that are defined twice."""

from typing import Any

import pytest


def test_something(my_fixture_that_is_a_fixture: Any) -> None:
    """Test some fixtures."""
    assert not my_fixture_that_is_a_fixture


def my_fixture_that_is_a_fixture() -> None:
    """A fixture."""
    return None


@pytest.fixture()
def my_fixture_that_is_a_fixture() -> None:  # [function-redefined]
    """A fixture."""
    return None


def test_something_else(
    my_fixture_that_is_not_a_fixture: Any,  # [redefined-outer-name]
) -> None:
    """Test some fixtures."""
    assert not my_fixture_that_is_not_a_fixture


@pytest.fixture()
def my_fixture_that_is_not_a_fixture() -> None:
    """A fixture."""
    return None


def my_fixture_that_is_not_a_fixture() -> None:  # [function-redefined]
    """A fixture."""
    return None
