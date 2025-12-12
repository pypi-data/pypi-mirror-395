"""Unit tests for template manager."""

from pathlib import Path

import pytest
import yaml

from mcpi.templates.models import PromptDefinition, ServerTemplate
from mcpi.templates.template_manager import (
    TemplateManager,
    create_default_template_manager,
    create_test_template_manager,
)


class TestTemplateManager:
    """Tests for TemplateManager class."""

    @pytest.fixture
    def template_dir(self, tmp_path: Path) -> Path:
        """Create a temporary template directory."""
        return tmp_path / "templates"

    @pytest.fixture
    def manager(self, template_dir: Path) -> TemplateManager:
        """Create a template manager for testing."""
        return TemplateManager(template_dir=template_dir)

    @pytest.fixture
    def sample_template(self) -> dict:
        """Sample template data."""
        return {
            "name": "production",
            "description": "Production PostgreSQL setup",
            "server_id": "postgres",
            "scope": "user-mcp",
            "priority": "high",
            "config": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres"],
                "env": {"POSTGRES_PORT": "5432"},
            },
            "prompts": [
                {
                    "name": "POSTGRES_HOST",
                    "description": "Database host",
                    "type": "string",
                    "required": True,
                }
            ],
            "notes": "Production setup with TLS",
        }

    def test_init(self, template_dir: Path):
        """Test manager initialization."""
        manager = TemplateManager(template_dir=template_dir)
        assert manager.template_dir == template_dir
        assert manager._templates == {}
        assert manager._loaded is False

    def test_load_templates_empty_directory(self, manager: TemplateManager):
        """Test loading from non-existent directory."""
        manager.load_templates()
        assert manager._loaded is True
        assert manager._templates == {}

    def test_load_templates_single_server(
        self, manager: TemplateManager, template_dir: Path, sample_template: dict
    ):
        """Test loading templates for a single server."""
        # Create directory structure
        postgres_dir = template_dir / "postgres"
        postgres_dir.mkdir(parents=True)

        # Write template file
        template_file = postgres_dir / "production.yaml"
        with open(template_file, "w") as f:
            yaml.dump(sample_template, f)

        # Load templates
        manager.load_templates()

        assert manager._loaded is True
        assert "postgres" in manager._templates
        assert "production" in manager._templates["postgres"]

        template = manager._templates["postgres"]["production"]
        assert isinstance(template, ServerTemplate)
        assert template.name == "production"
        assert template.server_id == "postgres"

    def test_load_templates_multiple_servers(
        self, manager: TemplateManager, template_dir: Path
    ):
        """Test loading templates for multiple servers."""
        # Create multiple server directories with templates
        for server_id in ["postgres", "github", "slack"]:
            server_dir = template_dir / server_id
            server_dir.mkdir(parents=True)

            template_data = {
                "name": "default",
                "description": f"Default {server_id} setup",
                "server_id": server_id,
                "scope": "user-mcp",
                "priority": "medium",
                "config": {"command": "npx", "args": ["-y", f"@mcp/{server_id}"]},
            }

            template_file = server_dir / "default.yaml"
            with open(template_file, "w") as f:
                yaml.dump(template_data, f)

        manager.load_templates()

        assert len(manager._templates) == 3
        assert all(
            server_id in manager._templates
            for server_id in ["postgres", "github", "slack"]
        )

    def test_load_templates_idempotent(
        self, manager: TemplateManager, template_dir: Path, sample_template: dict
    ):
        """Test that load_templates is idempotent."""
        # Create template
        postgres_dir = template_dir / "postgres"
        postgres_dir.mkdir(parents=True)
        template_file = postgres_dir / "production.yaml"
        with open(template_file, "w") as f:
            yaml.dump(sample_template, f)

        # Load multiple times
        manager.load_templates()
        first_load = manager._templates.copy()

        manager.load_templates()
        second_load = manager._templates

        assert first_load == second_load

    def test_load_templates_skip_invalid(
        self, manager: TemplateManager, template_dir: Path, sample_template: dict
    ):
        """Test that invalid templates are skipped without failing entire load."""
        postgres_dir = template_dir / "postgres"
        postgres_dir.mkdir(parents=True)

        # Valid template
        valid_file = postgres_dir / "valid.yaml"
        with open(valid_file, "w") as f:
            sample_template_copy = dict(sample_template)
            sample_template_copy["name"] = "valid"
            yaml.dump(sample_template_copy, f)

        # Invalid template (missing required fields)
        invalid_data = {
            "name": "invalid",
            "description": "Invalid template",
            # Missing server_id, scope, priority, config
        }
        invalid_file = postgres_dir / "invalid.yaml"
        with open(invalid_file, "w") as f:
            yaml.dump(invalid_data, f)

        # Should load valid template, skip invalid
        manager.load_templates()

        assert "postgres" in manager._templates
        assert "valid" in manager._templates["postgres"]
        assert "invalid" not in manager._templates["postgres"]

    def test_load_templates_skip_wrong_directory(
        self, manager: TemplateManager, template_dir: Path, sample_template: dict
    ):
        """Test that templates in wrong directory are skipped."""
        # Template says server_id is "postgres" but it's in "github" directory
        github_dir = template_dir / "github"
        github_dir.mkdir(parents=True)

        wrong_location_file = github_dir / "production.yaml"
        with open(wrong_location_file, "w") as f:
            yaml.dump(sample_template, f)  # server_id is "postgres"

        manager.load_templates()

        assert "github" in manager._templates
        assert len(manager._templates["github"]) == 0

    def test_load_templates_skip_non_directories(
        self, manager: TemplateManager, template_dir: Path
    ):
        """Test that non-directory files are skipped."""
        template_dir.mkdir(parents=True)

        # Create a file (not directory) in templates dir
        readme_file = template_dir / "README.md"
        readme_file.write_text("# Templates\n")

        # Should not crash
        manager.load_templates()
        assert manager._loaded is True

    def test_list_templates_empty(self, manager: TemplateManager):
        """Test listing templates for non-existent server."""
        templates = manager.list_templates("nonexistent")
        assert templates == []

    def test_list_templates_sorted_by_priority(
        self, manager: TemplateManager, template_dir: Path
    ):
        """Test that templates are sorted by priority."""
        postgres_dir = template_dir / "postgres"
        postgres_dir.mkdir(parents=True)

        # Create templates with different priorities
        priorities = [("low", "low"), ("high", "high"), ("medium", "medium")]
        for name, priority in priorities:
            template_data = {
                "name": name,
                "description": f"{name} setup",
                "server_id": "postgres",
                "scope": "user-mcp",
                "priority": priority,
                "config": {"command": "npx", "args": []},
            }
            template_file = postgres_dir / f"{name}.yaml"
            with open(template_file, "w") as f:
                yaml.dump(template_data, f)

        templates = manager.list_templates("postgres")

        # Should be sorted: high, medium, low
        assert len(templates) == 3
        assert templates[0].priority == "high"
        assert templates[1].priority == "medium"
        assert templates[2].priority == "low"

    def test_get_template_exists(
        self, manager: TemplateManager, template_dir: Path, sample_template: dict
    ):
        """Test getting an existing template."""
        postgres_dir = template_dir / "postgres"
        postgres_dir.mkdir(parents=True)
        template_file = postgres_dir / "production.yaml"
        with open(template_file, "w") as f:
            yaml.dump(sample_template, f)

        template = manager.get_template("postgres", "production")

        assert template is not None
        assert template.name == "production"
        assert template.server_id == "postgres"

    def test_get_template_not_exists(self, manager: TemplateManager):
        """Test getting non-existent template."""
        template = manager.get_template("postgres", "nonexistent")
        assert template is None

    def test_apply_template_static_only(self, manager: TemplateManager):
        """Test applying template with only static config."""
        template = ServerTemplate(
            name="basic",
            description="Basic setup",
            server_id="github",
            scope="user-mcp",
            priority="low",
            config={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_API_URL": "https://api.github.com"},
            },
        )

        config = manager.apply_template(template, {})

        assert config.command == "npx"
        assert config.args == ["-y", "@modelcontextprotocol/server-github"]
        assert config.env == {"GITHUB_API_URL": "https://api.github.com"}
        assert config.type == "stdio"

    def test_apply_template_with_user_values(self, manager: TemplateManager):
        """Test applying template with user-provided values."""
        template = ServerTemplate(
            name="production",
            description="Production setup",
            server_id="postgres",
            scope="user-mcp",
            priority="high",
            config={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres"],
                "env": {"POSTGRES_PORT": "5432"},
            },
            prompts=[
                PromptDefinition(
                    name="POSTGRES_HOST",
                    description="Database host",
                    type="string",
                    required=True,
                ),
                PromptDefinition(
                    name="POSTGRES_DB",
                    description="Database name",
                    type="string",
                    required=True,
                ),
            ],
        )

        user_values = {
            "POSTGRES_HOST": "db.example.com",
            "POSTGRES_DB": "production_db",
        }

        config = manager.apply_template(template, user_values)

        assert config.command == "npx"
        assert config.env["POSTGRES_PORT"] == "5432"  # Static from template
        assert config.env["POSTGRES_HOST"] == "db.example.com"  # User value
        assert config.env["POSTGRES_DB"] == "production_db"  # User value

    def test_apply_template_user_values_override(self, manager: TemplateManager):
        """Test that user values override static template values."""
        template = ServerTemplate(
            name="custom",
            description="Custom setup",
            server_id="test",
            scope="user-mcp",
            priority="medium",
            config={
                "command": "npx",
                "args": [],
                "env": {"PORT": "8080"},  # Default port
            },
        )

        user_values = {"PORT": "9000"}  # Override

        config = manager.apply_template(template, user_values)

        assert config.env["PORT"] == "9000"  # User value wins

    def test_apply_template_with_type(self, manager: TemplateManager):
        """Test applying template with custom type."""
        template = ServerTemplate(
            name="sse",
            description="SSE setup",
            server_id="test",
            scope="user-mcp",
            priority="low",
            config={
                "command": "npx",
                "args": [],
                "type": "sse",  # Custom type
            },
        )

        config = manager.apply_template(template, {})

        assert config.type == "sse"


class TestFactoryFunctions:
    """Tests for factory functions."""

    def test_create_default_template_manager(self):
        """Test creating default template manager."""
        manager = create_default_template_manager()

        assert isinstance(manager, TemplateManager)
        assert manager.template_dir.name == "templates"
        assert "data" in str(manager.template_dir)

    def test_create_test_template_manager(self, tmp_path: Path):
        """Test creating test template manager."""
        test_dir = tmp_path / "test_templates"
        manager = create_test_template_manager(test_dir)

        assert isinstance(manager, TemplateManager)
        assert manager.template_dir == test_dir
