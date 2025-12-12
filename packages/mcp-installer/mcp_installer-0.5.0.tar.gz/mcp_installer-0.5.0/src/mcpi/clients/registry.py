"""Client plugin registry with auto-discovery."""

import importlib
import logging
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Type

from .base import MCPClientPlugin
from .types import OperationResult, ServerInfo

logger = logging.getLogger(__name__)


class ClientRegistry:
    """Registry for MCP client plugins with auto-discovery."""

    def __init__(self, auto_discover: bool = True) -> None:
        """Initialize the client registry.

        Args:
            auto_discover: Whether to automatically discover and register plugins.
                          Set to False for testing to avoid instantiation issues.
        """
        self._plugins: Dict[str, Type[MCPClientPlugin]] = {}
        self._instances: Dict[str, MCPClientPlugin] = {}
        if auto_discover:
            self._discover_plugins()

    def _discover_plugins(self) -> None:
        """Automatically discover and register client plugins."""
        logger.debug("Starting plugin discovery")

        # Get the clients package path
        clients_package = importlib.import_module("mcpi.clients")
        clients_path = Path(clients_package.__file__).parent

        # Find all Python files in the clients directory
        for module_info in pkgutil.iter_modules([str(clients_path)]):
            module_name = module_info.name

            # Skip special modules
            if module_name.startswith("_") or module_name in [
                "base",
                "types",
                "protocols",
                "file_based",
                "registry",
            ]:
                continue

            try:
                # Import the module
                module = importlib.import_module(f"mcpi.clients.{module_name}")

                # Look for MCPClientPlugin subclasses
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    # Check if it's a class that inherits from MCPClientPlugin
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, MCPClientPlugin)
                        and attr is not MCPClientPlugin
                    ):

                        # Register the plugin
                        self._register_plugin_class(attr)
                        logger.debug(
                            f"Discovered plugin: {attr.__name__} in module {module_name}"
                        )

            except Exception as e:
                logger.warning(f"Failed to load plugin module {module_name}: {e}")

    def _register_plugin_class(self, plugin_class: Type[MCPClientPlugin]) -> None:
        """Register a plugin class.

        Args:
            plugin_class: Plugin class to register
        """
        try:
            # Create a temporary instance to get the client name
            temp_instance = plugin_class()
            client_name = temp_instance.name

            # Register the class
            self._plugins[client_name] = plugin_class
            logger.info(f"Registered plugin for client '{client_name}'")

        except Exception as e:
            logger.error(f"Failed to register plugin {plugin_class.__name__}: {e}")

    def register_plugin(self, plugin_class: Type[MCPClientPlugin]) -> None:
        """Manually register a plugin class.

        Args:
            plugin_class: Plugin class to register
        """
        self._register_plugin_class(plugin_class)

    def get_available_clients(self) -> List[str]:
        """Get list of available client names.

        Returns:
            List of client names
        """
        return list(self._plugins.keys())

    def has_client(self, client_name: str) -> bool:
        """Check if a client is available.

        Args:
            client_name: Name of the client to check

        Returns:
            True if client is available, False otherwise
        """
        return client_name in self._plugins

    def get_client(self, client_name: str) -> MCPClientPlugin:
        """Get a client plugin instance.

        Args:
            client_name: Name of the client

        Returns:
            Client plugin instance

        Raises:
            ValueError: If client is not available
        """
        if client_name not in self._plugins:
            available = ", ".join(self.get_available_clients())
            raise ValueError(f"Unknown client '{client_name}'. Available: {available}")

        # Return cached instance or create new one
        if client_name not in self._instances:
            plugin_class = self._plugins[client_name]
            self._instances[client_name] = plugin_class()
            logger.debug(f"Created instance for client '{client_name}'")

        return self._instances[client_name]

    def inject_client_instance(
        self, client_name: str, instance: MCPClientPlugin
    ) -> None:
        """Inject a custom client instance (useful for testing).

        Args:
            client_name: Name of the client
            instance: Client instance to inject
        """
        self._instances[client_name] = instance
        # Also register the class if not already registered
        if client_name not in self._plugins:
            self._plugins[client_name] = type(instance)
        logger.debug(f"Injected custom instance for client '{client_name}'")

    def list_all_servers(
        self, client_name: Optional[str] = None
    ) -> Dict[str, ServerInfo]:
        """List servers from all or specific clients.

        Args:
            client_name: Optional client name filter

        Returns:
            Dictionary mapping qualified server IDs to server information
        """
        servers = {}

        # Determine which clients to query
        if client_name:
            if not self.has_client(client_name):
                return {}
            client_names = [client_name]
        else:
            client_names = self.get_available_clients()

        # Collect servers from each client
        for name in client_names:
            try:
                client = self.get_client(name)
                client_servers = client.list_servers()
                servers.update(client_servers)
            except Exception as e:
                logger.error(f"Failed to list servers from client '{name}': {e}")

        return servers

    def find_server_client(self, server_id: str) -> Optional[str]:
        """Find which client contains a specific server.

        Args:
            server_id: Server identifier

        Returns:
            Client name if found, None otherwise
        """
        for client_name in self.get_available_clients():
            try:
                client = self.get_client(client_name)
                if client.get_server_info(server_id):
                    return client_name
            except Exception as e:
                logger.error(
                    f"Error checking client '{client_name}' for server '{server_id}': {e}"
                )

        return None

    def add_server(
        self, client_name: str, server_id: str, config, scope: str
    ) -> OperationResult:
        """Add a server to a specific client.

        Args:
            client_name: Target client name
            server_id: Unique server identifier
            config: Server configuration
            scope: Target scope name

        Returns:
            Operation result
        """
        if not self.has_client(client_name):
            available = ", ".join(self.get_available_clients())
            return OperationResult.failure_result(
                f"Unknown client '{client_name}'. Available: {available}"
            )

        try:
            client = self.get_client(client_name)
            return client.add_server(server_id, config, scope)
        except Exception as e:
            return OperationResult.failure_result(
                f"Failed to add server: {e}", errors=[str(e)]
            )

    def remove_server(
        self, client_name: str, server_id: str, scope: str
    ) -> OperationResult:
        """Remove a server from a specific client.

        Args:
            client_name: Source client name
            server_id: Server identifier
            scope: Source scope name

        Returns:
            Operation result
        """
        if not self.has_client(client_name):
            available = ", ".join(self.get_available_clients())
            return OperationResult.failure_result(
                f"Unknown client '{client_name}'. Available: {available}"
            )

        try:
            client = self.get_client(client_name)
            return client.remove_server(server_id, scope)
        except Exception as e:
            return OperationResult.failure_result(
                f"Failed to remove server: {e}", errors=[str(e)]
            )

    def enable_server(
        self, server_id: str, client_name: Optional[str] = None
    ) -> OperationResult:
        """Enable a server across all or specific clients.

        Args:
            server_id: Server identifier
            client_name: Optional client name filter

        Returns:
            Operation result
        """
        if client_name:
            if not self.has_client(client_name):
                available = ", ".join(self.get_available_clients())
                return OperationResult.failure_result(
                    f"Unknown client '{client_name}'. Available: {available}"
                )

            try:
                client = self.get_client(client_name)
                return client.enable_server(server_id)
            except Exception as e:
                return OperationResult.failure_result(
                    f"Failed to enable server: {e}", errors=[str(e)]
                )
        else:
            # Try to find the server in any client
            for name in self.get_available_clients():
                try:
                    client = self.get_client(name)
                    if client.get_server_info(server_id):
                        return client.enable_server(server_id)
                except Exception as e:
                    logger.error(f"Error enabling server in client '{name}': {e}")

            return OperationResult.failure_result(
                f"Server '{server_id}' not found in any client"
            )

    def disable_server(
        self, server_id: str, client_name: Optional[str] = None
    ) -> OperationResult:
        """Disable a server across all or specific clients.

        Args:
            server_id: Server identifier
            client_name: Optional client name filter

        Returns:
            Operation result
        """
        if client_name:
            if not self.has_client(client_name):
                available = ", ".join(self.get_available_clients())
                return OperationResult.failure_result(
                    f"Unknown client '{client_name}'. Available: {available}"
                )

            try:
                client = self.get_client(client_name)
                return client.disable_server(server_id)
            except Exception as e:
                return OperationResult.failure_result(
                    f"Failed to disable server: {e}", errors=[str(e)]
                )
        else:
            # Try to find the server in any client
            for name in self.get_available_clients():
                try:
                    client = self.get_client(name)
                    if client.get_server_info(server_id):
                        return client.disable_server(server_id)
                except Exception as e:
                    logger.error(f"Error disabling server in client '{name}': {e}")

            return OperationResult.failure_result(
                f"Server '{server_id}' not found in any client"
            )

    def get_client_info(self, client_name: Optional[str] = None) -> Dict[str, Dict]:
        """Get information about clients.

        Args:
            client_name: Optional client name filter

        Returns:
            Dictionary with client information
        """
        info = {}

        # Determine which clients to query
        if client_name:
            if not self.has_client(client_name):
                return {}
            client_names = [client_name]
        else:
            client_names = self.get_available_clients()

        # Collect information from each client
        for name in client_names:
            try:
                client = self.get_client(name)

                client_info = {
                    "name": client.name,
                    "scopes": [
                        {
                            "name": scope.name,
                            "description": scope.description,
                            "priority": scope.priority,
                            "is_user_level": scope.is_user_level,
                            "is_project_level": scope.is_project_level,
                            "path": str(scope.path) if scope.path else None,
                        }
                        for scope in client.get_scopes()
                    ],
                    "server_count": len(client.list_servers()),
                }

                # Add client-specific info if available
                if hasattr(client, "get_installation_info"):
                    client_info.update(client.get_installation_info())

                info[name] = client_info

            except Exception as e:
                logger.error(f"Failed to get info for client '{name}': {e}")
                info[name] = {"error": str(e)}

        return info

    def refresh_plugins(self) -> None:
        """Refresh plugin discovery and reload instances."""
        logger.info("Refreshing plugin registry")

        # Clear existing instances but keep plugin classes
        self._instances.clear()

        # Re-discover plugins
        self._discover_plugins()

    def get_registry_stats(self) -> Dict[str, int]:
        """Get registry statistics.

        Returns:
            Dictionary with registry statistics
        """
        total_servers = 0
        for client_name in self.get_available_clients():
            try:
                client = self.get_client(client_name)
                total_servers += len(client.list_servers())
            except Exception:
                pass

        return {
            "total_clients": len(self._plugins),
            "loaded_instances": len(self._instances),
            "total_servers": total_servers,
        }
