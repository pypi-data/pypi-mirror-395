"""Chat handlers for different backends (OpenAI, Anthropic, MCP, etc.)."""

import time
from collections.abc import Iterator
from typing import Any, Optional


class BaseHandler:
    """Base class for chat handlers."""

    def __call__(self, message: str) -> Iterator[str]:
        """
        Handle a message and yield response chunks.

        Args:
            message: User message

        Yields:
            Response chunks
        """
        raise NotImplementedError("Subclasses must implement __call__")


class EchoHandler(BaseHandler):
    """
    Simple echo handler for testing.

    Streams the user's message back character by character.

    Examples:
        >>> handler = EchoHandler(delay=0.05)
        >>> chatbot = ChatBot(handler=handler)
    """

    def __init__(self, delay: float = 0.03) -> None:
        """
        Initialize echo handler.

        Args:
            delay: Delay between characters (seconds)
        """
        self.delay = delay

    def __call__(self, message: str) -> Iterator[str]:
        """Echo the message back, streaming."""
        for char in f"Echo: {message}":
            yield char
            time.sleep(self.delay)


class OpenAIHandler(BaseHandler):
    """
    Handler for OpenAI API with streaming support.

    Requires: pip install openai

    Examples:
        >>> from ontonaut.handlers import OpenAIHandler
        >>> handler = OpenAIHandler(
        ...     api_key="your-key",
        ...     model="gpt-4",
        ...     system_prompt="You are a helpful assistant."
        ... )
        >>> chatbot = ChatBot(handler=handler)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize OpenAI handler.

        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: Model name (gpt-4, gpt-3.5-turbo, etc.)
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            **kwargs: Additional arguments for OpenAI API
        """
        try:
            import openai  # type: ignore[import-not-found,unused-ignore]
        except ImportError as e:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            ) from e

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs
        self.conversation_history: list[dict[str, str]] = []

        if system_prompt:
            self.conversation_history.append(
                {"role": "system", "content": system_prompt}
            )

    def __call__(self, message: str) -> Iterator[str]:
        """
        Send message to OpenAI and stream response.

        Args:
            message: User message

        Yields:
            Response chunks from OpenAI
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
                **self.kwargs,
            )

            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content

            # Add assistant response to history
            self.conversation_history.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            yield f"Error: {type(e).__name__}: {str(e)}"

    def clear_history(self) -> None:
        """Clear conversation history (keeping system prompt if set)."""
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append(
                {"role": "system", "content": self.system_prompt}
            )


class AnthropicHandler(BaseHandler):
    """
    Handler for Anthropic Claude API with streaming.

    Requires: pip install anthropic

    Examples:
        >>> from ontonaut.handlers import AnthropicHandler
        >>> handler = AnthropicHandler(
        ...     api_key="your-key",
        ...     model="claude-3-opus-20240229"
        ... )
        >>> chatbot = ChatBot(handler=handler)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-opus-20240229",
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
        **kwargs: Any,
    ) -> None:
        """
        Initialize Anthropic handler.

        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Model name (claude-3-opus, claude-3-sonnet, etc.)
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens in response
            **kwargs: Additional arguments for Anthropic API
        """
        try:
            import anthropic  # type: ignore[import-not-found]
        except ImportError as e:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            ) from e

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.kwargs = kwargs
        self.conversation_history: list[dict[str, str]] = []

    def __call__(self, message: str) -> Iterator[str]:
        """
        Send message to Anthropic and stream response.

        Args:
            message: User message

        Yields:
            Response chunks from Claude
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})

        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=self.conversation_history,
                system=self.system_prompt,
                **self.kwargs,
            ) as stream:
                full_response = ""
                for text in stream.text_stream:
                    full_response += text
                    yield text

            # Add assistant response to history
            self.conversation_history.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            yield f"Error: {type(e).__name__}: {str(e)}"


class MCPHandler(BaseHandler):
    """
    Handler for Model Context Protocol (MCP) servers.

    Allows integration with MCP tools and context providers.

    Examples:
        >>> from ontonaut.handlers import MCPHandler
        >>> handler = MCPHandler(
        ...     tools=[calculate_tool, search_tool],
        ...     context_provider=get_context
        ... )
        >>> chatbot = ChatBot(handler=handler)
    """

    def __init__(
        self,
        llm_handler: BaseHandler,
        tools: Optional[list[Any]] = None,
        context_provider: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize MCP handler.

        Args:
            llm_handler: Underlying LLM handler (OpenAI, Anthropic, etc.)
            tools: List of MCP tools
            context_provider: Function to provide additional context
            **kwargs: Additional arguments
        """
        self.llm_handler = llm_handler
        self.tools = tools or []
        self.context_provider = context_provider
        self.kwargs = kwargs

    def __call__(self, message: str) -> Iterator[str]:
        """
        Process message with MCP tools and stream response.

        Args:
            message: User message

        Yields:
            Response chunks
        """
        # Get additional context if provider exists
        context = ""
        if self.context_provider:
            try:
                context = self.context_provider(message)
                if context:
                    yield f"[Context: {context}]\n\n"
            except Exception as e:
                yield f"[Context error: {e}]\n\n"

        # Check if tools should be invoked
        # This is simplified - real MCP would parse tool calls from LLM
        enhanced_message = message
        if context:
            enhanced_message = f"Context: {context}\n\nUser: {message}"

        # Stream from underlying LLM
        yield from self.llm_handler(enhanced_message)


class CustomHandler(BaseHandler):
    """
    Custom handler that wraps any callable.

    Use this to create your own handlers with company-specific logic.

    Examples:
        >>> def my_company_handler(message: str):
        ...     # Your company's OpenAI wrapper
        ...     response = company_llm.query(message, stream=True)
        ...     for chunk in response:
        ...         yield chunk
        >>>
        >>> handler = CustomHandler(my_company_handler)
        >>> chatbot = ChatBot(handler=handler)
    """

    def __init__(self, func: Any) -> None:
        """
        Initialize custom handler.

        Args:
            func: Callable that takes a message and yields/returns response
        """
        self.func = func

    def __call__(self, message: str) -> Iterator[str]:
        """Call the wrapped function."""
        result = self.func(message)

        # Handle different return types
        if isinstance(result, str):
            yield result
        elif hasattr(result, "__iter__"):
            yield from result
        else:
            yield str(result)


def create_handler(
    backend: str,
    **kwargs: Any,
) -> BaseHandler:
    """
    Create a handler for a given backend.

    Args:
        backend: Backend name ('openai', 'anthropic', 'echo')
        **kwargs: Arguments passed to the handler

    Returns:
        Handler instance

    Examples:
        >>> handler = create_handler('openai', api_key='sk-...', model='gpt-4')
        >>> chatbot = ChatBot(handler=handler)
    """
    handlers = {
        "echo": EchoHandler,
        "openai": OpenAIHandler,
        "anthropic": AnthropicHandler,
    }

    handler_class = handlers.get(backend.lower())
    if not handler_class:
        raise ValueError(
            f"Unknown backend: {backend}. " f"Supported: {', '.join(handlers.keys())}"
        )

    instance = handler_class(**kwargs)
    return instance  # type: ignore[no-any-return]
