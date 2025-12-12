"""Registry validation utilities."""

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic import ValidationError

from mcpi.registry.catalog import MCPServer, ServerRegistry


class RegistryValidator:
    """Validates MCP server registry data."""

    def __init__(self):
        """Initialize the validator."""
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_registry_file(self, registry_path: Path) -> bool:
        """Validate a registry file.

        Args:
            registry_path: Path to registry JSON/YAML file

        Returns:
            True if valid, False otherwise
        """
        self.errors.clear()
        self.warnings.clear()

        if not registry_path.exists():
            self.errors.append(f"Registry file does not exist: {registry_path}")
            return False

        try:
            if registry_path.suffix.lower() in [".yaml", ".yml"]:
                with open(registry_path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            else:
                with open(registry_path, encoding="utf-8") as f:
                    data = json.load(f)
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            self.errors.append(f"Invalid file format: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading registry file: {e}")
            return False

        return self.validate_registry_data(data)

    def validate_registry_data(self, data: Dict[str, Any]) -> bool:
        """Validate registry data structure.

        Args:
            data: Registry data dictionary

        Returns:
            True if valid, False otherwise
        """
        try:
            registry = ServerRegistry(**data)

            # Validate individual servers
            for server_id, server in registry.servers.items():
                self._validate_server_semantics(server)

            # Check for duplicate IDs (handled by dict structure now)
            if len(registry.servers) == 0:
                self.warnings.append("Registry contains no servers")

            return len(self.errors) == 0

        except ValidationError as e:
            for error in e.errors():
                loc = " -> ".join(str(x) for x in error["loc"])
                self.errors.append(f"Validation error at {loc}: {error['msg']}")
            return False
        except Exception as e:
            self.errors.append(f"Unexpected error validating registry: {e}")
            return False

    def validate_single_server(self, server_data: Dict[str, Any]) -> bool:
        """Validate a single server entry.

        Args:
            server_data: Server data dictionary

        Returns:
            True if valid, False otherwise
        """
        try:
            server = MCPServer(**server_data)
            self._validate_server_semantics(server)
            return len(self.errors) == 0

        except ValidationError as e:
            for error in e.errors():
                loc = " -> ".join(str(x) for x in error["loc"])
                self.errors.append(f"Validation error at {loc}: {error['msg']}")
            return False
        except Exception as e:
            self.errors.append(f"Unexpected error validating server: {e}")
            return False

    def _validate_server_semantics(self, server: MCPServer) -> None:
        """Perform semantic validation on a server.

        Args:
            server: Validated MCPServer instance
        """
        server_ref = f"Server '{server.id}'"

        # Check command/package combinations
        if server.command == "npx" and not server.package:
            self.errors.append(f"{server_ref}: npx command requires a package")

        # Validate npx usage
        if server.install_method == "npx" and server.command != "npx":
            self.warnings.append(
                f"{server_ref}: install_method is 'npx' but command is '{server.command}'"
            )

        # Check for required config without defaults
        if server.required_config and len(server.required_config) > 5:
            self.warnings.append(
                f"{server_ref}: Many required parameters ({len(server.required_config)})"
            )

        # Validate repository URL
        if server.repository and not (
            server.repository.startswith("https://")
            or server.repository.startswith("http://")
            or server.repository.startswith("git://")
        ):
            self.warnings.append(
                f"{server_ref}: Repository URL should start with https://, http://, or git://"
            )

        # Check categories
        if not server.categories:
            self.warnings.append(f"{server_ref}: No categories specified")
        elif len(server.categories) > 5:
            self.warnings.append(
                f"{server_ref}: Many categories ({len(server.categories)})"
            )

        # Validate package names for known methods
        if server.install_method == "npm" and server.package.startswith("pip:"):
            self.errors.append(
                f"{server_ref}: NPM package should not start with 'pip:'"
            )

        if server.install_method == "pip" and server.package.startswith("@"):
            self.warnings.append(f"{server_ref}: PIP package should not start with '@'")

        # Check for conflicting configurations
        if server.install_package and server.install_package == server.package:
            self.warnings.append(
                f"{server_ref}: install_package is same as package (redundant)"
            )

    def get_validation_report(self) -> Dict[str, Any]:
        """Get detailed validation report.

        Returns:
            Dictionary containing validation results
        """
        return {
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors.copy(),
            "warnings": self.warnings.copy(),
        }

    def print_validation_report(self) -> None:
        """Print validation report to console."""
        if not self.errors and not self.warnings:
            print("✅ Registry validation passed with no issues")
            return

        if self.errors:
            print(f"❌ Registry validation failed with {len(self.errors)} errors:")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"⚠️  Registry validation has {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")

        if not self.errors:
            print("✅ Registry is valid despite warnings")
