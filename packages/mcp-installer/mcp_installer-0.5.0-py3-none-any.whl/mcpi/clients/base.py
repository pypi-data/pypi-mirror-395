"""Abstract base classes for MCP client plugins."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .types import OperationResult, ScopeConfig, ServerConfig, ServerInfo, ServerState


class ScopeHandler(ABC):
    """Abstract handler for configuration scopes."""

    def __init__(self, config: ScopeConfig) -> None:
        """Initialize scope handler.

        Args:
            config: Scope configuration
        """
        self.config = config

    @abstractmethod
    def exists(self) -> bool:
        """Check if this scope's configuration exists.

        Returns:
            True if configuration exists, False otherwise
        """
        ...

    @abstractmethod
    def get_servers(self) -> Dict[str, Dict[str, Any]]:
        """Get all servers in this scope.

        Returns:
            Dictionary mapping server IDs to their configurations
        """
        ...

    @abstractmethod
    def add_server(self, server_id: str, config: ServerConfig) -> OperationResult:
        """Add a server to this scope.

        Args:
            server_id: Unique server identifier
            config: Server configuration

        Returns:
            Operation result
        """
        ...

    @abstractmethod
    def remove_server(self, server_id: str) -> OperationResult:
        """Remove a server from this scope.

        Args:
            server_id: Server identifier to remove

        Returns:
            Operation result
        """
        ...

    @abstractmethod
    def update_server(self, server_id: str, config: ServerConfig) -> OperationResult:
        """Update an existing server configuration.

        Args:
            server_id: Server identifier to update
            config: New server configuration

        Returns:
            Operation result
        """
        ...

    @abstractmethod
    def get_server_config(self, server_id: str) -> Dict[str, Any]:
        """Get the full configuration for a specific server.

        Args:
            server_id: The ID of the server to retrieve

        Returns:
            Dictionary with full server configuration

        Raises:
            ValueError: If server doesn't exist in this scope
        """
        ...

    def has_server(self, server_id: str) -> bool:
        """Check if scope contains a specific server.

        Args:
            server_id: Server identifier to check

        Returns:
            True if server exists in scope, False otherwise
        """
        servers = self.get_servers()
        return server_id in servers


class MCPClientPlugin(ABC):
    """Abstract base class for MCP client plugins."""

    def __init__(self) -> None:
        """Initialize client plugin."""
        self._name: str = self._get_name()
        self._scopes: Dict[str, ScopeHandler] = self._initialize_scopes()

    @abstractmethod
    def _get_name(self) -> str:
        """Return the client name.

        Returns:
            Client name (e.g., 'claude-code', 'cursor')
        """
        ...

    @abstractmethod
    def _initialize_scopes(self) -> Dict[str, ScopeHandler]:
        """Initialize and return scope handlers.

        Returns:
            Dictionary mapping scope names to their handlers
        """
        ...

    @property
    def name(self) -> str:
        """Client name property.

        Returns:
            Client name
        """
        return self._name

    def get_scopes(self) -> List[ScopeConfig]:
        """Get all available scopes for this client.

        Returns:
            List of scope configurations
        """
        return [handler.config for handler in self._scopes.values()]

    def get_scope_names(self) -> List[str]:
        """Get all scope names for this client.

        Returns:
            List of scope names
        """
        return list(self._scopes.keys())

    def has_scope(self, scope: str) -> bool:
        """Check if client has a specific scope.

        Args:
            scope: Scope name to check

        Returns:
            True if scope exists, False otherwise
        """
        return scope in self._scopes

    def get_scope_handler(self, scope: str) -> ScopeHandler:
        """Get scope handler by name.

        Args:
            scope: Scope name

        Returns:
            Scope handler

        Raises:
            ValueError: If scope does not exist
        """
        if scope not in self._scopes:
            available = ", ".join(self._scopes.keys())
            raise ValueError(
                f"Unknown scope '{scope}' for client '{self.name}'. Available: {available}"
            )

        return self._scopes[scope]

    @abstractmethod
    def list_servers(self, scope: Optional[str] = None) -> Dict[str, ServerInfo]:
        """List all servers, optionally filtered by scope.

        Args:
            scope: Optional scope filter

        Returns:
            Dictionary mapping qualified server IDs to server information
        """
        ...

    @abstractmethod
    def add_server(
        self, server_id: str, config: ServerConfig, scope: str
    ) -> OperationResult:
        """Add a server to the specified scope.

        Args:
            server_id: Unique server identifier
            config: Server configuration
            scope: Target scope name

        Returns:
            Operation result
        """
        ...

    @abstractmethod
    def remove_server(self, server_id: str, scope: str) -> OperationResult:
        """Remove a server from the specified scope.

        Args:
            server_id: Server identifier
            scope: Source scope name

        Returns:
            Operation result
        """
        ...

    @abstractmethod
    def get_server_state(self, server_id: str) -> ServerState:
        """Get the current state of a server.

        Args:
            server_id: Server identifier

        Returns:
            Current server state
        """
        ...

    def get_server_info(self, server_id: str) -> Optional[ServerInfo]:
        """Get detailed information about a specific server.

        Args:
            server_id: Server identifier

        Returns:
            Server information if found, None otherwise
        """
        servers = self.list_servers()

        # Look for exact match first
        for qualified_id, info in servers.items():
            if info.id == server_id:
                return info

        # Look for qualified ID match
        if server_id in servers:
            return servers[server_id]

        return None

    def find_server_scope(self, server_id: str) -> Optional[str]:
        """Find which scope contains a specific server.

        Args:
            server_id: Server identifier

        Returns:
            Scope name if found, None otherwise
        """
        for scope_name, handler in self._scopes.items():
            if handler.has_server(server_id):
                return scope_name

        return None

    def find_all_server_scopes(self, server_id: str) -> List[str]:
        """Find ALL scopes that contain a specific server.

        Args:
            server_id: Server identifier

        Returns:
            List of scope names where server is found (may be empty)
        """
        found_scopes = []
        for scope_name, handler in self._scopes.items():
            if handler.has_server(server_id):
                found_scopes.append(scope_name)

        return found_scopes

    def enable_server(self, server_id: str) -> OperationResult:
        """Enable a disabled server.

        Default implementation - subclasses should override for client-specific logic.

        Args:
            server_id: Server identifier

        Returns:
            Operation result
        """
        return OperationResult.failure_result(
            f"Enable operation not implemented for client '{self.name}'"
        )

    def disable_server(self, server_id: str) -> OperationResult:
        """Disable an enabled server.

        Default implementation - subclasses should override for client-specific logic.

        Args:
            server_id: Server identifier

        Returns:
            Operation result
        """
        return OperationResult.failure_result(
            f"Disable operation not implemented for client '{self.name}'"
        )

    def validate_server_config(self, config: ServerConfig) -> List[str]:
        """Validate server configuration.

        Default implementation - subclasses can override for client-specific validation.

        Args:
            config: Server configuration to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        if not config.command:
            errors.append("Server command is required")

        if not isinstance(config.args, list):
            errors.append("Server args must be a list")

        if not isinstance(config.env, dict):
            errors.append("Server env must be a dictionary")

        return errors
