"""Plugin-based MCP server discovery for Claude Code.

This module discovers MCP servers defined in Claude Code plugins.
Plugin servers are read-only and cannot be managed via mcpi.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .base import ScopeHandler
from .types import OperationResult, ScopeConfig, ServerConfig

logger = logging.getLogger(__name__)


class PluginBasedScope(ScopeHandler):
    """Scope handler that discovers MCP servers from Claude Code plugins.

    This scope reads enabled plugins from settings and discovers their MCP servers.
    Plugin servers are read-only - they cannot be added, removed, or updated via mcpi.

    Discovery process:
    1. Read ~/.claude/settings.json for enabledPlugins
    2. Read ~/.claude/plugins/installed_plugins.json for plugin install paths
    3. For each enabled plugin, read <installPath>/.claude-plugin/plugin.json
    4. Extract mcpServers from each plugin

    Server IDs are prefixed with plugin name: <plugin-name>:<server-id>
    Example: "beads:beads" for the beads server from the beads plugin
    """

    def __init__(
        self,
        config: ScopeConfig,
        settings_path: Optional[Path] = None,
        installed_plugins_path: Optional[Path] = None,
    ) -> None:
        """Initialize plugin-based scope.

        Args:
            config: Scope configuration
            settings_path: Path to settings.json (default: ~/.claude/settings.json)
            installed_plugins_path: Path to installed_plugins.json
                (default: ~/.claude/plugins/installed_plugins.json)
        """
        super().__init__(config)
        self._settings_path = settings_path or Path.home() / ".claude" / "settings.json"
        self._installed_plugins_path = (
            installed_plugins_path
            or Path.home() / ".claude" / "plugins" / "installed_plugins.json"
        )
        # Cache for discovered servers
        self._servers_cache: Optional[Dict[str, Dict[str, Any]]] = None

    def _read_json_file(self, path: Path) -> Optional[Dict[str, Any]]:
        """Read and parse a JSON file.

        Args:
            path: Path to JSON file

        Returns:
            Parsed JSON as dict, or None if file doesn't exist or is invalid
        """
        try:
            if not path.exists():
                return None
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Failed to read {path}: {e}")
            return None

    def _get_enabled_plugins(self) -> Dict[str, bool]:
        """Get enabled plugins from settings.json.

        Returns:
            Dict mapping plugin identifiers to enabled state
        """
        settings = self._read_json_file(self._settings_path)
        if not settings:
            return {}
        return settings.get("enabledPlugins", {})

    def _get_installed_plugins(self) -> Dict[str, Dict[str, Any]]:
        """Get installed plugins from installed_plugins.json.

        Returns:
            Dict mapping plugin identifiers to their metadata (including installPath)
        """
        data = self._read_json_file(self._installed_plugins_path)
        if not data:
            return {}
        return data.get("plugins", {})

    def _resolve_plugin_variables(
        self, value: Any, plugin_root: Path
    ) -> Any:
        """Resolve plugin variables like ${CLAUDE_PLUGIN_ROOT}.

        Args:
            value: Value to process (string, list, or dict)
            plugin_root: Path to plugin root directory

        Returns:
            Value with variables resolved
        """
        if isinstance(value, str):
            return value.replace("${CLAUDE_PLUGIN_ROOT}", str(plugin_root))
        elif isinstance(value, list):
            return [self._resolve_plugin_variables(item, plugin_root) for item in value]
        elif isinstance(value, dict):
            return {
                k: self._resolve_plugin_variables(v, plugin_root)
                for k, v in value.items()
            }
        return value

    def _discover_servers(self) -> Dict[str, Dict[str, Any]]:
        """Discover MCP servers from all enabled plugins.

        Returns:
            Dict mapping server IDs to their configurations
        """
        servers: Dict[str, Dict[str, Any]] = {}

        enabled_plugins = self._get_enabled_plugins()
        installed_plugins = self._get_installed_plugins()

        for plugin_id, is_enabled in enabled_plugins.items():
            if not is_enabled:
                continue

            # Get install info for this plugin
            install_info = installed_plugins.get(plugin_id)
            if not install_info:
                logger.debug(f"Plugin {plugin_id} is enabled but not installed")
                continue

            install_path = install_info.get("installPath")
            if not install_path:
                logger.debug(f"Plugin {plugin_id} has no installPath")
                continue

            # Read plugin.json
            plugin_dir = Path(install_path)
            plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
            plugin_data = self._read_json_file(plugin_json_path)

            if not plugin_data:
                logger.debug(f"No plugin.json found for {plugin_id} at {plugin_json_path}")
                continue

            # Get plugin name (used in server ID prefix)
            plugin_name = plugin_data.get("name", plugin_id.split("@")[0])

            # Extract MCP servers
            mcp_servers = plugin_data.get("mcpServers", {})
            if not mcp_servers:
                logger.debug(f"Plugin {plugin_id} has no MCP servers")
                continue

            # Add each server with prefixed ID
            for server_id, server_config in mcp_servers.items():
                # Resolve plugin variables in config
                resolved_config = self._resolve_plugin_variables(
                    server_config, plugin_dir
                )

                # Create prefixed server ID: <plugin-name>:<server-id>
                prefixed_id = f"{plugin_name}:{server_id}"

                # Add metadata about source
                resolved_config["_plugin_source"] = {
                    "plugin_id": plugin_id,
                    "plugin_name": plugin_name,
                    "install_path": str(plugin_dir),
                }

                servers[prefixed_id] = resolved_config
                logger.debug(f"Discovered plugin server: {prefixed_id}")

        return servers

    def _get_cached_servers(self) -> Dict[str, Dict[str, Any]]:
        """Get servers with caching.

        Returns:
            Dict mapping server IDs to their configurations
        """
        if self._servers_cache is None:
            self._servers_cache = self._discover_servers()
        return self._servers_cache

    def invalidate_cache(self) -> None:
        """Invalidate the server cache, forcing rediscovery on next access."""
        self._servers_cache = None

    def exists(self) -> bool:
        """Check if this scope's configuration exists.

        Returns True if there are any enabled plugins with MCP servers.
        """
        return len(self._get_cached_servers()) > 0

    def get_servers(self) -> Dict[str, Dict[str, Any]]:
        """Get all servers discovered from plugins.

        Returns:
            Dictionary mapping server IDs to their configurations
        """
        return self._get_cached_servers().copy()

    def add_server(self, server_id: str, config: ServerConfig) -> OperationResult:
        """Add a server (NOT SUPPORTED for plugin scope).

        Plugin servers are managed by the plugin system, not mcpi.
        """
        return OperationResult(
            success=False,
            message="Cannot add servers to plugin scope. Plugin servers are managed by Claude Code's plugin system.",
        )

    def remove_server(self, server_id: str) -> OperationResult:
        """Remove a server (NOT SUPPORTED for plugin scope).

        Plugin servers are managed by the plugin system, not mcpi.
        """
        return OperationResult(
            success=False,
            message="Cannot remove servers from plugin scope. Plugin servers are managed by Claude Code's plugin system.",
        )

    def update_server(self, server_id: str, config: ServerConfig) -> OperationResult:
        """Update a server (NOT SUPPORTED for plugin scope).

        Plugin servers are managed by the plugin system, not mcpi.
        """
        return OperationResult(
            success=False,
            message="Cannot update servers in plugin scope. Plugin servers are managed by Claude Code's plugin system.",
        )

    def get_server_config(self, server_id: str) -> Dict[str, Any]:
        """Get the full configuration for a specific server.

        Args:
            server_id: The ID of the server to retrieve

        Returns:
            Dictionary with full server configuration

        Raises:
            ValueError: If server doesn't exist in this scope
        """
        servers = self._get_cached_servers()
        if server_id not in servers:
            raise ValueError(f"Server '{server_id}' not found in plugin scope")
        return servers[server_id].copy()
