"""TUI Adapters - Pluggable TUI backend implementations.

This package contains concrete implementations of the TUIAdapter protocol.
Each adapter wraps a different TUI library (fzf, InquirerPy, Textual, etc.).
"""

from mcpi.tui.adapters.fzf import FzfAdapter

__all__ = ["FzfAdapter"]
