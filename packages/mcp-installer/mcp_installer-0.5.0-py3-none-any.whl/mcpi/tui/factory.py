"""TUI Adapter Factory - Creates TUI adapter instances.

This module provides a factory function for creating TUI adapter instances
based on configuration. It supports environment variable configuration and
defaults to the fzf adapter.

Environment Variables:
- MCPI_TUI_BACKEND: Specify which TUI backend to use (default: "fzf")
"""

import os
from typing import Optional

from mcpi.tui.adapters import FzfAdapter
from mcpi.tui.protocol import TUIAdapter


def get_tui_adapter(backend: Optional[str] = None) -> TUIAdapter:
    """Get a TUI adapter instance.

    Creates and returns a TUI adapter based on the specified backend name.
    If no backend is specified, checks the MCPI_TUI_BACKEND environment
    variable. Defaults to "fzf" if neither is set.

    Args:
        backend: TUI backend name ("fzf", "inquirerpy", etc.)
                Defaults to MCPI_TUI_BACKEND env var or "fzf"

    Returns:
        TUIAdapter instance (currently only FzfAdapter is supported)

    Raises:
        ValueError: If the specified backend is not supported

    Example:
        # Use default (fzf)
        adapter = get_tui_adapter()
        adapter.launch(manager, catalog)

        # Specify backend explicitly
        adapter = get_tui_adapter("fzf")
        adapter.launch(manager, catalog)

        # Use environment variable
        os.environ["MCPI_TUI_BACKEND"] = "fzf"
        adapter = get_tui_adapter()
        adapter.launch(manager, catalog)
    """
    # Determine which backend to use
    if backend is None:
        backend = os.environ.get("MCPI_TUI_BACKEND", "fzf")

    # Normalize backend name (case-insensitive)
    backend = backend.lower()

    # Create appropriate adapter
    if backend == "fzf":
        return FzfAdapter()
    else:
        # For future expansion: inquirerpy, textual, etc.
        raise ValueError(
            f"Unsupported TUI backend: {backend}\n"
            f"Supported backends: fzf\n"
            f"Future backends: inquirerpy, textual"
        )
