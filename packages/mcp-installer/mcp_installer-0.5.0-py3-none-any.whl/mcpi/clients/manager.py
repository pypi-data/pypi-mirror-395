"""Main MCP manager for unified client and server management."""

import logging
from typing import Any, Dict, List, Optional, Tuple

from .registry import ClientRegistry
from .types import OperationResult, ServerConfig, ServerInfo, ServerState

logger = logging.getLogger(__name__)


class MCPManager:
    """Main manager for MCP clients and servers with type safety."""

    def __init__(
        self, registry: ClientRegistry, default_client: Optional[str] = None
    ) -> None:
        """Initialize the MCP manager.

        Args:
            registry: ClientRegistry instance (required for DI/testability)
            default_client: Default client name to use
        """
        self.registry = registry
        self._default_client = default_client

        # Auto-detect default client if not specified
        if not self._default_client:
            self._default_client = self._detect_default_client()

        logger.info(
            f"MCP Manager initialized with default client: {self._default_client}"
        )

    def _detect_default_client(self) -> Optional[str]:
        """Auto-detect the most appropriate default client.

        Returns:
            Detected client name or None if no suitable client found
        """
        available_clients = self.registry.get_available_clients()

        if not available_clients:
            logger.warning("No MCP clients available")
            return None

        # Priority order for auto-detection
        priority_clients = ["claude-code", "cursor", "vscode"]

        # Check if any priority clients are available and installed
        for client_name in priority_clients:
            if client_name in available_clients:
                try:
                    client = self.registry.get_client(client_name)
                    # Check if client appears to be installed
                    if hasattr(client, "is_installed") and client.is_installed():
                        logger.info(f"Auto-detected installed client: {client_name}")
                        return client_name
                except Exception as e:
                    logger.debug(f"Client {client_name} detection failed: {e}")

        # Fallback to first available client
        default = available_clients[0]
        logger.info(f"Defaulting to first available client: {default}")
        return default

    @property
    def default_client(self) -> Optional[str]:
        """Get the default client name.

        Returns:
            Default client name
        """
        return self._default_client

    def set_default_client(self, client_name: str) -> OperationResult:
        """Set the default client.

        Args:
            client_name: Client name to set as default

        Returns:
            Operation result
        """
        if not self.registry.has_client(client_name):
            available = ", ".join(self.registry.get_available_clients())
            return OperationResult.failure_result(
                f"Unknown client '{client_name}'. Available: {available}"
            )

        self._default_client = client_name
        logger.info(f"Default client set to: {client_name}")

        return OperationResult.success_result(
            f"Default client set to '{client_name}'", client=client_name
        )

    def get_available_clients(self) -> List[str]:
        """Get list of available client names.

        Returns:
            List of client names
        """
        return self.registry.get_available_clients()

    def get_client_info(self, client_name: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed information about clients.

        Args:
            client_name: Optional client name filter

        Returns:
            Dictionary with client information
        """
        return self.registry.get_client_info(client_name)

    def list_servers(
        self,
        client_name: Optional[str] = None,
        scope: Optional[str] = None,
        state_filter: Optional[ServerState] = None,
    ) -> Dict[str, ServerInfo]:
        """List all servers with optional filtering.

        Args:
            client_name: Optional client name filter
            scope: Optional scope filter
            state_filter: Optional server state filter

        Returns:
            Dictionary mapping qualified server IDs to server information
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        # Get servers from registry
        if client_name:
            if not self.registry.has_client(client_name):
                logger.warning(f"Client '{client_name}' not available")
                return {}

            try:
                client = self.registry.get_client(client_name)
                servers = client.list_servers(scope)
            except Exception as e:
                logger.error(f"Failed to list servers from client '{client_name}': {e}")
                return {}
        else:
            servers = self.registry.list_all_servers()

        # Apply state filter if specified
        if state_filter:
            servers = {
                server_id: info
                for server_id, info in servers.items()
                if info.state == state_filter
            }

        return servers

    def get_server_info(
        self, server_id: str, client_name: Optional[str] = None
    ) -> Optional[ServerInfo]:
        """Get detailed information about a specific server.

        Args:
            server_id: Server identifier
            client_name: Optional client name filter

        Returns:
            Server information if found, None otherwise
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if client_name:
            if not self.registry.has_client(client_name):
                return None

            try:
                client = self.registry.get_client(client_name)
                return client.get_server_info(server_id)
            except Exception as e:
                logger.error(
                    f"Error getting server info from client '{client_name}': {e}"
                )
                return None
        else:
            # Search across all clients
            all_servers = self.registry.list_all_servers()
            for qualified_id, info in all_servers.items():
                if info.id == server_id or qualified_id == server_id:
                    return info
            return None

    def add_server(
        self,
        server_id: str,
        config: ServerConfig,
        scope: str,
        client_name: Optional[str] = None,
    ) -> OperationResult:
        """Add a server to a client scope.

        Args:
            server_id: Unique server identifier
            config: Server configuration
            scope: Target scope name
            client_name: Optional client name (uses default if not specified)

        Returns:
            Operation result
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if not client_name:
            return OperationResult.failure_result(
                "No client specified and no default client available"
            )

        return self.registry.add_server(client_name, server_id, config, scope)

    def remove_server(
        self, server_id: str, scope: str, client_name: Optional[str] = None
    ) -> OperationResult:
        """Remove a server from a client scope.

        Args:
            server_id: Server identifier
            scope: Source scope name
            client_name: Optional client name (uses default if not specified)

        Returns:
            Operation result
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if not client_name:
            return OperationResult.failure_result(
                "No client specified and no default client available"
            )

        return self.registry.remove_server(client_name, server_id, scope)

    def enable_server(
        self,
        server_id: str,
        scope: Optional[str] = None,
        client_name: Optional[str] = None,
    ) -> OperationResult:
        """Enable a disabled server.

        Args:
            server_id: Server identifier
            scope: Optional scope name (if not provided, auto-detects from server location)
            client_name: Optional client name (uses default if not specified)

        Returns:
            Operation result
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if not client_name:
            return OperationResult.failure_result(
                "No client specified and no default client available"
            )

        # Get the client
        if not self.registry.has_client(client_name):
            return OperationResult.failure_result(f"Unknown client: {client_name}")

        client = self.registry.get_client(client_name)

        # Call enable_server with optional scope parameter
        return client.enable_server(server_id, scope)

    def disable_server(
        self,
        server_id: str,
        scope: Optional[str] = None,
        client_name: Optional[str] = None,
    ) -> OperationResult:
        """Disable an enabled server.

        Args:
            server_id: Server identifier
            scope: Optional scope name (if not provided, auto-detects from server location)
            client_name: Optional client name (uses default if not specified)

        Returns:
            Operation result
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if not client_name:
            return OperationResult.failure_result(
                "No client specified and no default client available"
            )

        # Get the client
        if not self.registry.has_client(client_name):
            return OperationResult.failure_result(f"Unknown client: {client_name}")

        client = self.registry.get_client(client_name)

        # Call disable_server with optional scope parameter
        return client.disable_server(server_id, scope)

    def get_server_state(
        self, server_id: str, client_name: Optional[str] = None
    ) -> ServerState:
        """Get the current state of a server.

        Args:
            server_id: Server identifier
            client_name: Optional client name (uses default if not specified)

        Returns:
            Current server state
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if not client_name:
            return ServerState.NOT_INSTALLED

        if not self.registry.has_client(client_name):
            return ServerState.NOT_INSTALLED

        try:
            client = self.registry.get_client(client_name)
            return client.get_server_state(server_id)
        except Exception as e:
            logger.error(f"Error getting server state from client '{client_name}': {e}")
            return ServerState.NOT_INSTALLED

    def find_server_location(self, server_id: str) -> Optional[Dict[str, str]]:
        """Find where a server is located across all clients and scopes.

        Args:
            server_id: Server identifier

        Returns:
            Dictionary with client and scope information if found
        """
        all_servers = self.registry.list_all_servers()

        for qualified_id, info in all_servers.items():
            if info.id == server_id:
                return {
                    "client": info.client,
                    "scope": info.scope,
                    "qualified_id": qualified_id,
                }

        return None

    def find_all_server_scopes(
        self, server_id: str, client_name: Optional[str] = None
    ) -> List[Tuple[str, str]]:
        """Find ALL scopes where a server is defined.

        Args:
            server_id: Server identifier
            client_name: Optional client name filter (uses default if not specified)

        Returns:
            List of (client_name, scope_name) tuples for all scopes containing the server
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if not client_name:
            return []

        if not self.registry.has_client(client_name):
            logger.warning(f"Client '{client_name}' not available")
            return []

        try:
            client = self.registry.get_client(client_name)
            scope_names = client.find_all_server_scopes(server_id)

            # Return as list of (client, scope) tuples
            return [(client_name, scope_name) for scope_name in scope_names]
        except Exception as e:
            logger.error(f"Error finding server scopes in client '{client_name}': {e}")
            return []

    def get_scopes_for_client(
        self, client_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get available scopes for a client.

        Args:
            client_name: Optional client name (uses default if not specified)

        Returns:
            List of scope information dictionaries
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if not client_name or not self.registry.has_client(client_name):
            return []

        try:
            client = self.registry.get_client(client_name)
            scopes = client.get_scopes()

            return [
                {
                    "name": scope.name,
                    "description": scope.description,
                    "priority": scope.priority,
                    "path": str(scope.path) if scope.path else None,
                    "is_user_level": scope.is_user_level,
                    "is_project_level": scope.is_project_level,
                    "exists": client.get_scope_handler(scope.name).exists(),
                }
                for scope in scopes
            ]
        except Exception as e:
            logger.error(f"Error getting scopes for client '{client_name}': {e}")
            return []

    def validate_server_config(
        self, config: ServerConfig, client_name: Optional[str] = None
    ) -> List[str]:
        """Validate server configuration for a specific client.

        Args:
            config: Server configuration to validate
            client_name: Optional client name (uses default if not specified)

        Returns:
            List of validation errors (empty if valid)
        """
        # Use default client if none specified
        if client_name is None:
            client_name = self._default_client

        if not client_name or not self.registry.has_client(client_name):
            return ["No valid client available for validation"]

        try:
            client = self.registry.get_client(client_name)
            return client.validate_server_config(config)
        except Exception as e:
            logger.error(f"Error validating config for client '{client_name}': {e}")
            return [f"Validation error: {e}"]

    def get_status_summary(self) -> Dict[str, Any]:
        """Get a comprehensive status summary.

        Returns:
            Dictionary with status information
        """
        try:
            stats = self.registry.get_registry_stats()
            all_servers = self.list_servers()

            # Count servers by state
            state_counts = {state.name: 0 for state in ServerState}
            for server_info in all_servers.values():
                state_counts[server_info.state.name] += 1

            return {
                "default_client": self._default_client,
                "available_clients": self.get_available_clients(),
                "registry_stats": stats,
                "server_states": state_counts,
                "total_servers": len(all_servers),
            }
        except Exception as e:
            logger.error(f"Error generating status summary: {e}")
            return {"error": str(e)}

    def refresh(self) -> None:
        """Refresh the manager by reloading plugins and clients."""
        logger.info("Refreshing MCP manager")
        self.registry.refresh_plugins()

        # Re-detect default client if current one is no longer available
        if self._default_client not in self.registry.get_available_clients():
            self._default_client = self._detect_default_client()
            logger.info(f"Default client updated to: {self._default_client}")

    def cleanup(self) -> None:
        """Clean up resources and connections."""
        logger.info("Cleaning up MCP manager")
        # Future: Add cleanup logic for active connections, temporary files, etc.


# Factory Functions for DIP Compliance


def create_default_manager(default_client: Optional[str] = None) -> MCPManager:
    """Create MCPManager with default ClientRegistry.

    This factory function provides the default behavior that was previously
    in MCPManager.__init__. Use this for production code that needs
    automatic client discovery.

    Args:
        default_client: Default client name to use (auto-detected if None)

    Returns:
        MCPManager instance with discovered clients
    """
    registry = ClientRegistry()
    return MCPManager(registry=registry, default_client=default_client)


def create_test_manager(
    registry: ClientRegistry, default_client: Optional[str] = None
) -> MCPManager:
    """Create MCPManager with custom ClientRegistry for testing.

    This factory function makes it easy to create test managers with
    pre-configured mock registries.

    Args:
        registry: Pre-configured ClientRegistry (e.g., with mocks)
        default_client: Default client name to use

    Returns:
        MCPManager instance configured with test registry
    """
    return MCPManager(registry=registry, default_client=default_client)
