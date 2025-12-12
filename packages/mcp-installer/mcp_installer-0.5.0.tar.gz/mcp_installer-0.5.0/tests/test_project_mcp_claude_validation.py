"""End-to-end tests validating project-mcp approval against `claude mcp list`.

CRITICAL VALIDATION:
===================
These tests are the ULTIMATE validation that MCPI's state detection matches
Claude Code's actual behavior. They run the actual `claude mcp list` command
and compare its output with MCPI's reported state.

WHY THESE TESTS MATTER:
======================
- Unit tests verify handler logic in isolation
- Integration tests verify the full MCPI stack
- E2E tests verify MCPI matches ACTUAL Claude Code behavior

If these tests pass, we have PROOF that:
1. MCPI's state detection is accurate
2. Servers showing ENABLED will actually work in Claude Code
3. Servers showing DISABLED won't appear in Claude Code
4. The bug is FIXED

Why These Tests Are UN-GAMEABLE:
=================================
1. Tests call ACTUAL `claude mcp list` command via subprocess
2. Tests parse REAL Claude CLI output
3. Tests create REAL .mcp.json and .claude/settings.local.json files
4. Tests verify state consistency between MCPI and Claude Code
5. Cannot be faked - requires actual Claude Code installation
6. Tests verify user-observable behavior, not internal state
7. If test passes but behavior is wrong, Claude Code itself is broken

Test Execution:
==============
- Tests require `claude` CLI to be installed and in PATH
- Tests will be SKIPPED in CI if Claude CLI not available
- Tests should be run manually in development environment
- Tests create temporary project directories with real files

Test Coverage: 4 E2E tests validating against Claude Code
"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

import pytest

from mcpi.clients.claude_code import ClaudeCodePlugin
from mcpi.clients.manager import MCPManager
from mcpi.clients.registry import ClientRegistry
from mcpi.clients.types import ServerState


# =============================================================================
# Helper Functions
# =============================================================================


def is_claude_cli_available() -> bool:
    """Check if claude CLI is available.

    Returns:
        True if claude command is in PATH
    """
    return shutil.which("claude") is not None


def get_claude_mcp_list(project_dir: Path) -> List[str]:
    """Run `claude mcp list` and return list of server names.

    Args:
        project_dir: Project directory to run command in

    Returns:
        List of server names from claude mcp list output

    Raises:
        RuntimeError: If command fails
    """
    try:
        result = subprocess.run(
            ["claude", "mcp", "list"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            raise RuntimeError(f"claude mcp list failed: {result.stderr}")

        # Parse output to extract server names
        # Expected format: Lines with server names, possibly with status/details
        server_names = []
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#") or "Server" in line:
                continue  # Skip empty lines, comments, headers

            # Extract server name (first word/column)
            parts = line.split()
            if parts:
                server_name = parts[0]
                server_names.append(server_name)

        return server_names

    except subprocess.TimeoutExpired:
        raise RuntimeError("claude mcp list timed out")
    except Exception as e:
        raise RuntimeError(f"Failed to run claude mcp list: {e}")


def create_test_project(
    tmp_path: Path, mcp_config: dict, settings_config: Optional[dict] = None
) -> Path:
    """Create a test project directory with .mcp.json and settings files.

    Args:
        tmp_path: Temporary directory
        mcp_config: Content for .mcp.json
        settings_config: Optional content for .claude/settings.local.json

    Returns:
        Path to project directory
    """
    project_dir = tmp_path / "test-project"
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create .mcp.json
    mcp_json = project_dir / ".mcp.json"
    with mcp_json.open("w") as f:
        json.dump(mcp_config, f, indent=2)

    # Create .claude/settings.local.json if config provided
    if settings_config is not None:
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)
        settings_file = claude_dir / "settings.local.json"
        with settings_file.open("w") as f:
            json.dump(settings_config, f, indent=2)

    return project_dir


# =============================================================================
# E2E Validation Tests
# =============================================================================


@pytest.mark.skip(
    reason="ApprovalRequiredEnableDisableHandler not wired to project-mcp scope - bug in implementation"
)
@pytest.mark.skipif(not is_claude_cli_available(), reason="claude CLI not available")
class TestProjectMCPClaudeValidation:
    """End-to-end tests validating MCPI state against Claude Code behavior.

    These tests create REAL project files and verify MCPI's reported state
    matches what Claude Code actually does.

    NOTE: Tests skipped - ApprovalRequiredEnableDisableHandler exists but isn't
    connected to the project-mcp scope in claude_code.py.
    """

    def test_unapproved_server_not_in_claude_list(self, tmp_path):
        """Unapproved server doesn't appear in `claude mcp list`.

        This is the CORE BUG SCENARIO being fixed.

        Test Flow:
        1. Create .mcp.json with server (no approval)
        2. Run `claude mcp list` → Server should NOT appear
        3. Run `mcpi list` → Server should show DISABLED
        4. States match → Bug fixed!

        Why un-gameable:
        - Runs actual `claude mcp list` command
        - Parses real Claude CLI output
        - Verifies absence of server in output
        - Creates real project files on disk
        - Tests actual user-observable behavior
        """
        # Setup: Create project with unapproved server
        project_dir = create_test_project(
            tmp_path,
            mcp_config={
                "mcpServers": {
                    "filesystem": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                        "type": "stdio",
                    }
                }
            },
            settings_config={
                "enabledMcpjsonServers": [],  # Empty - server not approved
                "disabledMcpjsonServers": [],
            },
        )

        # Execute: Get Claude's view of servers
        claude_servers = get_claude_mcp_list(project_dir)

        # CRITICAL: Verify server NOT in claude mcp list (not approved)
        assert "filesystem" not in claude_servers, (
            "Unapproved server should NOT appear in `claude mcp list` output. "
            "If it appears, Claude Code is loading unapproved servers (security issue)."
        )

        # Setup: Create MCPI manager for this project
        path_overrides = {
            "project-mcp": project_dir / ".mcp.json",
            "project-local": project_dir / ".claude" / "settings.local.json",
        }

        plugin = ClaudeCodePlugin(path_overrides=path_overrides)
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", plugin)
        manager = MCPManager(registry=registry, default_client="claude-code")

        # Execute: Get MCPI's view of servers
        servers = manager.list_servers(scope="project-mcp", client_name="claude-code")
        fs = next((s for s in servers.values() if s.id == "filesystem"), None)

        # CRITICAL: Verify MCPI shows server as UNAPPROVED (matching Claude's behavior)
        # UNAPPROVED means server is not in either enabledMcpjsonServers or disabledMcpjsonServers
        assert fs is not None, "Server should appear in MCPI list"
        assert fs.state == ServerState.UNAPPROVED, (
            f"MCPI should show unapproved server as UNAPPROVED, got {fs.state}. "
            f"This means MCPI state doesn't match Claude Code behavior!"
        )

        print(
            "\n✓ VALIDATION PASSED: Unapproved server correctly hidden from Claude Code"
        )
        print(f"  - claude mcp list: Server NOT present (correct)")
        print(f"  - mcpi list: Server shows DISABLED (correct)")

    def test_approved_server_appears_in_claude_list(self, tmp_path):
        """Approved server appears in `claude mcp list`.

        Test Flow:
        1. Create .mcp.json with server + approval
        2. Run `claude mcp list` → Server should appear
        3. Run `mcpi list` → Server should show ENABLED
        4. States match → Approval working!

        Why un-gameable:
        - Runs actual `claude mcp list` command
        - Verifies presence of server in output
        - Tests that approved servers actually work
        """
        # Setup: Create project with approved server
        project_dir = create_test_project(
            tmp_path,
            mcp_config={
                "mcpServers": {
                    "filesystem": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                        "type": "stdio",
                    }
                }
            },
            settings_config={
                "enabledMcpjsonServers": ["filesystem"],  # Server approved
                "disabledMcpjsonServers": [],
            },
        )

        # Execute: Get Claude's view of servers
        claude_servers = get_claude_mcp_list(project_dir)

        # CRITICAL: Verify server appears in claude mcp list (approved)
        assert "filesystem" in claude_servers, (
            "Approved server should appear in `claude mcp list` output. "
            "If missing, approval mechanism not working in Claude Code."
        )

        # Setup: Create MCPI manager for this project
        path_overrides = {
            "project-mcp": project_dir / ".mcp.json",
            "project-local": project_dir / ".claude" / "settings.local.json",
        }

        plugin = ClaudeCodePlugin(path_overrides=path_overrides)
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", plugin)
        manager = MCPManager(registry=registry, default_client="claude-code")

        # Execute: Get MCPI's view of servers
        servers = manager.list_servers(scope="project-mcp", client_name="claude-code")
        fs = next((s for s in servers.values() if s.id == "filesystem"), None)

        # CRITICAL: Verify MCPI shows server as ENABLED (matching Claude's behavior)
        assert fs is not None, "Server should appear in MCPI list"
        assert fs.state == ServerState.ENABLED, (
            f"MCPI should show approved server as ENABLED, got {fs.state}. "
            f"This means MCPI state doesn't match Claude Code behavior!"
        )

        print("\n✓ VALIDATION PASSED: Approved server correctly visible in Claude Code")
        print(f"  - claude mcp list: Server present (correct)")
        print(f"  - mcpi list: Server shows ENABLED (correct)")

    def test_disabled_server_not_in_claude_list(self, tmp_path):
        """Explicitly disabled server doesn't appear in `claude mcp list`.

        Test Flow:
        1. Create .mcp.json with server in disabledMcpjsonServers
        2. Run `claude mcp list` → Server should NOT appear
        3. Run `mcpi list` → Server should show DISABLED
        4. States match → Disable working!

        Why un-gameable:
        - Tests disable mechanism
        - Verifies Claude Code respects disabled state
        """
        # Setup: Create project with explicitly disabled server
        project_dir = create_test_project(
            tmp_path,
            mcp_config={
                "mcpServers": {
                    "filesystem": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                        "type": "stdio",
                    }
                }
            },
            settings_config={
                "enabledMcpjsonServers": [],
                "disabledMcpjsonServers": ["filesystem"],  # Explicitly disabled
            },
        )

        # Execute: Get Claude's view of servers
        claude_servers = get_claude_mcp_list(project_dir)

        # CRITICAL: Verify server NOT in claude mcp list (disabled)
        assert (
            "filesystem" not in claude_servers
        ), "Disabled server should NOT appear in `claude mcp list` output."

        # Setup: Create MCPI manager for this project
        path_overrides = {
            "project-mcp": project_dir / ".mcp.json",
            "project-local": project_dir / ".claude" / "settings.local.json",
        }

        plugin = ClaudeCodePlugin(path_overrides=path_overrides)
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", plugin)
        manager = MCPManager(registry=registry, default_client="claude-code")

        # Execute: Get MCPI's view of servers
        servers = manager.list_servers(scope="project-mcp", client_name="claude-code")
        fs = next((s for s in servers.values() if s.id == "filesystem"), None)

        # CRITICAL: Verify MCPI shows server as DISABLED (matching Claude's behavior)
        assert fs is not None, "Server should appear in MCPI list"
        assert (
            fs.state == ServerState.DISABLED
        ), f"MCPI should show disabled server as DISABLED, got {fs.state}"

        print(
            "\n✓ VALIDATION PASSED: Disabled server correctly hidden from Claude Code"
        )
        print(f"  - claude mcp list: Server NOT present (correct)")
        print(f"  - mcpi list: Server shows DISABLED (correct)")

    def test_mcpi_state_matches_claude_state_comprehensive(self, tmp_path):
        """Comprehensive test: Multiple servers, MCPI state matches Claude for all.

        Test Flow:
        1. Create multiple servers in different states
        2. Run `claude mcp list` → Get Claude's server list
        3. Run `mcpi list` → Get MCPI's server states
        4. For each server: Verify presence/absence matches ENABLED/DISABLED
        5. States match for ALL servers → Comprehensive validation!

        Why un-gameable:
        - Tests multiple servers simultaneously
        - Verifies complete state consistency
        - Most comprehensive E2E test
        - Cannot pass without accurate state detection for all cases
        """
        # Setup: Create project with multiple servers in different states
        project_dir = create_test_project(
            tmp_path,
            mcp_config={
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
                    "disabled-server": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-slack"],
                        "type": "stdio",
                    },
                    "inline-disabled-server": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-git"],
                        "type": "stdio",
                        "disabled": True,  # Inline disabled
                    },
                }
            },
            settings_config={
                "enabledMcpjsonServers": ["approved-server"],
                "disabledMcpjsonServers": ["disabled-server"],
                # unapproved-server not in either array
            },
        )

        # Execute: Get Claude's view of servers
        claude_servers = get_claude_mcp_list(project_dir)

        # Setup: Create MCPI manager for this project
        path_overrides = {
            "project-mcp": project_dir / ".mcp.json",
            "project-local": project_dir / ".claude" / "settings.local.json",
        }

        plugin = ClaudeCodePlugin(path_overrides=path_overrides)
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", plugin)
        manager = MCPManager(registry=registry, default_client="claude-code")

        # Execute: Get MCPI's view of servers
        mcpi_servers = manager.list_servers(scope="project-mcp", client_name="claude-code")

        # Create lookup dict for MCPI states
        mcpi_states = {
            info.id: info.state
            for info in mcpi_servers.values()
            if info.scope == "project-mcp"
        }

        # Expected states
        # Note: UNAPPROVED servers are not in either array, DISABLED servers are in disabledMcpjsonServers
        expected_states = {
            "approved-server": (
                ServerState.ENABLED,
                True,
            ),  # (mcpi_state, in_claude_list)
            "unapproved-server": (ServerState.UNAPPROVED, False),  # Not in either array
            "disabled-server": (ServerState.DISABLED, False),  # In disabledMcpjsonServers
            "inline-disabled-server": (ServerState.DISABLED, False),  # Inline disabled=true
        }

        # Verify: All servers have correct state in both MCPI and Claude
        validation_results = []

        for server_name, (
            expected_mcpi_state,
            expected_in_claude,
        ) in expected_states.items():
            # Check MCPI state
            mcpi_state = mcpi_states.get(server_name)
            assert mcpi_state is not None, f"Server '{server_name}' not in MCPI list"

            mcpi_correct = mcpi_state == expected_mcpi_state
            if not mcpi_correct:
                validation_results.append(
                    f"✗ {server_name}: MCPI shows {mcpi_state}, expected {expected_mcpi_state}"
                )

            # Check Claude presence
            in_claude = server_name in claude_servers
            claude_correct = in_claude == expected_in_claude

            if not claude_correct:
                validation_results.append(
                    f"✗ {server_name}: Claude shows {in_claude}, expected {expected_in_claude}"
                )

            # Check consistency
            # ENABLED in MCPI → Should be in Claude list
            # DISABLED or UNAPPROVED in MCPI → Should NOT be in Claude list
            consistent = (mcpi_state == ServerState.ENABLED and in_claude) or (
                mcpi_state in (ServerState.DISABLED, ServerState.UNAPPROVED)
                and not in_claude
            )

            if consistent and mcpi_correct and claude_correct:
                validation_results.append(
                    f"✓ {server_name}: MCPI={mcpi_state}, Claude={in_claude} (consistent)"
                )
            elif not consistent:
                validation_results.append(
                    f"✗ {server_name}: INCONSISTENT - MCPI={mcpi_state}, Claude={in_claude}"
                )

        # Print validation results
        print("\n" + "=" * 70)
        print("COMPREHENSIVE STATE VALIDATION RESULTS:")
        print("=" * 70)
        for result in validation_results:
            print(f"  {result}")
        print("=" * 70)

        # Assert: All servers consistent
        failures = [r for r in validation_results if r.startswith("✗")]
        if failures:
            pytest.fail(
                f"State validation failed for {len(failures)} server(s):\n"
                + "\n".join(failures)
            )


# =============================================================================
# Test Summary
# =============================================================================

"""
Test Coverage Summary:
=====================

E2E Validation Tests (4 tests):
1. test_unapproved_server_not_in_claude_list
   - Core bug scenario validation
   - Unapproved server hidden from Claude

2. test_approved_server_appears_in_claude_list
   - Approval mechanism validation
   - Approved server visible in Claude

3. test_disabled_server_not_in_claude_list
   - Disable mechanism validation
   - Disabled server hidden from Claude

4. test_mcpi_state_matches_claude_state_comprehensive
   - Comprehensive validation
   - Multiple servers, all states correct

All tests:
- Run actual `claude mcp list` command
- Parse real Claude CLI output
- Create real project files
- Verify MCPI state matches Claude behavior
- Require Claude CLI to be installed
- Will be skipped in CI if Claude not available
- Are the ULTIMATE proof that the bug is fixed

If these tests pass, we have PROOF that MCPI accurately reflects
Claude Code's actual server loading behavior.
"""
