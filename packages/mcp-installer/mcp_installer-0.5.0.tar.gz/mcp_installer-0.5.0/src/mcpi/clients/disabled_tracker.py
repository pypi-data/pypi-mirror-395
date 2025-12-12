"""Disabled servers tracking for scopes that don't support enable/disable arrays.

This module provides a separate file-based mechanism for tracking disabled servers
in scopes like user-global that don't have enabledMcpjsonServers/disabledMcpjsonServers
arrays in their configuration files.
"""

import json
from pathlib import Path
from typing import List, Set


class DisabledServersTracker:
    """Tracks disabled servers in a separate file.

    This is used for scopes like user-global that don't have enable/disable arrays
    in their configuration format. The disabled servers are tracked in a separate
    JSON file to avoid modifying the official Claude settings format.
    """

    def __init__(self, tracking_file: Path):
        """Initialize the disabled servers tracker.

        Args:
            tracking_file: Path to the JSON file that tracks disabled servers
        """
        self.tracking_file = tracking_file

    def is_disabled(self, server_id: str) -> bool:
        """Check if a server is disabled.

        Args:
            server_id: Server identifier

        Returns:
            True if server is disabled, False otherwise
        """
        disabled = self._read_disabled_servers()
        return server_id in disabled

    def disable(self, server_id: str) -> bool:
        """Mark a server as disabled.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded, False otherwise
        """
        try:
            disabled = self._read_disabled_servers()
            if server_id not in disabled:
                disabled.add(server_id)
                self._write_disabled_servers(disabled)
            return True
        except Exception:
            return False

    def enable(self, server_id: str) -> bool:
        """Remove a server from the disabled list.

        Args:
            server_id: Server identifier

        Returns:
            True if operation succeeded, False otherwise
        """
        try:
            disabled = self._read_disabled_servers()
            if server_id in disabled:
                disabled.remove(server_id)
                self._write_disabled_servers(disabled)
            return True
        except Exception:
            return False

    def get_disabled_servers(self) -> List[str]:
        """Get list of all disabled servers.

        Returns:
            List of disabled server IDs
        """
        return sorted(self._read_disabled_servers())

    def _read_disabled_servers(self) -> Set[str]:
        """Read the set of disabled servers from file.

        Returns:
            Set of disabled server IDs
        """
        if not self.tracking_file.exists():
            return set()

        try:
            with self.tracking_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                # Support both array format and the more verbose format
                if isinstance(data, list):
                    return set(data)
                elif isinstance(data, dict) and "disabled" in data:
                    return set(data["disabled"])
                else:
                    return set()
        except (json.JSONDecodeError, OSError):
            return set()

    def _write_disabled_servers(self, disabled: Set[str]) -> None:
        """Write the set of disabled servers to file.

        Args:
            disabled: Set of disabled server IDs
        """
        # Ensure directory exists
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)

        # Write as a simple JSON array for easy manual editing
        with self.tracking_file.open("w", encoding="utf-8") as f:
            json.dump(sorted(disabled), f, indent=2)
