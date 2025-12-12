"""Tests for custom code executors."""

import json

import pytest

from ontonaut.executors import (
    CalculatorExecutor,
    JSONExecutor,
    PythonExecutor,
    RegexExecutor,
    create_executor,
)


class TestPythonExecutor:
    """Tests for PythonExecutor."""

    def test_simple_expression(self) -> None:
        """Test executing simple Python expression."""
        executor = PythonExecutor()
        result = executor.execute("2 + 2")

        assert result == 4

    def test_multiline_code(self) -> None:
        """Test executing multiline Python code."""
        executor = PythonExecutor()
        # Multiline statements use exec, which updates locals
        code = "x = 10\ny = 20\nresult = x + y"
        executor.execute(code)
        # Variables are in locals_dict after exec
        assert executor.locals_dict.get("result") == 30

        # Simple expression uses eval and returns value
        result = executor.execute("10 + 20")
        assert result == 30

    def test_with_custom_globals(self) -> None:
        """Test executor with custom global variables."""
        executor = PythonExecutor(globals_dict={"PI": 3.14159})
        result = executor.execute("PI * 2")

        assert result == pytest.approx(6.28318)

    def test_with_custom_locals(self) -> None:
        """Test executor with custom local variables."""
        executor = PythonExecutor(locals_dict={"x": 100})
        result = executor.execute("x * 2")

        assert result == 200

    def test_callable_interface(self) -> None:
        """Test calling executor as a function."""
        executor = PythonExecutor()
        result = executor("5 * 5")

        assert result == 25

    def test_exec_vs_eval(self) -> None:
        """Test that executor handles both expressions and statements."""
        executor = PythonExecutor()

        # Expression (uses eval)
        result1 = executor.execute("10 + 20")
        assert result1 == 30

        # Statement (uses exec)
        result2 = executor.execute("x = 100")
        assert result2 is None  # exec returns None


class TestJSONExecutor:
    """Tests for JSONExecutor."""

    def test_valid_json(self) -> None:
        """Test with valid JSON."""
        executor = JSONExecutor()
        result = executor.execute('{"name": "Alice", "age": 30}')

        parsed = json.loads(result)
        assert parsed["name"] == "Alice"
        assert parsed["age"] == 30

    def test_json_pretty_print(self) -> None:
        """Test JSON pretty printing."""
        executor = JSONExecutor(indent=2)
        result = executor.execute('{"a":1,"b":2}')

        assert "  " in result  # Check for indentation
        assert "\n" in result  # Check for newlines

    def test_invalid_json(self) -> None:
        """Test with invalid JSON."""
        executor = JSONExecutor()

        with pytest.raises(json.JSONDecodeError):
            executor.execute("{invalid json}")

    def test_custom_indent(self) -> None:
        """Test with custom indentation."""
        executor = JSONExecutor(indent=4)
        result = executor.execute('{"key": "value"}')

        assert "    " in result


class TestCalculatorExecutor:
    """Tests for CalculatorExecutor."""

    def test_simple_arithmetic(self) -> None:
        """Test simple arithmetic operations."""
        executor = CalculatorExecutor()

        assert executor.execute("10 + 20") == 30
        assert executor.execute("50 - 10") == 40
        assert executor.execute("5 * 6") == 30
        assert executor.execute("100 / 4") == 25

    def test_variable_assignment(self) -> None:
        """Test variable assignment."""
        executor = CalculatorExecutor()
        code = "x = 10\ny = 20\nx + y"
        result = executor.execute(code)

        assert result == 30

    def test_variable_persistence(self) -> None:
        """Test that variables persist across executions."""
        executor = CalculatorExecutor()

        executor.execute("a = 5")
        result = executor.execute("a * 10")

        assert result == 50

    def test_complex_expression(self) -> None:
        """Test complex mathematical expressions."""
        executor = CalculatorExecutor()
        result = executor.execute("(10 + 20) * 2 - 5")

        assert result == 55

    def test_comments(self) -> None:
        """Test that comments are ignored."""
        executor = CalculatorExecutor()
        code = """
# This is a comment
x = 10
# Another comment
x * 2
"""
        result = executor.execute(code)
        assert result == 20

    def test_invalid_expression(self) -> None:
        """Test handling of invalid expressions."""
        executor = CalculatorExecutor()

        with pytest.raises(ValueError):
            executor.execute("invalid expression!!!")


class TestRegexExecutor:
    """Tests for RegexExecutor."""

    def test_simple_match(self) -> None:
        """Test simple regex matching."""
        executor = RegexExecutor()
        code = "pattern: \\d+\ntext: I have 42 apples"
        result = executor.execute(code)

        assert "42" in result
        assert "Matches:" in result

    def test_no_match(self) -> None:
        """Test when pattern doesn't match."""
        executor = RegexExecutor()
        code = "pattern: \\d+\ntext: No numbers here"
        result = executor.execute(code)

        assert "No matches found" in result

    def test_multiple_matches(self) -> None:
        """Test with multiple matches."""
        executor = RegexExecutor()
        code = "pattern: \\d+\ntext: 10 apples and 20 oranges"
        result = executor.execute(code)

        assert "10" in result
        assert "20" in result

    def test_invalid_regex(self) -> None:
        """Test with invalid regex pattern."""
        executor = RegexExecutor()
        code = "pattern: [invalid(\ntext: test"
        result = executor.execute(code)

        assert "Invalid regex" in result

    def test_missing_fields(self) -> None:
        """Test with missing pattern or text."""
        executor = RegexExecutor()

        result1 = executor.execute("pattern: \\d+")
        assert "Must specify both" in result1

        result2 = executor.execute("text: some text")
        assert "Must specify both" in result2


class TestCreateExecutor:
    """Tests for the create_executor factory function."""

    def test_create_python_executor(self) -> None:
        """Test creating Python executor."""
        executor = create_executor("python")
        result = executor("3 * 3")

        assert result == 9

    def test_create_json_executor(self) -> None:
        """Test creating JSON executor."""
        executor = create_executor("json", indent=2)
        result = executor('{"test": true}')

        assert "test" in result

    def test_create_calculator_executor(self) -> None:
        """Test creating calculator executor."""
        executor = create_executor("calculator")
        result = executor("5 + 5")

        assert result == 10

    def test_create_regex_executor(self) -> None:
        """Test creating regex executor."""
        executor = create_executor("regex")
        result = executor("pattern: test\ntext: this is a test")

        assert "test" in result

    def test_case_insensitive(self) -> None:
        """Test that language name is case insensitive."""
        executor = create_executor("PYTHON")
        result = executor("1 + 1")

        assert result == 2

    def test_unknown_language(self) -> None:
        """Test error with unknown language."""
        with pytest.raises(ValueError, match="Unknown language"):
            create_executor("unknown-lang")

    def test_with_kwargs(self) -> None:
        """Test passing kwargs to executor."""
        executor = create_executor("json", indent=4)
        result = executor('{"key": "value"}')

        # Check for 4-space indentation
        assert "    " in result
