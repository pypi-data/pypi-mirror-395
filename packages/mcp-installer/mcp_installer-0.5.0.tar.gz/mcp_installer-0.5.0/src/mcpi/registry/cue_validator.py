"""CUE schema validation for registry data."""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional


class CUEValidator:
    """Validate registry data against CUE schema."""

    def __init__(self, schema_path: Optional[Path] = None):
        """Initialize with CUE schema path."""
        if schema_path is None:
            # Default to package data directory (now inside the package)
            package_dir = Path(__file__).parent.parent
            schema_path = package_dir / "data" / "catalog.cue"

        self.schema_path = schema_path

        # Check if cue is available
        self._check_cue_available()

    def _check_cue_available(self) -> None:
        """Check if cue command is available."""
        try:
            result = subprocess.run(["cue", "version"], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(
                    "CUE command not found. Please install CUE from https://cuelang.org/docs/install/"
                )
        except FileNotFoundError:
            raise RuntimeError(
                "CUE command not found. Please install CUE from https://cuelang.org/docs/install/"
            )

    def _run_cue_vet(self, file_path: Path) -> tuple[bool, Optional[str]]:
        """Run cue vet on a file and return result.

        Args:
            file_path: Path to JSON file to validate

        Returns:
            (is_valid, error_message) tuple
        """
        try:
            result = subprocess.run(
                ["cue", "vet", str(self.schema_path), str(file_path)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return True, None
            return False, result.stderr.strip()
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def validate(self, data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate data against CUE schema.

        Args:
            data: Registry data to validate

        Returns:
            (is_valid, error_message) tuple
        """
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as f:
                json.dump(data, f, indent=2)
                temp_path = Path(f.name)

            try:
                return self._run_cue_vet(temp_path)
            finally:
                temp_path.unlink(missing_ok=True)
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def validate_file(self, file_path: Path) -> tuple[bool, Optional[str]]:
        """Validate a JSON file against CUE schema.

        Args:
            file_path: Path to JSON file to validate

        Returns:
            (is_valid, error_message) tuple
        """
        return self._run_cue_vet(file_path)
