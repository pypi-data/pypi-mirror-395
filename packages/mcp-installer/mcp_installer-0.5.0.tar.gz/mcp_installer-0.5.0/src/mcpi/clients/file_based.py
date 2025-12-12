"""File-based configuration scope handlers."""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jsonschema import ValidationError, validate

from .base import ScopeHandler
from .file_move_enable_disable_handler import FileMoveEnableDisableHandler
from .protocols import (
    CommandExecutor,
    ConfigReader,
    ConfigWriter,
    EnableDisableHandler,
    SchemaValidator,
)
from .types import OperationResult, ScopeConfig, ServerConfig


class JSONFileReader:
    """JSON file reader implementation."""

    def read(self, source: Path) -> Dict[str, Any]:
        """Read JSON from file.

        Args:
            source: Path to JSON file

        Returns:
            Parsed JSON data

        Raises:
            ValueError: If file cannot be read or parsed
        """
        if not source.exists():
            return {}

        try:
            with source.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to read {source}: {e}") from e


class JSONFileWriter:
    """JSON file writer implementation."""

    def write(self, target: Path, data: Dict[str, Any]) -> bool:
        """Write JSON to file.

        Args:
            target: Path to output file
            data: Data to write

        Returns:
            True if successful

        Raises:
            ValueError: If file cannot be written
        """
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except OSError as e:
            raise ValueError(f"Failed to write {target}: {e}") from e


class YAMLSchemaValidator:
    """YAML-based JSON schema validator."""

    def __init__(self) -> None:
        """Initialize validator."""
        self._errors: List[str] = []

    def validate(self, data: Dict[str, Any], schema_path: Path) -> bool:
        """Validate data against YAML schema.

        Args:
            data: Data to validate
            schema_path: Path to YAML schema file

        Returns:
            True if validation passes, False otherwise
        """
        self._errors = []

        if not schema_path.exists():
            self._errors.append(f"Schema file not found: {schema_path}")
            return False

        try:
            with schema_path.open("r", encoding="utf-8") as f:
                schema = yaml.safe_load(f)

            validate(instance=data, schema=schema)
            return True
        except ValidationError as e:
            self._errors.append(f"Validation error: {e.message}")
            return False
        except Exception as e:
            self._errors.append(f"Schema validation failed: {e}")
            return False

    def get_errors(self) -> List[str]:
        """Get validation errors from last validation attempt.

        Returns:
            List of error messages
        """
        return self._errors.copy()


class CommandLineExecutor:
    """Command line executor implementation."""

    def execute(self, command: str, args: List[str]) -> Dict[str, Any]:
        """Execute command with arguments.

        Args:
            command: Command to execute
            args: Command arguments

        Returns:
            Command result with stdout, stderr, and return code

        Raises:
            ValueError: If command execution fails
        """
        try:
            result = subprocess.run(
                [command] + args, capture_output=True, text=True, timeout=30
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired as e:
            raise ValueError(f"Command timed out: {e}") from e
        except subprocess.SubprocessError as e:
            raise ValueError(f"Command execution failed: {e}") from e


class FileBasedScope(ScopeHandler):
    """File-based configuration scope handler."""

    def __init__(
        self,
        config: ScopeConfig,
        reader: Optional[ConfigReader] = None,
        writer: Optional[ConfigWriter] = None,
        validator: Optional[SchemaValidator] = None,
        schema_path: Optional[Path] = None,
        enable_disable_handler: Optional[EnableDisableHandler] = None,
    ) -> None:
        """Initialize file-based scope handler.

        Args:
            config: Scope configuration
            reader: Configuration reader (defaults to JSONFileReader)
            writer: Configuration writer (defaults to JSONFileWriter)
            validator: Schema validator (optional)
            schema_path: Path to schema file (optional)
            enable_disable_handler: Handler for enable/disable operations (optional)
        """
        super().__init__(config)

        if not config.path:
            raise ValueError(f"File-based scope {config.name} requires a path")

        self.path = config.path.expanduser()
        self.reader = reader or JSONFileReader()
        self.writer = writer or JSONFileWriter()
        self.validator = validator
        self.schema_path = schema_path
        self.enable_disable_handler = enable_disable_handler

    def exists(self) -> bool:
        """Check if configuration file exists.

        Returns:
            True if file exists, False otherwise
        """
        return self.path.exists()

    def get_servers(self) -> Dict[str, Dict[str, Any]]:
        """Get all servers from this scope.

        For scopes using FileMoveEnableDisableHandler, this returns servers from
        BOTH the active file AND the disabled file. This ensures that `mcpi list`
        shows all servers (enabled + disabled) with correct states.

        Returns:
            Dictionary mapping server IDs to their configurations
        """
        if not self.exists():
            return {}

        try:
            # Get servers from active file
            data = self.reader.read(self.path)
            servers = data.get("mcpServers", {})

            # If using FileMoveEnableDisableHandler, also include disabled servers
            # Only FileMoveEnableDisableHandler stores server configs in separate files
            # (ApprovalRequiredEnableDisableHandler stores IDs in arrays, not configs)
            if isinstance(self.enable_disable_handler, FileMoveEnableDisableHandler):
                disabled_servers = self.enable_disable_handler.get_disabled_servers()
                # Merge disabled servers into the result
                # Note: We preserve the configuration from disabled file
                servers.update(disabled_servers)

            return servers
        except Exception:
            return {}

    def get_server_config(self, server_id: str) -> Dict[str, Any]:
        """Get the full configuration for a specific server.

        Args:
            server_id: The ID of the server to retrieve

        Returns:
            Dictionary with full server configuration

        Raises:
            ValueError: If server doesn't exist in this scope
        """
        servers = self.get_servers()
        if server_id not in servers:
            raise ValueError(
                f"Server '{server_id}' not found in scope '{self.config.name}'"
            )

        server_data = servers[server_id]
        return server_data

    def add_server(self, server_id: str, config: ServerConfig) -> OperationResult:
        """Add a server to this scope.

        Args:
            server_id: Unique server identifier
            config: Server configuration

        Returns:
            Operation result
        """
        try:
            # Load existing data or create new structure
            data = self.reader.read(self.path) if self.exists() else {}

            if "mcpServers" not in data:
                data["mcpServers"] = {}

            # Check if server already exists
            if server_id in data["mcpServers"]:
                return OperationResult.failure_result(
                    f"Server '{server_id}' already exists in scope '{self.config.name}'"
                )

            # Add server configuration
            data["mcpServers"][server_id] = config.to_dict()

            # Validate against schema if available
            if self.validator and self.schema_path:
                if not self.validator.validate(data, self.schema_path):
                    errors = self.validator.get_errors()
                    return OperationResult.failure_result(
                        f"Schema validation failed: {'; '.join(errors)}", errors=errors
                    )

            # Write the updated configuration
            self.writer.write(self.path, data)

            return OperationResult.success_result(
                f"Added server '{server_id}' to scope '{self.config.name}'",
                scope=self.config.name,
                server_id=server_id,
                path=str(self.path),
            )

        except Exception as e:
            return OperationResult.failure_result(
                f"Failed to add server: {e}", errors=[str(e)]
            )

    def remove_server(self, server_id: str) -> OperationResult:
        """Remove a server from this scope.

        Args:
            server_id: Server identifier to remove

        Returns:
            Operation result
        """
        if not self.exists():
            return OperationResult.failure_result(
                f"Configuration file does not exist: {self.path}"
            )

        try:
            data = self.reader.read(self.path)

            if "mcpServers" not in data or server_id not in data["mcpServers"]:
                return OperationResult.failure_result(
                    f"Server '{server_id}' not found in scope '{self.config.name}'"
                )

            # Remove the server
            del data["mcpServers"][server_id]

            # Write the updated configuration
            self.writer.write(self.path, data)

            return OperationResult.success_result(
                f"Removed server '{server_id}' from scope '{self.config.name}'",
                scope=self.config.name,
                server_id=server_id,
                path=str(self.path),
            )

        except Exception as e:
            return OperationResult.failure_result(
                f"Failed to remove server: {e}", errors=[str(e)]
            )

    def update_server(self, server_id: str, config: ServerConfig) -> OperationResult:
        """Update an existing server configuration.

        Args:
            server_id: Server identifier to update
            config: New server configuration

        Returns:
            Operation result
        """
        if not self.exists():
            return OperationResult.failure_result(
                f"Configuration file does not exist: {self.path}"
            )

        try:
            data = self.reader.read(self.path)

            if "mcpServers" not in data or server_id not in data["mcpServers"]:
                return OperationResult.failure_result(
                    f"Server '{server_id}' not found in scope '{self.config.name}'"
                )

            # Update server configuration
            data["mcpServers"][server_id] = config.to_dict()

            # Validate against schema if available
            if self.validator and self.schema_path:
                if not self.validator.validate(data, self.schema_path):
                    errors = self.validator.get_errors()
                    return OperationResult.failure_result(
                        f"Schema validation failed: {'; '.join(errors)}", errors=errors
                    )

            # Write the updated configuration
            self.writer.write(self.path, data)

            return OperationResult.success_result(
                f"Updated server '{server_id}' in scope '{self.config.name}'",
                scope=self.config.name,
                server_id=server_id,
                path=str(self.path),
            )

        except Exception as e:
            return OperationResult.failure_result(
                f"Failed to update server: {e}", errors=[str(e)]
            )


class CommandBasedScope(ScopeHandler):
    """Command-based configuration scope handler."""

    def __init__(
        self,
        config: ScopeConfig,
        executor: CommandExecutor,
        list_command: str,
        list_args: List[str],
        add_command: str,
        add_args_template: List[str],
        remove_command: str,
        remove_args_template: List[str],
        update_command: Optional[str] = None,
        update_args_template: Optional[List[str]] = None,
    ) -> None:
        """Initialize command-based scope handler.

        Args:
            config: Scope configuration
            executor: Command executor
            list_command: Command to list servers
            list_args: Arguments for list command
            add_command: Command to add servers
            add_args_template: Template for add command arguments (use {server_id}, {config_json})
            remove_command: Command to remove servers
            remove_args_template: Template for remove command arguments (use {server_id})
            update_command: Command to update servers (optional, defaults to add_command)
            update_args_template: Template for update command arguments (optional, defaults to add_args_template)
        """
        super().__init__(config)
        self.executor = executor
        self.list_command = list_command
        self.list_args = list_args
        self.add_command = add_command
        self.add_args_template = add_args_template
        self.remove_command = remove_command
        self.remove_args_template = remove_args_template
        self.update_command = update_command or add_command
        self.update_args_template = update_args_template or add_args_template

    def exists(self) -> bool:
        """Check if this scope is available.

        Returns:
            Always True for command-based scopes (availability checked by command execution)
        """
        return True

    def get_servers(self) -> Dict[str, Dict[str, Any]]:
        """Get all servers from this scope using command.

        Returns:
            Dictionary mapping server IDs to their configurations
        """
        try:
            result = self.executor.execute(self.list_command, self.list_args)

            if not result["success"]:
                return {}

            # Parse command output as JSON
            output = result["stdout"].strip()
            if not output:
                return {}

            data = json.loads(output)
            return data.get("mcpServers", {})

        except Exception:
            return {}

    def get_server_config(self, server_id: str) -> Dict[str, Any]:
        """Get the full configuration for a specific server.

        Args:
            server_id: The ID of the server to retrieve

        Returns:
            Dictionary with full server configuration

        Raises:
            ValueError: If server doesn't exist in this scope
        """
        servers = self.get_servers()
        if server_id not in servers:
            raise ValueError(
                f"Server '{server_id}' not found in scope '{self.config.name}'"
            )

        server_data = servers[server_id]
        return server_data

    def add_server(self, server_id: str, config: ServerConfig) -> OperationResult:
        """Add a server using command.

        Args:
            server_id: Unique server identifier
            config: Server configuration

        Returns:
            Operation result
        """
        try:
            # Format arguments using template
            config_json = json.dumps(config.to_dict())
            args = [
                arg.format(server_id=server_id, config_json=config_json)
                for arg in self.add_args_template
            ]

            result = self.executor.execute(self.add_command, args)

            if result["success"]:
                return OperationResult.success_result(
                    f"Added server '{server_id}' to scope '{self.config.name}'",
                    scope=self.config.name,
                    server_id=server_id,
                    command_output=result["stdout"],
                )
            else:
                return OperationResult.failure_result(
                    f"Command failed: {result['stderr']}", errors=[result["stderr"]]
                )

        except Exception as e:
            return OperationResult.failure_result(
                f"Failed to add server: {e}", errors=[str(e)]
            )

    def remove_server(self, server_id: str) -> OperationResult:
        """Remove a server using command.

        Args:
            server_id: Server identifier to remove

        Returns:
            Operation result
        """
        try:
            # Format arguments using template
            args = [
                arg.format(server_id=server_id) for arg in self.remove_args_template
            ]

            result = self.executor.execute(self.remove_command, args)

            if result["success"]:
                return OperationResult.success_result(
                    f"Removed server '{server_id}' from scope '{self.config.name}'",
                    scope=self.config.name,
                    server_id=server_id,
                    command_output=result["stdout"],
                )
            else:
                return OperationResult.failure_result(
                    f"Command failed: {result['stderr']}", errors=[result["stderr"]]
                )

        except Exception as e:
            return OperationResult.failure_result(
                f"Failed to remove server: {e}", errors=[str(e)]
            )

    def update_server(self, server_id: str, config: ServerConfig) -> OperationResult:
        """Update a server using command.

        Args:
            server_id: Server identifier to update
            config: New server configuration

        Returns:
            Operation result
        """
        try:
            # Format arguments using template
            config_json = json.dumps(config.to_dict())
            args = [
                arg.format(server_id=server_id, config_json=config_json)
                for arg in self.update_args_template
            ]

            result = self.executor.execute(self.update_command, args)

            if result["success"]:
                return OperationResult.success_result(
                    f"Updated server '{server_id}' in scope '{self.config.name}'",
                    scope=self.config.name,
                    server_id=server_id,
                    command_output=result["stdout"],
                )
            else:
                return OperationResult.failure_result(
                    f"Command failed: {result['stderr']}", errors=[result["stderr"]]
                )

        except Exception as e:
            return OperationResult.failure_result(
                f"Failed to update server: {e}", errors=[str(e)]
            )
