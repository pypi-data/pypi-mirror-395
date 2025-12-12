"""Custom code executors for different languages and DSLs."""

import ast
import json
import re
from typing import Any, Callable, Optional


class BaseExecutor:
    """
    Base class for code executors.

    Custom executors should inherit from this class and implement
    the execute method.
    """

    def execute(self, code: str) -> Any:
        """
        Execute code and return the result.

        Args:
            code: Code string to execute

        Returns:
            Execution result

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def __call__(self, code: str) -> Any:
        """Allow executor to be called as a function."""
        return self.execute(code)


class PythonExecutor(BaseExecutor):
    """
    Python code executor with optional globals and locals.

    Examples:
        >>> executor = PythonExecutor()
        >>> result = executor.execute("2 + 2")
        >>> print(result)
        4
        >>>
        >>> # With custom globals
        >>> executor = PythonExecutor(globals_dict={"x": 10})
        >>> result = executor.execute("x * 2")
        >>> print(result)
        20
    """

    def __init__(
        self,
        globals_dict: Optional[dict[str, Any]] = None,
        locals_dict: Optional[dict[str, Any]] = None,
        safe_mode: bool = False,
    ) -> None:
        """
        Initialize Python executor.

        Args:
            globals_dict: Global variables to inject
            locals_dict: Local variables to inject
            safe_mode: If True, restrict dangerous operations (experimental)
        """
        self.globals_dict = globals_dict or {}
        self.locals_dict = locals_dict or {}
        self.safe_mode = safe_mode

    def execute(self, code: str) -> Any:
        """
        Execute Python code.

        Args:
            code: Python code to execute

        Returns:
            Result of the last expression, or None
        """
        if self.safe_mode:
            # Basic AST check for dangerous operations
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        raise SecurityError("Imports not allowed in safe mode")
            except SyntaxError:
                pass  # Will be caught by exec

        # Try to eval first (for expressions)
        try:
            return eval(code, self.globals_dict, self.locals_dict)
        except SyntaxError:
            # If it's not an expression, exec it
            exec(code, self.globals_dict, self.locals_dict)
            return None


class JSONExecutor(BaseExecutor):
    """
    JSON validator and pretty-printer.

    Examples:
        >>> executor = JSONExecutor()
        >>> result = executor.execute('{"name": "Alice", "age": 30}')
        >>> print(result)
        {
          "name": "Alice",
          "age": 30
        }
    """

    def __init__(self, indent: int = 2) -> None:
        """
        Initialize JSON executor.

        Args:
            indent: Number of spaces for indentation
        """
        self.indent = indent

    def execute(self, code: str) -> str:
        """
        Parse and pretty-print JSON.

        Args:
            code: JSON string

        Returns:
            Pretty-printed JSON string
        """
        data = json.loads(code)
        return json.dumps(data, indent=self.indent)


class CalculatorExecutor(BaseExecutor):
    """
    Simple calculator DSL executor.

    Supports basic arithmetic and variables.

    Examples:
        >>> executor = CalculatorExecutor()
        >>> result = executor.execute("x = 10\\ny = 20\\nx + y")
        >>> print(result)
        30
    """

    def __init__(self) -> None:
        """Initialize calculator with empty variable store."""
        self.variables: dict[str, float] = {}

    def execute(self, code: str) -> Any:
        """
        Execute calculator code.

        Args:
            code: Calculator code (one statement per line)

        Returns:
            Result of the last expression
        """
        result = None
        for line in code.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Assignment: x = 10
            if "=" in line and not any(op in line for op in ["==", "!=", "<=", ">="]):
                var_name, expr = line.split("=", 1)
                var_name = var_name.strip()
                value = self._evaluate(expr.strip())
                self.variables[var_name] = value
                result = value
            else:
                # Expression
                result = self._evaluate(line)

        return result

    def _evaluate(self, expr: str) -> float:
        """
        Evaluate a mathematical expression.

        Args:
            expr: Expression to evaluate

        Returns:
            Numeric result
        """
        # Replace variables
        for var_name, value in self.variables.items():
            expr = re.sub(r"\b" + var_name + r"\b", str(value), expr)

        # Safe eval for math
        try:
            result: float = float(eval(expr, {"__builtins__": {}}, {}))
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {expr}") from e


class RegexExecutor(BaseExecutor):
    """
    Regex pattern tester.

    Tests regex patterns against input text.

    Examples:
        >>> executor = RegexExecutor()
        >>> result = executor.execute("pattern: \\\\d+\\ntext: I have 42 apples")
        >>> print(result)
        Matches: ['42']
    """

    def execute(self, code: str) -> str:
        """
        Test regex pattern.

        Expected format:
            pattern: <regex>
            text: <text to match>

        Args:
            code: Pattern and text specification

        Returns:
            Match results
        """
        lines = code.strip().split("\n")
        pattern = None
        text = None

        for line in lines:
            if line.startswith("pattern:"):
                pattern = line.split("pattern:", 1)[1].strip()
            elif line.startswith("text:"):
                text = line.split("text:", 1)[1].strip()

        if not pattern or not text:
            return "Error: Must specify both 'pattern:' and 'text:'"

        try:
            matches = re.findall(pattern, text)
            if matches:
                return f"Matches: {matches}"
            else:
                return "No matches found"
        except re.error as e:
            return f"Invalid regex: {e}"


def create_executor(
    language: str,
    **kwargs: Any,
) -> Callable[[str], Any]:
    """
    Create an executor for a given language.

    Args:
        language: Language name ('python', 'json', 'calculator', 'regex')
        **kwargs: Additional arguments passed to the executor

    Returns:
        Executor function

    Examples:
        >>> executor = create_executor('python')
        >>> result = executor("2 + 2")
        >>> print(result)
        4
        >>>
        >>> executor = create_executor('json', indent=4)
        >>> result = executor('{"key": "value"}')
    """
    executors = {
        "python": PythonExecutor,
        "json": JSONExecutor,
        "calculator": CalculatorExecutor,
        "regex": RegexExecutor,
    }

    executor_class = executors.get(language.lower())
    if not executor_class:
        raise ValueError(
            f"Unknown language: {language}. "
            f"Supported: {', '.join(executors.keys())}"
        )

    instance = executor_class(**kwargs)
    return instance  # type: ignore[no-any-return]


class SecurityError(Exception):
    """Raised when potentially dangerous code is detected."""

    pass
