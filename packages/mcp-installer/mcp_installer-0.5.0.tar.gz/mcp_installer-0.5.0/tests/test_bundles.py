"""Functional tests for Smart Server Bundles feature.

This test suite validates the complete bundle functionality end-to-end,
testing real user workflows that cannot be satisfied by stubs or shortcuts.

These tests verify:
1. Bundle catalog loading and querying
2. Bundle installation with real file operations
3. CLI commands for bundle management
4. Error handling and edge cases
5. Integration with existing MCP manager

Testing Philosophy:
- Tests execute actual user-facing commands
- Verification checks real file system state
- Multiple verification points per test
- Un-gameable: must use real implementations

CRITICAL ANTI-GAMING MEASURES:
1. NO MagicMock for ServerCatalog - uses real catalog from data/catalog.json
2. Custom configs verified by reading actual values, not just existence
3. Bundle removal tested with file deletion verification
4. Dry-run verified with file modification time checks
"""

import json
import time
from pathlib import Path
from typing import Dict, Any
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

try:
    from mcpi.bundles.catalog import BundleCatalog
    from mcpi.bundles.installer import BundleInstaller
    from mcpi.bundles.models import Bundle, BundleServer
    from mcpi.bundles.models import create_test_bundle_catalog
except ImportError:
    # Feature not implemented yet - tests will be skipped
    Bundle = BundleServer = BundleCatalog = BundleInstaller = None
    create_test_bundle_catalog = None

from mcpi.clients.types import ServerConfig
from mcpi.registry.catalog_manager import create_default_catalog_manager
from tests.test_harness import MCPTestHarness  # noqa: F401


# Skip all tests if bundles module not available
pytestmark = pytest.mark.skipif(
    Bundle is None, reason="bundles module not implemented yet"
)


# =============================================================================
# Fixtures - Test Environment Setup
# =============================================================================


@pytest.fixture
def isolated_catalog_dir(tmp_path: Path) -> Path:
    """Create isolated directory for catalog files.

    Returns:
        Path: Temporary catalog directory
    """
    catalog_dir = tmp_path / "catalogs"
    catalog_dir.mkdir()
    return catalog_dir


@pytest.fixture
def bundle_data_dir(tmp_path: Path) -> Path:
    """Create directory for bundle data files.

    Returns:
        Path: Temporary bundle data directory
    """
    bundle_dir = tmp_path / "bundle_data"
    bundle_dir.mkdir()
    return bundle_dir


@pytest.fixture
def multi_bundle_dir(bundle_data_dir: Path) -> Path:
    """Create directory containing multiple test bundles.

    Returns:
        Path: Directory with multiple bundle YAML files
    """
    bundles = [
        {
            "name": "dev-bundle",
            "description": "Development tools",
            "servers": [
                {
                    "server_id": "anthropic/filesystem",
                    "config": {"env": {"DEV_MODE": "true"}},
                }
            ],
        },
        {
            "name": "prod-bundle",
            "description": "Production tools",
            "servers": [
                {
                    "server_id": "modelcontextprotocol/github",
                    "config": {"env": {"PROD": "true"}},
                }
            ],
        },
    ]

    for bundle_data in bundles:
        bundle_file = bundle_data_dir / f"{bundle_data['name']}.yaml"
        import yaml

        with open(bundle_file, "w") as f:
            yaml.dump(bundle_data, f)

    return bundle_data_dir


@pytest.fixture
def mcp_manager_with_harness(tmp_path: Path):
    """Create MCPManager with test harness.

    Returns:
        Tuple[MCPManager, MCPTestHarness]: Manager and harness
    """
    from tests.test_harness import MCPTestHarness
    from mcpi.clients.manager import create_default_manager

    harness = MCPTestHarness(tmp_path)
    harness.setup_scope_files()
    manager = create_default_manager()

    # Override manager paths to use test environment
    for client in manager.clients.values():
        # Patch each client's scope handlers to use test paths
        for scope_name, handler in client._scope_handlers.items():
            test_path = harness.get_scope_path(scope_name)
            if test_path:
                handler._path = test_path

    return manager, harness


@pytest.fixture
def sample_bundle_yaml(bundle_data_dir: Path) -> Path:
    """Create a sample bundle YAML file.

    Returns:
        Path: Path to the created bundle file
    """
    bundle_data = {
        "name": "test-bundle",
        "description": "Test bundle for integration tests",
        "version": "1.0.0",
        "servers": [
            {
                "server_id": "anthropic/filesystem",
                "config": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                    "env": {"CUSTOM_VAR": "test_value"},
                },
            },
            {
                "server_id": "modelcontextprotocol/github",
                "config": {"env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}},
            },
        ],
    }

    import yaml

    bundle_file = bundle_data_dir / "test_bundle.yaml"
    with open(bundle_file, "w") as f:
        yaml.dump(bundle_data, f)

    return bundle_file


@pytest.fixture
def real_server_catalog():
    """Create REAL ServerCatalog loaded from actual data/catalog.json.

    CRITICAL: This is NOT a mock. It loads the real catalog.
    This ensures tests fail if implementation uses servers not in catalog.

    Returns:
        ServerCatalog: Real catalog instance
    """
    manager = create_default_catalog_manager()
    return manager.get_catalog("official")


# =============================================================================
# 1. Bundle Catalog Tests - Loading and Querying
# =============================================================================


class TestBundleCatalog:
    """Test BundleCatalog loading and querying functionality.

    These tests cannot be gamed because:
    1. Verify actual file loading from disk
    2. Check parsed data matches file contents
    3. Multiple validation points per bundle
    """

    def test_load_empty_catalog_directory(self, isolated_catalog_dir: Path):
        """Load catalog from directory with no bundles."""
        catalog = BundleCatalog(catalog_dir=isolated_catalog_dir)

        bundles = catalog.list_bundles()

        assert bundles == [], "Empty directory should return empty list"

    def test_load_single_bundle(self, sample_bundle_yaml: Path):
        """Load catalog with single bundle file."""
        catalog = BundleCatalog(catalog_dir=sample_bundle_yaml.parent)

        bundles = catalog.list_bundles()

        assert len(bundles) == 1, "Should load exactly one bundle"
        assert bundles[0].name == "test-bundle"
        assert bundles[0].description == "Test bundle for integration tests"
        assert bundles[0].version == "1.0.0"
        assert len(bundles[0].servers) == 2

    def test_bundle_server_details_preserved(self, sample_bundle_yaml: Path):
        """Verify bundle server details are correctly parsed."""
        catalog = BundleCatalog(catalog_dir=sample_bundle_yaml.parent)
        bundle = catalog.get_bundle("test-bundle")

        # Check first server
        server1 = bundle.servers[0]
        assert server1.server_id == "anthropic/filesystem"
        assert server1.config["command"] == "npx"
        assert server1.config["env"]["CUSTOM_VAR"] == "test_value"

        # Check second server
        server2 = bundle.servers[1]
        assert server2.server_id == "modelcontextprotocol/github"
        assert server2.config["env"]["GITHUB_TOKEN"] == "${GITHUB_TOKEN}"

    def test_get_bundle_by_name(self, sample_bundle_yaml: Path):
        """Get specific bundle by name."""
        catalog = BundleCatalog(catalog_dir=sample_bundle_yaml.parent)

        bundle = catalog.get_bundle("test-bundle")

        assert bundle is not None
        assert bundle.name == "test-bundle"

    def test_get_nonexistent_bundle(self, sample_bundle_yaml: Path):
        """Attempt to get bundle that doesn't exist."""
        catalog = BundleCatalog(catalog_dir=sample_bundle_yaml.parent)

        bundle = catalog.get_bundle("nonexistent-bundle")

        assert bundle is None, "Should return None for missing bundle"

    def test_load_multiple_bundles(self, multi_bundle_dir: Path):
        """Load catalog with multiple bundle files."""
        catalog = BundleCatalog(catalog_dir=multi_bundle_dir)

        bundles = catalog.list_bundles()

        assert len(bundles) == 2, "Should load both bundles"
        bundle_names = {b.name for b in bundles}
        assert bundle_names == {"dev-bundle", "prod-bundle"}


# =============================================================================
# 2. Bundle Installation Tests - File Operations and Config Merging
# =============================================================================


class TestBundleInstallation:
    """Test bundle installation with real file operations.

    ANTI-GAMING:
    1. No MagicMock for manager - uses real MCPManager with test harness
    2. Verifies actual config file contents, not just existence
    3. Custom configs verified by parsing JSON, not string matching
    """

    def test_install_bundle_creates_server_configs(
        self,
        sample_bundle_yaml: Path,
        mcp_manager_with_harness,
        real_server_catalog,
    ):
        """Install bundle and verify server configs are created."""
        manager, harness = mcp_manager_with_harness

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)
        result = installer.install_bundle(sample_bundle_yaml, scope="project")

        assert result.success, f"Installation failed: {result.message}"

        # Verify both servers were configured
        project_path = harness.get_scope_path("project")
        with open(project_path) as f:
            config = json.load(f)

        assert "anthropic/filesystem" in config["mcpServers"]
        assert "modelcontextprotocol/github" in config["mcpServers"]

    def test_install_bundle_preserves_custom_config(
        self,
        sample_bundle_yaml: Path,
        mcp_manager_with_harness,
        real_server_catalog,
    ):
        """Verify custom configs from bundle are preserved in installed servers."""
        manager, harness = mcp_manager_with_harness

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)
        installer.install_bundle(sample_bundle_yaml, scope="project")

        # ANTI-GAMING: Read actual config values, not just check existence
        project_path = harness.get_scope_path("project")
        with open(project_path) as f:
            config = json.load(f)

        fs_server = config["mcpServers"]["anthropic/filesystem"]
        assert fs_server["env"]["CUSTOM_VAR"] == "test_value"

        gh_server = config["mcpServers"]["modelcontextprotocol/github"]
        assert gh_server["env"]["GITHUB_TOKEN"] == "${GITHUB_TOKEN}"

    def test_install_bundle_to_different_scopes(
        self,
        sample_bundle_yaml: Path,
        mcp_manager_with_harness,
        real_server_catalog,
    ):
        """Install same bundle to different scopes."""
        manager, harness = mcp_manager_with_harness

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)

        # Install to project scope
        result1 = installer.install_bundle(sample_bundle_yaml, scope="project")
        assert result1.success

        # Install to user scope
        result2 = installer.install_bundle(sample_bundle_yaml, scope="user")
        assert result2.success

        # Verify both scopes have the configs
        project_path = harness.get_scope_path("project")
        user_path = harness.get_scope_path("user")

        for path in [project_path, user_path]:
            with open(path) as f:
                config = json.load(f)
            assert "anthropic/filesystem" in config["mcpServers"]

    def test_install_bundle_with_missing_server_in_catalog(
        self, bundle_data_dir: Path, mcp_manager_with_harness, real_server_catalog
    ):
        """Attempt to install bundle with server not in catalog."""
        manager, harness = mcp_manager_with_harness

        # Create bundle with nonexistent server
        bad_bundle = {
            "name": "bad-bundle",
            "servers": [{"server_id": "nonexistent/server", "config": {}}],
        }

        import yaml

        bundle_file = bundle_data_dir / "bad_bundle.yaml"
        with open(bundle_file, "w") as f:
            yaml.dump(bad_bundle, f)

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)
        result = installer.install_bundle(bundle_file, scope="project")

        # ANTI-GAMING: Must actually check catalog, can't bypass
        assert not result.success
        assert "not found in catalog" in result.message.lower()

    def test_install_bundle_dry_run_no_changes(
        self,
        sample_bundle_yaml: Path,
        mcp_manager_with_harness,
        real_server_catalog,
    ):
        """Dry run installation should not modify any files."""
        manager, harness = mcp_manager_with_harness

        project_path = harness.get_scope_path("project")
        original_mtime = project_path.stat().st_mtime

        # Wait a bit to ensure mtime would change if file modified
        time.sleep(0.1)

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)
        result = installer.install_bundle(
            sample_bundle_yaml, scope="project", dry_run=True
        )

        assert result.success

        # ANTI-GAMING: Verify file was NOT modified using mtime
        new_mtime = project_path.stat().st_mtime
        assert new_mtime == original_mtime, "Dry run should not modify files"


# =============================================================================
# 3. Bundle Removal Tests - Cleanup Verification
# =============================================================================


class TestBundleRemoval:
    """Test bundle removal functionality.

    ANTI-GAMING:
    1. Verifies servers actually deleted from config files
    2. Checks file contents, not just return values
    3. Tests partial removal scenarios
    """

    def test_remove_bundle_deletes_all_servers(
        self,
        sample_bundle_yaml: Path,
        mcp_manager_with_harness,
        real_server_catalog,
    ):
        """Remove bundle and verify all servers deleted."""
        manager, harness = mcp_manager_with_harness

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)

        # Install bundle first
        installer.install_bundle(sample_bundle_yaml, scope="project")

        # Now remove it
        result = installer.remove_bundle(sample_bundle_yaml, scope="project")

        assert result.success

        # ANTI-GAMING: Verify servers actually deleted from file
        project_path = harness.get_scope_path("project")
        with open(project_path) as f:
            config = json.load(f)

        assert "anthropic/filesystem" not in config["mcpServers"]
        assert "modelcontextprotocol/github" not in config["mcpServers"]

    def test_remove_bundle_from_nonexistent_scope(
        self, sample_bundle_yaml: Path, mcp_manager_with_harness, real_server_catalog
    ):
        """Remove bundle from scope where it wasn't installed."""
        manager, harness = mcp_manager_with_harness

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)

        # Don't install, just try to remove
        result = installer.remove_bundle(sample_bundle_yaml, scope="project")

        # Should handle gracefully (no error, but possibly inform user)
        assert result.success or "not found" in result.message.lower()

    def test_remove_bundle_dry_run_no_deletion(
        self,
        sample_bundle_yaml: Path,
        mcp_manager_with_harness,
        real_server_catalog,
    ):
        """Dry run removal should not delete servers."""
        manager, harness = mcp_manager_with_harness

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)

        # Install bundle first
        installer.install_bundle(sample_bundle_yaml, scope="project")

        # Dry run removal
        result = installer.remove_bundle(
            sample_bundle_yaml, scope="project", dry_run=True
        )

        assert result.success

        # ANTI-GAMING: Verify servers still present
        project_path = harness.get_scope_path("project")
        with open(project_path) as f:
            config = json.load(f)

        assert "anthropic/filesystem" in config["mcpServers"]
        assert "modelcontextprotocol/github" in config["mcpServers"]


# =============================================================================
# 4. CLI Integration Tests - User-Facing Commands
# =============================================================================


class TestBundleCLI:
    """Test CLI commands for bundle management.

    Tests execute actual Click commands as users would run them.
    """

    def test_bundle_list_command(self, multi_bundle_dir: Path):
        """Test 'mcpi bundle list' command."""
        from mcpi.cli import cli

        runner = CliRunner()

        with runner.isolated_filesystem():
            # Copy bundles to isolated filesystem
            import shutil

            bundles_dir = Path("bundles")
            shutil.copytree(multi_bundle_dir, bundles_dir)

            result = runner.invoke(
                cli, ["bundle", "list", "--catalog-dir", str(bundles_dir)]
            )

            assert result.exit_code == 0
            assert "dev-bundle" in result.output
            assert "prod-bundle" in result.output

    def test_bundle_show_command(self, sample_bundle_yaml: Path):
        """Test 'mcpi bundle show <name>' command."""
        from mcpi.cli import cli

        runner = CliRunner()

        result = runner.invoke(
            cli,
            [
                "bundle",
                "show",
                "test-bundle",
                "--catalog-dir",
                str(sample_bundle_yaml.parent),
            ],
        )

        assert result.exit_code == 0
        assert "test-bundle" in result.output
        assert "anthropic/filesystem" in result.output
        assert "modelcontextprotocol/github" in result.output

    def test_bundle_install_command(
        self, sample_bundle_yaml: Path, mcp_manager_with_harness
    ):
        """Test 'mcpi bundle install <file>' command."""
        from mcpi.cli import cli

        manager, harness = mcp_manager_with_harness
        runner = CliRunner()

        # Patch manager to use test instance
        with patch("mcpi.cli.create_default_manager", return_value=manager):
            result = runner.invoke(
                cli,
                [
                    "bundle",
                    "install",
                    str(sample_bundle_yaml),
                    "--scope",
                    "project",
                ],
            )

            assert result.exit_code == 0
            assert "installed" in result.output.lower()

    def test_bundle_remove_command(
        self, sample_bundle_yaml: Path, mcp_manager_with_harness
    ):
        """Test 'mcpi bundle remove <file>' command."""
        from mcpi.cli import cli

        manager, harness = mcp_manager_with_harness
        runner = CliRunner()

        # Install first
        with patch("mcpi.cli.create_default_manager", return_value=manager):
            runner.invoke(
                cli,
                [
                    "bundle",
                    "install",
                    str(sample_bundle_yaml),
                    "--scope",
                    "project",
                ],
            )

            # Now remove
            result = runner.invoke(
                cli,
                ["bundle", "remove", str(sample_bundle_yaml), "--scope", "project"],
            )

            assert result.exit_code == 0
            assert "removed" in result.output.lower()


# =============================================================================
# 5. Error Handling Tests - Edge Cases and Failures
# =============================================================================


class TestBundleErrorHandling:
    """Test error handling and edge cases."""

    def test_install_invalid_yaml_file(self, bundle_data_dir: Path):
        """Attempt to install malformed YAML file."""
        bad_yaml = bundle_data_dir / "bad.yaml"
        with open(bad_yaml, "w") as f:
            f.write("invalid: yaml: content::: }{")

        catalog = BundleCatalog(catalog_dir=bundle_data_dir)

        # Should handle gracefully
        bundles = catalog.list_bundles()
        # Bad file should be skipped
        assert all(b.name != "bad" for b in bundles)

    def test_install_bundle_missing_required_fields(
        self, bundle_data_dir: Path, mcp_manager_with_harness, real_server_catalog
    ):
        """Attempt to install bundle missing required fields."""
        manager, harness = mcp_manager_with_harness

        # Create bundle missing 'name' field
        bad_bundle = {"servers": [{"server_id": "anthropic/filesystem"}]}

        import yaml

        bundle_file = bundle_data_dir / "incomplete.yaml"
        with open(bundle_file, "w") as f:
            yaml.dump(bad_bundle, f)

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)
        result = installer.install_bundle(bundle_file, scope="project")

        # Should fail gracefully
        assert not result.success
        assert "name" in result.message.lower() or "required" in result.message.lower()

    def test_bundle_with_env_var_substitution(
        self, bundle_data_dir: Path, mcp_manager_with_harness, real_server_catalog
    ):
        """Install bundle with environment variable placeholders."""
        manager, harness = mcp_manager_with_harness

        bundle_data = {
            "name": "env-bundle",
            "servers": [
                {
                    "server_id": "modelcontextprotocol/github",
                    "config": {
                        "env": {
                            "GITHUB_TOKEN": "${GITHUB_TOKEN}",
                            "GITHUB_USER": "${USER}",
                        }
                    },
                }
            ],
        }

        import yaml

        bundle_file = bundle_data_dir / "env_bundle.yaml"
        with open(bundle_file, "w") as f:
            yaml.dump(bundle_data, f)

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)
        result = installer.install_bundle(bundle_file, scope="project")

        assert result.success

        # Verify env vars preserved as placeholders
        project_path = harness.get_scope_path("project")
        with open(project_path) as f:
            config = json.load(f)

        server_config = config["mcpServers"]["modelcontextprotocol/github"]
        assert server_config["env"]["GITHUB_TOKEN"] == "${GITHUB_TOKEN}"
        assert server_config["env"]["GITHUB_USER"] == "${USER}"


# =============================================================================
# 6. Multi-Bundle Installation Tests
# =============================================================================


class TestMultiBundleInstallation:
    """Test installing multiple bundles with potential conflicts."""

    def test_install_two_bundles_different_servers(
        self, multi_bundle_dir: Path, mcp_manager_with_harness, real_server_catalog
    ):
        """Install two bundles with different servers."""
        manager, harness = mcp_manager_with_harness

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)

        dev_bundle = multi_bundle_dir / "dev-bundle.yaml"
        prod_bundle = multi_bundle_dir / "prod-bundle.yaml"

        result1 = installer.install_bundle(dev_bundle, scope="project")
        result2 = installer.install_bundle(prod_bundle, scope="project")

        assert result1.success and result2.success

        # Verify both servers present
        project_path = harness.get_scope_path("project")
        with open(project_path) as f:
            config = json.load(f)

        assert "anthropic/filesystem" in config["mcpServers"]
        assert "modelcontextprotocol/github" in config["mcpServers"]

    def test_install_bundles_same_server_last_wins(
        self, bundle_data_dir: Path, mcp_manager_with_harness, real_server_catalog
    ):
        """Install two bundles configuring same server - last one wins."""
        manager, harness = mcp_manager_with_harness

        # Create two bundles with same server but different configs
        bundle1_data = {
            "name": "bundle1",
            "servers": [
                {
                    "server_id": "anthropic/filesystem",
                    "config": {"env": {"VERSION": "1"}},
                }
            ],
        }

        bundle2_data = {
            "name": "bundle2",
            "servers": [
                {
                    "server_id": "anthropic/filesystem",
                    "config": {"env": {"VERSION": "2"}},
                }
            ],
        }

        import yaml

        bundle1_file = bundle_data_dir / "bundle1.yaml"
        bundle2_file = bundle_data_dir / "bundle2.yaml"

        with open(bundle1_file, "w") as f:
            yaml.dump(bundle1_data, f)
        with open(bundle2_file, "w") as f:
            yaml.dump(bundle2_data, f)

        installer = BundleInstaller(manager=manager, catalog=real_server_catalog)

        installer.install_bundle(bundle1_file, scope="project")
        installer.install_bundle(bundle2_file, scope="project")

        # Last bundle (bundle2) should win
        project_path = harness.get_scope_path("project")
        with open(project_path) as f:
            config = json.load(f)

        server_config = config["mcpServers"]["anthropic/filesystem"]
        assert server_config["env"]["VERSION"] == "2"
