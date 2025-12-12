# Executors Reference

Executors are the backend engines that power the `CodeEditor` widget. They take code as a string and return execution results.

## Overview

```python
from ontonaut import CodeEditor, PythonExecutor

executor = PythonExecutor()
editor = CodeEditor(executor=executor)
```

## Built-in Executors

### PythonExecutor

Execute Python code with `eval()` or `exec()`.

**Usage:**

```python
from ontonaut import PythonExecutor

# Basic usage
executor = PythonExecutor()
result = executor("x = 10\ny = 20\nresult = x + y")  # Returns: 30

# With custom globals
import math
executor = PythonExecutor(globals_dict={"math": math})
result = executor("math.sqrt(16)")  # Returns: 4.0

# With custom locals
executor = PythonExecutor(locals_dict={"pi": 3.14159})
result = executor("result = pi * 2")  # Returns: 6.28318
```

**Constructor:**

```python
PythonExecutor(
    globals_dict: Optional[dict] = None,  # Custom global variables
    locals_dict: Optional[dict] = None     # Custom local variables
)
```

**Behavior:**
- Single expressions: Uses `eval()` - returns the value
- Multi-line code: Uses `exec()` - returns `result` variable
- Supports variables across executions
- Safe by default (no dangerous builtins)

**Example:**

```python
executor = PythonExecutor()

# Expression
executor("2 + 2")  # 4

# Multi-line
executor("""
x = 10
y = 20
result = x * y
""")  # 200

# With imports
import math
executor = PythonExecutor(globals_dict={"math": math})
executor("math.factorial(5)")  # 120
```

---

### JSONExecutor

Format and validate JSON strings.

**Usage:**

```python
from ontonaut import JSONExecutor

# Basic usage
executor = JSONExecutor()
result = executor('{"name":"John","age":30}')
# Returns pretty-formatted JSON

# Custom indentation
executor = JSONExecutor(indent=4)
result = executor('{"a":1,"b":2}')
```

**Constructor:**

```python
JSONExecutor(
    indent: int = 2  # Indentation level
)
```

**Behavior:**
- Parses JSON string
- Validates syntax
- Returns pretty-formatted JSON
- Shows error if invalid

**Example:**

```python
executor = JSONExecutor(indent=2)

# Valid JSON
result = executor('{"name": "Alice", "age": 30}')
print(result)
# {
#   "name": "Alice",
#   "age": 30
# }

# Invalid JSON
result = executor('{invalid}')
# Returns error message
```

---

### CalculatorExecutor

Simple calculator with variable support.

**Usage:**

```python
from ontonaut import CalculatorExecutor

executor = CalculatorExecutor()

# Simple math
executor("2 + 2")  # 4.0

# With variables
executor("x = 10\ny = 20\nx * y")  # 200.0

# Complex expressions
executor("(5 + 3) * 2 - 1")  # 15.0
```

**Constructor:**

```python
CalculatorExecutor()  # No parameters
```

**Behavior:**
- Supports: `+`, `-`, `*`, `/`, `**`, `()`, `%`
- Variable assignment: `x = 10`
- Comments: `# comment`
- Variables persist across executions
- Returns float result

**Example:**

```python
executor = CalculatorExecutor()

# Basic arithmetic
executor("10 + 5 * 2")  # 20.0

# Variables
executor("""
price = 100
tax = 0.08
total = price * (1 + tax)
""")  # 108.0

# Using previous variables
executor("total * 2")  # 216.0
```

---

### RegexExecutor

Test regular expressions against text.

**Usage:**

```python
from ontonaut import RegexExecutor

executor = RegexExecutor()

code = """
pattern: \\d+
text: There are 42 apples
"""

result = executor(code)
# Returns: "Matches: ['42']"
```

**Constructor:**

```python
RegexExecutor()  # No parameters
```

**Behavior:**
- Expects `pattern:` and `text:` lines
- Finds all matches
- Returns list of matches
- Shows error if invalid regex

**Format:**

```
pattern: <regex_pattern>
text: <text_to_match>
```

**Example:**

```python
executor = RegexExecutor()

# Find numbers
result = executor("""
pattern: \\d+
text: Phone: 555-1234
""")
# "Matches: ['555', '1234']"

# Find emails
result = executor("""
pattern: [a-z]+@[a-z]+\\.[a-z]+
text: Contact: user@example.com
""")
# "Matches: ['user@example.com']"

# No matches
result = executor("""
pattern: \\d+
text: No numbers here
""")
# "No matches found"
```

## Creating Custom Executors

### Function-based Executor

Simple function that takes code and returns result:

```python
def my_executor(code: str) -> str:
    """Custom executor for your DSL."""
    # Your logic here
    if "hello" in code.lower():
        return "Hello back!"
    return f"You wrote: {code}"

# Use it
from ontonaut import CodeEditor
editor = CodeEditor(executor=my_executor)
```

### Class-based Executor

More complex executor with state:

```python
class SQLExecutor:
    """Execute SQL queries."""

    def __init__(self, connection_string: str):
        import sqlite3
        self.conn = sqlite3.connect(connection_string)

    def __call__(self, code: str) -> str:
        """Execute SQL query."""
        try:
            cursor = self.conn.execute(code)
            rows = cursor.fetchall()
            return self._format_results(rows)
        except Exception as e:
            return f"Error: {e}"

    def _format_results(self, rows):
        if not rows:
            return "No results"
        return "\\n".join(str(row) for row in rows)

# Use it
executor = SQLExecutor(":memory:")
editor = CodeEditor(executor=executor, language="sql")
```

### With Dependencies

```python
class MarkdownExecutor:
    """Convert markdown to HTML."""

    def __init__(self):
        try:
            import markdown
            self.md = markdown.Markdown()
        except ImportError:
            raise ImportError("pip install markdown")

    def __call__(self, code: str) -> str:
        return self.md.convert(code)

# Use it
executor = MarkdownExecutor()
editor = CodeEditor(executor=executor, language="markdown")
```

## Executor Pattern

All executors follow this pattern:

```python
# Function signature
def executor(code: str) -> Any:
    """Execute code and return result."""
    # Your logic
    return result

# Or class with __call__
class MyExecutor:
    def __call__(self, code: str) -> Any:
        return result
```

**Requirements:**
- Must accept single `str` parameter (the code)
- Should return a value (Any type)
- Should handle exceptions internally (recommended)
- Can maintain state between calls (if class)

## Best Practices

### 1. Error Handling

Always catch and return errors gracefully:

```python
def safe_executor(code: str) -> str:
    try:
        result = eval(code)
        return str(result)
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"
```

### 2. Input Validation

Validate input before execution:

```python
def validated_executor(code: str) -> str:
    if not code.strip():
        return "Empty input"

    if len(code) > 1000:
        return "Code too long (max 1000 chars)"

    # Execute
    return execute(code)
```

### 3. Timeouts

Add timeouts for long-running code:

```python
import signal

def timeout_executor(code: str, timeout: int = 5) -> str:
    def handler(signum, frame):
        raise TimeoutError("Execution timeout")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)

    try:
        result = eval(code)
        signal.alarm(0)
        return str(result)
    except TimeoutError:
        return "Execution timeout"
    except Exception as e:
        signal.alarm(0)
        return f"Error: {e}"
```

### 4. Sandboxing

Restrict dangerous operations:

```python
def sandboxed_executor(code: str) -> str:
    # Restricted globals
    safe_globals = {
        "__builtins__": {
            "abs": abs,
            "max": max,
            "min": min,
            "sum": sum,
            # Add safe functions only
        }
    }

    try:
        result = eval(code, safe_globals, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"
```

### 5. Type Conversion

Always convert results to strings:

```python
def typed_executor(code: str) -> str:
    result = eval(code)

    if isinstance(result, (list, dict)):
        import json
        return json.dumps(result, indent=2)

    return str(result)
```

## Advanced Examples

### Multi-language Executor

```python
class MultiLanguageExecutor:
    """Execute multiple languages."""

    def __call__(self, code: str) -> str:
        # Detect language from first line
        if code.startswith("# python"):
            return self._exec_python(code)
        elif code.startswith("// javascript"):
            return self._exec_js(code)
        else:
            return "Unknown language. Start with # python or // javascript"

    def _exec_python(self, code: str) -> str:
        # Remove language comment
        code = "\\n".join(code.split("\\n")[1:])
        return str(eval(code))

    def _exec_js(self, code: str) -> str:
        import subprocess
        result = subprocess.run(
            ["node", "-e", code],
            capture_output=True,
            text=True
        )
        return result.stdout
```

### Cached Executor

```python
from functools import lru_cache

class CachedExecutor:
    """Cache execution results."""

    @lru_cache(maxsize=100)
    def __call__(self, code: str) -> str:
        # Expensive computation
        result = complex_evaluation(code)
        return str(result)
```

### Logging Executor

```python
import logging

class LoggingExecutor:
    """Log all executions."""

    def __init__(self, base_executor):
        self.base_executor = base_executor
        self.logger = logging.getLogger(__name__)

    def __call__(self, code: str) -> str:
        self.logger.info(f"Executing: {code[:50]}...")

        try:
            result = self.base_executor(code)
            self.logger.info(f"Result: {str(result)[:50]}...")
            return result
        except Exception as e:
            self.logger.error(f"Error: {e}")
            raise
```

## Testing Executors

Always test your executors:

```python
def test_my_executor():
    executor = MyExecutor()

    # Test basic execution
    assert executor("2 + 2") == "4"

    # Test error handling
    result = executor("invalid code")
    assert "Error" in result

    # Test edge cases
    assert executor("") == "Empty input"

    print("All tests passed!")
```

## See Also

- [CodeEditor Widget](./code-editor.md)
- [Custom Executors Guide](./custom-executors.md)
- [Examples](../../examples/basic_usage.py)
