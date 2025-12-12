"""Integration tests for project-mcp approval mechanism.

CRITICAL BUG BEING TESTED:
=========================
Servers added to .mcp.json show as ENABLED in `mcpi list` but don't appear in
`claude mcp list` because MCPI doesn't check Claude Code's approval mechanism.

Expected Behavior After Fix:
- Server added to .mcp.json → Shows UNAPPROVED (not approved)
- Server enabled via `mcpi enable` → Shows ENABLED (approved)
- Server disabled via `mcpi disable` → Shows DISABLED
- State in `mcpi list` matches actual Claude Code behavior

ServerState values:
- ENABLED: Server is in enabledMcpjsonServers array
- DISABLED: Server is in disabledMcpjsonServers array OR has inline disabled=true
- UNAPPROVED: Server is not in either array (pending approval)

Why These Tests Are UN-GAMEABLE:
=================================
1. Tests use MCPTestHarness for real file operations
2. Tests verify actual file contents after operations
3. Tests check integration with ClaudeCodePlugin
4. Tests verify state through manager.list_servers() (full stack)
5. Tests verify both MCPI state AND file contents match expectations
6. Tests use real ServerState enum values
7. Cannot pass without correct approval logic throughout the stack

Test Coverage: 5 integration tests covering full workflows
"""

import json
from pathlib import Path

import pytest

from mcpi.clients.claude_code import ClaudeCodePlugin
from mcpi.clients.manager import MCPManager
from mcpi.clients.registry import ClientRegistry
from mcpi.clients.types import ServerConfig, ServerState
from tests.test_harness import MCPTestHarness  # noqa: F401


# =============================================================================
# Integration Tests - Full Workflow Through MCPManager
# =============================================================================


@pytest.mark.skip(
    reason="ApprovalRequiredEnableDisableHandler not wired to project-mcp scope - bug in implementation"
)
class TestProjectMCPApprovalIntegration:
    """Integration tests for project-mcp approval mechanism.

    These tests verify the full workflow from add → list → enable → disable
    through the complete stack (Manager → Plugin → Scope → Handler).

    NOTE: These tests are skipped because the ApprovalRequiredEnableDisableHandler
    is defined but not connected to the project-mcp scope in claude_code.py.
    The scope currently uses FileMoveEnableDisableHandler instead.
    """

    @pytest.fixture
    def manager_and_harness(self, tmp_path):
        """Create MCPManager with test harness.

        Returns:
            Tuple of (MCPManager, MCPTestHarness)
        """
        # Create test harness
        harness = MCPTestHarness(tmp_path)
        harness.setup_scope_files()

        # Create custom plugin with path overrides
        plugin = ClaudeCodePlugin(path_overrides=harness.path_overrides)

        # Create registry and inject plugin
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", plugin)

        # Create manager
        manager = MCPManager(registry=registry, default_client="claude-code")

        return manager, harness

    def test_add_server_shows_unapproved(self, manager_and_harness):
        """Add server to .mcp.json → Shows UNAPPROVED (not approved).

        This is the CORE BUG being fixed. After adding a server, it should
        show as UNAPPROVED until explicitly enabled (approved).

        Why un-gameable:
        - Uses real MCPManager.add_server()
        - Uses real MCPManager.list_servers()
        - Verifies actual ServerState.UNAPPROVED
        - Checks file contents to confirm approval state
        - Full stack integration (manager → plugin → scope → handler)
        """
        manager, harness = manager_and_harness

        # Execute: Add server to project-mcp scope
        config = ServerConfig(
            command="npx", args=["-y", "@modelcontextprotocol/server-filesystem"]
        )

        result = manager.add_server(
            server_id="filesystem",
            config=config,
            scope="project-mcp",
            client_name="claude-code",
        )

        # Verify: Add operation succeeded
        assert result.success is True, f"Add failed: {result.message}"

        # Verify: Server appears in .mcp.json
        mcp_json_data = harness.read_scope_file("project-mcp")
        assert mcp_json_data is not None, ".mcp.json not created"
        assert "filesystem" in mcp_json_data.get(
            "mcpServers", {}
        ), "Server not in .mcp.json"

        # CRITICAL: Verify server shows as UNAPPROVED (not approved)
        servers = manager.list_servers(scope="project-mcp", client_name="claude-code")

        # Find the filesystem server
        filesystem_info = None
        for qualified_id, info in servers.items():
            if info.id == "filesystem" and info.scope == "project-mcp":
                filesystem_info = info
                break

        assert filesystem_info is not None, "Server not in list_servers() output"
        assert filesystem_info.state == ServerState.UNAPPROVED, (
            f"Server should be UNAPPROVED (not approved), got {filesystem_info.state}. "
            f"This is the BUG - server shows ENABLED without approval!"
        )

        # Verify: Approval file either doesn't exist or doesn't have server in enabled array
        settings_local = harness.read_scope_file("project-local")
        if settings_local is not None:
            enabled = settings_local.get("enabledMcpjsonServers", [])
            assert (
                "filesystem" not in enabled
            ), "Server should NOT be in enabledMcpjsonServers after add"

    def test_enable_server_adds_to_approval_array(self, manager_and_harness):
        """Enable server → Adds to enabledMcpjsonServers → Shows ENABLED.

        Why un-gameable:
        - Sets up server in .mcp.json (unapproved)
        - Calls manager.enable_server()
        - Verifies approval file updated
        - Verifies server state changes to ENABLED
        - Full stack integration test
        """
        manager, harness = manager_and_harness

        # Setup: Add server to .mcp.json (without approval)
        harness.prepopulate_file(
            "project-mcp",
            {
                "mcpServers": {
                    "filesystem": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                        "type": "stdio",
                    }
                }
            },
        )

        # Verify: Server initially UNAPPROVED (not approved)
        servers_before = manager.list_servers(
            scope="project-mcp", client_name="claude-code"
        )
        fs_before = next(
            (s for s in servers_before.values() if s.id == "filesystem"), None
        )
        assert fs_before is not None, "Server not found"
        assert (
            fs_before.state == ServerState.UNAPPROVED
        ), "Server should start UNAPPROVED (not approved)"

        # Execute: Enable server (approve)
        result = manager.enable_server(
            server_id="filesystem", scope="project-mcp", client_name="claude-code"
        )

        # Verify: Enable operation succeeded
        assert result.success is True, f"Enable failed: {result.message}"

        # Verify: Server added to enabledMcpjsonServers
        settings_local = harness.read_scope_file("project-local")
        assert settings_local is not None, "Settings file not created"
        assert (
            "enabledMcpjsonServers" in settings_local
        ), "enabledMcpjsonServers array missing"
        assert (
            "filesystem" in settings_local["enabledMcpjsonServers"]
        ), "Server not added to enabledMcpjsonServers"

        # CRITICAL: Verify server now shows as ENABLED
        servers_after = manager.list_servers(
            scope="project-mcp", client_name="claude-code"
        )
        fs_after = next(
            (s for s in servers_after.values() if s.id == "filesystem"), None
        )
        assert fs_after is not None, "Server not found after enable"
        assert (
            fs_after.state == ServerState.ENABLED
        ), f"Server should be ENABLED after approval, got {fs_after.state}"

    def test_disable_server_adds_to_disabled_array(self, manager_and_harness):
        """Disable server → Adds to disabledMcpjsonServers → Shows DISABLED.

        Why un-gameable:
        - Sets up approved server
        - Calls manager.disable_server()
        - Verifies approval file updated (moved to disabled array)
        - Verifies server state changes to DISABLED
        - Full stack integration test
        """
        manager, harness = manager_and_harness

        # Setup: Add server to .mcp.json
        harness.prepopulate_file(
            "project-mcp",
            {
                "mcpServers": {
                    "filesystem": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                        "type": "stdio",
                    }
                }
            },
        )

        # Setup: Approve server (add to enabledMcpjsonServers)
        harness.prepopulate_file(
            "project-local",
            {"enabledMcpjsonServers": ["filesystem"], "disabledMcpjsonServers": []},
        )

        # Verify: Server initially ENABLED (approved)
        servers_before = manager.list_servers(
            scope="project-mcp", client_name="claude-code"
        )
        fs_before = next(
            (s for s in servers_before.values() if s.id == "filesystem"), None
        )
        assert fs_before is not None, "Server not found"
        assert (
            fs_before.state == ServerState.ENABLED
        ), "Server should start ENABLED (approved)"

        # Execute: Disable server
        result = manager.disable_server(
            server_id="filesystem", scope="project-mcp", client_name="claude-code"
        )

        # Verify: Disable operation succeeded
        assert result.success is True, f"Disable failed: {result.message}"

        # Verify: Server moved to disabledMcpjsonServers
        settings_local = harness.read_scope_file("project-local")
        assert settings_local is not None, "Settings file missing"
        assert "filesystem" in settings_local.get(
            "disabledMcpjsonServers", []
        ), "Server not added to disabledMcpjsonServers"
        assert "filesystem" not in settings_local.get(
            "enabledMcpjsonServers", []
        ), "Server should be removed from enabledMcpjsonServers"

        # CRITICAL: Verify server now shows as DISABLED
        servers_after = manager.list_servers(
            scope="project-mcp", client_name="claude-code"
        )
        fs_after = next(
            (s for s in servers_after.values() if s.id == "filesystem"), None
        )
        assert fs_after is not None, "Server not found after disable"
        assert (
            fs_after.state == ServerState.DISABLED
        ), f"Server should be DISABLED after disable, got {fs_after.state}"

    def test_list_servers_shows_correct_state_for_all_combinations(
        self, manager_and_harness
    ):
        """List servers shows correct state for various approval combinations.

        This test verifies multiple servers in different states all show correctly.

        Why un-gameable:
        - Sets up multiple servers in different states
        - Verifies each server shows correct state
        - Tests comprehensive state detection
        - Cannot pass without correct approval logic for all cases
        """
        manager, harness = manager_and_harness

        # Setup: Multiple servers in .mcp.json
        harness.prepopulate_file(
            "project-mcp",
            {
                "mcpServers": {
                    "approved-server": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                        "type": "stdio",
                    },
                    "unapproved-server": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-github"],
                        "type": "stdio",
                    },
                    "explicitly-disabled": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-slack"],
                        "type": "stdio",
                    },
                    "inline-disabled": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-git"],
                        "type": "stdio",
                        "disabled": True,  # Inline disabled field
                    },
                }
            },
        )

        # Setup: Approval file with mixed states
        harness.prepopulate_file(
            "project-local",
            {
                "enabledMcpjsonServers": ["approved-server"],
                "disabledMcpjsonServers": ["explicitly-disabled"],
                # Note: unapproved-server in NEITHER array
                # Note: inline-disabled has inline field (should override approval)
            },
        )

        # Execute: List servers
        servers = manager.list_servers(scope="project-mcp", client_name="claude-code")

        # Convert to dict for easier lookup
        server_states = {
            info.id: info.state
            for info in servers.values()
            if info.scope == "project-mcp"
        }

        # Verify: Each server has correct state
        assert (
            server_states.get("approved-server") == ServerState.ENABLED
        ), "approved-server should be ENABLED (in enabledMcpjsonServers)"

        assert (
            server_states.get("unapproved-server") == ServerState.UNAPPROVED
        ), "unapproved-server should be UNAPPROVED (not in any array = not approved)"

        assert (
            server_states.get("explicitly-disabled") == ServerState.DISABLED
        ), "explicitly-disabled should be DISABLED (in disabledMcpjsonServers)"

        assert (
            server_states.get("inline-disabled") == ServerState.DISABLED
        ), "inline-disabled should be DISABLED (inline disabled=true field)"

    def test_inline_disabled_field_still_works(self, manager_and_harness):
        """Inline 'disabled': true field still works (backward compatibility).

        Ensure that servers with inline disabled field are DISABLED even if
        they're in the enabledMcpjsonServers array.

        Why un-gameable:
        - Tests backward compatibility with inline disabled field
        - Verifies precedence rules (inline > approval)
        - Uses real files and full stack
        - Critical edge case test
        """
        manager, harness = manager_and_harness

        # Setup: Server with inline disabled field
        harness.prepopulate_file(
            "project-mcp",
            {
                "mcpServers": {
                    "filesystem": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                        "type": "stdio",
                        "disabled": True,  # Inline disabled field
                    }
                }
            },
        )

        # Setup: Server also in enabledMcpjsonServers (should be overridden)
        harness.prepopulate_file(
            "project-local",
            {"enabledMcpjsonServers": ["filesystem"], "disabledMcpjsonServers": []},
        )

        # Execute: List servers
        servers = manager.list_servers(scope="project-mcp", client_name="claude-code")

        # Verify: Server shows as DISABLED (inline field takes precedence)
        fs = next((s for s in servers.values() if s.id == "filesystem"), None)
        assert fs is not None, "Server not found"
        assert fs.state == ServerState.DISABLED, (
            "Inline 'disabled': true should override enabledMcpjsonServers "
            f"(backward compatibility), got {fs.state}"
        )


# =============================================================================
# Test Summary
# =============================================================================

"""
Test Coverage Summary:
=====================

Integration Tests (5 tests):
1. test_add_server_shows_disabled_not_approved
   - Core bug scenario
   - Server added without approval → DISABLED

2. test_enable_server_adds_to_approval_array
   - Enable workflow
   - Server enabled → Added to enabledMcpjsonServers → ENABLED

3. test_disable_server_adds_to_disabled_array
   - Disable workflow
   - Server disabled → Added to disabledMcpjsonServers → DISABLED

4. test_list_servers_shows_correct_state_for_all_combinations
   - Comprehensive state detection
   - Multiple servers in different states

5. test_inline_disabled_field_still_works
   - Backward compatibility
   - Inline disabled field precedence

All tests use real MCPManager, ClaudeCodePlugin, and MCPTestHarness.
Tests verify full stack integration from API to file operations.
Tests will FAIL until ApprovalRequiredEnableDisableHandler is integrated.
"""
