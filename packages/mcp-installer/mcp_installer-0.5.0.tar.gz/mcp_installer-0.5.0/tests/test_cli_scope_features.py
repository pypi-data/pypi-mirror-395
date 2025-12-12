"""Tests for CLI scope features including dynamic scope type and interactive selection."""

from unittest.mock import Mock, patch

import click
import pytest
from click.testing import CliRunner

from mcpi.cli import DynamicScopeType, get_available_scopes, main


class TestDynamicScopeType:
    """Tests for the DynamicScopeType parameter type."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scope_type = DynamicScopeType()

    def test_get_metavar(self):
        """Test that metavar shows dynamic scope message."""
        metavar = self.scope_type.get_metavar(None)
        assert "varies by client" in metavar
        assert "user|project|workspace" in metavar

    def test_get_metavar_with_ctx(self):
        """Test that metavar works with ctx parameter."""
        # Click can pass ctx as keyword argument
        metavar = self.scope_type.get_metavar(None, ctx=None)
        assert "varies by client" in metavar

    def test_convert_none_value(self):
        """Test that None values pass through."""
        result = self.scope_type.convert(None, None, None)
        assert result is None

    def test_convert_without_validation(self):
        """Test that values pass through when no context available."""
        result = self.scope_type.convert("any-scope", None, None)
        assert result == "any-scope"

    @patch("mcpi.cli.get_mcp_manager")
    def test_convert_with_validation_valid_scope(self, mock_get_manager):
        """Test validation accepts valid scopes."""
        # Setup mock manager with scopes
        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": "user", "description": "User scope"},
            {"name": "project", "description": "Project scope"},
        ]

        # Setup context
        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {"client": "test-client"}

        # Test valid scope
        result = self.scope_type.convert("user", None, mock_ctx)
        assert result == "user"
        mock_manager.get_scopes_for_client.assert_called_once_with("test-client")

    @patch("mcpi.cli.get_mcp_manager")
    def test_convert_with_validation_invalid_scope(self, mock_get_manager):
        """Test validation rejects invalid scopes."""
        # Setup mock manager with scopes
        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": "user", "description": "User scope"},
            {"name": "project", "description": "Project scope"},
        ]
        mock_manager.default_client = "default-client"

        # Setup context
        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {}

        # Test invalid scope
        with pytest.raises(click.exceptions.BadParameter) as exc_info:
            self.scope_type.convert("invalid-scope", None, mock_ctx)

        assert "invalid-scope" in str(exc_info.value)
        assert "not a valid scope" in str(exc_info.value)
        assert "user, project" in str(exc_info.value)

    def test_shell_complete_with_client(self):
        """Test shell completion with client context."""
        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": "user-internal"},
            {"name": "user-mcp"},
            {"name": "project-mcp"},
        ]

        mock_ctx = Mock()
        mock_ctx.obj = {"mcp_manager": mock_manager}
        mock_ctx.params = {"client": "claude-code"}

        # Test completion with prefix
        completions = self.scope_type.shell_complete(mock_ctx, None, "user")
        completion_values = [c.value for c in completions]

        assert "user-internal" in completion_values
        assert "user-mcp" in completion_values
        assert "project-mcp" not in completion_values  # Doesn't start with "user"

    def test_shell_complete_fallback(self):
        """Test shell completion fallback when no context available."""
        # Test with no context
        completions = self.scope_type.shell_complete(None, None, "proj")
        completion_values = [c.value for c in completions]

        assert "project" in completion_values
        assert "project-mcp" in completion_values
        assert "user" not in completion_values  # Doesn't start with "proj"


class TestGetAvailableScopes:
    """Tests for the get_available_scopes helper function."""

    @patch("mcpi.cli.get_mcp_manager")
    def test_get_available_scopes_with_client(self, mock_get_manager):
        """Test getting scopes for a specific client."""
        mock_manager = Mock()
        mock_manager.get_scopes_for_client.return_value = [
            {"name": "scope1", "description": "First scope"},
            {"name": "scope2", "description": "Second scope"},
        ]

        mock_ctx = Mock()
        mock_ctx.obj = {}
        mock_get_manager.return_value = mock_manager

        scopes = get_available_scopes(mock_ctx, "test-client")

        assert scopes == ["scope1", "scope2"]
        mock_manager.get_scopes_for_client.assert_called_once_with("test-client")

    @patch("mcpi.cli.get_mcp_manager")
    def test_get_available_scopes_exception_fallback(self, mock_get_manager):
        """Test fallback to default scopes on exception."""
        mock_get_manager.side_effect = Exception("Connection failed")

        mock_ctx = Mock()
        scopes = get_available_scopes(mock_ctx, None)

        # Should return default scopes
        assert "user" in scopes
        assert "user-internal" in scopes
        assert "project" in scopes
        assert "project-mcp" in scopes


class TestInteractiveScopeSelection:
    """Tests for interactive scope selection in add command."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("mcpi.cli.get_catalog")
    @patch("mcpi.cli.get_mcp_manager")
    @patch("mcpi.cli.Prompt.ask")
    def test_add_command_interactive_scope_selection(
        self, mock_prompt, mock_get_manager, mock_get_catalog
    ):
        """Test interactive scope selection when no scope provided."""
        # Setup mock catalog with server
        mock_server = Mock()
        mock_server.id = "test-server"
        mock_server.name = "Test Server"
        mock_server.description = "Test description"
        mock_server.command = "npx"
        mock_server.package = "test-package"
        mock_server.args = []
        mock_server.env = {}
        mock_server.install_method = "npx"

        mock_catalog = Mock()
        mock_catalog.get_server.return_value = mock_server
        mock_get_catalog.return_value = mock_catalog

        # Setup mock manager with scopes
        mock_manager = Mock()
        mock_manager.default_client = "claude-code"
        mock_manager.get_scopes_for_client.return_value = [
            {
                "name": "user-internal",
                "description": "User internal scope",
                "is_user_level": True,
                "exists": True,
            },
            {
                "name": "project-mcp",
                "description": "Project MCP scope",
                "is_user_level": False,
                "exists": False,
            },
        ]
        mock_manager.get_server_info.return_value = None  # Server doesn't exist yet
        mock_get_manager.return_value = mock_manager

        # Mock user selecting option 2
        mock_prompt.return_value = "2"

        # Run command (will fail at actual add, but we're testing the selection)
        result = self.runner.invoke(main, ["add", "test-server"], input="n\n")

        # Check that scope selection was displayed
        # CLI uses server ID in prompt, not server name
        assert "Select a scope for 'test-server'" in result.output
        assert "[1] user-internal - User scope ✓" in result.output
        assert "[2] project-mcp - Project scope ✗" in result.output
        assert "Selected scope: project-mcp" in result.output

        # Verify prompt was called
        mock_prompt.assert_called_once()
        choices = mock_prompt.call_args[1]["choices"]
        assert choices == ["1", "2"]

    @patch("mcpi.cli.get_catalog")
    @patch("mcpi.cli.get_mcp_manager")
    def test_add_command_skip_interactive_with_explicit_scope(
        self, mock_get_manager, mock_get_catalog
    ):
        """Test that interactive selection is skipped when scope is provided."""
        # Setup mock catalog with server
        mock_server = Mock()
        mock_server.id = "test-server"
        mock_server.name = "Test Server"
        mock_server.description = "Test description"
        mock_server.command = "npx"
        mock_server.package = "test-package"
        mock_server.args = []
        mock_server.env = {}
        mock_server.install_method = "npx"

        mock_catalog = Mock()
        mock_catalog.get_server.return_value = mock_server
        mock_get_catalog.return_value = mock_catalog

        # Setup mock manager
        mock_manager = Mock()
        mock_manager.default_client = "claude-code"
        mock_manager.get_server_info.return_value = None
        mock_get_manager.return_value = mock_manager

        # Run command with explicit scope
        result = self.runner.invoke(
            main, ["add", "test-server", "--scope", "user-internal"], input="n\n"
        )

        # Check that scope selection was NOT displayed
        assert "Select a scope for" not in result.output
        assert "Enter the number of your choice" not in result.output

        # But the specified scope should be shown in confirmation
        assert "Target Scope: user-internal" in result.output

    @patch("mcpi.cli.get_catalog")
    @patch("mcpi.cli.get_mcp_manager")
    def test_add_command_dry_run_auto_scope(self, mock_get_manager, mock_get_catalog):
        """Test that dry-run mode auto-selects first scope."""
        # Setup mock catalog with server
        mock_server = Mock()
        mock_server.id = "test-server"
        mock_server.name = "Test Server"
        mock_server.description = "Test description"
        mock_server.command = "npx"
        mock_server.package = "test-package"
        mock_server.args = []
        mock_server.env = {}
        mock_server.install_method = "npx"

        mock_catalog = Mock()
        mock_catalog.get_server.return_value = mock_server
        mock_get_catalog.return_value = mock_catalog

        # Setup mock manager with scopes
        mock_manager = Mock()
        mock_manager.default_client = "claude-code"
        mock_manager.get_scopes_for_client.return_value = [
            {
                "name": "first-scope",
                "description": "First scope",
                "is_user_level": True,
                "exists": True,
            },
            {
                "name": "second-scope",
                "description": "Second scope",
                "is_user_level": False,
                "exists": False,
            },
        ]
        mock_manager.get_server_info.return_value = None
        mock_manager.add_server = Mock()
        mock_get_manager.return_value = mock_manager

        # Run command in dry-run mode
        result = self.runner.invoke(main, ["add", "test-server", "--dry-run"])

        # Check that it auto-selected first scope
        assert "Dry-run: Would use scope 'first-scope'" in result.output
        assert "Select a scope for" not in result.output  # No interactive menu
        # CLI uses server ID in output, not server name
        assert "Would add: test-server" in result.output
        assert "Scope: first-scope" in result.output

    @patch("mcpi.cli.get_catalog")
    @patch("mcpi.cli.get_mcp_manager")
    def test_add_command_no_scopes_available(self, mock_get_manager, mock_get_catalog):
        """Test handling when no scopes are available."""
        # Setup mock catalog with server
        mock_server = Mock()
        mock_server.id = "test-server"
        mock_server.name = "Test Server"

        mock_catalog = Mock()
        mock_catalog.get_server.return_value = mock_server
        mock_get_catalog.return_value = mock_catalog

        # Setup mock manager with no scopes
        mock_manager = Mock()
        mock_manager.default_client = "claude-code"
        mock_manager.get_scopes_for_client.return_value = []
        mock_get_manager.return_value = mock_manager

        # Run command
        result = self.runner.invoke(main, ["add", "test-server"])

        # Should show error message
        assert "No scopes available for client 'claude-code'" in result.output
        assert result.exit_code != 0


class TestScopeCommandHelp:
    """Tests for scope-related help text in commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_list_command_help_shows_dynamic_scope(self):
        """Test that list command help shows dynamic scope type."""
        result = self.runner.invoke(main, ["list", "--help"])

        assert "--scope" in result.output
        assert "varies by client" in result.output
        # Check for scope-related help text
        output_oneline = result.output.replace("\n", " ")
        assert "--scope" in output_oneline and "scope" in output_oneline.lower()

    def test_add_command_help_shows_dynamic_scope(self):
        """Test that add command help shows dynamic scope type."""
        result = self.runner.invoke(main, ["add", "--help"])

        assert "--scope" in result.output
        assert "varies by client" in result.output
        # Check for scope-related help text
        output_oneline = result.output.replace("\n", " ")
        assert "--scope" in output_oneline and "scope" in output_oneline.lower()

    def test_remove_command_help_shows_dynamic_scope(self):
        """Test that remove command help shows dynamic scope type."""
        result = self.runner.invoke(main, ["remove", "--help"])

        assert "--scope" in result.output
        assert "varies by client" in result.output
        # Check for scope-related help text
        output_oneline = result.output.replace("\n", " ")
        assert "--scope" in output_oneline and "scope" in output_oneline.lower()

    @patch("mcpi.cli.get_mcp_manager")
    def test_scope_list_command(self, mock_get_manager):
        """Test scope list command displays available scopes."""
        # Setup mock manager
        mock_manager = Mock()
        mock_manager.default_client = "test-client"
        mock_manager.get_scopes_for_client.return_value = [
            {
                "name": "user-scope",
                "description": "User level scope",
                "priority": 1,
                "path": "/home/user/.config",
                "is_user_level": True,
                "is_project_level": False,
                "exists": True,
            },
            {
                "name": "project-scope",
                "description": "Project level scope",
                "priority": 2,
                "path": "/project/.config",
                "is_user_level": False,
                "is_project_level": True,
                "exists": False,
            },
        ]
        mock_get_manager.return_value = mock_manager

        # Run scope list command
        result = self.runner.invoke(main, ["scope", "list"])

        assert result.exit_code == 0
        assert "Configuration Scopes: test-client" in result.output
        assert "user-scope" in result.output
        assert "User" in result.output
        assert "✓" in result.output  # exists marker
        assert "project-scope" in result.output
        assert "Project" in result.output
        assert "✗" in result.output  # not exists marker
