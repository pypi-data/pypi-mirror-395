"""Tests for file-based scope handlers."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest
import yaml

from mcpi.clients.file_based import (
    CommandBasedScope,
    CommandLineExecutor,
    FileBasedScope,
    JSONFileReader,
    JSONFileWriter,
    YAMLSchemaValidator,
)
from mcpi.clients.types import ScopeConfig, ServerConfig


class TestJSONFileReader:
    """Test JSONFileReader class."""

    def test_read_existing_file(self):
        """Test reading an existing JSON file."""
        data = {"test": "value", "number": 42}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            temp_path = Path(f.name)

        try:
            reader = JSONFileReader()
            result = reader.read(temp_path)
            assert result == data
        finally:
            temp_path.unlink()

    def test_read_nonexistent_file(self):
        """Test reading a non-existent file returns empty dict."""
        reader = JSONFileReader()
        nonexistent = Path("/nonexistent/file.json")
        result = reader.read(nonexistent)
        assert result == {}

    def test_read_invalid_json(self):
        """Test reading invalid JSON raises ValueError."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            temp_path = Path(f.name)

        try:
            reader = JSONFileReader()
            with pytest.raises(ValueError, match="Failed to read"):
                reader.read(temp_path)
        finally:
            temp_path.unlink()


class TestJSONFileWriter:
    """Test JSONFileWriter class."""

    def test_write_file(self):
        """Test writing JSON data to file."""
        data = {"test": "value", "list": [1, 2, 3]}

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "test.json"

            writer = JSONFileWriter()
            result = writer.write(temp_path, data)

            assert result is True
            assert temp_path.exists()

            # Verify content
            with temp_path.open("r") as f:
                written_data = json.load(f)
            assert written_data == data

    def test_write_creates_directories(self):
        """Test that writing creates parent directories."""
        data = {"test": "value"}

        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = Path(temp_dir) / "nested" / "dir" / "test.json"

            writer = JSONFileWriter()
            result = writer.write(nested_path, data)

            assert result is True
            assert nested_path.exists()
            assert nested_path.parent.exists()

    def test_write_permission_error(self):
        """Test handling of permission errors."""
        data = {"test": "value"}
        invalid_path = Path("/invalid/permission/path.json")

        writer = JSONFileWriter()
        with pytest.raises(ValueError, match="Failed to write"):
            writer.write(invalid_path, data)


class TestYAMLSchemaValidator:
    """Test YAMLSchemaValidator class."""

    def test_validate_with_valid_data(self):
        """Test validation with valid data."""
        schema_data = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
            "required": ["name"],
        }

        test_data = {"name": "John", "age": 30}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(schema_data, f)
            schema_path = Path(f.name)

        try:
            validator = YAMLSchemaValidator()
            result = validator.validate(test_data, schema_path)
            assert result is True
            assert validator.get_errors() == []
        finally:
            schema_path.unlink()

    def test_validate_with_invalid_data(self):
        """Test validation with invalid data."""
        schema_data = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
            "required": ["name"],
        }

        test_data = {"age": 30}  # Missing required 'name'

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(schema_data, f)
            schema_path = Path(f.name)

        try:
            validator = YAMLSchemaValidator()
            result = validator.validate(test_data, schema_path)
            assert result is False
            errors = validator.get_errors()
            assert len(errors) > 0
            assert "name" in errors[0] or "required" in errors[0]
        finally:
            schema_path.unlink()

    def test_validate_nonexistent_schema(self):
        """Test validation with non-existent schema file."""
        validator = YAMLSchemaValidator()
        nonexistent = Path("/nonexistent/schema.yaml")

        result = validator.validate({}, nonexistent)
        assert result is False
        errors = validator.get_errors()
        assert len(errors) > 0
        assert "not found" in errors[0]


class TestCommandLineExecutor:
    """Test CommandLineExecutor class."""

    def test_execute_successful_command(self):
        """Test executing a successful command."""
        executor = CommandLineExecutor()
        result = executor.execute("echo", ["hello", "world"])

        assert result["success"] is True
        assert result["returncode"] == 0
        assert "hello world" in result["stdout"]
        assert result["stderr"] == ""

    def test_execute_failing_command(self):
        """Test executing a failing command."""
        executor = CommandLineExecutor()
        result = executor.execute("false", [])  # 'false' command always fails

        assert result["success"] is False
        assert result["returncode"] != 0

    @pytest.mark.skip(reason="Platform-specific command availability")
    def test_execute_nonexistent_command(self):
        """Test executing a non-existent command."""
        executor = CommandLineExecutor()
        with pytest.raises(ValueError, match="Command execution failed"):
            executor.execute("nonexistent_command_12345", [])


class TestFileBasedScope:
    """Test FileBasedScope class."""

    def test_file_based_scope_creation(self):
        """Test FileBasedScope creation."""
        config = ScopeConfig(
            name="test-scope",
            description="Test scope",
            priority=1,
            path=Path("/test/path.json"),
        )

        scope = FileBasedScope(config)
        assert scope.config == config
        assert scope.path == Path("/test/path.json")
        assert isinstance(scope.reader, JSONFileReader)
        assert isinstance(scope.writer, JSONFileWriter)

    def test_file_based_scope_without_path(self):
        """Test FileBasedScope creation without path raises error."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        with pytest.raises(ValueError, match="requires a path"):
            FileBasedScope(config)

    def test_exists_with_existing_file(self):
        """Test exists() method with existing file."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        try:
            config = ScopeConfig(
                name="test-scope", description="Test scope", priority=1, path=temp_path
            )

            scope = FileBasedScope(config)
            assert scope.exists() is True
        finally:
            temp_path.unlink()

    def test_exists_with_nonexistent_file(self):
        """Test exists() method with non-existent file."""
        config = ScopeConfig(
            name="test-scope",
            description="Test scope",
            priority=1,
            path=Path("/nonexistent/file.json"),
        )

        scope = FileBasedScope(config)
        assert scope.exists() is False

    def test_get_servers_empty_file(self):
        """Test get_servers() with non-existent file."""
        config = ScopeConfig(
            name="test-scope",
            description="Test scope",
            priority=1,
            path=Path("/nonexistent/file.json"),
        )

        scope = FileBasedScope(config)
        servers = scope.get_servers()
        assert servers == {}

    def test_get_servers_with_data(self):
        """Test get_servers() with existing data."""
        data = {
            "mcpServers": {
                "server1": {"command": "python", "args": ["-m", "server1"]},
                "server2": {"command": "node", "args": ["server2.js"]},
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            temp_path = Path(f.name)

        try:
            config = ScopeConfig(
                name="test-scope", description="Test scope", priority=1, path=temp_path
            )

            scope = FileBasedScope(config)
            servers = scope.get_servers()
            assert servers == data["mcpServers"]
        finally:
            temp_path.unlink()

    def test_add_server_new_file(self):
        """Test adding server to new file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "new_file.json"

            config = ScopeConfig(
                name="test-scope", description="Test scope", priority=1, path=temp_path
            )

            scope = FileBasedScope(config)
            server_config = ServerConfig(command="python", args=["-m", "test"])

            result = scope.add_server("test-server", server_config)

            assert result.success
            assert temp_path.exists()

            # Verify content
            with temp_path.open("r") as f:
                data = json.load(f)

            assert "mcpServers" in data
            assert "test-server" in data["mcpServers"]
            assert data["mcpServers"]["test-server"]["command"] == "python"

    def test_add_server_existing_file(self):
        """Test adding server to existing file."""
        initial_data = {
            "mcpServers": {
                "existing-server": {"command": "node", "args": ["existing.js"]}
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(initial_data, f)
            temp_path = Path(f.name)

        try:
            config = ScopeConfig(
                name="test-scope", description="Test scope", priority=1, path=temp_path
            )

            scope = FileBasedScope(config)
            server_config = ServerConfig(command="python", args=["-m", "new"])

            result = scope.add_server("new-server", server_config)

            assert result.success

            # Verify content
            with temp_path.open("r") as f:
                data = json.load(f)

            assert len(data["mcpServers"]) == 2
            assert "existing-server" in data["mcpServers"]
            assert "new-server" in data["mcpServers"]
            assert data["mcpServers"]["new-server"]["command"] == "python"
        finally:
            temp_path.unlink()

    def test_add_server_duplicate(self):
        """Test adding duplicate server fails."""
        initial_data = {
            "mcpServers": {
                "existing-server": {"command": "node", "args": ["existing.js"]}
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(initial_data, f)
            temp_path = Path(f.name)

        try:
            config = ScopeConfig(
                name="test-scope", description="Test scope", priority=1, path=temp_path
            )

            scope = FileBasedScope(config)
            server_config = ServerConfig(command="python", args=["-m", "test"])

            result = scope.add_server("existing-server", server_config)

            assert not result.success
            assert "already exists" in result.message
        finally:
            temp_path.unlink()

    def test_remove_server_success(self):
        """Test successful server removal."""
        initial_data = {
            "mcpServers": {
                "server1": {"command": "python", "args": ["-m", "server1"]},
                "server2": {"command": "node", "args": ["server2.js"]},
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(initial_data, f)
            temp_path = Path(f.name)

        try:
            config = ScopeConfig(
                name="test-scope", description="Test scope", priority=1, path=temp_path
            )

            scope = FileBasedScope(config)
            result = scope.remove_server("server1")

            assert result.success

            # Verify content
            with temp_path.open("r") as f:
                data = json.load(f)

            assert len(data["mcpServers"]) == 1
            assert "server1" not in data["mcpServers"]
            assert "server2" in data["mcpServers"]
        finally:
            temp_path.unlink()

    def test_remove_server_not_found(self):
        """Test removing non-existent server."""
        initial_data = {
            "mcpServers": {"server1": {"command": "python", "args": ["-m", "server1"]}}
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(initial_data, f)
            temp_path = Path(f.name)

        try:
            config = ScopeConfig(
                name="test-scope", description="Test scope", priority=1, path=temp_path
            )

            scope = FileBasedScope(config)
            result = scope.remove_server("nonexistent-server")

            assert not result.success
            assert "not found" in result.message
        finally:
            temp_path.unlink()


class TestCommandBasedScope:
    """Test CommandBasedScope class."""

    def test_command_based_scope_creation(self):
        """Test CommandBasedScope creation."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        executor = Mock()
        scope = CommandBasedScope(
            config=config,
            executor=executor,
            list_command="list",
            list_args=["--json"],
            add_command="add",
            add_args_template=["{server_id}", "{config_json}"],
            remove_command="remove",
            remove_args_template=["{server_id}"],
        )

        assert scope.config == config
        assert scope.executor == executor
        assert scope.list_command == "list"
        assert scope.add_command == "add"
        assert scope.update_command == "add"  # Should default to add_command
        assert scope.update_args_template == [
            "{server_id}",
            "{config_json}",
        ]  # Should default to add_args_template

    def test_exists_always_true(self):
        """Test exists() always returns True for command-based scopes."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        executor = Mock()
        scope = CommandBasedScope(
            config=config,
            executor=executor,
            list_command="list",
            list_args=[],
            add_command="add",
            add_args_template=[],
            remove_command="remove",
            remove_args_template=[],
        )

        assert scope.exists() is True

    def test_get_servers_success(self):
        """Test get_servers() with successful command execution."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        mock_output = {
            "mcpServers": {
                "server1": {"command": "python", "args": ["-m", "server1"]},
                "server2": {"command": "node", "args": ["server2.js"]},
            }
        }

        executor = Mock()
        executor.execute.return_value = {
            "success": True,
            "stdout": json.dumps(mock_output),
            "stderr": "",
            "returncode": 0,
        }

        scope = CommandBasedScope(
            config=config,
            executor=executor,
            list_command="list",
            list_args=["--json"],
            add_command="add",
            add_args_template=[],
            remove_command="remove",
            remove_args_template=[],
        )

        servers = scope.get_servers()
        assert servers == mock_output["mcpServers"]
        executor.execute.assert_called_once_with("list", ["--json"])

    def test_get_servers_command_failure(self):
        """Test get_servers() with command failure."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        executor = Mock()
        executor.execute.return_value = {
            "success": False,
            "stdout": "",
            "stderr": "Command failed",
            "returncode": 1,
        }

        scope = CommandBasedScope(
            config=config,
            executor=executor,
            list_command="list",
            list_args=[],
            add_command="add",
            add_args_template=[],
            remove_command="remove",
            remove_args_template=[],
        )

        servers = scope.get_servers()
        assert servers == {}

    def test_add_server_success(self):
        """Test add_server() with successful command execution."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        executor = Mock()
        executor.execute.return_value = {
            "success": True,
            "stdout": "Server added successfully",
            "stderr": "",
            "returncode": 0,
        }

        scope = CommandBasedScope(
            config=config,
            executor=executor,
            list_command="list",
            list_args=[],
            add_command="add",
            add_args_template=["{server_id}", "{config_json}"],
            remove_command="remove",
            remove_args_template=[],
        )

        server_config = ServerConfig(command="python", args=["-m", "test"])
        result = scope.add_server("test-server", server_config)

        assert result.success
        assert "Added server" in result.message

        # Verify the executor was called with formatted arguments
        expected_config_json = json.dumps(server_config.to_dict())
        executor.execute.assert_called_once_with(
            "add", ["test-server", expected_config_json]
        )

    def test_remove_server_success(self):
        """Test remove_server() with successful command execution."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        executor = Mock()
        executor.execute.return_value = {
            "success": True,
            "stdout": "Server removed successfully",
            "stderr": "",
            "returncode": 0,
        }

        scope = CommandBasedScope(
            config=config,
            executor=executor,
            list_command="list",
            list_args=[],
            add_command="add",
            add_args_template=[],
            remove_command="remove",
            remove_args_template=["{server_id}"],
        )

        result = scope.remove_server("test-server")

        assert result.success
        assert "Removed server" in result.message
        executor.execute.assert_called_once_with("remove", ["test-server"])

    def test_update_server_success(self):
        """Test update_server() with successful command execution."""
        config = ScopeConfig(name="test-scope", description="Test scope", priority=1)

        executor = Mock()
        executor.execute.return_value = {
            "success": True,
            "stdout": "Server updated successfully",
            "stderr": "",
            "returncode": 0,
        }

        scope = CommandBasedScope(
            config=config,
            executor=executor,
            list_command="list",
            list_args=[],
            add_command="add",
            add_args_template=["{server_id}", "{config_json}"],
            remove_command="remove",
            remove_args_template=[],
            update_command="update",
            update_args_template=["{server_id}", "update", "{config_json}"],
        )

        server_config = ServerConfig(command="python", args=["-m", "test"])
        result = scope.update_server("test-server", server_config)

        assert result.success
        assert "Updated server" in result.message

        # Verify the executor was called with update command and formatted arguments
        expected_config_json = json.dumps(server_config.to_dict())
        executor.execute.assert_called_once_with(
            "update", ["test-server", "update", expected_config_json]
        )
