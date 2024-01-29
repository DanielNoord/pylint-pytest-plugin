"""Tests using the functional test framework of Pylint."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock

import pytest
from _pytest.config import Config
from pylint import testutils
from pylint.testutils import UPDATE_FILE, UPDATE_OPTION
from pylint.testutils.functional import (
    FunctionalTestFile,
    LintModuleOutputUpdate,
    get_functional_test_files_from_directory,
)

TESTS = get_functional_test_files_from_directory(
    Path(__file__).parent.resolve() / "functional"
)
TESTS_NAMES = [t.base for t in TESTS]


@pytest.fixture
def pytestconfig() -> mock.MagicMock:
    """Mock the pytest config object."""

    def _mock_getoption(_: str) -> bool:
        return False

    config = mock.MagicMock()
    config.getoption.side_effect = _mock_getoption
    return config


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_functional(
    test_file: FunctionalTestFile,
    pytestconfig: Config,  # pylint: disable=redefined-outer-name
) -> None:
    """Run the functional tests."""
    # pylint: disable=protected-access
    __tracebackhide__ = True
    lint_test: LintModuleOutputUpdate | testutils.LintModuleTest
    if UPDATE_FILE.exists():
        lint_test = LintModuleOutputUpdate(test_file, pytestconfig)
    else:
        lint_test = testutils.LintModuleTest(test_file, pytestconfig)
    lint_test._linter.load_plugin_modules(["pylint_pytest_plugin"])
    lint_test._linter.enable("useless-suppression")
    lint_test.setUp()
    lint_test.runTest()


if __name__ == "__main__":
    if UPDATE_OPTION in sys.argv:
        UPDATE_FILE.touch()
        sys.argv.remove(UPDATE_OPTION)
    try:
        pytest.main(sys.argv)
    finally:
        if UPDATE_FILE.exists():
            UPDATE_FILE.unlink()
