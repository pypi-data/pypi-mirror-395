"""Ontonaut - Customizable widgets for marimo with pluggable execution backends."""

__version__ = "0.1.0"
__author__ = "Ashley Cottrell"
__email__ = "your.email@example.com"

# Code Editor
# Chat Bot
from ontonaut.chatbot import ChatBot
from ontonaut.editor import CodeEditor
from ontonaut.executors import PythonExecutor, create_executor
from ontonaut.handlers import (
    AnthropicHandler,
    BaseHandler,
    CustomHandler,
    EchoHandler,
    MCPHandler,
    OpenAIHandler,
    create_handler,
)

__all__ = [
    # Editor
    "CodeEditor",
    "PythonExecutor",
    "create_executor",
    # ChatBot
    "ChatBot",
    "BaseHandler",
    "EchoHandler",
    "OpenAIHandler",
    "AnthropicHandler",
    "MCPHandler",
    "CustomHandler",
    "create_handler",
    # Meta
    "__version__",
]
