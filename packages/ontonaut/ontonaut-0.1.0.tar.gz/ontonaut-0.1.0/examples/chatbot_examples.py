"""ChatBot examples for Ontonaut."""

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from ontonaut import ChatBot, CustomHandler, EchoHandler, OpenAIHandler

    return ChatBot, CustomHandler, EchoHandler, OpenAIHandler, mo


@app.cell
def _(mo):
    mo.md(
        """
    # Ontonaut ChatBot Examples

    Stream AI responses in marimo with custom backends!

    **✨ New Features:**
    - 📑 **Tabs**: Each new question creates a tab with previous output
    - 💻 **Code Formatting**: Markdown code blocks render with syntax highlighting
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 1: Echo Handler (Testing)

    Simple echo handler that streams your message back.
    """
    )
    return


@app.cell
def _(ChatBot, EchoHandler):
    # Create echo handler for testing
    echo_handler = EchoHandler(delay=0.03)

    chatbot1 = ChatBot(
        handler=echo_handler, placeholder="Type a message to echo back..."
    )
    chatbot1
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 2: OpenAI Streaming

    Connect to OpenAI with streaming responses.

    **Setup:**
    ```bash
    pip install openai
    export OPENAI_API_KEY="your-key"
    ```
    """
    )
    return


@app.cell
def _(ChatBot, OpenAIHandler):
    import os

    # Check if API key is set
    if os.getenv("OPENAI_API_KEY"):
        openai_handler = OpenAIHandler(
            model="gpt-4",
            system_prompt="You are a helpful AI assistant in a marimo notebook.",
            temperature=0.7,
        )

        chatbot2 = ChatBot(
            handler=openai_handler, placeholder="Ask me anything...", theme="light"
        )
        chatbot2
    else:
        print("⚠️  Set OPENAI_API_KEY environment variable to use OpenAI")
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 3: Custom Company Handler

    Wrap your company's OpenAI logic with custom preprocessing.
    """
    )
    return


@app.cell
def _(ChatBot, CustomHandler):
    def company_openai_wrapper(message: str):
        """
        Your company's custom OpenAI wrapper.

        This could include:
        - Custom authentication
        - Rate limiting
        - Logging
        - Content filtering
        - Cost tracking
        """
        # Example: Add company context
        enhanced_message = f"[Company Context]: User query: {message}"

        # Simulate streaming response
        import time

        words = f"I received your message: '{message}'. In a real implementation, this would call your company's OpenAI wrapper.".split()

        for word in words:
            yield word + " "
            time.sleep(0.05)

    company_handler = CustomHandler(company_openai_wrapper)

    chatbot3 = ChatBot(
        handler=company_handler,
        placeholder="Ask with company context...",
        max_height="400px",
    )
    chatbot3
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 4: MCP Server Integration

    Use Model Context Protocol for tool calling and context.
    """
    )
    return


@app.cell
def _(ChatBot):
    from ontonaut.handlers import EchoHandler, MCPHandler

    # Define your tools
    def calculator_tool(expression: str) -> str:
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {e}"

    # Define context provider
    def get_user_context(message: str) -> str:
        # This could fetch from databases, files, APIs, etc.
        if "weather" in message.lower():
            return "Current location: San Francisco. Temperature: 72°F"
        return ""

    # Create base LLM handler
    base_handler = EchoHandler(delay=0.02)

    # Wrap with MCP
    mcp_handler = MCPHandler(
        llm_handler=base_handler,
        tools=[calculator_tool],
        context_provider=get_user_context,
    )

    chatbot4 = ChatBot(
        handler=mcp_handler, placeholder="Ask about weather or calculations..."
    )
    chatbot4
    return (EchoHandler,)


@app.cell
def _(mo):
    mo.md(
        """
    ## Example 5: Custom Streaming Handler

    Build your own handler with custom logic.
    """
    )
    return


@app.cell
def _(ChatBot):
    def my_custom_handler(message: str):
        """
        Your completely custom handler.

        This is where you can:
        - Call your custom LLM endpoints
        - Integrate with internal APIs
        - Add business logic
        - Implement custom streaming
        """
        import time

        # Simulate processing
        yield "🤔 Thinking...\n\n"
        time.sleep(0.5)

        # Custom response logic with code examples
        if "hello" in message.lower():
            response = "Hello! I'm your custom AI assistant. Here's how to use inline code:\n\n"
            response += "Try using `print('Hello World')` in Python!\n\n"
        elif "code" in message.lower():
            # Show code block formatting
            response = "Here's a Python example:\n\n```python\ndef greet(name):\n    return f'Hello {name}!'\n\nresult = greet('Ontonaut')\nprint(result)\n```\n\n"
            response += "And here's JavaScript:\n\n```javascript\nconst greet = (name) => {\n  return `Hello ${name}!`;\n};\n\nconsole.log(greet('World'));\n```"
        elif "?" in message:
            response = f"Great question! Let me think about '{message}'... In a real implementation, this would connect to your backend."
        else:
            response = f"I understand you said: '{message}'. I'm a custom handler - implement your own logic here!"

        # Stream word by word
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    chatbot5 = ChatBot(
        handler=my_custom_handler,
        placeholder="Ask about 'code' to see formatting...",
        theme="dark",
    )
    chatbot5
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Building Your Own Handler

    ### Pattern 1: Simple Function
    ```python
    def my_handler(message: str):
        # Your logic here
        yield "Response chunk 1"
        yield "Response chunk 2"

    chatbot = ChatBot(handler=my_handler)
    ```

    ### Pattern 2: Class-Based Handler
    ```python
    from ontonaut.handlers import BaseHandler

    class MyHandler(BaseHandler):
        def __init__(self, config):
            self.config = config

        def __call__(self, message: str):
            # Your logic with self.config
            for chunk in process(message):
                yield chunk

    handler = MyHandler(config={...})
    chatbot = ChatBot(handler=handler)
    ```

    ### Pattern 3: Async Streaming (Future)
    ```python
    async def async_handler(message: str):
        async for chunk in stream_from_api(message):
            yield chunk

    chatbot = ChatBot(handler=async_handler)
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


if __name__ == "__main__":
    app.run()
