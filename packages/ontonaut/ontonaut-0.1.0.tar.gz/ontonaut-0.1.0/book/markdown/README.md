# Ontonaut Documentation

Welcome to the Ontonaut documentation! This guide covers all widgets and their usage.

## 📚 Table of Contents

### Widgets
- [CodeEditor](./code-editor.md) - Interactive code editor with custom execution
- [ChatBot](./chatbot.md) - Streaming AI chatbot with custom handlers

### Components
- [Executors](./executors.md) - Code execution backends (Python, JSON, Calculator, Regex)
- [Handlers](./handlers.md) - Chat handlers (Echo, OpenAI, Anthropic, MCP, Custom)

### Guides
- [Quick Start](./quick-start.md) - Get up and running in 5 minutes
- [Custom Executors](./custom-executors.md) - Build your own code executors
- [Custom Handlers](./custom-handlers.md) - Build your own chat handlers
- [Styling & Themes](./styling.md) - Customize widget appearance

## 🎯 What is Ontonaut?

Ontonaut is a Python package that provides **marimo-compatible interactive widgets** built with `anywidget`. It enables:

- **Custom code execution** with pluggable backends
- **AI streaming interfaces** with customizable handlers
- **Beautiful, modern UI** matching marimo's aesthetic
- **Type-safe APIs** with full IDE support

## 🚀 Quick Example

### CodeEditor
```python
from ontonaut import CodeEditor, PythonExecutor

editor = CodeEditor(
    executor=PythonExecutor(),
    code="x = 10\nresult = x * 2",
    theme="dark"
)
editor
```

### ChatBot
```python
from ontonaut import ChatBot, EchoHandler

chatbot = ChatBot(
    handler=EchoHandler(),
    placeholder="Ask me anything...",
    theme="dark"
)
chatbot
```

## 📦 Installation

```bash
pip install ontonaut
```

For development:
```bash
git clone https://github.com/yourusername/ontonaut.git
cd ontonaut
make setup
```

## 🎨 Features

### CodeEditor
- ✅ Syntax highlighting
- ✅ Line numbers
- ✅ Multiple language support
- ✅ Custom execution backends
- ✅ Real-time error handling
- ✅ Light/dark themes

### ChatBot
- ✅ Streaming responses
- ✅ Automatic tab creation
- ✅ Code formatting in output
- ✅ Custom AI handlers
- ✅ OpenAI/Anthropic integration
- ✅ MCP server support

## 🔗 Links

- [GitHub Repository](https://github.com/yourusername/ontonaut)
- [Examples](../../examples/)
- [Architecture Docs](../../docs/)
- [Marimo Notebooks](../marimo/)

## 📝 License

MIT License - See [LICENSE](../../LICENSE) for details.
