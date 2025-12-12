"""TUI Adapter Protocol - Defines interface for pluggable TUI backends.

This module defines the protocol (interface) that all TUI adapters must implement.
This allows MCPI to support multiple TUI libraries (fzf, InquirerPy, Textual, etc.)
without changing the CLI code.

Architecture:
    CLI → TUIAdapter (protocol) → Concrete adapter (FzfAdapter, InquirerPyAdapter, etc.)

Example:
    adapter = get_tui_adapter()  # Returns FzfAdapter by default
    adapter.launch(servers, current_scope, on_selection)
"""

from dataclasses import dataclass
from typing import Callable, List, Optional, Protocol, Tuple

from mcpi.clients.manager import MCPManager
from mcpi.registry.catalog import ServerCatalog


@dataclass
class ServerSelection:
    """Result of user interaction with TUI."""

    server_id: str
    action: str  # "add", "remove", "enable", "disable", "info", "quit"
    scope: Optional[str] = None  # Scope selected for operation


class TUIAdapter(Protocol):
    """Protocol that all TUI adapters must implement.

    This defines the interface for pluggable TUI backends. Any TUI library
    (fzf, InquirerPy, Textual, etc.) can be used by implementing this protocol.
    """

    def launch(
        self,
        manager: MCPManager,
        catalog: ServerCatalog,
        initial_scope: Optional[str] = None,
    ) -> None:
        """Launch interactive TUI for managing MCP servers.

        The TUI should allow users to:
        - Fuzzy search through available servers
        - View server details (preview/info)
        - Perform operations: add, remove, enable, disable
        - Cycle through scopes (project-mcp, user-global, etc.)
        - Exit gracefully

        Args:
            manager: MCPManager instance for server operations
            catalog: ServerCatalog instance for server registry
            initial_scope: Starting scope (defaults to first available)

        Note:
            This method blocks until user exits the TUI. It handles the
            entire interaction loop internally.
        """
        ...

    def get_name(self) -> str:
        """Return human-readable name of this TUI adapter.

        Returns:
            Name like "fzf", "inquirerpy", "textual"
        """
        ...

    def get_version(self) -> str:
        """Return version of the underlying TUI library.

        Returns:
            Version string like "0.54.3" for fzf
        """
        ...


# Type alias for readability
ServerListItem = Tuple[str, str, str, str]  # (status, server_id, name, description)
