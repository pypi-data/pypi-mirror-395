"""Enable/disable handler implementations for different scope types."""

from pathlib import Path
from typing import Any, Dict, List

from .disabled_tracker import DisabledServersTracker
from .protocols import ConfigReader, ConfigWriter, EnableDisableHandler


class ArrayBasedEnableDisableHandler:
    """Enable/disable handler using enabledMcpjsonServers/disabledMcpjsonServers arrays.

    This handler is used for scopes like project-local and user-local that support
    the enabledMcpjsonServers and disabledMcpjsonServers arrays in their settings file.
    """

    def __init__(
        self, config_path: Path, reader: ConfigReader, writer: ConfigWriter
    ) -> None:
        """Initialize the array-based handler.

        Args:
            config_path: Path to the configuration file
            reader: Configuration file reader
            writer: Configuration file writer
        """
        self.config_path = config_path
        self.reader = reader
        self.writer = writer

    def is_disabled(self, server_id: str) -> bool:
        """Check if a server is disabled.

        Args:
            server_id: Server identifier

        Returns:
            True if server is in disabledMcpjsonServers array
        """
        if not self.config_path.exists():
            return False

        try:
            data = self.reader.read(self.config_path)
            disabled_servers = data.get("disabledMcpjsonServers", [])
            return server_id in disabled_servers
        except Exception:
            return False

    def disable_server(self, server_id: str) -> bool:
        """Mark a server as disabled by adding to disabledMcpjsonServers array.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded
        """
        try:
            # Read current data
            if self.config_path.exists():
                data = self.reader.read(self.config_path)
            else:
                data = {}

            # Initialize arrays if needed
            enabled_servers = data.get("enabledMcpjsonServers", [])
            disabled_servers = data.get("disabledMcpjsonServers", [])

            # Remove from enabled if present
            if server_id in enabled_servers:
                enabled_servers.remove(server_id)

            # Add to disabled if not already there
            if server_id not in disabled_servers:
                disabled_servers.append(server_id)

            # Update data
            data["enabledMcpjsonServers"] = enabled_servers
            data["disabledMcpjsonServers"] = disabled_servers

            # Write back
            self.writer.write(self.config_path, data)
            return True

        except Exception:
            return False

    def enable_server(self, server_id: str) -> bool:
        """Mark a server as enabled by adding to enabledMcpjsonServers array.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded
        """
        try:
            # Read current data
            if self.config_path.exists():
                data = self.reader.read(self.config_path)
            else:
                data = {}

            # Initialize arrays if needed
            enabled_servers = data.get("enabledMcpjsonServers", [])
            disabled_servers = data.get("disabledMcpjsonServers", [])

            # Remove from disabled if present
            if server_id in disabled_servers:
                disabled_servers.remove(server_id)

            # Add to enabled if not already there
            if server_id not in enabled_servers:
                enabled_servers.append(server_id)

            # Update data
            data["enabledMcpjsonServers"] = enabled_servers
            data["disabledMcpjsonServers"] = disabled_servers

            # Write back
            self.writer.write(self.config_path, data)
            return True

        except Exception:
            return False


class FileTrackedEnableDisableHandler:
    """Enable/disable handler using a separate disabled tracking file.

    This handler is used for scopes like user-global that don't support
    enabledMcpjsonServers/disabledMcpjsonServers arrays in their configuration format.
    Instead, disabled servers are tracked in a separate JSON file.
    """

    def __init__(self, tracker: DisabledServersTracker) -> None:
        """Initialize the file-tracked handler.

        Args:
            tracker: Disabled servers tracker instance
        """
        self.tracker = tracker

    def is_disabled(self, server_id: str) -> bool:
        """Check if a server is disabled.

        Args:
            server_id: Server identifier

        Returns:
            True if server is in disabled tracking file
        """
        return self.tracker.is_disabled(server_id)

    def disable_server(self, server_id: str) -> bool:
        """Mark a server as disabled by adding to tracking file.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded
        """
        return self.tracker.disable(server_id)

    def enable_server(self, server_id: str) -> bool:
        """Mark a server as enabled by removing from tracking file.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded
        """
        return self.tracker.enable(server_id)


class InlineEnableDisableHandler:
    """Enable/disable handler using inline 'disabled' field in server config.

    This handler is used for scopes like project-mcp that use .mcp.json format,
    which doesn't support enabledMcpjsonServers/disabledMcpjsonServers arrays.
    Instead, each server can have a 'disabled' field directly in its configuration.
    """

    def __init__(
        self, config_path: Path, reader: ConfigReader, writer: ConfigWriter
    ) -> None:
        """Initialize the inline handler.

        Args:
            config_path: Path to the configuration file
            reader: Configuration file reader
            writer: Configuration file writer
        """
        self.config_path = config_path
        self.reader = reader
        self.writer = writer

    def is_disabled(self, server_id: str) -> bool:
        """Check if a server is disabled.

        Args:
            server_id: Server identifier

        Returns:
            True if server has 'disabled' field set to true
        """
        if not self.config_path.exists():
            return False

        try:
            data = self.reader.read(self.config_path)
            servers = data.get("mcpServers", {})
            server_config = servers.get(server_id, {})
            return server_config.get("disabled") is True
        except Exception:
            return False

    def disable_server(self, server_id: str) -> bool:
        """Mark a server as disabled by setting 'disabled': true in config.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded
        """
        try:
            # Read current data
            if not self.config_path.exists():
                return False  # Can't disable if config doesn't exist

            data = self.reader.read(self.config_path)

            # Get servers
            servers = data.get("mcpServers", {})
            if server_id not in servers:
                return False  # Can't disable if server doesn't exist

            # Set disabled flag
            servers[server_id]["disabled"] = True

            # Write back
            self.writer.write(self.config_path, data)
            return True

        except Exception:
            return False

    def enable_server(self, server_id: str) -> bool:
        """Mark a server as enabled by removing 'disabled' field from config.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded
        """
        try:
            # Read current data
            if not self.config_path.exists():
                return False  # Can't enable if config doesn't exist

            data = self.reader.read(self.config_path)

            # Get servers
            servers = data.get("mcpServers", {})
            if server_id not in servers:
                return False  # Can't enable if server doesn't exist

            # Remove disabled flag if present
            if "disabled" in servers[server_id]:
                del servers[server_id]["disabled"]

            # Write back
            self.writer.write(self.config_path, data)
            return True

        except Exception:
            return False


class ApprovalRequiredEnableDisableHandler:
    """Enable/disable handler for scopes that require approval arrays.

    Used for project-mcp scope where servers must be explicitly approved
    via enabledMcpjsonServers array in .claude/settings.local.json

    State Detection Logic (priority order):
    1. Inline disabled=true in .mcp.json → DISABLED
    2. Server in disabledMcpjsonServers → DISABLED
    3. Server in enabledMcpjsonServers → ENABLED
    4. Server not in either array → DISABLED (not approved - security default)

    This handler reads from TWO files:
    - .mcp.json: For server configs and inline disabled field
    - .claude/settings.local.json: For approval arrays
    """

    def __init__(
        self,
        mcp_json_path: Path,
        settings_local_path: Path,
        reader: ConfigReader,
        writer: ConfigWriter,
    ) -> None:
        """Initialize the approval-required handler.

        Args:
            mcp_json_path: Path to .mcp.json file (for inline disabled field)
            settings_local_path: Path to .claude/settings.local.json (approval arrays)
            reader: JSON file reader for DIP
            writer: JSON file writer for DIP
        """
        self.mcp_json_path = mcp_json_path
        self.settings_local_path = settings_local_path
        self.reader = reader
        self.writer = writer

    def is_disabled(self, server_id: str) -> bool:
        """Check if a server is disabled.

        Implements the full approval logic:
        1. Check inline disabled field in .mcp.json (highest priority)
        2. Check disabledMcpjsonServers array
        3. Check enabledMcpjsonServers array
        4. Default to disabled if not in either array (security default)

        Args:
            server_id: Server identifier

        Returns:
            True if server is disabled, False if enabled
        """
        # Step 1: Check inline disabled field in .mcp.json (highest priority)
        if self.mcp_json_path.exists():
            try:
                mcp_data = self.reader.read(self.mcp_json_path)
                servers = mcp_data.get("mcpServers", {})
                server_config = servers.get(server_id, {})
                if server_config.get("disabled") is True:
                    return True  # Inline disabled field takes precedence
            except Exception:
                # If we can't read .mcp.json, fail-safe to disabled
                pass

        # Step 2-4: Check approval arrays in settings.local.json
        if not self.settings_local_path.exists():
            # No approval file = not approved = disabled (security default)
            return True

        try:
            settings_data = self.reader.read(self.settings_local_path)
            enabled_servers = settings_data.get("enabledMcpjsonServers", [])
            disabled_servers = settings_data.get("disabledMcpjsonServers", [])

            # Check if in disabled array (step 2)
            if server_id in disabled_servers:
                return True

            # Check if in enabled array (step 3)
            if server_id in enabled_servers:
                return False

            # Not in either array = not approved = disabled (step 4 - security default)
            return True

        except Exception:
            # If we can't read approval file, fail-safe to disabled
            return True

    def enable_server(self, server_id: str) -> bool:
        """Enable a server by adding to enabledMcpjsonServers array.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded
        """
        try:
            # Read current settings (or create empty)
            if self.settings_local_path.exists():
                data = self.reader.read(self.settings_local_path)
            else:
                # Create parent directory if needed
                self.settings_local_path.parent.mkdir(parents=True, exist_ok=True)
                data = {}

            # Initialize arrays if needed
            enabled_servers = data.get("enabledMcpjsonServers", [])
            disabled_servers = data.get("disabledMcpjsonServers", [])

            # Remove from disabled if present
            if server_id in disabled_servers:
                disabled_servers.remove(server_id)

            # Add to enabled if not already there
            if server_id not in enabled_servers:
                enabled_servers.append(server_id)

            # Update data
            data["enabledMcpjsonServers"] = enabled_servers
            data["disabledMcpjsonServers"] = disabled_servers

            # Write back
            self.writer.write(self.settings_local_path, data)
            return True

        except Exception:
            return False

    def disable_server(self, server_id: str) -> bool:
        """Disable a server by adding to disabledMcpjsonServers array.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded
        """
        try:
            # Read current settings (or create empty)
            if self.settings_local_path.exists():
                data = self.reader.read(self.settings_local_path)
            else:
                # Create parent directory if needed
                self.settings_local_path.parent.mkdir(parents=True, exist_ok=True)
                data = {}

            # Initialize arrays if needed
            enabled_servers = data.get("enabledMcpjsonServers", [])
            disabled_servers = data.get("disabledMcpjsonServers", [])

            # Remove from enabled if present
            if server_id in enabled_servers:
                enabled_servers.remove(server_id)

            # Add to disabled if not already there
            if server_id not in disabled_servers:
                disabled_servers.append(server_id)

            # Update data
            data["enabledMcpjsonServers"] = enabled_servers
            data["disabledMcpjsonServers"] = disabled_servers

            # Write back
            self.writer.write(self.settings_local_path, data)
            return True

        except Exception:
            return False

    def get_disabled_servers(self) -> List[str]:
        """Get list of all disabled server IDs.

        This returns servers that are explicitly in the disabledMcpjsonServers array.
        Note: Servers that are simply unapproved (not in either array) are NOT
        included in this list, though they are considered disabled by is_disabled().

        Returns:
            List of server IDs in disabledMcpjsonServers array
        """
        if not self.settings_local_path.exists():
            return []

        try:
            data = self.reader.read(self.settings_local_path)
            return data.get("disabledMcpjsonServers", [])
        except Exception:
            return []

    def is_unapproved(self, server_id: str) -> bool:
        """Check if a server is unapproved (not in either enabled or disabled array).

        This is distinct from is_disabled() which returns True for both
        explicitly disabled AND unapproved servers.

        Args:
            server_id: Server identifier

        Returns:
            True if server is not in either enabledMcpjsonServers or disabledMcpjsonServers
        """
        # Check inline disabled field first - if disabled inline, it's not "unapproved"
        if self.mcp_json_path.exists():
            try:
                mcp_data = self.reader.read(self.mcp_json_path)
                servers = mcp_data.get("mcpServers", {})
                server_config = servers.get(server_id, {})
                if server_config.get("disabled") is True:
                    return False  # Explicitly disabled, not unapproved
            except Exception:
                pass

        # Check approval arrays
        if not self.settings_local_path.exists():
            # No approval file = unapproved
            return True

        try:
            settings_data = self.reader.read(self.settings_local_path)
            enabled_servers = settings_data.get("enabledMcpjsonServers", [])
            disabled_servers = settings_data.get("disabledMcpjsonServers", [])

            # Unapproved = not in either array
            return server_id not in enabled_servers and server_id not in disabled_servers

        except Exception:
            # Can't read file = assume unapproved
            return True
