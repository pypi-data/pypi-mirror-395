"""Bundle installer for installing/removing server bundles."""

from typing import List, Optional

from mcpi.bundles.models import Bundle
from mcpi.clients.manager import MCPManager
from mcpi.clients.types import OperationResult, ServerConfig
from mcpi.registry.catalog import ServerCatalog


class BundleInstaller:
    """Handles installation and removal of server bundles.

    The installer coordinates between the bundle catalog, server catalog,
    and MCP manager to install/remove multiple servers as a unit.
    """

    def __init__(self, manager: MCPManager, catalog: ServerCatalog):
        """Initialize bundle installer.

        Args:
            manager: MCP manager for performing server operations
            catalog: Server catalog for looking up server definitions
        """
        self.manager = manager
        self.catalog = catalog

    def install_bundle(
        self,
        bundle: Bundle,
        scope: str,
        client_name: str,
        dry_run: bool = False,
    ) -> List[OperationResult]:
        """Install all servers from a bundle to a scope.

        Args:
            bundle: Bundle to install
            scope: Target scope name
            client_name: Client name (e.g., 'claude-code')
            dry_run: If True, preview installation without making changes

        Returns:
            List of operation results (one per server in bundle)
        """
        results: List[OperationResult] = []

        for bundle_server in bundle.servers:
            server_id = bundle_server.id

            # In dry-run mode, just report what would be done
            if dry_run:
                # Check if server exists in catalog
                catalog_server = self.catalog.get_server(server_id)
                if catalog_server is None:
                    results.append(
                        OperationResult.failure_result(
                            f"Server '{server_id}' not found in catalog"
                        )
                    )
                else:
                    results.append(
                        OperationResult.success_result(
                            f"Would install server '{server_id}' to {scope}"
                        )
                    )
                continue

            # Look up server in catalog
            catalog_server = self.catalog.get_server(server_id)
            if catalog_server is None:
                # Server not in catalog - record failure and continue with others
                results.append(
                    OperationResult.failure_result(
                        f"Server '{server_id}' not found in catalog"
                    )
                )
                continue

            # Build server configuration
            # Start with catalog defaults
            base_config = catalog_server.get_run_command()

            # Apply bundle-specific config overrides if provided
            if bundle_server.config:
                # Merge bundle config with base config
                if "args" in bundle_server.config:
                    base_config["args"] = bundle_server.config["args"]
                if "env" in bundle_server.config:
                    base_config["env"] = bundle_server.config["env"]
                if "command" in bundle_server.config:
                    base_config["command"] = bundle_server.config["command"]

            # Create ServerConfig from merged config
            server_config = ServerConfig(
                command=base_config.get("command", ""),
                args=base_config.get("args", []),
                env=base_config.get("env", {}),
                type=base_config.get("type", "stdio"),
            )

            # Install server via manager
            result = self.manager.add_server(
                server_id=server_id,
                config=server_config,
                scope=scope,
                client_name=client_name,
            )

            results.append(result)

        return results

    def remove_bundle(
        self,
        bundle: Bundle,
        scope: str,
        client_name: str,
    ) -> List[OperationResult]:
        """Remove all servers from a bundle from a scope.

        Args:
            bundle: Bundle to remove
            scope: Target scope name
            client_name: Client name (e.g., 'claude-code')

        Returns:
            List of operation results (one per server in bundle)
        """
        results: List[OperationResult] = []

        for bundle_server in bundle.servers:
            server_id = bundle_server.id

            # Remove server via manager
            result = self.manager.remove_server(
                server_id=server_id,
                scope=scope,
                client_name=client_name,
            )

            results.append(result)

        return results
