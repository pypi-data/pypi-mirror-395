"""Bundle catalog for loading and managing server bundles."""

import json
from pathlib import Path
from typing import List, Optional, Tuple

from mcpi.bundles.models import Bundle


class BundleCatalog:
    """Catalog of available MCP server bundles.

    Bundles are loaded from JSON files in a bundles directory.
    Each JSON file defines one bundle with its metadata and server list.
    """

    def __init__(self, bundles_dir: Path):
        """Initialize bundle catalog.

        Args:
            bundles_dir: Directory containing bundle JSON files (required for DI/testability)
        """
        self.bundles_dir = bundles_dir
        self._bundles: dict[str, Bundle] = {}
        self._loaded = False

    def load_bundles(self) -> None:
        """Load all bundles from the bundles directory.

        Loads all .json files from bundles_dir. Invalid files are skipped
        with a warning, allowing valid bundles to still load.
        """
        # Start with empty catalog
        self._bundles = {}

        # If directory doesn't exist, just keep empty catalog
        if not self.bundles_dir.exists():
            self._loaded = True
            return

        # Load all .json files from directory
        for bundle_file in self.bundles_dir.glob("*.json"):
            try:
                # Read and parse JSON
                with open(bundle_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Validate with Pydantic and create Bundle
                bundle = Bundle(**data)

                # Store by bundle name
                self._bundles[bundle.name] = bundle

            except json.JSONDecodeError as e:
                # Skip files with invalid JSON
                print(f"Warning: Skipping invalid JSON file {bundle_file.name}: {e}")
                continue

            except Exception as e:
                # Skip files that fail Pydantic validation
                print(f"Warning: Skipping invalid bundle file {bundle_file.name}: {e}")
                continue

        self._loaded = True

    def get_bundle(self, bundle_id: str) -> Optional[Bundle]:
        """Get a bundle by ID (name).

        Args:
            bundle_id: Bundle identifier (e.g., 'web-dev', 'data-science')

        Returns:
            Bundle object if found, None otherwise
        """
        # Ensure bundles are loaded
        if not self._loaded:
            self.load_bundles()

        return self._bundles.get(bundle_id)

    def list_bundles(self) -> List[Tuple[str, Bundle]]:
        """List all available bundles.

        Returns:
            List of (bundle_id, Bundle) tuples, sorted by bundle ID
        """
        # Ensure bundles are loaded
        if not self._loaded:
            self.load_bundles()

        # Return sorted list of (id, bundle) tuples
        return sorted(self._bundles.items(), key=lambda x: x[0])


def create_default_bundle_catalog() -> BundleCatalog:
    """Create BundleCatalog with default production bundles directory.

    This factory function provides the default behavior for loading
    built-in bundles shipped with MCPI.

    Returns:
        BundleCatalog instance configured with production bundles directory
    """
    # Calculate production bundles directory path (now inside the package)
    package_dir = Path(__file__).parent.parent
    bundles_dir = package_dir / "data" / "bundles"

    catalog = BundleCatalog(bundles_dir=bundles_dir)
    catalog.load_bundles()
    return catalog


def create_test_bundle_catalog(test_bundles_dir: Path) -> BundleCatalog:
    """Create BundleCatalog with custom test bundles directory.

    This factory function makes it easy to create test catalogs with
    isolated test data.

    Args:
        test_bundles_dir: Path to directory containing test bundle files

    Returns:
        BundleCatalog instance configured with test bundles directory
    """
    catalog = BundleCatalog(bundles_dir=test_bundles_dir)
    catalog.load_bundles()
    return catalog
