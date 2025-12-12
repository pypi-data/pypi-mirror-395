"""Multi-catalog management for MCP servers.

This module provides CatalogManager for managing multiple server catalogs
(official and local). Implements Phase 1 of multi-catalog support with
dependency injection patterns.

Key Features:
- Manages two catalogs: official (built-in) and local (user)
- Lazy loading: catalogs loaded only when accessed
- Case-insensitive catalog lookup
- Search across multiple catalogs with ordering
- DIP-compliant: all dependencies injected via constructor
"""

import warnings
from pathlib import Path
from typing import Optional

from .catalog import MCPServer, ServerCatalog


class CatalogInfo:
    """Metadata about a catalog.

    Attributes:
        name: Catalog name (e.g., "official", "local")
        type: Catalog type (e.g., "builtin", "local")
        path: Path to catalog file
        description: Human-readable description
        server_count: Number of servers in catalog
    """

    def __init__(
        self,
        name: str,
        type: str,
        path: Path,
        description: str,
        server_count: int,
    ):
        self.name = name
        self.type = type
        self.path = path
        self.description = description
        self.server_count = server_count


class CatalogManager:
    """Manages multiple MCP server catalogs.

    This manager handles two catalogs:
    - official: Built-in catalog from package data
    - local: User's custom catalog in ~/.mcpi/catalogs/local

    Features:
    - Lazy loading: catalogs loaded only when first accessed
    - Case-insensitive lookup: "official", "OFFICIAL", "Official" all work
    - Search across all catalogs with priority ordering
    - DIP-compliant: paths injected via constructor

    Example:
        >>> manager = CatalogManager(
        ...     official_path=Path("data/catalog.json"),
        ...     local_path=Path("~/.mcpi/catalogs/local/catalog.json")
        ... )
        >>> catalog = manager.get_catalog("official")
        >>> results = manager.search_all("filesystem")
    """

    def __init__(self, official_path: Path, local_path: Path):
        """Initialize catalog manager with paths.

        Args:
            official_path: Path to official catalog JSON file
            local_path: Path to local catalog JSON file
        """
        self.official_path = official_path
        self.local_path = local_path

        # Lazy loading: catalogs not loaded until accessed
        self._official: Optional[ServerCatalog] = None
        self._local: Optional[ServerCatalog] = None
        self._default_catalog = "official"

    def get_catalog(self, name: str) -> Optional[ServerCatalog]:
        """Get catalog by name (case-insensitive).

        Args:
            name: Catalog name ("official", "local", etc.)

        Returns:
            ServerCatalog instance or None if not found
        """
        # Normalize to lowercase for case-insensitive lookup
        name_lower = name.lower()

        if name_lower == "official":
            if self._official is None:
                # Check if official catalog exists (it should always exist)
                if not self.official_path.exists():
                    raise FileNotFoundError(
                        f"Official catalog not found at {self.official_path}"
                    )

                # Lazy load official catalog
                self._official = ServerCatalog(
                    catalog_path=self.official_path, validate_with_cue=True
                )
                self._official.load_catalog()
            return self._official

        elif name_lower == "local":
            if self._local is None:
                # Lazy load local catalog
                self._local = ServerCatalog(
                    catalog_path=self.local_path,
                    validate_with_cue=False,  # Local catalog is user-controlled
                )
                self._local.load_catalog()
            return self._local

        # Unknown catalog name
        return None

    def get_default_catalog(self) -> ServerCatalog:
        """Get default catalog (official).

        Returns:
            ServerCatalog instance
        """
        catalog = self.get_catalog(self._default_catalog)
        assert catalog is not None, "Default catalog should always exist"
        return catalog

    def list_catalogs(self) -> list[CatalogInfo]:
        """List all available catalogs.

        Returns:
            List of CatalogInfo objects (official, then local)
        """
        catalogs = []

        # Official catalog
        official = self.get_catalog("official")
        if official:
            catalogs.append(
                CatalogInfo(
                    name="official",
                    type="builtin",
                    path=self.official_path,
                    description="Official MCP server catalog",
                    server_count=len(official.list_servers()),
                )
            )

        # Local catalog
        local = self.get_catalog("local")
        if local:
            catalogs.append(
                CatalogInfo(
                    name="local",
                    type="local",
                    path=self.local_path,
                    description="Your custom MCP servers",
                    server_count=len(local.list_servers()),
                )
            )

        return catalogs

    def search_all(self, query: str) -> list[tuple[str, str, MCPServer]]:
        """Search all catalogs for servers matching query.

        Results ordered by catalog priority (official first), then alphabetically
        by server_id within each catalog. No deduplication: same server_id in
        multiple catalogs will appear multiple times.

        Args:
            query: Search query string

        Returns:
            List of (catalog_name, server_id, server_config) tuples
        """
        results = []

        # Search catalogs in priority order (official first, then local)
        for catalog_name in ["official", "local"]:
            catalog = self.get_catalog(catalog_name)
            if catalog:
                # Search this catalog
                catalog_results = catalog.search_servers(query)

                # Sort results alphabetically by server_id within this catalog
                sorted_results = sorted(catalog_results, key=lambda x: x[0])

                # Add results with catalog name
                for server_id, server in sorted_results:
                    results.append((catalog_name, server_id, server))

        return results


# Factory Functions for DIP Compliance


def create_default_catalog_manager() -> CatalogManager:
    """Create CatalogManager with default paths.

    Official catalog: package data/catalog.json
    Local catalog: ~/.mcpi/catalogs/local/catalog.json

    Auto-initializes local catalog directory and empty catalog.json if they
    don't exist. Handles errors gracefully with warnings.

    Returns:
        CatalogManager instance

    Raises:
        FileNotFoundError: If official catalog doesn't exist
    """
    # Official catalog (now inside the package)
    package_dir = Path(__file__).parent.parent
    official_path = package_dir / "data" / "catalog.json"

    if not official_path.exists():
        raise FileNotFoundError(
            f"Official catalog not found at {official_path}. "
            "This indicates a corrupted installation."
        )

    # Local catalog (new user directory)
    local_dir = Path.home() / ".mcpi" / "catalogs" / "local"
    local_path = local_dir / "catalog.json"

    # Auto-initialize local catalog directory and file
    try:
        local_dir.mkdir(parents=True, exist_ok=True)

        if not local_path.exists():
            # Create empty catalog
            local_path.write_text("{}", encoding="utf-8")
    except (PermissionError, OSError) as e:
        # Warn but don't fail - local catalog is optional
        warnings.warn(
            f"Could not initialize local catalog at {local_path}: {e}. "
            "Local catalog functionality will be limited.",
            UserWarning,
            stacklevel=2,
        )

    return CatalogManager(official_path=official_path, local_path=local_path)


def create_test_catalog_manager(
    official_path: Path,
    local_path: Path,
) -> CatalogManager:
    """Create CatalogManager with custom paths for testing.

    Args:
        official_path: Path to test official catalog
        local_path: Path to test local catalog

    Returns:
        CatalogManager instance
    """
    return CatalogManager(official_path=official_path, local_path=local_path)
