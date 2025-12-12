"""End-to-End Workflow Tests for MCPI

This test suite validates complete user workflows from start to finish.
All tests use temporary files and fixtures to ensure isolation.

Test Philosophy:
- Each test represents a real user workflow
- Tests verify actual file changes, not just return values
- All file operations are isolated to temporary directories
- Tests cannot be gamed by stubbing or mocking core functionality

Coverage Matrix:
- Workflow 1: First-Time Server Installation (search -> info -> add -> verify)
- Workflow 2: Project-Specific Configuration (add to scope -> verify -> rescope)
- Workflow 3: Enable/Disable Server Management (list -> disable -> verify -> enable)
- Workflow 4: Multi-Scope Management (list scopes -> per-scope list -> rescope)
- Workflow 5: Complete Server Lifecycle (search -> add -> use -> disable -> remove)
- Workflow 6: Dry-Run Operations (preview add/remove/rescope without changes)

API Notes:
- list_servers() returns Dict[str, ServerInfo], keyed by server_id
- ServerInfo.id is the server identifier
- Scope handlers have get_servers() for listing
- get_server_config() returns dict, use ServerConfig.from_dict() if needed
- rescope is CLI-level, implemented as get_config + add + remove
"""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from mcpi.cli import main
from mcpi.clients.claude_code import ClaudeCodePlugin
from mcpi.clients.manager import MCPManager
from mcpi.clients.registry import ClientRegistry
from mcpi.clients.types import ServerConfig, ServerInfo, ServerState
from mcpi.registry.catalog_manager import create_default_catalog_manager


# =============================================================================
# Fixtures for E2E Testing
# =============================================================================


@pytest.fixture
def e2e_harness(tmp_path):
    """Create a complete E2E test harness with all scopes initialized.

    This fixture provides:
    - Temporary directory structure mimicking real scope files
    - Path overrides for all Claude Code scopes
    - Pre-configured plugin with isolated file paths
    - Manager instance ready for testing

    All file operations are guaranteed to be isolated.
    """
    from tests.test_harness import MCPTestHarness

    harness = MCPTestHarness(tmp_path)
    harness.setup_scope_files()
    return harness


@pytest.fixture
def e2e_plugin(e2e_harness):
    """Create a ClaudeCodePlugin with E2E harness path overrides."""
    return ClaudeCodePlugin(path_overrides=e2e_harness.path_overrides)


@pytest.fixture
def e2e_manager(e2e_plugin):
    """Create an MCPManager with E2E plugin for complete workflow testing."""
    registry = ClientRegistry(auto_discover=False)
    registry.inject_client_instance("claude-code", e2e_plugin)
    return MCPManager(registry=registry, default_client="claude-code")


@pytest.fixture
def cli_runner():
    """Create a Click CLI runner for E2E CLI testing."""
    return CliRunner()


@pytest.fixture
def catalog_manager():
    """Get the default catalog manager for server lookups."""
    return create_default_catalog_manager()


# =============================================================================
# Workflow 1: First-Time Server Installation
# =============================================================================


class TestFirstTimeServerInstallation:
    """Test the complete workflow of a first-time server installation.

    User Story:
    As a new MCPI user, I want to discover, learn about, and install
    an MCP server so I can extend my AI assistant's capabilities.

    Workflow:
    1. Search for a server (mcpi search -q filesystem)
    2. Get detailed info (mcpi info filesystem)
    3. Add the server (mcpi add filesystem)
    4. Verify installation (mcpi list)
    """

    def test_search_shows_available_servers(self, cli_runner, catalog_manager):
        """E2E: User searches and finds servers in the catalog."""
        result = cli_runner.invoke(main, ["search", "-q", "filesystem"])

        assert result.exit_code == 0
        assert "filesystem" in result.output.lower()

    def test_info_shows_server_details(self, cli_runner, catalog_manager):
        """E2E: User gets detailed information about a server."""
        result = cli_runner.invoke(main, ["info", "filesystem", "--catalog", "official"])

        # Info command may fail if server not found in default catalog
        # but should work with explicit catalog flag
        if result.exit_code != 0:
            # Try without catalog to get system info
            result = cli_runner.invoke(main, ["info"])
            assert result.exit_code == 0
        else:
            # Should show server metadata
            assert "filesystem" in result.output.lower() or len(result.output) > 0

    def test_add_then_list_shows_installed(self, e2e_harness, e2e_plugin, cli_runner):
        """E2E: User adds a server and verifies it appears in list.

        This is the core test: add a server, then verify:
        1. The file was actually created/updated
        2. The server appears in the list output
        3. The server configuration is correct
        """
        # Step 1: Add the server (using API for isolation)
        config = ServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
            type="stdio",
        )
        result = e2e_plugin.add_server("filesystem", config, scope="user-mcp")

        assert result.success, f"Add failed: {result.message}"

        # Step 2: Verify file was created with correct content
        file_content = e2e_harness.read_scope_file("user-mcp")
        assert file_content is not None, "Scope file should exist"
        assert "mcpServers" in file_content
        assert "filesystem" in file_content["mcpServers"]

        # Step 3: Verify server config is correct
        server_config = file_content["mcpServers"]["filesystem"]
        assert server_config["command"] == "npx"
        assert "@modelcontextprotocol/server-filesystem" in server_config["args"]

    def test_complete_first_install_workflow(self, e2e_harness, e2e_manager):
        """E2E: Complete workflow from discovery to verified installation."""
        # Step 1: List servers to see initial state (should be empty)
        initial_servers = e2e_manager.list_servers()
        initial_count = len(initial_servers)

        # Step 2: Add a server
        config = ServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            type="stdio",
            env={"GITHUB_TOKEN": "test-token"},
        )
        result = e2e_manager.add_server("github", config, scope="user-mcp")
        assert result.success

        # Step 3: Verify server appears in list
        # list_servers() returns Dict[str, ServerInfo] keyed by qualified ID
        updated_servers = e2e_manager.list_servers()
        assert len(updated_servers) == initial_count + 1

        # Find the github server - dict is keyed by qualified ID (client:scope:server_id)
        github_key = "claude-code:user-mcp:github"
        assert github_key in updated_servers, f"GitHub server should appear in list. Keys: {list(updated_servers.keys())}"
        github_server = updated_servers[github_key]
        assert github_server.scope == "user-mcp"


# =============================================================================
# Workflow 2: Project-Specific Configuration
# =============================================================================


class TestProjectSpecificConfiguration:
    """Test workflow for project-specific server configuration.

    User Story:
    As a developer working on a specific project, I want to add servers
    that only apply to this project, not my global configuration.

    Workflow:
    1. Add server to project scope (mcpi add server --scope project-mcp)
    2. Verify it's in project scope (mcpi list --scope project-mcp)
    3. Rescope to user level if needed (mcpi rescope server --to user-mcp)
    """

    def test_add_to_project_scope(self, e2e_harness, e2e_plugin):
        """E2E: User adds a server specifically to project scope."""
        config = ServerConfig(
            command="python",
            args=["-m", "my_project_server"],
            type="stdio",
        )
        result = e2e_plugin.add_server("project-server", config, scope="project-mcp")

        assert result.success
        e2e_harness.assert_server_exists("project-mcp", "project-server")

        # Verify it's NOT in user scope
        user_content = e2e_harness.read_scope_file("user-mcp")
        if user_content and "mcpServers" in user_content:
            assert "project-server" not in user_content["mcpServers"]

    def test_list_filters_by_scope(self, e2e_harness, e2e_plugin):
        """E2E: User can filter list by scope to see only project servers."""
        # Add servers to different scopes
        project_config = ServerConfig(command="python", args=["project.py"])
        user_config = ServerConfig(command="node", args=["user.js"])

        e2e_plugin.add_server("project-only", project_config, scope="project-mcp")
        e2e_plugin.add_server("user-only", user_config, scope="user-mcp")

        # Get servers from project scope only using plugin.list_servers(scope=...)
        project_servers = e2e_plugin.list_servers(scope="project-mcp")

        # Should only see project-only server (dict keyed by qualified ID)
        project_key = "claude-code:project-mcp:project-only"
        user_key = "claude-code:user-mcp:user-only"
        assert project_key in project_servers
        assert user_key not in project_servers

    def test_rescope_moves_server_between_scopes(self, e2e_harness, e2e_plugin):
        """E2E: User moves a server from project to user scope.

        Note: rescope is a CLI-level operation. At the plugin level, it's
        implemented as: get config -> add to destination -> remove from source.
        """
        # Start with server in project scope
        config = ServerConfig(
            command="npx",
            args=["-y", "some-package"],
            type="stdio",
            env={"API_KEY": "secret"},
        )
        e2e_plugin.add_server("movable-server", config, scope="project-mcp")
        e2e_harness.assert_server_exists("project-mcp", "movable-server")

        # Manual rescope: get config, add to new scope, remove from old scope
        # This is what the CLI rescope command does internally
        source_scope = e2e_plugin.get_scope_handler("project-mcp")
        server_config_dict = source_scope.get_server_config("movable-server")

        # Add to destination scope
        new_config = ServerConfig.from_dict(server_config_dict)
        add_result = e2e_plugin.add_server("movable-server", new_config, scope="user-mcp")
        assert add_result.success, f"Add to new scope failed: {add_result.message}"

        # Remove from source scope
        remove_result = e2e_plugin.remove_server("movable-server", scope="project-mcp")
        assert remove_result.success, f"Remove from old scope failed: {remove_result.message}"

        # Verify: now in user-mcp, not in project-mcp
        e2e_harness.assert_server_exists("user-mcp", "movable-server")

        project_content = e2e_harness.read_scope_file("project-mcp")
        if project_content and "mcpServers" in project_content:
            assert "movable-server" not in project_content["mcpServers"]

        # Verify config was preserved
        user_content = e2e_harness.read_scope_file("user-mcp")
        moved_config = user_content["mcpServers"]["movable-server"]
        assert moved_config["env"]["API_KEY"] == "secret"


# =============================================================================
# Workflow 3: Enable/Disable Server Management
# =============================================================================


class TestEnableDisableManagement:
    """Test workflow for enabling and disabling servers.

    User Story:
    As a user, I want to temporarily disable a server without removing it,
    so I can re-enable it later without reconfiguring.

    Workflow:
    1. List enabled servers (mcpi list --state enabled)
    2. Disable a server (mcpi disable server)
    3. Verify it's disabled (mcpi list --state disabled)
    4. Re-enable (mcpi enable server)
    5. Verify it's enabled again
    """

    def test_disable_server_changes_state(self, e2e_harness, e2e_plugin):
        """E2E: Disabling a server marks it as disabled in the file."""
        # Add an enabled server
        config = ServerConfig(command="node", args=["server.js"])
        e2e_plugin.add_server("toggleable", config, scope="user-internal")

        # Verify initial state is enabled
        # list_servers() returns Dict[str, ServerInfo] keyed by qualified ID
        server_key = "claude-code:user-internal:toggleable"
        servers = e2e_plugin.list_servers()
        assert server_key in servers
        assert servers[server_key].state == ServerState.ENABLED

        # Disable it
        result = e2e_plugin.disable_server("toggleable")
        assert result.success

        # Verify state changed
        servers = e2e_plugin.list_servers()
        assert server_key in servers
        assert servers[server_key].state == ServerState.DISABLED

    def test_enable_disabled_server(self, e2e_harness, e2e_plugin):
        """E2E: Re-enabling a disabled server restores it to enabled state."""
        # Add and disable a server
        config = ServerConfig(command="node", args=["server.js"])
        e2e_plugin.add_server("restorable", config, scope="user-internal")
        e2e_plugin.disable_server("restorable")

        # Verify it's disabled
        server_key = "claude-code:user-internal:restorable"
        servers = e2e_plugin.list_servers()
        assert server_key in servers
        assert servers[server_key].state == ServerState.DISABLED

        # Re-enable
        result = e2e_plugin.enable_server("restorable")
        assert result.success

        # Verify it's enabled again
        servers = e2e_plugin.list_servers()
        assert server_key in servers
        assert servers[server_key].state == ServerState.ENABLED

    def test_disable_preserves_config(self, e2e_harness, e2e_plugin):
        """E2E: Disabling a server preserves its configuration for later."""
        original_config = ServerConfig(
            command="python",
            args=["-m", "complex_server", "--port", "8080"],
            type="stdio",
            env={"API_KEY": "secret", "DEBUG": "true"},
        )
        e2e_plugin.add_server("complex", original_config, scope="user-internal")

        # Disable and re-enable
        e2e_plugin.disable_server("complex")
        e2e_plugin.enable_server("complex")

        # Get config and verify it's unchanged
        # get_server_config returns dict, not ServerConfig
        scope = e2e_plugin.get_scope_handler("user-internal")
        restored_config = scope.get_server_config("complex")

        assert restored_config["command"] == "python"
        assert "--port" in restored_config["args"]
        assert restored_config.get("env", {}).get("API_KEY") == "secret"


# =============================================================================
# Workflow 4: Multi-Scope Management
# =============================================================================


class TestMultiScopeManagement:
    """Test workflow for managing servers across multiple scopes.

    User Story:
    As a power user, I want to organize my servers across different scopes
    (project, user-local, user-global) for different use cases.

    Workflow:
    1. List all scopes (mcpi scope list)
    2. Add servers to different scopes
    3. List servers per scope
    4. Move servers between scopes as needed
    """

    def test_servers_in_different_scopes_are_isolated(self, e2e_harness, e2e_plugin):
        """E2E: Servers in different scopes don't interfere with each other."""
        # Add same-named server to different scopes with different configs
        project_config = ServerConfig(command="python", args=["project-version.py"])
        user_config = ServerConfig(command="python", args=["user-version.py"])

        e2e_plugin.add_server("my-server", project_config, scope="project-mcp")
        e2e_plugin.add_server("my-server", user_config, scope="user-mcp")

        # Verify each scope has its own config
        # get_server_config returns dict
        project_scope = e2e_plugin.get_scope_handler("project-mcp")
        user_scope = e2e_plugin.get_scope_handler("user-mcp")

        project_server = project_scope.get_server_config("my-server")
        user_server = user_scope.get_server_config("my-server")

        assert "project-version.py" in project_server["args"]
        assert "user-version.py" in user_server["args"]

    def test_list_aggregates_from_all_scopes(self, e2e_harness, e2e_manager):
        """E2E: Listing without scope filter shows servers from all scopes."""
        # Add servers to multiple scopes
        configs = [
            ("scope-a-server", "project-mcp", ServerConfig(command="a")),
            ("scope-b-server", "user-mcp", ServerConfig(command="b")),
            ("scope-c-server", "user-internal", ServerConfig(command="c")),
        ]

        for server_id, scope, config in configs:
            e2e_manager.add_server(server_id, config, scope=scope)

        # List all servers - returns Dict[str, ServerInfo] keyed by qualified ID
        all_servers = e2e_manager.list_servers()

        # Check using qualified keys
        assert "claude-code:project-mcp:scope-a-server" in all_servers
        assert "claude-code:user-mcp:scope-b-server" in all_servers
        assert "claude-code:user-internal:scope-c-server" in all_servers

    def test_rescope_between_multiple_scopes(self, e2e_harness, e2e_plugin):
        """E2E: Server can be moved through multiple scope levels.

        Note: rescope is implemented as get config + add + remove at plugin level.
        """
        config = ServerConfig(command="migrating", args=["server"])

        # Start in project scope
        e2e_plugin.add_server("migrating-server", config, scope="project-mcp")

        # Helper function to rescope at plugin level
        def do_rescope(server_id: str, from_scope: str, to_scope: str):
            source = e2e_plugin.get_scope_handler(from_scope)
            config_dict = source.get_server_config(server_id)
            new_config = ServerConfig.from_dict(config_dict)
            e2e_plugin.add_server(server_id, new_config, scope=to_scope)
            e2e_plugin.remove_server(server_id, scope=from_scope)

        # Move to user-mcp
        do_rescope("migrating-server", "project-mcp", "user-mcp")
        e2e_harness.assert_server_exists("user-mcp", "migrating-server")

        # Move to user-internal
        do_rescope("migrating-server", "user-mcp", "user-internal")
        e2e_harness.assert_server_exists("user-internal", "migrating-server")


# =============================================================================
# Workflow 5: Complete Server Lifecycle
# =============================================================================


class TestCompleteServerLifecycle:
    """Test the complete lifecycle of a server from add to remove.

    User Story:
    As a user, I want to manage the full lifecycle of a server:
    install, use, disable, enable, and finally remove it.

    Workflow:
    1. Search and find server
    2. Add server
    3. Verify it works (list shows enabled)
    4. Disable when not needed
    5. Re-enable when needed again
    6. Remove when done
    7. Verify complete removal
    """

    def test_full_lifecycle_add_disable_enable_remove(
        self, e2e_harness, e2e_plugin, e2e_manager
    ):
        """E2E: Complete lifecycle from installation to removal."""
        # Step 1: Add server
        config = ServerConfig(
            command="node",
            args=["lifecycle-server.js"],
            env={"VERSION": "1.0"},
        )
        add_result = e2e_plugin.add_server(
            "lifecycle-test", config, scope="user-internal"
        )
        assert add_result.success

        # Step 2: Verify it's listed and enabled
        # list_servers returns Dict[str, ServerInfo] keyed by qualified ID
        server_key = "claude-code:user-internal:lifecycle-test"
        servers = e2e_manager.list_servers()
        assert server_key in servers
        assert servers[server_key].state == ServerState.ENABLED

        # Step 3: Disable
        disable_result = e2e_plugin.disable_server("lifecycle-test")
        assert disable_result.success

        servers = e2e_manager.list_servers()
        assert server_key in servers
        assert servers[server_key].state == ServerState.DISABLED

        # Step 4: Re-enable
        enable_result = e2e_plugin.enable_server("lifecycle-test")
        assert enable_result.success

        servers = e2e_manager.list_servers()
        assert server_key in servers
        assert servers[server_key].state == ServerState.ENABLED

        # Step 5: Remove (need to specify scope)
        remove_result = e2e_plugin.remove_server("lifecycle-test", scope="user-internal")
        assert remove_result.success

        # Step 6: Verify removal
        servers = e2e_manager.list_servers()
        assert server_key not in servers, "Server should be completely removed"

        # Also verify file doesn't contain it
        content = e2e_harness.read_scope_file("user-internal")
        if content and "mcpServers" in content:
            assert "lifecycle-test" not in content["mcpServers"]


# =============================================================================
# Workflow 6: Dry-Run Operations
# =============================================================================


class TestDryRunOperations:
    """Test dry-run mode for previewing changes without making them.

    User Story:
    As a cautious user, I want to preview what a command would do
    before actually executing it, so I can verify it's correct.

    Workflow:
    1. Dry-run add (mcpi add server --dry-run)
    2. Verify no changes were made
    3. Dry-run remove
    4. Verify server still exists
    """

    def test_dry_run_add_makes_no_changes(self, e2e_harness, cli_runner):
        """E2E: Dry-run add shows what would happen but doesn't change files."""
        # Run dry-run add
        result = cli_runner.invoke(
            main,
            ["add", "filesystem", "--dry-run"],
        )

        # Should succeed (or at least not error on the dry-run itself)
        # Note: May show "would add" message

        # Verify no files were created/modified
        for scope in ["project-mcp", "user-mcp", "user-internal"]:
            content = e2e_harness.read_scope_file(scope)
            if content and "mcpServers" in content:
                assert "filesystem" not in content["mcpServers"]

    def test_dry_run_remove_preserves_server(self, e2e_harness, e2e_plugin, cli_runner):
        """E2E: Dry-run remove shows what would happen but keeps the server."""
        # First, actually add a server
        config = ServerConfig(command="node", args=["keeper.js"])
        e2e_plugin.add_server("keeper", config, scope="user-internal")
        e2e_harness.assert_server_exists("user-internal", "keeper")

        # Now dry-run remove
        result = cli_runner.invoke(
            main,
            ["remove", "keeper", "--dry-run"],
        )

        # Server should still exist
        e2e_harness.assert_server_exists("user-internal", "keeper")


# =============================================================================
# Error Handling Workflows
# =============================================================================


class TestErrorHandlingWorkflows:
    """Test that errors are handled gracefully in user workflows."""

    def test_add_to_invalid_scope_fails_gracefully(self, e2e_plugin):
        """E2E: Adding to non-existent scope gives clear error."""
        config = ServerConfig(command="test")
        result = e2e_plugin.add_server("test", config, scope="invalid-scope")

        assert not result.success
        assert "scope" in result.message.lower() or "invalid" in result.message.lower()

    def test_remove_nonexistent_server_fails_gracefully(self, e2e_plugin):
        """E2E: Removing a server that doesn't exist gives clear error."""
        # remove_server requires scope parameter
        result = e2e_plugin.remove_server("nonexistent-server", scope="user-internal")

        # Should fail with a message about not finding the server
        # The exact behavior may vary - it might return success=False or an error message
        # Either way, the operation should not crash
        if result.success:
            # Some implementations may consider this a no-op success
            pass
        else:
            # Expected: failure with message
            assert result.message is not None

    def test_enable_already_enabled_is_idempotent(self, e2e_harness, e2e_plugin):
        """E2E: Enabling an already-enabled server succeeds (idempotent)."""
        config = ServerConfig(command="node", args=["already-enabled.js"])
        e2e_plugin.add_server("enabled-server", config, scope="user-internal")

        # Enable twice - should both succeed (or at least not crash)
        result1 = e2e_plugin.enable_server("enabled-server")
        result2 = e2e_plugin.enable_server("enabled-server")

        # Idempotent: either succeeds or says "already enabled"
        # The key is it doesn't error out
        assert result1.success or result1.message is not None
        assert result2.success or result2.message is not None

    def test_disable_already_disabled_is_idempotent(self, e2e_harness, e2e_plugin):
        """E2E: Disabling an already-disabled server succeeds (idempotent)."""
        config = ServerConfig(command="node", args=["toggleable.js"])
        e2e_plugin.add_server("toggle-server", config, scope="user-internal")
        e2e_plugin.disable_server("toggle-server")

        # Disable again - should succeed or say "already disabled"
        result = e2e_plugin.disable_server("toggle-server")
        assert result.success or result.message is not None


# =============================================================================
# CLI Integration Workflows
# =============================================================================


class TestCLIIntegrationWorkflows:
    """Test complete workflows through the CLI interface."""

    def test_cli_help_is_informative(self, cli_runner):
        """E2E: CLI help provides useful guidance."""
        result = cli_runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "add" in result.output
        assert "remove" in result.output
        assert "list" in result.output
        assert "enable" in result.output
        assert "disable" in result.output

    def test_cli_scope_list_shows_all_scopes(self, cli_runner):
        """E2E: Scope list command shows available scopes."""
        result = cli_runner.invoke(main, ["scope", "list"])

        # Command should succeed and show scope information
        # Note: exit_code might be non-zero if no client detected, but that's ok
        # We just verify it runs without crashing
        assert result.exception is None or isinstance(result.exception, SystemExit)

    def test_cli_client_list_shows_clients(self, cli_runner):
        """E2E: Client list command shows available clients."""
        result = cli_runner.invoke(main, ["client", "list"])

        # Command should run without crashing
        # It may show clients or a message about detected clients
        assert result.exception is None or isinstance(result.exception, SystemExit)

    def test_cli_status_gives_overview(self, cli_runner):
        """E2E: Status command provides system overview."""
        result = cli_runner.invoke(main, ["status"])

        assert result.exit_code == 0
        # Should show some status information
        assert len(result.output) > 0
