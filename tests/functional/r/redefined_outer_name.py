"""Test for redefined-outer-name for fixtures."""

from typing import Any

import pytest
from pytest import fixture as aliased_fixture


@pytest.fixture()
def my_fixture() -> None:
    """A fixture."""
    return None


@pytest.fixture(scope="module")
def my_second_fixture() -> None:
    """A second fixture."""
    return None


@pytest.fixture(name="my_third_fixture")
def my_third_fixture_definition() -> None:
    """A third fixture."""
    return None


@pytest.fixture
def my_fourth_fixture() -> None:
    """A fourth fixture."""
    return None


@aliased_fixture
def my_fifth_fixture() -> None:
    """A fifth fixture."""
    return None


def test_something(
    my_fixture: Any,
    my_second_fixture: Any,
    my_third_fixture: Any,
    my_fourth_fixture: Any,
    my_fifth_fixture: Any,
) -> None:
    """Test some fixtures."""
    assert not my_fixture
    assert not my_second_fixture
    assert not my_third_fixture
    assert not my_fourth_fixture
    assert not my_fifth_fixture


NOTAFIXTURE = None


def also_not_a_fixture() -> None:
    """A function that is not a fixture."""
    return None


def test_something_else(
    NOTAFIXTURE: Any,  # [redefined-outer-name, invalid-name]
    also_not_a_fixture: Any,  # [redefined-outer-name]
) -> None:
    """Test some fixtures."""
    assert not NOTAFIXTURE
    assert not also_not_a_fixture
