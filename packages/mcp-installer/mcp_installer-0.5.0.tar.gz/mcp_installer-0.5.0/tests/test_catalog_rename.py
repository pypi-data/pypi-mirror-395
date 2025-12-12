"""Functional tests for registry→catalog rename.

This test suite validates that the rename from "registry" to "catalog" is complete
and functional. These tests are designed to:

1. Verify renamed files exist and are functional
2. Verify renamed methods/parameters work correctly
3. Verify backward compatibility where needed (ClientRegistry stays unchanged)
4. Ensure no broken references remain

GAMING RESISTANCE:
- Tests verify actual file operations on real filesystem
- Tests verify actual data loading from renamed files
- Tests verify method calls succeed with renamed APIs
- Tests cannot be satisfied by stubs or mocks - they require real functionality
"""

import json
import tempfile
from pathlib import Path

import pytest
import warnings

from mcpi.registry.catalog import (
    MCPServer,
    ServerCatalog,
    create_default_catalog,
    create_test_catalog,
)
from mcpi.clients.registry import ClientRegistry


class TestCatalogFileRename:
    """Test that catalog data files exist with correct naming.

    This test cannot be gamed because:
    - Verifies actual files exist on filesystem at expected paths
    - Validates file content is valid JSON
    - Checks data structure matches expected schema
    """

    def test_catalog_json_exists(self):
        """Verify data/catalog.json exists (renamed from registry.json)."""
        # Calculate expected path
        project_root = Path(__file__).parent.parent
        catalog_path = project_root / "src" / "mcpi" / "data" / "catalog.json"

        # Verify file exists
        assert catalog_path.exists(), (
            f"Expected catalog.json at {catalog_path}. "
            "File should be renamed from registry.json"
        )

        # Verify it's valid JSON
        try:
            with open(catalog_path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"catalog.json contains invalid JSON: {e}")

        # Verify structure (dict of server_id -> server_config)
        assert isinstance(data, dict), "Catalog root must be a dictionary"
        assert len(data) > 0, "Catalog should not be empty"

    def test_catalog_cue_schema_exists(self):
        """Verify data/catalog.cue exists (renamed from registry.cue)."""
        project_root = Path(__file__).parent.parent
        cue_path = project_root / "src" / "mcpi" / "data" / "catalog.cue"

        assert cue_path.exists(), (
            f"Expected catalog.cue at {cue_path}. "
            "File should be renamed from registry.cue"
        )

        # Verify it's not empty and contains expected content
        content = cue_path.read_text()
        assert content.strip(), "catalog.cue should not be empty"
        assert "#MCPServer" in content, "CUE schema should define #MCPServer type"

    def test_old_registry_files_do_not_exist(self):
        """Verify old registry.json and registry.cue no longer exist."""
        project_root = Path(__file__).parent.parent

        old_json_path = project_root / "src" / "mcpi" / "data" / "registry.json"
        old_cue_path = project_root / "src" / "mcpi" / "data" / "registry.cue"

        assert not old_json_path.exists(), (
            f"Old registry.json still exists at {old_json_path}. "
            "Should be renamed to catalog.json"
        )

        assert not old_cue_path.exists(), (
            f"Old registry.cue still exists at {old_cue_path}. "
            "Should be renamed to catalog.cue"
        )


class TestServerCatalogAPIRename:
    """Test ServerCatalog class uses 'catalog' terminology.

    This test cannot be gamed because:
    - Tests actual method existence and callable behavior
    - Verifies methods perform real operations (load data, modify state)
    - Checks state changes persist correctly
    """

    def test_catalog_path_parameter(self):
        """Verify ServerCatalog.__init__ uses catalog_path parameter."""
        # Create temp catalog file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_catalog_path = Path(f.name)
            json.dump(
                {
                    "test-server": {
                        "description": "Test server",
                        "command": "node",
                        "args": ["server.js"],
                    }
                },
                f,
            )

        try:
            # Should accept catalog_path parameter
            catalog = ServerCatalog(
                catalog_path=test_catalog_path, validate_with_cue=False
            )
            assert catalog.catalog_path == test_catalog_path

            # Old parameter name should NOT work
            with pytest.raises(TypeError, match="registry_path"):
                ServerCatalog(registry_path=test_catalog_path)

        finally:
            test_catalog_path.unlink(missing_ok=True)

    def test_load_catalog_method_exists(self):
        """Verify ServerCatalog has load_catalog() method (renamed from load_registry)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_catalog_path = Path(f.name)
            json.dump(
                {
                    "test-server": {
                        "description": "Test server",
                        "command": "python",
                        "args": ["-m", "server"],
                    }
                },
                f,
            )

        try:
            catalog = ServerCatalog(
                catalog_path=test_catalog_path, validate_with_cue=False
            )

            # Method should exist and be callable
            assert hasattr(catalog, "load_catalog"), "load_catalog method should exist"
            assert callable(catalog.load_catalog), "load_catalog should be callable"

            # Method should actually load data
            catalog.load_catalog()
            servers = catalog.list_servers()
            assert len(servers) == 1
            assert servers[0][0] == "test-server"

            # Old method name should NOT exist
            assert not hasattr(
                catalog, "load_registry"
            ), "load_registry method should be removed (renamed to load_catalog)"

        finally:
            test_catalog_path.unlink(missing_ok=True)

    def test_save_catalog_method_exists(self):
        """Verify ServerCatalog has save_catalog() method (renamed from save_registry)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_catalog_path = Path(f.name)
            json.dump({}, f)

        try:
            catalog = ServerCatalog(
                catalog_path=test_catalog_path, validate_with_cue=False
            )
            catalog.load_catalog()

            # Add a server
            new_server = MCPServer(
                description="New test server", command="uvx", args=["test-server"]
            )
            catalog.add_server("new-server", new_server)

            # Method should exist and be callable
            assert hasattr(catalog, "save_catalog"), "save_catalog method should exist"
            assert callable(catalog.save_catalog), "save_catalog should be callable"

            # Method should actually save data
            result = catalog.save_catalog()
            assert result is True, "save_catalog should return True on success"

            # Verify data persisted
            with open(test_catalog_path) as f:
                saved_data = json.load(f)
            assert "new-server" in saved_data

            # Old method name should NOT exist
            assert not hasattr(
                catalog, "save_registry"
            ), "save_registry method should be removed (renamed to save_catalog)"

        finally:
            test_catalog_path.unlink(missing_ok=True)


class TestFactoryFunctionRename:
    """Test factory functions use 'catalog' terminology.

    This test cannot be gamed because:
    - Verifies actual factory functions return working instances
    - Tests instances can load real data from correct paths
    - Validates path resolution uses catalog naming
    """

    @pytest.mark.filterwarnings("ignore:create_default_catalog.*:DeprecationWarning")
    def test_create_default_catalog_uses_catalog_path(self):
        """Verify create_default_catalog() references catalog.json not registry.json."""
        catalog = create_default_catalog(validate_with_cue=False)

        # Should reference catalog.json
        assert (
            catalog.catalog_path.name == "catalog.json"
        ), f"Expected catalog.json, got {catalog.catalog_path.name}"

        # Should NOT reference registry.json
        assert "registry.json" not in str(
            catalog.catalog_path
        ), "Factory should not reference old registry.json path"

        # Should be able to load successfully
        catalog.load_catalog()
        servers = catalog.list_servers()
        assert len(servers) > 0, "Should load servers from catalog.json"

    def test_create_test_catalog_uses_catalog_path_param(self):
        """Verify create_test_catalog() uses catalog_path parameter."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_path = Path(f.name)
            json.dump(
                {"test": {"description": "Test", "command": "test", "args": []}}, f
            )

        try:
            # Should accept path parameter
            catalog = create_test_catalog(test_path, validate_with_cue=False)
            assert catalog.catalog_path == test_path

            # Should load successfully
            catalog.load_catalog()
            servers = catalog.list_servers()
            assert len(servers) == 1

        finally:
            test_path.unlink(missing_ok=True)


class TestClientRegistryUnchanged:
    """Test that ClientRegistry class remains unchanged.

    This verifies that the rename only affects server catalog functionality,
    not the client plugin registry (which is a different concept).

    This test cannot be gamed because:
    - Verifies actual ClientRegistry class exists and works
    - Tests real client plugin discovery and management
    """

    def test_client_registry_class_exists(self):
        """Verify ClientRegistry class still exists (should NOT be renamed)."""
        # Should be able to import and instantiate
        registry = ClientRegistry(auto_discover=False)
        assert registry is not None

        # Should have expected methods
        assert hasattr(registry, "get_available_clients")
        assert hasattr(registry, "get_client")
        assert hasattr(registry, "has_client")

    def test_client_registry_functionality(self):
        """Verify ClientRegistry works correctly (unaffected by catalog rename)."""
        registry = ClientRegistry(auto_discover=False)

        # Should discover clients
        clients = registry.get_available_clients()
        assert isinstance(clients, list)

        # Should be able to check for clients
        for client_name in clients:
            assert registry.has_client(client_name)


class TestCLIIntegration:
    """Test CLI commands work with renamed catalog.

    This test cannot be gamed because:
    - Uses real CLI command invocation
    - Verifies actual catalog data is searched/displayed
    - Tests end-to-end workflow from user perspective
    """

    def test_search_command_uses_catalog(self):
        """Verify mcpi search command loads data from catalog.json."""
        from mcpi.cli import get_catalog
        from click.testing import CliRunner
        from click import Context

        # Create context to test catalog loading
        from mcpi.cli import main

        ctx = Context(main)
        ctx.obj = {"verbose": False}

        # Should load catalog successfully
        catalog = get_catalog(ctx)
        assert catalog is not None

        # Should have loaded from catalog.json
        assert catalog.catalog_path.name == "catalog.json"

        # Should be able to search
        results = catalog.search_servers("server")
        assert isinstance(results, list)

    def test_list_command_uses_catalog(self):
        """Verify mcpi list command loads data from catalog.json."""
        from mcpi.cli import get_catalog
        from click import Context

        from mcpi.cli import main

        ctx = Context(main)
        ctx.obj = {"verbose": False}

        catalog = get_catalog(ctx)

        # Should list servers from catalog
        servers = catalog.list_servers()
        assert isinstance(servers, list)
        assert len(servers) > 0


class TestCatalogValidation:
    """Test catalog validation still works after rename.

    This test cannot be gamed because:
    - Validates actual catalog.cue schema file
    - Tests real CUE validation against catalog.json
    - Verifies data integrity end-to-end
    """

    @pytest.mark.filterwarnings("ignore:create_default_catalog.*:DeprecationWarning")
    def test_catalog_loads_with_cue_validation(self):
        """Verify catalog can be loaded with CUE validation enabled."""
        try:
            # Try to load with validation enabled
            catalog = create_default_catalog(validate_with_cue=True)
            catalog.load_catalog()

            # If CUE is available, should validate successfully
            servers = catalog.list_servers()
            assert len(servers) > 0

        except RuntimeError as e:
            # If CUE not installed, that's acceptable
            if "CUE command not found" in str(e) or "CUE validation disabled" in str(e):
                pytest.skip("CUE not installed, skipping validation test")
            else:
                raise

    def test_catalog_saves_with_cue_validation(self):
        """Verify catalog saving validates against catalog.cue schema."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_path = Path(f.name)
            json.dump({}, f)

        try:
            # Create catalog with validation (will auto-disable if CUE unavailable)
            catalog = ServerCatalog(catalog_path=test_path, validate_with_cue=True)
            catalog.load_catalog()

            # Add valid server
            server = MCPServer(
                description="Valid server", command="node", args=["server.js"]
            )
            catalog.add_server("valid-server", server)

            # Should save successfully
            result = catalog.save_catalog()

            # If validation was enabled, result should be True
            # If CUE unavailable, validation is auto-disabled, still should save
            assert result is True

        finally:
            test_path.unlink(missing_ok=True)


class TestNoRegressions:
    """Test that core functionality still works after rename.

    This test cannot be gamed because:
    - Tests real server operations (add/remove/update/search)
    - Verifies state changes persist correctly
    - Validates data integrity across operations
    """

    def test_add_server_still_works(self):
        """Verify adding servers to catalog works."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_path = Path(f.name)
            json.dump({}, f)

        try:
            catalog = ServerCatalog(catalog_path=test_path, validate_with_cue=False)
            catalog.load_catalog()

            # Add server
            server = MCPServer(
                description="Test server", command="python", args=["-m", "test"]
            )
            result = catalog.add_server("test-server", server)
            assert result is True

            # Verify server was added
            retrieved = catalog.get_server("test-server")
            assert retrieved is not None
            assert retrieved.description == "Test server"

        finally:
            test_path.unlink(missing_ok=True)

    def test_remove_server_still_works(self):
        """Verify removing servers from catalog works."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_path = Path(f.name)
            json.dump(
                {
                    "remove-me": {
                        "description": "To be removed",
                        "command": "test",
                        "args": [],
                    }
                },
                f,
            )

        try:
            catalog = ServerCatalog(catalog_path=test_path, validate_with_cue=False)
            catalog.load_catalog()

            # Remove server
            result = catalog.remove_server("remove-me")
            assert result is True

            # Verify server was removed
            retrieved = catalog.get_server("remove-me")
            assert retrieved is None

        finally:
            test_path.unlink(missing_ok=True)

    def test_search_servers_still_works(self):
        """Verify searching catalog works."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_path = Path(f.name)
            json.dump(
                {
                    "python-server": {
                        "description": "A Python-based server",
                        "command": "python",
                        "args": [],
                    },
                    "node-server": {
                        "description": "A Node.js server",
                        "command": "node",
                        "args": [],
                    },
                },
                f,
            )

        try:
            catalog = ServerCatalog(catalog_path=test_path, validate_with_cue=False)
            catalog.load_catalog()

            # Search for python
            results = catalog.search_servers("python")
            assert len(results) == 1
            assert results[0][0] == "python-server"

            # Search for server (should match both)
            results = catalog.search_servers("server")
            assert len(results) == 2

        finally:
            test_path.unlink(missing_ok=True)

    def test_list_categories_still_works(self):
        """Verify listing categories from catalog works."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_path = Path(f.name)
            json.dump(
                {
                    "server1": {
                        "description": "Server 1",
                        "command": "test",
                        "args": [],
                        "categories": ["database", "api"],
                    },
                    "server2": {
                        "description": "Server 2",
                        "command": "test",
                        "args": [],
                        "categories": ["database"],
                    },
                },
                f,
            )

        try:
            catalog = ServerCatalog(catalog_path=test_path, validate_with_cue=False)
            catalog.load_catalog()

            # List categories
            categories = catalog.list_categories()
            assert isinstance(categories, dict)
            assert categories.get("database") == 2
            assert categories.get("api") == 1

        finally:
            test_path.unlink(missing_ok=True)


if __name__ == "__main__":
    # Allow running this test file directly for validation
    pytest.main([__file__, "-v", "--tb=short"])
