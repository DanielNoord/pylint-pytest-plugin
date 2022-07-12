"""Plugin for pytest compatibiltiy for pylint.

The plugin works by inserting itself into the add_message method of the
standard PyLinter class.
Therefore, it is highly susceptible to internal changes within pylint, but
it should be fine.
"""

from functools import partial

from pylint.lint import PyLinter

from pylint_pytest_plugin._mock_add_message import mock_message_mock


def register(linter: PyLinter) -> None:
    """Register the plugin checker."""
    original_add_mesage = linter.add_message
    linter.add_message = partial(
        mock_message_mock, add_message=original_add_mesage, linter=linter
    )
