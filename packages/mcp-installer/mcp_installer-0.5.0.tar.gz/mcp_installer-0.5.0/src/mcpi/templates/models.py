"""Pydantic models for configuration templates."""

import re
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class PromptDefinition(BaseModel):
    """Interactive prompt definition for template parameter.

    Defines how to prompt the user for a single configuration value,
    including validation rules and help text.
    """

    name: str = Field(..., description="Parameter name (e.g., 'POSTGRES_HOST')")
    description: str = Field(..., description="Help text shown to user")
    type: Literal["string", "secret", "path", "port", "url"] = Field(
        ..., description="Type of value expected"
    )
    required: bool = Field(False, description="Whether this parameter is required")
    default: Optional[str] = Field(
        None, description="Default value if user provides nothing"
    )
    validation_pattern: Optional[str] = Field(
        None, description="Regex pattern for validation"
    )

    @field_validator("validation_pattern")
    @classmethod
    def validate_regex_pattern(cls, v: Optional[str]) -> Optional[str]:
        """Ensure validation pattern is a valid regex."""
        if v is not None:
            try:
                re.compile(v)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}") from e
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure parameter name follows conventions."""
        if not v:
            raise ValueError("Parameter name cannot be empty")
        # Parameter names should be uppercase with underscores (env var convention)
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                f"Parameter name '{v}' must contain only alphanumeric characters, underscores, and hyphens"
            )
        return v

    def validate_value(self, value: str) -> tuple[bool, Optional[str]]:
        """Validate a user-provided value against this prompt's rules.

        Args:
            value: The value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required
        if self.required and not value:
            return False, f"{self.name} is required"

        # If empty and not required, allow it
        if not value:
            return True, None

        # Type-specific validation
        if self.type == "port":
            try:
                port = int(value)
                if not (1 <= port <= 65535):
                    return False, f"Port must be between 1 and 65535, got {port}"
            except ValueError:
                return False, f"Port must be a number, got '{value}'"

        elif self.type == "path":
            # Path validation: check if it looks like a valid path format
            # Don't check existence yet (may be created later)
            if not value.strip():
                return False, "Path cannot be empty"
            # Basic path validation - no null bytes
            if "\x00" in value:
                return False, "Path cannot contain null bytes"

        elif self.type == "url":
            # Basic URL validation
            if not value.startswith(("http://", "https://", "ws://", "wss://")):
                return (
                    False,
                    f"URL must start with http://, https://, ws://, or wss://, got '{value}'",
                )

        # Regex validation (if provided)
        if self.validation_pattern:
            try:
                if not re.match(self.validation_pattern, value):
                    return False, f"{self.name} does not match expected format"
            except re.error as e:
                return False, f"Validation regex error: {e}"

        return True, None


class ServerTemplate(BaseModel):
    """Template for server configuration with interactive prompts.

    Combines static configuration (command, args) with dynamic prompts
    that guide the user through providing required parameters.
    """

    name: str = Field(..., description="Template name (e.g., 'production')")
    description: str = Field(..., description="Brief description of this template")
    server_id: str = Field(
        ..., description="Server ID this template is for (e.g., 'postgres')"
    )
    scope: str = Field(
        ..., description="Recommended scope (e.g., 'user-global', 'project-mcp')"
    )
    priority: Literal["high", "medium", "low"] = Field(
        ..., description="Priority for sorting templates"
    )
    config: dict[str, Any] = Field(
        ..., description="Static configuration (command, args, env)"
    )
    prompts: list[PromptDefinition] = Field(
        default_factory=list, description="Interactive prompts for dynamic values"
    )
    notes: str = Field(
        default="", description="Additional notes and setup instructions"
    )

    # Metadata fields for template discovery and recommendation
    best_for: list[str] = Field(
        default_factory=list,
        description="Tags describing what this template is best suited for (e.g., 'docker', 'local-development', 'production')"
    )
    keywords: list[str] = Field(
        default_factory=list,
        description="Keywords for matching against project context (e.g., 'compose', 'containers', 'postgresql')"
    )
    recommendations: dict[str, Any] = Field(
        default_factory=dict,
        description="Recommendation hints (e.g., minimum scores, required context)"
    )

    @field_validator("config")
    @classmethod
    def validate_config(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Ensure config has required fields."""
        if "command" not in v:
            raise ValueError("config must have 'command' field")
        if "args" not in v:
            raise ValueError("config must have 'args' field")
        if not isinstance(v["args"], list):
            raise ValueError("config['args'] must be a list")
        if "env" in v and not isinstance(v["env"], dict):
            raise ValueError("config['env'] must be a dict")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure template name follows conventions."""
        if not v:
            raise ValueError("Template name cannot be empty")
        # Template names should be lowercase with hyphens
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError(
                f"Template name '{v}' must contain only alphanumeric characters, hyphens, and underscores"
            )
        return v
