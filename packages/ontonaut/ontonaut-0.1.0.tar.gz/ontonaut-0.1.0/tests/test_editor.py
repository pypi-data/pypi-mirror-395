"""Tests for the CodeEditor widget."""

from typing import Any

from ontonaut import CodeEditor


class TestCodeEditor:
    """Tests for the CodeEditor widget."""

    def test_editor_initialization(self) -> None:
        """Test editor initializes with default values."""
        editor = CodeEditor()

        assert editor.code == ""
        assert editor.language == "python"
        assert editor.theme == "light"
        assert editor.output == ""
        assert editor.error == ""
        assert editor.line_numbers is True
        assert editor.read_only is False

    def test_editor_with_initial_code(self) -> None:
        """Test editor with initial code."""
        initial_code = "print('Hello, World!')"
        editor = CodeEditor(code=initial_code)

        assert editor.code == initial_code

    def test_editor_set_get_code(self) -> None:
        """Test setting and getting code."""
        editor = CodeEditor()

        test_code = "x = 10\ny = 20\nx + y"
        editor.set_code(test_code)

        assert editor.get_code() == test_code
        assert editor.code == test_code

    def test_editor_clear(self) -> None:
        """Test clearing editor."""
        editor = CodeEditor(code="test code", output="test output")

        editor.clear()

        assert editor.code == ""
        assert editor.output == ""
        assert editor.error == ""

    def test_editor_with_custom_language(self) -> None:
        """Test editor with custom language."""
        editor = CodeEditor(language="javascript", theme="dark")

        assert editor.language == "javascript"
        assert editor.theme == "dark"

    def test_editor_read_only(self) -> None:
        """Test read-only mode."""
        editor = CodeEditor(read_only=True)

        assert editor.read_only is True


class TestCodeEditorExecution:
    """Tests for code execution in the editor."""

    def test_execute_with_simple_executor(self) -> None:
        """Test execution with a simple executor."""

        def simple_executor(code: str) -> int:
            return eval(code)

        editor = CodeEditor(code="2 + 2", executor=simple_executor)
        result = editor.execute()

        assert result == 4
        assert editor.output == "4"
        assert editor.error == ""

    def test_execute_with_custom_code(self) -> None:
        """Test execution with custom code argument."""

        def calculator(code: str) -> int:
            return eval(code)

        editor = CodeEditor(executor=calculator)
        result = editor.execute("10 * 5")

        assert result == 50
        assert editor.output == "50"

    def test_execute_without_executor(self) -> None:
        """Test execution without an executor."""
        editor = CodeEditor(code="test code")
        result = editor.execute()

        assert result is None
        assert editor.output == ""
        assert editor.error == "No executor configured"

    def test_execute_with_error(self) -> None:
        """Test execution that raises an error."""

        def error_executor(code: str) -> int:
            raise ValueError("Test error")

        editor = CodeEditor(code="test", executor=error_executor)
        result = editor.execute()

        assert result is None
        assert editor.output == ""
        assert "ValueError: Test error" in editor.error

    def test_execute_returns_none(self) -> None:
        """Test execution that returns None."""

        def none_executor(code: str) -> None:
            return None

        editor = CodeEditor(code="test", executor=none_executor)
        result = editor.execute()

        assert result is None
        assert editor.output == ""
        assert editor.error == ""

    def test_executor_property(self) -> None:
        """Test getting and setting executor property."""
        editor = CodeEditor()

        assert editor.executor is None

        def test_executor(code: str) -> str:
            return "executed"

        editor.executor = test_executor
        assert editor.executor == test_executor

        result = editor.execute("test")
        assert result == "executed"

    def test_execute_with_multiline_code(self) -> None:
        """Test execution with multiline code."""

        def python_executor(code: str) -> Any:
            try:
                return eval(code)
            except SyntaxError:
                local_vars: dict = {}
                exec(code, {}, local_vars)
                return local_vars.get("result")

        code = """
x = 10
y = 20
result = x + y
"""
        editor = CodeEditor(code=code, executor=python_executor)
        result = editor.execute()

        assert result == 30


class TestCodeEditorConfiguration:
    """Tests for editor configuration options."""

    def test_placeholder_text(self) -> None:
        """Test custom placeholder text."""
        placeholder = "Enter your code here..."
        editor = CodeEditor(placeholder=placeholder)

        assert editor.placeholder == placeholder

    def test_line_numbers_disabled(self) -> None:
        """Test disabling line numbers."""
        editor = CodeEditor(line_numbers=False)

        assert editor.line_numbers is False

    def test_multiple_theme_options(self) -> None:
        """Test different theme options."""
        light_editor = CodeEditor(theme="light")
        dark_editor = CodeEditor(theme="dark")

        assert light_editor.theme == "light"
        assert dark_editor.theme == "dark"

    def test_language_options(self) -> None:
        """Test different language options."""
        languages = ["python", "javascript", "json", "markdown", "custom-lang"]

        for lang in languages:
            editor = CodeEditor(language=lang)
            assert editor.language == lang
