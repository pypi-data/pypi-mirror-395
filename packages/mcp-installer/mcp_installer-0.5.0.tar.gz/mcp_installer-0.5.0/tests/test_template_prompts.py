"""Unit tests for template prompt handler."""

from unittest.mock import patch

import pytest

from mcpi.templates.models import PromptDefinition, ServerTemplate
from mcpi.templates.prompt_handler import collect_template_values, prompt_for_value


class TestPromptForValue:
    """Tests for prompt_for_value function."""

    def test_string_prompt(self):
        """Test basic string prompt."""
        prompt_def = PromptDefinition(
            name="API_KEY",
            description="Your API key",
            type="string",
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.return_value = "test-key-123"
            value = prompt_for_value(prompt_def)
            assert value == "test-key-123"
            mock_ask.assert_called_once_with("Your API key")

    def test_secret_prompt_masked(self):
        """Test secret prompt uses password masking."""
        prompt_def = PromptDefinition(
            name="PASSWORD",
            description="Your password",
            type="secret",
            required=True,
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.return_value = "super-secret"
            value = prompt_for_value(prompt_def)
            assert value == "super-secret"
            mock_ask.assert_called_once_with("Your password", password=True)

    def test_default_value_shown(self):
        """Test default value is shown in prompt."""
        prompt_def = PromptDefinition(
            name="PORT",
            description="Port number",
            type="port",
            default="5432",
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.return_value = ""  # User presses enter
            value = prompt_for_value(prompt_def)
            assert value == "5432"  # Default used
            mock_ask.assert_called_once_with("Port number [5432]")

    def test_default_value_used_on_empty(self):
        """Test default value is used when user provides empty input."""
        prompt_def = PromptDefinition(
            name="HOST",
            description="Database host",
            type="string",
            default="localhost",
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.return_value = ""
            value = prompt_for_value(prompt_def)
            assert value == "localhost"

    def test_validation_port_valid(self):
        """Test port validation accepts valid ports."""
        prompt_def = PromptDefinition(
            name="PORT",
            description="Port number",
            type="port",
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.return_value = "8080"
            value = prompt_for_value(prompt_def)
            assert value == "8080"

    def test_validation_port_invalid_retries(self):
        """Test port validation rejects invalid ports and retries."""
        prompt_def = PromptDefinition(
            name="PORT",
            description="Port number",
            type="port",
        )

        with (
            patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask,
            patch("mcpi.templates.prompt_handler.console.print") as mock_print,
        ):
            # First attempt: invalid (not a number)
            # Second attempt: invalid (out of range)
            # Third attempt: valid
            mock_ask.side_effect = ["abc", "99999", "8080"]
            value = prompt_for_value(prompt_def)
            assert value == "8080"
            assert mock_ask.call_count == 3
            # Should have printed error messages
            assert mock_print.call_count >= 2

    def test_validation_url_valid(self):
        """Test URL validation accepts valid URLs."""
        prompt_def = PromptDefinition(
            name="API_URL",
            description="API endpoint",
            type="url",
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.return_value = "https://api.example.com"
            value = prompt_for_value(prompt_def)
            assert value == "https://api.example.com"

    def test_validation_url_invalid_retries(self):
        """Test URL validation rejects invalid URLs and retries."""
        prompt_def = PromptDefinition(
            name="API_URL",
            description="API endpoint",
            type="url",
        )

        with (
            patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask,
            patch("mcpi.templates.prompt_handler.console.print"),
        ):
            # First attempt: invalid (no protocol)
            # Second attempt: valid
            mock_ask.side_effect = ["example.com", "https://example.com"]
            value = prompt_for_value(prompt_def)
            assert value == "https://example.com"
            assert mock_ask.call_count == 2

    def test_validation_path_valid(self):
        """Test path validation accepts valid paths."""
        prompt_def = PromptDefinition(
            name="DATA_PATH",
            description="Data directory",
            type="path",
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.return_value = "/home/user/data"
            value = prompt_for_value(prompt_def)
            assert value == "/home/user/data"

    def test_validation_regex_valid(self):
        """Test regex validation accepts matching values."""
        prompt_def = PromptDefinition(
            name="CODE",
            description="Validation code",
            type="string",
            validation_pattern=r"^[A-Z]{3}-\d{4}$",
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.return_value = "ABC-1234"
            value = prompt_for_value(prompt_def)
            assert value == "ABC-1234"

    def test_validation_regex_invalid_retries(self):
        """Test regex validation rejects non-matching values and retries."""
        prompt_def = PromptDefinition(
            name="CODE",
            description="Validation code",
            type="string",
            validation_pattern=r"^[A-Z]{3}-\d{4}$",
        )

        with (
            patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask,
            patch("mcpi.templates.prompt_handler.console.print"),
        ):
            # First attempt: invalid format
            # Second attempt: valid
            mock_ask.side_effect = ["abc-1234", "ABC-1234"]
            value = prompt_for_value(prompt_def)
            assert value == "ABC-1234"
            assert mock_ask.call_count == 2

    def test_required_field_rejects_empty(self):
        """Test required fields reject empty input."""
        prompt_def = PromptDefinition(
            name="REQUIRED",
            description="Required field",
            type="string",
            required=True,
        )

        with (
            patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask,
            patch("mcpi.templates.prompt_handler.console.print"),
        ):
            # First attempt: empty (invalid for required)
            # Second attempt: valid
            mock_ask.side_effect = ["", "value"]
            value = prompt_for_value(prompt_def)
            assert value == "value"
            assert mock_ask.call_count == 2

    def test_keyboard_interrupt_propagates(self):
        """Test Ctrl+C is handled gracefully."""
        prompt_def = PromptDefinition(
            name="TEST",
            description="Test field",
            type="string",
        )

        with patch("mcpi.templates.prompt_handler.Prompt.ask") as mock_ask:
            mock_ask.side_effect = KeyboardInterrupt()
            with pytest.raises(KeyboardInterrupt):
                prompt_for_value(prompt_def)


class TestCollectTemplateValues:
    """Tests for collect_template_values function."""

    def test_no_prompts_returns_empty(self):
        """Test template with no prompts returns empty dict."""
        template = ServerTemplate(
            name="simple",
            description="Simple template",
            server_id="test",
            scope="user-mcp",
            priority="high",
            config={"command": "npx", "args": ["test"]},
            prompts=[],
        )

        values = collect_template_values(template)
        assert values == {}

    def test_single_prompt_collected(self):
        """Test collecting a single prompt value."""
        template = ServerTemplate(
            name="test",
            description="Test template",
            server_id="test",
            scope="user-mcp",
            priority="high",
            config={"command": "npx", "args": ["test"]},
            prompts=[
                PromptDefinition(
                    name="API_KEY",
                    description="Your API key",
                    type="string",
                )
            ],
        )

        with patch("mcpi.templates.prompt_handler.prompt_for_value") as mock_prompt:
            mock_prompt.return_value = "test-key"
            values = collect_template_values(template)
            assert values == {"API_KEY": "test-key"}
            assert mock_prompt.call_count == 1

    def test_multiple_prompts_collected(self):
        """Test collecting multiple prompt values."""
        template = ServerTemplate(
            name="test",
            description="Test template",
            server_id="postgres",
            scope="user-mcp",
            priority="high",
            config={"command": "npx", "args": ["test"]},
            prompts=[
                PromptDefinition(
                    name="POSTGRES_HOST",
                    description="Database host",
                    type="string",
                ),
                PromptDefinition(
                    name="POSTGRES_PORT",
                    description="Database port",
                    type="port",
                ),
                PromptDefinition(
                    name="POSTGRES_PASSWORD",
                    description="Database password",
                    type="secret",
                ),
            ],
        )

        with patch("mcpi.templates.prompt_handler.prompt_for_value") as mock_prompt:
            mock_prompt.side_effect = ["localhost", "5432", "secret123"]
            values = collect_template_values(template)
            assert values == {
                "POSTGRES_HOST": "localhost",
                "POSTGRES_PORT": "5432",
                "POSTGRES_PASSWORD": "secret123",
            }
            assert mock_prompt.call_count == 3

    def test_keyboard_interrupt_propagates(self):
        """Test Ctrl+C during collection is handled."""
        template = ServerTemplate(
            name="test",
            description="Test template",
            server_id="test",
            scope="user-mcp",
            priority="high",
            config={"command": "npx", "args": ["test"]},
            prompts=[
                PromptDefinition(
                    name="API_KEY",
                    description="Your API key",
                    type="string",
                )
            ],
        )

        with patch("mcpi.templates.prompt_handler.prompt_for_value") as mock_prompt:
            mock_prompt.side_effect = KeyboardInterrupt()
            with pytest.raises(KeyboardInterrupt):
                collect_template_values(template)

    def test_displays_template_info(self):
        """Test template header and notes are displayed."""
        template = ServerTemplate(
            name="production",
            description="Production setup",
            server_id="postgres",
            scope="user-mcp",
            priority="high",
            config={"command": "npx", "args": ["test"]},
            prompts=[
                PromptDefinition(
                    name="API_KEY",
                    description="Your API key",
                    type="string",
                )
            ],
            notes="This template sets up PostgreSQL for production use.",
        )

        with (
            patch("mcpi.templates.prompt_handler.prompt_for_value") as mock_prompt,
            patch("mcpi.templates.prompt_handler.console.print") as mock_print,
        ):
            mock_prompt.return_value = "test"
            collect_template_values(template)

            # Check that template info was displayed
            # Should print header, notes, and success message
            assert mock_print.call_count >= 3
