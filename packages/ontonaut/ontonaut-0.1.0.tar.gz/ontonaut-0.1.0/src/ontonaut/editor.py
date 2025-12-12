"""Main code editor widget using Anywidget."""

from pathlib import Path
from typing import Any, Callable, Optional

import anywidget
import traitlets


class CodeEditor(anywidget.AnyWidget):
    """
    A customizable code editor widget for marimo.

    The editor follows marimo's clean visual style and allows custom
    execution backends for any language or DSL.

    Attributes:
        code: The current code in the editor
        language: Syntax highlighting language (e.g., 'python', 'javascript', 'custom')
        theme: Editor theme ('light' or 'dark')
        output: Execution output from the last run
        executor: Custom function to execute code (receives code string, returns output)

    Examples:
        >>> # Basic Python executor
        >>> editor = CodeEditor(language="python")
        >>> editor.executor = lambda code: eval(code)
        >>>
        >>> # Custom language executor
        >>> def my_lang_executor(code: str) -> str:
        ...     # Custom parsing and execution logic
        ...     return f"Executed: {code}"
        >>> editor = CodeEditor(language="mylang", executor=my_lang_executor)
    """

    # Get the directory containing this file
    _esm = Path(__file__).parent / "static" / "editor.js"
    _css = Path(__file__).parent / "static" / "editor.css"

    # Widget state synchronized between Python and JavaScript
    code = traitlets.Unicode("").tag(sync=True)
    language = traitlets.Unicode("python").tag(sync=True)
    theme = traitlets.Unicode("light").tag(sync=True)
    output = traitlets.Unicode("").tag(sync=True)
    error = traitlets.Unicode("").tag(sync=True)
    placeholder = traitlets.Unicode("Enter code here...").tag(sync=True)
    read_only = traitlets.Bool(False).tag(sync=True)
    line_numbers = traitlets.Bool(True).tag(sync=True)

    def __init__(
        self,
        code: str = "",
        language: str = "python",
        theme: str = "light",
        executor: Optional[Callable[[str], Any]] = None,
        placeholder: str = "Enter code here...",
        read_only: bool = False,
        line_numbers: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the code editor.

        Args:
            code: Initial code to display
            language: Programming language for syntax highlighting
            theme: Editor theme ('light' or 'dark')
            executor: Function that takes code string and returns execution result
            placeholder: Placeholder text when editor is empty
            read_only: Whether the editor is read-only
            line_numbers: Whether to show line numbers
            **kwargs: Additional arguments passed to AnyWidget
        """
        super().__init__(**kwargs)
        self.code = code
        self.language = language
        self.theme = theme
        self.placeholder = placeholder
        self.read_only = read_only
        self.line_numbers = line_numbers
        self._executor = executor

        # Listen for execution requests from the frontend
        self.on_msg(self._handle_execute_request)

    @property
    def executor(self) -> Optional[Callable[[str], Any]]:
        """Get the current executor function."""
        return self._executor

    @executor.setter
    def executor(self, func: Optional[Callable[[str], Any]]) -> None:
        """Set the executor function."""
        self._executor = func

    def _handle_execute_request(
        self, widget: Any, content: dict, buffers: list
    ) -> None:
        """
        Handle code execution requests from the frontend.

        Args:
            widget: The widget instance
            content: Message content with 'type' and 'code'
            buffers: Binary buffers (unused)
        """
        if content.get("type") == "execute":
            code_to_execute = content.get("code", self.code)
            self.execute(code_to_execute)

    def execute(self, code: Optional[str] = None) -> Any:
        """
        Execute code using the configured executor.

        Args:
            code: Code to execute. If None, uses current editor code.

        Returns:
            The result from the executor function.
        """
        if code is None:
            code = self.code

        if self._executor is None:
            self.error = "No executor configured"
            self.output = ""
            return None

        try:
            result = self._executor(code)
            self.output = str(result) if result is not None else ""
            self.error = ""
            return result
        except Exception as e:
            self.error = f"{type(e).__name__}: {str(e)}"
            self.output = ""
            return None

    def set_code(self, code: str) -> None:
        """
        Set the editor code.

        Args:
            code: Code to set in the editor
        """
        self.code = code

    def get_code(self) -> str:
        """
        Get the current editor code.

        Returns:
            Current code string
        """
        return self.code

    def clear(self) -> None:
        """Clear the editor and output."""
        self.code = ""
        self.output = ""
        self.error = ""
