# ChatBot Widget

The `ChatBot` is a streaming AI chat widget for marimo with automatic tab creation, code formatting, and custom handlers.

## Overview

```python
from ontonaut import ChatBot, EchoHandler

chatbot = ChatBot(
    handler=EchoHandler(),
    placeholder="Ask me anything...",
    theme="dark"
)
chatbot
```

## Features

- ✅ **Streaming Responses** - Token-by-token output
- ✅ **Automatic Tabs** - Each question creates a new tab
- ✅ **Code Formatting** - Markdown code blocks render beautifully
- ✅ **Custom Handlers** - OpenAI, Anthropic, or your own
- ✅ **MCP Integration** - Model Context Protocol support
- ✅ **Keyboard Shortcuts** - Cmd/Ctrl+Enter to send
- ✅ **Themes** - Light and dark modes
- ✅ **No Backend Required** - History managed in UI

## Basic Usage

### Simple Echo Handler

```python
from ontonaut import ChatBot, EchoHandler

chatbot = ChatBot(
    handler=EchoHandler(delay=0.03),
    placeholder="Type a message..."
)
chatbot
```

### OpenAI Streaming

```python
from ontonaut import ChatBot, OpenAIHandler
import os

chatbot = ChatBot(
    handler=OpenAIHandler(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4",
        system_prompt="You are a helpful assistant.",
        temperature=0.7
    ),
    theme="dark"
)
chatbot
```

## Configuration

### Constructor Parameters

```python
ChatBot(
    handler: Optional[Callable[[str], Union[str, Iterator[str]]]] = None,
    input_text: str = "",
    placeholder: str = "Ask me anything...",
    theme: str = "light",
    language: str = "text"
)
```

**Parameters:**
- `handler`: Function that takes input and returns/streams response
- `input_text`: Initial input text
- `placeholder`: Placeholder text for input box
- `theme`: UI theme ("light" or "dark")
- `language`: Default language for syntax highlighting

### Attributes

```python
chatbot.input_text    # Current input (get/set)
chatbot.output        # Current output
chatbot.error         # Error message (if any)
chatbot.is_streaming  # True if currently streaming
chatbot.tabs          # List of historical tabs
chatbot.active_tab    # Currently viewed tab index
chatbot.theme         # Current theme
```

## Handlers

### Built-in Handlers

#### EchoHandler

Echo back the user's message (for testing):

```python
from ontonaut import ChatBot, EchoHandler

chatbot = ChatBot(
    handler=EchoHandler(
        delay=0.03,  # Delay between tokens (seconds)
        prefix="You said: "
    )
)
```

#### OpenAIHandler

Stream from OpenAI's GPT models:

```python
from ontonaut import ChatBot, OpenAIHandler
import os

handler = OpenAIHandler(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4",
    system_prompt="You are a helpful coding assistant.",
    temperature=0.7,
    max_tokens=1000
)

chatbot = ChatBot(handler=handler)
```

#### AnthropicHandler

Stream from Anthropic's Claude models:

```python
from ontonaut import ChatBot, AnthropicHandler
import os

handler = AnthropicHandler(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-opus-20240229",
    system_prompt="You are a helpful assistant.",
    temperature=0.7,
    max_tokens=1000
)

chatbot = ChatBot(handler=handler)
```

#### MCPHandler

Use Model Context Protocol for tool calling:

```python
from ontonaut import ChatBot, MCPHandler, EchoHandler

def calculator_tool(expression: str) -> str:
    """Evaluate math expressions."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

def context_provider(message: str) -> str:
    """Provide context based on message."""
    if "weather" in message.lower():
        return "Current: 72°F, Sunny"
    return ""

handler = MCPHandler(
    llm_handler=EchoHandler(),
    tools=[calculator_tool],
    context_provider=context_provider
)

chatbot = ChatBot(handler=handler)
```

#### CustomHandler

Wrap any function as a handler:

```python
from ontonaut import ChatBot, CustomHandler

def my_function(message: str):
    """Custom streaming logic."""
    import time
    words = f"Response to: {message}".split()
    for word in words:
        yield word + " "
        time.sleep(0.05)

chatbot = ChatBot(handler=CustomHandler(my_function))
```

### Custom Handlers

Create your own streaming handler:

```python
def my_handler(message: str):
    """Custom handler with streaming."""
    import time

    # Process message
    response = process_message(message)

    # Stream response word by word
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

chatbot = ChatBot(handler=my_handler)
```

Class-based handler:

```python
class MyCompanyHandler:
    def __init__(self, config):
        self.config = config
        self.client = init_client(config)

    def __call__(self, message: str):
        """Stream from company API."""
        stream = self.client.chat(message, stream=True)

        for chunk in stream:
            if chunk.text:
                yield chunk.text

handler = MyCompanyHandler(config={...})
chatbot = ChatBot(handler=handler)
```

## Methods

### execute()

Send a message programmatically:

```python
chatbot = ChatBot(handler=EchoHandler())

# Execute specific message
chatbot.execute("Hello, world!")

# Execute current input
chatbot.execute()

# Access response
print(chatbot.output)
```

### clear()

Clear current input and output:

```python
chatbot.clear()
# Clears: input_text, output, error
```

### clear_all()

Clear everything including tabs:

```python
chatbot.clear_all()
# Clears: input_text, output, error, tabs
```

### get_tab()

Get a specific tab by index:

```python
tab = chatbot.get_tab(0)
# Returns: {"title": str, "content": str, "input": str}

if tab:
    print(f"Input: {tab['input']}")
    print(f"Output: {tab['content']}")
```

## Tabs

### Automatic Tab Creation

Every time you ask a new question, the previous output is saved to a tab:

```python
chatbot = ChatBot(handler=EchoHandler())

chatbot.execute("Question 1")
# No tabs yet

chatbot.execute("Question 2")
# 1 tab created with "Question 1" output

chatbot.execute("Question 3")
# 2 tabs total
```

### Tab Structure

Each tab contains:

```python
{
    "title": str,    # First 30 chars of input
    "content": str,  # Full output
    "input": str     # Full input text
}
```

### Access Tabs

```python
# Get number of tabs
num_tabs = len(chatbot.tabs)

# Iterate tabs
for i, tab in enumerate(chatbot.tabs):
    print(f"Tab {i}: {tab['title']}")
    print(f"  Input: {tab['input']}")
    print(f"  Output: {tab['content'][:50]}...")

# Get specific tab
tab = chatbot.get_tab(0)
```

### Switch Tabs

Tabs switch automatically in the UI:
- Click any historical tab to view it
- Click "Current" to return to live output
- Close tabs with the × button

Programmatically:

```python
chatbot.active_tab = 0  # View first tab
chatbot.active_tab = -1  # View current
```

## Code Formatting

### Inline Code

Use backticks in your handler:

```python
def code_helper(message: str):
    yield "Try using `print('hello')` in Python!"

chatbot = ChatBot(handler=code_helper)
```

Renders as: Try using `print('hello')` in Python!

### Code Blocks

Use triple backticks with language:

```python
def code_teacher(message: str):
    yield "Here's a Python example:\n\n"
    yield "```python\n"
    yield "def greet(name):\n"
    yield "    return f'Hello {name}!'\n"
    yield "```"

chatbot = ChatBot(handler=code_teacher)
```

Renders as a formatted code block with:
- Syntax highlighting preparation
- Language badge (top-right)
- Proper spacing and borders

### Supported Languages

- `python`, `javascript`, `typescript`, `java`, `rust`, `go`
- `sql`, `bash`, `shell`, `json`, `yaml`, `xml`
- `html`, `css`, `markdown`
- Any string (displayed in badge)

## Keyboard Shortcuts

- **Cmd/Ctrl + Enter**: Send message
- **Tab**: Insert 4 spaces (in input)

## Styling

### Themes

```python
# Light theme
chatbot = ChatBot(handler=my_handler, theme="light")

# Dark theme
chatbot = ChatBot(handler=my_handler, theme="dark")

# Change theme dynamically
chatbot.theme = "dark"
```

### Placeholder

```python
chatbot = ChatBot(
    handler=my_handler,
    placeholder="Ask about Python, JavaScript, or React..."
)
```

## Advanced Usage

### Company OpenAI Wrapper

```python
def company_openai(message: str):
    """Wrap company's OpenAI integration."""
    # Add authentication
    headers = get_company_auth()

    # Add logging
    log_request(message)

    # Add rate limiting
    rate_limiter.check()

    # Call company endpoint
    stream = company_api.chat(
        message=message,
        stream=True
    )

    # Stream response
    for chunk in stream:
        if chunk.delta:
            yield chunk.delta

    # Log completion
    log_completion()

chatbot = ChatBot(handler=company_openai)
```

### Multi-step Processing

```python
def multi_step_handler(message: str):
    """Handler with multiple steps."""
    import time

    # Step 1: Acknowledge
    yield "🤔 Thinking...\n\n"
    time.sleep(0.5)

    # Step 2: Process
    result = process(message)

    # Step 3: Format response with code
    yield "Here's what I found:\n\n"
    yield f"```python\n{result}\n```\n\n"
    yield "Does this help?"

chatbot = ChatBot(handler=multi_step_handler)
```

### Async Handlers (Future)

```python
async def async_handler(message: str):
    """Async streaming handler."""
    async for chunk in stream_from_api(message):
        yield chunk

chatbot = ChatBot(handler=async_handler)
```

## Examples

### Simple Q&A Bot

```python
def qa_bot(question: str):
    """Simple Q&A bot."""
    responses = {
        "python": "Python is a high-level programming language...",
        "javascript": "JavaScript is a versatile scripting language...",
        "react": "React is a JavaScript library for building UIs..."
    }

    for key, answer in responses.items():
        if key in question.lower():
            for word in answer.split():
                yield word + " "
                time.sleep(0.03)
            return

    yield "I don't know about that. Try asking about Python, JavaScript, or React!"

chatbot = ChatBot(handler=qa_bot)
```

### Code Example Generator

```python
def code_generator(prompt: str):
    """Generate code examples."""
    import time

    if "function" in prompt.lower():
        yield "Here's a function example:\n\n```python\n"
        yield "def my_function(param):\n"
        yield "    '''Docstring here'''\n"
        yield "    return param * 2\n"
        yield "```"
    elif "class" in prompt.lower():
        yield "Here's a class example:\n\n```python\n"
        yield "class MyClass:\n"
        yield "    def __init__(self, value):\n"
        yield "        self.value = value\n"
        yield "```"
    else:
        yield "Ask about 'function' or 'class' to see examples!"

chatbot = ChatBot(handler=code_generator)
```

## Tips & Best Practices

1. **Always yield strings** in streaming handlers
2. **Add small delays** for smooth streaming effect
3. **Format code** with markdown backticks
4. **Handle errors gracefully** in your handler
5. **Test streaming** before deploying
6. **Use appropriate theme** for your notebook
7. **Clear tabs periodically** with `clear_all()`

## Common Issues

### Handler Not Streaming

Ensure your handler uses `yield`:

```python
# Bad - not streaming
def bad_handler(msg: str) -> str:
    return "response"

# Good - streaming
def good_handler(msg: str):
    yield "response"
```

### Tabs Not Creating

Tabs are created automatically when you execute a new message while there's existing output.

### Code Not Formatting

Use proper markdown syntax:

````python
# Inline code
yield "Use `print()` function"

# Code blocks
yield "```python\nprint('hello')\n```"
````

### Streaming Too Fast/Slow

Adjust delay in your handler:

```python
import time

def handler(msg: str):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)  # Adjust this
```

## See Also

- [Handlers Guide](./handlers.md)
- [Custom Handlers](./custom-handlers.md)
- [Styling Guide](./styling.md)
- [Examples](../../examples/chatbot_examples.py)
