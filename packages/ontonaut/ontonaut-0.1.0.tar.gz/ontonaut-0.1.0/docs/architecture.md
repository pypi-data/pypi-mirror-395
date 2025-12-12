# Ontonaut Architecture

Complete architectural overview of the Ontonaut package.

## System Overview

Ontonaut is a Python package providing interactive widgets for marimo notebooks. It uses `anywidget` to create bidirectional Python-JavaScript widgets with pluggable backends.

```
┌─────────────────────────────────────────────────────────┐
│                    Marimo Notebook                       │
│  ┌───────────────┐              ┌───────────────┐      │
│  │  CodeEditor   │              │   ChatBot     │      │
│  │   Widget      │              │    Widget     │      │
│  └───────┬───────┘              └───────┬───────┘      │
│          │                              │              │
│          │                              │              │
└──────────┼──────────────────────────────┼──────────────┘
           │                              │
           │ anywidget                    │ anywidget
           │                              │
┌──────────┼──────────────────────────────┼──────────────┐
│          ▼                              ▼              │
│    Python Backend                 Python Backend       │
│  ┌─────────────────┐         ┌─────────────────┐     │
│  │   Executors     │         │    Handlers     │     │
│  │  - Python       │         │  - Echo         │     │
│  │  - JSON         │         │  - OpenAI       │     │
│  │  - Calculator   │         │  - Anthropic    │     │
│  │  - Regex        │         │  - MCP          │     │
│  │  - Custom       │         │  - Custom       │     │
│  └─────────────────┘         └─────────────────┘     │
└──────────────────────────────────────────────────────┘
           │                              │
           │                              │
┌──────────┼──────────────────────────────┼──────────────┐
│          ▼                              ▼              │
│    JavaScript Frontend          JavaScript Frontend    │
│  ┌─────────────────┐         ┌─────────────────┐     │
│  │  editor.js      │         │  chatbot.js     │     │
│  │  editor.css     │         │  chatbot.css    │     │
│  └─────────────────┘         └─────────────────┘     │
└──────────────────────────────────────────────────────┘
```

## Core Components

### 1. Widget Layer (Python)

#### CodeEditor (`src/ontonaut/editor.py`)
- Inherits from `anywidget.AnyWidget`
- Defines state with `traitlets`
- Manages code execution
- Handles executor interface

**Key Responsibilities:**
- State management (code, output, error)
- Executor validation and invocation
- Error handling and formatting
- Bidirectional sync with JS

#### ChatBot (`src/ontonaut/chatbot.py`)
- Inherits from `anywidget.AnyWidget`
- Manages chat state and history
- Handles streaming responses
- Manages tab creation

**Key Responsibilities:**
- Input/output state management
- Streaming response coordination
- Tab creation and management
- Handler invocation

### 2. Backend Layer (Python)

#### Executors (`src/ontonaut/executors.py`)
Pluggable code execution backends:

```python
# Interface
def executor(code: str) -> Any:
    """Execute code and return result."""
    return result
```

**Built-in Executors:**
- `PythonExecutor`: Execute Python code with eval/exec
- `JSONExecutor`: Format and validate JSON
- `CalculatorExecutor`: Evaluate math expressions
- `RegexExecutor`: Test regular expressions

**Pattern:**
- Single function or callable class
- Takes code string, returns result
- Handles own exceptions
- Can maintain state (if class)

#### Handlers (`src/ontonaut/handlers.py`)
Pluggable chat response generators:

```python
# Interface (streaming)
def handler(message: str) -> Iterator[str]:
    """Generate response tokens."""
    yield token

# Interface (non-streaming)
def handler(message: str) -> str:
    """Generate response."""
    return response
```

**Built-in Handlers:**
- `EchoHandler`: Echo back user message (testing)
- `OpenAIHandler`: Stream from OpenAI GPT models
- `AnthropicHandler`: Stream from Anthropic Claude
- `MCPHandler`: Model Context Protocol integration
- `CustomHandler`: Wrapper for any function

**Pattern:**
- Single function or callable class
- Takes message string
- Yields tokens (streaming) or returns string
- Handles own exceptions
- Can maintain conversation context (if class)

### 3. Frontend Layer (JavaScript/CSS)

#### editor.js (`src/ontonaut/static/editor.js`)
- ESM module with default export
- Renders code editor UI
- Handles user interactions
- Syncs state with Python

**Key Features:**
- Syntax highlighting preparation
- Line numbers
- Keyboard shortcuts (Cmd/Ctrl+Enter)
- Execute button
- Error display
- Theme switching

#### chatbot.js (`src/ontonaut/static/chatbot.js`)
- ESM module with default export
- Renders chat interface
- Manages tabs
- Handles streaming updates
- Formats code blocks

**Key Features:**
- Streaming text display
- Tab management (create, switch, close)
- Markdown code formatting
- Keyboard shortcuts
- Theme switching

#### CSS Files
- `editor.css`: CodeEditor styles
- `chatbot.css`: ChatBot styles

**Design:**
- Modern, sleek aesthetic
- Matching marimo look and feel
- Light/dark theme support
- Responsive layout
- Smooth animations

## Data Flow

### CodeEditor Execution Flow

```
1. User types code in UI (JavaScript)
   ↓
2. Input event syncs to Python (anywidget)
   code traitlet updated
   ↓
3. User clicks "Run" or presses Cmd/Ctrl+Enter
   ↓
4. JavaScript sends execute message
   model.send({type: "execute", code: code})
   ↓
5. Python _handle_execute() receives message
   ↓
6. Python calls executor with code string
   result = self._executor(code)
   ↓
7. Executor processes and returns result
   ↓
8. Python updates output traitlet
   self.output = str(result)
   ↓
9. anywidget syncs output to JavaScript
   ↓
10. JavaScript renders output in UI
    model.on("change:output", ...)
```

### ChatBot Streaming Flow

```
1. User types message in UI (JavaScript)
   ↓
2. Input syncs to Python (anywidget)
   input_text traitlet updated
   ↓
3. User clicks "Run" or presses Cmd/Ctrl+Enter
   ↓
4. JavaScript sends execute message
   model.send({type: "execute", input: input})
   ↓
5. Python _handle_input() receives message
   ↓
6. Python saves previous output to tab (if exists)
   self._save_to_tab(self._last_input, self.output)
   ↓
7. Python calls handler with message
   response = self._handler(message)
   ↓
8. Handler yields tokens (streaming)
   for token in generate_tokens(message):
       yield token
   ↓
9. Python _stream_response() processes tokens
   for token in response:
       self.output += token
       # anywidget syncs to JS automatically
   ↓
10. JavaScript receives incremental updates
    model.on("change:output", ...)
    ↓
11. JavaScript updates DOM incrementally
    outputContent.innerHTML = formatOutput(output)
```

## State Management

### Traitlets
Ontonaut uses `traitlets` for reactive state:

```python
class CodeEditor(anywidget.AnyWidget):
    # State synchronized with JavaScript
    code = traitlets.Unicode("").tag(sync=True)
    output = traitlets.Unicode("").tag(sync=True)
    error = traitlets.Unicode("").tag(sync=True)
    is_executing = traitlets.Bool(False).tag(sync=True)
```

**Key Points:**
- `.tag(sync=True)` enables Python ↔ JS sync
- Changes in Python automatically update JS
- Changes in JS automatically update Python
- No manual sync code needed

### JavaScript State Listeners

```javascript
function render({ model, el }) {
  // Listen for Python changes
  model.on("change:output", () => {
    const output = model.get("output");
    updateUI(output);
  });

  // Send changes to Python
  inputBox.addEventListener("input", () => {
    model.set("code", inputBox.value);
    model.save_changes();
  });
}
```

### Message Passing
For actions (not state):

```javascript
// JavaScript → Python
model.send({type: "execute", code: "..."});

// Python receives
def _handle_execute(self, data, buffers):
    code = data.get("code")
    result = self._executor(code)
```

## File Structure

```
ontonaut/
├── src/ontonaut/
│   ├── __init__.py              # Package exports
│   ├── editor.py                # CodeEditor widget (200 lines)
│   ├── chatbot.py               # ChatBot widget (250 lines)
│   ├── executors.py             # Built-in executors (300 lines)
│   ├── handlers.py              # Built-in handlers (400 lines)
│   ├── py.typed                 # Type hint marker
│   └── static/
│       ├── editor.js            # CodeEditor frontend (180 lines)
│       ├── editor.css           # CodeEditor styles (260 lines)
│       ├── chatbot.js           # ChatBot frontend (310 lines)
│       └── chatbot.css          # ChatBot styles (340 lines)
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_editor.py           # CodeEditor tests (200 lines)
│   ├── test_chatbot.py          # ChatBot tests (200 lines)
│   └── test_executors.py        # Executor tests (260 lines)
├── examples/
│   ├── basic_usage.py           # CodeEditor examples
│   ├── chatbot_examples.py      # ChatBot examples
│   └── simple_openai.py         # OpenAI integration
├── book/
│   ├── markdown/                # User documentation
│   └── marimo/                  # Interactive notebooks
├── docs/                        # Architecture docs (you are here)
├── scripts/
│   ├── setup.sh                 # Environment setup
│   ├── test.sh                  # Run tests
│   ├── lint.sh                  # Run linters
│   ├── format.sh                # Format code
│   ├── build.sh                 # Build package
│   ├── clean.sh                 # Clean artifacts
│   └── ruff.sh                  # Run ruff
├── pyproject.toml               # Package configuration
├── Makefile                     # Development commands
├── LICENSE                      # MIT License
└── README.md                    # Main documentation
```

## Dependencies

### Core Dependencies
- `anywidget>=0.9.0` - Widget framework
- `traitlets>=5.14.0` - Reactive state
- (Python 3.9+ required)

### Optional Dependencies
- `openai` - For OpenAIHandler
- `anthropic` - For AnthropicHandler

### Development Dependencies
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-asyncio` - Async test support
- `black` - Code formatting
- `ruff` - Fast linting
- `mypy` - Type checking
- `marimo` - Interactive notebooks

## Design Patterns

### 1. Plugin Pattern
Both executors and handlers follow the plugin pattern:
- Simple function/callable interface
- No inheritance required
- Easy to extend
- Type-safe

### 2. Traitlet Pattern
State management via traitlets:
- Declarative state definition
- Automatic synchronization
- Type validation
- Change notifications

### 3. Anywidget Pattern
Widget structure:
- Python class extends `anywidget.AnyWidget`
- JavaScript ESM module with `render()` function
- CSS for styling
- Bidirectional communication

### 4. Streaming Pattern
For real-time updates:
- Python generator yields tokens
- Traitlet updates trigger JS listeners
- JS updates DOM incrementally
- No blocking, smooth UX

### 5. Separation of Concerns
- **Python**: State, logic, execution
- **JavaScript**: UI rendering, interaction
- **CSS**: Styling, themes
- **Executors/Handlers**: Pluggable backends

## Performance Considerations

### Initial Render
- Keep JavaScript module small
- Lazy load heavy dependencies
- Minimal DOM operations
- Target: <100ms initial render

### Streaming
- Incremental DOM updates (not full replace)
- Use `innerHTML` for formatted content
- Debounce rapid updates if needed
- Target: 60fps smooth animation

### State Sync
- Only sync necessary state
- Use `.tag(sync=True)` sparingly
- Batch updates when possible
- Avoid sync loops

### Execution
- Run in Python (not JS)
- Handle long-running code gracefully
- Show loading state (`is_executing`, `is_streaming`)
- Consider timeouts for custom executors

## Security Considerations

### Code Execution
- PythonExecutor uses `eval()`/`exec()` - sandboxed by Python's execution model
- Custom executors should validate input
- Never execute untrusted code without sandboxing
- Consider timeout mechanisms

### API Keys
- Never hardcode API keys
- Use environment variables
- Document security best practices
- Consider key rotation

### XSS Prevention
- Escape HTML in output
- Use `textContent` for untrusted strings
- Sanitize markdown rendering
- Be careful with `innerHTML`

## Error Handling

### Python Side
```python
try:
    result = self._executor(code)
    self.output = str(result)
    self.error = ""
except Exception as e:
    self.error = f"{type(e).__name__}: {str(e)}"
    self.output = ""
```

### JavaScript Side
```javascript
model.on("change:error", () => {
  const error = model.get("error");
  if (error) {
    errorDisplay.textContent = error;
    errorDisplay.style.display = "block";
  } else {
    errorDisplay.style.display = "none";
  }
});
```

### Best Practices
- Catch exceptions at widget level
- Display user-friendly errors
- Log detailed errors for debugging
- Never crash the widget
- Provide recovery mechanisms

## Testing Strategy

### Unit Tests
- Test all executors independently
- Test all handlers independently
- Test widget state management
- Test error handling

### Integration Tests
- Test widget + executor combinations
- Test widget + handler combinations
- Test state synchronization
- Test user interactions

### Coverage Target
- Overall: >85%
- Core widgets: >90%
- Executors/Handlers: >95%

### Test Structure
```python
class TestCodeEditor:
    def test_initialization(self):
        """Test widget creation."""

    def test_execution(self):
        """Test code execution."""

    def test_error_handling(self):
        """Test error cases."""
```

## Build and Release

### Development Build
```bash
make setup    # Create venv, install deps
make test     # Run tests
make lint     # Run linters
make format   # Format code
```

### Production Build
```bash
make build    # Build wheel and sdist
```

### Release Process
1. Update version in `pyproject.toml`
2. Update CHANGELOG
3. Run full test suite
4. Build package
5. Test package locally
6. Push to PyPI

## Future Enhancements

### Potential Features
- [ ] Syntax highlighting in CodeEditor
- [ ] Copy-to-clipboard for code blocks
- [ ] Tab persistence (save/load)
- [ ] More built-in executors (Lua, R, etc.)
- [ ] More built-in handlers (Cohere, etc.)
- [ ] Async handler support
- [ ] Collaborative editing
- [ ] Cell linking and dataflow
- [ ] Export functionality

### Architecture Evolution
- Consider separate packages for executors/handlers
- Plugin registry system
- Configuration management
- Theme customization API

## Contributing

See [contributing.md](./contributing.md) for:
- Code style guidelines
- PR process
- Testing requirements
- Documentation standards

## References

- [anywidget Documentation](https://anywidget.dev/)
- [Traitlets Documentation](https://traitlets.readthedocs.io/)
- [Marimo Documentation](https://docs.marimo.io/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
