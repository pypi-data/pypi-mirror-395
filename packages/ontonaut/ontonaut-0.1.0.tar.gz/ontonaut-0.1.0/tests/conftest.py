"""Pytest configuration and fixtures."""

import pytest

from ontonaut import CodeEditor
from ontonaut.executors import PythonExecutor


@pytest.fixture
def python_executor() -> PythonExecutor:
    """
    Provide a Python executor for tests.

    Returns:
        A new PythonExecutor instance.
    """
    return PythonExecutor()


@pytest.fixture
def simple_editor() -> CodeEditor:
    """
    Provide a simple code editor for tests.

    Returns:
        A new CodeEditor instance with basic configuration.
    """
    return CodeEditor(code="print('test')", language="python")


@pytest.fixture
def editor_with_executor() -> CodeEditor:
    """
    Provide a code editor with a Python executor.

    Returns:
        A new CodeEditor with PythonExecutor configured.
    """
    return CodeEditor(code="2 + 2", language="python", executor=lambda code: eval(code))
