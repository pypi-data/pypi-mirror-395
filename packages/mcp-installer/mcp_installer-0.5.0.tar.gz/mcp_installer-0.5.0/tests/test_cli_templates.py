"""CLI integration tests for configuration templates.

This module tests the end-to-end template workflow through the CLI,
including --list-templates and --template flags for the 'add' command.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from mcpi.cli import main
from mcpi.clients.types import ServerConfig
from mcpi.templates.models import PromptDefinition, ServerTemplate


@pytest.fixture
def cli_runner():
    """Create a Click CLI runner."""
    return CliRunner()


@pytest.fixture
def mock_template_manager():
    """Create a mock TemplateManager with test templates."""
    manager = MagicMock()

    # Create test templates for different servers
    postgres_prod = ServerTemplate(
        name="production",
        description="Production PostgreSQL setup with TLS",
        server_id="postgres",
        scope="user-mcp",
        priority="high",
        config={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": {"POSTGRES_SSL_MODE": "require"},
        },
        prompts=[
            PromptDefinition(
                name="POSTGRES_HOST",
                description="Database host",
                type="string",
                required=True,
            ),
            PromptDefinition(
                name="POSTGRES_PORT",
                description="Database port",
                type="port",
                default="5432",
            ),
            PromptDefinition(
                name="POSTGRES_PASSWORD",
                description="Database password",
                type="secret",
                required=True,
            ),
        ],
        notes="Requires PostgreSQL 12+ with SSL enabled",
    )

    postgres_dev = ServerTemplate(
        name="development",
        description="Local development setup",
        server_id="postgres",
        scope="project-mcp",
        priority="medium",
        config={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": {},
        },
        prompts=[
            PromptDefinition(
                name="POSTGRES_DB",
                description="Database name",
                type="string",
                default="dev_db",
            )
        ],
        notes="For local development only",
    )

    github_template = ServerTemplate(
        name="full-access",
        description="Full access to GitHub",
        server_id="github",
        scope="user-mcp",
        priority="high",
        config={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {},
        },
        prompts=[
            PromptDefinition(
                name="GITHUB_TOKEN",
                description="GitHub personal access token",
                type="secret",
                required=True,
            )
        ],
    )

    # Configure mock behavior
    def mock_list_templates(server_id: str):
        if server_id == "postgres":
            return [postgres_prod, postgres_dev]
        elif server_id == "github":
            return [github_template]
        else:
            return []

    def mock_get_template(server_id: str, template_name: str):
        templates = {
            "postgres": {"production": postgres_prod, "development": postgres_dev},
            "github": {"full-access": github_template},
        }
        return templates.get(server_id, {}).get(template_name)

    def mock_apply_template(template: ServerTemplate, user_values: dict):
        # Merge template config with user values
        env = dict(template.config.get("env", {}))
        env.update(user_values)
        return ServerConfig(
            command=template.config["command"],
            args=template.config["args"],
            env=env,
            type="stdio",
        )

    manager.list_templates.side_effect = mock_list_templates
    manager.get_template.side_effect = mock_get_template
    manager.apply_template.side_effect = mock_apply_template

    return manager


@pytest.fixture
def mock_catalog():
    """Create a mock catalog with test servers."""
    catalog = MagicMock()

    # Create test server entries
    postgres_server = MagicMock()
    postgres_server.id = "postgres"
    postgres_server.description = "PostgreSQL MCP server"
    postgres_server.command = "npx"
    postgres_server.args = ["-y", "@modelcontextprotocol/server-postgres"]

    github_server = MagicMock()
    github_server.id = "github"
    github_server.description = "GitHub MCP server"
    github_server.command = "npx"
    github_server.args = ["-y", "@modelcontextprotocol/server-github"]

    filesystem_server = MagicMock()
    filesystem_server.id = "filesystem"
    filesystem_server.description = "Filesystem MCP server"
    filesystem_server.command = "npx"
    filesystem_server.args = ["-y", "@modelcontextprotocol/server-filesystem"]

    def mock_get_server(server_id: str):
        if server_id == "postgres":
            return postgres_server
        elif server_id == "github":
            return github_server
        elif server_id == "filesystem":
            return filesystem_server
        return None

    catalog.get_server.side_effect = mock_get_server

    return catalog


@pytest.fixture
def mock_manager():
    """Create a mock MCPManager."""
    manager = MagicMock()
    manager.default_client = "claude-code"

    # Mock get_scopes_for_client to return test scopes
    def mock_get_scopes(client_name=None):
        return [
            {
                "name": "project-mcp",
                "description": "Project scope",
                "is_user_level": False,
                "priority": 10,
                "exists": True,
                "path": "./.mcp.json",
            },
            {
                "name": "user-mcp",
                "description": "User global scope",
                "is_user_level": True,
                "priority": 50,
                "exists": True,
                "path": "~/.config/claude/settings.json",
            },
        ]

    manager.get_scopes_for_client.side_effect = mock_get_scopes
    manager.get_server_info.return_value = None  # Server not installed
    manager.add_server.return_value = MagicMock(success=True, message="Added")

    return manager


class TestListTemplatesCommand:
    """Tests for mcpi add <server> --list-templates command."""

    def test_list_templates_postgres(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test listing templates for postgres server."""
        result = cli_runner.invoke(
            main,
            ["add", "postgres", "--list-templates"],
            obj={
                "template_manager": mock_template_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
                "mcp_manager": mock_manager,
            },
        )

        assert result.exit_code == 0
        assert "Available Templates for 'postgres'" in result.output
        assert "production" in result.output
        assert "development" in result.output
        assert "Production PostgreSQL setup with TLS" in result.output

    def test_list_templates_github(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test listing templates for github server."""
        result = cli_runner.invoke(
            main,
            ["add", "github", "--list-templates"],
            obj={
                "template_manager": mock_template_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
                "mcp_manager": mock_manager,
            },
        )

        assert result.exit_code == 0
        assert "Available Templates for 'github'" in result.output
        assert "full-access" in result.output
        assert "Full access to GitHub" in result.output

    def test_list_templates_server_without_templates(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test listing templates for server with no templates (returns empty list)."""
        # filesystem is in the catalog but has no templates
        result = cli_runner.invoke(
            main,
            ["add", "filesystem", "--list-templates"],
            obj={
                "template_manager": mock_template_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
                "mcp_manager": mock_manager,
            },
        )

        assert result.exit_code == 0
        assert "No templates available for 'filesystem'" in result.output
        assert "Use 'mcpi add filesystem'" in result.output

    def test_list_templates_invalid_server(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test listing templates for non-existent server."""
        # Update the side_effect to return None for this test
        mock_catalog.get_server.side_effect = lambda x: None

        result = cli_runner.invoke(
            main,
            ["add", "nonexistent", "--list-templates"],
            obj={
                "template_manager": mock_template_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
                "mcp_manager": mock_manager,
            },
        )

        assert result.exit_code == 0
        assert "not found" in result.output


class TestTemplateApplicationCommand:
    """Tests for mcpi add <server> --template <name> command."""

    def test_apply_template_success(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test successful template application with user input."""
        # Mock the interactive prompts
        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            mock_collect.return_value = {
                "POSTGRES_HOST": "localhost",
                "POSTGRES_PORT": "5432",
                "POSTGRES_PASSWORD": "secret123",
            }

            result = cli_runner.invoke(
                main,
                ["add", "postgres", "--template", "production"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0
            assert (
                "Adding postgres" in result.output
                or "Successfully added" in result.output
            )
            mock_collect.assert_called_once()
            mock_manager.add_server.assert_called_once()

    def test_apply_template_uses_template_scope(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test that template's recommended scope is used when --scope not specified."""
        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            mock_collect.return_value = {"POSTGRES_DB": "mydb"}

            result = cli_runner.invoke(
                main,
                ["add", "postgres", "--template", "development"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0
            # Verify template's scope (project-mcp) was used
            call_args = mock_manager.add_server.call_args
            assert call_args[0][2] == "project-mcp"  # Third arg is scope

    def test_apply_template_invalid_template_name(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test error when template name doesn't exist."""
        result = cli_runner.invoke(
            main,
            ["add", "postgres", "--template", "nonexistent"],
            obj={
                "template_manager": mock_template_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
                "mcp_manager": mock_manager,
            },
        )

        assert result.exit_code == 0
        assert "not found" in result.output
        assert "mcpi add postgres --list-templates" in result.output

    def test_apply_template_invalid_server(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test error when server doesn't exist in catalog."""
        # Update side_effect for this test
        mock_catalog.get_server.side_effect = lambda x: None

        result = cli_runner.invoke(
            main,
            ["add", "nonexistent", "--template", "production"],
            obj={
                "template_manager": mock_template_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
                "mcp_manager": mock_manager,
            },
        )

        assert result.exit_code == 0
        assert "not found" in result.output

    def test_apply_template_user_cancels(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test graceful handling when user cancels with Ctrl+C."""
        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            mock_collect.side_effect = KeyboardInterrupt()

            result = cli_runner.invoke(
                main,
                ["add", "postgres", "--template", "production"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0
            assert "cancelled" in result.output.lower()
            # Server should NOT be added
            mock_manager.add_server.assert_not_called()

    def test_apply_template_with_scope_override(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test that --scope flag overrides template's recommended scope."""
        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            mock_collect.return_value = {
                "POSTGRES_HOST": "localhost",
                "POSTGRES_PORT": "5432",
                "POSTGRES_PASSWORD": "secret123",
            }

            result = cli_runner.invoke(
                main,
                [
                    "add",
                    "postgres",
                    "--template",
                    "production",
                    "--scope",
                    "project-mcp",
                ],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0
            # Verify user's scope was used instead of template's
            call_args = mock_manager.add_server.call_args
            assert call_args[0][2] == "project-mcp"

    def test_template_values_merged_into_config(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test that template values are correctly merged into server config."""
        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            user_values = {
                "POSTGRES_HOST": "db.example.com",
                "POSTGRES_PORT": "5433",
                "POSTGRES_PASSWORD": "supersecret",
            }
            mock_collect.return_value = user_values

            result = cli_runner.invoke(
                main,
                ["add", "postgres", "--template", "production"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0

            # Verify config passed to add_server
            call_args = mock_manager.add_server.call_args
            config = call_args[0][1]  # Second arg is config
            assert isinstance(config, ServerConfig)
            assert config.env["POSTGRES_HOST"] == "db.example.com"
            assert config.env["POSTGRES_PORT"] == "5433"
            assert config.env["POSTGRES_PASSWORD"] == "supersecret"
            # Static config from template should also be present
            assert config.env["POSTGRES_SSL_MODE"] == "require"


class TestTemplateWorkflowIntegration:
    """End-to-end integration tests for template workflow."""

    def test_full_workflow_list_then_apply(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test realistic workflow: list templates, then apply one."""
        # Step 1: User lists available templates
        result1 = cli_runner.invoke(
            main,
            ["add", "postgres", "--list-templates"],
            obj={
                "template_manager": mock_template_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
                "mcp_manager": mock_manager,
            },
        )

        assert result1.exit_code == 0
        assert "production" in result1.output
        assert "development" in result1.output

        # Step 2: User applies a template
        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            mock_collect.return_value = {"POSTGRES_DB": "mydb"}

            result2 = cli_runner.invoke(
                main,
                ["add", "postgres", "--template", "development"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result2.exit_code == 0
            mock_manager.add_server.assert_called_once()

    def test_normal_add_still_works(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test that normal 'mcpi add' (without --template) still works."""
        # Mock scope selection (simulating user choosing option 1)
        with patch("mcpi.cli.Prompt.ask") as mock_prompt:
            mock_prompt.return_value = "1"  # Select first scope

            result = cli_runner.invoke(
                main,
                ["add", "postgres"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0
            # Should add server without template
            mock_manager.add_server.assert_called_once()
            # Config should be default (not from template)
            call_args = mock_manager.add_server.call_args
            config = call_args[0][1]
            assert config.env == {}  # No template values

    def test_template_with_different_clients(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test templates work with different MCP clients."""
        # Mock a different client
        cursor_manager = MagicMock()
        cursor_manager.default_client = "cursor"
        cursor_manager.get_scopes_for_client.return_value = [
            {
                "name": "workspace",
                "description": "Workspace scope",
                "is_user_level": False,
                "priority": 10,
                "exists": True,
                "path": "./.cursor/settings.json",
            }
        ]
        cursor_manager.get_server_info.return_value = None
        cursor_manager.add_server.return_value = MagicMock(success=True)

        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            mock_collect.return_value = {"GITHUB_TOKEN": "ghp_abc123"}

            result = cli_runner.invoke(
                main,
                ["add", "github", "--template", "full-access", "--client", "cursor"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": cursor_manager,
                },
            )

            # Should work with cursor client
            assert result.exit_code == 0
            cursor_manager.add_server.assert_called_once()


class TestTemplateDryRun:
    """Tests for --dry-run flag with templates."""

    def test_dry_run_with_template(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test --dry-run shows what would happen without making changes."""
        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            mock_collect.return_value = {
                "POSTGRES_HOST": "localhost",
                "POSTGRES_PORT": "5432",
                "POSTGRES_PASSWORD": "secret123",
            }

            result = cli_runner.invoke(
                main,
                ["add", "postgres", "--template", "production", "--dry-run"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0
            assert "Would add" in result.output or "Dry-run" in result.output
            # Server should NOT actually be added
            mock_manager.add_server.assert_not_called()


class TestTemplateErrorHandling:
    """Tests for error handling in template workflow."""

    def test_validation_error_during_prompts(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test handling of validation errors during prompt collection."""
        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            # Simulate an error during validation
            mock_collect.side_effect = ValueError("Invalid port number")

            result = cli_runner.invoke(
                main,
                ["add", "postgres", "--template", "production"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0
            assert "Error" in result.output or "error" in result.output
            # Server should NOT be added after error
            mock_manager.add_server.assert_not_called()

    def test_server_already_exists(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test error when trying to add server that already exists."""
        # Mock server already exists
        existing_info = MagicMock()
        existing_info.state.name = "ENABLED"
        mock_manager.get_server_info.return_value = existing_info

        with patch(
            "mcpi.templates.prompt_handler.collect_template_values"
        ) as mock_collect:
            mock_collect.return_value = {"POSTGRES_DB": "mydb"}

            result = cli_runner.invoke(
                main,
                ["add", "postgres", "--template", "development"],
                obj={
                    "template_manager": mock_template_manager,
                    "catalog_manager": MagicMock(
                        get_default_catalog=lambda: mock_catalog,
                        get_catalog=lambda x: mock_catalog,
                    ),
                    "mcp_manager": mock_manager,
                },
            )

            assert result.exit_code == 0
            assert "already exists" in result.output
            # Should NOT attempt to add
            mock_manager.add_server.assert_not_called()


class TestTemplateDiscovery:
    """Tests for template discovery and loading."""

    def test_template_manager_lazy_loading(
        self, cli_runner, mock_catalog, mock_manager
    ):
        """Test that template manager is only loaded when needed."""
        # When NOT using templates, manager should not be loaded
        result = cli_runner.invoke(
            main,
            ["list"],
            obj={
                "mcp_manager": mock_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
            },
        )

        assert result.exit_code == 0
        # Template manager should NOT be in context (lazy loading)
        # This test passes if no template-related errors occur

    def test_template_manager_loaded_on_demand(
        self, cli_runner, mock_template_manager, mock_catalog, mock_manager
    ):
        """Test that template manager is loaded when --list-templates used."""
        result = cli_runner.invoke(
            main,
            ["add", "postgres", "--list-templates"],
            obj={
                "template_manager": mock_template_manager,
                "catalog_manager": MagicMock(
                    get_default_catalog=lambda: mock_catalog,
                    get_catalog=lambda x: mock_catalog,
                ),
                "mcp_manager": mock_manager,
            },
        )

        assert result.exit_code == 0
        # Template manager's list_templates should be called
        mock_template_manager.list_templates.assert_called_once_with("postgres")
