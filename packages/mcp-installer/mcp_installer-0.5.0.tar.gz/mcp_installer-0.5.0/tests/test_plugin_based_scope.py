"""Tests for plugin-based MCP server discovery."""

import json
import pytest
from pathlib import Path

from mcpi.clients.plugin_based import PluginBasedScope
from mcpi.clients.types import ScopeConfig, ServerConfig


@pytest.fixture
def temp_plugin_env(tmp_path):
    """Create a temporary plugin environment for testing."""
    # Create settings.json with enabled plugins
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    settings = {
        "enabledPlugins": {
            "test-plugin@test-marketplace": True,
            "disabled-plugin@test-marketplace": False,
            "missing-plugin@test-marketplace": True,
        }
    }
    settings_path = claude_dir / "settings.json"
    settings_path.write_text(json.dumps(settings))

    # Create installed_plugins.json
    plugins_dir = claude_dir / "plugins"
    plugins_dir.mkdir()

    # Create test plugin directory
    test_plugin_dir = plugins_dir / "marketplaces" / "test-marketplace" / "test-plugin"
    test_plugin_dir.mkdir(parents=True)

    claude_plugin_dir = test_plugin_dir / ".claude-plugin"
    claude_plugin_dir.mkdir()

    plugin_json = {
        "name": "test-plugin",
        "version": "1.0.0",
        "mcpServers": {
            "server1": {
                "command": "node",
                "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
                "env": {"API_KEY": "test123"},
            },
            "server2": {
                "command": "python",
                "args": ["-m", "server"],
                "env": {},
            },
        },
    }
    (claude_plugin_dir / "plugin.json").write_text(json.dumps(plugin_json))

    installed_plugins = {
        "version": 1,
        "plugins": {
            "test-plugin@test-marketplace": {
                "version": "1.0.0",
                "installPath": str(test_plugin_dir),
            },
            "disabled-plugin@test-marketplace": {
                "version": "1.0.0",
                "installPath": str(tmp_path / "nonexistent"),
            },
        },
    }
    (plugins_dir / "installed_plugins.json").write_text(json.dumps(installed_plugins))

    return {
        "root": tmp_path,
        "settings_path": settings_path,
        "installed_plugins_path": plugins_dir / "installed_plugins.json",
        "test_plugin_dir": test_plugin_dir,
    }


@pytest.fixture
def plugin_scope(temp_plugin_env):
    """Create a PluginBasedScope with test environment."""
    return PluginBasedScope(
        config=ScopeConfig(
            name="plugin",
            description="Test plugin scope",
            priority=0,
            path=temp_plugin_env["settings_path"],
            is_user_level=True,
        ),
        settings_path=temp_plugin_env["settings_path"],
        installed_plugins_path=temp_plugin_env["installed_plugins_path"],
    )


class TestPluginBasedScopeDiscovery:
    """Tests for plugin server discovery."""

    def test_discovers_enabled_plugin_servers(self, plugin_scope, temp_plugin_env):
        """Test that servers from enabled plugins are discovered."""
        servers = plugin_scope.get_servers()

        assert "test-plugin:server1" in servers
        assert "test-plugin:server2" in servers
        assert len(servers) == 2

    def test_server_config_preserved(self, plugin_scope):
        """Test that server configuration is preserved correctly."""
        servers = plugin_scope.get_servers()

        server1 = servers["test-plugin:server1"]
        assert server1["command"] == "node"
        assert server1["env"]["API_KEY"] == "test123"

    def test_plugin_root_variable_resolved(self, plugin_scope, temp_plugin_env):
        """Test that ${CLAUDE_PLUGIN_ROOT} is resolved to install path."""
        servers = plugin_scope.get_servers()

        server1 = servers["test-plugin:server1"]
        expected_path = str(temp_plugin_env["test_plugin_dir"]) + "/server.js"
        assert server1["args"][0] == expected_path

    def test_plugin_source_metadata_added(self, plugin_scope):
        """Test that plugin source metadata is added to config."""
        servers = plugin_scope.get_servers()

        server1 = servers["test-plugin:server1"]
        assert "_plugin_source" in server1
        assert server1["_plugin_source"]["plugin_name"] == "test-plugin"
        assert server1["_plugin_source"]["plugin_id"] == "test-plugin@test-marketplace"

    def test_disabled_plugins_ignored(self, plugin_scope):
        """Test that disabled plugins are not discovered."""
        servers = plugin_scope.get_servers()

        # Should not have any servers from disabled-plugin
        for server_id in servers:
            assert not server_id.startswith("disabled-plugin:")

    def test_missing_plugins_ignored(self, plugin_scope):
        """Test that plugins not in installed_plugins.json are ignored."""
        servers = plugin_scope.get_servers()

        # missing-plugin is enabled but not installed
        for server_id in servers:
            assert not server_id.startswith("missing-plugin:")


class TestPluginBasedScopeExists:
    """Tests for exists() method."""

    def test_exists_when_servers_found(self, plugin_scope):
        """Test exists() returns True when servers are discovered."""
        assert plugin_scope.exists() is True

    def test_exists_false_when_no_settings(self, tmp_path):
        """Test exists() returns False when settings.json doesn't exist."""
        scope = PluginBasedScope(
            config=ScopeConfig(
                name="plugin",
                description="Test",
                priority=0,
                path=tmp_path / "nonexistent.json",
                is_user_level=True,
            ),
            settings_path=tmp_path / "nonexistent.json",
            installed_plugins_path=tmp_path / "nonexistent2.json",
        )
        assert scope.exists() is False

    def test_exists_false_when_no_enabled_plugins(self, tmp_path):
        """Test exists() returns False when no plugins are enabled."""
        settings_path = tmp_path / "settings.json"
        settings_path.write_text(json.dumps({"enabledPlugins": {}}))

        scope = PluginBasedScope(
            config=ScopeConfig(
                name="plugin",
                description="Test",
                priority=0,
                path=settings_path,
                is_user_level=True,
            ),
            settings_path=settings_path,
            installed_plugins_path=tmp_path / "installed.json",
        )
        assert scope.exists() is False


class TestPluginBasedScopeReadOnly:
    """Tests for read-only operations."""

    def test_add_server_fails(self, plugin_scope):
        """Test that add_server returns failure."""
        result = plugin_scope.add_server(
            "new-server",
            ServerConfig(command="test", args=[], env={}),
        )
        assert result.success is False
        assert "plugin system" in result.message.lower()

    def test_remove_server_fails(self, plugin_scope):
        """Test that remove_server returns failure."""
        result = plugin_scope.remove_server("test-plugin:server1")
        assert result.success is False
        assert "plugin system" in result.message.lower()

    def test_update_server_fails(self, plugin_scope):
        """Test that update_server returns failure."""
        result = plugin_scope.update_server(
            "test-plugin:server1",
            ServerConfig(command="updated", args=[], env={}),
        )
        assert result.success is False
        assert "plugin system" in result.message.lower()


class TestPluginBasedScopeGetServerConfig:
    """Tests for get_server_config method."""

    def test_get_server_config_success(self, plugin_scope):
        """Test getting config for existing server."""
        config = plugin_scope.get_server_config("test-plugin:server1")
        assert config["command"] == "node"

    def test_get_server_config_not_found(self, plugin_scope):
        """Test getting config for non-existent server raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            plugin_scope.get_server_config("nonexistent:server")


class TestPluginBasedScopeCache:
    """Tests for server caching."""

    def test_cache_invalidation(self, plugin_scope, temp_plugin_env):
        """Test that cache can be invalidated."""
        # Get servers (populates cache)
        servers1 = plugin_scope.get_servers()
        assert len(servers1) == 2

        # Modify plugin.json to add a server
        plugin_json_path = (
            temp_plugin_env["test_plugin_dir"] / ".claude-plugin" / "plugin.json"
        )
        plugin_data = json.loads(plugin_json_path.read_text())
        plugin_data["mcpServers"]["server3"] = {
            "command": "new",
            "args": [],
            "env": {},
        }
        plugin_json_path.write_text(json.dumps(plugin_data))

        # Cache should still have old data
        servers2 = plugin_scope.get_servers()
        assert len(servers2) == 2

        # Invalidate cache
        plugin_scope.invalidate_cache()

        # Now should see new server
        servers3 = plugin_scope.get_servers()
        assert len(servers3) == 3
        assert "test-plugin:server3" in servers3


class TestPluginBasedScopeEdgeCases:
    """Tests for edge cases and error handling."""

    def test_malformed_plugin_json_ignored(self, tmp_path):
        """Test that malformed plugin.json files are gracefully ignored."""
        # Create settings with enabled plugin
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        settings = {"enabledPlugins": {"bad-plugin@test": True}}
        settings_path = claude_dir / "settings.json"
        settings_path.write_text(json.dumps(settings))

        # Create installed_plugins.json
        plugins_dir = claude_dir / "plugins"
        plugins_dir.mkdir()

        bad_plugin_dir = plugins_dir / "bad-plugin"
        bad_plugin_dir.mkdir()
        claude_plugin_dir = bad_plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        # Write malformed JSON
        (claude_plugin_dir / "plugin.json").write_text("{ invalid json }")

        installed = {
            "version": 1,
            "plugins": {"bad-plugin@test": {"installPath": str(bad_plugin_dir)}},
        }
        (plugins_dir / "installed_plugins.json").write_text(json.dumps(installed))

        scope = PluginBasedScope(
            config=ScopeConfig(
                name="plugin",
                description="Test",
                priority=0,
                path=settings_path,
                is_user_level=True,
            ),
            settings_path=settings_path,
            installed_plugins_path=plugins_dir / "installed_plugins.json",
        )

        # Should not raise, just return empty
        servers = scope.get_servers()
        assert len(servers) == 0

    def test_plugin_without_mcp_servers(self, tmp_path):
        """Test plugins without mcpServers field are handled gracefully."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        settings = {"enabledPlugins": {"no-mcp@test": True}}
        settings_path = claude_dir / "settings.json"
        settings_path.write_text(json.dumps(settings))

        plugins_dir = claude_dir / "plugins"
        plugins_dir.mkdir()

        plugin_dir = plugins_dir / "no-mcp"
        plugin_dir.mkdir()
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        # Plugin without mcpServers
        plugin_json = {"name": "no-mcp", "version": "1.0.0", "commands": ["cmd.md"]}
        (claude_plugin_dir / "plugin.json").write_text(json.dumps(plugin_json))

        installed = {
            "version": 1,
            "plugins": {"no-mcp@test": {"installPath": str(plugin_dir)}},
        }
        (plugins_dir / "installed_plugins.json").write_text(json.dumps(installed))

        scope = PluginBasedScope(
            config=ScopeConfig(
                name="plugin",
                description="Test",
                priority=0,
                path=settings_path,
                is_user_level=True,
            ),
            settings_path=settings_path,
            installed_plugins_path=plugins_dir / "installed_plugins.json",
        )

        servers = scope.get_servers()
        assert len(servers) == 0

    def test_has_server_method(self, plugin_scope):
        """Test has_server method works correctly."""
        assert plugin_scope.has_server("test-plugin:server1") is True
        assert plugin_scope.has_server("nonexistent:server") is False
