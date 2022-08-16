"""Test for redefined-outer-name for imports within tests."""

# pylint: disable=unused-import, import-error, reimported, import-outside-toplevel

import baz
import pytest
from spam import foo


def test_import_from() -> None:
    """Test ImportFrom still redefines."""
    from spam import foo  # [redefined-outer-name]


def test_import() -> None:
    """Test Import still redefines."""
    import baz  # [redefined-outer-name]
