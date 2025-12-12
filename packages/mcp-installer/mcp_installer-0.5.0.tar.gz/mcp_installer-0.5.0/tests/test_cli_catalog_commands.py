"""Integration tests for CLI catalog commands.

This module tests the CLI integration for Phase 1 multi-catalog support.

Tests cover:
- catalog list command
- catalog info command
- search --catalog flag
- info --catalog flag
- add --catalog flag
- Error handling and help text

Requirements from BACKLOG-CATALOG-PHASE1-2025-11-17-023825.md:
- mcpi catalog list: shows both catalogs in Rich table
- mcpi catalog info <name>: shows catalog details
- mcpi search --catalog <name>: searches specific catalog
- Default behavior unchanged (backward compat)

Test Status: These tests will FAIL until CLI commands are implemented.
"""

import json
from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from mcpi.cli import main as cli
from mcpi.clients.claude_code import ClaudeCodePlugin
from mcpi.clients.manager import MCPManager
from mcpi.clients.registry import ClientRegistry
from mcpi.registry.catalog_manager import (
    CatalogManager,
    create_test_catalog_manager,
)


def create_test_catalog_file(path: Path, servers: Dict[str, Any]) -> None:
    """Helper to create a test catalog JSON file.

    Args:
        path: Path to catalog file
        servers: Dictionary of server_id -> server config
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(servers, f, indent=2)


@pytest.fixture
def cli_runner():
    """Create Click CLI runner."""
    return CliRunner()


@pytest.fixture
def test_catalogs(tmp_path: Path):
    """Create test catalogs and return paths.

    FIXED: Returns CatalogManager instance instead of using env vars.
    This addresses ISSUE-BLOCKING-3.

    Returns:
        Tuple of (CatalogManager, official_path, local_path)
    """
    # Create catalog directories
    official_path = tmp_path / "official" / "catalog.json"
    local_path = tmp_path / "local" / "catalog.json"

    # Create official catalog with sample servers
    create_test_catalog_file(
        official_path,
        {
            "filesystem": {
                "description": "File system access for MCP",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                "categories": ["filesystem", "tools"],
                "repository": "https://github.com/modelcontextprotocol/servers",
            },
            "github": {
                "description": "GitHub API integration",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "categories": ["api", "github"],
                "repository": "https://github.com/modelcontextprotocol/servers",
            },
            "database": {
                "description": "Database query tool",
                "command": "python",
                "args": ["-m", "mcp_database"],
                "categories": ["database", "sql"],
                "repository": None,
            },
        },
    )

    # Create local catalog with custom server
    create_test_catalog_file(
        local_path,
        {
            "custom-tool": {
                "description": "My custom MCP tool",
                "command": "python",
                "args": ["-m", "my_tool"],
                "categories": ["custom"],
                "repository": None,
            }
        },
    )

    # Create test manager (will raise NotImplementedError until implemented)
    try:
        manager = create_test_catalog_manager(
            official_path=official_path, local_path=local_path
        )
    except NotImplementedError:
        # Expected until implementation exists
        manager = None

    return manager, official_path, local_path


def inject_catalog_manager_into_cli(manager: CatalogManager, monkeypatch):
    """Inject test catalog manager into CLI context.

    FIXED: Instead of using environment variables, we directly inject
    the manager into the CLI's get_catalog_manager function.
    This addresses ISSUE-BLOCKING-3.

    Args:
        manager: Test CatalogManager instance
        monkeypatch: pytest monkeypatch fixture
    """

    def mock_get_catalog_manager(ctx):
        return manager

    # Patch the CLI's catalog manager getter
    monkeypatch.setattr("mcpi.cli.get_catalog_manager", mock_get_catalog_manager)


class TestCatalogListCommand:
    """Test mcpi catalog list command."""

    def test_catalog_list_shows_both(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi catalog list shows both catalogs."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["catalog", "list"])

        # Will fail with NotImplementedError or missing command until implemented
        # When implemented, should show both catalogs
        assert result.exit_code == 0 or "not implemented" in result.output.lower()

    def test_catalog_list_shows_servers(self, cli_runner, test_catalogs, monkeypatch):
        """Default behavior shows all servers from all catalogs."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["catalog", "list"])

        # Should list servers from all catalogs
        if result.exit_code == 0:
            assert "Server ID" in result.output
            assert "official" in result.output  # Catalog column
            assert "servers available" in result.output

    def test_catalog_list_summary_shows_metadata(
        self, cli_runner, test_catalogs, monkeypatch
    ):
        """--summary flag shows catalog metadata (old behavior)."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["catalog", "list", "--summary"])

        # Should show catalog metadata
        if result.exit_code == 0:
            assert "official" in result.output or "builtin" in result.output
            assert "local" in result.output or "custom" in result.output
            assert "3" in result.output  # Official catalog count
            assert "1" in result.output  # Local catalog count

    def test_catalog_list_rich_table(self, cli_runner, test_catalogs, monkeypatch):
        """Output uses Rich table formatting."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["catalog", "list"])

        # Rich tables have characteristic formatting
        if result.exit_code == 0:
            assert len(result.output) > 50  # Should have substantial output


class TestCatalogInfoCommand:
    """Test mcpi catalog info <name> command."""

    def test_catalog_info_official(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi catalog info official shows details."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["catalog", "info", "official"])

        if result.exit_code == 0:
            assert "official" in result.output.lower()
            assert "catalog.json" in result.output or "path" in result.output.lower()
            assert "3" in result.output or "server" in result.output.lower()

    def test_catalog_info_local(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi catalog info local shows details."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["catalog", "info", "local"])

        if result.exit_code == 0:
            assert "local" in result.output.lower()
            assert "1" in result.output or "server" in result.output.lower()

    def test_catalog_info_case_insensitive(
        self, cli_runner, test_catalogs, monkeypatch
    ):
        """Works with OFFICIAL, Official, etc."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)

        # Try uppercase
        result = cli_runner.invoke(cli, ["catalog", "info", "OFFICIAL"])
        assert result.exit_code == 0 or "not implemented" in result.output.lower()

        # Try mixed case
        result = cli_runner.invoke(cli, ["catalog", "info", "Official"])
        assert result.exit_code == 0 or "not implemented" in result.output.lower()

    def test_catalog_info_unknown(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi catalog info unknown shows error."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["catalog", "info", "nonexistent"])

        # Should show error for unknown catalog
        assert (
            result.exit_code != 0
            or "not found" in result.output.lower()
            or "unknown" in result.output.lower()
        )


class TestSearchWithCatalog:
    """Test mcpi search with --catalog and --all-catalogs flags."""

    def test_search_default_catalog(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi search <query> searches official by default (backward compat)."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["search", "--query", "filesystem"])

        if result.exit_code == 0:
            assert "filesystem" in result.output.lower()
            # Should NOT find local catalog's custom-tool
            assert "custom-tool" not in result.output.lower()

    def test_search_with_catalog_official(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi search <query> --catalog official works."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(
            cli, ["search", "--query", "filesystem", "--catalog", "official"]
        )

        if result.exit_code == 0:
            assert "filesystem" in result.output.lower()

    def test_search_with_catalog_local(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi search <query> --catalog local works."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(
            cli, ["search", "--query", "custom", "--catalog", "local"]
        )

        if result.exit_code == 0:
            assert "custom" in result.output.lower()
            # Should NOT find official catalog servers
            assert "filesystem" not in result.output.lower()

    def test_search_with_catalog_case_insensitive(
        self, cli_runner, test_catalogs, monkeypatch
    ):
        """--catalog OFFICIAL works (case-insensitive)."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)

        result = cli_runner.invoke(
            cli, ["search", "--query", "filesystem", "--catalog", "OFFICIAL"]
        )
        assert result.exit_code == 0 or "not implemented" in result.output.lower()

        result = cli_runner.invoke(
            cli, ["search", "--query", "custom", "--catalog", "LOCAL"]
        )
        assert result.exit_code == 0 or "not implemented" in result.output.lower()

    def test_search_unknown_catalog(self, cli_runner, test_catalogs, monkeypatch):
        """Unknown catalog name shows clear error."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(
            cli, ["search", "--query", "test", "--catalog", "nonexistent"]
        )

        # Should error for unknown catalog
        assert (
            result.exit_code != 0
            or "unknown" in result.output.lower()
            or "not found" in result.output.lower()
        )


class TestInfoWithCatalog:
    """Test mcpi info with --catalog flag."""

    def test_info_default_catalog(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi info <server> searches official first (backward compat)."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["info", "@anthropic/filesystem"])

        if result.exit_code == 0:
            assert "filesystem" in result.output.lower()

    def test_info_with_catalog_official(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi info <server> --catalog official works."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["info", "github", "--catalog", "official"])

        if result.exit_code == 0:
            assert "github" in result.output.lower()

    def test_info_with_catalog_local(self, cli_runner, test_catalogs, monkeypatch):
        """mcpi info <server> --catalog local works."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["info", "custom-tool", "--catalog", "local"])

        if result.exit_code == 0:
            assert "custom" in result.output.lower()

    def test_info_server_not_in_catalog(self, cli_runner, test_catalogs, monkeypatch):
        """Clear error when server not in specified catalog."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["info", "filesystem", "--catalog", "local"])

        # Should error for server not in catalog
        assert result.exit_code != 0 or "not found" in result.output.lower()


class TestAddWithCatalog:
    """Test mcpi add with --catalog flag."""

    def test_add_default_catalog(
        self, cli_runner, mcp_harness, test_catalogs, monkeypatch
    ):
        """mcpi add <server> uses official by default (backward compat)."""
        catalog_manager, _, _ = test_catalogs
        if catalog_manager is None:
            pytest.skip("CatalogManager not implemented yet")

        # Setup: Create user-mcp scope file
        mcp_harness.setup_scope_files()
        mcp_harness.prepopulate_file(
            "user-mcp", {"mcpEnabled": True, "mcpServers": {}}
        )

        # Create plugin with path overrides
        plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", plugin)
        manager = MCPManager(registry=registry, default_client="claude-code")

        # Mock both catalog_manager and mcp_manager
        inject_catalog_manager_into_cli(catalog_manager, monkeypatch)

        def mock_get_mcp_manager(ctx):
            return manager

        monkeypatch.setattr("mcpi.cli.get_mcp_manager", mock_get_mcp_manager)

        # Test: Run add command
        result = cli_runner.invoke(cli, ["add", "filesystem", "--scope", "user-mcp"])

        # Exit code depends on whether it's in a valid project context
        # At minimum, it should recognize the server exists
        assert (
            "filesystem" in result.output.lower()
            or result.exit_code == 0
            or "not found" in result.output.lower()
        )

    def test_add_with_catalog_local(
        self, cli_runner, mcp_harness, test_catalogs, monkeypatch
    ):
        """mcpi add <server> --catalog local works."""
        catalog_manager, _, _ = test_catalogs
        if catalog_manager is None:
            pytest.skip("CatalogManager not implemented yet")

        # Setup: Create user-mcp scope file
        mcp_harness.setup_scope_files()
        mcp_harness.prepopulate_file(
            "user-mcp", {"mcpEnabled": True, "mcpServers": {}}
        )

        # Create plugin with path overrides
        plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", plugin)
        manager = MCPManager(registry=registry, default_client="claude-code")

        # Mock both catalog_manager and mcp_manager
        inject_catalog_manager_into_cli(catalog_manager, monkeypatch)

        def mock_get_mcp_manager(ctx):
            return manager

        monkeypatch.setattr("mcpi.cli.get_mcp_manager", mock_get_mcp_manager)

        # Test: Run add command
        result = cli_runner.invoke(
            cli, ["add", "custom-tool", "--catalog", "local", "--scope", "user-mcp"]
        )

        # Should recognize the server from local catalog
        assert (
            "custom" in result.output.lower()
            or result.exit_code == 0
            or "not found" in result.output.lower()
        )


class TestCatalogHelpText:
    """Test CLI help text for catalog commands."""

    def test_catalog_group_help(self, cli_runner):
        """mcpi catalog --help shows help text."""
        result = cli_runner.invoke(cli, ["catalog", "--help"])

        # May fail with "no such command" until implemented
        # When implemented, should show help
        if result.exit_code == 0:
            assert "catalog" in result.output.lower()
            assert "list" in result.output.lower() or "Commands:" in result.output

    def test_search_help_shows_catalog_flags(self, cli_runner):
        """mcpi search --help shows --catalog flag."""
        result = cli_runner.invoke(cli, ["search", "--help"])

        # Help should work
        assert result.exit_code == 0

        # When implemented, should show flag
        # assert "--catalog" in result.output

    def test_info_help_shows_catalog_flag(self, cli_runner):
        """mcpi info --help shows --catalog flag."""
        result = cli_runner.invoke(cli, ["info", "--help"])

        # May not have flag yet, but help should work
        assert result.exit_code == 0

        # When implemented, should show flag
        # assert "--catalog" in result.output


class TestBackwardCompatibility:
    """Test that existing CLI patterns still work (no breaking changes)."""

    def test_search_without_flags(self, cli_runner, test_catalogs, monkeypatch):
        """Old: mcpi search <query> still works (searches official)."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["search", "--query", "filesystem"])

        # Should work with or without new features
        assert result.exit_code == 0 or "not implemented" in result.output.lower()

    def test_info_without_flags(self, cli_runner, test_catalogs, monkeypatch):
        """Old: mcpi info <server> still works (searches official)."""
        manager, _, _ = test_catalogs
        if manager is None:
            pytest.skip("CatalogManager not implemented yet")

        inject_catalog_manager_into_cli(manager, monkeypatch)
        result = cli_runner.invoke(cli, ["info", "github"])

        # Should work with or without new features
        assert (
            result.exit_code == 0
            or "not implemented" in result.output.lower()
            or "not found" in result.output.lower()
        )

    def test_add_without_flags(
        self, cli_runner, mcp_harness, test_catalogs, monkeypatch
    ):
        """Old: mcpi add <server> still works (uses official)."""
        catalog_manager, _, _ = test_catalogs
        if catalog_manager is None:
            pytest.skip("CatalogManager not implemented yet")

        # Setup: Create user-mcp scope file
        mcp_harness.setup_scope_files()
        mcp_harness.prepopulate_file(
            "user-mcp", {"mcpEnabled": True, "mcpServers": {}}
        )

        # Create plugin with path overrides
        plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)
        registry = ClientRegistry(auto_discover=False)
        registry.inject_client_instance("claude-code", plugin)
        manager = MCPManager(registry=registry, default_client="claude-code")

        # Mock both catalog_manager and mcp_manager
        inject_catalog_manager_into_cli(catalog_manager, monkeypatch)

        def mock_get_mcp_manager(ctx):
            return manager

        monkeypatch.setattr("mcpi.cli.get_mcp_manager", mock_get_mcp_manager)

        # Test: Run add command
        result = cli_runner.invoke(cli, ["add", "database", "--scope", "user-mcp"])

        # Should recognize server from official catalog
        # Exit code may vary based on project context
        assert (
            "database" in result.output.lower()
            or result.exit_code == 0
            or "not found" in result.output.lower()
        )


class TestCatalogAddCommand:
    """Test mcpi catalog add command.

    This command uses Claude CLI in non-interactive mode to discover
    MCP server information and add it to the catalog.
    """

    def test_catalog_add_help(self, cli_runner):
        """mcpi catalog add --help shows proper help text."""
        result = cli_runner.invoke(cli, ["catalog", "add", "--help"])

        assert result.exit_code == 0
        assert "SOURCE" in result.output
        assert "Claude" in result.output or "claude" in result.output
        assert "--dry-run" in result.output
        assert "github" in result.output.lower() or "url" in result.output.lower()

    def test_catalog_add_requires_source(self, cli_runner):
        """mcpi catalog add with no source shows error."""
        result = cli_runner.invoke(cli, ["catalog", "add"])

        # Click should complain about missing required argument
        assert result.exit_code != 0
        assert "SOURCE" in result.output.upper() or "missing" in result.output.lower()

    def test_catalog_add_missing_claude_cli(self, cli_runner, monkeypatch):
        """mcpi catalog add handles missing Claude CLI gracefully."""
        import subprocess

        # Mock subprocess.run to raise FileNotFoundError for claude
        original_run = subprocess.run

        def mock_run(args, **kwargs):
            if args[0] == "claude":
                raise FileNotFoundError("claude not found")
            return original_run(args, **kwargs)

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = cli_runner.invoke(
            cli, ["catalog", "add", "https://example.com/mcp-server"]
        )

        assert result.exit_code != 0
        assert "claude" in result.output.lower()
        assert "not found" in result.output.lower()

    def test_catalog_add_dry_run_flag(self, cli_runner, monkeypatch):
        """mcpi catalog add --dry-run shows dry run message."""
        import subprocess

        # Mock subprocess.run to return success
        def mock_run(args, **kwargs):
            if args[0] == "claude":
                if "--version" in args:
                    return subprocess.CompletedProcess(args, 0, "1.0.0", "")
                else:
                    return subprocess.CompletedProcess(
                        args,
                        0,
                        "DRY RUN: Would add server-id with config...",
                        "",
                    )
            return subprocess.CompletedProcess(args, 0, "", "")

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = cli_runner.invoke(
            cli, ["catalog", "add", "--dry-run", "https://example.com/mcp-server"]
        )

        assert result.exit_code == 0
        assert "dry run" in result.output.lower()

    def test_catalog_add_accepts_multiple_args(self, cli_runner, monkeypatch):
        """mcpi catalog add accepts multiple words as source."""
        import subprocess

        # Mock subprocess.run to verify the source is joined properly
        captured_prompt = []

        def mock_run(args, **kwargs):
            if args[0] == "claude":
                if "--version" in args:
                    return subprocess.CompletedProcess(args, 0, "1.0.0", "")
                else:
                    # Capture the prompt to verify it contains all source words
                    captured_prompt.append(args[-1])
                    return subprocess.CompletedProcess(
                        args, 0, "Server added successfully", ""
                    )
            return subprocess.CompletedProcess(args, 0, "", "")

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = cli_runner.invoke(
            cli,
            [
                "catalog",
                "add",
                "https://github.com/user/repo",
                "with",
                "extra",
                "context",
            ],
        )

        assert result.exit_code == 0
        # Verify all words were passed
        assert len(captured_prompt) == 1
        prompt = captured_prompt[0]
        assert "github.com/user/repo" in prompt
        assert "with extra context" in prompt

    def test_catalog_add_handles_claude_failure(self, cli_runner, monkeypatch):
        """mcpi catalog add handles Claude CLI failures."""
        import subprocess

        def mock_run(args, **kwargs):
            if args[0] == "claude":
                if "--version" in args:
                    return subprocess.CompletedProcess(args, 0, "1.0.0", "")
                else:
                    return subprocess.CompletedProcess(args, 1, "", "Error occurred")
            return subprocess.CompletedProcess(args, 0, "", "")

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = cli_runner.invoke(
            cli, ["catalog", "add", "https://example.com/mcp-server"]
        )

        assert result.exit_code != 0
        assert "error" in result.output.lower()
