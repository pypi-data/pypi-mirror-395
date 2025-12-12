"""Tests for ChatBot widget."""

from ontonaut import ChatBot, EchoHandler


class TestChatBot:
    """Tests for the ChatBot widget (simple streaming input/output)."""

    def test_chatbot_initialization(self) -> None:
        """Test chatbot initializes with default values."""
        chatbot = ChatBot()

        assert chatbot.input_text == ""
        assert chatbot.output == ""
        assert chatbot.error == ""
        assert chatbot.is_streaming is False
        assert chatbot.theme == "light"
        assert chatbot.placeholder == "Ask me anything..."

    def test_chatbot_execute_simple(self) -> None:
        """Test executing with simple handler."""

        def simple_handler(input_text: str) -> str:
            return f"Response: {input_text}"

        chatbot = ChatBot(handler=simple_handler)
        chatbot.execute("Test input")

        assert chatbot.output == "Response: Test input"
        assert chatbot.error == ""

    def test_chatbot_streaming_handler(self) -> None:
        """Test chatbot with streaming handler."""

        def streaming_handler(input_text: str):
            yield from ["Hello", " ", "World", "!"]

        chatbot = ChatBot(handler=streaming_handler)
        chatbot.execute("Test")

        assert chatbot.output == "Hello World!"
        assert chatbot.error == ""

    def test_chatbot_no_handler(self) -> None:
        """Test chatbot without handler."""
        chatbot = ChatBot()
        chatbot.execute("Test")

        assert chatbot.output == ""
        assert chatbot.error == "No handler configured"

    def test_chatbot_handler_error(self) -> None:
        """Test chatbot with handler that raises error."""

        def error_handler(input_text: str) -> str:
            raise ValueError("Test error")

        chatbot = ChatBot(handler=error_handler)
        chatbot.execute("Test")

        assert chatbot.output == ""
        assert "ValueError: Test error" in chatbot.error

    def test_chatbot_clear(self) -> None:
        """Test clearing chatbot."""
        chatbot = ChatBot(input_text="test input")
        chatbot.output = "test output"
        chatbot.error = "test error"

        chatbot.clear()

        assert chatbot.input_text == ""
        assert chatbot.output == ""
        assert chatbot.error == ""

    def test_chatbot_handler_property(self) -> None:
        """Test getting and setting handler property."""
        chatbot = ChatBot()
        assert chatbot.handler is None

        def test_handler(input_text: str) -> str:
            return "test"

        chatbot.handler = test_handler
        assert chatbot.handler == test_handler

        chatbot.execute("input")
        assert chatbot.output == "test"

    def test_chatbot_theme(self) -> None:
        """Test different themes."""
        light_chatbot = ChatBot(theme="light")
        dark_chatbot = ChatBot(theme="dark")

        assert light_chatbot.theme == "light"
        assert dark_chatbot.theme == "dark"

    def test_chatbot_custom_placeholder(self) -> None:
        """Test custom placeholder."""
        chatbot = ChatBot(placeholder="Custom placeholder...")
        assert chatbot.placeholder == "Custom placeholder..."

    def test_chatbot_with_initial_input(self) -> None:
        """Test chatbot with initial input text."""
        chatbot = ChatBot(input_text="Initial input")
        assert chatbot.input_text == "Initial input"

    def test_chatbot_tabs_creation(self) -> None:
        """Test that executing creates tabs for previous outputs."""

        def simple_handler(input_text: str) -> str:
            return f"Response: {input_text}"

        chatbot = ChatBot(handler=simple_handler)

        # First execution
        chatbot.execute("Question 1")
        assert chatbot.output == "Response: Question 1"
        assert len(chatbot.tabs) == 0  # No tab yet

        # Second execution should save first output to tab
        chatbot.execute("Question 2")
        assert len(chatbot.tabs) == 1
        assert chatbot.tabs[0]["input"] == "Question 1"
        assert chatbot.tabs[0]["content"] == "Response: Question 1"
        assert chatbot.output == "Response: Question 2"

        # Third execution
        chatbot.execute("Question 3")
        assert len(chatbot.tabs) == 2
        assert chatbot.output == "Response: Question 3"

    def test_chatbot_get_tab(self) -> None:
        """Test getting tab by index."""

        def handler(text: str) -> str:
            return f"Output: {text}"

        chatbot = ChatBot(handler=handler)
        chatbot.execute("First")
        chatbot.execute("Second")

        # Get first tab
        tab = chatbot.get_tab(0)
        assert tab is not None
        assert tab["input"] == "First"
        assert tab["content"] == "Output: First"

        # Invalid index
        assert chatbot.get_tab(999) is None

    def test_chatbot_clear_all(self) -> None:
        """Test clearing all tabs and output."""

        def handler(text: str) -> str:
            return f"Output: {text}"

        chatbot = ChatBot(handler=handler)
        chatbot.execute("First")
        chatbot.execute("Second")
        assert len(chatbot.tabs) == 1

        chatbot.clear_all()
        assert len(chatbot.tabs) == 0
        assert chatbot.output == ""
        assert chatbot.input_text == ""


class TestEchoHandler:
    """Tests for EchoHandler."""

    def test_echo_handler(self) -> None:
        """Test echo handler functionality."""
        handler = EchoHandler(delay=0)
        result = list(handler("Hello"))

        assert "".join(result) == "Echo: Hello"

    def test_echo_handler_with_chatbot(self) -> None:
        """Test echo handler integration with chatbot."""
        handler = EchoHandler(delay=0)
        chatbot = ChatBot(handler=handler)

        chatbot.execute("Test")

        assert chatbot.output == "Echo: Test"
        assert chatbot.error == ""
