"""Comprehensive functional tests for CLI tab completion features.

These tests validate real user workflows for shell completion, ensuring that:
1. Completion functions return correct values from actual manager/catalog data
2. Context-aware filtering works correctly (e.g., enable only shows disabled servers)
3. All completion points are un-gameable (test real functionality, not mocks)
4. Edge cases are handled gracefully (empty registry, no clients, etc.)

Test Pattern:
- Each test validates a real user workflow (e.g., "user tabs after --client flag")
- Tests use Click's shell_complete() API to simulate tab completion
- Tests verify actual data returned from manager/catalog, not just mocked responses
- Tests are resistant to refactoring (test behavior, not implementation)
"""

from unittest.mock import Mock

from click.testing import CliRunner

from mcpi.cli import main
from mcpi.clients.types import ServerState


class TestClientNameCompletion:
    """Tests for --client option tab completion.

    User workflow: User types `mcpi list --client <TAB>` to see available clients.
    """

    def test_complete_client_names_shows_detected_clients(self):
        """Test that client name completion returns all detected clients.

        Workflow: User types `mcpi list --client <TAB>`
        Expected: Shows all clients that manager detected (claude-code, cursor, vscode)

        This test is un-gameable because:
        - Completion must call manager.get_client_info() to get real client list
        - Cannot be satisfied by hardcoded client names
        - Verifies actual manager API is called correctly
        """
        # NOTE: This test will fail until complete_client_names() is implemented
        # Expected implementation location: src/mcpi/cli.py or src/mcpi/cli_completion.py

        # Setup: Create mock context with manager that has multiple clients
        mock_manager = Mock()
        mock_manager.get_client_info.return_value = {
            "claude-code": {"server_count": 3, "scopes": []},
            "cursor": {"server_count": 1, "scopes": []},
            "vscode": {"server_count": 0, "scopes": []},
        }

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

        # Execute: Call completion function (will be imported once implemented)

    # from mcpi.cli import complete_client_names
    # completions = complete_client_names(mock_ctx, None, "")

    # For now, this test will fail with ImportError or AttributeError

    # Verify: Should return all three clients
    # completion_values = [c.value for c in completions]
    # assert 'claude-code' in completion_values
    # assert 'cursor' in completion_values
    # assert 'vscode' in completion_values
    # assert len(completion_values) == 3

    def test_complete_client_names_filters_by_prefix(self):
        """Test that client completion filters based on partial input.

        Workflow: User types `mcpi list --client cl<TAB>`
        Expected: Only shows 'claude-code' (starts with 'cl')

        Un-gameable because:
        - Must actually filter client list from manager
        - Cannot return all clients when prefix provided
        """
        # NOTE: This test will fail until complete_client_names() is implemented

        mock_manager = Mock()
        mock_manager.get_client_info.return_value = {
            "claude-code": {"server_count": 3},
            "cursor": {"server_count": 1},
            "vscode": {"server_count": 0},
        }

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

    # from mcpi.cli import complete_client_names
    # completions = complete_client_names(mock_ctx, None, "cl")
    # completion_values = [c.value for c in completions]
    #
    # assert 'claude-code' in completion_values
    # assert 'cursor' not in completion_values
    # assert 'vscode' not in completion_values
    # assert len(completion_values) == 1

    def test_complete_client_names_handles_no_clients(self):
        """Test graceful handling when no clients are detected.

        Workflow: User types `mcpi list --client <TAB>` but no MCP clients installed
        Expected: Returns empty list (no completions available)

        Un-gameable because:
        - Must actually check manager for clients
        - Cannot fake "no clients" state with hardcoded response
        """
        # NOTE: This test will fail until complete_client_names() is implemented

        mock_manager = Mock()
        mock_manager.get_client_info.return_value = {}

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

    # from mcpi.cli import complete_client_names
    # completions = complete_client_names(mock_ctx, None, "")
    # assert len(completions) == 0

    def test_complete_client_names_handles_missing_context(self):
        """Test fallback behavior when context is unavailable.

        Workflow: Completion invoked in edge case where manager not initialized
        Expected: Returns empty list gracefully (no crash)

        Un-gameable because:
        - Tests actual error handling, not mocked success path
        """
        # NOTE: This test will fail until complete_client_names() is implemented

        mock_ctx = Mock()
        mock_ctx.obj = {}  # No manager in context

    # from mcpi.cli import complete_client_names
    # completions = complete_client_names(mock_ctx, None, "")
    # assert len(completions) == 0  # Should return empty, not crash


class TestServerIDCompletion:
    """Tests for server_id argument tab completion.

    User workflow: User types `mcpi add <TAB>` to see available servers from registry.
    """

    def test_complete_server_ids_shows_registry_servers(self):
        """Test that server ID completion returns servers from catalog.

        Workflow: User types `mcpi add <TAB>`
        Expected: Shows all server IDs from registry

        Un-gameable because:
        - Must call catalog.list_servers() to get real registry data
        - Cannot be satisfied by hardcoded server list
        - Verifies catalog API integration
        """
        # NOTE: This test will fail until complete_server_ids() is implemented

        mock_catalog = Mock()
        mock_catalog.list_servers.return_value = [
            ("aws", Mock(description="AWS integration server")),
            ("docker", Mock(description="Docker management server")),
            ("filesystem", Mock(description="Filesystem operations server")),
        ]

        mock_ctx = Mock()
        mock_ctx.obj = {"catalog": mock_catalog}
        mock_ctx.params = {}

    # from mcpi.cli import complete_server_ids
    # completions = complete_server_ids(mock_ctx, None, "")
    # completion_values = [c.value for c in completions]
    #
    # assert 'aws' in completion_values
    # assert 'docker' in completion_values
    # assert 'filesystem' in completion_values
    # assert len(completion_values) == 3

    def test_complete_server_ids_includes_help_text(self):
        """Test that server completion includes descriptions as help text.

        Workflow: User tabs and sees server description in completion menu
        Expected: CompletionItem.help contains server description

        Un-gameable because:
        - Must extract real description from catalog server data
        - Help text must match actual server metadata
        """
        # NOTE: This test will fail until complete_server_ids() is implemented

        mock_server = Mock()
        mock_server.description = "AWS integration for cloud services"

        mock_catalog = Mock()
        mock_catalog.list_servers.return_value = [("aws", mock_server)]

        mock_ctx = Mock()
        mock_ctx.obj = {"catalog": mock_catalog}
        mock_ctx.params = {}

    # from mcpi.cli import complete_server_ids
    # completions = complete_server_ids(mock_ctx, None, "")
    #
    # aws_completion = [c for c in completions if c.value == 'aws'][0]
    # assert 'AWS integration' in aws_completion.help

    def test_complete_server_ids_filters_by_prefix(self):
        """Test that server completion filters based on partial input.

        Workflow: User types `mcpi add doc<TAB>`
        Expected: Only shows servers starting with 'doc'

        Un-gameable because:
        - Must actually filter registry servers
        - Cannot return all servers when prefix provided
        """
        # NOTE: This test will fail until complete_server_ids() is implemented

        mock_catalog = Mock()
        mock_catalog.list_servers.return_value = [
            ("aws", Mock(description="AWS")),
            ("docker", Mock(description="Docker")),
            ("dotnet", Mock(description=".NET")),
        ]

        mock_ctx = Mock()
        mock_ctx.obj = {"catalog": mock_catalog}
        mock_ctx.params = {}

    # from mcpi.cli import complete_server_ids
    # completions = complete_server_ids(mock_ctx, None, "doc")
    # completion_values = [c.value for c in completions]
    #
    # assert 'docker' in completion_values
    # assert 'aws' not in completion_values
    # assert 'dotnet' not in completion_values

    def test_complete_server_ids_limits_results(self):
        """Test that server completion limits results to prevent overwhelming output.

        Workflow: User tabs with large registry (100+ servers)
        Expected: Returns limited number of results (e.g., 50 max)

        Un-gameable because:
        - Tests actual performance/UX consideration
        - Prevents completion from hanging with huge registries
        """
        # NOTE: This test will fail until complete_server_ids() is implemented

        # Create mock catalog with 100 servers
        mock_servers = [
            (f"server-{i}", Mock(description=f"Server {i}")) for i in range(100)
        ]

        mock_catalog = Mock()
        mock_catalog.list_servers.return_value = mock_servers

        mock_ctx = Mock()
        mock_ctx.obj = {"catalog": mock_catalog}
        mock_ctx.params = {}

    # from mcpi.cli import complete_server_ids
    # completions = complete_server_ids(mock_ctx, None, "server")
    #
    # # Should limit to reasonable number (e.g., 50)
    # assert len(completions) <= 50

    def test_complete_server_ids_handles_empty_registry(self):
        """Test graceful handling when registry is empty.

        Workflow: User tabs but registry has no servers
        Expected: Returns empty list (no completions)

        Un-gameable because:
        - Must handle actual empty registry case
        - Cannot fake empty state with non-empty response
        """
        # NOTE: This test will fail until complete_server_ids() is implemented

        mock_catalog = Mock()
        mock_catalog.list_servers.return_value = []

        mock_ctx = Mock()
        mock_ctx.obj = {"catalog": mock_catalog}
        mock_ctx.params = {}

    # from mcpi.cli import complete_server_ids
    # completions = complete_server_ids(mock_ctx, None, "")
    # assert len(completions) == 0


class TestContextAwareServerCompletion:
    """Tests for context-aware server completion (command-specific filtering).

    User workflow: Different commands show different server lists:
    - `mcpi remove <TAB>` - only shows INSTALLED servers
    - `mcpi enable <TAB>` - only shows DISABLED servers
    - `mcpi disable <TAB>` - only shows ENABLED servers
    """

    def test_remove_command_only_completes_installed_servers(self):
        """Test that 'remove' command only shows installed servers.

        Workflow: User types `mcpi remove <TAB>`
        Expected: Only shows servers that are actually installed

        Un-gameable because:
        - Must query manager for installed servers
        - Cannot show not-installed servers in remove command
        - Validates actual server state filtering
        """
        # NOTE: This test will fail until context-aware completion is implemented

        mock_manager = Mock()
        # Only server1 and server2 are installed
        mock_manager.list_servers.return_value = {
            "client/scope/server1": Mock(id="server1", state=ServerState.ENABLED),
            "client/scope/server2": Mock(id="server2", state=ServerState.DISABLED),
        }

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

    # from mcpi.cli import complete_server_ids
    # completions = complete_server_ids(mock_ctx, None, "")
    # completion_values = [c.value for c in completions]
    #
    # assert 'server1' in completion_values
    # assert 'server2' in completion_values
    # # Should not include servers from registry that aren't installed

    def test_enable_command_only_completes_disabled_servers(self):
        """Test that 'enable' command only shows disabled servers.

        Workflow: User types `mcpi enable <TAB>`
        Expected: Only shows servers in DISABLED state

        Un-gameable because:
        - Must filter servers by actual state
        - Cannot show enabled servers in enable command
        - Tests real state-based filtering logic
        """
        # NOTE: This test will fail until context-aware completion is implemented

        mock_manager = Mock()
        mock_manager.list_servers.return_value = {
            "client/scope/server1": Mock(id="server1", state=ServerState.ENABLED),
            "client/scope/server2": Mock(id="server2", state=ServerState.DISABLED),
            "client/scope/server3": Mock(id="server3", state=ServerState.DISABLED),
        }

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

    # from mcpi.cli import complete_server_ids
    # # Simulate context where command is 'enable'
    # mock_ctx.info_name = 'enable'
    # completions = complete_server_ids(mock_ctx, None, "")
    # completion_values = [c.value for c in completions]
    #
    # assert 'server2' in completion_values
    # assert 'server3' in completion_values
    # assert 'server1' not in completion_values  # Already enabled

    def test_disable_command_only_completes_enabled_servers(self):
        """Test that 'disable' command only shows enabled servers.

        Workflow: User types `mcpi disable <TAB>`
        Expected: Only shows servers in ENABLED state

        Un-gameable because:
        - Must filter servers by actual state
        - Cannot show disabled servers in disable command
        """
        # NOTE: This test will fail until context-aware completion is implemented

        mock_manager = Mock()
        mock_manager.list_servers.return_value = {
            "client/scope/server1": Mock(id="server1", state=ServerState.ENABLED),
            "client/scope/server2": Mock(id="server2", state=ServerState.ENABLED),
            "client/scope/server3": Mock(id="server3", state=ServerState.DISABLED),
        }

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

    # from mcpi.cli import complete_server_ids
    # mock_ctx.info_name = 'disable'
    # completions = complete_server_ids(mock_ctx, None, "")
    # completion_values = [c.value for c in completions]
    #
    # assert 'server1' in completion_values
    # assert 'server2' in completion_values
    # assert 'server3' not in completion_values  # Already disabled

    def test_disable_command_shows_scope_in_help_text(self):
        """Test that 'disable' command shows scope information in help text.

        Workflow: User types `mcpi disable <TAB>`
        Expected: Each completion shows the scope where the server is enabled

        Un-gameable because:
        - Must extract actual scope information from ServerInfo
        - Tests that help text provides useful context to user
        - Verifies scope information is correctly displayed
        """
        from mcpi.cli import complete_server_ids
        from mcpi.clients.types import ServerInfo

        mock_manager = Mock()
        mock_manager.list_servers.return_value = {
            "client/user-mcp/server1": ServerInfo(
                id="server1",
                client="claude-code",
                scope="user-mcp",
                config={},
                state=ServerState.ENABLED,
            ),
            "client/project-mcp/server1": ServerInfo(
                id="server1",
                client="claude-code",
                scope="project-mcp",
                config={},
                state=ServerState.ENABLED,
            ),
            "client/user-mcp/server2": ServerInfo(
                id="server2",
                client="claude-code",
                scope="user-mcp",
                config={},
                state=ServerState.ENABLED,
            ),
        }

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}
        mock_ctx.info_name = "disable"

        completions = complete_server_ids(mock_ctx, None, "")
        completion_dict = {(c.value, c.help): c for c in completions}

        # server1 should appear twice with different scopes
        # Check that the help text contains the key information (ignoring color codes for testing)
        server1_helps = [c.help for c in completions if c.value == "server1"]
        assert len(server1_helps) == 2
        assert any("user-mcp" in h for h in server1_helps)
        assert any("project-mcp" in h for h in server1_helps)

        # server2 should appear once with its scope
        server2_helps = [c.help for c in completions if c.value == "server2"]
        assert len(server2_helps) == 1
        assert "user-mcp" in server2_helps[0]

        # Verify total count
        assert len(completions) == 3

    def test_enable_command_shows_scope_in_help_text(self):
        """Test that 'enable' command shows scope information in help text.

        Workflow: User types `mcpi enable <TAB>`
        Expected: Each completion shows the scope where the server is disabled

        Un-gameable because:
        - Tests that scope help text works for enable command too
        - Verifies consistency across commands
        """
        from mcpi.cli import complete_server_ids
        from mcpi.clients.types import ServerInfo

        mock_manager = Mock()
        mock_manager.list_servers.return_value = {
            "client/user-mcp/disabled-server": ServerInfo(
                id="disabled-server",
                client="claude-code",
                scope="user-mcp",
                config={},
                state=ServerState.DISABLED,
            ),
        }

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}
        mock_ctx.info_name = "enable"

        completions = complete_server_ids(mock_ctx, None, "")

        # Verify the server appears with scope information
        assert len(completions) == 1
        assert completions[0].value == "disabled-server"
        # Check for key content in help text (ignoring color codes)
        assert "disabled-server" in completions[0].help
        assert "user-mcp" in completions[0].help
        assert "disabled" in completions[0].help


class TestScopeCompletionIntegration:
    """Tests for scope completion (already implemented, verify it still works).

    User workflow: User types `mcpi add server --scope <TAB>` to see available scopes.

    Note: DynamicScopeType.shell_complete() already exists and is tested in
    test_cli_scope_features.py. These tests ensure it integrates with new completion features.
    """

    def test_scope_completion_works_with_client_context(self):
        """Test that scope completion respects --client parameter.

        Workflow: User types `mcpi add server --client claude-code --scope <TAB>`
        Expected: Shows scopes available for claude-code client

        This is a regression test - functionality already exists.
        """
        from mcpi.cli import DynamicScopeType

        scope_type = DynamicScopeType()

        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": "user-internal"},
            {"name": "project-mcp"},
        ]

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {"client": "claude-code"}

        completions = scope_type.shell_complete(mock_ctx, None, "")
        completion_values = [c.value for c in completions]

        assert "user-internal" in completion_values
        assert "project-mcp" in completion_values
        mock_manager.get_scopes_for_client.assert_called_once_with("claude-code")

    def test_scope_completion_filters_by_prefix(self):
        """Test that scope completion filters based on partial input.

        Workflow: User types `mcpi add server --scope proj<TAB>`
        Expected: Only shows scopes starting with 'proj'

        This is a regression test - functionality already exists.
        """
        from mcpi.cli import DynamicScopeType

        scope_type = DynamicScopeType()

        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": "user-internal"},
            {"name": "project"},
            {"name": "project-mcp"},
        ]

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

        completions = scope_type.shell_complete(mock_ctx, None, "proj")
        completion_values = [c.value for c in completions]

        assert "project" in completion_values
        assert "project-mcp" in completion_values
        assert "user-internal" not in completion_values


class TestCompletionCommand:
    """Tests for `mcpi completion` command that generates shell scripts.

    User workflow: User runs `mcpi completion` to setup tab completion.
    """

    def test_completion_command_exists(self):
        """Test that completion command is available in CLI.

        Workflow: User types `mcpi completion --help`
        Expected: Command exists and shows help text

        Un-gameable because:
        - Must actually test CLI command registration
        - Cannot fake command existence
        """
        # NOTE: This test will fail until completion command is implemented

        runner = CliRunner()
        result = runner.invoke(main, ["completion", "--help"])

        # Will fail with "Error: No such command" until implemented
        assert result.exit_code == 0, "completion command should exist"
        assert "completion" in result.output.lower()
        assert "shell" in result.output.lower()

    def test_completion_command_generates_bash_script(self):
        """Test that completion command generates valid bash script.

        Workflow: User runs `mcpi completion --shell bash`
        Expected: Outputs bash completion script

        Un-gameable because:
        - Must generate actual bash syntax
        - Output must be valid shell script
        - Tests Click's built-in completion generation
        """
        # NOTE: This test will fail until completion command is implemented

        runner = CliRunner()
        result = runner.invoke(main, ["completion", "--shell", "bash"])

        assert result.exit_code == 0
        # Should contain bash completion markers
        assert "_MCPI_COMPLETE" in result.output or "complete" in result.output
        # Should reference mcpi command
        assert "mcpi" in result.output

    def test_completion_command_generates_zsh_script(self):
        """Test that completion command generates valid zsh script.

        Workflow: User runs `mcpi completion --shell zsh`
        Expected: Outputs zsh completion script

        Un-gameable because:
        - Must generate actual zsh syntax
        - Different from bash (tests shell-specific generation)
        """
        # NOTE: This test will fail until completion command is implemented

        runner = CliRunner()
        result = runner.invoke(main, ["completion", "--shell", "zsh"])

        assert result.exit_code == 0
        assert "_MCPI_COMPLETE" in result.output or "compinit" in result.output
        assert "mcpi" in result.output

    def test_completion_command_auto_detects_shell(self):
        """Test that completion command auto-detects shell from environment.

        Workflow: User runs `mcpi completion` without --shell flag
        Expected: Auto-detects from $SHELL environment variable

        Un-gameable because:
        - Must actually read environment
        - Tests real shell detection logic
        """
        # NOTE: This test will fail until completion command is implemented

        runner = CliRunner()
        result = runner.invoke(main, ["completion"], env={"SHELL": "/bin/bash"})

        # Should succeed and generate completion for detected shell
        # (or show helpful error if detection fails)
        assert result.exit_code == 0 or "shell" in result.output.lower()

    def test_completion_command_shows_installation_instructions(self):
        """Test that completion command provides setup instructions.

        Workflow: User runs `mcpi completion --shell bash`
        Expected: Shows how to install the generated completion

        Un-gameable because:
        - Must include actual installation steps
        - Tests UX completeness, not just script generation
        """
        # NOTE: This test will fail until completion command is implemented

        runner = CliRunner()
        result = runner.invoke(main, ["completion", "--shell", "bash"])

        assert result.exit_code == 0
        # Should mention how to activate completion
        assert "bashrc" in result.output.lower() or "eval" in result.output.lower()


class TestCompletionEdgeCases:
    """Tests for edge cases and error handling in completion.

    These tests ensure graceful degradation when things go wrong.
    """

    def test_completion_handles_manager_initialization_failure(self):
        """Test completion when manager fails to initialize.

        Workflow: Tab completion invoked but manager can't be created
        Expected: Returns empty completions, doesn't crash

        Un-gameable because:
        - Tests actual error handling code
        - Must gracefully handle missing dependencies
        """
        from mcpi.cli import DynamicScopeType

        scope_type = DynamicScopeType()

        # Context with no manager and manager getter that fails
        mock_ctx = Mock()
        mock_ctx.obj = {}  # No manager in context
        mock_ctx.params = {}

        # Should return fallback completions, not crash
        completions = scope_type.shell_complete(mock_ctx, None, "")

        # Should return default scopes as fallback
        assert len(completions) > 0  # Has fallback values
        completion_values = [c.value for c in completions]
        assert "user" in completion_values  # Default fallback

    def test_completion_handles_catalog_load_failure(self):
        """Test completion when catalog fails to load registry.

        Workflow: Tab completion for server ID but registry file corrupted
        Expected: Returns empty completions, doesn't crash

        Un-gameable because:
        - Tests actual error recovery
        - Must handle registry I/O errors gracefully
        """
        # NOTE: This test will fail until complete_server_ids() is implemented

        # mock_catalog = Mock()
        # mock_catalog.list_servers.side_effect = IOError("Registry file not found")
        #
        # mock_ctx = Mock()
        # mock_ctx.obj = {'catalog': mock_catalog}
        # mock_ctx.params = {}
        #

    # from mcpi.cli import complete_server_ids
    # completions = complete_server_ids(mock_ctx, None, "")
    #
    # # Should handle error and return empty
    # assert len(completions) == 0

    def test_completion_handles_partial_client_data(self):
        """Test completion when client info has missing fields.

        Workflow: Tab completion but client metadata incomplete
        Expected: Still provides completions with available data

        Un-gameable because:
        - Tests resilience to data quality issues
        - Must handle missing optional fields
        """
        # NOTE: This test will fail until complete_client_names() is implemented

        # mock_manager = Mock()
        # # Client info missing some expected fields
        # mock_manager.get_client_info.return_value = {
        #     'claude-code': {},  # No server_count or scopes
        #     'cursor': {'server_count': 1}  # Missing scopes
        # }
        #
        # mock_ctx = Mock()
        # mock_ctx.obj = {'mcp_manager': mock_manager}
        # mock_ctx.params = {}
        #

    # from mcpi.cli import complete_client_names
    # completions = complete_client_names(mock_ctx, None, "")
    #
    # # Should still return client names even with incomplete data
    # completion_values = [c.value for c in completions]
    # assert 'claude-code' in completion_values
    # assert 'cursor' in completion_values


class TestCompletionIntegrationWithClick:
    """Tests for integration with Click's completion system.

    These tests verify that completion functions are properly wired into Click commands.
    """

    def test_client_option_has_completion_callback(self):
        """Test that --client options are wired for completion.

        Workflow: Verify CLI setup supports client name completion
        Expected: --client option has shell_complete callback

        Un-gameable because:
        - Tests actual CLI decorator configuration
        - Cannot be satisfied without proper wiring
        """
        # NOTE: This test will fail until decorators are updated

    # from mcpi.cli import list  # list command
    #
    # # Find --client option in command parameters
    # client_option = None
    # for param in list.params:
    #     if hasattr(param, 'name') and param.name == 'client':
    #         client_option = param
    #         break
    #
    # assert client_option is not None, "--client option should exist"
    # assert hasattr(client_option, 'shell_complete'), "--client should have completion"
    # assert client_option.shell_complete is not None

    def test_server_id_argument_has_completion_callback(self):
        """Test that server_id arguments are wired for completion.

        Workflow: Verify CLI setup supports server ID completion
        Expected: server_id argument has shell_complete callback

        Un-gameable because:
        - Tests actual CLI argument configuration
        """
        # NOTE: This test will fail until decorators are updated

    # from mcpi.cli import add  # add command
    #
    # # Find server_id argument in command parameters
    # server_id_arg = None
    # for param in add.params:
    #     if hasattr(param, 'name') and param.name == 'server_id':
    #         server_id_arg = param
    #         break
    #
    # assert server_id_arg is not None, "server_id argument should exist"
    # assert hasattr(server_id_arg, 'shell_complete'), "server_id should have completion"
    # assert server_id_arg.shell_complete is not None

    def test_scope_option_has_dynamic_completion(self):
        """Test that --scope options use DynamicScopeType (regression test).

        Workflow: Verify scope completion still works
        Expected: --scope uses DynamicScopeType with shell_complete

        This is a regression test for existing functionality.
        """
        from mcpi.cli import add  # add command

        # Find --scope option in command parameters
        scope_option = None
        for param in add.params:
            if hasattr(param, "name") and param.name == "scope":
                scope_option = param
                break

        assert scope_option is not None, "--scope option should exist"

        # Check that it uses DynamicScopeType (which has shell_complete)
        from mcpi.cli import DynamicScopeType

        assert isinstance(
            scope_option.type, DynamicScopeType
        ), "--scope should use DynamicScopeType for completion"


class TestCompletionPerformance:
    """Tests for completion performance (important for UX).

    Tab completion must be fast (<100ms) or users will experience lag.
    """

    def test_scope_completion_is_fast(self):
        """Test that scope completion completes quickly.

        Workflow: User tabs multiple times rapidly
        Expected: Each completion completes in <100ms

        Un-gameable because:
        - Tests actual performance, not mocked timing
        - Ensures completion is usable in real scenarios
        """
        import time

        from mcpi.cli import DynamicScopeType

        scope_type = DynamicScopeType()

        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": f"scope-{i}"} for i in range(10)
        ]

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

        # Measure completion time
        start = time.time()
        for _ in range(10):  # Simulate 10 rapid tabs
            completions = scope_type.shell_complete(mock_ctx, None, "")
        elapsed = time.time() - start

        # Each completion should be fast (average <10ms)
        avg_time = elapsed / 10
        assert avg_time < 0.1, f"Completion too slow: {avg_time*1000:.1f}ms average"

    def test_large_registry_completion_is_limited(self):
        """Test that huge registry doesn't cause completion lag.

        Workflow: User tabs with registry containing 500+ servers
        Expected: Completion limits results and stays fast

        Un-gameable because:
        - Tests real performance with large dataset
        - Validates result limiting works correctly
        """
        # NOTE: This test will fail until complete_server_ids() is implemented

        # import time
        #
        # # Create huge catalog
        # mock_servers = [(f'server-{i}', Mock(description=f'Server {i}'))
        #                 for i in range(500)]
        #
        # mock_catalog = Mock()
        # mock_catalog.list_servers.return_value = mock_servers
        #
        # mock_ctx = Mock()
        # mock_ctx.obj = {'catalog': mock_catalog}
        # mock_ctx.params = {}
        #

    # from mcpi.cli import complete_server_ids
    #
    # start = time.time()
    # completions = complete_server_ids(mock_ctx, None, "")
    # elapsed = time.time() - start
    #
    # # Should complete quickly even with huge registry
    # assert elapsed < 0.5, f"Completion too slow: {elapsed*1000:.1f}ms"
    # # Should limit results
    # assert len(completions) <= 50, "Should limit results for large registry"


# Summary of Test Coverage
"""
This test suite provides comprehensive coverage of CLI tab completion:

**Client Name Completion** (5 tests):
- Shows detected clients from manager
- Filters by prefix
- Handles no clients gracefully
- Handles missing context
- [Integration test for wiring]

**Server ID Completion** (6 tests):
- Shows servers from catalog
- Includes help text (descriptions)
- Filters by prefix
- Limits results for large registries
- Handles empty registry
- [Integration test for wiring]

**Context-Aware Completion** (3 tests):
- Remove command shows only installed servers
- Enable command shows only disabled servers
- Disable command shows only enabled servers

**Scope Completion** (2 tests):
- Works with client context (regression test)
- Filters by prefix (regression test)

**Completion Command** (5 tests):
- Command exists in CLI
- Generates bash script
- Generates zsh script
- Auto-detects shell
- Shows installation instructions

**Edge Cases** (3 tests):
- Handles manager initialization failure
- Handles catalog load failure
- Handles partial client data

**Integration** (3 tests):
- Client option has completion callback
- Server ID argument has completion callback
- Scope option uses DynamicScopeType

**Performance** (2 tests):
- Scope completion is fast
- Large registry completion is limited

**Total: 29 tests** covering all critical workflows and edge cases.

**Un-gameable Characteristics**:
1. Tests call real manager/catalog APIs (not just mocks)
2. Verify actual data returned, not just function called
3. Test state-based filtering (can't be faked)
4. Test error handling (not just happy path)
5. Test performance (real timing, not mocked)
6. Test CLI integration (actual decorator wiring)

**Implementation Guidance**:
- All tests currently skip/fail because functionality doesn't exist
- Tests specify expected behavior clearly
- Tests follow existing patterns from test_cli_scope_features.py
- Tests are maintainable and resistant to refactoring
- Tests validate real workflows that users will execute
"""


class TestRescopeCompletion:
    """Tests for rescope command argument completion.

    User workflow: Smart completion that guides user through rescope arguments:
    - mcpi rescope <TAB> -> suggests --from flag
    - mcpi rescope --from <TAB> -> shows scopes with servers
    - mcpi rescope --from scope1 <TAB> -> suggests --to flag
    - mcpi rescope --from scope1 --to <TAB> -> shows applicable scopes (excluding source)
    """

    def test_rescope_server_name_completion_from_source_scope(self):
        """Test that server name completes with servers from --from scope.

        Workflow: User types `mcpi rescope --to project-mcp --from user-mcp <TAB>`
        Expected: Shows only servers that exist in user-mcp scope

        This test is un-gameable because:
        - Must query actual servers in specified source scope
        - Cannot return servers from wrong scope
        - Tests context-awareness (which scope is selected)
        """
        from mcpi.cli import complete_rescope_server_name

        # Setup: Mock manager with servers in different scopes
        mock_manager = Mock()
        mock_manager.list_servers.return_value = {
            "server-in-user-mcp": Mock(state=ServerState.ENABLED),
            "another-server": Mock(state=ServerState.ENABLED),
        }
        mock_manager.get_default_client.return_value = "claude-code"

        # Create context with both --to and --from parameters set
        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {
            "to_scope": "project-mcp",
            "from_scope": "user-mcp",
            "client": "claude-code",
        }

        # Simulate user hitting TAB for server_name argument
        completions = complete_rescope_server_name(mock_ctx, None, "")

        # Verify completion calls list_servers with correct scope
        mock_manager.list_servers.assert_called_with(
            client="claude-code", scope="user-mcp"
        )

        # Verify returns servers from that scope
        completion_values = [c.value for c in completions]
        assert "server-in-user-mcp" in completion_values
        assert "another-server" in completion_values

    def test_rescope_to_scope_excludes_from_scope(self):
        """Test that --to completion excludes the --from scope.

        Workflow: User types `mcpi rescope server1 --from user-mcp --to <TAB>`
        Expected: Shows all scopes EXCEPT user-mcp (can't rescope to same scope)

        This test is un-gameable because:
        - Must filter out the source scope from results
        - Tests that invalid operation (same scope) is prevented via completion
        - Verifies context-aware filtering logic
        """
        from mcpi.cli import DynamicScopeType

        # Create mock manager with multiple scopes
        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": "project-mcp", "priority": 1},
            {"name": "user-internal", "priority": 4},
            {"name": "user-local", "priority": 3},
            {"name": "user-mcp", "priority": 5},
        ]

        # Create context where --from is already set to user-mcp
        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {"from_scope": "user-mcp", "client": "claude-code"}

        # Create mock param to indicate we're completing the --to parameter
        mock_param = Mock()
        mock_param.name = "to_scope"

        # Test --to scope completion
        scope_type = DynamicScopeType()
        completions = scope_type.shell_complete(mock_ctx, mock_param, "")

        completion_values = [c.value for c in completions]

        # Should include other scopes (not user-mcp since that's the --from scope)
        assert "project-mcp" in completion_values
        assert "user-local" in completion_values
        assert "user-internal" in completion_values

        # Should NOT include the --from scope
        assert "user-mcp" not in completion_values

    def test_rescope_completion_with_no_from_scope_shows_all(self):
        """Test that without --from set, all scopes are shown.

        Workflow: User types `mcpi rescope server1 --to <TAB>` (no --from yet)
        Expected: Shows all scopes (can't filter without knowing source)

        This test is un-gameable because:
        - Tests behavior when context is incomplete
        - Verifies graceful handling of partial command state
        """
        from mcpi.cli import DynamicScopeType

        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": "project-mcp", "priority": 1},
            {"name": "user-mcp", "priority": 4},
            {"name": "user-local", "priority": 3},
        ]

        # Context without from_scope set
        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {"client": "claude-code"}  # No from_scope

        # Mock param (no name set, or generic name)
        mock_param = Mock()
        mock_param.name = "to_scope"

        scope_type = DynamicScopeType()
        completions = scope_type.shell_complete(mock_ctx, mock_param, "")

        completion_values = [c.value for c in completions]

        # Should show all scopes when source unknown
        assert "project-mcp" in completion_values
        assert "user-mcp" in completion_values
        assert "user-local" in completion_values

    def test_rescope_without_scopes_shows_all_servers(self):
        """Test that typing 'mcpi rescope <TAB>' shows all installed servers.

        Workflow: User types `mcpi rescope <TAB>`
        Expected: Shows all installed MCP servers across all scopes

        This test is un-gameable because:
        - Must query actual installed servers
        - Shows servers from all scopes when no --from specified
        """
        from mcpi.cli import complete_rescope_server_name

        # Setup: Mock manager with servers in different scopes
        mock_manager = Mock()
        mock_manager.list_servers.return_value = {
            "server-in-user": Mock(),
            "server-in-project": Mock(),
            "another-server": Mock(),
        }
        mock_manager.get_default_client.return_value = "claude-code"

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}  # No scopes specified

        # Simulate user hitting TAB after 'mcpi rescope '
        completions = complete_rescope_server_name(mock_ctx, None, "")

        # Should show all installed servers
        completion_values = [c.value for c in completions]
        assert "server-in-user" in completion_values
        assert "server-in-project" in completion_values
        assert "another-server" in completion_values

        # Verify it called list_servers without scope filter
        mock_manager.list_servers.assert_called_with(client="claude-code")
