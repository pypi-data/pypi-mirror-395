"""Template manager for loading and applying configuration templates."""

from pathlib import Path
from typing import Optional

import yaml

from mcpi.clients.types import ServerConfig

from .models import ServerTemplate


class TemplateManager:
    """Manages configuration templates for MCP servers.

    Loads templates from YAML files organized by server ID and provides
    methods to list, retrieve, and apply templates with user-provided values.
    """

    def __init__(self, template_dir: Path):
        """Initialize template manager.

        Args:
            template_dir: Directory containing template files organized as
                         {server_id}/{template_name}.yaml
        """
        self.template_dir = template_dir
        self._templates: dict[str, dict[str, ServerTemplate]] = {}
        self._loaded = False

    def load_templates(self) -> None:
        """Load all templates from template directory.

        Templates are organized as: data/templates/{server_id}/{template_name}.yaml
        This method is idempotent - calling it multiple times is safe.
        """
        if self._loaded:
            return

        if not self.template_dir.exists():
            # Template directory doesn't exist yet - that's OK
            self._loaded = True
            return

        # Scan each server subdirectory
        for server_dir in self.template_dir.iterdir():
            if not server_dir.is_dir():
                continue

            server_id = server_dir.name
            self._templates[server_id] = {}

            # Load all YAML files in this server's directory
            for template_file in server_dir.glob("*.yaml"):
                try:
                    template = self._load_template_file(template_file)
                    if template.server_id != server_id:
                        # Template file is in wrong directory
                        continue
                    self._templates[server_id][template.name] = template
                except Exception:
                    # Skip invalid templates - don't fail entire load
                    continue

        self._loaded = True

    def _load_template_file(self, template_path: Path) -> ServerTemplate:
        """Load a single template file.

        Args:
            template_path: Path to template YAML file

        Returns:
            Parsed ServerTemplate

        Raises:
            Exception: If file cannot be parsed or validated
        """
        with open(template_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return ServerTemplate(**data)

    def list_templates(self, server_id: str) -> list[ServerTemplate]:
        """List available templates for a server.

        Args:
            server_id: Server ID to list templates for

        Returns:
            List of templates sorted by priority (high, medium, low)
        """
        if not self._loaded:
            self.load_templates()

        templates = self._templates.get(server_id, {}).values()

        # Sort by priority: high -> medium -> low
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(templates, key=lambda t: priority_order.get(t.priority, 99))

    def get_template(
        self, server_id: str, template_name: str
    ) -> Optional[ServerTemplate]:
        """Get specific template by server ID and name.

        Args:
            server_id: Server ID
            template_name: Template name

        Returns:
            ServerTemplate if found, None otherwise
        """
        if not self._loaded:
            self.load_templates()

        return self._templates.get(server_id, {}).get(template_name)

    def apply_template(
        self, template: ServerTemplate, user_values: dict[str, str]
    ) -> ServerConfig:
        """Apply template with user-provided values to create server configuration.

        Merges static template configuration with dynamic user values to produce
        a complete ServerConfig ready for installation.

        Args:
            template: Template to apply
            user_values: User-provided values for prompts (keys are prompt names)

        Returns:
            Complete ServerConfig with merged configuration
        """
        # Start with static config from template
        env = dict(template.config.get("env", {}))

        # Merge in user-provided values
        env.update(user_values)

        return ServerConfig(
            command=template.config["command"],
            args=template.config["args"],
            env=env,
            type=template.config.get("type", "stdio"),
        )


def create_default_template_manager() -> TemplateManager:
    """Create template manager with default template directory.

    Returns:
        TemplateManager configured with package's template directory
    """
    # Navigate from this file to package data/templates (now inside the package)
    package_dir = Path(__file__).parent.parent
    template_dir = package_dir / "data" / "templates"
    return TemplateManager(template_dir=template_dir)


def create_test_template_manager(test_dir: Path) -> TemplateManager:
    """Create template manager for testing.

    Args:
        test_dir: Test directory containing templates

    Returns:
        TemplateManager configured for testing
    """
    return TemplateManager(template_dir=test_dir)
