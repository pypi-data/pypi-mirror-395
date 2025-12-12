"""Basic usage examples for Ontonaut code editor."""

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from ontonaut import CodeEditor

    return CodeEditor, mo


@app.cell
def _(mo):
    mo.md(
        """
    # Ontonaut Code Editor Examples
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 1: Basic Python Executor
    """
    )
    return


@app.cell(hide_code=True)
def _(CodeEditor):
    # Create a simple Python executor
    editor1 = CodeEditor(
        code="# Calculate factorial\nn = 5\nresult = 1\nfor i in range(1, n + 1):\n    result *= i\nresult",
        language="python",
        executor=lambda code: eval(code),
    )
    editor1
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 2: Custom Math Language
    """
    )
    return


@app.cell
def _(CodeEditor):
    # Custom calculator executor
    def calc_executor(code: str) -> str:
        """Simple calculator that evaluates math expressions."""
        try:
            result = eval(code, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {e}"

    editor2 = CodeEditor(
        code="10 + 20 * 3", language="calculator", executor=calc_executor
    )
    editor2
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 3: JSON Formatter
    """
    )
    return


@app.cell
def _(CodeEditor):
    import json

    def json_executor(code: str) -> str:
        """Parse and pretty-print JSON."""
        try:
            data = json.loads(code)
            return json.dumps(data, indent=2)
        except json.JSONDecodeError as e:
            return f"Invalid JSON: {e}"

    editor3 = CodeEditor(
        code='{"name":"Alice","age":30,"city":"NYC"}',
        language="json",
        executor=json_executor,
        theme="dark",
    )
    editor3
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 4: Custom DSL - Todo Commands
    """
    )
    return


@app.cell
def _(CodeEditor):
    def todo_executor(code: str) -> str:
        """
        Execute todo list commands.

        Commands:
          ADD <task>
          LIST
          DONE <number>
        """
        todos = []
        output = []

        for line in code.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.startswith("ADD "):
                task = line[4:].strip()
                todos.append(task)
                output.append(f"✓ Added: {task}")
            elif line == "LIST":
                if todos:
                    output.append("Todo List:")
                    for i, task in enumerate(todos, 1):
                        output.append(f"  {i}. {task}")
                else:
                    output.append("No todos")
            elif line.startswith("DONE "):
                try:
                    num = int(line[5:].strip()) - 1
                    if 0 <= num < len(todos):
                        completed = todos.pop(num)
                        output.append(f"✓ Completed: {completed}")
                    else:
                        output.append("Invalid todo number")
                except ValueError:
                    output.append("Invalid todo number")
            else:
                output.append(f"Unknown command: {line}")

        return "\n".join(output)

    editor4 = CodeEditor(
        code="ADD Write documentation\nADD Write tests\nADD Deploy to production\nLIST",
        language="todo-dsl",
        executor=todo_executor,
    )
    editor4
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Creating Your Own Executor

    Simply define a function that takes a code string and returns a result:

    ```python
    def my_executor(code: str) -> Any:
        # Your custom logic here
        # Parse the code, execute it, return results
        return result

    editor = CodeEditor(
        code="your code here",
        language="mylang",
        executor=my_executor
    )
    ```
    """
    )
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
