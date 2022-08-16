"""Main PytestChecker class."""

from __future__ import annotations

from typing import Any, Callable, Optional

from astroid import nodes
from pylint import interfaces
from pylint.lint import PyLinter

import pylint_pytest_plugin._utils as utils

AddMessage = Callable[
    [
        str,
        Optional[int],
        Optional[nodes.NodeNG],
        Optional[Any],
        Optional[interfaces.Confidence],
        Optional[int],
        Optional[int],
        Optional[int],
    ],
    None,
]


# pylint: disable-next=too-many-arguments
def mock_message_mock(
    msgid: str,
    line: int | None = None,
    node: nodes.NodeNG | None = None,
    args: Any | None = None,
    confidence: interfaces.Confidence | None = None,
    col_offset: int | None = None,
    end_lineno: int | None = None,
    end_col_offset: int | None = None,
    add_message: AddMessage | None = None,
    linter: PyLinter | None = None,
) -> None:
    """Mock the add_message method of a PyLinter object."""
    # pylint: disable=confusing-consecutive-elif
    assert add_message, "mock_message_mock() requires add_message"
    assert linter, "mock_message_mock() requires linter"

    if msgid == "unused-variable":
        if not emit_unused_variable(linter, node):
            return
    elif msgid == "unnecessary-lambda-assignment":
        if not emit_unnecessary_lambda_assignment(linter, node):
            return
    elif msgid == "redefined-outer-name":
        if not emit_redefined_outer_name(linter, node):
            return

    add_message(
        msgid,
        line,
        node,
        args,
        confidence,
        col_offset,
        end_lineno,
        end_col_offset,
    )


@utils.message_emitted_in_pytest_file
def emit_unused_variable(_: PyLinter, node: nodes.NodeNG | None) -> bool:
    """Check whether we should emit 'unused-variable'.

    We whitelist '__tracebackhide__'.
    """
    assert node
    if isinstance(node, nodes.AssignName):
        if node.name == "__tracebackhide__":
            return False
    return True


@utils.message_emitted_in_pytest_file
def emit_unnecessary_lambda_assignment(
    _: PyLinter,
    node: nodes.NodeNG | None,
) -> bool:
    """Check whether we should emit 'unnecessary-lambda-assignment'.

    We whitelist '__tracebackhide__'.
    """
    assert node
    if isinstance(node.parent, nodes.Assign) and isinstance(
        node.parent.targets[0], nodes.AssignName
    ):
        if node.parent.targets[0].name == "__tracebackhide__":
            return False
    return True


@utils.message_emitted_in_pytest_file
def emit_redefined_outer_name(
    _: PyLinter,
    node: nodes.NodeNG | None,
) -> bool:
    """Check whether we should emit 'redefined-outer-name'.

    This checks whether the name is actually a pytest fixture.
    """
    # Imports always redefine names from outer scopes
    if isinstance(node, (nodes.ImportFrom, nodes.Import)):
        return True

    assert isinstance(node, nodes.AssignName)
    definitions: nodes.NodeNG = node.root().locals.get(node.name, [])

    # Because we are redefinig we should always have at least one definition.
    assert definitions

    # We use the last definition as that is what pytest uses
    definition = definitions[-1]

    # Fixtures should be functions.
    if not isinstance(definition, nodes.FunctionDef):
        return True

    # Needs to be decorated with @pytest.fixture
    if not definition.decorators:
        return True

    for decorator in definition.decorators.nodes:
        if isinstance(decorator, nodes.Call):
            to_infer = decorator.func
        elif isinstance(decorator, nodes.Attribute):
            to_infer = decorator
        elif isinstance(decorator, nodes.Name):
            to_infer = decorator
        else:
            return True  # pragma: no cover, covered on 3.9+

        decorator_def = next(to_infer.infer())
        if (
            isinstance(decorator_def, nodes.FunctionDef)
            and decorator_def.qname() == "_pytest.fixtures.fixture"
        ):
            return False

    return True
