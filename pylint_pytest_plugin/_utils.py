"""Main PytestChecker class."""

from __future__ import annotations

import functools
from functools import lru_cache
from typing import Callable

from astroid import nodes
from pylint.lint import PyLinter


def message_emitted_in_pytest_file(
    func: Callable[[PyLinter, nodes.NodeNG | None], bool]
) -> functools._lru_cache_wrapper[bool]:
    """See whether the function is called on a pytest module or node."""

    @lru_cache(maxsize=None)
    def wrapper(linter: PyLinter, node: nodes.NodeNG | None) -> bool:
        """This calls the wrapped function if we are linting a pytest file."""
        # Check if the node is within a pytest function or class
        if node:
            frame = node.frame()
            while frame != node.root():
                if isinstance(frame, (nodes.ClassDef, nodes.FunctionDef)):
                    if frame.name.lower().startswith("test"):
                        return func(linter, node)
                assert frame.parent, "Frame has no parent"
                frame = frame.parent.frame()

        # Check if the module is a pytest module
        # pylint: disable-next=protected-access
        if contains_pytest_import(linter.file_state._module):
            return func(linter, node)
        return True

    return wrapper


@lru_cache(maxsize=None)
def contains_pytest_import(module: nodes.Module) -> bool:
    """Return True if the linter is linting a pytest file."""
    for import_node in module.nodes_of_class((nodes.Import, nodes.ImportFrom)):
        if isinstance(import_node, nodes.ImportFrom):
            if import_node.modname == "pytest":
                return True
        # pylint: disable-next=confusing-consecutive-elif
        elif isinstance(import_node, nodes.Import):
            if "pytest" == import_node.names[0][0]:
                return True
    return False
