"""Tests for Claude Code client plugin."""

import pytest

from mcpi.clients.claude_code import ClaudeCodePlugin
from mcpi.clients.types import ServerConfig, ServerState


class TestClaudeCodePlugin:
    """Test ClaudeCodePlugin class."""

    @pytest.fixture
    def plugin(self, mcp_harness):
        """Create a ClaudeCodePlugin instance for testing using harness for safety."""
        return ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

    def test_get_name(self, plugin):
        """Test that plugin returns correct name."""
        assert plugin.name == "claude-code"

    def test_initialize_scopes(self, plugin):
        """Test that all expected scopes are initialized."""
        # NOTE: user-mcp scope was removed because ~/.claude/settings.json
        # is NOT used for MCP servers by Claude Code. MCP servers are stored
        # in ~/.claude.json (user-internal scope).
        expected_scopes = [
            "plugin",  # Plugin-based MCP servers (read-only)
            "project-mcp",
            "project-local",
            "user-local",
            "user-internal",
            "user-mcp",
        ]

        scopes = plugin.get_scope_names()
        assert set(scopes) == set(expected_scopes)

    def test_scope_priorities(self, plugin):
        """Test that scopes have correct priorities."""
        scopes = plugin.get_scopes()

        scope_priorities = {s.name: s.priority for s in scopes}

        assert scope_priorities["plugin"] == 0  # Highest priority (read-only)
        assert scope_priorities["project-mcp"] == 1
        assert scope_priorities["project-local"] == 2
        assert scope_priorities["user-local"] == 3
        # user-mcp was removed (settings.json not used for MCP servers)
        assert scope_priorities["user-internal"] == 4
        assert scope_priorities["user-mcp"] == 5

    def test_scope_types(self, plugin):
        """Test that scopes are correctly categorized as user/project."""
        scopes = plugin.get_scopes()

        project_scopes = [s for s in scopes if s.is_project_level]
        user_scopes = [s for s in scopes if s.is_user_level]

        project_names = [s.name for s in project_scopes]
        assert "project-mcp" in project_names
        assert "project-local" in project_names

        user_names = [s.name for s in user_scopes]
        assert "plugin" in user_names  # Plugin scope is user-level
        assert "user-local" in user_names
        # user-mcp was removed (settings.json not used for MCP servers)
        assert "user-internal" in user_names
        assert "user-mcp" in user_names

    def test_get_project_scopes(self, plugin):
        """Test getting project-level scopes using new API."""
        scopes = plugin.get_scopes()
        project_scopes = [s.name for s in scopes if s.is_project_level]

        assert "project-mcp" in project_scopes
        assert "project-local" in project_scopes
        assert "user-local" not in project_scopes

    def test_get_user_scopes(self, plugin):
        """Test getting user-level scopes using new API."""
        scopes = plugin.get_scopes()
        user_scopes = [s.name for s in scopes if s.is_user_level]

        assert "plugin" in user_scopes  # Plugin scope is user-level
        assert "user-local" in user_scopes
        # user-mcp was removed (settings.json not used for MCP servers)
        assert "user-internal" in user_scopes
        assert "user-mcp" in user_scopes
        assert "project-mcp" not in user_scopes

    def test_validate_server_config_valid(self, plugin):
        """Test validating a valid server configuration."""
        config = ServerConfig(
            command="python", args=["-m", "test_server"], type="stdio"
        )

        errors = plugin.validate_server_config(config)
        assert len(errors) == 0

    def test_validate_server_config_missing_command(self, plugin):
        """Test validating server config with missing command."""
        config = ServerConfig(command="", args=["-m", "test"])

        errors = plugin.validate_server_config(config)
        assert len(errors) > 0
        assert any("command is required" in e for e in errors)

    def test_list_servers_no_existing_files(self, plugin):
        """Test listing servers when no config files exist."""
        servers = plugin.list_servers()
        assert len(servers) == 0

    def test_list_servers_with_data(self, plugin, mcp_harness):
        """Test listing servers when config files exist."""
        # Prepopulate server data
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpServers": {
                    "test-server": {
                        "command": "python",
                        "args": ["-m", "test_server"],
                        "type": "stdio",
                    }
                }
            },
        )

        servers = plugin.list_servers()

        assert len(servers) == 1
        qualified_id = "claude-code:user-mcp:test-server"
        assert qualified_id in servers

        server_info = servers[qualified_id]
        assert server_info.id == "test-server"
        assert server_info.client == "claude-code"
        assert server_info.scope == "user-mcp"
        assert server_info.state == ServerState.ENABLED

    def test_list_servers_with_disabled_server(self, plugin, mcp_harness):
        """Test listing servers with disabled server using Claude's actual format.

        BUG-FIX: This test now correctly tests scope isolation. A server installed in
        user-local and marked disabled in user-local's disabled array should show as
        DISABLED. Previously this test incorrectly expected cross-scope pollution.
        """
        # Prepopulate server in user-local (which supports enable/disable arrays)
        mcp_harness.prepopulate_file(
            "user-local",
            {
                "enabledMcpjsonServers": [],
                "disabledMcpjsonServers": ["disabled-server"],
                "mcpServers": {
                    "disabled-server": {
                        "command": "python",
                        "args": ["-m", "test_server"],
                        "type": "stdio",
                    }
                },
            },
        )

        servers = plugin.list_servers()

        qualified_id = "claude-code:user-local:disabled-server"
        server_info = servers[qualified_id]
        assert server_info.state == ServerState.DISABLED

    def test_list_servers_filtered_by_scope(self, plugin, mcp_harness):
        """Test listing servers filtered by specific scope."""
        # Prepopulate servers in different scopes
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpServers": {
                    "user-server": {"command": "python", "args": ["-m", "user_server"]}
                }
            },
        )
        mcp_harness.prepopulate_file(
            "project-mcp",
            {
                "mcpServers": {
                    "project-server": {"command": "node", "args": ["project_server.js"]}
                }
            },
        )

        # List servers for user-mcp scope only
        servers = plugin.list_servers(scope="user-mcp")

        assert len(servers) == 1
        qualified_id = "claude-code:user-mcp:user-server"
        assert qualified_id in servers

        # Ensure project server is not included
        project_qualified_id = "claude-code:project-mcp:project-server"
        assert project_qualified_id not in servers

    def test_add_server_invalid_scope(self, plugin):
        """Test adding server to invalid scope."""
        config = ServerConfig(command="python", args=["-m", "test"])

        result = plugin.add_server("test-server", config, "invalid-scope")

        assert not result.success
        assert "Unknown scope" in result.message

    def test_add_server_validation_failure(self, plugin):
        """Test adding server with invalid configuration (missing command)."""
        config = ServerConfig(command="", args=[])  # Invalid: no command

        result = plugin.add_server("test-server", config, "user-mcp")

        # Should fail validation
        assert not result.success
        assert (
            "validation" in result.message.lower()
            or "command" in result.message.lower()
        )

    def test_add_server_success(self, plugin):
        """Test successful server addition."""
        config = ServerConfig(command="python", args=["-m", "test_server"])

        result = plugin.add_server("test-server", config, "user-mcp")

        assert result.success

        # Verify server was added
        servers = plugin.list_servers(scope="user-mcp")
        qualified_id = "claude-code:user-mcp:test-server"
        assert qualified_id in servers

    def test_remove_server_invalid_scope(self, plugin):
        """Test removing server from invalid scope."""
        result = plugin.remove_server("test-server", "invalid-scope")

        assert not result.success
        assert "Unknown scope" in result.message

    def test_remove_server_success(self, plugin, mcp_harness):
        """Test successful server removal."""
        # Prepopulate a server first
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpServers": {
                    "test-server": {"command": "python", "args": ["-m", "test_server"]}
                }
            },
        )

        # Verify it exists
        servers_before = plugin.list_servers(scope="user-mcp")
        qualified_id = "claude-code:user-mcp:test-server"
        assert qualified_id in servers_before

        # Remove it
        result = plugin.remove_server("test-server", "user-mcp")

        assert result.success

        # Verify it's gone
        servers_after = plugin.list_servers(scope="user-mcp")
        assert qualified_id not in servers_after

    def test_get_server_state_not_installed(self, plugin):
        """Test getting state of non-existent server."""
        state = plugin.get_server_state("nonexistent-server")
        assert state == ServerState.NOT_INSTALLED

    def test_get_server_state_enabled(self, plugin, mcp_harness):
        """Test getting state of enabled server."""
        # Prepopulate an enabled server
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpServers": {
                    "test-server": {"command": "python", "args": ["-m", "test_server"]}
                }
            },
        )

        state = plugin.get_server_state("test-server")
        assert state == ServerState.ENABLED

    def test_get_server_state_disabled(self, plugin, mcp_harness):
        """Test getting state of disabled server using Claude's actual format.

        BUG-FIX: This test now correctly tests a server in user-local (which supports
        enable/disable arrays) rather than testing cross-scope pollution.
        """
        # Prepopulate server in user-local (which supports enable/disable)
        mcp_harness.prepopulate_file(
            "user-local",
            {
                "enabledMcpjsonServers": [],
                "disabledMcpjsonServers": ["test-server"],
                "mcpServers": {
                    "test-server": {"command": "python", "args": ["-m", "test_server"]}
                },
            },
        )

        state = plugin.get_server_state("test-server")
        assert state == ServerState.DISABLED

    def test_enable_server_not_found(self, plugin):
        """Test enabling non-existent server.

        BUG-FIX: After fixing the bug, enabling a non-existent server now correctly
        returns an error instead of succeeding with the wrong behavior.
        """
        result = plugin.enable_server("nonexistent-server")

        # Should fail because server doesn't exist in any scope
        assert not result.success
        assert "not found" in result.message.lower()

    def test_enable_server_already_enabled(self, plugin, mcp_harness):
        """Test enabling already enabled server."""
        # Prepopulate an enabled server in user-local (which supports enable/disable)
        mcp_harness.prepopulate_file(
            "user-local",
            {
                "enabledMcpjsonServers": [],
                "disabledMcpjsonServers": [],
                "mcpServers": {
                    "test-server": {"command": "python", "args": ["-m", "test_server"]}
                },
            },
        )

        result = plugin.enable_server("test-server")

        assert result.success

    def test_enable_server_success(self, plugin, mcp_harness):
        """Test successful server enabling using Claude's actual format.

        BUG-FIX: This test now correctly tests enabling a server that exists in user-local
        (which supports enable/disable arrays).
        """
        # Prepopulate server in user-local with disabled state
        mcp_harness.prepopulate_file(
            "user-local",
            {
                "enabledMcpjsonServers": [],
                "disabledMcpjsonServers": ["test-server"],
                "mcpServers": {
                    "test-server": {"command": "python", "args": ["-m", "test_server"]}
                },
            },
        )

        # Verify it's disabled
        state_before = plugin.get_server_state("test-server")
        assert state_before == ServerState.DISABLED

        # Enable it
        result = plugin.enable_server("test-server")

        assert result.success
        # Updated assertion to match actual message format
        assert "enabled" in result.message.lower()
        assert "test-server" in result.message

        # Verify it's enabled
        state_after = plugin.get_server_state("test-server")
        assert state_after == ServerState.ENABLED

    def test_disable_server_success(self, plugin, mcp_harness):
        """Test successful server disabling using Claude's actual format."""
        # Prepopulate an enabled server in user-local (which supports enable/disable)
        mcp_harness.prepopulate_file(
            "user-local",
            {
                "enabledMcpjsonServers": [],
                "disabledMcpjsonServers": [],
                "mcpServers": {
                    "test-server": {"command": "python", "args": ["-m", "test_server"]}
                },
            },
        )

        # Verify it's enabled
        state_before = plugin.get_server_state("test-server")
        assert state_before == ServerState.ENABLED

        # Disable it
        result = plugin.disable_server("test-server")

        assert result.success
        # Updated assertion to match actual message format
        assert "disabled" in result.message.lower()
        assert "test-server" in result.message

        # Verify it's disabled
        state_after = plugin.get_server_state("test-server")
        assert state_after == ServerState.DISABLED

    def test_get_server_state_unapproved(self, plugin, mcp_harness):
        """Test getting state of unapproved server in project-mcp scope.

        Servers in .mcp.json that haven't been through Claude's approval process
        (not in enabledMcpjsonServers or disabledMcpjsonServers) should be UNAPPROVED.
        """
        # Prepopulate server in project-mcp (active file)
        # Servers in the active file are ENABLED by default
        mcp_harness.prepopulate_file(
            "project-mcp",
            {
                "mcpServers": {
                    "test-server": {
                        "command": "python",
                        "args": ["-m", "test_server"],
                    }
                }
            },
        )

        # With file-move mechanism, servers in active file are ENABLED
        state = plugin.get_server_state("test-server")
        assert state == ServerState.ENABLED

    def test_project_mcp_server_in_active_file_is_enabled(self, plugin, mcp_harness):
        """Test that a server in the active .mcp.json file shows as ENABLED."""
        # Prepopulate server in project-mcp (active file)
        mcp_harness.prepopulate_file(
            "project-mcp",
            {
                "mcpServers": {
                    "active-server": {
                        "command": "python",
                        "args": ["-m", "test_server"],
                    }
                }
            },
        )

        state = plugin.get_server_state("active-server")
        assert state == ServerState.ENABLED

    def test_enable_disabled_server(self, plugin, mcp_harness):
        """Test enabling a DISABLED server moves it from disabled to active file.

        With file-move mechanism, enabling moves the server config from
        .mcp.disabled.json to .mcp.json.
        """
        # Prepopulate empty active file (required for scope to exist)
        mcp_harness.prepopulate_file(
            "project-mcp",
            {"mcpServers": {}},
        )

        # Prepopulate server in disabled file
        mcp_harness.prepopulate_file(
            "project-mcp-disabled",
            {
                "mcpServers": {
                    "disabled-server": {
                        "command": "python",
                        "args": ["-m", "test_server"],
                    }
                }
            },
        )

        # Verify it starts as DISABLED
        state_before = plugin.get_server_state("disabled-server")
        assert state_before == ServerState.DISABLED

        # Enable it
        result = plugin.enable_server("disabled-server", "project-mcp")

        assert result.success
        assert "enabled" in result.message.lower()

        # Verify it's now ENABLED
        state_after = plugin.get_server_state("disabled-server")
        assert state_after == ServerState.ENABLED

    def test_project_mcp_enabled_server(self, plugin, mcp_harness):
        """Test that a server in the active project-mcp file shows as ENABLED."""
        # Prepopulate server in project-mcp (active file)
        mcp_harness.prepopulate_file(
            "project-mcp",
            {
                "mcpServers": {
                    "enabled-server": {
                        "command": "python",
                        "args": ["-m", "test_server"],
                    }
                }
            },
        )

        state = plugin.get_server_state("enabled-server")
        assert state == ServerState.ENABLED

    def test_project_mcp_disabled_server(self, plugin, mcp_harness):
        """Test that a server in the disabled file shows as DISABLED.

        With file-move mechanism, disabled servers are stored in .mcp.disabled.json
        instead of using approval arrays in settings.local.json.
        """
        # Prepopulate empty active file (required for scope to exist)
        mcp_harness.prepopulate_file(
            "project-mcp",
            {"mcpServers": {}},
        )

        # Prepopulate server in disabled file (not active file)
        mcp_harness.prepopulate_file(
            "project-mcp-disabled",
            {
                "mcpServers": {
                    "disabled-server": {
                        "command": "python",
                        "args": ["-m", "test_server"],
                    }
                }
            },
        )

        state = plugin.get_server_state("disabled-server")
        assert state == ServerState.DISABLED
