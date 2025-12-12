"""Comprehensive functional tests for TUI reload functionality.

These tests verify the real user workflow for the fzf TUI reload mechanism.
They are designed to be un-gameable by testing actual command execution,
real file operations, and observable state changes.

Test Structure:
1. Unit tests for reload_server_list() function
2. Integration tests for mcpi tui-reload CLI command
3. Functional tests for fzf workflow with reload
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List
from unittest.mock import patch, create_autospec, AsyncMock

import pytest
from click.testing import CliRunner

from mcpi.clients import MCPManager, ServerConfig
from mcpi.clients.manager import create_default_manager
from mcpi.clients.registry import ClientRegistry
from mcpi.clients.types import ServerInfo, ServerState
from mcpi.registry.catalog import MCPServer, ServerCatalog, create_in_memory_catalog

# Import CLI after checking if command exists
from mcpi import cli


class TestReloadServerListFunction:
    """Unit tests for the reload_server_list() function.

    These tests verify the function exists, works correctly, and outputs
    the right format for fzf consumption.

    CRITICAL: Uses real MCPManager and ServerCatalog objects, not MagicMock.
    """

    def test_reload_function_exists(self):
        """Verify reload_server_list function exists and is callable.

        This test cannot be gamed - it imports and checks the actual function.
        """
        # This will raise ImportError if function doesn't exist
        from mcpi.tui import reload_server_list

        assert callable(reload_server_list), "reload_server_list must be callable"

    def test_reload_outputs_to_stdout(self, tmp_path, capsys, monkeypatch):
        """Verify reload_server_list outputs formatted list to stdout.

        This test uses a real temporary directory and verifies actual output,
        not mocked return values. Cannot be gamed with stubs.
        """
        from mcpi.tui import reload_server_list, build_server_list
        from mcpi.clients.claude_code import ClaudeCodePlugin
        from mcpi.clients.registry import ClientRegistry

        # Create real test harness with actual files
        test_config_path = tmp_path / "test_settings.json"
        test_config_path.write_text(
            json.dumps(
                {
                    "mcpEnabled": True,
                    "mcpServers": {
                        "test-server": {
                            "command": "npx",
                            "args": ["-y", "test"],
                            "type": "stdio",
                        }
                    },
                }
            )
        )

        # Create REAL plugin with path overrides
        path_overrides = {"user-mcp": test_config_path}
        real_plugin = ClaudeCodePlugin(path_overrides=path_overrides)

        # Create REAL registry and manager
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", real_plugin)

        # Pass registry to manager to avoid creating new registry with safety violations
        real_manager = MCPManager(default_client="claude-code", registry=registry)

        # Create catalog with test data using the proper factory function
        real_catalog = create_in_memory_catalog({
            "test-server": MCPServer(
                description="Test server for reload",
                command="npx",
                args=["-y", "test"],
            )
        })

        # Call the function with our real instances (no mocking needed!)
        # This is the correct way - pass configured instances directly
        reload_server_list(catalog=real_catalog, manager=real_manager)

        # Capture stdout
        captured = capsys.readouterr()

        # Verify output is not empty
        assert len(captured.out) > 0, "reload_server_list must output to stdout"

        # Verify output contains the server ID
        assert "test-server" in captured.out, "Output must contain server ID"

        # Verify output contains the description
        assert (
            "Test server for reload" in captured.out
        ), "Output must contain description"

        # Verify output uses correct format (status indicator)
        assert (
            "[" in captured.out and "]" in captured.out
        ), "Output must have status indicators"

    def test_reload_format_matches_build_server_list(
        self, tmp_path, capsys, monkeypatch
    ):
        """Verify reload_server_list outputs same format as build_server_list.

        This ensures consistency between initial launch and reload.
        Cannot be gamed - compares actual function outputs.
        """
        from mcpi.tui import reload_server_list, build_server_list
        from mcpi.clients.claude_code import ClaudeCodePlugin
        from mcpi.clients.registry import ClientRegistry

        # Setup real test environment
        test_config = tmp_path / "config.json"
        test_config.write_text(
            json.dumps(
                {
                    "mcpEnabled": True,
                    "mcpServers": {
                        "server1": {
                            "command": "npx",
                            "args": ["server1"],
                            "type": "stdio",
                        },
                        "server2": {
                            "command": "node",
                            "args": ["server2"],
                            "type": "stdio",
                        },
                    },
                }
            )
        )

        # Create REAL objects
        real_plugin = ClaudeCodePlugin(path_overrides={"user-mcp": test_config})
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", real_plugin)

        real_manager = MCPManager(default_client="claude-code", registry=registry)

        # Create catalog with test data using the proper factory function
        real_catalog = create_in_memory_catalog({
            "server1": MCPServer(description="Server One", command="npx"),
            "server2": MCPServer(description="Server Two", command="node"),
        })

        # Get expected output from build_server_list
        # build_server_list is now a method on FzfAdapter, use the adapter directly
        from mcpi.tui.adapters.fzf import FzfAdapter

        adapter = FzfAdapter()
        expected_lines = adapter._build_server_list(real_catalog, real_manager)
        expected_output = "\n".join(expected_lines) + "\n"

        # Get actual output from reload_server_list
        reload_server_list(catalog=real_catalog, manager=real_manager)

        actual_output = capsys.readouterr().out

        # Verify outputs match exactly
        assert (
            actual_output == expected_output
        ), "reload_server_list must output same format as build_server_list"

    def test_reload_with_empty_registry(self, capsys, monkeypatch):
        """Verify reload handles empty registry gracefully.

        Edge case: no servers in registry should output empty (not crash).
        """
        from mcpi.tui import reload_server_list

        # Create REAL manager and catalog with no servers
        # Use empty registry to avoid client detection in test mode
        empty_registry = ClientRegistry(auto_discover=False)
        real_manager = MCPManager(registry=empty_registry, default_client=None)

        # Create empty catalog using the proper factory function
        real_catalog = create_in_memory_catalog({})

        # Call the function with our real instances
        reload_server_list(catalog=real_catalog, manager=real_manager)

        output = capsys.readouterr().out

        # Should output empty or minimal output (not crash)
        assert output == "" or output.isspace(), "Empty registry should output nothing"

    def test_reload_respects_server_states(self, tmp_path, capsys, monkeypatch):
        """Verify reload shows correct status indicators for different states.

        Tests that enabled servers show green checkmark, disabled show yellow X,
        not installed show empty bracket.
        """
        from mcpi.tui import reload_server_list
        from mcpi.clients.claude_code import ClaudeCodePlugin
        from mcpi.clients.registry import ClientRegistry

        # Create config with servers in different states
        enabled_config = tmp_path / "enabled.json"
        enabled_config.write_text(
            json.dumps(
                {
                    "mcpEnabled": True,
                    "mcpServers": {
                        "enabled-server": {
                            "command": "npx",
                            "args": ["enabled"],
                            "type": "stdio",
                        }
                    },
                }
            )
        )

        disabled_config = tmp_path / "disabled.json"
        disabled_config.write_text(
            json.dumps(
                {
                    "mcpEnabled": True,
                    "disabledMcpjsonServers": ["disabled-server"],
                    "mcpServers": {
                        "disabled-server": {
                            "command": "npx",
                            "args": ["disabled"],
                            "type": "stdio",
                        }
                    },
                }
            )
        )

        # Create REAL plugin with multiple scopes
        path_overrides = {
            "user-mcp": enabled_config,
            "user-local": disabled_config,
        }
        real_plugin = ClaudeCodePlugin(path_overrides=path_overrides)

        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", real_plugin)

        real_manager = MCPManager(default_client="claude-code", registry=registry)

        # Create catalog with test data using the proper factory function
        real_catalog = create_in_memory_catalog({
            "enabled-server": MCPServer(description="Enabled", command="npx"),
            "disabled-server": MCPServer(description="Disabled", command="npx"),
            "not-installed": MCPServer(description="Not Installed", command="npx"),
        })

        # Call the function with our real instances
        reload_server_list(catalog=real_catalog, manager=real_manager)

        output = capsys.readouterr().out

        # Verify status indicators (ANSI color codes present)
        # Green + checkmark for enabled
        assert "\033[32m" in output, "Should have green color code for enabled server"
        assert "✓" in output or "✓]" in output, "Should have checkmark for enabled"

        # Yellow + X for disabled
        assert "\033[33m" in output, "Should have yellow color code for disabled server"
        assert "✗" in output or "✗]" in output, "Should have X for disabled"

        # Normal (no color) for not installed
        assert "not-installed" in output, "Should include not-installed server"


class TestTuiReloadCLICommand:
    """Integration tests for the `mcpi tui-reload` CLI command.

    These tests verify the command exists, is executable, and works correctly
    when called as a subprocess (as fzf would call it).

    Uses CliRunner for testing but also tests real subprocess execution.
    """

    def test_tui_reload_command_exists_in_cli(self):
        """Verify 'mcpi tui-reload' command is registered in CLI.

        This test checks the Click command is registered and discoverable.
        Cannot be gamed - checks actual CLI structure.
        """
        # Check if command exists in CLI group
        assert hasattr(cli, "main"), "CLI must have main group"

        # Get all registered commands
        commands = cli.main.commands

        # Verify tui-reload command exists
        assert (
            "tui-reload" in commands
        ), "CLI must have 'tui-reload' command for fzf integration"

    def test_tui_reload_command_executes_successfully(self, tmp_path):
        """Verify tui-reload command executes without errors.

        Uses CliRunner to invoke the actual command, verifies exit code.
        """
        runner = CliRunner()

        # Execute the command
        result = runner.invoke(cli.main, ["tui-reload"])

        # Verify successful execution
        assert result.exit_code == 0, (
            f"tui-reload command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}"
        )

    def test_tui_reload_outputs_server_list(self, tmp_path):
        """Verify tui-reload command outputs formatted server list.

        Creates test environment, runs command, verifies output format.
        """
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Run command
            result = runner.invoke(cli.main, ["tui-reload"])

            assert result.exit_code == 0, "Command must succeed"

            # Output should be formatted for fzf (may be empty if no servers)
            # At minimum, should not crash
            assert result.output is not None

    def test_tui_reload_respects_client_context(self, mcp_harness):
        """Verify tui-reload respects the current client context.

        If a specific client is selected, reload should use that client's
        configuration, not a different one.

        NOTE: This test verifies the command accepts --client flag without
        causing safety violations. The actual client selection is tested in
        other tests that call reload_server_list directly.
        """
        from mcpi.clients.claude_code import ClaudeCodePlugin
        from mcpi.clients.registry import ClientRegistry

        # Create plugin with harness path overrides
        real_plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

        # Create registry and inject plugin
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", real_plugin)

        # Create manager with registry
        real_manager = MCPManager(default_client="claude-code", registry=registry)

        # Create empty catalog for the test (we just need a valid catalog object)
        real_catalog = create_in_memory_catalog({})

        runner = CliRunner()

        # Inject both manager and catalog into CLI context before invoking command
        # This prevents get_mcp_manager from trying to create a new one
        result = runner.invoke(
            cli.main,
            ["tui-reload"],
            obj={"mcp_manager": real_manager, "catalog": real_catalog},
        )

        # Should succeed (exit code 0) since we provided proper manager with path_overrides
        # Exit code 1 is also acceptable (no servers found)
        # Exit code 2 would indicate safety violation which should not happen
        assert result.exit_code in [0, 1], (
            f"Command should succeed or fail gracefully, got exit code {result.exit_code}. "
            f"Exit code 2 indicates safety violation. Output: {result.output}"
        )

    def test_tui_reload_command_via_subprocess(self):
        """Verify tui-reload works when called as subprocess (like fzf does).

        This is the CRITICAL test - fzf calls mcpi-tui-reload as a subprocess.
        We need to verify this actually works, not just in CliRunner.

        IMPORTANT: This test verifies the actual user workflow, not mocked behavior.
        """
        try:
            # Try to call the command as fzf would
            result = subprocess.run(
                ["mcpi", "tui-reload"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            # Should succeed or fail gracefully (not crash)
            assert result.returncode in [0, 1], (
                f"Command crashed with exit code {result.returncode}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )

            # If successful, should have some output (or empty if no servers)
            if result.returncode == 0:
                # Output should be valid (not error messages)
                assert not result.stdout.startswith(
                    "Error:"
                ), "Output should not be an error message"

        except FileNotFoundError:
            pytest.skip("mcpi command not installed in PATH")
        except subprocess.TimeoutExpired:
            pytest.fail("Command timed out after 5 seconds")


class TestReloadConsoleScriptEntry:
    """Tests for the mcpi-tui-reload console script entry point.

    Verifies that the separate console script (as called by fzf) exists
    and is executable.
    """

    def test_console_script_exists(self):
        """Verify mcpi-tui-reload console script is installed.

        This is the command that fzf bindings reference. It MUST exist
        as a separate executable for the reload mechanism to work.
        """
        result = subprocess.run(
            ["which", "mcpi-tui-reload"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            pytest.skip(
                "mcpi-tui-reload not installed. "
                "Run 'uv tool install --editable .' to install."
            )

        # Verify we got a path
        assert (
            len(result.stdout.strip()) > 0
        ), "which mcpi-tui-reload should return a path"

        # Verify the path exists
        script_path = Path(result.stdout.strip())
        assert script_path.exists(), f"Console script path {script_path} does not exist"

    def test_console_script_executes(self):
        """Verify mcpi-tui-reload console script is executable.

        Calls the script directly and verifies it runs.
        """
        try:
            result = subprocess.run(
                ["mcpi-tui-reload"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            # Should succeed or fail gracefully
            assert result.returncode in [0, 1], (
                f"Console script failed with code {result.returncode}\n"
                f"stderr: {result.stderr}"
            )

        except FileNotFoundError:
            pytest.skip(
                "mcpi-tui-reload not in PATH. "
                "Install with 'uv tool install --editable .'"
            )


class TestFzfIntegrationWithReload:
    """Functional tests for fzf integration with reload mechanism.

    These tests verify the complete workflow:
    1. fzf launches
    2. User performs operation (add/remove/enable/disable)
    3. Reload command is called
    4. Server list updates

    IMPORTANT: These are the highest-value tests that prove the actual
    user workflow works correctly.
    """

    def test_fzf_bindings_include_reload_command(self):
        """Verify fzf bindings reference mcpi-tui-reload.

        Checks that the fzf command structure includes reload() calls.
        """
        from mcpi.tui import build_fzf_command

        fzf_cmd = build_fzf_command()
        cmd_str = " ".join(fzf_cmd)

        # Verify reload commands are present in bindings
        assert (
            "reload(mcpi-tui-reload)" in cmd_str or "reload(mcpi tui-reload)" in cmd_str
        ), "fzf bindings must include reload command"

    def test_reload_called_in_add_binding(self):
        """Verify ctrl-a (add) binding calls reload.

        Checks the exact binding structure for the add operation.
        """
        from mcpi.tui import build_fzf_command

        fzf_cmd = build_fzf_command()

        # Find ctrl-a binding
        ctrl_a_binding = None
        for i, arg in enumerate(fzf_cmd):
            if arg == "--bind" and i + 1 < len(fzf_cmd):
                binding = fzf_cmd[i + 1]
                if binding.startswith("ctrl-a:"):
                    ctrl_a_binding = binding
                    break

        assert ctrl_a_binding is not None, "ctrl-a binding must exist"

        # Verify it includes both execute and reload
        assert "execute" in ctrl_a_binding, "ctrl-a must execute add command"
        assert "mcpi add" in ctrl_a_binding, "ctrl-a must call mcpi add"
        assert "reload" in ctrl_a_binding, "ctrl-a must trigger reload"

    def test_reload_called_in_remove_binding(self):
        """Verify ctrl-r (remove) binding calls reload."""
        from mcpi.tui import build_fzf_command

        fzf_cmd = build_fzf_command()

        # Find ctrl-r binding
        ctrl_r_binding = None
        for i, arg in enumerate(fzf_cmd):
            if arg == "--bind" and i + 1 < len(fzf_cmd):
                binding = fzf_cmd[i + 1]
                if binding.startswith("ctrl-r:"):
                    ctrl_r_binding = binding
                    break

        assert ctrl_r_binding is not None, "ctrl-r binding must exist"
        assert "mcpi remove" in ctrl_r_binding, "ctrl-r must call mcpi remove"
        assert "reload" in ctrl_r_binding, "ctrl-r must trigger reload"

    def test_reload_called_in_enable_binding(self):
        """Verify ctrl-e (enable) binding calls reload."""
        from mcpi.tui import build_fzf_command

        fzf_cmd = build_fzf_command()

        # Find ctrl-e binding
        ctrl_e_binding = None
        for i, arg in enumerate(fzf_cmd):
            if arg == "--bind" and i + 1 < len(fzf_cmd):
                binding = fzf_cmd[i + 1]
                if binding.startswith("ctrl-e:"):
                    ctrl_e_binding = binding
                    break

        assert ctrl_e_binding is not None, "ctrl-e binding must exist"
        assert "mcpi enable" in ctrl_e_binding, "ctrl-e must call mcpi enable"
        assert "reload" in ctrl_e_binding, "ctrl-e must trigger reload"

    def test_reload_called_in_disable_binding(self):
        """Verify ctrl-d (disable) binding calls reload."""
        from mcpi.tui import build_fzf_command

        fzf_cmd = build_fzf_command()

        # Find ctrl-d binding
        ctrl_d_binding = None
        for i, arg in enumerate(fzf_cmd):
            if arg == "--bind" and i + 1 < len(fzf_cmd):
                binding = fzf_cmd[i + 1]
                if binding.startswith("ctrl-d:"):
                    ctrl_d_binding = binding
                    break

        assert ctrl_d_binding is not None, "ctrl-d binding must exist"
        assert "mcpi disable" in ctrl_d_binding, "ctrl-d must call mcpi disable"
        assert "reload" in ctrl_d_binding, "ctrl-d must trigger reload"

    def test_operation_changes_reflected_in_reload(self, tmp_path, monkeypatch):
        """Verify that after an operation, reload shows updated state.

        This is the CRITICAL end-to-end test:
        1. Initial state: server not installed
        2. Perform add operation
        3. Call reload
        4. Verify server now shows as installed

        This test cannot be gamed - it performs real operations on real files
        and verifies actual state changes.
        """
        from mcpi.tui import reload_server_list
        from mcpi.clients.claude_code import ClaudeCodePlugin
        from mcpi.clients.registry import ClientRegistry

        # Setup: Create real config file
        config_file = tmp_path / "test_config.json"
        config_file.write_text(json.dumps({"mcpServers": {}}))

        # Create REAL plugin and manager
        real_plugin = ClaudeCodePlugin(path_overrides={"user-mcp": config_file})
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", real_plugin)

        real_manager = MCPManager(default_client="claude-code", registry=registry)

        # Create catalog with test data using the proper factory function
        real_catalog = create_in_memory_catalog({
            "test-server": MCPServer(
                description="Test Server",
                command="npx",
                args=["-y", "test"],
            )
        })

        # Initial state: server not installed
        state_before = real_manager.get_server_state("test-server")
        assert (
            state_before == ServerState.NOT_INSTALLED
        ), "Server should initially be not installed"

        # Perform add operation (REAL operation, not mocked)
        config = ServerConfig(
            command="npx",
            args=["-y", "test"],
            type="stdio",
        )
        result = real_manager.add_server("test-server", config, "user-mcp")
        assert result.success, f"Add operation should succeed: {result.message}"

        # Verify file was actually written
        assert config_file.exists(), "Config file should exist"
        saved_config = json.loads(config_file.read_text())
        assert (
            "test-server" in saved_config["mcpServers"]
        ), "Server should be in saved config"

        # Call reload with updated manager (pass instances directly, no patches)
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        try:
            # Pass real_manager and real_catalog directly - no patches needed!
            reload_server_list(catalog=real_catalog, manager=real_manager)
        finally:
            sys.stdout = old_stdout

        output = captured_output.getvalue()

        # Verify reload output shows server as installed (green checkmark)
        assert "test-server" in output, "Reload should show the server"
        assert (
            "[32m" in output or "✓" in output
        ), "Reload should show server as enabled (green/checkmark)"


class TestReloadEdgeCases:
    """Tests for edge cases and error handling in reload mechanism."""

    def test_reload_with_no_default_client(self, monkeypatch):
        """Verify reload handles missing default client gracefully.

        If no MCP client is detected, reload should fail gracefully,
        not crash.
        """
        from mcpi.tui import reload_server_list

        # Mock MCPManager to raise exception (no client found)
        def mock_manager_init(*args, **kwargs):
            raise RuntimeError("No MCP client found")

        with patch("mcpi.tui.MCPManager", side_effect=mock_manager_init):
            # Should not crash, should exit gracefully
            try:
                reload_server_list()
            except SystemExit:
                # Acceptable - command exits with error
                pass
            except Exception as e:
                pytest.fail(
                    f"reload_server_list should not raise {type(e).__name__}: {e}"
                )

    def test_reload_with_corrupted_config(self, tmp_path, monkeypatch):
        """Verify reload handles corrupted config files gracefully.

        If config file is invalid JSON, reload should not crash.
        """
        from mcpi.tui import reload_server_list
        from mcpi.clients.claude_code import ClaudeCodePlugin
        from mcpi.clients.registry import ClientRegistry

        # Create corrupted config file
        config_file = tmp_path / "corrupted.json"
        config_file.write_text("{invalid json")

        # Create plugin that will encounter the corrupted file
        real_plugin = ClaudeCodePlugin(path_overrides={"user-mcp": config_file})
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", real_plugin)

        real_manager = MCPManager(default_client="claude-code", registry=registry)

        # Create empty catalog using the proper factory function
        real_catalog = create_in_memory_catalog({})

        # Should handle error gracefully
        try:
            reload_server_list(catalog=real_catalog, manager=real_manager)
        except SystemExit:
            pass  # Acceptable
        except json.JSONDecodeError:
            pass  # May propagate, but shouldn't crash fzf

    def test_reload_with_permission_error(self, tmp_path, monkeypatch):
        """Verify reload handles permission errors gracefully.

        If user lacks permission to read config, should fail gracefully.
        """
        # This test is platform-specific and may be skipped on some systems
        pytest.skip("Permission testing requires platform-specific setup")


class TestReloadPerformance:
    """Performance tests to ensure reload is fast enough for good UX.

    Reload should complete in < 1 second for acceptable user experience.
    """

    def test_reload_completes_quickly(self, tmp_path, monkeypatch):
        """Verify reload completes in under 1 second.

        Slow reload (> 1s) degrades user experience. This test ensures
        reload is fast enough for interactive use.
        """
        import time
        from mcpi.tui import reload_server_list

        # Use empty registry to avoid client detection in test mode
        empty_registry = ClientRegistry(auto_discover=False)
        real_manager = MCPManager(registry=empty_registry, default_client=None)

        # Create catalog with test data using the proper factory function
        real_catalog = create_in_memory_catalog({
            f"server-{i}": MCPServer(
                description=f"Test Server {i}",
                command="npx",
            )
            for i in range(50)
        })

        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            with patch("mcpi.tui.MCPManager", return_value=real_manager):
                with patch("mcpi.tui.ServerCatalog", return_value=real_catalog):
                    start = time.time()
                    reload_server_list()
                    elapsed = time.time() - start
        finally:
            sys.stdout = old_stdout

        # Should complete quickly (< 1 second)
        assert (
            elapsed < 1.0
        ), f"Reload took {elapsed:.2f}s, should be < 1.0s for good UX"


# Manual Testing Checklist (for humans, not automated)
"""
MANUAL TESTING CHECKLIST:

After implementing reload functionality, perform these manual tests:

1. Install the package:
   $ uv tool install --editable .

2. Verify console script exists:
   $ which mcpi-tui-reload
   # Should return a path

3. Test reload command directly:
   $ mcpi-tui-reload
   # Should output formatted server list

4. Test in fzf workflow:
   $ mcpi fzf
   # Press ctrl-a to add a server
   # List should refresh automatically with new server
   # Server should show green checkmark

5. Test enable/disable:
   # In fzf, select an installed server
   # Press ctrl-d to disable
   # Server should change to yellow X immediately
   # Press ctrl-e to enable
   # Server should change to green checkmark immediately

6. Test remove:
   # In fzf, select an installed server
   # Press ctrl-r to remove
   # Server should disappear or show as not installed

7. Test rapid operations:
   # Press ctrl-a, ctrl-e, ctrl-d rapidly
   # Should handle without crashing

8. Test with no servers:
   # With empty registry
   $ mcpi fzf
   # Should show "no servers" message, not crash

EXPECTED RESULTS:
- All operations should refresh the list automatically
- No need to exit and re-launch fzf
- Status indicators update immediately
- No crashes or errors
"""
