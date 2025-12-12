# Quick Start Guide

Get up and running with Ontonaut in 5 minutes!

## Installation

```bash
pip install ontonaut
```

## Your First Widget

### 1. CodeEditor - Interactive Code Execution

Create a Python code editor in your marimo notebook:

```python
import marimo as mo
from ontonaut import CodeEditor, PythonExecutor

# Create editor
editor = CodeEditor(
    executor=PythonExecutor(),
    code="# Try some Python\nx = 10\ny = 20\nresult = x + y",
    theme="light",
    language="python"
)

# Display in marimo
editor
```

**Try it:**
1. Edit the code
2. Click "Run" or press Cmd/Ctrl+Enter
3. See the result appear below!

### 2. ChatBot - Streaming AI Responses

Create a chatbot with the echo handler:

```python
import marimo as mo
from ontonaut import ChatBot, EchoHandler

# Create chatbot
chatbot = ChatBot(
    handler=EchoHandler(delay=0.03),
    placeholder="Type a message...",
    theme="light"
)

# Display in marimo
chatbot
```

**Try it:**
1. Type a message
2. Click "Run" or press Cmd/Ctrl+Enter
3. Watch it stream back!

## Next Steps

### Try Different Executors

```python
from ontonaut import (
    CodeEditor,
    PythonExecutor,
    JSONExecutor,
    CalculatorExecutor,
    RegexExecutor
)

# JSON formatter
json_editor = CodeEditor(
    executor=JSONExecutor(indent=2),
    code='{"name": "John", "age": 30}',
    language="json"
)

# Calculator
calc_editor = CodeEditor(
    executor=CalculatorExecutor(),
    code="x = 10\ny = 20\nx * y + 5",
    language="calculator"
)

# Regex tester
regex_editor = CodeEditor(
    executor=RegexExecutor(),
    code='pattern: \\d+\ntext: There are 42 apples',
    language="regex"
)
```

### Try Different Handlers

```python
from ontonaut import ChatBot, OpenAIHandler
import os

# OpenAI streaming (requires API key)
if os.getenv("OPENAI_API_KEY"):
    chatbot = ChatBot(
        handler=OpenAIHandler(
            model="gpt-4",
            system_prompt="You are a helpful assistant.",
            temperature=0.7
        ),
        theme="dark"
    )
    chatbot
```

### Custom Execution

Build your own executor:

```python
from ontonaut import CodeEditor

def my_executor(code: str) -> str:
    """Custom executor for your DSL"""
    if "hello" in code.lower():
        return "Hello back!"
    return f"You wrote: {code}"

editor = CodeEditor(
    executor=my_executor,
    code="hello world",
    language="custom"
)
```

### Custom Chat Handler

Build your own handler:

```python
from ontonaut import ChatBot

def my_handler(message: str):
    """Custom streaming handler"""
    import time

    response = f"You said: '{message}'. Here's my response!"

    for word in response.split():
        yield word + " "
        time.sleep(0.05)

chatbot = ChatBot(handler=my_handler)
```

## Themes

Both widgets support `theme="light"` or `theme="dark"`:

```python
# Light theme
editor_light = CodeEditor(executor=PythonExecutor(), theme="light")

# Dark theme
editor_dark = CodeEditor(executor=PythonExecutor(), theme="dark")

# Same for chatbot
chatbot_light = ChatBot(handler=EchoHandler(), theme="light")
chatbot_dark = ChatBot(handler=EchoHandler(), theme="dark")
```

## Configuration Options

### CodeEditor

```python
editor = CodeEditor(
    executor=my_executor,          # Required: execution backend
    code="initial code",            # Initial code content
    language="python",              # Language for syntax highlighting
    theme="light",                  # UI theme
    placeholder="Write code...",    # Placeholder text
    show_line_numbers=True,         # Show/hide line numbers
    read_only=False                 # Make editor read-only
)
```

### ChatBot

```python
chatbot = ChatBot(
    handler=my_handler,             # Required: chat handler
    input_text="",                  # Initial input
    placeholder="Ask me...",        # Placeholder text
    theme="light"                   # UI theme
)
```

## Common Patterns

### Execute Programmatically

```python
# CodeEditor
editor = CodeEditor(executor=PythonExecutor())
result = editor.execute("x = 10\nx * 2")
print(f"Result: {result}")  # 20

# ChatBot
chatbot = ChatBot(handler=EchoHandler())
chatbot.execute("Hello!")
print(chatbot.output)  # "Hello!"
```

### Clear Output

```python
# CodeEditor
editor.clear()  # Clears code, output, and errors

# ChatBot
chatbot.clear()      # Clears input and output
chatbot.clear_all()  # Also clears all tabs
```

### Access State

```python
# CodeEditor
print(editor.code)    # Current code
print(editor.output)  # Last output
print(editor.error)   # Last error (if any)

# ChatBot
print(chatbot.input_text)  # Current input
print(chatbot.output)      # Current output
print(len(chatbot.tabs))   # Number of history tabs
```

## What's Next?

- [CodeEditor Deep Dive](./code-editor.md)
- [ChatBot Deep Dive](./chatbot.md)
- [Build Custom Executors](./custom-executors.md)
- [Build Custom Handlers](./custom-handlers.md)
- [Styling Guide](./styling.md)

## Need Help?

- Check out [examples/](../../examples/)
- Read the [architecture docs](../../docs/)
- Browse [marimo notebooks](../marimo/)
- Open an issue on GitHub
