"""ChatBot widget with streaming support for marimo."""

from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from typing import Any, Callable, Optional, Union

import anywidget
import traitlets


class ChatBot(anywidget.AnyWidget):
    """
    A chat interface widget for marimo with streaming support.

    Perfect for building AI chatbots with custom backends like OpenAI,
    Anthropic, or custom MCP servers.

    Attributes:
        messages: List of chat messages [{"role": "user|assistant", "content": "..."}]
        input_text: Current input text
        is_streaming: Whether a response is currently streaming
        handler: Custom function to handle messages and generate responses

    Examples:
        >>> # Basic OpenAI streaming
        >>> import openai
        >>> def openai_handler(message: str):
        ...     stream = openai.chat.completions.create(
        ...         model="gpt-4",
        ...         messages=[{"role": "user", "content": message}],
        ...         stream=True
        ...     )
        ...     for chunk in stream:
        ...         if chunk.choices[0].delta.content:
        ...             yield chunk.choices[0].delta.content
        >>>
        >>> chatbot = ChatBot(handler=openai_handler)
        >>>
        >>> # Custom MCP server
        >>> def mcp_handler(message: str):
        ...     # Your MCP logic here
        ...     yield from process_with_tools(message)
        >>>
        >>> chatbot = ChatBot(handler=mcp_handler)
    """

    # Frontend assets
    _esm = Path(__file__).parent / "static" / "chatbot.js"
    _css = Path(__file__).parent / "static" / "chatbot.css"

    # Widget state (like CodeEditor + tabs)
    input_text = traitlets.Unicode("").tag(sync=True)
    output = traitlets.Unicode("").tag(sync=True)
    error = traitlets.Unicode("").tag(sync=True)
    is_streaming = traitlets.Bool(False).tag(sync=True)
    placeholder = traitlets.Unicode("Ask me anything...").tag(sync=True)
    theme = traitlets.Unicode("light").tag(sync=True)
    language = traitlets.Unicode("text").tag(sync=True)
    # Tabs: list of {"title": str, "content": str, "input": str}
    tabs: list[dict[str, str]] = traitlets.List([]).tag(sync=True)  # type: ignore[assignment]
    active_tab = traitlets.Int(0).tag(sync=True)  # Current tab index

    def __init__(
        self,
        handler: Optional[
            Callable[[str], Union[str, Iterator[str], AsyncIterator[str]]]
        ] = None,
        input_text: str = "",
        placeholder: str = "Ask me anything...",
        theme: str = "light",
        language: str = "text",
        **kwargs: Any,
    ) -> None:
        """
        Initialize the streaming widget.

        Args:
            handler: Function that takes input and returns/streams response
            input_text: Initial input text
            placeholder: Input placeholder text
            theme: UI theme ('light' or 'dark')
            language: Output language for syntax highlighting
            **kwargs: Additional arguments passed to AnyWidget
        """
        super().__init__(**kwargs)
        self._handler = handler
        self._last_input: str = ""  # Track last input for tab creation
        self.input_text = input_text
        self.placeholder = placeholder
        self.theme = theme
        self.language = language

        # Listen for messages from frontend
        self.on_msg(self._handle_execute)

    @property
    def handler(
        self,
    ) -> Optional[Callable[[str], Union[str, Iterator[str], AsyncIterator[str]]]]:
        """Get the current message handler."""
        return self._handler

    @handler.setter
    def handler(
        self, func: Callable[[str], Union[str, Iterator[str], AsyncIterator[str]]]
    ) -> None:
        """Set the message handler."""
        self._handler = func

    def _handle_execute(self, widget: Any, content: dict, buffers: list) -> None:
        """
        Handle execution requests from the frontend.

        Args:
            widget: The widget instance
            content: Message content with 'type' and 'input'
            buffers: Binary buffers (unused)
        """
        if content.get("type") == "execute":
            user_input = content.get("input", self.input_text)
            if user_input:
                self.execute(user_input)

    def execute(self, input_text: Optional[str] = None) -> Any:
        """
        Execute input using the configured handler.

        Args:
            input_text: Input to execute. If None, uses current input_text.

        Returns:
            The result from the handler function.
        """
        if input_text is None:
            input_text = self.input_text

        if self._handler is None:
            self.error = "No handler configured"
            self.output = ""
            return None

        # Save previous output to a tab if exists (using the PREVIOUS input)
        if self.output and hasattr(self, "_last_input"):
            self._save_to_tab(self._last_input, self.output)

        # Store current input for next execution
        self._last_input = input_text

        # Clear for new execution
        self.output = ""
        self.error = ""

        try:
            self.is_streaming = True
            response = self._handler(input_text)

            # Handle different response types
            if isinstance(response, str):
                # Simple string response
                self.output = response
            elif hasattr(response, "__iter__") and not isinstance(response, str):
                # Streaming response (generator/iterator)
                self._stream_response(response)  # type: ignore[arg-type]
            else:
                # Fallback
                self.output = str(response)

            return response

        except Exception as e:
            self.error = f"{type(e).__name__}: {str(e)}"
            self.output = ""
            return None
        finally:
            self.is_streaming = False

    def _stream_response(self, stream: Iterator[str]) -> None:
        """
        Stream a response chunk by chunk.

        Args:
            stream: Iterator yielding response chunks
        """
        full_content = ""
        try:
            for chunk in stream:
                if chunk:
                    full_content += chunk
                    # Update output in real-time (like streaming terminal)
                    self.output = full_content
        except Exception as e:
            # Handle streaming errors
            self.error = f"Stream error: {type(e).__name__}: {str(e)}"
            self.output = full_content

    def _save_to_tab(self, input_text: str, output_text: str) -> None:
        """
        Save current output to a new tab.

        Args:
            input_text: The input that generated this output
            output_text: The output to save
        """
        # Create tab title from input (first 30 chars)
        title = input_text[:30] + "..." if len(input_text) > 30 else input_text

        new_tab = {
            "title": title,
            "content": output_text,
            "input": input_text,
        }

        self.tabs = self.tabs + [new_tab]
        # Set active tab to the newest (current output stays visible)
        self.active_tab = -1  # -1 means "current" tab

    def clear(self) -> None:
        """Clear input, output, and errors."""
        self.input_text = ""
        self.output = ""
        self.error = ""

    def clear_all(self) -> None:
        """Clear everything including all tabs."""
        self.input_text = ""
        self.output = ""
        self.error = ""
        self.tabs = []
        self.active_tab = 0

    def get_tab(self, index: int) -> Optional[dict[str, str]]:
        """
        Get tab at index.

        Args:
            index: Tab index

        Returns:
            Tab dict or None if invalid index
        """
        if 0 <= index < len(self.tabs):
            return dict(self.tabs[index])
        return None
