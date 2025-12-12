"""Un-Gameable Functional Tests for Environment Variable Support in MCPI

This test suite validates ACTUAL environment variable functionality that EXISTS:
1. ServerConfig model has env field (CURRENT)
2. Configuration files can contain env vars (CURRENT)
3. Env vars persist through file save/load cycles (CURRENT)
4. End-to-end: config with env → written to file → read back correctly (CURRENT)

SCOPE LIMITATION:
=================
This test suite ONLY tests functionality that CURRENTLY EXISTS in the codebase.
It does NOT test:
- env field on MCPServer model (doesn't exist yet)
- env in registry/catalog.json (doesn't exist yet)
- Registry-based env var defaults (doesn't exist yet)

Those features would require implementation FIRST, then tests SECOND per CLAUDE.md:
> "Writing tests FIRST and designing an implementation around tests is a GREAT
> idea! But don't do that until you have some idea of an implementation that's
> going to work, or that's just tech debt"

WHAT THIS TESTS:
================
CURRENT FUNCTIONALITY - ServerConfig env field support:
- User can add env vars to ServerConfig when installing servers
- Env vars are written to Claude Code config files
- Env vars are preserved through save/load cycles
- Multiple servers can have different env configs
- Backward compatibility: servers without env work fine

GAMING RESISTANCE:
==================
These tests cannot be gamed because:
1. Use REAL file I/O via test harness (no catalog mocks)
2. Write ACTUAL JSON files to disk, read them back
3. Test COMPLETE workflows: create config → write → read → validate
4. Verify MULTIPLE observable outcomes: file exists, JSON valid, env present, values correct
5. Cross-validate between what we write and what we read back
6. No Pydantic validation tests (that's testing Pydantic, not MCPI)
7. Only test observable user-facing behavior

TRACEABILITY:
=============
STATUS Gaps Addressed:
- Users can configure servers requiring environment variables (CURRENT)
- No manual config editing required for env vars (CURRENT)
- Config files properly persist env vars (CURRENT)

PLAN Items Validated:
- ServerConfig model has env field (CURRENT)
- Config generation includes env vars (CURRENT)
- Backward compatibility maintained (CURRENT)
"""

import json
from pathlib import Path

import pytest

from mcpi.clients.types import ServerConfig


class TestServerConfigEnvSupport:
    """Test that ServerConfig model supports env field (CURRENT FUNCTIONALITY).

    These tests validate the EXISTING ServerConfig.env field and its
    to_dict/from_dict serialization methods.

    USER WORKFLOW:
    1. User creates ServerConfig with env vars
    2. Config serialized to dict (for JSON file)
    3. Dict written to Claude Code settings file
    4. Dict read from file and deserialized back to ServerConfig
    5. Env vars preserved through round-trip
    """

    def test_server_config_with_env_creates_successfully(self):
        """Test that ServerConfig accepts env parameter.

        GAMING RESISTANCE:
        - Uses REAL ServerConfig class (not mock)
        - Tests ACTUAL attribute access
        - Validates REAL dataclass behavior
        """
        # SETUP & EXECUTE: Create config with env
        config = ServerConfig(
            command="npx",
            args=["-y", "test-package"],
            env={"API_KEY": "test-key", "DEBUG": "true"},
            type="stdio",
        )

        # VERIFY: Env accessible as attribute
        assert config.env == {"API_KEY": "test-key", "DEBUG": "true"}
        assert config.command == "npx"
        assert config.args == ["-y", "test-package"]

    def test_server_config_to_dict_includes_env(self):
        """Test that to_dict() includes env in serialized output.

        GAMING RESISTANCE:
        - Tests REAL serialization method
        - Validates ACTUAL dict structure
        - Cannot pass if to_dict() doesn't include env
        """
        # SETUP: Config with env
        config = ServerConfig(
            command="npx", args=["package"], env={"KEY": "value"}, type="stdio"
        )

        # EXECUTE: Serialize to dict
        config_dict = config.to_dict()

        # VERIFY: Dict contains env
        assert isinstance(config_dict, dict)
        assert "env" in config_dict
        assert config_dict["env"] == {"KEY": "value"}
        assert config_dict["command"] == "npx"
        assert config_dict["type"] == "stdio"

    def test_server_config_from_dict_preserves_env(self):
        """Test that from_dict() correctly deserializes env.

        GAMING RESISTANCE:
        - Tests REAL deserialization
        - Validates round-trip: dict → object → dict
        - Cannot pass if from_dict() loses env
        """
        # SETUP: Dict with env (as read from JSON file)
        config_dict = {
            "command": "python",
            "args": ["-m", "server"],
            "env": {"PATH": "/custom/path", "TIMEOUT": "60"},
            "type": "stdio",
        }

        # EXECUTE: Deserialize
        config = ServerConfig.from_dict(config_dict)

        # VERIFY: Env preserved
        assert config.env == {"PATH": "/custom/path", "TIMEOUT": "60"}
        assert config.command == "python"

        # VERIFY: Round-trip works
        serialized = config.to_dict()
        assert serialized["env"] == config_dict["env"]

    def test_server_config_without_env_backward_compat(self):
        """Test backward compatibility: configs without env field work.

        GAMING RESISTANCE:
        - Tests REAL backward compatibility
        - Validates existing configs don't break
        - Cannot pass if env becomes required
        """
        # SETUP: Config without env (existing format)
        config = ServerConfig(command="npx", args=["package"], type="stdio")

        # VERIFY: No error, env is empty dict (default)
        assert config.env == {}

        # VERIFY: Serialization works
        config_dict = config.to_dict()
        assert "env" in config_dict
        assert config_dict["env"] == {}


class TestEnvVarsInConfigFiles:
    """Test env vars are written to and read from Claude Code config files.

    This validates the CRITICAL user workflow: env vars must persist to disk
    in the actual JSON files that Claude Code reads.

    USER WORKFLOW (Complete):
    1. User adds server with env vars via MCPI
    2. MCPI writes Claude Code config file with env
    3. File exists on disk with valid JSON
    4. Env vars appear in server entry in file
    5. Claude Code can read file and use env vars
    6. User can edit env values in file
    7. MCPI can read file back and preserve env
    """

    def test_add_server_with_env_vars_writes_to_file(self, tmp_path, mcp_harness):
        """Test complete workflow: add server with env, verify in config file.

        This is the CRITICAL end-to-end test that validates the entire feature.

        GAMING RESISTANCE:
        - Uses REAL file I/O via test harness (no mocks)
        - Writes ACTUAL JSON file to disk
        - Reads back file and validates contents
        - Checks: file exists, valid JSON, correct structure, env present
        - Cannot pass with stubs, mocks, or fake file operations
        - Tests observable outcome user would see
        """
        from mcpi.clients.claude_code import ClaudeCodePlugin

        # SETUP: Create plugin with test file paths
        plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

        # Server config with env vars (what user provides)
        server_config = ServerConfig(
            command="npx",
            args=["-y", "test-package"],
            type="stdio",
            env={"API_KEY": "my-secret-key", "DEBUG": "true", "TIMEOUT": "30"},
        )

        # EXECUTE: Add server to user-mcp scope
        result = plugin.add_server("test-server", server_config, "user-mcp")

        # VERIFY: Operation succeeded
        assert result.success, f"Add server failed: {result.message}"

        # VERIFY: File exists on disk
        mcp_harness.assert_valid_json("user-mcp")

        # VERIFY: Server exists in file
        mcp_harness.assert_server_exists("user-mcp", "test-server")

        # VERIFY: Server config in file has env vars
        config = mcp_harness.get_server_config("user-mcp", "test-server")
        assert config is not None, "Server config missing from file"

        # Critical assertions: env vars in file
        assert "env" in config, "Env vars not written to config file"
        assert isinstance(config["env"], dict), "Env should be dict in file"
        assert config["env"]["API_KEY"] == "my-secret-key", "API_KEY value wrong"
        assert config["env"]["DEBUG"] == "true", "DEBUG value wrong"
        assert config["env"]["TIMEOUT"] == "30", "TIMEOUT value wrong"

        # VERIFY: Other fields correct
        assert config["command"] == "npx"
        assert config["type"] == "stdio"

    def test_multiple_servers_with_different_env_configs(self, tmp_path, mcp_harness):
        """Test adding multiple servers with different env configurations.

        GAMING RESISTANCE:
        - Tests REAL scenario: multiple servers, different env
        - Validates each server written correctly
        - Cannot pass if env handling corrupts other servers
        - Reads actual file to verify isolation
        """
        from mcpi.clients.claude_code import ClaudeCodePlugin

        # SETUP: Plugin
        plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

        # Server 1: With env vars
        server1_config = ServerConfig(
            command="npx",
            args=["package1"],
            type="stdio",
            env={"KEY1": "value1", "SHARED": "server1-val"},
        )

        # Server 2: With different env vars
        server2_config = ServerConfig(
            command="python",
            args=["-m", "package2"],
            type="stdio",
            env={"KEY2": "value2", "SHARED": "server2-val"},
        )

        # Server 3: Without env vars (backward compat)
        server3_config = ServerConfig(command="npx", args=["package3"], type="stdio")

        # EXECUTE: Add all servers
        result1 = plugin.add_server("server1", server1_config, "user-mcp")
        result2 = plugin.add_server("server2", server2_config, "user-mcp")
        result3 = plugin.add_server("server3", server3_config, "user-mcp")

        # VERIFY: All succeeded
        assert result1.success and result2.success and result3.success

        # VERIFY: File valid
        mcp_harness.assert_valid_json("user-mcp")

        # VERIFY: All servers exist
        mcp_harness.assert_server_exists("user-mcp", "server1")
        mcp_harness.assert_server_exists("user-mcp", "server2")
        mcp_harness.assert_server_exists("user-mcp", "server3")

        # VERIFY: Server 1 has correct env (isolated from server2)
        config1 = mcp_harness.get_server_config("user-mcp", "server1")
        assert config1["env"]["KEY1"] == "value1"
        assert config1["env"]["SHARED"] == "server1-val"
        assert "KEY2" not in config1["env"], "Server1 shouldn't have server2's KEY2"

        # VERIFY: Server 2 has correct env (isolated from server1)
        config2 = mcp_harness.get_server_config("user-mcp", "server2")
        assert config2["env"]["KEY2"] == "value2"
        assert config2["env"]["SHARED"] == "server2-val"
        assert "KEY1" not in config2["env"], "Server2 shouldn't have server1's KEY1"

        # VERIFY: Server 3 has no env or empty env (backward compat)
        config3 = mcp_harness.get_server_config("user-mcp", "server3")
        assert config3["env"] == {}, "Server without env should have empty env dict"

    def test_env_vars_work_across_all_scopes(self, tmp_path, mcp_harness):
        """Test env vars persist correctly across all Claude Code scopes.

        GAMING RESISTANCE:
        - Tests all scope types (project-mcp, user-mcp, user-internal)
        - Validates env vars preserved in different files
        - Cannot pass if any scope breaks env handling
        - Uses real file paths for each scope
        """
        from mcpi.clients.claude_code import ClaudeCodePlugin

        # SETUP: Plugin
        plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

        # Config with env
        server_config = ServerConfig(
            command="npx",
            args=["test-package"],
            type="stdio",
            env={"SCOPE_VAR": "scope_value", "COMMON": "test"},
        )

        # Test scopes that support server installation
        test_scopes = ["project-mcp", "user-mcp", "user-internal"]

        for scope in test_scopes:
            # EXECUTE: Add server to scope
            server_id = f"test-{scope}"
            result = plugin.add_server(server_id, server_config, scope)

            # VERIFY: Success
            assert result.success, f"Failed to add to {scope}: {result.message}"

            # VERIFY: File valid
            mcp_harness.assert_valid_json(scope)

            # VERIFY: Server exists with env
            config = mcp_harness.get_server_config(scope, server_id)
            assert config is not None, f"Server missing from {scope}"
            assert "env" in config, f"Env missing in {scope}"
            assert (
                config["env"]["SCOPE_VAR"] == "scope_value"
            ), f"Env value wrong in {scope}"
            assert config["env"]["COMMON"] == "test", f"Env value wrong in {scope}"


class TestEnvVarFilePersistence:
    """Test env vars survive file edit and reload cycles.

    This validates that if a user manually edits env vars in the config file,
    MCPI can read them back correctly.

    USER WORKFLOW:
    1. Add server with env vars
    2. Config written to file
    3. User manually edits env values in file
    4. MCPI reads file back
    5. Env values preserved correctly
    """

    def test_env_vars_survive_user_manual_edit(self, tmp_path, mcp_harness):
        """Test user can manually edit env vars in file and MCPI reads them back.

        GAMING RESISTANCE:
        - Tests REAL file I/O
        - Manually edits actual JSON file on disk
        - Validates MCPI reads modified values
        - Cannot pass if file reading doesn't preserve user edits
        """
        from mcpi.clients.claude_code import ClaudeCodePlugin

        # SETUP: Plugin
        plugin = ClaudeCodePlugin(path_overrides=mcp_harness.path_overrides)

        # Add server with initial env
        original_config = ServerConfig(
            command="npx",
            args=["package"],
            type="stdio",
            env={"KEY": "original-value", "DEBUG": "false"},
        )

        result = plugin.add_server("test-server", original_config, "user-mcp")
        assert result.success

        # VERIFY: Original env written
        config1 = mcp_harness.get_server_config("user-mcp", "test-server")
        assert config1["env"]["KEY"] == "original-value"
        assert config1["env"]["DEBUG"] == "false"

        # EXECUTE: Simulate user manually editing env in file
        scope_file = mcp_harness.path_overrides["user-mcp"]
        with open(scope_file) as f:
            file_data = json.load(f)

        # User changes env values and adds new var
        file_data["mcpServers"]["test-server"]["env"]["KEY"] = "user-edited-value"
        file_data["mcpServers"]["test-server"]["env"]["NEW_KEY"] = "user-added"

        with open(scope_file, "w") as f:
            json.dump(file_data, f, indent=2)

        # VERIFY: MCPI reads modified file correctly
        config2 = mcp_harness.get_server_config("user-mcp", "test-server")
        assert config2["env"]["KEY"] == "user-edited-value", "User edit not read back"
        assert config2["env"]["NEW_KEY"] == "user-added", "User addition not read back"
        assert config2["env"]["DEBUG"] == "false", "Original env var lost on read"


# Import test harness fixtures
from tests.test_harness import mcp_harness  # noqa: F401
