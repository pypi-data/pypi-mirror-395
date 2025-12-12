"""TUI Package - Interactive terminal UI for MCPI.

This package provides interactive terminal user interfaces for managing MCP servers.
It uses a plugin architecture to support multiple TUI backends (fzf, InquirerPy, etc.).

Public API:
- get_tui_adapter(): Factory function to create TUI adapter instances
- launch_fzf_interface(): Backward compatibility wrapper for fzf

Internal Components:
- protocol: TUIAdapter protocol definition
- factory: Adapter factory function
- adapters: Concrete adapter implementations (fzf, etc.)
"""

from typing import Any, Dict, List, Optional

from mcpi.clients import MCPManager
from mcpi.clients.types import ServerState
from mcpi.registry.catalog import MCPServer, ServerCatalog
from mcpi.tui.factory import get_tui_adapter

# Re-export standalone functions for console scripts
from mcpi.tui.adapters.fzf import cycle_scope_and_reload, reload_server_list

__all__ = [
    "get_tui_adapter",
    "launch_fzf_interface",
    "reload_server_list",
    "cycle_scope_and_reload",
    # Backward compatibility exports for tests
    "check_fzf_installed",
    "get_server_status",
    "format_server_line",
    "build_server_list",
    "build_fzf_command",
]


# =============================================================================
# Backward Compatibility Wrappers for Tests
# These delegate to the FzfAdapter implementation
# =============================================================================


def check_fzf_installed() -> bool:
    """Check if fzf is installed and available.

    Backward compatibility wrapper for tests.

    Returns:
        True if fzf is installed, False otherwise
    """
    from mcpi.tui.adapters.fzf import FzfAdapter

    adapter = FzfAdapter()
    return adapter._check_fzf_installed()


def get_server_status(
    manager: MCPManager, server_id: str, client: Optional[str] = None
) -> Dict[str, Any]:
    """Get the current status of a server.

    Backward compatibility wrapper for tests.

    Args:
        manager: MCP manager instance
        server_id: Server identifier
        client: Optional client name

    Returns:
        Dictionary with installation status and state information
    """
    from mcpi.tui.adapters.fzf import FzfAdapter

    adapter = FzfAdapter()
    return adapter._get_server_status(manager, server_id, client)


def format_server_line(
    server_id: str, server: MCPServer, status: Dict[str, Any]
) -> str:
    """Format a server as a line for fzf display.

    Backward compatibility wrapper for tests.

    Args:
        server_id: Server identifier
        server: Server catalog entry
        status: Server status dictionary from get_server_status

    Returns:
        Formatted line with ANSI color codes
    """
    from mcpi.tui.adapters.fzf import FzfAdapter

    adapter = FzfAdapter()
    return adapter._format_server_line(server_id, server, status)


def build_server_list(catalog: ServerCatalog, manager: MCPManager) -> List[str]:
    """Build the complete server list for fzf.

    Backward compatibility wrapper for tests.

    Args:
        catalog: Server catalog
        manager: MCP manager

    Returns:
        List of formatted server lines
    """
    from mcpi.tui.adapters.fzf import FzfAdapter

    adapter = FzfAdapter()
    return adapter._build_server_list(catalog, manager)


def build_fzf_command(current_scope: Optional[str] = None) -> List[str]:
    """Build the fzf command with all options and bindings.

    Backward compatibility wrapper for tests.

    Args:
        current_scope: Current target scope to display in header (optional)

    Returns:
        List of command arguments for subprocess
    """
    from mcpi.tui.adapters.fzf import FzfAdapter

    adapter = FzfAdapter()
    return adapter._build_fzf_command(current_scope)


# =============================================================================
# Public API
# =============================================================================


def launch_fzf_interface(
    manager: MCPManager,
    catalog: ServerCatalog,
    initial_scope: Optional[str] = None,
) -> None:
    """Launch the interactive fzf interface.

    This is a backward compatibility wrapper that uses the new adapter pattern.
    New code should use get_tui_adapter() directly.

    Args:
        manager: MCP manager instance
        catalog: Server catalog instance
        initial_scope: Starting scope (optional)

    Raises:
        RuntimeError: If fzf is not installed

    Example:
        # Old way (still works)
        from mcpi.tui import launch_fzf_interface
        launch_fzf_interface(manager, catalog)

        # New way (recommended)
        from mcpi.tui import get_tui_adapter
        adapter = get_tui_adapter("fzf")
        adapter.launch(manager, catalog)
    """
    adapter = get_tui_adapter("fzf")
    adapter.launch(manager, catalog, initial_scope)
