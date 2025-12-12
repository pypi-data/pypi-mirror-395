"""Debug logging utilities for shell completion.

This module provides a clean, centralized way to debug shell completion issues
without cluttering the main code with logging statements.

Usage:
    from mcpi.utils.completion_debug import CompletionLogger

    logger = CompletionLogger.get_logger()
    logger.log("Starting completion", context=ctx, incomplete=incomplete)
    logger.log("Found servers", count=len(servers))
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime


class CompletionLogger:
    """Centralized logger for shell completion debugging.

    This logger writes to ~/.mcpi_completion_debug.log when debug mode is enabled.
    Debug mode is enabled by:
    1. Setting MCPI_DEBUG environment variable
    2. Setting MCPI_COMPLETION_DEBUG environment variable
    3. Using --debug flag on CLI (sets context flag)
    """

    _instance: Optional["CompletionLogger"] = None
    _log_file: Path = Path.home() / ".mcpi_completion_debug.log"
    _enabled: Optional[bool] = None

    def __init__(self):
        """Initialize the logger."""
        self._session_start = datetime.now()

    @classmethod
    def get_logger(cls) -> "CompletionLogger":
        """Get the singleton logger instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def is_enabled(cls, ctx: Any = None) -> bool:
        """Check if debug logging is enabled.

        Args:
            ctx: Optional Click context (checks for debug flag)

        Returns:
            True if debugging is enabled
        """
        # Check environment variables first (always takes precedence)
        if os.environ.get("MCPI_DEBUG") or os.environ.get("MCPI_COMPLETION_DEBUG"):
            return True

        # Check context for --debug flag
        if ctx and hasattr(ctx, "obj") and ctx.obj:
            if ctx.obj.get("debug", False):
                return True

        # Check parent context
        if ctx and hasattr(ctx, "parent") and ctx.parent:
            if hasattr(ctx.parent, "obj") and ctx.parent.obj:
                if ctx.parent.obj.get("debug", False):
                    return True

        return False

    def log(self, message: str, ctx: Any = None, **kwargs: Any) -> None:
        """Log a message if debugging is enabled.

        Args:
            message: The message to log
            ctx: Optional Click context
            **kwargs: Additional key-value pairs to log
        """
        if not self.is_enabled(ctx):
            return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            with open(self._log_file, "a") as f:
                f.write(f"\n[{timestamp}] {message}\n")

                # Log additional context
                for key, value in kwargs.items():
                    f.write(f"  {key}: {self._format_value(value)}\n")

        except Exception:
            # Silently fail - don't break completion if logging fails
            pass

    def log_section(self, title: str, ctx: Any = None) -> None:
        """Log a section separator.

        Args:
            title: Section title
            ctx: Optional Click context
        """
        if not self.is_enabled(ctx):
            return

        try:
            with open(self._log_file, "a") as f:
                f.write(f"\n{'=' * 70}\n")
                f.write(f"  {title}\n")
                f.write(f"{'=' * 70}\n")
        except Exception:
            pass

    def log_error(self, error: Exception, ctx: Any = None, **kwargs: Any) -> None:
        """Log an error with traceback.

        Args:
            error: The exception to log
            ctx: Optional Click context
            **kwargs: Additional context
        """
        if not self.is_enabled(ctx):
            return

        try:
            import traceback

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            with open(self._log_file, "a") as f:
                f.write(f"\n[{timestamp}] ERROR: {str(error)}\n")

                # Log additional context
                for key, value in kwargs.items():
                    f.write(f"  {key}: {self._format_value(value)}\n")

                # Log traceback
                f.write("\nTraceback:\n")
                f.write(traceback.format_exc())
                f.write("\n")

        except Exception:
            pass

    def clear_log(self) -> None:
        """Clear the debug log file."""
        try:
            if self._log_file.exists():
                self._log_file.unlink()
        except Exception:
            pass

    @staticmethod
    def _format_value(value: Any) -> str:
        """Format a value for logging.

        Args:
            value: The value to format

        Returns:
            Formatted string representation
        """
        if value is None:
            return "None"

        if isinstance(value, (str, int, float, bool)):
            return repr(value)

        if isinstance(value, (list, tuple)):
            if len(value) == 0:
                return "[]" if isinstance(value, list) else "()"
            if len(value) <= 5:
                return repr(value)
            return f"[{len(value)} items: {repr(value[:3])}...]"

        if isinstance(value, dict):
            if len(value) == 0:
                return "{}"
            if len(value) <= 3:
                return repr(value)
            keys = list(value.keys())[:3]
            return f"{{{len(value)} items: {keys}...}}"

        # For objects, try to show useful info
        if hasattr(value, "__dict__"):
            return f"{type(value).__name__}(...)"

        return str(value)


# Convenience function for quick logging
def log_completion(message: str, ctx: Any = None, **kwargs: Any) -> None:
    """Quick logging function for completion debugging.

    Args:
        message: Message to log
        ctx: Optional Click context
        **kwargs: Additional key-value pairs
    """
    logger = CompletionLogger.get_logger()
    logger.log(message, ctx=ctx, **kwargs)
