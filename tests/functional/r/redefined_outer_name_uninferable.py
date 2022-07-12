"""Test for redefined-outer-name for fixtures that are uninferable."""

from typing import Any

import undefined as pytest  # [import-error]


@pytest.fixture()
def my_fixture() -> None:
    """A fixture."""
    return None


def test_something(
    my_fixture: Any,  # [redefined-outer-name]
) -> None:
    """Test some fixtures."""
    assert not my_fixture
