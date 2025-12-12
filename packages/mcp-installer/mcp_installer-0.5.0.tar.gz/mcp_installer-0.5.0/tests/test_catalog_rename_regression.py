"""Regression tests for registry→catalog rename.

These tests validate CURRENT functionality (before rename) and can be
easily updated after the rename to verify behavior is preserved.

CRITICAL: These tests should PASS NOW (before rename).
After rename, update API calls but keep same assertions.

Test Strategy:
- Test current functionality with registry_path, load_registry(), etc.
- After rename: update to catalog_path, load_catalog(), etc.
- Assertions stay the same - we're testing behavior, not names
- Provides confidence that rename doesn't break anything

Gaming Resistance:
- Tests real file loading (not mocks)
- Verifies actual data parsing
- Checks complete workflows
- Cannot pass with stubs
"""

import json
import pytest
import warnings
from pathlib import Path
from mcpi.registry.catalog import (
    ServerCatalog,
    MCPServer,
    ServerRegistry,
    create_default_catalog,
    create_test_catalog,
)


class TestCurrentRegistryBehavior:
    """Test current behavior before rename.

    These tests validate that the current implementation works correctly.
    After rename, update method/parameter names but keep assertions.
    """

    @pytest.fixture
    def test_registry_data(self):
        """Sample registry data for testing."""
        return {
            "test-server-1": {
                "description": "First test server",
                "command": "npx",
                "args": ["-y", "test-package-1"],
                "repository": "https://github.com/test/server1",
                "categories": ["testing", "example"],
            },
            "test-server-2": {
                "description": "Second test server",
                "command": "python",
                "args": ["-m", "test.module"],
                "repository": None,
                "categories": ["testing"],
            },
        }

    @pytest.fixture
    def test_registry_file(self, tmp_path, test_registry_data):
        """Create a temporary registry file with test data."""
        registry_path = tmp_path / "test_registry.json"
        registry_path.write_text(json.dumps(test_registry_data, indent=2))
        return registry_path

    @pytest.fixture
    def empty_registry_file(self, tmp_path):
        """Create an empty but valid registry file."""
        registry_path = tmp_path / "empty_registry.json"
        registry_path.write_text(json.dumps({}))
        return registry_path

    def test_server_catalog_loads_from_file(self, test_registry_file):
        """Verify ServerCatalog can load servers from registry file.

        CURRENT: Uses registry_path parameter and load_registry() method
        AFTER RENAME: Update to catalog_path parameter and load_catalog() method
        ASSERTION: Same - verify servers load successfully
        """
        # BEFORE RENAME: Use current API
        catalog = ServerCatalog(
            catalog_path=test_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME: Update to this:
        # catalog = ServerCatalog(catalog_path=test_registry_file, validate_with_cue=False)
        # catalog.load_catalog()

        # Assertions stay the same - verify behavior
        servers = catalog.list_servers()
        assert len(servers) == 2, "Should load 2 servers from file"

        server_ids = [sid for sid, _ in servers]
        assert "test-server-1" in server_ids
        assert "test-server-2" in server_ids

    def test_server_catalog_get_server_by_id(self, test_registry_file):
        """Verify get_server() retrieves correct server data.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - verify server data is correct
        """
        # BEFORE RENAME
        catalog = ServerCatalog(
            catalog_path=test_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        # Assertions stay the same
        server = catalog.get_server("test-server-1")
        assert server is not None
        assert server.description == "First test server"
        assert server.command == "npx"
        assert server.args == ["-y", "test-package-1"]
        assert server.repository == "https://github.com/test/server1"
        assert "testing" in server.categories
        assert "example" in server.categories

    def test_server_catalog_search(self, test_registry_file):
        """Verify search_servers() finds matching servers.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - verify search works correctly

        NOTE: search_servers() searches server_id and description fields only.
        """
        # BEFORE RENAME
        catalog = ServerCatalog(
            catalog_path=test_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        # Assertions stay the same
        # Search for "Second" which appears in test-server-2's description
        results = catalog.search_servers("Second")
        assert len(results) == 1
        server_id, server = results[0]
        assert server_id == "test-server-2"
        assert "Second" in server.description

    def test_server_catalog_list_categories(self, test_registry_file):
        """Verify list_categories() returns category counts.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - verify categories are counted correctly
        """
        # BEFORE RENAME
        catalog = ServerCatalog(
            catalog_path=test_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        # Assertions stay the same
        categories = catalog.list_categories()
        assert categories["testing"] == 2  # Both servers have "testing"
        assert categories["example"] == 1  # Only server-1 has "example"

    def test_server_catalog_add_server(self, test_registry_file):
        """Verify add_server() adds new server to catalog.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - verify add operation works
        """
        # BEFORE RENAME
        catalog = ServerCatalog(
            catalog_path=test_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        # Add a new server
        new_server = MCPServer(
            description="Third test server",
            command="node",
            args=["server.js"],
            repository=None,
            categories=["nodejs"],
        )
        result = catalog.add_server("test-server-3", new_server)

        # Assertions stay the same
        assert result is True, "Should successfully add new server"

        # Verify server was added
        servers = catalog.list_servers()
        assert len(servers) == 3

        added = catalog.get_server("test-server-3")
        assert added is not None
        assert added.description == "Third test server"

    def test_server_catalog_remove_server(self, test_registry_file):
        """Verify remove_server() removes server from catalog.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - verify remove operation works
        """
        # BEFORE RENAME
        catalog = ServerCatalog(
            catalog_path=test_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        # Remove a server
        result = catalog.remove_server("test-server-1")

        # Assertions stay the same
        assert result is True, "Should successfully remove server"

        # Verify server was removed
        servers = catalog.list_servers()
        assert len(servers) == 1

        removed = catalog.get_server("test-server-1")
        assert removed is None

    def test_server_catalog_update_server(self, test_registry_file):
        """Verify update_server() updates existing server.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - verify update operation works
        """
        # BEFORE RENAME
        catalog = ServerCatalog(
            catalog_path=test_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        # Update a server
        updated = MCPServer(
            description="Updated description",
            command="npx",
            args=["-y", "updated-package"],
            repository="https://github.com/test/updated",
            categories=["updated"],
        )
        result = catalog.update_server("test-server-1", updated)

        # Assertions stay the same
        assert result is True, "Should successfully update server"

        # Verify server was updated
        server = catalog.get_server("test-server-1")
        assert server.description == "Updated description"
        assert server.args == ["-y", "updated-package"]

    def test_server_catalog_save_and_reload(self, test_registry_file, tmp_path):
        """Verify save/reload cycle preserves data.

        CURRENT: Uses load_registry() and save_registry()
        AFTER RENAME: Update to load_catalog() and save_catalog()
        ASSERTION: Same - verify data persists correctly
        """
        # BEFORE RENAME
        catalog = ServerCatalog(
            catalog_path=test_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        # Add a server and save
        new_server = MCPServer(
            description="Server to persist",
            command="npx",
            args=["-y", "persist"],
        )
        catalog.add_server("persistent-server", new_server)

        # Save to new location
        save_path = tmp_path / "saved_registry.json"
        catalog.catalog_path = save_path

        # BEFORE RENAME
        result = catalog.save_catalog()

        # AFTER RENAME: result = catalog.save_catalog()
        # AFTER RENAME: catalog.catalog_path = save_path

        # Assertions stay the same
        assert result is True, "Should successfully save"
        assert save_path.exists(), "File should exist after save"

        # Reload from saved file
        # BEFORE RENAME
        catalog2 = ServerCatalog(catalog_path=save_path, validate_with_cue=False)
        catalog2.load_catalog()

        # AFTER RENAME:
        # catalog2 = ServerCatalog(catalog_path=save_path, validate_with_cue=False)
        # catalog2.load_catalog()

        # Verify data was preserved
        servers = catalog2.list_servers()
        assert len(servers) == 3  # Original 2 + 1 added

        persisted = catalog2.get_server("persistent-server")
        assert persisted is not None
        assert persisted.description == "Server to persist"

    def test_server_catalog_handles_empty_file(self, empty_registry_file):
        """Verify catalog handles empty file gracefully.

        CURRENT: Uses registry_path and load_registry()
        AFTER RENAME: Update to catalog_path and load_catalog()
        ASSERTION: Same - verify empty file handling
        """
        # BEFORE RENAME
        catalog = ServerCatalog(
            catalog_path=empty_registry_file, validate_with_cue=False
        )
        catalog.load_catalog()

        # AFTER RENAME:
        # catalog = ServerCatalog(catalog_path=empty_registry_file, validate_with_cue=False)
        # catalog.load_catalog()

        # Assertions stay the same
        servers = catalog.list_servers()
        assert len(servers) == 0, "Empty file should result in empty catalog"

        server = catalog.get_server("any-id")
        assert server is None

    def test_server_catalog_handles_missing_file(self, tmp_path):
        """Verify catalog handles missing file gracefully.

        CURRENT: Uses registry_path and load_registry()
        AFTER RENAME: Update to catalog_path and load_catalog()
        ASSERTION: Same - verify missing file handling
        """
        missing_file = tmp_path / "nonexistent.json"
        assert not missing_file.exists()

        # BEFORE RENAME
        catalog = ServerCatalog(catalog_path=missing_file, validate_with_cue=False)
        catalog.load_catalog()

        # AFTER RENAME:
        # catalog = ServerCatalog(catalog_path=missing_file, validate_with_cue=False)
        # catalog.load_catalog()

        # Assertions stay the same
        servers = catalog.list_servers()
        assert len(servers) == 0, "Missing file should result in empty catalog"


class TestFactoryFunctionsBehavior:
    """Test factory functions before rename.

    After rename, these functions will reference catalog.json instead of registry.json.
    """

    @pytest.mark.filterwarnings("ignore:create_default_catalog.*:DeprecationWarning")
    def test_create_default_catalog_loads_production_data(self):
        """Verify create_default_catalog() loads from data/catalog.json.

        CURRENT: Loads from data/catalog.json
        AFTER RENAME: Will load from data/catalog.json
        ASSERTION: Same - verify production data loads
        """
        catalog = create_default_catalog()

        # Verify it's configured with production path
        # BEFORE RENAME
        assert catalog.catalog_path.name == "catalog.json"
        assert "data" in str(catalog.catalog_path)

        # AFTER RENAME: assert catalog.catalog_path.name == "catalog.json"

        # Verify it can load servers (production data exists)
        servers = catalog.list_servers()
        assert len(servers) > 0, "Production registry should have servers"

    def test_create_test_catalog_uses_custom_path(self, tmp_path):
        """Verify create_test_catalog() accepts custom path.

        CURRENT: Uses registry_path parameter
        AFTER RENAME: Will use catalog_path parameter
        ASSERTION: Same - verify custom path is used
        """
        test_data = {
            "factory-test": {
                "description": "Factory test server",
                "command": "npx",
                "args": ["-y", "factory-test"],
            }
        }
        test_file = tmp_path / "factory_test.json"
        test_file.write_text(json.dumps(test_data))

        catalog = create_test_catalog(test_file)

        # BEFORE RENAME
        assert catalog.catalog_path == test_file

        # AFTER RENAME: assert catalog.catalog_path == test_file

        # Verify it loads from the test file
        servers = catalog.list_servers()
        assert len(servers) == 1

        server = catalog.get_server("factory-test")
        assert server is not None
        assert server.description == "Factory test server"


class TestProductionDataIntegrity:
    """Test that actual production data loads correctly.

    These tests verify the real data/catalog.json file.
    After rename, update path to data/catalog.json.
    """

    def test_production_registry_file_exists(self):
        """Verify production registry file exists.

        CURRENT: data/catalog.json
        AFTER RENAME: data/catalog.json
        ASSERTION: Same - file exists
        """
        # BEFORE RENAME
        registry_path = Path(__file__).parent.parent / "src" / "mcpi" / "data" / "catalog.json"
        assert registry_path.exists(), "Production registry file must exist"

        # AFTER RENAME:
        # catalog_path = Path(__file__).parent.parent / "src" / "mcpi" / "data" / "catalog.json"
        # assert catalog_path.exists(), "Production catalog file must exist"

    def test_production_registry_is_valid_json(self):
        """Verify production registry has valid JSON syntax.

        CURRENT: data/catalog.json
        AFTER RENAME: data/catalog.json
        ASSERTION: Same - valid JSON
        """
        # BEFORE RENAME
        registry_path = Path(__file__).parent.parent / "src" / "mcpi" / "data" / "catalog.json"

        # AFTER RENAME:
        # catalog_path = Path(__file__).parent.parent / "src" / "mcpi" / "data" / "catalog.json"

        with open(registry_path, encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), "Registry should be a dictionary"
        assert len(data) > 0, "Registry should contain servers"

    def test_production_registry_loads_into_catalog(self):
        """Verify production registry loads into ServerCatalog.

        CURRENT: Uses registry_path and load_registry()
        AFTER RENAME: Use catalog_path and load_catalog()
        ASSERTION: Same - data loads successfully
        """
        # BEFORE RENAME
        registry_path = Path(__file__).parent.parent / "src" / "mcpi" / "data" / "catalog.json"
        catalog = ServerCatalog(catalog_path=registry_path, validate_with_cue=False)
        catalog.load_catalog()

        # AFTER RENAME:
        # catalog_path = Path(__file__).parent.parent / "src" / "mcpi" / "data" / "catalog.json"
        # catalog = ServerCatalog(catalog_path=catalog_path, validate_with_cue=False)
        # catalog.load_catalog()

        # Assertions stay the same
        servers = catalog.list_servers()
        assert len(servers) > 0, "Should load servers from production file"

        # Verify all servers have required fields
        for server_id, server in servers:
            assert server.description, f"Server {server_id} must have description"
            assert server.command, f"Server {server_id} must have command"
            assert isinstance(
                server.args, list
            ), f"Server {server_id} args must be list"

    def test_production_registry_all_servers_valid(self):
        """Verify all servers in production registry are valid.

        CURRENT: Uses registry_path and load_registry()
        AFTER RENAME: Use catalog_path and load_catalog()
        ASSERTION: Same - all servers valid
        """
        # BEFORE RENAME
        registry_path = Path(__file__).parent.parent / "src" / "mcpi" / "data" / "catalog.json"
        catalog = ServerCatalog(catalog_path=registry_path, validate_with_cue=False)
        catalog.load_catalog()

        # AFTER RENAME:
        # catalog_path = Path(__file__).parent.parent / "src" / "mcpi" / "data" / "catalog.json"
        # catalog = ServerCatalog(catalog_path=catalog_path, validate_with_cue=False)
        # catalog.load_catalog()

        servers = catalog.list_servers()

        for server_id, server in servers:
            # Required fields
            assert (
                server.description.strip()
            ), f"{server_id}: description cannot be empty"
            assert server.command.strip(), f"{server_id}: command cannot be empty"

            # Args must be list
            assert isinstance(server.args, list), f"{server_id}: args must be a list"

            # Repository is optional but must be string or None
            assert server.repository is None or isinstance(
                server.repository, str
            ), f"{server_id}: repository must be string or None"


class TestEdgeCases:
    """Test edge cases and error handling.

    These verify error handling works correctly.
    After rename, update method names but keep error assertions.
    """

    def test_invalid_json_raises_error(self, tmp_path):
        """Verify invalid JSON raises clear error.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - proper error raised
        """
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("{ invalid json")

        # BEFORE RENAME
        catalog = ServerCatalog(catalog_path=invalid_file, validate_with_cue=False)

        # AFTER RENAME:
        # catalog = ServerCatalog(catalog_path=invalid_file, validate_with_cue=False)

        with pytest.raises(RuntimeError) as exc_info:
            # BEFORE RENAME
            catalog.load_catalog()
            # AFTER RENAME: catalog.load_catalog()

        error_msg = str(exc_info.value)
        assert "Failed to load" in error_msg
        assert str(invalid_file) in error_msg

    def test_add_duplicate_server_fails(self, tmp_path):
        """Verify adding duplicate server ID fails.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - duplicate add fails
        """
        test_data = {
            "existing": {"description": "Existing server", "command": "npx", "args": []}
        }
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps(test_data))

        # BEFORE RENAME
        catalog = ServerCatalog(catalog_path=test_file, validate_with_cue=False)
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        # Try to add server with existing ID
        duplicate = MCPServer(description="Duplicate", command="npx", args=[])
        result = catalog.add_server("existing", duplicate)

        assert result is False, "Should fail to add duplicate server ID"

    def test_remove_nonexistent_server_fails(self, tmp_path):
        """Verify removing non-existent server fails.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - remove non-existent fails
        """
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps({}))

        # BEFORE RENAME
        catalog = ServerCatalog(catalog_path=test_file, validate_with_cue=False)
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        result = catalog.remove_server("nonexistent")
        assert result is False, "Should fail to remove non-existent server"

    def test_update_nonexistent_server_fails(self, tmp_path):
        """Verify updating non-existent server fails.

        CURRENT: Uses load_registry()
        AFTER RENAME: Update to load_catalog()
        ASSERTION: Same - update non-existent fails
        """
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps({}))

        # BEFORE RENAME
        catalog = ServerCatalog(catalog_path=test_file, validate_with_cue=False)
        catalog.load_catalog()

        # AFTER RENAME: catalog.load_catalog()

        updated = MCPServer(description="Updated", command="npx", args=[])
        result = catalog.update_server("nonexistent", updated)
        assert result is False, "Should fail to update non-existent server"


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
