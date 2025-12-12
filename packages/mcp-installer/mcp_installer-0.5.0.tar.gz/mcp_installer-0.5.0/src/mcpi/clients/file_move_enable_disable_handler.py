"""File-based move enable/disable handler for user-global scope.

This handler implements a custom disable mechanism for user-global MCP servers
by MOVING server configurations between two files:
- Active file: ~/.claude/settings.json (contains ENABLED servers)
- Disabled file: ~/.claude/disabled-mcp.json (contains DISABLED servers)

REQUIREMENT (from CLAUDE.md lines 406-411):
- disable operation: MOVE server config FROM active file TO disabled file
- enable operation: MOVE server config FROM disabled file TO active file
- list operation: Show servers from BOTH files with correct enabled/disabled state

This is fundamentally different from FileTrackedEnableDisableHandler which just
tracks disabled server IDs. This handler actually moves the full configuration.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from .protocols import ConfigReader, ConfigWriter


class FileMoveEnableDisableHandler:
    """Enable/disable handler that moves server configs between active and disabled files.

    This handler is specifically designed for user-global scope where:
    - Active file: ~/.claude/settings.json
    - Disabled file: ~/.claude/disabled-mcp.json

    When a server is disabled:
    1. Read server config from active file
    2. Remove it from active file's mcpServers
    3. Add it to disabled file's mcpServers
    4. Write both files

    When a server is enabled:
    1. Read server config from disabled file
    2. Remove it from disabled file's mcpServers
    3. Add it to active file's mcpServers
    4. Write both files
    """

    def __init__(
        self,
        active_file_path: Path,
        disabled_file_path: Path,
        reader: ConfigReader,
        writer: ConfigWriter,
    ) -> None:
        """Initialize the file-move handler.

        Args:
            active_file_path: Path to active config file (e.g., ~/.claude/settings.json)
            disabled_file_path: Path to disabled config file (e.g., ~/.claude/disabled-mcp.json)
            reader: Configuration file reader
            writer: Configuration file writer
        """
        self.active_file_path = active_file_path
        self.disabled_file_path = disabled_file_path
        self.reader = reader
        self.writer = writer

    def is_disabled(self, server_id: str) -> bool:
        """Check if a server is disabled.

        A server is disabled if it exists in the disabled file.

        Args:
            server_id: Server identifier

        Returns:
            True if server is in disabled file
        """
        if not self.disabled_file_path.exists():
            return False

        try:
            disabled_data = self.reader.read(self.disabled_file_path)
            disabled_servers = disabled_data.get("mcpServers", {})
            return server_id in disabled_servers
        except Exception:
            return False

    def disable_server(self, server_id: str) -> bool:
        """Disable a server by MOVING its config from active to disabled file.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded, False otherwise
        """
        try:
            # Step 1: Read active file
            if not self.active_file_path.exists():
                return False  # Can't disable if active file doesn't exist

            active_data = self.reader.read(self.active_file_path)
            active_servers = active_data.get("mcpServers", {})

            # Step 2: Verify server exists in active file
            if server_id not in active_servers:
                return False  # Can't disable if server not in active file

            # Step 3: Extract server config
            server_config = active_servers[server_id]

            # Step 4: Remove from active file
            del active_servers[server_id]
            active_data["mcpServers"] = active_servers

            # Step 5: Read or create disabled file
            if self.disabled_file_path.exists():
                disabled_data = self.reader.read(self.disabled_file_path)
            else:
                disabled_data = {"mcpServers": {}}

            disabled_servers = disabled_data.get("mcpServers", {})

            # Step 6: Add to disabled file
            disabled_servers[server_id] = server_config
            disabled_data["mcpServers"] = disabled_servers

            # Step 7: Write both files
            self.writer.write(self.active_file_path, active_data)
            self.writer.write(self.disabled_file_path, disabled_data)

            return True

        except Exception as e:
            # Log error for debugging (in production, use proper logging)
            print(f"Error disabling server '{server_id}': {e}")
            return False

    def enable_server(self, server_id: str) -> bool:
        """Enable a server by MOVING its config from disabled to active file.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded, False otherwise
        """
        try:
            # Step 1: Read disabled file
            if not self.disabled_file_path.exists():
                return False  # Can't enable if disabled file doesn't exist

            disabled_data = self.reader.read(self.disabled_file_path)
            disabled_servers = disabled_data.get("mcpServers", {})

            # Step 2: Verify server exists in disabled file
            if server_id not in disabled_servers:
                return False  # Can't enable if server not in disabled file

            # Step 3: Extract server config
            server_config = disabled_servers[server_id]

            # Step 4: Remove from disabled file
            del disabled_servers[server_id]
            disabled_data["mcpServers"] = disabled_servers

            # Step 5: Read active file
            if self.active_file_path.exists():
                active_data = self.reader.read(self.active_file_path)
            else:
                # Should not happen in practice, but handle gracefully
                active_data = {"mcpEnabled": True, "mcpServers": {}}

            active_servers = active_data.get("mcpServers", {})

            # Step 6: Add to active file
            active_servers[server_id] = server_config
            active_data["mcpServers"] = active_servers

            # Step 7: Write both files
            self.writer.write(self.active_file_path, active_data)
            self.writer.write(self.disabled_file_path, disabled_data)

            return True

        except Exception as e:
            # Log error for debugging (in production, use proper logging)
            print(f"Error enabling server '{server_id}': {e}")
            return False

    def get_disabled_servers(self) -> Dict[str, Any]:
        """Get all servers from the disabled file.

        This is used by list_servers to show disabled servers.

        Returns:
            Dictionary mapping server IDs to their configurations
        """
        if not self.disabled_file_path.exists():
            return {}

        try:
            disabled_data = self.reader.read(self.disabled_file_path)
            return disabled_data.get("mcpServers", {})
        except Exception:
            return {}
