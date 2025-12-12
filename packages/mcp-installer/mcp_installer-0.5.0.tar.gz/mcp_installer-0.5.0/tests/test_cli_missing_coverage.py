"""Targeted tests for missing lines in cli.py to boost coverage from 85% to 90%+."""

import json
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from mcpi.cli import main


class TestCLIMissingCoverage:
    """Tests specifically targeting high-impact missing lines in cli.py."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.mock_catalog = Mock()
        self.mock_server = Mock()
        self.mock_server.id = "test-server"
        self.mock_server.name = "Test Server"
        self.mock_server.description = "A test server"
        self.mock_server.model_dump.return_value = {
            "id": "test-server",
            "name": "Test Server",
            "description": "A test server",
        }
        self.mock_server.installation = Mock()
        self.mock_server.installation.method = "npm"
        self.mock_manager = Mock()

    def test_registry_info_with_json_output(self):
        """Test info command with --json flag.

        Targets JSON output for server info.
        """
        with patch("mcpi.cli.get_catalog") as mock_get_catalog:
            mock_get_catalog.return_value = self.mock_catalog
            self.mock_catalog.get_server.return_value = self.mock_server

            result = self.runner.invoke(main, ["info", "test-server", "--json"])

            # Should succeed and output JSON
            assert result.exit_code == 0
            # Verify JSON output format
            try:
                json_data = json.loads(result.output.strip())
                assert json_data["id"] == "test-server"
            except json.JSONDecodeError:
                pytest.fail("Output should be valid JSON")

    def test_registry_search_with_json_output_tuple_result(self):
        """Test search command with --json and tuple results.

        Targets tuple unpacking for search results with scores.
        """
        with patch("mcpi.cli.get_catalog") as mock_get_catalog:
            mock_get_catalog.return_value = self.mock_catalog

            # Mock search results as tuples (server_id, server)
            self.mock_catalog.search_servers.return_value = [
                ("test-server", self.mock_server)
            ]

            result = self.runner.invoke(main, ["search", "-q", "test", "--json"])

            assert result.exit_code == 0
            # Verify JSON output
            try:
                json_data = json.loads(result.output.strip())
                assert len(json_data) == 1
                assert json_data[0]["id"] == "test-server"
            except json.JSONDecodeError:
                pytest.fail("Output should be valid JSON")

    def test_status_command_with_json_output(self):
        """Test status command with --json flag.

        Targets JSON output paths in status command.
        """
        with patch("mcpi.cli.create_default_manager") as mock_manager_fn:
            mock_manager_fn.return_value = self.mock_manager
            self.mock_manager.get_status_summary.return_value = {
                "default_client": "claude-code",
                "available_clients": ["claude-code"],
                "total_servers": 1,
                "server_states": {"ENABLED": 1},
                "registry_stats": {"total_clients": 1, "loaded_instances": 1},
            }

            result = self.runner.invoke(main, ["status", "--json"])

            assert result.exit_code == 0
            # Should output JSON format
            try:
                json_data = json.loads(result.output.strip())
                assert isinstance(json_data, (dict, list))
                assert "default_client" in json_data
            except json.JSONDecodeError:
                pytest.fail("Output should be valid JSON")

    def test_registry_info_server_not_found(self):
        """Test info with non-existent server.

        Targets error handling paths.
        """
        with patch("mcpi.cli.get_catalog") as mock_get_catalog:
            mock_get_catalog.return_value = self.mock_catalog
            self.mock_catalog.get_server.return_value = None

            result = self.runner.invoke(main, ["info", "nonexistent-server"])

            assert result.exit_code == 1
            assert "not found" in result.output

    def test_status_command_no_servers_configured(self):
        """Test status command when no servers are configured.

        Targets edge cases in status display.
        """
        with patch("mcpi.cli.create_default_manager") as mock_manager_fn:
            mock_manager_fn.return_value = self.mock_manager
            self.mock_manager.get_status_summary.return_value = {
                "default_client": "claude-code",
                "available_clients": ["claude-code"],
                "total_servers": 0,
                "server_states": {},
                "registry_stats": {"total_clients": 1, "loaded_instances": 1},
            }

            result = self.runner.invoke(main, ["status"])

            assert result.exit_code == 0
            # Should handle empty servers gracefully
            assert len(result.output) > 0

    def test_registry_search_with_empty_results(self):
        """Test search with no results.

        Targets empty search results handling.
        """
        with patch("mcpi.cli.get_catalog") as mock_get_catalog:
            mock_get_catalog.return_value = self.mock_catalog
            self.mock_catalog.search_servers.return_value = []

            result = self.runner.invoke(main, ["search", "-q", "nonexistent"])

            assert result.exit_code == 0
            # Should handle empty results gracefully
