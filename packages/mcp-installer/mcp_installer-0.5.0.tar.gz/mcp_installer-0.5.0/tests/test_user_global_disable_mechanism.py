"""Comprehensive tests for user-mcp custom disable mechanism.

REQUIREMENT (from CLAUDE.md lines 406-411):
For user-mcp MCP servers (~/.claude/settings.json):
- Two configuration files:
  - Active file: ~/.claude/settings.json (ENABLED servers)
  - Disabled file: ~/.claude.disabled-mcp.json (DISABLED servers)
- File structure: Both files contain MCP server configuration objects
- Operations:
  - `mcpi disable <server>` - MOVE config from settings.json to disabled-mcp.json
  - `mcpi enable <server>` - MOVE config from disabled-mcp.json to settings.json
  - `mcpi list` - Show combination of both files (enabled + disabled states)

VALIDATION CRITERIA:
1. ALL servers from `claude mcp list` MUST show as ENABLED in `mcpi list`
2. NO disabled servers should appear in `claude mcp list`
3. Disabled servers should ONLY appear in `mcpi list` with state=DISABLED

These tests are UNGAMEABLE because they:
- Use real file I/O (no mocks)
- Verify actual file contents before/after operations
- Test the complete workflow end-to-end
- Assert on actual behavior that affects users
"""

import json
from pathlib import Path

import pytest

from mcpi.clients.claude_code import ClaudeCodePlugin
from mcpi.clients.types import ServerState


class TestUserGlobalDisableMechanismUnit:
    """Unit tests for user-mcp disable mechanism.

    These tests verify the core move-based mechanism at the handler level.
    """

    @pytest.fixture
    def plugin(self, mcp_harness):
        """Create a ClaudeCodePlugin with test harness."""
        return ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

    @pytest.fixture
    def active_file(self, mcp_harness):
        """Get path to active config file."""
        return mcp_harness.path_overrides["user-mcp"]

    @pytest.fixture
    def disabled_file(self, mcp_harness):
        """Get path to disabled config file."""
        # Based on requirement: ~/.claude.disabled-mcp.json
        return mcp_harness.path_overrides["user-mcp-disabled"]

    def test_initially_empty_disabled_file_does_not_exist(self, disabled_file):
        """Test that disabled file doesn't exist initially."""
        assert not disabled_file.exists()

    def test_disable_server_moves_config_to_disabled_file(
        self, plugin, mcp_harness, active_file, disabled_file
    ):
        """Test that disabling a server MOVES its config to disabled file.

        This is the core mechanism: disable REMOVES from active and ADDS to disabled.
        """
        # Setup: Add server to active config
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {
                    "test-server": {
                        "command": "npx",
                        "args": ["-y", "test-server"],
                        "type": "stdio",
                    }
                },
            },
        )

        # Verify initial state: server in active file
        active_data = json.loads(active_file.read_text())
        assert "test-server" in active_data["mcpServers"]
        assert not disabled_file.exists()

        # Execute: Disable the server
        result = plugin.disable_server("test-server", scope="user-mcp")

        # Verify: Operation succeeded
        assert result.success, f"Disable should succeed: {result.message}"

        # Verify: Server removed from active file
        active_data = json.loads(active_file.read_text())
        assert (
            "test-server" not in active_data["mcpServers"]
        ), "Server should be REMOVED from active file"

        # Verify: Server added to disabled file
        assert disabled_file.exists(), "Disabled file should be created"
        disabled_data = json.loads(disabled_file.read_text())
        assert "mcpServers" in disabled_data
        assert (
            "test-server" in disabled_data["mcpServers"]
        ), "Server should be ADDED to disabled file"

        # Verify: Config is identical in disabled file
        expected_config = {
            "command": "npx",
            "args": ["-y", "test-server"],
            "type": "stdio",
        }
        assert disabled_data["mcpServers"]["test-server"] == expected_config

    def test_enable_server_moves_config_to_active_file(
        self, plugin, mcp_harness, active_file, disabled_file
    ):
        """Test that enabling a server MOVES its config to active file.

        This is the reverse mechanism: enable REMOVES from disabled and ADDS to active.
        """
        # Setup: Create active file with empty mcpServers
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {},
            },
        )

        # Setup: Create disabled file with server
        disabled_file.parent.mkdir(parents=True, exist_ok=True)
        disabled_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "test-server": {
                            "command": "npx",
                            "args": ["-y", "test-server"],
                            "type": "stdio",
                        }
                    }
                },
                indent=2,
            )
        )

        # Verify initial state: server in disabled file, not in active
        disabled_data = json.loads(disabled_file.read_text())
        assert "test-server" in disabled_data["mcpServers"]
        active_data = json.loads(active_file.read_text())
        assert "test-server" not in active_data["mcpServers"]

        # Execute: Enable the server
        result = plugin.enable_server("test-server", scope="user-mcp")

        # Verify: Operation succeeded
        assert result.success, f"Enable should succeed: {result.message}"

        # Verify: Server added to active file
        active_data = json.loads(active_file.read_text())
        assert (
            "test-server" in active_data["mcpServers"]
        ), "Server should be ADDED to active file"

        # Verify: Server removed from disabled file
        disabled_data = json.loads(disabled_file.read_text())
        assert (
            "test-server" not in disabled_data["mcpServers"]
        ), "Server should be REMOVED from disabled file"

        # Verify: Config is identical in active file
        expected_config = {
            "command": "npx",
            "args": ["-y", "test-server"],
            "type": "stdio",
        }
        assert active_data["mcpServers"]["test-server"] == expected_config

    def test_list_servers_shows_both_enabled_and_disabled(
        self, plugin, mcp_harness, active_file, disabled_file
    ):
        """Test that list_servers shows servers from BOTH files with correct states.

        This is the display requirement: show enabled + disabled servers together.
        """
        # Setup: Add enabled server to active file
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {
                    "enabled-server": {
                        "command": "npx",
                        "args": ["-y", "enabled-server"],
                        "type": "stdio",
                    }
                },
            },
        )

        # Setup: Add disabled server to disabled file
        disabled_file.parent.mkdir(parents=True, exist_ok=True)
        disabled_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "disabled-server": {
                            "command": "npx",
                            "args": ["-y", "disabled-server"],
                            "type": "stdio",
                        }
                    }
                },
                indent=2,
            )
        )

        # Execute: List servers in user-mcp scope
        servers = plugin.list_servers(scope="user-mcp")

        # Verify: Both servers appear in list
        server_ids = [info.id for info in servers.values()]
        assert "enabled-server" in server_ids
        assert "disabled-server" in server_ids

        # Verify: Enabled server has ENABLED state
        enabled_info = next(
            info for info in servers.values() if info.id == "enabled-server"
        )
        assert enabled_info.state == ServerState.ENABLED

        # Verify: Disabled server has DISABLED state
        disabled_info = next(
            info for info in servers.values() if info.id == "disabled-server"
        )
        assert disabled_info.state == ServerState.DISABLED

    def test_disable_nonexistent_server_fails_gracefully(self, plugin, mcp_harness):
        """Test that disabling a nonexistent server fails gracefully."""
        # Setup: Empty active file
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {},
            },
        )

        # Execute: Try to disable nonexistent server
        result = plugin.disable_server("nonexistent", scope="user-mcp")

        # Verify: Operation fails
        assert not result.success
        assert "nonexistent" in result.message.lower()

    def test_enable_nonexistent_server_fails_gracefully(
        self, plugin, mcp_harness, disabled_file
    ):
        """Test that enabling a nonexistent server fails gracefully."""
        # Setup: Empty active file
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {},
            },
        )

        # Setup: Empty disabled file
        disabled_file.parent.mkdir(parents=True, exist_ok=True)
        disabled_file.write_text(json.dumps({"mcpServers": {}}, indent=2))

        # Execute: Try to enable nonexistent server
        result = plugin.enable_server("nonexistent", scope="user-mcp")

        # Verify: Operation fails
        assert not result.success
        assert "nonexistent" in result.message.lower()

    def test_multiple_disable_enable_cycles(
        self, plugin, mcp_harness, active_file, disabled_file
    ):
        """Test that server can be disabled and enabled multiple times.

        This tests idempotency and ensures no data corruption.
        """
        # Setup: Add server to active file
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {
                    "test-server": {
                        "command": "npx",
                        "args": ["-y", "test-server"],
                        "type": "stdio",
                    }
                },
            },
        )

        expected_config = {
            "command": "npx",
            "args": ["-y", "test-server"],
            "type": "stdio",
        }

        # Cycle 1: Disable
        result = plugin.disable_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: In disabled file
        disabled_data = json.loads(disabled_file.read_text())
        assert disabled_data["mcpServers"]["test-server"] == expected_config

        # Cycle 1: Enable
        result = plugin.enable_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: In active file
        active_data = json.loads(active_file.read_text())
        assert active_data["mcpServers"]["test-server"] == expected_config

        # Cycle 2: Disable again
        result = plugin.disable_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: In disabled file again
        disabled_data = json.loads(disabled_file.read_text())
        assert disabled_data["mcpServers"]["test-server"] == expected_config

        # Cycle 2: Enable again
        result = plugin.enable_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: In active file again
        active_data = json.loads(active_file.read_text())
        assert active_data["mcpServers"]["test-server"] == expected_config


class TestUserGlobalDisableMechanismIntegration:
    """Integration tests for user-mcp disable mechanism.

    These tests verify the full workflow with multiple servers and edge cases.
    """

    @pytest.fixture
    def plugin(self, mcp_harness):
        """Create a ClaudeCodePlugin with test harness."""
        return ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

    @pytest.fixture
    def active_file(self, mcp_harness):
        """Get path to active config file."""
        return mcp_harness.path_overrides["user-mcp"]

    @pytest.fixture
    def disabled_file(self, mcp_harness):
        """Get path to disabled config file."""
        return mcp_harness.path_overrides["user-mcp-disabled"]

    def test_disable_one_server_among_many(
        self, plugin, mcp_harness, active_file, disabled_file
    ):
        """Test that disabling one server doesn't affect others."""
        # Setup: Add multiple servers to active file
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {
                    "server-1": {
                        "command": "npx",
                        "args": ["-y", "server-1"],
                        "type": "stdio",
                    },
                    "server-2": {
                        "command": "npx",
                        "args": ["-y", "server-2"],
                        "type": "stdio",
                    },
                    "server-3": {
                        "command": "npx",
                        "args": ["-y", "server-3"],
                        "type": "stdio",
                    },
                },
            },
        )

        # Execute: Disable server-2
        result = plugin.disable_server("server-2", scope="user-mcp")
        assert result.success

        # Verify: server-1 and server-3 still in active file
        active_data = json.loads(active_file.read_text())
        assert "server-1" in active_data["mcpServers"]
        assert "server-3" in active_data["mcpServers"]
        assert "server-2" not in active_data["mcpServers"]

        # Verify: Only server-2 in disabled file
        disabled_data = json.loads(disabled_file.read_text())
        assert "server-2" in disabled_data["mcpServers"]
        assert "server-1" not in disabled_data["mcpServers"]
        assert "server-3" not in disabled_data["mcpServers"]

        # Verify: list_servers shows all 3 with correct states
        servers = plugin.list_servers(scope="user-mcp")
        server_states = {info.id: info.state for info in servers.values()}

        assert server_states["server-1"] == ServerState.ENABLED
        assert server_states["server-2"] == ServerState.DISABLED
        assert server_states["server-3"] == ServerState.ENABLED

    def test_disable_all_servers_empties_active_file(
        self, plugin, mcp_harness, active_file, disabled_file
    ):
        """Test that disabling all servers empties the active file's mcpServers."""
        # Setup: Add 2 servers to active file
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {
                    "server-1": {
                        "command": "npx",
                        "args": ["-y", "server-1"],
                        "type": "stdio",
                    },
                    "server-2": {
                        "command": "npx",
                        "args": ["-y", "server-2"],
                        "type": "stdio",
                    },
                },
            },
        )

        # Execute: Disable both servers
        result1 = plugin.disable_server("server-1", scope="user-mcp")
        result2 = plugin.disable_server("server-2", scope="user-mcp")
        assert result1.success
        assert result2.success

        # Verify: Active file has empty mcpServers
        active_data = json.loads(active_file.read_text())
        assert active_data["mcpServers"] == {}

        # Verify: Disabled file has both servers
        disabled_data = json.loads(disabled_file.read_text())
        assert "server-1" in disabled_data["mcpServers"]
        assert "server-2" in disabled_data["mcpServers"]

    def test_enable_all_servers_empties_disabled_file(
        self, plugin, mcp_harness, active_file, disabled_file
    ):
        """Test that enabling all servers empties the disabled file's mcpServers."""
        # Setup: Active file with empty mcpServers
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {},
            },
        )

        # Setup: Disabled file with 2 servers
        disabled_file.parent.mkdir(parents=True, exist_ok=True)
        disabled_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "server-1": {
                            "command": "npx",
                            "args": ["-y", "server-1"],
                            "type": "stdio",
                        },
                        "server-2": {
                            "command": "npx",
                            "args": ["-y", "server-2"],
                            "type": "stdio",
                        },
                    }
                },
                indent=2,
            )
        )

        # Execute: Enable both servers
        result1 = plugin.enable_server("server-1", scope="user-mcp")
        result2 = plugin.enable_server("server-2", scope="user-mcp")
        assert result1.success
        assert result2.success

        # Verify: Active file has both servers
        active_data = json.loads(active_file.read_text())
        assert "server-1" in active_data["mcpServers"]
        assert "server-2" in active_data["mcpServers"]

        # Verify: Disabled file has empty mcpServers
        disabled_data = json.loads(disabled_file.read_text())
        assert disabled_data["mcpServers"] == {}

    def test_preserves_other_config_fields_in_active_file(
        self, plugin, mcp_harness, active_file
    ):
        """Test that disable/enable preserves other fields in active file (mcpEnabled, etc)."""
        # Setup: Active file with additional fields
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "someOtherField": "value",
                "mcpServers": {
                    "test-server": {
                        "command": "npx",
                        "args": ["-y", "test-server"],
                        "type": "stdio",
                    }
                },
            },
        )

        # Execute: Disable server
        result = plugin.disable_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: Other fields preserved
        active_data = json.loads(active_file.read_text())
        assert active_data["mcpEnabled"] is True
        assert active_data["someOtherField"] == "value"

        # Execute: Enable server
        result = plugin.enable_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: Other fields still preserved
        active_data = json.loads(active_file.read_text())
        assert active_data["mcpEnabled"] is True
        assert active_data["someOtherField"] == "value"


class TestUserGlobalDisableMechanismE2E:
    """End-to-end tests for user-mcp disable mechanism.

    These tests verify the complete workflow including validation criteria.
    """

    @pytest.fixture
    def plugin(self, mcp_harness):
        """Create a ClaudeCodePlugin with test harness."""
        return ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

    def test_validation_criterion_1_enabled_servers_match_claude_mcp_list(
        self, plugin, mcp_harness
    ):
        """VALIDATION CRITERION 1: ALL servers from `claude mcp list` MUST show as ENABLED.

        Simulates: `claude mcp list` returns servers from active file only.
        Requirement: `mcpi list` must show these same servers as ENABLED.
        """
        # Setup: Add servers to active file (these would be in `claude mcp list`)
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {
                    "active-server-1": {
                        "command": "npx",
                        "args": ["-y", "active-server-1"],
                        "type": "stdio",
                    },
                    "active-server-2": {
                        "command": "npx",
                        "args": ["-y", "active-server-2"],
                        "type": "stdio",
                    },
                },
            },
        )

        # Execute: List servers (equivalent to `mcpi list`)
        servers = plugin.list_servers(scope="user-mcp")

        # Verify: Both servers shown as ENABLED
        server_states = {info.id: info.state for info in servers.values()}
        assert server_states["active-server-1"] == ServerState.ENABLED
        assert server_states["active-server-2"] == ServerState.ENABLED

    def test_validation_criterion_2_disabled_servers_not_in_claude_mcp_list(
        self, plugin, mcp_harness
    ):
        """VALIDATION CRITERION 2: NO disabled servers should appear in `claude mcp list`.

        Simulates: Disabled servers are in disabled-mcp.json, NOT in settings.json.
        Requirement: `claude mcp list` (which reads settings.json) won't see them.
        """
        # Setup: Add server to disabled file (NOT in active file)
        disabled_file = mcp_harness.path_overrides["user-mcp-disabled"]
        disabled_file.parent.mkdir(parents=True, exist_ok=True)
        disabled_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "disabled-server": {
                            "command": "npx",
                            "args": ["-y", "disabled-server"],
                            "type": "stdio",
                        }
                    }
                },
                indent=2,
            )
        )

        # Setup: Active file has NO servers
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {},
            },
        )

        # Verify: Active file is empty (simulates `claude mcp list` seeing nothing)
        active_file = mcp_harness.path_overrides["user-mcp"]
        active_data = json.loads(active_file.read_text())
        assert active_data["mcpServers"] == {}

        # Execute: List servers (equivalent to `mcpi list`)
        servers = plugin.list_servers(scope="user-mcp")

        # Verify: mcpi shows the disabled server
        server_ids = [info.id for info in servers.values()]
        assert "disabled-server" in server_ids

        # Verify: mcpi shows it as DISABLED
        disabled_info = next(
            info for info in servers.values() if info.id == "disabled-server"
        )
        assert disabled_info.state == ServerState.DISABLED

    def test_validation_criterion_3_only_mcpi_list_shows_disabled(
        self, plugin, mcp_harness
    ):
        """VALIDATION CRITERION 3: Disabled servers ONLY appear in `mcpi list` with state=DISABLED.

        Requirement: mcpi list must show disabled servers (from disabled-mcp.json)
        with correct DISABLED state.
        """
        # Setup: One enabled, one disabled
        mcp_harness.prepopulate_file(
            "user-mcp",
            {
                "mcpEnabled": True,
                "mcpServers": {
                    "enabled-server": {
                        "command": "npx",
                        "args": ["-y", "enabled-server"],
                        "type": "stdio",
                    }
                },
            },
        )

        disabled_file = mcp_harness.path_overrides["user-mcp-disabled"]
        disabled_file.parent.mkdir(parents=True, exist_ok=True)
        disabled_file.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "disabled-server": {
                            "command": "npx",
                            "args": ["-y", "disabled-server"],
                            "type": "stdio",
                        }
                    }
                },
                indent=2,
            )
        )

        # Execute: List servers
        servers = plugin.list_servers(scope="user-mcp")

        # Verify: Both servers appear
        server_ids = [info.id for info in servers.values()]
        assert "enabled-server" in server_ids
        assert "disabled-server" in server_ids

        # Verify: Correct states
        server_states = {info.id: info.state for info in servers.values()}
        assert server_states["enabled-server"] == ServerState.ENABLED
        assert server_states["disabled-server"] == ServerState.DISABLED

    def test_complete_workflow_add_disable_enable_remove(self, plugin, mcp_harness):
        """Test complete workflow: add → disable → enable → remove.

        This is the full user journey.
        """
        from mcpi.clients.types import ServerConfig

        # Step 1: Add server
        config = ServerConfig(
            command="npx",
            args=["-y", "test-server"],
            type="stdio",
        )
        result = plugin.add_server("test-server", config, scope="user-mcp")
        assert result.success

        # Verify: Server is ENABLED
        info = plugin.get_server_info("test-server", scope="user-mcp")
        assert info is not None
        assert info.state == ServerState.ENABLED

        # Step 2: Disable server
        result = plugin.disable_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: Server is DISABLED
        info = plugin.get_server_info("test-server", scope="user-mcp")
        assert info is not None
        assert info.state == ServerState.DISABLED

        # Step 3: Enable server
        result = plugin.enable_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: Server is ENABLED again
        info = plugin.get_server_info("test-server", scope="user-mcp")
        assert info is not None
        assert info.state == ServerState.ENABLED

        # Step 4: Remove server
        result = plugin.remove_server("test-server", scope="user-mcp")
        assert result.success

        # Verify: Server is gone
        info = plugin.get_server_info("test-server", scope="user-mcp")
        assert info is None
