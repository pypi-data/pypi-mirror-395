"""Integration tests for CLI commands with minimal mocking."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from mcpi.cli import main


# Import test harness fixtures
from tests.test_harness import (  # noqa: F401
    mcp_harness,
    mcp_test_dir,
    mcp_manager_with_harness,
)


class TestCliIntegration:
    """Integration tests that use real components with minimal mocking."""

    def setup_method(self):
        """Set up test environment for each test."""
        self.runner = CliRunner()

    def test_help_command(self):
        """Test help command works."""
        result = self.runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "MCP Server Package Installer" in result.output

    def test_version_command(self):
        """Test version command works."""
        result = self.runner.invoke(main, ["--version"])
        assert result.exit_code == 0

    def test_status_command_no_servers(self, mcp_manager_with_harness):
        """Test status command when no servers are installed."""
        manager, harness = mcp_manager_with_harness

        # Manager has no servers installed in test environment
        result = self.runner.invoke(main, ["status"], obj={"mcp_manager": manager})

        assert result.exit_code == 0
        # Should show 0 servers instead of "No MCP servers installed"
        assert "Total Servers: 0" in result.output

    def test_status_json_no_servers(self, mcp_manager_with_harness):
        """Test status --json command when no servers are installed."""
        manager, harness = mcp_manager_with_harness

        result = self.runner.invoke(
            main, ["status", "--json"], obj={"mcp_manager": manager}
        )

        assert result.exit_code == 0
        data = json.loads(result.output)
        # Status returns a dict, not a list
        assert isinstance(data, dict)
        assert data.get("total_servers") == 0

    def test_registry_search(self):
        """Test search functionality."""
        result = self.runner.invoke(main, ["search", "--query", "filesystem"])
        assert result.exit_code == 0
        # Should show search results or "No servers found"
        assert "CATALOG" in result.output or "No servers found" in result.output

    def test_info_nonexistent(self):
        """Test showing a nonexistent server."""
        result = self.runner.invoke(main, ["info", "nonexistent-server"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_verbose_flag(self):
        """Test verbose flag doesn't break anything."""
        result = self.runner.invoke(main, ["--verbose", "status"])
        assert result.exit_code == 0
        # Verbose might add extra output, but should still work
        assert "servers" in result.output.lower()

    def test_dry_run_flag(self):
        """Test dry-run flag doesn't break anything."""
        result = self.runner.invoke(main, ["--dry-run", "status"])
        assert result.exit_code == 0
        # Dry-run shouldn't change status command behavior
        assert "servers" in result.output.lower()
