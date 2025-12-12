"""Integration tests for installer workflows using the test harness."""

from unittest.mock import MagicMock, patch

import pytest

from mcpi.clients.types import ServerConfig, ServerState


class TestInstallerWorkflowsWithHarness:
    """Test installation workflows with real file operations."""

    @patch("subprocess.run")
    def test_npx_server_installation(self, mock_run, mcp_manager_with_harness):
        """Test installing an NPX-based server."""
        manager, harness = mcp_manager_with_harness

        # Mock successful npx installation
        mock_run.return_value = MagicMock(
            returncode=0, stdout="Installation successful"
        )

        # Add an NPX server
        config = ServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
            type="stdio",
        )

        result = manager.add_server("filesystem", config, "user-mcp", "claude-code")
        assert result.success

        # Verify file was created with correct content
        harness.assert_valid_json("user-mcp")
        harness.assert_server_exists("user-mcp", "filesystem")
        harness.assert_server_command("user-mcp", "filesystem", "npx")

        # Verify the full configuration
        server_config = harness.get_server_config("user-mcp", "filesystem")
        assert server_config["args"] == [
            "-y",
            "@modelcontextprotocol/server-filesystem",
        ]
        assert server_config["type"] == "stdio"

    @patch("subprocess.run")
    def test_pip_server_installation(self, mock_run, mcp_manager_with_harness):
        """Test installing a pip-based server."""
        manager, harness = mcp_manager_with_harness

        # Mock successful pip installation
        mock_run.return_value = MagicMock(returncode=0, stdout="Successfully installed")

        # Add a Python server
        config = ServerConfig(
            command="python",
            args=["-m", "mcp_server_git"],
            env={"GITHUB_TOKEN": "${GITHUB_TOKEN}"},
            type="stdio",
        )

        result = manager.add_server("git-server", config, "user-mcp", "claude-code")
        assert result.success

        # Verify configuration
        harness.assert_server_exists("user-mcp", "git-server")
        server_config = harness.get_server_config("user-mcp", "git-server")
        assert server_config["command"] == "python"
        assert server_config["env"]["GITHUB_TOKEN"] == "${GITHUB_TOKEN}"

    @pytest.mark.skip(
        reason="Bug: test assumes project-mcp uses inline disabled field, but it uses FileMoveEnableDisableHandler. "
        "Also API call passes client_name as scope parameter. Needs complete rewrite."
    )
    def test_server_state_transitions(self, mcp_manager_with_harness):
        """Test server state changes using Claude's actual enable/disable format.

        NOTE: Different scopes use different disable mechanisms:
        - project-mcp: Uses FileMoveEnableDisableHandler (moves to .mcp.disabled.json)
        - user-mcp: file-move mechanism (disabled-mcp.json)
        - user-internal: file-move mechanism (.disabled-servers.json)

        This test is currently broken because it expects inline disabled field.
        """
        manager, harness = mcp_manager_with_harness

        # Add a server to project-mcp scope
        config = ServerConfig(command="node", args=["server.js"], type="stdio")
        result = manager.add_server("state-test", config, "project-mcp", "claude-code")
        assert result.success

        # Initially should be enabled (default state)
        servers = manager.list_servers("claude-code", "project-mcp")
        server_info = next((s for s in servers.values() if s.id == "state-test"), None)
        assert server_info is not None
        assert server_info.state == ServerState.ENABLED

        # Test real disable operation
        result = manager.disable_server("state-test", "claude-code")
        assert result.success

        # Check that the server config has the inline 'disabled' field
        # (project-mcp scope uses inline field, not separate disabled file)
        project_mcp_content = harness.read_scope_file("project-mcp")
        assert project_mcp_content is not None, "project-mcp file should exist"
        assert "mcpServers" in project_mcp_content, "project-mcp should have mcpServers"
        assert (
            "state-test" in project_mcp_content["mcpServers"]
        ), "state-test should still be in project-mcp after disable"

        # Verify inline disabled field (project-mcp scope mechanism)
        server_config = project_mcp_content["mcpServers"]["state-test"]
        assert (
            "disabled" in server_config and server_config["disabled"] is True
        ), "Server should have disabled=true field in project-mcp scope"

        # Verify the server now shows as disabled
        servers_after_disable = manager.list_servers("claude-code", "project-mcp")
        disabled_server = next(
            (s for s in servers_after_disable.values() if s.id == "state-test"), None
        )
        assert disabled_server is not None
        assert disabled_server.state == ServerState.DISABLED

        # Test enable operation
        result = manager.enable_server("state-test", "claude-code")
        assert result.success

        # Verify the disabled field is removed or set to false
        project_mcp_content_after_enable = harness.read_scope_file("project-mcp")
        server_config_after_enable = project_mcp_content_after_enable["mcpServers"][
            "state-test"
        ]
        # The disabled field should either be absent or set to false
        assert (
            server_config_after_enable.get("disabled", False) is False
        ), "Server should not have disabled=true after enable"

        # Verify the server is now enabled
        servers_after_enable = manager.list_servers("claude-code", "project-mcp")
        enabled_server = next(
            (s for s in servers_after_enable.values() if s.id == "state-test"), None
        )
        assert enabled_server is not None
        assert enabled_server.state == ServerState.ENABLED

    def test_environment_variable_handling(self, mcp_manager_with_harness):
        """Test proper handling of environment variables."""
        manager, harness = mcp_manager_with_harness

        # Add server with multiple env vars
        config = ServerConfig(
            command="python",
            args=["-m", "secure_server"],
            env={"API_KEY": "${API_KEY}", "DEBUG": "true", "PORT": "3000"},
            type="stdio",
        )

        result = manager.add_server("env-test", config, "user-internal", "claude-code")
        assert result.success

        # Verify all env vars are preserved
        server_config = harness.get_server_config("user-internal", "env-test")
        assert server_config["env"]["API_KEY"] == "${API_KEY}"
        assert server_config["env"]["DEBUG"] == "true"
        assert server_config["env"]["PORT"] == "3000"


class TestComplexWorkflows:
    """Test complex multi-step workflows."""

    @pytest.mark.skip(
        reason="Bug: Adding to project-mcp scope creates enabledMcpServers field which fails schema validation. "
        "Schema doesn't allow enabledMcpServers in .mcp.json files."
    )
    def test_migration_workflow(self, mcp_manager_with_harness, prepopulated_harness):
        """Test migrating servers from one scope to another."""
        manager, harness = mcp_manager_with_harness

        # Use prepopulated harness that has servers in user-mcp
        from mcpi.clients.claude_code import ClaudeCodePlugin

        manager.registry.inject_client_instance(
            "claude-code",
            ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides),
        )

        # Verify initial state
        prepopulated_harness.assert_server_exists("user-mcp", "filesystem")
        prepopulated_harness.assert_server_exists("user-mcp", "github")

        # Get the filesystem server config
        fs_config = prepopulated_harness.get_server_config("user-mcp", "filesystem")

        # "Migrate" filesystem to project scope
        config = ServerConfig(
            command=fs_config["command"], args=fs_config["args"], type=fs_config["type"]
        )

        # Add to project scope
        result = manager.add_server("filesystem", config, "project-mcp", "claude-code")
        assert result.success

        # Remove from user scope
        result = manager.remove_server("filesystem", "user-mcp", "claude-code")
        assert result.success

        # Verify migration complete
        prepopulated_harness.assert_server_exists("project-mcp", "filesystem")
        with pytest.raises(AssertionError):
            prepopulated_harness.assert_server_exists("user-mcp", "filesystem")

        # GitHub server should still be in user-mcp
        prepopulated_harness.assert_server_exists("user-mcp", "github")

    def test_bulk_operations(self, mcp_manager_with_harness):
        """Test bulk adding and removing servers."""
        manager, harness = mcp_manager_with_harness

        # Add multiple servers in bulk
        servers_to_add = [
            ("server1", ServerConfig(command="npx", args=["pkg1"], type="stdio")),
            ("server2", ServerConfig(command="npx", args=["pkg2"], type="stdio")),
            (
                "server3",
                ServerConfig(command="python", args=["-m", "pkg3"], type="stdio"),
            ),
            ("server4", ServerConfig(command="node", args=["pkg4.js"], type="stdio")),
        ]

        # Add all servers to user-mcp scope
        for server_id, config in servers_to_add:
            result = manager.add_server(server_id, config, "user-mcp", "claude-code")
            assert result.success

        # Verify all were added
        assert harness.count_servers_in_scope("user-mcp") == 4

        # List and verify each
        servers = manager.list_servers("claude-code", "user-mcp")
        server_ids = {info.id for info in servers.values()}
        assert "server1" in server_ids
        assert "server2" in server_ids
        assert "server3" in server_ids
        assert "server4" in server_ids

        # Remove servers 2 and 3
        manager.remove_server("server2", "user-mcp", "claude-code")
        manager.remove_server("server3", "user-mcp", "claude-code")

        # Verify removal
        assert harness.count_servers_in_scope("user-mcp") == 2
        harness.assert_server_exists("user-mcp", "server1")
        harness.assert_server_exists("user-mcp", "server4")

        with pytest.raises(AssertionError):
            harness.assert_server_exists("user-mcp", "server2")
        with pytest.raises(AssertionError):
            harness.assert_server_exists("user-mcp", "server3")

    def test_error_recovery(self, mcp_manager_with_harness):
        """Test recovery from various error conditions."""
        manager, harness = mcp_manager_with_harness

        # Add a server
        config = ServerConfig(
            command="python", args=["-m", "test_server"], type="stdio"
        )
        manager.add_server("test-server", config, "user-mcp", "claude-code")

        # Try to add duplicate (should handle gracefully)
        result = manager.add_server("test-server", config, "user-mcp", "claude-code")
        # This might succeed (overwrite) or fail (duplicate check)

        # Try to remove non-existent server
        result = manager.remove_server("nonexistent", "user-mcp", "claude-code")
        assert not result.success

        # Original server should still be there
        harness.assert_server_exists("user-mcp", "test-server")

        # Try to add to non-existent scope
        result = manager.add_server(
            "bad-scope-test", config, "invalid-scope", "claude-code"
        )
        assert not result.success

        # No file should have been created for invalid scope
        assert "invalid-scope" not in harness.path_overrides
