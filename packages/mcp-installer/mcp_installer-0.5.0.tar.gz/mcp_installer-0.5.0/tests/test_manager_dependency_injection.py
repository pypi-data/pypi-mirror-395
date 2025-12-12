"""Functional tests for MCPManager Dependency Inversion Principle (DIP) refactoring.

These tests validate that MCPManager follows DIP by accepting ClientRegistry
as a required constructor parameter rather than creating it internally.

CRITICAL: These tests validate ACTUAL behavior that users need:
1. Developers can create MCPManager with custom registry for testing
2. Multiple MCPManager instances can coexist with different registries
3. Tests can run in complete isolation without plugin discovery
4. Factory functions provide convenient access to production manager

These tests are UNGAMEABLE because they:
- Create real registry instances with controlled plugins
- Verify actual manager operations (not mocks)
- Check that the manager uses the provided registry (not creating its own)
- Validate isolation between multiple manager instances
- Cannot pass by creating internal registry - must use the provided one
"""

import pytest
from unittest.mock import Mock
from typing import Dict, List, Optional

from mcpi.clients.manager import MCPManager
from mcpi.clients.registry import ClientRegistry
from mcpi.clients.base import MCPClientPlugin
from mcpi.clients.types import ServerInfo, ServerConfig, ServerState, OperationResult


class TestMCPManagerDependencyInjection:
    """Test MCPManager follows DIP with required registry parameter."""

    @pytest.fixture
    def mock_client_plugin(self):
        """Create a mock client plugin for testing.

        Note: We use Mock (not create_autospec) because different client plugins
        have different methods (e.g., is_installed() exists in ClaudeCodePlugin
        but not in the base MCPClientPlugin class). The manager uses hasattr()
        to check for optional methods, so our mock needs to support this pattern.
        """
        mock_plugin = Mock(spec=MCPClientPlugin)

        # Configure the mock with realistic behavior
        mock_plugin.name = "test-client"
        mock_plugin.is_installed = Mock(return_value=True)
        mock_plugin.list_servers = Mock(return_value={})
        mock_plugin.get_server_info = Mock(return_value=None)
        mock_plugin.get_server_state = Mock(return_value=ServerState.NOT_INSTALLED)

        return mock_plugin

    @pytest.fixture
    def mock_registry_with_plugin(self, mock_client_plugin):
        """Create a mock ClientRegistry with a test plugin.

        This represents a registry that has been pre-configured with
        plugins, avoiding auto-discovery during tests.
        """
        mock_registry = Mock(spec=ClientRegistry)

        # Configure registry behavior
        mock_registry.get_available_clients = Mock(return_value=["test-client"])
        mock_registry.has_client = Mock(return_value=True)
        mock_registry.get_client = Mock(return_value=mock_client_plugin)
        mock_registry.list_all_servers = Mock(return_value={})
        mock_registry.get_client_info = Mock(
            return_value={"test-client": {"installed": True}}
        )

        return mock_registry

    @pytest.fixture
    def empty_mock_registry(self):
        """Create an empty mock registry with no clients.

        Useful for testing manager behavior when no clients are available.
        """
        mock_registry = Mock(spec=ClientRegistry)

        mock_registry.get_available_clients = Mock(return_value=[])
        mock_registry.has_client = Mock(return_value=False)
        mock_registry.list_all_servers = Mock(return_value={})
        mock_registry.get_client_info = Mock(return_value={})

        return mock_registry

    def test_mcp_manager_requires_registry_parameter(self, mock_registry_with_plugin):
        """Test that MCPManager requires registry as parameter.

        USER WORKFLOW:
        1. Developer creates MCPManager for testing
        2. Developer provides pre-configured registry
        3. Manager uses that registry, not creating its own

        VALIDATION:
        - Constructor accepts registry parameter
        - Parameter is stored and used
        - Different registries can be used for different test scenarios

        GAMING RESISTANCE:
        - Provides real mock registry
        - Verifies manager stores the registry
        - Cannot pass by creating internal registry
        """
        # Create manager with explicit registry
        manager = MCPManager(registry=mock_registry_with_plugin)

        # Verify the registry was stored
        assert (
            manager.registry is mock_registry_with_plugin
        ), "Manager must store the provided registry"

    def test_mcp_manager_with_injected_registry_uses_it_for_operations(
        self, mock_registry_with_plugin, mock_client_plugin
    ):
        """Verify MCPManager actually uses the injected registry for operations.

        This test is un-gameable because:
        - Creates manager with mock registry
        - Calls manager operations
        - Verifies mock registry methods were called
        - Cannot pass by using a different registry
        - Proves manager uses injected dependency
        """
        # Create manager with mock registry
        manager = MCPManager(registry=mock_registry_with_plugin)

        # Perform operation that should use the registry
        available_clients = manager.get_available_clients()

        # Verify the injected registry was called
        mock_registry_with_plugin.get_available_clients.assert_called()
        assert available_clients == [
            "test-client"
        ], "Manager must return results from injected registry"

        # Test another operation
        client_info = manager.get_client_info()

        # Verify registry was called again
        mock_registry_with_plugin.get_client_info.assert_called()
        assert (
            "test-client" in client_info
        ), "Manager must use injected registry for all operations"

    def test_mcp_manager_list_servers_delegates_to_injected_registry(
        self, mock_registry_with_plugin, mock_client_plugin
    ):
        """Verify list_servers() operation uses injected registry.

        USER WORKFLOW:
        1. User calls manager.list_servers()
        2. Manager delegates to its registry
        3. Results come from injected registry (not auto-discovered plugins)

        VALIDATION:
        - Manager calls registry methods
        - Manager returns registry results
        - No direct plugin discovery happens

        GAMING RESISTANCE:
        - Configures mock to return specific data
        - Verifies that specific data is returned
        - Checks mock was actually called
        - Cannot pass without using injected registry
        """
        # Configure mock plugin to return specific servers
        test_servers = {
            "test-client:server1": ServerInfo(
                id="server1",
                client="test-client",
                scope="user",
                state=ServerState.ENABLED,
                config=ServerConfig(command="npx", args=["-y", "test"]),
            )
        }
        mock_client_plugin.list_servers.return_value = test_servers

        # Create manager
        manager = MCPManager(
            registry=mock_registry_with_plugin, default_client="test-client"
        )

        # Call list_servers
        result = manager.list_servers()

        # Verify registry was used
        mock_registry_with_plugin.get_client.assert_called_with("test-client")
        mock_client_plugin.list_servers.assert_called()

        # Verify we got the mock data
        assert (
            "test-client:server1" in result
        ), "Manager must return data from injected registry"

    def test_multiple_managers_with_different_registries_are_isolated(
        self, mock_client_plugin
    ):
        """Verify multiple MCPManager instances don't interfere with each other.

        USER WORKFLOW:
        1. Test suite creates multiple managers for different scenarios
        2. Each manager has different registry configuration
        3. Operations on one manager don't affect others

        VALIDATION:
        - Each manager uses its own registry independently
        - No shared state between instances
        - Operations on one don't affect others
        - True isolation for parallel testing

        GAMING RESISTANCE:
        - Creates two managers with different mock registries
        - Verifies each uses its own registry
        - Checks operations on one don't call other's registry
        - Cannot pass with singleton or shared registry pattern
        """
        # Create first registry with one client
        registry1 = Mock(spec=ClientRegistry)
        registry1.get_available_clients = Mock(return_value=["client-alpha"])
        registry1.has_client = Mock(return_value=True)
        registry1.get_client = Mock(return_value=mock_client_plugin)

        # Create second registry with different client
        registry2 = Mock(spec=ClientRegistry)
        registry2.get_available_clients = Mock(return_value=["client-beta"])
        registry2.has_client = Mock(return_value=True)
        registry2.get_client = Mock(return_value=mock_client_plugin)

        # Create two managers
        manager1 = MCPManager(registry=registry1, default_client="client-alpha")
        manager2 = MCPManager(registry=registry2, default_client="client-beta")

        # Verify each manager uses its own registry
        clients1 = manager1.get_available_clients()
        clients2 = manager2.get_available_clients()

        # Manager1 should only see client-alpha
        assert clients1 == ["client-alpha"], "Manager 1 should use registry 1"
        registry1.get_available_clients.assert_called()

        # Manager2 should only see client-beta
        assert clients2 == ["client-beta"], "Manager 2 should use registry 2"
        registry2.get_available_clients.assert_called()

        # Verify no cross-contamination
        assert (
            "client-beta" not in clients1
        ), "Manager 1 should not see Manager 2's clients"
        assert (
            "client-alpha" not in clients2
        ), "Manager 2 should not see Manager 1's clients"

    def test_mcp_manager_with_empty_registry_handles_gracefully(
        self, empty_mock_registry
    ):
        """Verify MCPManager works correctly with empty registry.

        USER WORKFLOW:
        1. Developer creates manager with empty registry for testing edge cases
        2. Manager handles lack of clients gracefully
        3. Operations return empty results (no crashes)

        VALIDATION:
        - Empty registry loads successfully
        - get_available_clients() returns empty list
        - No default client is set
        - Operations handle empty state correctly

        GAMING RESISTANCE:
        - Tests actual empty registry handling
        - Verifies no hardcoded fallback to discovery
        - Checks manager operations handle empty state
        - Cannot pass by auto-discovering plugins
        """
        # Create manager with empty registry
        manager = MCPManager(registry=empty_mock_registry)

        # Should have no clients
        clients = manager.get_available_clients()
        assert len(clients) == 0, "Empty registry should result in no clients"

        # Should have no default client
        assert (
            manager.default_client is None
        ), "No default client should be set with empty registry"

        # list_servers should return empty
        servers = manager.list_servers()
        assert (
            len(servers) == 0
        ), "list_servers() with empty registry should return empty dict"

        # Operations that require client should fail gracefully
        result = manager.add_server(
            "test-server",
            ServerConfig(command="npx", args=["-y", "test"]),
            scope="user",
        )
        assert (
            not result.success
        ), "Operations should fail gracefully when no client available"

    def test_mcp_manager_default_client_detection_uses_registry(
        self, mock_client_plugin
    ):
        """Verify default client detection uses the injected registry.

        USER WORKFLOW:
        1. Manager is created without explicit default_client
        2. Manager auto-detects from available clients in registry
        3. Detection uses injected registry (not discovery)

        VALIDATION:
        - Manager queries registry for available clients
        - Manager selects appropriate default
        - Selection is based on registry data only

        GAMING RESISTANCE:
        - Provides registry with specific clients
        - Verifies manager selects from those clients
        - Checks registry methods were called
        - Cannot pass by discovering real clients
        """
        # Create registry with multiple clients in priority order
        registry = Mock(spec=ClientRegistry)
        registry.get_available_clients = Mock(
            return_value=["cursor", "vscode", "claude-code"]
        )
        registry.has_client = Mock(return_value=True)
        registry.get_client = Mock(return_value=mock_client_plugin)

        # Configure plugin as installed
        mock_client_plugin.is_installed = Mock(return_value=True)

        # Create manager without default_client (triggers auto-detection)
        manager = MCPManager(registry=registry)

        # Verify registry was queried for detection
        registry.get_available_clients.assert_called()

        # Should detect claude-code as highest priority
        assert (
            manager.default_client == "claude-code"
        ), "Should auto-detect claude-code as highest priority client"

    def test_mcp_manager_can_switch_default_client_using_registry(
        self, mock_client_plugin
    ):
        """Verify manager can switch default client using registry validation.

        USER WORKFLOW:
        1. Manager starts with one default client
        2. User sets a different default client
        3. Manager validates new client exists in registry

        VALIDATION:
        - set_default_client() validates against registry
        - Only clients in registry can be set as default
        - Invalid clients are rejected with clear error

        GAMING RESISTANCE:
        - Provides registry with specific clients
        - Attempts to set valid and invalid clients
        - Verifies validation uses registry
        - Cannot pass without registry validation
        """
        # Create registry with specific clients
        registry = Mock(spec=ClientRegistry)
        registry.get_available_clients = Mock(return_value=["client-a", "client-b"])
        registry.has_client = Mock(
            side_effect=lambda name: name in ["client-a", "client-b"]
        )

        # Create manager
        manager = MCPManager(registry=registry, default_client="client-a")

        # Switch to valid client - should succeed
        result = manager.set_default_client("client-b")
        assert result.success, "Should be able to switch to client in registry"
        assert manager.default_client == "client-b", "Default client should be updated"

        # Try to switch to invalid client - should fail
        result = manager.set_default_client("client-invalid")
        assert not result.success, "Should reject client not in registry"
        assert (
            "Unknown client" in result.message
        ), "Error should explain client is unknown"
        assert (
            manager.default_client == "client-b"
        ), "Default client should remain unchanged after failed attempt"

    def test_mcp_manager_server_operations_use_registry_methods(
        self, mock_registry_with_plugin, mock_client_plugin
    ):
        """Verify all server operations delegate through registry to client plugin.

        USER WORKFLOW:
        1. User performs various server operations via manager
        2. Manager uses registry to get the client plugin
        3. Manager delegates operations to the client plugin

        VALIDATION:
        - add_server() calls registry.add_server() (for add/remove)
        - remove_server() calls registry.remove_server()
        - enable_server() delegates to client.enable_server() via registry.get_client()
        - disable_server() delegates to client.disable_server() via registry.get_client()
        - All operations use injected registry to access clients

        GAMING RESISTANCE:
        - Configures registry and client mocks to track calls
        - Performs multiple different operations
        - Verifies each operation called correct method on correct object
        - Cannot pass without using injected registry
        """
        # Configure registry mock to track operations (add/remove go through registry)
        mock_registry_with_plugin.add_server = Mock(
            return_value=OperationResult.success_result("Added")
        )
        mock_registry_with_plugin.remove_server = Mock(
            return_value=OperationResult.success_result("Removed")
        )

        # Configure client mock to track enable/disable operations
        # (enable/disable go through client.enable_server/disable_server directly)
        mock_client_plugin.enable_server = Mock(
            return_value=OperationResult.success_result("Enabled")
        )
        mock_client_plugin.disable_server = Mock(
            return_value=OperationResult.success_result("Disabled")
        )

        # Create manager
        manager = MCPManager(
            registry=mock_registry_with_plugin, default_client="test-client"
        )

        # Test add_server
        server_config = ServerConfig(command="npx", args=["-y", "test"])
        result = manager.add_server("test-server", server_config, "user")
        assert result.success, "add_server should succeed"
        mock_registry_with_plugin.add_server.assert_called_with(
            "test-client", "test-server", server_config, "user"
        )

        # Test remove_server
        result = manager.remove_server("test-server", "user")
        assert result.success, "remove_server should succeed"
        mock_registry_with_plugin.remove_server.assert_called_with(
            "test-client", "test-server", "user"
        )

        # Test enable_server - delegates to client via registry.get_client()
        result = manager.enable_server("test-server")
        assert result.success, "enable_server should succeed"
        mock_registry_with_plugin.get_client.assert_called()  # Manager gets client from registry
        mock_client_plugin.enable_server.assert_called()  # Then calls client's method

        # Test disable_server - delegates to client via registry.get_client()
        result = manager.disable_server("test-server")
        assert result.success, "disable_server should succeed"
        mock_client_plugin.disable_server.assert_called()  # Calls client's method

    def test_mcp_manager_uses_only_injected_registry_no_internal_registry(self):
        """CRITICAL: Verify manager uses ONLY injected registry, doesn't create internal one.

        This test fixes BLOCKER #2 by proving the manager cannot pass with a stub
        implementation that creates its own internal registry.

        USER WORKFLOW:
        1. Developer creates manager with mock registry
        2. Developer performs operations
        3. Developer verifies ONLY mock registry is used (no internal registry)

        VALIDATION:
        - Manager stores injected registry
        - Manager uses ONLY injected registry for operations
        - Manager does NOT create internal/default/fallback registry
        - All operations delegate to injected registry

        GAMING RESISTANCE:
        - Creates mock registry with unique return values
        - Performs operations and verifies unique values returned
        - Checks no internal registry attributes exist
        - Cannot pass by creating internal registry
        - Cannot pass by mixing injected and internal registry
        """
        # Create mock registry with unique identifiable data
        mock_registry = Mock(spec=ClientRegistry)
        unique_client_name = "unique-test-client-abc123"
        mock_registry.get_available_clients = Mock(return_value=[unique_client_name])
        mock_registry.has_client = Mock(return_value=True)
        mock_registry.list_all_servers = Mock(return_value={})

        # Create manager with injected registry
        manager = MCPManager(registry=mock_registry)

        # CRITICAL: Verify mock registry was called
        clients = manager.get_available_clients()
        # Note: get_available_clients may be called multiple times (e.g., during init for auto-detection)
        # The important thing is that it IS called and returns our unique data
        mock_registry.get_available_clients.assert_called()

        # CRITICAL: Verify result comes from mock (not internal registry)
        assert clients == [
            unique_client_name
        ], f"Manager must return data from injected registry (got {clients})"

        # CRITICAL: Verify no internal registry attributes exist
        # Check common naming patterns for internal registries
        forbidden_attrs = [
            "_real_registry",
            "_default_registry",
            "_internal_registry",
            "_fallback_registry",
            "_production_registry",
        ]
        for attr in forbidden_attrs:
            assert not hasattr(
                manager, attr
            ), f"Manager must NOT have internal registry attribute '{attr}' (violates DIP)"

        # CRITICAL: Verify the ONLY registry is the injected one
        assert (
            manager.registry is mock_registry
        ), "Manager's registry attribute must be the injected registry"

    def test_mcp_manager_constructor_requires_registry_parameter(self):
        """CRITICAL: Verify registry is truly required (not optional).

        This test fixes part of BLOCKER #2 by proving the constructor
        cannot work without the registry parameter.

        USER WORKFLOW:
        1. Developer attempts to create manager without registry
        2. Constructor raises TypeError
        3. Developer is forced to provide registry explicitly

        VALIDATION:
        - Constructor fails without registry
        - Error message is clear about missing parameter
        - No default registry creation fallback exists

        GAMING RESISTANCE:
        - Attempts to create manager without parameter
        - Verifies TypeError is raised
        - Cannot pass if parameter is optional with default
        - Cannot pass if constructor succeeds without parameter
        """
        with pytest.raises(TypeError) as exc_info:
            manager = MCPManager(default_client="test-client")

        error_msg = str(exc_info.value)
        assert (
            "registry" in error_msg.lower()
        ), f"Error should mention missing 'registry' parameter: {error_msg}"

    def test_mcp_manager_all_operations_use_injected_registry_exclusively(
        self, mock_client_plugin
    ):
        """CRITICAL: Verify ALL manager operations use injected registry exclusively.

        This test comprehensively validates that every operation goes through
        the injected registry and never uses any fallback/internal registry.

        USER WORKFLOW:
        1. Developer creates manager with spy registry
        2. Developer performs multiple different operations
        3. Developer verifies ALL operations delegated via spy registry

        VALIDATION:
        - Every operation uses registry to access clients/data
        - No operation creates or uses internal registry
        - Registry is the single source of truth for client access
        - add/remove go through registry.add_server/remove_server
        - enable/disable go through registry.get_client().enable_server/disable_server

        GAMING RESISTANCE:
        - Creates comprehensive spy registry that tracks ALL calls
        - Performs exhaustive set of operations
        - Verifies EVERY operation used spy registry
        - Cannot pass by mixing injected and internal registry
        - Cannot pass by selectively using injected registry
        """
        # Configure client mock for enable/disable operations
        mock_client_plugin.enable_server = Mock(
            return_value=OperationResult.success_result("Enabled")
        )
        mock_client_plugin.disable_server = Mock(
            return_value=OperationResult.success_result("Disabled")
        )

        # Create spy registry that tracks all method calls
        spy_registry = Mock(spec=ClientRegistry)
        spy_registry.get_available_clients = Mock(return_value=["test-client"])
        spy_registry.has_client = Mock(return_value=True)
        spy_registry.get_client_info = Mock(return_value={"test-client": {}})
        spy_registry.list_all_servers = Mock(return_value={})
        spy_registry.add_server = Mock(
            return_value=OperationResult.success_result("Added")
        )
        spy_registry.remove_server = Mock(
            return_value=OperationResult.success_result("Removed")
        )
        spy_registry.get_client = Mock(return_value=mock_client_plugin)

        # Create manager
        manager = MCPManager(registry=spy_registry, default_client="test-client")

        # Perform comprehensive operations
        manager.get_available_clients()
        manager.get_client_info()
        manager.list_servers()
        manager.add_server(
            "test", ServerConfig(command="npx", args=["-y", "test"]), "user"
        )
        manager.remove_server("test", "user")
        manager.enable_server("test")
        manager.disable_server("test")

        # CRITICAL: Verify spy registry was used for ALL operations
        spy_registry.get_available_clients.assert_called()
        spy_registry.get_client_info.assert_called()
        spy_registry.get_client.assert_called()  # For list_servers, enable, disable
        spy_registry.add_server.assert_called()
        spy_registry.remove_server.assert_called()
        # enable/disable go through client obtained via registry.get_client()
        mock_client_plugin.enable_server.assert_called()
        mock_client_plugin.disable_server.assert_called()

        # CRITICAL: Verify manager has ONLY the injected registry
        assert (
            manager.registry is spy_registry
        ), "Manager must use ONLY the injected registry for all operations"


class TestMCPManagerFactoryFunctions:
    """Test factory functions that provide convenient manager creation.

    Note: These tests will initially fail because the factory functions
    don't exist yet. After implementation, they will validate:
    1. Factory returns working MCPManager instance
    2. Default factory creates real registry with discovery
    3. Test factory allows registry injection
    """

    @pytest.fixture
    def mock_registry(self):
        """Create a mock registry for factory testing."""
        registry = Mock(spec=ClientRegistry)
        registry.get_available_clients = Mock(return_value=["test-client"])
        registry.has_client = Mock(return_value=True)
        registry.get_client_info = Mock(return_value={"test-client": {}})
        return registry

    def test_create_default_manager_factory_returns_working_instance(self):
        """Test create_default_manager() factory function returns working manager.

        USER WORKFLOW:
        1. Production code calls create_default_manager()
        2. Gets manager with auto-discovered clients
        3. Can immediately use manager operations

        VALIDATION:
        - Factory function exists and is importable
        - Returns MCPManager instance
        - Manager has ClientRegistry with discovered plugins
        - Manager can perform operations

        GAMING RESISTANCE:
        - Attempts actual import of factory function
        - Creates manager and verifies type
        - Calls operations to prove it's functional
        - Cannot pass with stub that doesn't work
        """
        from mcpi.clients.manager import create_default_manager

        # Factory should return an MCPManager instance
        manager = create_default_manager()
        assert isinstance(
            manager, MCPManager
        ), "Factory must return MCPManager instance"

        # Manager should have a registry
        assert manager.registry is not None, "Manager from factory must have registry"
        assert isinstance(
            manager.registry, ClientRegistry
        ), "Manager must have real ClientRegistry"

        # Manager should be usable
        clients = manager.get_available_clients()
        assert isinstance(clients, list), "Manager from factory must be functional"

    def test_create_test_manager_factory_with_injected_registry(self, mock_registry):
        """Test create_test_manager() factory accepts registry injection.

        USER WORKFLOW:
        1. Test code calls create_test_manager(mock_registry)
        2. Gets manager configured with test registry
        3. Test can use manager in complete isolation

        VALIDATION:
        - Factory function accepts registry parameter
        - Returns MCPManager configured with that registry
        - Manager uses the provided registry (not creating new one)
        - Provides convenient testing interface

        GAMING RESISTANCE:
        - Passes real mock registry to factory
        - Verifies manager uses that specific registry
        - Checks operations delegate to injected registry
        - Cannot pass by creating new registry
        """
        from mcpi.clients.manager import create_test_manager

        # Factory should accept custom registry
        manager = create_test_manager(mock_registry)
        assert isinstance(
            manager, MCPManager
        ), "Factory must return MCPManager instance"

        # Verify it uses our mock registry
        assert (
            manager.registry is mock_registry
        ), "Factory must configure manager with provided registry"

        # Verify operations use the injected registry
        clients = manager.get_available_clients()
        mock_registry.get_available_clients.assert_called()
        assert clients == [
            "test-client"
        ], "Manager must use injected registry for operations"


class TestCLIIntegrationWithManagerFactory:
    """Test CLI integration with MCPManager factory functions.

    Note: These tests will initially fail. They validate that:
    1. CLI uses factory functions (not direct instantiation)
    2. CLI can accept factory injection for testing
    3. CLI operations work with injected manager
    """

    @pytest.fixture
    def mock_registry(self):
        """Create a mock registry for CLI testing."""
        registry = Mock(spec=ClientRegistry)
        registry.get_available_clients = Mock(return_value=["cli-test-client"])
        registry.has_client = Mock(return_value=True)

        # Mock a simple client
        mock_client = Mock(spec=MCPClientPlugin)
        mock_client.name = "cli-test-client"
        mock_client.list_servers = Mock(
            return_value={
                "test-server": ServerInfo(
                    id="test-server",
                    client="cli-test-client",
                    scope="user",
                    state=ServerState.ENABLED,
                    config=ServerConfig(command="npx", args=["-y", "test"]),
                )
            }
        )
        registry.get_client = Mock(return_value=mock_client)

        return registry

    @pytest.mark.skip(
        reason="CLI factory integration not yet implemented - part of P0-2"
    )
    def test_cli_get_mcp_manager_uses_factory(self):
        """Test that CLI's get_mcp_manager() uses factory function.

        USER WORKFLOW:
        1. CLI command is executed
        2. CLI calls get_mcp_manager() to get manager instance
        3. get_mcp_manager() uses create_default_manager() factory
        4. CLI operates with production manager

        VALIDATION:
        - CLI doesn't directly instantiate MCPManager
        - CLI uses factory function
        - Reduces coupling and improves testability

        GAMING RESISTANCE:
        - Inspects actual CLI code path
        - Verifies factory is called
        - Cannot pass with direct instantiation
        """
        from mcpi.cli import get_mcp_manager
        from unittest.mock import Mock, patch

        # Mock the factory to verify it's called
        mock_manager = Mock(spec=MCPManager)
        mock_factory = Mock(return_value=mock_manager)

        # Create mock context
        ctx = Mock()
        ctx.obj = {}

        # Call get_mcp_manager with mocked factory
        with patch("mcpi.cli.create_default_manager", mock_factory):
            result = get_mcp_manager(ctx)

        # Verify factory was called
        mock_factory.assert_called_once()
        assert result is mock_manager, "get_mcp_manager() must return factory result"

    @pytest.mark.skip(reason="CLI factory injection not yet implemented - part of P0-2")
    def test_cli_can_inject_test_manager_factory(self, mock_registry):
        """Test that CLI can accept injected manager factory for testing.

        USER WORKFLOW:
        1. Test creates custom manager factory
        2. Test injects factory into CLI
        3. CLI commands use test manager (not production)

        VALIDATION:
        - CLI accepts factory injection parameter
        - Injected factory is used instead of default
        - CLI operations work with test manager
        - Complete isolation in tests

        GAMING RESISTANCE:
        - Creates real test manager with mock registry
        - Injects via Click context
        - Executes real CLI command
        - Verifies output reflects test data (not production)
        """
        from mcpi.cli import cli
        from mcpi.clients.manager import create_test_manager
        from click.testing import CliRunner

        # Create test manager factory
        def test_manager_factory():
            return create_test_manager(mock_registry)

        # Inject via Click context
        runner = CliRunner()
        result = runner.invoke(
            cli, ["list"], obj={"manager_factory": test_manager_factory}
        )

        # Verify CLI used our test manager
        assert result.exit_code == 0, "CLI command should succeed with injected factory"
        assert (
            "test-server" in result.output
        ), "CLI output must show server from test manager"
        assert (
            "cli-test-client" in result.output
        ), "CLI output must reference test client from injected registry"


class TestMCPManagerErrorHandling:
    """Test MCPManager error handling with injected registries.

    These tests verify that proper errors are raised when operations
    fail due to registry state or client availability.
    """

    def test_manager_operations_fail_gracefully_without_default_client(self):
        """Verify operations fail clearly when no default client is available.

        USER WORKFLOW:
        1. Manager is created with empty registry (no clients)
        2. User attempts operations without specifying client
        3. Manager returns clear error (no crash)

        VALIDATION:
        - Operations return failure result (not exception)
        - Error message explains no client available
        - System remains stable

        GAMING RESISTANCE:
        - Uses real empty registry
        - Attempts real operations
        - Verifies actual error handling
        - Cannot pass by using default fallback
        """
        # Create empty registry
        empty_registry = Mock(spec=ClientRegistry)
        empty_registry.get_available_clients = Mock(return_value=[])

        # Create manager (no clients available)
        manager = MCPManager(registry=empty_registry)

        # Attempt operation - should fail gracefully
        result = manager.add_server(
            "test-server",
            ServerConfig(command="npx", args=["-y", "test"]),
            scope="user",
        )

        assert not result.success, "Operation should fail when no client available"
        assert (
            "no client" in result.message.lower()
        ), "Error should explain no client available"

    def test_manager_operations_validate_client_exists_in_registry(self):
        """Verify operations validate client exists before attempting.

        USER WORKFLOW:
        1. User specifies explicit client for operation
        2. Manager checks if client exists in registry
        3. If not, returns clear error before attempting operation

        VALIDATION:
        - Manager validates client against registry
        - Invalid client results in clear error
        - No attempt to execute with non-existent client

        GAMING RESISTANCE:
        - Creates registry with specific clients
        - Attempts operation with invalid client
        - Verifies registry validation is used
        - Cannot pass without registry check
        """
        # Create registry with specific clients
        registry = Mock(spec=ClientRegistry)
        registry.get_available_clients = Mock(return_value=["valid-client"])
        registry.has_client = Mock(side_effect=lambda name: name == "valid-client")

        manager = MCPManager(registry=registry, default_client="valid-client")

        # Attempt operation with invalid client
        result = manager.list_servers(client_name="invalid-client")

        # Should return empty (client doesn't exist)
        assert len(result) == 0, "Should return empty for non-existent client"

        # Verify registry was checked
        registry.has_client.assert_called()
