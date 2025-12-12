# Handlers Reference

Handlers are the backend engines that power the `ChatBot` widget. They take user input and return/stream responses.

## Overview

```python
from ontonaut import ChatBot, EchoHandler

handler = EchoHandler()
chatbot = ChatBot(handler=handler)
```

## Built-in Handlers

### EchoHandler

Echo back user's message with streaming effect (for testing).

**Usage:**

```python
from ontonaut import EchoHandler

# Basic usage
handler = EchoHandler()
for chunk in handler("Hello"):
    print(chunk, end="")  # "Hello"

# With prefix and delay
handler = EchoHandler(
    prefix="You said: ",
    delay=0.03
)
for chunk in handler("Hi"):
    print(chunk, end="")  # "You said: Hi"
```

**Constructor:**

```python
EchoHandler(
    prefix: str = "",      # Prefix before echoed message
    delay: float = 0.02    # Delay between tokens (seconds)
)
```

**Behavior:**
- Streams message back token by token
- Adds optional prefix
- Simulates streaming delay
- Perfect for testing UI

---

### OpenAIHandler

Stream from OpenAI's GPT models.

**Usage:**

```python
from ontonaut import OpenAIHandler
import os

handler = OpenAIHandler(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4",
    system_prompt="You are a helpful assistant.",
    temperature=0.7
)

for chunk in handler("What is Python?"):
    print(chunk, end="")
```

**Constructor:**

```python
OpenAIHandler(
    api_key: str,                    # OpenAI API key
    model: str = "gpt-4",            # Model name
    system_prompt: str = "...",      # System prompt
    temperature: float = 0.7,        # Temperature (0-2)
    max_tokens: Optional[int] = None,# Max response tokens
    **kwargs                         # Additional OpenAI parameters
)
```

**Requirements:**

```bash
pip install openai
```

**Example:**

```python
import os
from ontonaut import ChatBot, OpenAIHandler

handler = OpenAIHandler(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4",
    system_prompt="You are a Python expert. Answer questions about Python programming.",
    temperature=0.7,
    max_tokens=1000
)

chatbot = ChatBot(handler=handler)
```

---

### AnthropicHandler

Stream from Anthropic's Claude models.

**Usage:**

```python
from ontonaut import AnthropicHandler
import os

handler = AnthropicHandler(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-opus-20240229",
    system_prompt="You are a helpful assistant.",
    temperature=0.7
)

for chunk in handler("Explain async/await"):
    print(chunk, end="")
```

**Constructor:**

```python
AnthropicHandler(
    api_key: str,                    # Anthropic API key
    model: str = "claude-3-...",     # Model name
    system_prompt: str = "...",      # System prompt
    temperature: float = 0.7,        # Temperature (0-1)
    max_tokens: int = 1024,          # Max response tokens
    **kwargs                         # Additional Anthropic parameters
)
```

**Requirements:**

```bash
pip install anthropic
```

**Example:**

```python
import os
from ontonaut import ChatBot, AnthropicHandler

handler = AnthropicHandler(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-opus-20240229",
    system_prompt="You are a code review assistant.",
    temperature=0.5,
    max_tokens=2000
)

chatbot = ChatBot(handler=handler)
```

---

### MCPHandler

Use Model Context Protocol for tool calling and context.

**Usage:**

```python
from ontonaut import MCPHandler, EchoHandler

# Define tools
def calculator(expression: str) -> str:
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

# Define context provider
def get_context(message: str) -> str:
    if "weather" in message.lower():
        return "Current: 72°F, Sunny in SF"
    return ""

# Create handler
handler = MCPHandler(
    llm_handler=EchoHandler(),
    tools=[calculator],
    context_provider=get_context
)

for chunk in handler("What's 10 * 5?"):
    print(chunk, end="")
```

**Constructor:**

```python
MCPHandler(
    llm_handler: Callable,              # Base LLM handler
    tools: Optional[List[Callable]] = None,  # Tool functions
    context_provider: Optional[Callable] = None  # Context function
)
```

**Tool Signature:**

```python
def tool_function(arg: str) -> str:
    """Tool docstring (used as description)."""
    # Your logic
    return result
```

**Context Provider Signature:**

```python
def context_provider(message: str) -> str:
    """Get context for message."""
    # Your logic
    return context_string
```

**Example:**

```python
from ontonaut import MCPHandler, OpenAIHandler
import os

# Define tools
def search_docs(query: str) -> str:
    """Search documentation for query."""
    results = search_index(query)
    return format_results(results)

def get_code_example(topic: str) -> str:
    """Get code example for topic."""
    return code_examples.get(topic, "No example found")

# Context provider
def get_project_context(message: str) -> str:
    """Add project-specific context."""
    if "react" in message.lower():
        return "Project uses React 18 with TypeScript"
    return ""

# Create handler
handler = MCPHandler(
    llm_handler=OpenAIHandler(api_key=os.getenv("OPENAI_API_KEY")),
    tools=[search_docs, get_code_example],
    context_provider=get_project_context
)

chatbot = ChatBot(handler=handler)
```

---

### CustomHandler

Wrap any function as a handler.

**Usage:**

```python
from ontonaut import CustomHandler

def my_function(message: str):
    """Custom logic."""
    yield f"You said: {message}"

handler = CustomHandler(my_function)

for chunk in handler("Hello"):
    print(chunk, end="")
```

**Constructor:**

```python
CustomHandler(
    handler_function: Callable[[str], Union[str, Iterator[str]]]
)
```

**Example:**

```python
from ontonaut import ChatBot, CustomHandler
import time

def company_handler(message: str):
    """Company-specific handler."""
    # Add authentication
    user = authenticate_user()

    # Add logging
    log_request(user, message)

    # Process with company logic
    response = company_llm.generate(message)

    # Stream response
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

    # Log completion
    log_completion(user)

chatbot = ChatBot(handler=CustomHandler(company_handler))
```

## Creating Custom Handlers

### Simple Streaming Handler

```python
def my_handler(message: str):
    """Simple streaming handler."""
    import time

    response = f"You asked: {message}. Here's my answer!"

    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Use it
from ontonaut import ChatBot
chatbot = ChatBot(handler=my_handler)
```

### Non-streaming Handler

```python
def simple_handler(message: str) -> str:
    """Non-streaming handler (returns full string)."""
    return f"Response to: {message}"

chatbot = ChatBot(handler=simple_handler)
```

### Class-based Handler

```python
class MyHandler:
    """Stateful handler with configuration."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = init_client(api_key)

    def __call__(self, message: str):
        """Stream from API."""
        stream = self.client.chat(
            message=message,
            model=self.model,
            stream=True
        )

        for chunk in stream:
            if chunk.text:
                yield chunk.text

# Use it
handler = MyHandler(api_key="...", model="gpt-4")
chatbot = ChatBot(handler=handler)
```

### With Error Handling

```python
def safe_handler(message: str):
    """Handler with error handling."""
    try:
        # Your logic
        response = process_message(message)

        for token in response:
            yield token

    except Exception as e:
        yield f"Error: {type(e).__name__}: {str(e)}"
```

## Handler Pattern

All handlers follow this pattern:

```python
# Streaming (preferred)
def handler(message: str) -> Iterator[str]:
    """Stream response token by token."""
    for token in generate_tokens(message):
        yield token

# Non-streaming
def handler(message: str) -> str:
    """Return full response."""
    return generate_response(message)

# Class-based
class MyHandler:
    def __call__(self, message: str) -> Iterator[str]:
        """Stream response."""
        for token in self.generate(message):
            yield token
```

**Requirements:**
- Must accept single `str` parameter (the message)
- Should return `str` OR yield `str` tokens
- Should handle exceptions internally (recommended)
- Can maintain state between calls (if class)

## Best Practices

### 1. Error Handling

Always catch and handle errors:

```python
def safe_handler(message: str):
    try:
        for chunk in stream_response(message):
            yield chunk
    except APIError as e:
        yield f"API Error: {e}"
    except Exception as e:
        yield f"Error: {e}"
```

### 2. Rate Limiting

Implement rate limiting:

```python
import time

class RateLimitedHandler:
    def __init__(self, base_handler, calls_per_minute=10):
        self.base_handler = base_handler
        self.calls_per_minute = calls_per_minute
        self.last_call = 0

    def __call__(self, message: str):
        # Check rate limit
        elapsed = time.time() - self.last_call
        wait_time = 60 / self.calls_per_minute

        if elapsed < wait_time:
            time.sleep(wait_time - elapsed)

        self.last_call = time.time()

        # Call base handler
        for chunk in self.base_handler(message):
            yield chunk
```

### 3. Logging

Add logging for debugging:

```python
import logging

class LoggingHandler:
    def __init__(self, base_handler):
        self.base_handler = base_handler
        self.logger = logging.getLogger(__name__)

    def __call__(self, message: str):
        self.logger.info(f"Request: {message[:50]}...")

        response = ""
        for chunk in self.base_handler(message):
            response += chunk
            yield chunk

        self.logger.info(f"Response: {response[:50]}...")
```

### 4. Caching

Cache responses for common queries:

```python
from functools import lru_cache

class CachedHandler:
    def __init__(self, base_handler):
        self.base_handler = base_handler
        self.cache = {}

    def __call__(self, message: str):
        # Check cache
        if message in self.cache:
            for char in self.cache[message]:
                yield char
                time.sleep(0.01)
            return

        # Generate and cache
        response = ""
        for chunk in self.base_handler(message):
            response += chunk
            yield chunk

        self.cache[message] = response
```

### 5. Context Management

Manage conversation context:

```python
class ContextualHandler:
    def __init__(self, base_handler):
        self.base_handler = base_handler
        self.context = []

    def __call__(self, message: str):
        # Add to context
        self.context.append({"role": "user", "content": message})

        # Generate response with context
        response = ""
        for chunk in self.base_handler(self.context):
            response += chunk
            yield chunk

        # Add response to context
        self.context.append({"role": "assistant", "content": response})
```

## Advanced Examples

### Company OpenAI Wrapper

```python
class CompanyOpenAIHandler:
    """Wrap company's OpenAI integration."""

    def __init__(self, config):
        self.config = config
        self.client = self._init_client()

    def _init_client(self):
        # Company-specific initialization
        return openai.OpenAI(
            api_key=self.config["api_key"],
            base_url=self.config["base_url"],
            default_headers=self.config["headers"]
        )

    def __call__(self, message: str):
        # Add rate limiting
        self._check_rate_limit()

        # Add logging
        self._log_request(message)

        # Add cost tracking
        self._track_usage("request")

        try:
            stream = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": message}],
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    yield text
                    self._track_usage("token", len(text))

            self._log_completion()

        except Exception as e:
            self._log_error(e)
            yield f"Error: {e}"
```

### Multi-Model Handler

```python
class MultiModelHandler:
    """Use different models based on query."""

    def __init__(self, openai_key, anthropic_key):
        self.openai = OpenAIHandler(openai_key)
        self.anthropic = AnthropicHandler(anthropic_key)

    def __call__(self, message: str):
        # Route to appropriate model
        if self._needs_code(message):
            # Use GPT-4 for code
            for chunk in self.openai(message):
                yield chunk
        else:
            # Use Claude for text
            for chunk in self.anthropic(message):
                yield chunk

    def _needs_code(self, message: str) -> bool:
        keywords = ["code", "function", "implement", "debug"]
        return any(kw in message.lower() for kw in keywords)
```

### RAG Handler

```python
class RAGHandler:
    """Retrieval-Augmented Generation handler."""

    def __init__(self, llm_handler, vector_store):
        self.llm_handler = llm_handler
        self.vector_store = vector_store

    def __call__(self, message: str):
        # Retrieve relevant documents
        docs = self.vector_store.search(message, k=5)

        # Build context
        context = "\\n\\n".join(docs)

        # Create augmented prompt
        prompt = f"""Context:\\n{context}\\n\\nQuestion: {message}\\n\\nAnswer:"""

        # Stream response
        for chunk in self.llm_handler(prompt):
            yield chunk
```

## Testing Handlers

Always test your handlers:

```python
def test_my_handler():
    handler = MyHandler()

    # Test streaming
    response = "".join(handler("test message"))
    assert len(response) > 0

    # Test error handling
    response = "".join(handler("error trigger"))
    assert "Error" in response

    print("All tests passed!")

# Test with chatbot
def test_with_chatbot():
    from ontonaut import ChatBot

    chatbot = ChatBot(handler=MyHandler())
    chatbot.execute("test")

    assert chatbot.output != ""
    assert chatbot.error == ""
```

## See Also

- [ChatBot Widget](./chatbot.md)
- [Custom Handlers Guide](./custom-handlers.md)
- [Examples](../../examples/chatbot_examples.py)
