# Ontonaut Architecture Documentation

This directory contains comprehensive architecture documentation for developers and AI assistants working on Ontonaut.

## 📚 Documentation Files

### Core Architecture
- **[architecture.md](./architecture.md)** - Overall system architecture
- **[widget-system.md](./widget-system.md)** - anywidget integration and patterns
- **[frontend.md](./frontend.md)** - JavaScript/CSS frontend architecture
- **[state-management.md](./state-management.md)** - Python-JS state synchronization

### Components
- **[code-editor-internals.md](./code-editor-internals.md)** - CodeEditor implementation
- **[chatbot-internals.md](./chatbot-internals.md)** - ChatBot implementation
- **[executors-internals.md](./executors-internals.md)** - Executor system design
- **[handlers-internals.md](./handlers-internals.md)** - Handler system design

### Development
- **[development-setup.md](./development-setup.md)** - Dev environment setup
- **[testing-strategy.md](./testing-strategy.md)** - Testing approach
- **[build-system.md](./build-system.md)** - Build and packaging
- **[contributing.md](./contributing.md)** - Contribution guidelines

## 🎯 Purpose

This documentation serves multiple audiences:

### For Developers
- Understand the codebase structure
- Learn implementation patterns
- Make informed architectural decisions
- Debug issues effectively

### For AI Assistants
- Context for implementing new features
- Patterns to follow when generating code
- Understanding of design decisions
- Bug fixing guidance

### For Contributors
- How to add new widgets
- How to extend existing functionality
- Testing requirements
- Code style and conventions

## 🏗️ High-Level Overview

```
ontonaut/
├── src/ontonaut/          # Python package
│   ├── editor.py          # CodeEditor widget
│   ├── chatbot.py         # ChatBot widget
│   ├── executors.py       # Code execution backends
│   ├── handlers.py        # Chat handlers
│   └── static/            # Frontend assets
│       ├── editor.js      # CodeEditor JS
│       ├── editor.css     # CodeEditor CSS
│       ├── chatbot.js     # ChatBot JS
│       └── chatbot.css    # ChatBot CSS
├── tests/                 # Test suite
├── examples/              # Usage examples
├── book/                  # Documentation
│   ├── markdown/          # User guides
│   └── marimo/            # Interactive notebooks
└── docs/                  # Architecture docs (you are here)
```

## 🔑 Key Concepts

### anywidget Pattern
Ontonaut uses `anywidget` to create Jupyter/marimo widgets:
- Python class defines widget state (traitlets)
- JavaScript renders the UI
- State syncs bidirectionally between Python and JS

### Widget Lifecycle
1. **Initialization**: Python creates widget with initial state
2. **Rendering**: JS receives state and creates DOM
3. **Interaction**: User interacts with UI
4. **Sync**: Changes flow Python ↔ JS via traitlets
5. **Execution**: Backend logic runs in Python
6. **Update**: Results flow back to JS for display

### Pluggable Architecture
- **Executors**: Pluggable code execution backends
- **Handlers**: Pluggable chat response generators
- **Themes**: Light/dark mode support
- **Languages**: Syntax highlighting for any language

## 📖 Reading Order

### For New Developers
1. [architecture.md](./architecture.md) - Start here
2. [widget-system.md](./widget-system.md) - Understand anywidget
3. [code-editor-internals.md](./code-editor-internals.md) - Learn by example
4. [development-setup.md](./development-setup.md) - Get coding

### For Feature Implementation
1. [architecture.md](./architecture.md) - System overview
2. Relevant component docs (editor/chatbot/executors/handlers)
3. [testing-strategy.md](./testing-strategy.md) - Test requirements
4. [contributing.md](./contributing.md) - Guidelines

### For Bug Fixing
1. Relevant component docs
2. [state-management.md](./state-management.md) - If state-related
3. [frontend.md](./frontend.md) - If UI-related
4. [testing-strategy.md](./testing-strategy.md) - Add regression test

## 🎨 Design Principles

### 1. Simplicity
- Clean, minimal APIs
- Sensible defaults
- Easy to use, powerful when needed

### 2. Consistency
- Similar patterns across widgets
- Predictable behavior
- Uniform styling

### 3. Extensibility
- Easy to add executors/handlers
- Pluggable architecture
- No need to modify core code

### 4. Type Safety
- Full type hints
- Runtime validation
- IDE support

### 5. Performance
- Fast initial render
- Efficient updates
- Smooth streaming

## 🔧 Common Tasks

### Adding a New Executor
See [executors-internals.md](./executors-internals.md)

### Adding a New Handler
See [handlers-internals.md](./handlers-internals.md)

### Adding a New Widget
See [widget-system.md](./widget-system.md)

### Modifying UI
See [frontend.md](./frontend.md)

### Adding Tests
See [testing-strategy.md](./testing-strategy.md)

## 🐛 Debugging Guide

### Widget Not Rendering
1. Check browser console for JS errors
2. Verify anywidget ESM export format
3. Check static file paths
4. Rebuild package: `make build`

### State Not Syncing
1. Verify traitlet `.tag(sync=True)`
2. Check `model.on("change:attr")` listeners
3. Verify `model.save_changes()` calls
4. See [state-management.md](./state-management.md)

### Streaming Issues
1. Check generator yields strings
2. Verify no blocking operations
3. Check `is_streaming` state management
4. See [chatbot-internals.md](./chatbot-internals.md)

### Type Errors
1. Check type hints match usage
2. Run `make lint` for mypy errors
3. Add `# type: ignore` with comment if needed
4. Update type stubs if using optional deps

## 📊 Metrics

### Test Coverage
Target: >85% coverage
- Unit tests for all executors/handlers
- Widget integration tests
- UI interaction tests

### Performance
- Initial render: <100ms
- Execution latency: <50ms overhead
- Streaming: 60fps smooth animation

### Code Quality
- Mypy strict mode
- Ruff linting
- Black formatting
- Pre-commit hooks

## 🚀 Release Process

See [contributing.md](./contributing.md) for:
- Version bumping
- Changelog updates
- Testing checklist
- PyPI publishing

## 📝 Documentation Standards

### Code Comments
- Document why, not what
- Explain non-obvious decisions
- Link to relevant docs/issues

### Docstrings
- Google style docstrings
- Include Args, Returns, Raises
- Provide usage examples

### Type Hints
- All public APIs fully typed
- Use modern typing (e.g., `list[str]` not `List[str]`)
- Document complex types

## 🤝 Getting Help

- Read relevant architecture docs
- Check examples in `examples/`
- Review tests in `tests/`
- Open an issue on GitHub

## 🔄 Keeping Documentation Updated

When making changes:
1. Update relevant architecture docs
2. Update user guides if needed
3. Add/update examples
4. Update this README if structure changes

This documentation is living and should evolve with the codebase.
