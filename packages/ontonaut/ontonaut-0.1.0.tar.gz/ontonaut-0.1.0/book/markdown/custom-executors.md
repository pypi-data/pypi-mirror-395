# Building Custom Executors

Learn how to build custom executors for the `CodeEditor` widget to support your own languages, DSLs, or execution logic.

## Quick Start

```python
from ontonaut import CodeEditor

def my_executor(code: str) -> str:
    """Execute my custom DSL."""
    # Your logic here
    return f"Result: {code.upper()}"

editor = CodeEditor(executor=my_executor)
```

## Pattern

All executors follow this simple pattern:

```python
def executor(code: str) -> Any:
    """
    Execute code and return result.

    Args:
        code: The code string to execute

    Returns:
        Execution result (any type, will be converted to string for display)
    """
    # Your execution logic here
    result = process(code)
    return result
```

## Examples

### Example 1: Simple DSL

```python
def greeting_dsl(code: str) -> str:
    """Execute greeting DSL.

    Syntax:
        greet NAME
        farewell NAME
    """
    lines = code.strip().split("\\n")
    results = []

    for line in lines:
        parts = line.split()

        if len(parts) != 2:
            results.append(f"Invalid syntax: {line}")
            continue

        command, name = parts

        if command == "greet":
            results.append(f"Hello, {name}!")
        elif command == "farewell":
            results.append(f"Goodbye, {name}!")
        else:
            results.append(f"Unknown command: {command}")

    return "\\n".join(results)

# Use it
from ontonaut import CodeEditor

editor = CodeEditor(
    executor=greeting_dsl,
    code="greet Alice\\nfarewell Bob",
    language="dsl"
)
```

### Example 2: Math Expression Evaluator

```python
import ast
import operator

class SafeMathExecutor:
    """Safe mathematical expression evaluator."""

    ALLOWED_OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def __call__(self, code: str) -> str:
        """Evaluate math expression."""
        try:
            tree = ast.parse(code, mode='eval')
            result = self._eval(tree.body)
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    def _eval(self, node):
        """Recursively evaluate AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            op = self.ALLOWED_OPS.get(type(node.op))
            if not op:
                raise ValueError(f"Operation not allowed: {node.op}")
            left = self._eval(node.left)
            right = self._eval(node.right)
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            op = self.ALLOWED_OPS.get(type(node.op))
            if not op:
                raise ValueError(f"Operation not allowed: {node.op}")
            operand = self._eval(node.operand)
            return op(operand)
        else:
            raise ValueError(f"Node type not allowed: {type(node)}")

# Use it
editor = CodeEditor(
    executor=SafeMathExecutor(),
    code="(5 + 3) * 2 - 1",
    language="math"
)
```

### Example 3: SQL Query Executor

```python
import sqlite3
from typing import List, Tuple

class SQLiteExecutor:
    """Execute SQL queries against SQLite database."""

    def __init__(self, database: str = ":memory:"):
        """
        Initialize SQLite executor.

        Args:
            database: Database path or ":memory:" for in-memory DB
        """
        self.conn = sqlite3.connect(database)
        self._init_demo_data()

    def _init_demo_data(self):
        """Create demo tables."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)
        cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'Alice', 30)")
        cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'Bob', 25)")
        self.conn.commit()

    def __call__(self, code: str) -> str:
        """Execute SQL query."""
        try:
            cursor = self.conn.execute(code)

            # Handle SELECT queries
            if code.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                return self._format_table(rows, cursor.description)

            # Handle modifications
            self.conn.commit()
            return f"Query executed. {cursor.rowcount} rows affected."

        except Exception as e:
            return f"SQL Error: {e}"

    def _format_table(self, rows: List[Tuple], description) -> str:
        """Format query results as table."""
        if not rows:
            return "No results"

        # Get column names
        cols = [desc[0] for desc in description]

        # Build table
        header = " | ".join(cols)
        separator = "-" * len(header)
        lines = [header, separator]

        for row in rows:
            line = " | ".join(str(val) for val in row)
            lines.append(line)

        return "\\n".join(lines)

# Use it
editor = CodeEditor(
    executor=SQLiteExecutor(),
    code="SELECT * FROM users WHERE age > 25",
    language="sql"
)
```

### Example 4: Template Engine

```python
import re

class TemplateExecutor:
    """Simple template engine executor."""

    def __init__(self):
        self.variables = {}

    def __call__(self, code: str) -> str:
        """
        Execute template code.

        Syntax:
            set name = value
            render template with {{variables}}
        """
        lines = code.strip().split("\\n")
        results = []

        for line in lines:
            if line.startswith("set "):
                # Variable assignment
                match = re.match(r"set (\\w+) = (.+)", line)
                if match:
                    var, value = match.groups()
                    self.variables[var] = value.strip()
                    results.append(f"Set {var} = {value}")

            elif line.startswith("render "):
                # Template rendering
                template = line[7:]  # Remove "render "
                rendered = self._render_template(template)
                results.append(rendered)

            else:
                results.append(f"Unknown command: {line}")

        return "\\n".join(results)

    def _render_template(self, template: str) -> str:
        """Render template with variables."""
        def replace_var(match):
            var = match.group(1)
            return self.variables.get(var, f"{{{{var}}}}}")

        return re.sub(r"{{(\\w+)}}", replace_var, template)

# Use it
code = """
set name = Alice
set greeting = Hello
render {{greeting}}, {{name}}!
"""

editor = CodeEditor(
    executor=TemplateExecutor(),
    code=code,
    language="template"
)
```

### Example 5: HTTP Request Executor

```python
import requests
import json

class HTTPExecutor:
    """Execute HTTP requests."""

    def __call__(self, code: str) -> str:
        """
        Execute HTTP request.

        Syntax:
            GET https://api.example.com/data
            POST https://api.example.com/data
            {"key": "value"}
        """
        lines = code.strip().split("\\n")

        if not lines:
            return "Empty request"

        # Parse first line (method and URL)
        first_line = lines[0].split()
        if len(first_line) != 2:
            return "Invalid syntax. Use: METHOD URL"

        method, url = first_line

        # Parse body (if any)
        body = None
        if len(lines) > 1:
            try:
                body = json.loads("\\n".join(lines[1:]))
            except json.JSONDecodeError as e:
                return f"Invalid JSON body: {e}"

        # Execute request
        try:
            if method.upper() == "GET":
                response = requests.get(url)
            elif method.upper() == "POST":
                response = requests.post(url, json=body)
            elif method.upper() == "PUT":
                response = requests.put(url, json=body)
            elif method.upper() == "DELETE":
                response = requests.delete(url)
            else:
                return f"Unknown method: {method}"

            # Format response
            result = f"Status: {response.status_code}\\n"
            result += f"Headers: {dict(response.headers)}\\n\\n"

            try:
                result += json.dumps(response.json(), indent=2)
            except:
                result += response.text

            return result

        except Exception as e:
            return f"Request failed: {e}"

# Use it
editor = CodeEditor(
    executor=HTTPExecutor(),
    code='GET https://api.github.com/users/octocat',
    language="http"
)
```

## Best Practices

### 1. Error Handling

Always catch and return errors gracefully:

```python
def robust_executor(code: str) -> str:
    try:
        result = execute_code(code)
        return str(result)
    except ValueError as e:
        return f"Value Error: {e}"
    except TypeError as e:
        return f"Type Error: {e}"
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"
```

### 2. Input Validation

Validate input before processing:

```python
def validated_executor(code: str) -> str:
    # Check empty
    if not code.strip():
        return "Error: Empty input"

    # Check length
    if len(code) > 10000:
        return "Error: Code too long (max 10000 chars)"

    # Check syntax
    if not is_valid_syntax(code):
        return "Error: Invalid syntax"

    # Execute
    return execute(code)
```

### 3. Provide Helpful Messages

Guide users with clear output:

```python
def helpful_executor(code: str) -> str:
    if not code.strip():
        return """No code provided.

Example usage:
    command arg1 arg2
"""

    try:
        return execute(code)
    except Exception as e:
        return f"""Error: {e}

Syntax:
    command arg1 arg2

Examples:
    greet Alice
    farewell Bob
"""
```

### 4. State Management

Use classes for stateful executors:

```python
class StatefulExecutor:
    \"\"\"Executor with persistent state.\"\"\"

    def __init__(self):
        self.variables = {}
        self.history = []

    def __call__(self, code: str) -> str:
        \"\"\"Execute with state.\"\"\"
        # Add to history
        self.history.append(code)

        # Execute
        result = self._execute(code)

        # Return with context
        return f\"Result: {result}\\nVariables: {self.variables}\"

    def _execute(self, code: str):
        # Your logic using self.variables
        pass
```

### 5. Documentation

Document your executor well:

```python
def my_executor(code: str) -> str:
    \"\"\"
    Execute MyLanguage code.

    Syntax:
        command arg1 arg2 ...

    Commands:
        greet NAME      - Greet someone
        farewell NAME   - Say goodbye
        calc EXPR       - Calculate expression

    Examples:
        greet Alice
        farewell Bob
        calc 2 + 2

    Args:
        code: MyLanguage code to execute

    Returns:
        Execution result as string

    Raises:
        No exceptions - all errors returned as strings
    \"\"\"
    # Implementation
    pass
```

## Testing

Always test your executors:

```python
def test_my_executor():
    executor = MyExecutor()

    # Test valid input
    assert executor("valid code") == "expected output"

    # Test error handling
    result = executor("invalid")
    assert "Error" in result

    # Test edge cases
    assert executor("") == "Empty input"
    assert executor("a" * 10001) == "Code too long"

    # Test with CodeEditor
    from ontonaut import CodeEditor
    editor = CodeEditor(executor=executor, code="test")
    editor.execute()
    assert editor.output != ""

    print("✅ All tests passed!")

test_my_executor()
```

## Tips

1. **Start simple** - Build basic version first, add features later
2. **Handle errors** - Never let exceptions crash the widget
3. **Provide examples** - Show users how to use your DSL
4. **Test thoroughly** - Test edge cases and errors
5. **Document well** - Clear docstrings and error messages
6. **Consider state** - Use classes if you need persistent state
7. **Be performant** - Optimize for fast execution

## See Also

- [Executors Reference](./executors.md)
- [CodeEditor Widget](./code-editor.md)
- [Examples](../../examples/basic_usage.py)
