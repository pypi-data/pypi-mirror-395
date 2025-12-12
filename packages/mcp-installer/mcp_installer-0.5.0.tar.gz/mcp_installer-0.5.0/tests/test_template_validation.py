"""Comprehensive validation tests for all template files.

Tests verify that all template YAML files:
- Load and parse correctly
- Validate against Pydantic models
- Have all required fields
- Apply correctly with user values
- Validate user input correctly
"""

import pytest
from pathlib import Path

from mcpi.templates.template_manager import create_default_template_manager
from mcpi.templates.models import ServerTemplate, PromptDefinition


class TestTemplateFileLoading:
    """Test all template YAML files load and validate correctly."""

    def test_all_templates_load_successfully(self):
        """All 12 templates should load without errors."""
        manager = create_default_template_manager()
        manager.load_templates()

        # Count all templates across all servers
        total_templates = sum(
            len(templates) for templates in manager._templates.values()
        )
        assert total_templates == 12, f"Expected 12 templates, found {total_templates}"

    def test_postgres_templates_load(self):
        """All PostgreSQL templates load successfully."""
        manager = create_default_template_manager()
        templates = manager.list_templates("postgres")

        assert len(templates) == 3
        template_names = {t.name for t in templates}
        assert template_names == {
            "local-development",
            "docker",
            "production",
        }

    def test_github_templates_load(self):
        """All GitHub templates load successfully."""
        manager = create_default_template_manager()
        templates = manager.list_templates("github")

        assert len(templates) == 3
        template_names = {t.name for t in templates}
        assert template_names == {
            "personal-full-access",
            "read-only",
            "public-repos",
        }

    def test_filesystem_templates_load(self):
        """All filesystem templates load successfully."""
        manager = create_default_template_manager()
        templates = manager.list_templates("filesystem")

        assert len(templates) == 3
        template_names = {t.name for t in templates}
        assert template_names == {
            "project-files",
            "user-documents",
            "custom-directories",
        }

    def test_slack_templates_load(self):
        """All Slack templates load successfully."""
        manager = create_default_template_manager()
        templates = manager.list_templates("slack")

        assert len(templates) == 2
        template_names = {t.name for t in templates}
        assert template_names == {
            "bot-token",
            "limited-channels",
        }

    def test_brave_search_templates_load(self):
        """All Brave Search templates load successfully."""
        manager = create_default_template_manager()
        templates = manager.list_templates("brave-search")

        assert len(templates) == 1
        template_names = {t.name for t in templates}
        assert template_names == {"api-key"}


class TestTemplateStructure:
    """Test that all templates have required fields and proper structure."""

    @pytest.fixture
    def all_templates(self):
        """Get all templates for testing."""
        manager = create_default_template_manager()
        manager.load_templates()
        templates = []
        for server_templates in manager._templates.values():
            templates.extend(server_templates.values())
        return templates

    def test_all_templates_have_descriptions(self, all_templates):
        """All templates must have descriptions."""
        for template in all_templates:
            assert template.description, f"Template {template.name} missing description"
            assert (
                len(template.description) > 10
            ), f"Template {template.name} description too short"

    def test_all_templates_have_valid_priority(self, all_templates):
        """All templates must have valid priority values."""
        valid_priorities = {"high", "medium", "low"}
        for template in all_templates:
            assert (
                template.priority in valid_priorities
            ), f"Template {template.name} has invalid priority: {template.priority}"

    def test_all_templates_have_valid_scopes(self, all_templates):
        """All templates must have valid scope values."""
        valid_scopes = {
            "project-mcp",
            "project-local",
            "user-mcp",
            "user-internal",
        }
        for template in all_templates:
            assert (
                template.scope in valid_scopes
            ), f"Template {template.name} has invalid scope: {template.scope}"

    def test_all_templates_have_command_and_args(self, all_templates):
        """All templates must have command and args in config."""
        for template in all_templates:
            assert (
                "command" in template.config
            ), f"Template {template.name} missing command"
            assert "args" in template.config, f"Template {template.name} missing args"
            assert isinstance(
                template.config["args"], list
            ), f"Template {template.name} args must be a list"

    def test_secrets_are_marked_correctly(self, all_templates):
        """Prompts for sensitive data should be marked as 'secret' type."""
        secret_keywords = ["token", "key", "password", "secret", "api"]
        for template in all_templates:
            for prompt in template.prompts:
                # If prompt name contains secret keyword, type should be 'secret'
                has_secret_keyword = any(
                    keyword in prompt.name.lower() for keyword in secret_keywords
                )
                if has_secret_keyword:
                    assert prompt.type == "secret", (
                        f"Template {template.name} prompt {prompt.name} "
                        f"contains secret keyword but type is {prompt.type}"
                    )

    def test_required_prompts_have_descriptions(self, all_templates):
        """All required prompts must have descriptions."""
        for template in all_templates:
            for prompt in template.prompts:
                if prompt.required:
                    assert prompt.description, (
                        f"Template {template.name} prompt {prompt.name} "
                        f"is required but has no description"
                    )


class TestTemplateApplication:
    """Test applying templates generates valid configurations."""

    def test_postgres_local_development_template(self):
        """Apply PostgreSQL local-development template with mock values."""
        manager = create_default_template_manager()
        template = manager.get_template("postgres", "local-development")
        assert template is not None

        user_values = {
            "POSTGRES_DATABASE": "myapp_dev",
            "POSTGRES_USER": "postgres",
        }

        config = manager.apply_template(template, user_values)

        assert config.command == "npx"
        assert config.args == ["-y", "@modelcontextprotocol/server-postgres"]
        assert config.env["POSTGRES_DATABASE"] == "myapp_dev"
        assert config.env["POSTGRES_USER"] == "postgres"

    def test_github_personal_full_access_template(self):
        """Apply GitHub personal-full-access template with mock values."""
        manager = create_default_template_manager()
        template = manager.get_template("github", "personal-full-access")
        assert template is not None

        user_values = {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_123456789012345678901234567890123456",
        }

        config = manager.apply_template(template, user_values)

        assert config.command == "npx"
        assert config.args == ["-y", "@modelcontextprotocol/server-github"]
        assert (
            config.env["GITHUB_PERSONAL_ACCESS_TOKEN"]
            == user_values["GITHUB_PERSONAL_ACCESS_TOKEN"]
        )

    def test_filesystem_project_files_template(self):
        """Apply filesystem project-files template with mock values."""
        manager = create_default_template_manager()
        template = manager.get_template("filesystem", "project-files")
        assert template is not None

        user_values = {
            "PROJECT_DIRECTORY": "/Users/test/myproject",
        }

        config = manager.apply_template(template, user_values)

        assert config.command == "npx"
        assert config.args == ["-y", "@modelcontextprotocol/server-filesystem"]
        assert config.env["PROJECT_DIRECTORY"] == "/Users/test/myproject"

    def test_slack_bot_token_template(self):
        """Apply Slack bot-token template with mock values."""
        manager = create_default_template_manager()
        template = manager.get_template("slack", "bot-token")
        assert template is not None

        user_values = {
            "SLACK_BOT_TOKEN": "xoxb-0000000000-0000000000-FAKEFAKEFAKEFAKEFAKEFAK",
            "SLACK_TEAM_ID": "T1234567890",
        }

        config = manager.apply_template(template, user_values)

        assert config.command == "npx"
        assert config.args == ["-y", "@modelcontextprotocol/server-slack"]
        assert config.env["SLACK_BOT_TOKEN"] == user_values["SLACK_BOT_TOKEN"]
        assert config.env["SLACK_TEAM_ID"] == user_values["SLACK_TEAM_ID"]

    def test_brave_search_api_key_template(self):
        """Apply Brave Search api-key template with mock values."""
        manager = create_default_template_manager()
        template = manager.get_template("brave-search", "api-key")
        assert template is not None

        user_values = {
            "BRAVE_API_KEY": "BSA1234567890abcdefghijklmnopqrstuvwxyz",
        }

        config = manager.apply_template(template, user_values)

        assert config.command == "npx"
        assert config.args == ["-y", "@modelcontextprotocol/server-brave-search"]
        assert config.env["BRAVE_API_KEY"] == user_values["BRAVE_API_KEY"]


class TestValidationRules:
    """Test validation rules in templates work correctly."""

    def test_port_validation_valid(self):
        """Port prompts accept valid port numbers."""
        prompt = PromptDefinition(
            name="PORT",
            description="Port number",
            type="port",
            required=True,
        )

        # Valid ports
        for port in ["80", "443", "5432", "8080", "65535", "1"]:
            is_valid, error = prompt.validate_value(port)
            assert is_valid, f"Port {port} should be valid, got error: {error}"

    def test_port_validation_invalid(self):
        """Port prompts reject invalid port numbers."""
        prompt = PromptDefinition(
            name="PORT",
            description="Port number",
            type="port",
            required=True,
        )

        # Invalid ports
        invalid_ports = [
            ("0", "out of range"),
            ("65536", "out of range"),
            ("-1", "out of range"),
            ("abc", "not a number"),
            ("80.5", "not an integer"),
        ]

        for port, reason in invalid_ports:
            is_valid, error = prompt.validate_value(port)
            assert not is_valid, f"Port {port} should be invalid ({reason})"

    def test_url_validation_valid(self):
        """URL prompts accept valid URLs."""
        prompt = PromptDefinition(
            name="URL",
            description="URL",
            type="url",
            required=True,
        )

        # Valid URLs
        valid_urls = [
            "http://localhost",
            "https://example.com",
            "http://192.168.1.1",
            "https://api.example.com/v1",
            "ws://localhost:8080",
            "wss://secure.example.com",
        ]

        for url in valid_urls:
            is_valid, error = prompt.validate_value(url)
            assert is_valid, f"URL {url} should be valid, got error: {error}"

    def test_url_validation_invalid(self):
        """URL prompts reject invalid URLs."""
        prompt = PromptDefinition(
            name="URL",
            description="URL",
            type="url",
            required=True,
        )

        # Invalid URLs
        invalid_urls = [
            "ftp://example.com",  # Wrong scheme
            "example.com",  # Missing scheme
            "//example.com",  # Missing scheme
            "localhost",  # Missing scheme
        ]

        for url in invalid_urls:
            is_valid, error = prompt.validate_value(url)
            assert not is_valid, f"URL {url} should be invalid"

    def test_path_validation_valid(self):
        """Path prompts accept valid paths."""
        prompt = PromptDefinition(
            name="PATH",
            description="File path",
            type="path",
            required=True,
        )

        # Valid paths (format-wise, don't need to exist)
        valid_paths = [
            "/Users/test/myproject",
            "/home/user/documents",
            "/var/log",
            "C:\\Users\\test\\project",
            "./relative/path",
        ]

        for path in valid_paths:
            is_valid, error = prompt.validate_value(path)
            assert is_valid, f"Path {path} should be valid, got error: {error}"

    def test_path_validation_invalid(self):
        """Path prompts reject invalid paths."""
        prompt = PromptDefinition(
            name="PATH",
            description="File path",
            type="path",
            required=True,
        )

        # Invalid paths
        is_valid, error = prompt.validate_value("")
        assert not is_valid, "Empty path should be invalid"

        is_valid, error = prompt.validate_value("   ")
        assert not is_valid, "Whitespace-only path should be invalid"

        is_valid, error = prompt.validate_value("/path/with\x00null")
        assert not is_valid, "Path with null byte should be invalid"

    def test_required_field_validation(self):
        """Required prompts reject empty values."""
        prompt = PromptDefinition(
            name="REQUIRED_FIELD",
            description="Required field",
            type="string",
            required=True,
        )

        is_valid, error = prompt.validate_value("")
        assert not is_valid, "Required field should reject empty value"
        assert "required" in error.lower()

    def test_optional_field_validation(self):
        """Optional prompts accept empty values."""
        prompt = PromptDefinition(
            name="OPTIONAL_FIELD",
            description="Optional field",
            type="string",
            required=False,
        )

        is_valid, error = prompt.validate_value("")
        assert is_valid, "Optional field should accept empty value"

    def test_regex_pattern_validation_valid(self):
        """Regex patterns validate correctly."""
        prompt = PromptDefinition(
            name="DATABASE_NAME",
            description="Database name",
            type="string",
            required=True,
            validation_pattern="^[a-zA-Z0-9_]+$",
        )

        # Valid database names
        valid_names = ["mydb", "my_database", "DB123", "test_db_01"]
        for name in valid_names:
            is_valid, error = prompt.validate_value(name)
            assert is_valid, f"Database name {name} should be valid, got error: {error}"

    def test_regex_pattern_validation_invalid(self):
        """Regex patterns reject invalid values."""
        prompt = PromptDefinition(
            name="DATABASE_NAME",
            description="Database name",
            type="string",
            required=True,
            validation_pattern="^[a-zA-Z0-9_]+$",
        )

        # Invalid database names
        invalid_names = ["my-db", "my db", "db!", "my.db"]
        for name in invalid_names:
            is_valid, error = prompt.validate_value(name)
            assert not is_valid, f"Database name {name} should be invalid"


class TestServerSpecificValidation:
    """Test server-specific validation rules in templates."""

    def test_postgres_connection_format(self):
        """PostgreSQL templates should support connection string format."""
        manager = create_default_template_manager()

        # Test all postgres templates have database name prompt
        for template_name in ["local-development", "docker", "production"]:
            template = manager.get_template("postgres", template_name)
            assert template is not None

            # Should have POSTGRES_DATABASE prompt
            prompt_names = {p.name for p in template.prompts}
            assert (
                "POSTGRES_DATABASE" in prompt_names
            ), f"Template {template_name} missing POSTGRES_DATABASE prompt"

    def test_github_token_format_validation(self):
        """GitHub templates should validate token format."""
        manager = create_default_template_manager()
        template = manager.get_template("github", "personal-full-access")
        assert template is not None

        # Find token prompt
        token_prompt = next(p for p in template.prompts if "TOKEN" in p.name)

        # Valid GitHub tokens (exact format from template regex)
        # Pattern: ^(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82})$
        valid_tokens = [
            "ghp_123456789012345678901234567890123456",  # ghp_ + 36 chars = 40 total
            "github_pat_" + "A" * 82,  # github_pat_ + 82 chars = 93 total
        ]

        for token in valid_tokens:
            is_valid, error = token_prompt.validate_value(token)
            assert is_valid, f"Token {token} should be valid, got error: {error}"

        # Invalid GitHub tokens
        invalid_tokens = [
            "ghp_short",  # Too short
            "invalid_format",  # Wrong prefix
            "xoxb-0000000000-0000000000-FAKEFAKEFAKEFAKEFAKEFAK",  # Slack token
        ]

        for token in invalid_tokens:
            is_valid, error = token_prompt.validate_value(token)
            assert not is_valid, f"Token {token} should be invalid"

    def test_filesystem_path_arguments(self):
        """Filesystem templates should have path arguments."""
        manager = create_default_template_manager()

        for template_name in ["project-files", "user-documents", "custom-directories"]:
            template = manager.get_template("filesystem", template_name)
            assert template is not None

            # Should have at least one path prompt
            path_prompts = [p for p in template.prompts if p.type == "path"]
            assert (
                len(path_prompts) > 0
            ), f"Template {template_name} should have path prompts"

    def test_slack_token_and_team_id_format(self):
        """Slack templates should validate token and team ID format."""
        manager = create_default_template_manager()
        template = manager.get_template("slack", "bot-token")
        assert template is not None

        # Find token and team ID prompts
        prompts_by_name = {p.name: p for p in template.prompts}
        token_prompt = prompts_by_name["SLACK_BOT_TOKEN"]
        team_id_prompt = prompts_by_name["SLACK_TEAM_ID"]

        # Valid token format
        valid_token = "xoxb-0000000000-0000000000-FAKEFAKEFAKEFAKEFAKEFAK"
        is_valid, error = token_prompt.validate_value(valid_token)
        assert is_valid, f"Valid Slack token rejected: {error}"

        # Invalid token formats
        invalid_tokens = [
            "xoxp-1234567890-1234567890-abcdefghijklmnopqrstuvwx",  # Wrong prefix
            "xoxb-invalid",  # Wrong format
            "ghp_123456789012345678901234567890123456",  # GitHub token
        ]

        for token in invalid_tokens:
            is_valid, error = token_prompt.validate_value(token)
            assert not is_valid, f"Invalid token {token} should be rejected"

        # Valid team ID format
        valid_team_id = "T1234567890"
        is_valid, error = team_id_prompt.validate_value(valid_team_id)
        assert is_valid, f"Valid team ID rejected: {error}"

        # Invalid team ID formats
        invalid_team_ids = ["1234567890", "t1234567890", "W1234567890"]
        for team_id in invalid_team_ids:
            is_valid, error = team_id_prompt.validate_value(team_id)
            assert not is_valid, f"Invalid team ID {team_id} should be rejected"

    def test_brave_search_api_key_handling(self):
        """Brave Search templates should handle API key correctly."""
        manager = create_default_template_manager()
        template = manager.get_template("brave-search", "api-key")
        assert template is not None

        # Find API key prompt
        api_key_prompt = next(p for p in template.prompts if "API_KEY" in p.name)

        # Should be marked as secret
        assert api_key_prompt.type == "secret", "API key should be secret type"

        # Should be required
        assert api_key_prompt.required, "API key should be required"

        # Valid API key formats (alphanumeric, hyphens, underscores)
        valid_keys = [
            "BSA1234567890",
            "api-key-with-hyphens",
            "api_key_with_underscores",
            "MixedCase123",
        ]

        for key in valid_keys:
            is_valid, error = api_key_prompt.validate_value(key)
            assert is_valid, f"API key {key} should be valid, got error: {error}"

        # Invalid API key formats
        invalid_keys = [
            "key with spaces",
            "key@with!special#chars",
            "",  # Empty
        ]

        for key in invalid_keys:
            is_valid, error = api_key_prompt.validate_value(key)
            assert not is_valid, f"API key {key} should be invalid"


class TestTemplateConsistency:
    """Test consistency across all templates."""

    @pytest.fixture
    def all_templates(self):
        """Get all templates for testing."""
        manager = create_default_template_manager()
        manager.load_templates()
        templates = []
        for server_templates in manager._templates.values():
            templates.extend(server_templates.values())
        return templates

    def test_all_npx_templates_use_y_flag(self, all_templates):
        """All npx-based templates should use -y flag."""
        for template in all_templates:
            if template.config["command"] == "npx":
                assert (
                    "-y" in template.config["args"]
                ), f"Template {template.name} uses npx but missing -y flag"

    def test_template_names_follow_convention(self, all_templates):
        """Template names should follow kebab-case convention."""
        for template in all_templates:
            # Should be lowercase with hyphens
            assert (
                template.name.islower() or "-" in template.name
            ), f"Template name {template.name} should be lowercase/kebab-case"
            # Should not have spaces
            assert (
                " " not in template.name
            ), f"Template name {template.name} should not have spaces"

    def test_high_priority_templates_are_simplest(self, all_templates):
        """High priority templates should generally be simpler (fewer prompts)."""
        templates_by_server = {}
        for template in all_templates:
            if template.server_id not in templates_by_server:
                templates_by_server[template.server_id] = []
            templates_by_server[template.server_id].append(template)

        # For each server, high priority templates should not have MORE prompts
        # than medium/low priority templates (generally)
        for server_id, templates in templates_by_server.items():
            if len(templates) <= 1:
                continue

            high_priority = [t for t in templates if t.priority == "high"]
            other_priority = [t for t in templates if t.priority != "high"]

            if high_priority and other_priority:
                avg_high_prompts = sum(len(t.prompts) for t in high_priority) / len(
                    high_priority
                )
                avg_other_prompts = sum(len(t.prompts) for t in other_priority) / len(
                    other_priority
                )

                # High priority templates should generally be simpler
                # Allow some tolerance (within 2 prompts)
                assert avg_high_prompts <= avg_other_prompts + 2, (
                    f"Server {server_id}: high priority templates should be simpler, "
                    f"but have {avg_high_prompts:.1f} prompts vs {avg_other_prompts:.1f}"
                )

    def test_all_templates_have_notes(self, all_templates):
        """All templates should have helpful notes."""
        for template in all_templates:
            # Notes can be empty for very simple templates, but most should have them
            if template.prompts:  # If has prompts, should have notes
                assert (
                    template.notes
                ), f"Template {template.name} has prompts but no notes"
