"""Smoke tests for CLI commands to ensure they don't crash immediately."""

import json
from typing import List

import pytest
from click.testing import CliRunner

from mcpi.cli import main


def run_cli_command(args: List[str]) -> tuple[int, str, str]:
    """Run a CLI command and return exit code, stdout, stderr.

    Uses Click's CliRunner for fast, reliable testing without subprocess overhead.
    Note: Click errors (like missing arguments) go to output, not stderr.
    """
    runner = CliRunner()
    result = runner.invoke(main, args, catch_exceptions=False)
    # CliRunner puts everything (stdout + stderr + Click errors) in output
    # For tests checking stderr for Click errors, check output instead
    return result.exit_code, result.output, result.output


class TestCliSmoke:
    """Smoke tests to ensure CLI commands don't immediately fail."""

    def test_mcpi_help(self):
        """Test that mcpi --help works."""
        code, stdout, stderr = run_cli_command(["--help"])
        assert code == 0
        assert "MCPI - MCP Server Package Installer" in stdout
        assert "Commands:" in stdout

    def test_mcpi_version(self):
        """Test that mcpi --version works."""
        code, stdout, stderr = run_cli_command(["--version"])
        assert code == 0

    def test_status_command(self):
        """Test that mcpi status works without crashing."""
        code, stdout, stderr = run_cli_command(["status"])
        assert code == 0
        # Should show MCPI Status panel
        assert "MCPI Status" in stdout or "Default Client" in stdout

    def test_status_json(self):
        """Test that mcpi status --json works."""
        code, stdout, stderr = run_cli_command(["status", "--json"])
        assert code == 0
        # Should be valid JSON dict with status summary
        try:
            data = json.loads(stdout)
            assert isinstance(data, dict)
            assert "total_servers" in data or "default_client" in data
        except json.JSONDecodeError:
            pytest.fail("status --json did not output valid JSON")

    def test_registry_search_help(self):
        """Test that search --help works."""
        code, stdout, stderr = run_cli_command(["search", "--help"])
        assert code == 0
        assert "Search for MCP servers" in stdout

    def test_registry_search_basic(self):
        """Test that search works without crashing."""
        code, stdout, stderr = run_cli_command(["search", "--query", "test"])
        # Should work even if no results
        assert code == 0
        assert "CATALOG" in stdout or "No servers found" in stdout

    def test_info_help(self):
        """Test that info --help works."""
        code, stdout, stderr = run_cli_command(["info", "--help"])
        assert code == 0
        assert "Show detailed information" in stdout

    def test_verbose_flag(self):
        """Test that --verbose flag works."""
        code, stdout, stderr = run_cli_command(["--verbose", "status"])
        assert code == 0
        # Should not crash with verbose flag

    def test_dry_run_flag(self):
        """Test that --dry-run flag works."""
        code, stdout, stderr = run_cli_command(["--dry-run", "status"])
        assert code == 0
        # Should not crash with dry-run flag


class TestCliEdgeCases:
    """Test edge cases and error conditions."""

    def test_info_nonexistent(self):
        """Test showing nonexistent server."""
        code, stdout, stderr = run_cli_command(["info", "nonexistent"])
        assert code == 1
        assert "not found" in stdout

    def test_invalid_command(self):
        """Test invalid command."""
        code, stdout, stderr = run_cli_command(["invalid-command"])
        assert code == 2  # Click error
        assert "No such command" in stderr
