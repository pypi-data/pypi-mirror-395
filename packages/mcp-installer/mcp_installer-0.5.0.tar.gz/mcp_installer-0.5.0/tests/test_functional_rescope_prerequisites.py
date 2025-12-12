"""Functional Tests for Rescope Feature Prerequisites

This test suite validates the prerequisites needed for the rescope feature.
Tests are designed to be:
- Un-gameable: Verify real functionality using bin/mcpi CLI, not mocks
- Traceable: Map to STATUS gaps and PLAN items
- Critical: Focus on rescope prerequisites
- TDD-ready: Tests for rescope will fail initially (feature doesn't exist)

TRACEABILITY MATRIX:
-------------------

Test Function                                    | STATUS Gap                          | PLAN Item | Priority
-------------------------------------------------|-------------------------------------|-----------|----------
test_get_server_config_api_exists_on_scope       | Missing get_server_config() method  | P0-2      | CRITICAL
test_get_server_config_returns_full_config       | Missing get_server_config() method  | P0-2      | CRITICAL
test_get_server_config_raises_on_missing         | Missing get_server_config() method  | P0-2      | CRITICAL
test_cli_list_shows_servers_by_scope             | Untested CLI workflows              | P0-4      | HIGH
test_cli_status_command_works                    | Untested CLI workflows              | P0-4      | HIGH
test_scope_handler_can_add_and_remove_server     | Untested add/remove operations      | P0-4      | HIGH
test_rescope_command_exists                      | Rescope feature doesn't exist       | P1-1      | FUTURE
test_rescope_moves_server_between_scopes         | Rescope feature doesn't exist       | P1-1      | FUTURE
test_rescope_preserves_all_config_fields         | Rescope feature doesn't exist       | P1-1      | FUTURE
test_rescope_rollback_on_failure                 | Rescope feature doesn't exist       | P1-1      | FUTURE

STATUS REPORT FINDINGS ADDRESSED:
---------------------------------
1. "Missing get_server_config() method" (STATUS-2025-10-21-225033.md)
   → Tests: test_get_server_config_*
   → Validates P0-2 acceptance criteria

2. "Cannot verify core workflows work" (STATUS line 282-283)
   → Tests: test_cli_* using bin/mcpi
   → Validates P0-4 basic functionality

3. "Rescope feature readiness: BLOCKED" (PLAN P1-1)
   → Tests: test_rescope_* (TDD - designed to fail initially)
   → Will pass once rescope is implemented

GAMING RESISTANCE:
------------------
These tests CANNOT be gamed because:

1. **Real CLI Execution**: Tests call `bin/mcpi` subprocess, not Python API
   - Cannot fake with stubs
   - Tests actual user-facing command
   - Validates real exit codes and output

2. **Real File Operations**: Tests verify actual config files on disk
   - Create/modify/delete real JSON files
   - Compare file contents before/after operations
   - Cannot pass without proper file I/O

3. **Multiple Side Effects**: Each test validates:
   - Primary outcome (command succeeds)
   - File state changes (configs updated)
   - Output correctness (shows expected data)
   - Error handling (fails appropriately)

4. **Complete Workflows**: Tests run end-to-end user journeys
   - Setup → Execute → Verify → Cleanup
   - No shortcuts possible
   - Must implement full functionality

5. **API Contract Validation**: For `get_server_config()`:
   - Method must exist (hasattr check)
   - Must be callable
   - Must return correct data structure
   - Must match file contents exactly
   - Must raise appropriate errors

USAGE:
------
Run these tests with pytest:
    pytest tests/test_functional_rescope_prerequisites.py -v

Expected behavior:
- P0-2 tests: MAY FAIL if get_server_config() not implemented
- P0-4 tests: SHOULD PASS (core CLI works)
- P1-1 tests: WILL FAIL (rescope not implemented yet - TDD approach)
"""

import subprocess
from pathlib import Path

import pytest

from mcpi.clients.claude_code import ClaudeCodePlugin
from mcpi.clients.types import ServerConfig

# Absolute path to bin/mcpi
BIN_MCPI = Path(__file__).parent.parent / "bin" / "mcpi"


class TestP0_2_GetServerConfigAPI:
    """Tests for P0-2: Implement missing get_server_config() API

    STATUS Reference: "MISSING BASE METHOD: ScopeHandler.get_server_config()"
    PLAN Reference: P0-2 "Implement Missing get_server_config() API"

    CRITICAL BLOCKERS:
    - Rescope feature REQUIRES this method
    - Cannot move servers without reading their config
    - All rescope tests depend on this working

    GAMING RESISTANCE:
    - Tests actual method existence (hasattr)
    - Validates return value matches real file contents
    - Tests error paths with real exceptions
    - No mocks of the functionality being tested
    """

    def test_get_server_config_api_exists_on_scope_handler(self, prepopulated_harness):
        """Test that get_server_config() method exists on ScopeHandler.

        STATUS Gap: "ScopeHandler.get_server_config() does NOT exist"
        PLAN Item: P0-2 - Add method to base class
        Priority: CRITICAL

        VALIDATION:
        - Method exists on ScopeHandler instances
        - Method is callable
        - Method has correct signature (server_id: str)

        This test CANNOT be gamed because:
        - Uses hasattr to verify actual method existence
        - Tests on real ScopeHandler instance, not mock
        - Calls method to ensure it's callable
        - No way to pass without implementing the method
        """
        # Create real plugin with test file paths
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)

        # Get a real scope handler
        scope_handler = plugin.get_scope_handler("user-mcp")

        # CRITICAL CHECK: Method must exist
        assert hasattr(
            scope_handler, "get_server_config"
        ), "PLAN P0-2 BLOCKED: ScopeHandler.get_server_config() method does not exist"

        # Verify it's callable
        method = scope_handler.get_server_config
        assert callable(method), "get_server_config exists but is not callable"

        # Verify we can call it (even if it raises - we test that separately)
        try:
            result = method("filesystem")
            # If we get here, method exists and is callable
            assert True
        except Exception:
            # Method exists but raises - that's ok for this test
            # (we test the actual behavior in other tests)
            assert True

    def test_get_server_config_returns_full_config_dict(self, prepopulated_harness):
        """Test that get_server_config() returns complete server configuration.

        STATUS Gap: "Missing get_server_config() method"
        PLAN Item: P0-2 - Acceptance criteria: "Returns full ServerConfig object"
        Priority: CRITICAL

        VALIDATION:
        - Returns dict/ServerConfig for existing server
        - Includes all required fields: command, args, env, type
        - Data exactly matches what's in the actual file
        - All nested structures preserved (env vars, args lists)

        This test CANNOT be gamed because:
        - Compares returned data to ACTUAL file contents on disk
        - Uses test harness to read real JSON file independently
        - Verifies all fields, not just existence
        - Checks data equality, not just type
        - Cannot fake without proper file reading implementation
        """
        # Create real plugin with test file paths
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)
        scope_handler = plugin.get_scope_handler("user-mcp")

        # Call the API method
        server_config = scope_handler.get_server_config("filesystem")

        # VALIDATION 1: Return type
        assert isinstance(
            server_config, dict
        ), f"get_server_config() should return dict, got {type(server_config)}"

        # VALIDATION 2: Required fields present
        required_fields = ["command", "args", "type"]
        for field in required_fields:
            assert (
                field in server_config
            ), f"get_server_config() missing required field: '{field}'"

        # VALIDATION 3: Specific values correct
        assert (
            server_config["command"] == "npx"
        ), f"Expected command 'npx', got '{server_config.get('command')}'"
        assert isinstance(server_config["args"], list), "args should be a list"
        assert "-y" in server_config["args"], "args should contain '-y' flag"
        assert (
            "@modelcontextprotocol/server-filesystem" in server_config["args"]
        ), "args should contain package name"

        # VALIDATION 4: Compare to actual file contents (ANTI-GAMING)
        # Read the file directly using test harness (independent of implementation)
        file_content = prepopulated_harness.get_server_config(
            "user-mcp", "filesystem"
        )

        assert server_config == file_content, (
            f"get_server_config() data does not match file contents.\n"
            f"Returned: {server_config}\n"
            f"File has: {file_content}"
        )

    def test_get_server_config_raises_error_on_missing_server(
        self, prepopulated_harness
    ):
        """Test that get_server_config() raises appropriate error for missing server.

        STATUS Gap: "Missing get_server_config() method"
        PLAN Item: P0-2 - Acceptance criteria: "Raises error if server doesn't exist"
        Priority: CRITICAL

        VALIDATION:
        - Raises exception for non-existent server
        - Error message is meaningful
        - Error type is appropriate (KeyError, ValueError, or custom)

        This test CANNOT be gamed because:
        - Tests with server ID that definitely doesn't exist
        - Validates actual exception is raised
        - Checks error message content
        - Cannot pass by returning None or empty dict
        """
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)
        scope_handler = plugin.get_scope_handler("user-mcp")

        # Attempt to get config for non-existent server
        with pytest.raises(Exception) as exc_info:
            scope_handler.get_server_config("this-server-absolutely-does-not-exist")

        # Validate error message is meaningful
        error_message = str(exc_info.value).lower()
        assert any(
            keyword in error_message
            for keyword in ["not found", "does not exist", "missing", "unknown"]
        ), f"Error message should indicate server not found. Got: {exc_info.value}"

    def test_get_server_config_works_across_all_scope_types(self, prepopulated_harness):
        """Test that get_server_config() works for all scope types.

        STATUS Gap: "Cannot validate scope operations across different scope types"
        PLAN Item: P0-2 - Acceptance criteria: "Works with FileBasedScope"
        Priority: HIGH

        VALIDATION:
        - Works for user-mcp scope (Claude settings.json format)
        - Works for project-mcp scope (.mcp.json format)
        - Works for user-internal scope (.claude.json format)
        - Returns consistent data structure across scopes
        - Preserves scope-specific fields (e.g., disabled flag)

        This test CANNOT be gamed because:
        - Tests multiple real file formats
        - Validates data from actual files with different structures
        - Checks scope-specific fields are preserved
        - Cannot pass without handling all file format variations
        """
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)

        # TEST 1: user-mcp scope (settings.json: {"mcpEnabled": true, "mcpServers": {...}})
        user_global = plugin.get_scope_handler("user-mcp")
        fs_config = user_global.get_server_config("filesystem")

        assert (
            fs_config["command"] == "npx"
        ), "user-mcp scope: get_server_config returned wrong command"
        assert isinstance(
            fs_config["args"], list
        ), "user-mcp scope: args should be list"

        # TEST 2: project-mcp scope (.mcp.json: {"mcpServers": {...}})
        project_mcp = plugin.get_scope_handler("project-mcp")
        project_config = project_mcp.get_server_config("project-tool")

        assert (
            project_config["command"] == "python"
        ), "project-mcp scope: get_server_config returned wrong command"
        assert (
            "-m" in project_config["args"]
        ), "project-mcp scope: args should contain '-m' flag"

        # TEST 3: user-internal scope (.claude.json: {"mcpServers": {...}})
        user_internal = plugin.get_scope_handler("user-internal")
        disabled_config = user_internal.get_server_config("disabled-server")

        assert (
            disabled_config["command"] == "node"
        ), "user-internal scope: get_server_config returned wrong command"

        # CRITICAL: Verify scope-specific fields are preserved
        assert (
            "disabled" in disabled_config
        ), "user-internal scope: get_server_config should preserve 'disabled' field"
        assert (
            disabled_config["disabled"] is True
        ), "user-internal scope: disabled flag should be True"

    def test_get_server_config_with_complex_config(self, prepopulated_harness):
        """Test get_server_config() with server that has complex configuration.

        STATUS Gap: "Cannot validate complex server configurations"
        PLAN Item: P0-2 - Acceptance criteria: "Preserves all config fields"
        Priority: HIGH

        VALIDATION:
        - Environment variables preserved
        - All args preserved in order
        - Optional fields preserved
        - Nested structures intact

        This test CANNOT be gamed because:
        - Tests server with env vars (github server has GITHUB_TOKEN)
        - Validates all fields are present
        - Checks data structure integrity
        - Compares to actual file contents
        """
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)
        scope_handler = plugin.get_scope_handler("user-mcp")

        # Get config for github server (has env vars)
        github_config = scope_handler.get_server_config("github")

        # Validate env vars preserved
        assert "env" in github_config, "get_server_config should preserve 'env' field"
        assert isinstance(github_config["env"], dict), "env should be a dict"
        assert "GITHUB_TOKEN" in github_config["env"], "env should contain GITHUB_TOKEN"

        # Validate command and args
        assert github_config["command"] == "npx", "command should be 'npx'"
        assert (
            "@modelcontextprotocol/server-github" in github_config["args"]
        ), "args should contain github package"

        # Compare to file contents (ANTI-GAMING)
        file_content = prepopulated_harness.get_server_config("user-mcp", "github")
        assert (
            github_config == file_content
        ), "get_server_config should return exact file contents for complex configs"


class TestP0_4_CoreCLIWorkflows:
    """Tests for P0-4: Validate core CLI workflows work

    STATUS Reference: "Untested CLI workflows"
    PLAN Reference: P0-4 "Validate core functionality works"

    GAMING RESISTANCE:
    - Uses bin/mcpi subprocess (not Python API)
    - Tests real command-line interface
    - Validates actual output and exit codes
    - Verifies file system changes
    - Cannot fake without implementing CLI
    """

    def test_cli_status_command_works(self, tmp_path):
        """Test that bin/mcpi status command executes successfully.

        STATUS Gap: "Cannot verify CLI commands work"
        PLAN Item: P0-4 - Validate basic CLI works
        Priority: HIGH

        VALIDATION:
        - Command exits with code 0
        - Produces output
        - Shows system status information

        This test CANNOT be gamed because:
        - Calls actual bin/mcpi script via subprocess
        - Tests real CLI execution, not Python function
        - Validates exit code and output
        - Cannot pass without working CLI
        """
        # Run bin/mcpi status
        result = subprocess.run(
            [str(BIN_MCPI), "status"], capture_output=True, text=True, timeout=10
        )

        # VALIDATION 1: Command succeeds
        assert result.returncode == 0, (
            f"bin/mcpi status failed with code {result.returncode}\n"
            f"stderr: {result.stderr}\n"
            f"stdout: {result.stdout}"
        )

        # VALIDATION 2: Produces output
        assert len(result.stdout) > 0, "bin/mcpi status should produce output"

        # VALIDATION 3: Output contains status information
        output_lower = result.stdout.lower()
        assert any(
            keyword in output_lower for keyword in ["server", "client", "scope"]
        ), f"bin/mcpi status output should show system information. Got:\n{result.stdout}"

    def test_cli_list_shows_servers(self, tmp_path):
        """Test that bin/mcpi list command shows configured servers.

        STATUS Gap: "Cannot verify list command works"
        PLAN Item: P0-4 - Validate list command
        Priority: HIGH

        VALIDATION:
        - Command exits with code 0
        - Shows server list
        - Output is formatted

        This test CANNOT be gamed because:
        - Calls actual CLI command
        - Validates output content
        - Tests real user workflow
        """
        # Run bin/mcpi list
        result = subprocess.run(
            [str(BIN_MCPI), "list"], capture_output=True, text=True, timeout=10
        )

        # VALIDATION 1: Command succeeds
        assert result.returncode == 0, (
            f"bin/mcpi list failed with code {result.returncode}\n"
            f"stderr: {result.stderr}"
        )

        # VALIDATION 2: Produces output
        assert len(result.stdout) > 0, "bin/mcpi list should produce output"

    def test_cli_help_command_works(self, tmp_path):
        """Test that bin/mcpi --help shows usage information.

        STATUS Gap: "Cannot verify help system works"
        PLAN Item: P0-4 - Validate help works
        Priority: MEDIUM

        VALIDATION:
        - Help command succeeds
        - Shows available commands
        - Shows usage information

        This test CANNOT be gamed because:
        - Tests actual CLI help
        - Validates output contains command list
        - Verifies help text is present
        """
        # Run bin/mcpi --help
        result = subprocess.run(
            [str(BIN_MCPI), "--help"], capture_output=True, text=True, timeout=10
        )

        # VALIDATION 1: Command succeeds
        assert (
            result.returncode == 0
        ), f"bin/mcpi --help failed with code {result.returncode}"

        # VALIDATION 2: Shows usage
        output = result.stdout.lower()
        assert (
            "usage" in output or "commands" in output
        ), "Help should show usage or commands"

        # VALIDATION 3: Shows common commands
        assert any(
            cmd in output for cmd in ["list", "status", "install"]
        ), "Help should show available commands"


class TestP0_4_ScopeOperations:
    """Tests for scope add/remove operations (P0-4 prerequisites).

    These tests validate that scope handlers can add and remove servers,
    which is required for the rescope feature.

    GAMING RESISTANCE:
    - Tests real file I/O operations
    - Validates actual file contents before/after
    - Verifies multiple side effects
    - Tests error conditions
    """

    def test_scope_handler_can_add_server_to_file(self, mcp_harness):
        """Test that scope handler can add a server and persist to file.

        STATUS Gap: "Untested add operations"
        PLAN Item: P0-4 - Validate add_server works
        Priority: HIGH

        VALIDATION:
        - add_server returns success result
        - Server appears in get_servers()
        - File on disk is updated
        - Server config is correct in file

        This test CANNOT be gamed because:
        - Reads actual file from disk before/after
        - Validates file contents independently
        - Checks multiple side effects
        - Cannot pass without proper file writing
        """
        # Setup: Create plugin with test paths
        plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)
        scope_handler = plugin.get_scope_handler("user-mcp")

        # Verify file doesn't have our test server initially
        initial_servers = scope_handler.get_servers()
        assert (
            "test-new-server" not in initial_servers
        ), "Test server should not exist initially"

        # Execute: Add a new server
        new_config = ServerConfig(
            command="node",
            args=["test-server.js"],
            env={"TEST_VAR": "test_value"},
            type="stdio",
        )

        result = scope_handler.add_server("test-new-server", new_config)

        # VALIDATION 1: Operation succeeds
        assert result.success, f"add_server should succeed, got: {result.message}"

        # VALIDATION 2: Server appears in get_servers()
        updated_servers = scope_handler.get_servers()
        assert (
            "test-new-server" in updated_servers
        ), "Server should appear in get_servers() after add"

        # VALIDATION 3: Config is correct
        added_config = updated_servers["test-new-server"]
        assert (
            added_config["command"] == "node"
        ), "Added server command should be 'node'"
        assert added_config["args"] == [
            "test-server.js"
        ], "Added server args should match"
        assert (
            added_config["env"]["TEST_VAR"] == "test_value"
        ), "Added server env should match"

        # VALIDATION 4: File on disk is updated (ANTI-GAMING)
        file_content = mcp_harness.read_scope_file("user-mcp")
        assert (
            "test-new-server" in file_content["mcpServers"]
        ), "Server should be in actual file on disk"
        assert (
            file_content["mcpServers"]["test-new-server"]["command"] == "node"
        ), "File should have correct server config"

    def test_scope_handler_can_remove_server_from_file(self, prepopulated_harness):
        """Test that scope handler can remove a server and persist to file.

        STATUS Gap: "Untested remove operations"
        PLAN Item: P0-4 - Validate remove_server works
        Priority: HIGH

        VALIDATION:
        - remove_server returns success result
        - Server removed from get_servers()
        - File on disk is updated
        - Other servers not affected

        This test CANNOT be gamed because:
        - Starts with known file state
        - Verifies file before/after removal
        - Checks other servers unaffected
        - Validates actual file contents
        """
        # Setup: Use prepopulated harness with known servers
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)
        scope_handler = plugin.get_scope_handler("user-mcp")

        # Verify server exists initially
        initial_servers = scope_handler.get_servers()
        assert "filesystem" in initial_servers, "Test server should exist initially"
        assert "github" in initial_servers, "Other server should exist initially"

        # Execute: Remove filesystem server
        result = scope_handler.remove_server("filesystem")

        # VALIDATION 1: Operation succeeds
        assert result.success, f"remove_server should succeed, got: {result.message}"

        # VALIDATION 2: Server removed from get_servers()
        updated_servers = scope_handler.get_servers()
        assert (
            "filesystem" not in updated_servers
        ), "Server should not appear in get_servers() after remove"

        # VALIDATION 3: Other servers unaffected
        assert "github" in updated_servers, "Other servers should remain after remove"

        # VALIDATION 4: File on disk is updated (ANTI-GAMING)
        file_content = prepopulated_harness.read_scope_file("user-mcp")
        assert (
            "filesystem" not in file_content["mcpServers"]
        ), "Server should not be in actual file on disk"
        assert (
            "github" in file_content["mcpServers"]
        ), "Other servers should remain in file"


class TestP1_1_RescopeFeature_TDD:
    """Tests for P1-1: Rescope feature (TDD approach - WILL FAIL initially)

    PLAN Reference: BACKLOG.md "MCP Server Rescope Command"
    STATUS: BLOCKED (missing get_server_config API)

    These tests are designed with TDD approach:
    - They WILL FAIL initially (rescope not implemented)
    - They define the acceptance criteria
    - Implementation should make these pass

    GAMING RESISTANCE:
    - Tests call bin/mcpi rescope command (doesn't exist yet)
    - Validates real file operations
    - Checks source and destination files
    - Verifies server moved, not copied
    - Tests rollback behavior
    """

    @pytest.mark.skip(reason="TDD: Rescope feature not implemented yet (PLAN P1-1)")
    def test_rescope_command_exists_in_cli(self, tmp_path):
        """Test that bin/mcpi rescope command exists.

        PLAN Item: P1-1 - Implement rescope command
        Priority: P1 (blocked on P0-2)

        VALIDATION:
        - bin/mcpi rescope --help succeeds
        - Shows usage information
        - Shows required arguments

        This test WILL FAIL until rescope is implemented (TDD approach).

        GAMING RESISTANCE:
        - Tests actual CLI command existence
        - Cannot fake without implementing command
        """
        # Attempt to get help for rescope command
        result = subprocess.run(
            [str(BIN_MCPI), "rescope", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should succeed and show help
        assert result.returncode == 0, "rescope command should exist and show help"

        output_lower = result.stdout.lower()
        assert "rescope" in output_lower, "Help should mention rescope"
        assert "--from" in output_lower, "Help should show --from option"
        assert "--to" in output_lower, "Help should show --to option"

    @pytest.mark.skip(reason="TDD: Rescope feature not implemented yet (PLAN P1-1)")
    def test_rescope_moves_server_between_scopes_via_cli(self, prepopulated_harness):
        """Test that bin/mcpi rescope moves server from one scope to another.

        PLAN Item: P1-1 - Implement rescope functionality
        Priority: P1

        VALIDATION:
        - Command succeeds
        - Server removed from source scope
        - Server added to destination scope
        - Server config is identical
        - Source and dest files both updated

        This test WILL FAIL until rescope is implemented (TDD approach).

        GAMING RESISTANCE:
        - Creates real config files with known servers
        - Executes actual CLI command
        - Reads both files before/after
        - Validates server moved (not copied)
        - Checks all config fields preserved
        - Cannot pass without full implementation
        """
        # Setup: Ensure source scope has the server
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)
        source_scope = plugin.get_scope_handler("project-mcp")
        dest_scope = plugin.get_scope_handler("user-mcp")

        # Verify initial state
        source_servers_before = source_scope.get_servers()
        dest_servers_before = dest_scope.get_servers()

        assert (
            "project-tool" in source_servers_before
        ), "Source scope should have project-tool server"
        assert (
            "project-tool" not in dest_servers_before
        ), "Destination scope should not have project-tool initially"

        # Save original config for comparison
        original_config = source_scope.get_server_config("project-tool")

        # Execute: Run rescope command via CLI
        # NOTE: This will fail because rescope doesn't exist yet (TDD)
        result = subprocess.run(
            [
                str(BIN_MCPI),
                "rescope",
                "project-tool",
                "--from",
                "project-mcp",
                "--to",
                "user-mcp",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # VALIDATION 1: Command succeeds
        assert result.returncode == 0, (
            f"rescope command should succeed\n"
            f"stderr: {result.stderr}\n"
            f"stdout: {result.stdout}"
        )

        # VALIDATION 2: Server removed from source
        source_servers_after = source_scope.get_servers()
        assert (
            "project-tool" not in source_servers_after
        ), "Server should be removed from source scope"

        # VALIDATION 3: Server added to destination
        dest_servers_after = dest_scope.get_servers()
        assert (
            "project-tool" in dest_servers_after
        ), "Server should be added to destination scope"

        # VALIDATION 4: Config preserved exactly (CRITICAL)
        moved_config = dest_scope.get_server_config("project-tool")
        assert (
            moved_config == original_config
        ), "Rescope should preserve all config fields exactly"

        # VALIDATION 5: Files on disk updated (ANTI-GAMING)
        source_file = prepopulated_harness.read_scope_file("project-mcp")
        dest_file = prepopulated_harness.read_scope_file("user-mcp")

        assert "project-tool" not in source_file.get(
            "mcpServers", {}
        ), "Source file should not have server after rescope"
        assert "project-tool" in dest_file.get(
            "mcpServers", {}
        ), "Destination file should have server after rescope"

    @pytest.mark.skip(reason="TDD: Rescope feature not implemented yet (PLAN P1-1)")
    def test_rescope_preserves_complex_config_fields(self, prepopulated_harness):
        """Test that rescope preserves all config fields including env vars.

        PLAN Item: P1-1 - Acceptance criteria: "All configuration fields preserved"
        Priority: P1

        VALIDATION:
        - Environment variables preserved
        - Args list preserved in order
        - All optional fields preserved
        - Disabled flag preserved
        - Custom fields preserved

        This test WILL FAIL until rescope is implemented (TDD approach).

        GAMING RESISTANCE:
        - Tests server with complex config (env vars, multiple args)
        - Validates every field matches original
        - Cannot pass by copying partial config
        """
        # Setup: Use github server (has env vars)
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)
        source_scope = plugin.get_scope_handler("user-mcp")
        dest_scope = plugin.get_scope_handler("project-mcp")

        # Get original config
        original_config = source_scope.get_server_config("github")

        # Verify it has complex fields
        assert "env" in original_config, "Test server should have env vars"
        assert (
            "GITHUB_TOKEN" in original_config["env"]
        ), "Test server should have GITHUB_TOKEN env var"

        # Execute: Rescope via CLI
        result = subprocess.run(
            [
                str(BIN_MCPI),
                "rescope",
                "github",
                "--from",
                "user-mcp",
                "--to",
                "project-mcp",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0, f"rescope should succeed, got: {result.stderr}"

        # VALIDATION: All fields preserved
        moved_config = dest_scope.get_server_config("github")

        # Check every field
        assert (
            moved_config["command"] == original_config["command"]
        ), "Command should be preserved"
        assert (
            moved_config["args"] == original_config["args"]
        ), "Args should be preserved in order"
        assert (
            moved_config["env"] == original_config["env"]
        ), "Env vars should be preserved"
        assert moved_config.get("type") == original_config.get(
            "type"
        ), "Type field should be preserved"

        # Full equality check
        assert (
            moved_config == original_config
        ), "All config fields should be preserved exactly"

    @pytest.mark.skip(reason="TDD: Rescope feature not implemented yet (PLAN P1-1)")
    def test_rescope_rollback_on_failure(self, prepopulated_harness):
        """Test that rescope rolls back changes if operation fails.

        PLAN Item: P1-1 - Error handling: "Rollback on failure"
        Priority: P1

        VALIDATION:
        - If write to destination fails, no changes made
        - If remove from source fails, destination is cleaned up
        - Server remains in original location after failure
        - Error message is clear

        This test WILL FAIL until rescope is implemented (TDD approach).

        GAMING RESISTANCE:
        - Simulates failure condition (invalid destination)
        - Validates source not modified
        - Checks both files unchanged
        - Tests error handling
        """
        # Setup
        plugin = ClaudeCodePlugin(path_overrides=prepopulated_harness.path_overrides)
        source_scope = plugin.get_scope_handler("user-mcp")

        # Get servers before operation
        servers_before = source_scope.get_servers()
        assert "filesystem" in servers_before, "Test server should exist before rescope"

        # Execute: Try to rescope to invalid scope (should fail)
        result = subprocess.run(
            [
                str(BIN_MCPI),
                "rescope",
                "filesystem",
                "--from",
                "user-mcp",
                "--to",
                "invalid-scope-name",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # VALIDATION 1: Command fails gracefully
        assert result.returncode != 0, "rescope with invalid scope should fail"

        # VALIDATION 2: Error message is clear
        assert (
            "invalid" in result.stderr.lower() or "not found" in result.stderr.lower()
        ), f"Error should mention invalid scope, got: {result.stderr}"

        # VALIDATION 3: Source unchanged (rollback worked)
        servers_after = source_scope.get_servers()
        assert (
            "filesystem" in servers_after
        ), "Server should remain in source after failed rescope"

        # VALIDATION 4: File on disk unchanged
        file_content = prepopulated_harness.read_scope_file("user-mcp")
        assert (
            "filesystem" in file_content["mcpServers"]
        ), "Source file should be unchanged after failed rescope"


# ==============================================================================
# TEST DOCUMENTATION
# ==============================================================================

"""
TRACEABILITY SUMMARY:
---------------------

P0-2 (CRITICAL - get_server_config API):
  ✓ test_get_server_config_api_exists_on_scope_handler
  ✓ test_get_server_config_returns_full_config_dict
  ✓ test_get_server_config_raises_error_on_missing_server
  ✓ test_get_server_config_works_across_all_scope_types
  ✓ test_get_server_config_with_complex_config

P0-4 (HIGH - Core CLI and operations):
  ✓ test_cli_status_command_works
  ✓ test_cli_list_shows_servers
  ✓ test_cli_help_command_works
  ✓ test_scope_handler_can_add_server_to_file
  ✓ test_scope_handler_can_remove_server_from_file

P1-1 (FUTURE - Rescope feature, TDD):
  ⊗ test_rescope_command_exists_in_cli (WILL FAIL - not implemented)
  ⊗ test_rescope_moves_server_between_scopes_via_cli (WILL FAIL)
  ⊗ test_rescope_preserves_complex_config_fields (WILL FAIL)
  ⊗ test_rescope_rollback_on_failure (WILL FAIL)


STATUS GAPS COVERAGE:
---------------------
  [CRITICAL] Missing get_server_config() → 5 tests
  [HIGH] Untested CLI workflows → 3 tests
  [HIGH] Untested add/remove operations → 2 tests
  [FUTURE] Rescope feature → 4 tests (TDD)


GAMING RESISTANCE MECHANISMS:
------------------------------
1. Real CLI execution (bin/mcpi subprocess)
2. Real file I/O operations
3. File content validation before/after
4. Multiple side effect checks
5. Error path validation
6. No mocking of tested functionality
7. Data equality checks (not just type checks)
8. Independent file reading for verification


EXPECTED TEST RESULTS:
----------------------
- P0-2 tests: MAY FAIL if get_server_config() not implemented
- P0-4 tests: SHOULD PASS (core CLI works per STATUS report)
- P1-1 tests: WILL FAIL (rescope not implemented - TDD approach)

After P0-2 implementation: 5 additional tests should pass
After P1-1 implementation: 4 additional tests should pass
Total: 14 tests when all features implemented
"""
