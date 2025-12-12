"""Test harness for testing MCPI with real file operations."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

import pytest

from mcpi.clients.claude_code import ClaudeCodePlugin
from mcpi.clients.manager import MCPManager
from mcpi.clients.registry import ClientRegistry


class MCPTestHarness:
    """Test harness for MCP client file operations."""

    def __init__(self, tmp_dir: Path):
        """Initialize test harness.

        Args:
            tmp_dir: Temporary directory for test files
        """
        self.tmp_dir = tmp_dir
        self.file_contents: Dict[str, Any] = {}
        self.path_overrides: Dict[str, Path] = {}

    def setup_scope_files(self, client_name: str = "claude-code") -> Dict[str, Path]:
        """Set up file paths for all scopes in the tmp directory.

        Args:
            client_name: Name of the client

        Returns:
            Dictionary mapping scope names to file paths
        """
        # Define all scopes we want to test
        # NOTE: user-mcp scope was removed because ~/.claude/settings.json
        # is NOT used for MCP servers by Claude Code.
        scopes = [
            "project-mcp",
            "project-local",
            "user-local",
            "user-internal",
            "user-mcp",
        ]

        # Create path overrides for each scope
        for scope_name in scopes:
            # Determine original filename based on scope
            if scope_name == "project-mcp":
                original = ".mcp.json"
            elif scope_name == "project-local":
                original = "settings.local.json"
            elif scope_name == "user-local":
                original = "settings.local.json"
            elif scope_name == "user-internal":
                original = ".claude.json"
            elif scope_name == "user-mcp":
                original = ".mcp.json"
            else:
                original = "config.json"

            # Create the test file path
            file_path = self.tmp_dir / f"{client_name}_{scope_name}_{original}"
            self.path_overrides[scope_name] = file_path

        # NOTE: user-mcp scope was removed because ~/.claude/settings.json
        # is NOT used for MCP servers by Claude Code.

        # Add disabled files for scopes using file-move mechanism
        # These store disabled server configurations

        # project-mcp: .mcp.disabled.json
        project_mcp_disabled_file = (
            self.tmp_dir / f"{client_name}_project-mcp-disabled_.mcp.disabled.json"
        )
        self.path_overrides["project-mcp-disabled"] = project_mcp_disabled_file

        # user-internal: ~/.claude/.disabled-servers.json
        user_internal_disabled_file = (
            self.tmp_dir
            / f"{client_name}_user-internal-disabled_.disabled-servers.json"
        )
        self.path_overrides["user-internal-disabled"] = user_internal_disabled_file

        # user-mcp: ~/.mcp.disabled.json
        user_mcp_disabled_file = (
            self.tmp_dir / f"{client_name}_user-mcp-disabled_.mcp.disabled.json"
        )
        self.path_overrides["user-mcp-disabled"] = user_mcp_disabled_file

        # Add path overrides for plugin scope
        # These ensure plugin discovery reads from test files, not real user files
        plugin_settings_file = self.tmp_dir / f"{client_name}_plugin-settings.json"
        self.path_overrides["plugin-settings"] = plugin_settings_file

        plugin_installed_file = (
            self.tmp_dir / f"{client_name}_plugin-installed_plugins.json"
        )
        self.path_overrides["plugin-installed"] = plugin_installed_file

        return self.path_overrides

    def prepopulate_file(self, scope_name: str, content: Dict[str, Any]) -> None:
        """Prepopulate a scope file with test data.

        Args:
            scope_name: Name of the scope
            content: Content to write to the file
        """
        if scope_name not in self.path_overrides:
            raise ValueError(
                f"Scope '{scope_name}' not set up. Call setup_scope_files first."
            )

        file_path = self.path_overrides[scope_name]
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as f:
            json.dump(content, f, indent=2)

        self.file_contents[scope_name] = content

    def read_scope_file(self, scope_name: str) -> Optional[Dict[str, Any]]:
        """Read and parse a scope file.

        Args:
            scope_name: Name of the scope

        Returns:
            Parsed JSON content or None if file doesn't exist
        """
        if scope_name not in self.path_overrides:
            raise ValueError(f"Scope '{scope_name}' not set up.")

        file_path = self.path_overrides[scope_name]

        if not file_path.exists():
            return None

        with open(file_path) as f:
            return json.load(f)

    def assert_valid_json(self, scope_name: str) -> None:
        """Assert that a scope file contains valid JSON.

        Args:
            scope_name: Name of the scope

        Raises:
            AssertionError: If file doesn't exist or contains invalid JSON
        """
        file_path = self.path_overrides.get(scope_name)
        assert file_path is not None, f"Scope '{scope_name}' not set up"
        assert file_path.exists(), f"File for scope '{scope_name}' does not exist"

        try:
            self.read_scope_file(scope_name)
        except json.JSONDecodeError as e:
            raise AssertionError(f"Invalid JSON in scope '{scope_name}': {e}")

    def assert_server_exists(self, scope_name: str, server_id: str) -> None:
        """Assert that a server exists in a scope file.

        Args:
            scope_name: Name of the scope
            server_id: Server ID to check

        Raises:
            AssertionError: If server doesn't exist
        """
        content = self.read_scope_file(scope_name)
        assert content is not None, f"No content in scope '{scope_name}'"

        # Handle different file formats
        if scope_name in ["project-mcp", "user-mcp"]:
            # MCP config format: {"mcpServers": {...}}
            servers = content.get("mcpServers", {})
        elif scope_name in ["project-local", "user-local"]:
            # Claude settings format: {"mcpEnabled": true, "mcpServers": {...}}
            servers = content.get("mcpServers", {})
        elif scope_name == "user-internal":
            # Internal config format: {"mcpServers": {...}}
            servers = content.get("mcpServers", {})
        else:
            servers = content

        assert (
            server_id in servers
        ), f"Server '{server_id}' not found in scope '{scope_name}'"

    def get_server_config(
        self, scope_name: str, server_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get the configuration for a specific server.

        Args:
            scope_name: Name of the scope
            server_id: Server ID

        Returns:
            Server configuration or None if not found
        """
        content = self.read_scope_file(scope_name)
        if content is None:
            return None

        # Handle different file formats
        if scope_name in ["project-mcp", "user-mcp"]:
            servers = content.get("mcpServers", {})
        elif scope_name in ["project-local", "user-local"]:
            servers = content.get("mcpServers", {})
        elif scope_name == "user-internal":
            servers = content.get("mcpServers", {})
        else:
            servers = content

        return servers.get(server_id)

    def assert_server_command(
        self, scope_name: str, server_id: str, expected_command: str
    ) -> None:
        """Assert that a server has the expected command.

        Args:
            scope_name: Name of the scope
            server_id: Server ID
            expected_command: Expected command value

        Raises:
            AssertionError: If command doesn't match
        """
        config = self.get_server_config(scope_name, server_id)
        assert (
            config is not None
        ), f"Server '{server_id}' not found in scope '{scope_name}'"
        assert (
            config.get("command") == expected_command
        ), f"Expected command '{expected_command}', got '{config.get('command')}'"

    def count_servers_in_scope(self, scope_name: str) -> int:
        """Count the number of servers in a scope.

        Args:
            scope_name: Name of the scope

        Returns:
            Number of servers
        """
        content = self.read_scope_file(scope_name)
        if content is None:
            return 0

        # Handle different file formats
        if scope_name in ["project-mcp", "user-mcp"]:
            servers = content.get("mcpServers", {})
        elif scope_name in ["project-local", "user-local"]:
            servers = content.get("mcpServers", {})
        elif scope_name == "user-internal":
            servers = content.get("mcpServers", {})
        else:
            servers = content

        return len(servers)


@pytest.fixture
def mcp_test_dir(tmp_path):
    """Create a temporary directory for MCP testing.

    Returns:
        Path to temporary directory
    """
    test_dir = tmp_path / "mcp_test"
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


@pytest.fixture
def mcp_harness(mcp_test_dir):
    """Create an MCP test harness.

    Args:
        mcp_test_dir: Temporary directory fixture

    Returns:
        MCPTestHarness instance
    """
    harness = MCPTestHarness(mcp_test_dir)
    harness.setup_scope_files()
    return harness


@pytest.fixture
def mcp_manager_with_harness(mcp_harness):
    """Create an MCP manager with test harness configuration.

    Args:
        mcp_harness: Test harness fixture

    Returns:
        Tuple of (MCPManager, MCPTestHarness)
    """
    # Create a custom ClaudeCodePlugin with path overrides
    custom_plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

    # Create a registry and inject our custom plugin
    registry = ClientRegistry(auto_discover=False)
    registry.inject_client_instance("claude-code", custom_plugin)

    # Create manager with our custom registry
    # Create manager with our custom registry - FIXED: pass registry parameter
    manager = MCPManager(registry=registry, default_client="claude-code")
    return manager, mcp_harness


@pytest.fixture
def prepopulated_harness(mcp_harness):
    """Create a harness with pre-populated test data.

    Args:
        mcp_harness: Test harness fixture

    Returns:
        MCPTestHarness with sample data
    """
    # Add some sample servers to different scopes

    # User-mcp scope with a couple servers (~/.mcp.json)
    mcp_harness.prepopulate_file(
        "user-mcp",
        {
            "mcpServers": {
                "filesystem": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                    "type": "stdio",
                },
                "github": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-github"],
                    "env": {"GITHUB_TOKEN": "test-token"},
                    "type": "stdio",
                },
            },
        },
    )

    # Project-mcp scope with a project-specific server
    mcp_harness.prepopulate_file(
        "project-mcp",
        {
            "mcpServers": {
                "project-tool": {
                    "command": "python",
                    "args": ["-m", "project_mcp_server"],
                    "type": "stdio",
                }
            },
            "enabledMcpServers": ["project-tool"],
        },
    )

    # User-internal with a regular server and a disabled server
    mcp_harness.prepopulate_file(
        "user-internal",
        {
            "mcpServers": {
                "internal-server": {
                    "command": "node",
                    "args": ["internal-server.js"],
                    "type": "stdio",
                },
                "disabled-server": {
                    "command": "node",
                    "args": ["disabled-server.js"],
                    "type": "stdio",
                    "disabled": True,
                },
            }
        },
    )

    # User-local settings with a disabled server (using Claude's actual format)
    mcp_harness.prepopulate_file(
        "user-local",
        {
            "enabledMcpjsonServers": ["filesystem"],
            "disabledMcpjsonServers": ["disabled-server"],
            "mcpServers": {
                "disabled-server": {
                    "command": "node",
                    "args": ["disabled-server.js"],
                    "type": "stdio",
                }
            },
        },
    )

    return mcp_harness
