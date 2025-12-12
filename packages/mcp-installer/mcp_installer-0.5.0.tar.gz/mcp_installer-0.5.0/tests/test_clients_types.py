"""Tests for client types and data structures."""

from pathlib import Path

import pytest

from mcpi.clients.types import (
    OperationResult,
    ScopeConfig,
    ServerConfig,
    ServerInfo,
    ServerState,
)


class TestServerState:
    """Test ServerState enum."""

    def test_server_state_values(self):
        """Test ServerState enum values."""
        assert ServerState.ENABLED
        assert ServerState.DISABLED
        assert ServerState.NOT_INSTALLED

        # Test that they are different
        assert ServerState.ENABLED != ServerState.DISABLED
        assert ServerState.DISABLED != ServerState.NOT_INSTALLED


class TestScopeConfig:
    """Test ScopeConfig dataclass."""

    def test_scope_config_creation(self):
        """Test basic ScopeConfig creation."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        assert config.name == "test-scope"
        assert config.description == "Test scope"
        assert config.priority == 1
        assert config.path is None
        assert not config.is_user_level
        assert not config.is_project_level

    def test_scope_config_with_path(self):
        """Test ScopeConfig with path."""
        test_path = Path("/test/path")
        config = ScopeConfig(
            name="test-scope",
            description="Test scope",
            priority=1,
            path=test_path,
            is_user_level=True,
        )

        assert config.path == test_path
        assert config.is_user_level
        assert not config.is_project_level

    def test_scope_config_validation_error(self):
        """Test ScopeConfig validation for conflicting flags."""
        with pytest.raises(
            ValueError, match="cannot be both user-level and project-level"
        ):
            ScopeConfig(
                name="invalid-scope",
                description="Invalid scope",
                priority=1,
                is_user_level=True,
                is_project_level=True,
            )


class TestServerInfo:
    """Test ServerInfo dataclass."""

    def test_server_info_creation(self):
        """Test basic ServerInfo creation."""
        config = {"command": "test-command", "args": ["arg1", "arg2"]}
        info = ServerInfo(
            id="test-server", client="test-client", scope="test-scope", config=config
        )

        assert info.id == "test-server"
        assert info.client == "test-client"
        assert info.scope == "test-scope"
        assert info.config == config
        assert info.state == ServerState.ENABLED  # default
        assert info.priority == 0  # default

    def test_qualified_id(self):
        """Test qualified ID generation."""
        info = ServerInfo(
            id="test-server", client="claude-code", scope="user-mcp", config={}
        )

        assert info.qualified_id == "claude-code:user-mcp:test-server"

    def test_command_property(self):
        """Test command property extraction."""
        config = {"command": "python", "args": ["-m", "test"]}
        info = ServerInfo(
            id="test-server", client="test-client", scope="test-scope", config=config
        )

        assert info.command == "python"

    def test_args_property(self):
        """Test args property extraction."""
        config = {"command": "python", "args": ["-m", "test", "arg"]}
        info = ServerInfo(
            id="test-server", client="test-client", scope="test-scope", config=config
        )

        assert info.args == ["-m", "test", "arg"]

    def test_env_property(self):
        """Test env property extraction."""
        config = {"command": "python", "env": {"VAR1": "value1", "VAR2": "value2"}}
        info = ServerInfo(
            id="test-server", client="test-client", scope="test-scope", config=config
        )

        assert info.env == {"VAR1": "value1", "VAR2": "value2"}

    def test_missing_properties(self):
        """Test handling of missing properties."""
        config = {}  # Empty config
        info = ServerInfo(
            id="test-server", client="test-client", scope="test-scope", config=config
        )

        assert info.command is None
        assert info.args == []
        assert info.env == {}


class TestServerConfig:
    """Test ServerConfig dataclass."""

    def test_server_config_creation(self):
        """Test basic ServerConfig creation."""
        config = ServerConfig(command="python")

        assert config.command == "python"
        assert config.args == []
        assert config.env == {}
        assert config.type == "stdio"

    def test_server_config_with_all_fields(self):
        """Test ServerConfig with all fields."""
        config = ServerConfig(
            command="node",
            args=["server.js", "--port", "3000"],
            env={"NODE_ENV": "production"},
            type="websocket",
        )

        assert config.command == "node"
        assert config.args == ["server.js", "--port", "3000"]
        assert config.env == {"NODE_ENV": "production"}
        assert config.type == "websocket"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = ServerConfig(
            command="python", args=["-m", "server"], env={"DEBUG": "1"}, type="stdio"
        )

        result = config.to_dict()
        expected = {
            "command": "python",
            "args": ["-m", "server"],
            "env": {"DEBUG": "1"},
            "type": "stdio",
        }

        assert result == expected

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "command": "npm",
            "args": ["start"],
            "env": {"PORT": "8080"},
            "type": "http",
        }

        config = ServerConfig.from_dict(data)

        assert config.command == "npm"
        assert config.args == ["start"]
        assert config.env == {"PORT": "8080"}
        assert config.type == "http"

    def test_from_dict_minimal(self):
        """Test creation from minimal dictionary."""
        data = {"command": "test"}

        config = ServerConfig.from_dict(data)

        assert config.command == "test"
        assert config.args == []
        assert config.env == {}
        assert config.type == "stdio"


class TestOperationResult:
    """Test OperationResult dataclass."""

    def test_operation_result_creation(self):
        """Test basic OperationResult creation."""
        result = OperationResult(success=True, message="Operation completed")

        assert result.success
        assert result.message == "Operation completed"
        assert result.errors == []
        assert result.details == {}

    def test_success_result_factory(self):
        """Test success result factory method."""
        result = OperationResult.success_result(
            "Server added successfully", server_id="test-server", scope="test-scope"
        )

        assert result.success
        assert result.message == "Server added successfully"
        assert result.errors == []
        assert result.details == {"server_id": "test-server", "scope": "test-scope"}

    def test_failure_result_factory(self):
        """Test failure result factory method."""
        errors = ["Error 1", "Error 2"]
        result = OperationResult.failure_result("Operation failed", errors=errors)

        assert not result.success
        assert result.message == "Operation failed"
        assert result.errors == errors
        assert result.details == {}

    def test_failure_result_no_errors(self):
        """Test failure result without explicit errors."""
        result = OperationResult.failure_result("Simple failure")

        assert not result.success
        assert result.message == "Simple failure"
        assert result.errors == []
        assert result.details == {}
