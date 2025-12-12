"""Unit tests for template models."""

import pytest
from pydantic import ValidationError

from mcpi.templates.models import PromptDefinition, ServerTemplate


class TestPromptDefinition:
    """Tests for PromptDefinition model."""

    def test_valid_prompt(self):
        """Test creating a valid prompt definition."""
        prompt = PromptDefinition(
            name="POSTGRES_HOST",
            description="Database host",
            type="string",
            required=True,
            default="localhost",
            validation_pattern=r"^[a-zA-Z0-9.-]+$",
        )

        assert prompt.name == "POSTGRES_HOST"
        assert prompt.description == "Database host"
        assert prompt.type == "string"
        assert prompt.required is True
        assert prompt.default == "localhost"
        assert prompt.validation_pattern == r"^[a-zA-Z0-9.-]+$"

    def test_prompt_with_minimal_fields(self):
        """Test prompt with only required fields."""
        prompt = PromptDefinition(
            name="API_KEY",
            description="Your API key",
            type="secret",
        )

        assert prompt.name == "API_KEY"
        assert prompt.required is False
        assert prompt.default is None
        assert prompt.validation_pattern is None

    def test_prompt_types(self):
        """Test all supported prompt types."""
        types = ["string", "secret", "path", "port", "url"]
        for prompt_type in types:
            prompt = PromptDefinition(
                name="TEST",
                description="Test",
                type=prompt_type,
            )
            assert prompt.type == prompt_type

    def test_invalid_prompt_type(self):
        """Test that invalid type is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            PromptDefinition(
                name="TEST",
                description="Test",
                type="invalid",  # type: ignore
            )
        assert "type" in str(exc_info.value)

    def test_invalid_regex_pattern(self):
        """Test that invalid regex is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            PromptDefinition(
                name="TEST",
                description="Test",
                type="string",
                validation_pattern="[invalid(",  # Invalid regex
            )
        assert "Invalid regex pattern" in str(exc_info.value)

    def test_empty_name_rejected(self):
        """Test that empty name is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            PromptDefinition(
                name="",
                description="Test",
                type="string",
            )
        assert "Parameter name cannot be empty" in str(exc_info.value)

    def test_invalid_name_characters(self):
        """Test that invalid characters in name are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            PromptDefinition(
                name="INVALID NAME!",  # Space and exclamation not allowed
                description="Test",
                type="string",
            )
        assert "must contain only alphanumeric" in str(exc_info.value)

    def test_validate_value_required(self):
        """Test validation of required field."""
        prompt = PromptDefinition(
            name="REQUIRED_FIELD",
            description="Required field",
            type="string",
            required=True,
        )

        # Empty value should fail
        valid, error = prompt.validate_value("")
        assert not valid
        assert "required" in error.lower()

        # Non-empty value should pass
        valid, error = prompt.validate_value("something")
        assert valid
        assert error is None

    def test_validate_value_optional(self):
        """Test validation of optional field."""
        prompt = PromptDefinition(
            name="OPTIONAL_FIELD",
            description="Optional field",
            type="string",
            required=False,
        )

        # Empty value should pass for optional
        valid, error = prompt.validate_value("")
        assert valid
        assert error is None

    def test_validate_port(self):
        """Test port validation."""
        prompt = PromptDefinition(
            name="PORT",
            description="Port number",
            type="port",
        )

        # Valid ports
        for port in ["1", "80", "443", "5432", "65535"]:
            valid, error = prompt.validate_value(port)
            assert valid, f"Port {port} should be valid but got: {error}"

        # Invalid ports
        invalid_ports = [
            ("0", "must be between"),  # Too low
            ("65536", "must be between"),  # Too high
            ("abc", "must be a number"),  # Not a number
            ("-1", "must be between"),  # Negative
        ]
        for port, expected_error in invalid_ports:
            valid, error = prompt.validate_value(port)
            assert not valid, f"Port {port} should be invalid"
            assert (
                expected_error in error.lower()
            ), f"Expected '{expected_error}' in error: {error}"

    def test_validate_path(self):
        """Test path validation."""
        prompt = PromptDefinition(
            name="PATH",
            description="File path",
            type="path",
        )

        # Valid paths
        valid_paths = ["/home/user", "./relative", "~/Documents", "C:\\Users\\test"]
        for path in valid_paths:
            valid, error = prompt.validate_value(path)
            assert valid, f"Path '{path}' should be valid but got: {error}"

        # Invalid paths
        valid, error = prompt.validate_value("   ")  # Whitespace only
        assert not valid
        assert "cannot be empty" in error.lower()

        valid, error = prompt.validate_value("path\x00with\x00null")  # Null bytes
        assert not valid
        assert "null byte" in error.lower()

    def test_validate_url(self):
        """Test URL validation."""
        prompt = PromptDefinition(
            name="URL",
            description="API URL",
            type="url",
        )

        # Valid URLs
        valid_urls = [
            "http://example.com",
            "https://api.example.com/v1",
            "ws://localhost:8080",
            "wss://secure.example.com",
        ]
        for url in valid_urls:
            valid, error = prompt.validate_value(url)
            assert valid, f"URL '{url}' should be valid but got: {error}"

        # Invalid URLs
        invalid_urls = [
            "ftp://example.com",  # Wrong protocol
            "example.com",  # Missing protocol
            "//example.com",  # Missing protocol
        ]
        for url in invalid_urls:
            valid, error = prompt.validate_value(url)
            assert not valid, f"URL '{url}' should be invalid"
            assert "must start with" in error.lower()

    def test_validate_regex(self):
        """Test regex validation."""
        prompt = PromptDefinition(
            name="CODE",
            description="Validation code",
            type="string",
            validation_pattern=r"^[A-Z]{3}-\d{4}$",  # Format: ABC-1234
        )

        # Valid values
        valid, error = prompt.validate_value("ABC-1234")
        assert valid
        assert error is None

        # Invalid values
        valid, error = prompt.validate_value("abc-1234")  # Lowercase
        assert not valid
        assert "does not match" in error.lower()

        valid, error = prompt.validate_value("AB-123")  # Wrong length
        assert not valid


class TestServerTemplate:
    """Tests for ServerTemplate model."""

    def test_valid_template(self):
        """Test creating a valid server template."""
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
                )
            ],
            notes="Production configuration with TLS",
        )

        assert template.name == "production"
        assert template.description == "Production setup"
        assert template.server_id == "postgres"
        assert template.scope == "user-mcp"
        assert template.priority == "high"
        assert template.config["command"] == "npx"
        assert len(template.prompts) == 1
        assert template.notes == "Production configuration with TLS"

    def test_template_with_minimal_fields(self):
        """Test template with only required fields."""
        template = ServerTemplate(
            name="basic",
            description="Basic setup",
            server_id="github",
            scope="project-mcp",
            priority="medium",
            config={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
            },
        )

        assert template.name == "basic"
        assert template.prompts == []
        assert template.notes == ""

    def test_config_missing_command(self):
        """Test that config without command is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ServerTemplate(
                name="invalid",
                description="Invalid",
                server_id="test",
                scope="user-mcp",
                priority="low",
                config={
                    "args": ["test"],  # Missing command
                },
            )
        assert "config must have 'command' field" in str(exc_info.value)

    def test_config_missing_args(self):
        """Test that config without args is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ServerTemplate(
                name="invalid",
                description="Invalid",
                server_id="test",
                scope="user-mcp",
                priority="low",
                config={
                    "command": "npx",  # Missing args
                },
            )
        assert "config must have 'args' field" in str(exc_info.value)

    def test_config_invalid_args_type(self):
        """Test that config with non-list args is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ServerTemplate(
                name="invalid",
                description="Invalid",
                server_id="test",
                scope="user-mcp",
                priority="low",
                config={
                    "command": "npx",
                    "args": "not a list",  # Should be list
                },
            )
        assert "config['args'] must be a list" in str(exc_info.value)

    def test_config_invalid_env_type(self):
        """Test that config with non-dict env is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ServerTemplate(
                name="invalid",
                description="Invalid",
                server_id="test",
                scope="user-mcp",
                priority="low",
                config={
                    "command": "npx",
                    "args": [],
                    "env": "not a dict",  # Should be dict
                },
            )
        assert "config['env'] must be a dict" in str(exc_info.value)

    def test_invalid_priority(self):
        """Test that invalid priority is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ServerTemplate(
                name="invalid",
                description="Invalid",
                server_id="test",
                scope="user-mcp",
                priority="critical",  # Not valid priority
                config={"command": "npx", "args": []},
            )
        assert "priority" in str(exc_info.value)

    def test_empty_template_name(self):
        """Test that empty template name is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ServerTemplate(
                name="",
                description="Invalid",
                server_id="test",
                scope="user-mcp",
                priority="low",
                config={"command": "npx", "args": []},
            )
        assert "Template name cannot be empty" in str(exc_info.value)

    def test_invalid_template_name_characters(self):
        """Test that invalid characters in template name are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ServerTemplate(
                name="invalid name!",  # Space and exclamation not allowed
                description="Invalid",
                server_id="test",
                scope="user-mcp",
                priority="low",
                config={"command": "npx", "args": []},
            )
        assert "must contain only alphanumeric" in str(exc_info.value)
