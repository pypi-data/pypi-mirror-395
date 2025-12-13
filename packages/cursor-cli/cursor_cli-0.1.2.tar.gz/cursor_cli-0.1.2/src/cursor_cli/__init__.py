"""
Cursor CLI - A wrapper for cursor-agent with formatted output support.
"""

from .runner import CursorCLIRunner, cursor_cli
from .formatter import StreamJsonFormatter

__version__ = "0.1.0"
__all__ = ["CursorCLIRunner", "StreamJsonFormatter", "cursor_cli"]
