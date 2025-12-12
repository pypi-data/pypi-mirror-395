"""Example tests demonstrating the MCP test harness."""

import pytest

from mcpi.clients.types import ServerConfig, ServerState


class TestMCPHarnessBasics:
    """Basic tests demonstrating harness usage."""

    def test_harness_creates_temp_files(self, mcp_harness):
        """Test that harness creates files in temp directory."""
        # Verify path overrides are set up
        assert len(mcp_harness.path_overrides) > 0

        # Check that all paths point to temp directory
        for scope_name, path in mcp_harness.path_overrides.items():
            assert str(mcp_harness.tmp_dir) in str(path)
            assert "claude-code" in path.name
            assert scope_name in path.name

    def test_prepopulate_and_read(self, mcp_harness):
        """Test prepopulating files and reading them back."""
        test_data = {
            "mcpServers": {
                "test-server": {
                    "command": "npx",
                    "args": ["-y", "test-package"],
                    "type": "stdio",
                }
            }
        }

        # Prepopulate a scope
        mcp_harness.prepopulate_file("user-mcp", test_data)

        # Read it back
        content = mcp_harness.read_scope_file("user-mcp")
        assert content == test_data

        # Verify file exists on disk
        file_path = mcp_harness.path_overrides["user-mcp"]
        assert file_path.exists()

    def test_assert_valid_json(self, mcp_harness):
        """Test JSON validation assertions."""
        # Prepopulate with valid JSON
        mcp_harness.prepopulate_file("user-mcp", {"test": "data"})

        # Should not raise
        mcp_harness.assert_valid_json("user-mcp")

        # Test with non-existent file
        with pytest.raises(AssertionError, match="does not exist"):
            mcp_harness.assert_valid_json("project-mcp")

    def test_server_assertions(self, prepopulated_harness):
        """Test server-related assertions."""
        # Test server exists
        prepopulated_harness.assert_server_exists("user-mcp", "filesystem")
        prepopulated_harness.assert_server_exists("project-mcp", "project-tool")

        # Test server doesn't exist
        with pytest.raises(AssertionError, match="not found"):
            prepopulated_harness.assert_server_exists("user-mcp", "nonexistent")

        # Test command assertion
        prepopulated_harness.assert_server_command("user-mcp", "filesystem", "npx")
        prepopulated_harness.assert_server_command(
            "project-mcp", "project-tool", "python"
        )

        # Test wrong command
        with pytest.raises(AssertionError, match="Expected command"):
            prepopulated_harness.assert_server_command(
                "user-mcp", "filesystem", "node"
            )

    def test_count_servers(self, prepopulated_harness):
        """Test counting servers in scopes."""
        assert prepopulated_harness.count_servers_in_scope("user-mcp") == 2
        assert prepopulated_harness.count_servers_in_scope("project-mcp") == 1
        # The prepopulated_harness has 2 servers in user-internal scope
        assert prepopulated_harness.count_servers_in_scope("user-internal") == 2
        assert (
            prepopulated_harness.count_servers_in_scope("user-local") == 1
        )  # Has disabled-server


class TestMCPManagerIntegration:
    """Tests using the MCP manager with the test harness."""

    def test_manager_with_custom_paths(self, mcp_manager_with_harness):
        """Test that manager uses custom paths from harness."""
        manager, harness = mcp_manager_with_harness

        # Add a server
        config = ServerConfig(command="npx", args=["-y", "test-server"], type="stdio")

        result = manager.add_server("test-server", config, "user-mcp", "claude-code")
        assert result.success

        # Verify the file was written to the test directory
        harness.assert_valid_json("user-mcp")
        harness.assert_server_exists("user-mcp", "test-server")
        harness.assert_server_command("user-mcp", "test-server", "npx")

    def test_list_servers_from_prepopulated(
        self, mcp_manager_with_harness, prepopulated_harness
    ):
        """Test listing servers from prepopulated files."""
        manager, harness = mcp_manager_with_harness

        # Replace harness with prepopulated one
        manager.registry.inject_client_instance(
            "claude-code",
            ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides),
        )

        # List all servers
        servers = manager.list_servers("claude-code")

        # Should find servers from multiple scopes
        server_ids = {info.id for info in servers.values()}
        assert "filesystem" in server_ids
        assert "github" in server_ids
        assert "project-tool" in server_ids
        assert "disabled-server" in server_ids

        # Check states
        for qualified_id, info in servers.items():
            if info.id == "disabled-server":
                assert info.state == ServerState.DISABLED
            else:
                assert info.state == ServerState.ENABLED

    def test_remove_server(self, mcp_manager_with_harness):
        """Test removing a server."""
        manager, harness = mcp_manager_with_harness

        # First add a server
        config = ServerConfig(command="node", args=["server.js"], type="stdio")
        manager.add_server("temp-server", config, "user-mcp", "claude-code")

        # Verify it exists
        harness.assert_server_exists("user-mcp", "temp-server")

        # Remove it
        result = manager.remove_server("temp-server", "user-mcp", "claude-code")
        assert result.success

        # Verify it's gone
        with pytest.raises(AssertionError, match="not found"):
            harness.assert_server_exists("user-mcp", "temp-server")

    def test_update_server(self, mcp_manager_with_harness):
        """Test updating a server configuration by removing and re-adding."""
        manager, harness = mcp_manager_with_harness

        # Add initial server
        initial_config = ServerConfig(
            command="python", args=["-m", "old_module"], type="stdio"
        )
        manager.add_server("update-test", initial_config, "project-mcp", "claude-code")

        # Verify initial state
        harness.assert_server_command("project-mcp", "update-test", "python")
        config = harness.get_server_config("project-mcp", "update-test")
        assert config["args"] == ["-m", "old_module"]

        # Update the server by removing and re-adding
        result = manager.remove_server("update-test", "project-mcp", "claude-code")
        assert result.success

        new_config = ServerConfig(
            command="python3",
            args=["-m", "new_module"],
            env={"PYTHONPATH": "/custom/path"},
            type="stdio",
        )
        result = manager.add_server(
            "update-test", new_config, "project-mcp", "claude-code"
        )
        assert result.success

        # Verify updated state
        harness.assert_server_command("project-mcp", "update-test", "python3")
        config = harness.get_server_config("project-mcp", "update-test")
        assert config["args"] == ["-m", "new_module"]
        assert config["env"]["PYTHONPATH"] == "/custom/path"


class TestMultiClientScenarios:
    """Tests with multiple clients and scopes."""

    def test_scope_priority(self, mcp_manager_with_harness):
        """Test that servers from higher priority scopes override lower ones."""
        manager, harness = mcp_manager_with_harness

        # Add same server to multiple scopes with different configs
        config1 = ServerConfig(command="npx", args=["project-version"], type="stdio")
        config2 = ServerConfig(command="npx", args=["user-version"], type="stdio")

        # Add to project scope (higher priority)
        manager.add_server("multi-scope", config1, "project-mcp", "claude-code")

        # Add to user scope (lower priority)
        manager.add_server("multi-scope", config2, "user-mcp", "claude-code")

        # Verify both files have the server
        harness.assert_server_exists("project-mcp", "multi-scope")
        harness.assert_server_exists("user-mcp", "multi-scope")

        # List servers and check that we get both
        servers = manager.list_servers("claude-code")

        # Find the servers
        project_server = None
        user_server = None

        for qualified_id, info in servers.items():
            if info.id == "multi-scope":
                if info.scope == "project-mcp":
                    project_server = info
                elif info.scope == "user-mcp":
                    user_server = info

        assert project_server is not None
        assert user_server is not None

        # Project scope should have higher priority (lower number)
        assert project_server.priority < user_server.priority

    def test_isolated_scopes(self, mcp_manager_with_harness):
        """Test that operations in one scope don't affect others."""
        manager, harness = mcp_manager_with_harness

        # Add servers to different scopes
        configs = {
            "user-mcp": ServerConfig(
                command="npx", args=["global-server"], type="stdio"
            ),
            "user-local": ServerConfig(
                command="npx", args=["local-server"], type="stdio"
            ),
            "project-mcp": ServerConfig(
                command="npx", args=["project-server"], type="stdio"
            ),
        }

        for scope, config in configs.items():
            manager.add_server(f"{scope}-test", config, scope, "claude-code")

        # Verify each scope has only its server
        assert harness.count_servers_in_scope("user-mcp") == 1
        assert harness.count_servers_in_scope("user-local") == 1
        assert harness.count_servers_in_scope("project-mcp") == 1

        # Remove from one scope
        manager.remove_server("user-mcp-test", "user-mcp", "claude-code")

        # Verify only that scope was affected
        assert harness.count_servers_in_scope("user-mcp") == 0
        assert harness.count_servers_in_scope("user-local") == 1
        assert harness.count_servers_in_scope("project-mcp") == 1


# Import the plugin for manager test
from mcpi.clients.claude_code import ClaudeCodePlugin
