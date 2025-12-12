"""Claude Code specific MCP server installer."""

import json
import os
import platform
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcpi.installer.base import BaseInstaller, InstallationResult
from mcpi.registry.catalog import MCPServer

# Configuration constants
MCP_SERVERS_KEY = "mcpServers"


class ClaudeCodeInstaller(BaseInstaller):
    """Installer for Claude Code MCP server integration.

    Note: With the simplified MCPServer catalog format, this installer
    no longer handles package installation. It simply adds server
    configurations to Claude Code's MCP config file.
    """

    def __init__(self, config_path: Optional[Path] = None, dry_run: bool = False):
        """Initialize Claude Code installer.

        Args:
            config_path: Path to Claude Code MCP configuration file
            dry_run: If True, simulate installation without making changes
        """
        if config_path is None:
            config_path = self._find_claude_code_config()

        super().__init__(config_path=config_path, dry_run=dry_run)

    def _find_claude_code_config(self) -> Path:
        """Find Claude Code MCP configuration file.

        Returns:
            Path to Claude Code MCP configuration file
        """
        system = platform.system()

        if system == "Darwin":  # macOS
            config_path = Path.home() / ".claude" / "mcp_servers.json"
        elif system == "Linux":
            config_path = Path.home() / ".config" / "claude" / "mcp_servers.json"
        elif system == "Windows":
            appdata = Path(os.environ.get("APPDATA", str(Path.home())))
            config_path = appdata / "claude" / "mcp_servers.json"
        else:
            # Fallback to home directory
            config_path = Path.home() / ".claude" / "mcp_servers.json"

        return config_path

    def _load_config(self) -> Dict[str, Any]:
        """Load Claude Code MCP configuration.

        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            return {MCP_SERVERS_KEY: {}}

        try:
            with open(self.config_path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {MCP_SERVERS_KEY: {}}

    def _save_config(self, config: Dict[str, Any]) -> bool:
        """Save Claude Code MCP configuration.

        Args:
            config: Configuration to save

        Returns:
            True if save successful, False otherwise
        """
        if self.dry_run:
            return True

        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            return True
        except OSError:
            return False

    def install(
        self,
        server: MCPServer,
        server_id: str,
        config_params: Optional[Dict[str, Any]] = None,
    ) -> InstallationResult:
        """Install MCP server for Claude Code.

        Args:
            server: MCP server to install
            server_id: Server ID (catalog key)
            config_params: Configuration parameters

        Returns:
            Installation result
        """
        if config_params is None:
            config_params = {}

        # Validate installation requirements
        validation_errors = self.validate_installation(server, server_id)
        if validation_errors:
            return self._create_failure_result(
                server_id,
                f"Validation failed: {'; '.join(validation_errors)}",
                validation_errors=validation_errors,
            )

        # Check if already installed
        if self.is_installed(server_id):
            return self._create_failure_result(
                server_id,
                f"Server {server_id} is already installed",
                already_installed=True,
            )

        # Create backup of existing configuration
        backup_path = self.create_backup(self.config_path)

        # Load current configuration
        config = self._load_config()

        # Generate server configuration from catalog entry
        server_config = self._generate_server_config(server, config_params)

        # Add server to configuration
        config[MCP_SERVERS_KEY][server_id] = server_config

        # Save updated configuration
        if not self._save_config(config):
            return self._create_failure_result(
                server_id,
                "Failed to save Claude Code configuration",
                backup_path=backup_path,
            )

        return self._create_success_result(
            server_id,
            f"Successfully installed {server_id} for Claude Code",
            config_path=self.config_path,
            backup_path=backup_path,
            server_config=server_config,
        )

    def _generate_server_config(
        self,
        server: MCPServer,
        config_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate Claude Code server configuration.

        Args:
            server: MCP server (from catalog)
            config_params: User-provided configuration parameters

        Returns:
            Claude Code server configuration
        """
        # Start with command and args from catalog
        config = {"command": server.command, "args": server.args.copy()}

        # Add environment variables if provided
        if "env" in config_params:
            config["env"] = config_params["env"]

        # Add any additional args from config_params
        if "args" in config_params:
            config["args"].extend(config_params["args"])

        return config

    def uninstall(self, server_id: str) -> InstallationResult:
        """Uninstall MCP server from Claude Code.

        Args:
            server_id: ID of server to uninstall

        Returns:
            Installation result
        """
        if not self.is_installed(server_id):
            return self._create_failure_result(
                server_id, f"Server {server_id} is not installed"
            )

        # Create backup
        backup_path = self.create_backup(self.config_path)

        # Load configuration
        config = self._load_config()

        # Remove server from configuration
        if server_id in config.get(MCP_SERVERS_KEY, {}):
            del config[MCP_SERVERS_KEY][server_id]

        # Save updated configuration
        if not self._save_config(config):
            return self._create_failure_result(
                server_id,
                "Failed to save Claude Code configuration",
                backup_path=backup_path,
            )

        return self._create_success_result(
            server_id,
            f"Successfully uninstalled {server_id} from Claude Code",
            config_path=self.config_path,
            backup_path=backup_path,
        )

    def is_installed(self, server_id: str) -> bool:
        """Check if server is installed in Claude Code.

        Args:
            server_id: Server ID to check

        Returns:
            True if installed, False otherwise
        """
        config = self._load_config()
        return server_id in config.get(MCP_SERVERS_KEY, {})

    def get_installed_servers(self) -> List[str]:
        """Get list of installed server IDs.

        Returns:
            List of installed server IDs
        """
        config = self._load_config()
        return list(config.get(MCP_SERVERS_KEY, {}).keys())

    def get_server_config(self, server_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for installed server.

        Args:
            server_id: Server ID

        Returns:
            Server configuration or None if not found
        """
        config = self._load_config()
        return config.get(MCP_SERVERS_KEY, {}).get(server_id)

    def update_server_config(self, server_id: str, new_config: Dict[str, Any]) -> bool:
        """Update configuration for installed server.

        Args:
            server_id: Server ID
            new_config: New configuration

        Returns:
            True if update successful, False otherwise
        """
        if not self.is_installed(server_id):
            return False

        config = self._load_config()
        config[MCP_SERVERS_KEY][server_id] = new_config

        return self._save_config(config)

    def validate_config(self) -> List[str]:
        """Validate Claude Code MCP configuration.

        Returns:
            List of validation errors
        """
        errors = []

        if not self.config_path.exists():
            errors.append(f"Configuration file does not exist: {self.config_path}")
            return errors

        config = self._load_config()

        if MCP_SERVERS_KEY not in config:
            errors.append(f"Configuration missing '{MCP_SERVERS_KEY}' section")
            return errors

        for server_id, server_config in config[MCP_SERVERS_KEY].items():
            if not isinstance(server_config, dict):
                errors.append(f"Server {server_id}: Configuration must be an object")
                continue

            if "command" not in server_config:
                errors.append(f"Server {server_id}: Missing 'command' field")

            if "args" not in server_config:
                errors.append(f"Server {server_id}: Missing 'args' field")
            elif not isinstance(server_config["args"], list):
                errors.append(f"Server {server_id}: 'args' must be an array")

        return errors
