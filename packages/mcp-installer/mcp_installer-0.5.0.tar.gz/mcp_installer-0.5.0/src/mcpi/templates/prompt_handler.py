"""Interactive prompt handler for configuration templates.

This module provides functions to collect user input for template parameters
using Rich's interactive prompt system with validation and secret masking.
"""

from typing import Dict

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text

from .models import PromptDefinition, ServerTemplate

console = Console()


def prompt_for_value(prompt_def: PromptDefinition) -> str:
    """Prompt user for a single value with validation.

    Args:
        prompt_def: Definition of the prompt with validation rules

    Returns:
        User-provided value (validated)

    Raises:
        KeyboardInterrupt: If user presses Ctrl+C
    """
    # Build prompt text with description
    prompt_text = prompt_def.description

    # Add default value hint if available
    if prompt_def.default:
        prompt_text = f"{prompt_text} [{prompt_def.default}]"

    # Loop until we get a valid value
    while True:
        try:
            # Use password mode for secrets (masked input)
            if prompt_def.type == "secret":
                value = Prompt.ask(prompt_text, password=True)
            else:
                value = Prompt.ask(prompt_text)

            # If empty and we have a default, use it
            if not value and prompt_def.default:
                value = prompt_def.default

            # Validate the value
            is_valid, error_message = prompt_def.validate_value(value)

            if is_valid:
                return value

            # Show error and re-prompt
            console.print(f"[red]✗ {error_message}[/red]")

            # Show example for common types
            if prompt_def.type == "port":
                console.print("[dim]Example: 5432, 8080, 3000[/dim]")
            elif prompt_def.type == "url":
                console.print("[dim]Example: https://api.example.com[/dim]")
            elif prompt_def.type == "path":
                console.print("[dim]Example: /home/user/data or ~/Documents[/dim]")

        except (EOFError, KeyboardInterrupt):
            # User pressed Ctrl+C or Ctrl+D
            console.print("\n[yellow]Setup cancelled[/yellow]")
            raise KeyboardInterrupt("User cancelled setup")


def collect_template_values(template: ServerTemplate) -> Dict[str, str]:
    """Collect all values for a template's prompts interactively.

    Args:
        template: The template to collect values for

    Returns:
        Dictionary mapping prompt names to user-provided values

    Raises:
        KeyboardInterrupt: If user cancels the setup
    """
    # If no prompts, return empty dict
    if not template.prompts:
        return {}

    # Show template header
    console.print()
    header = Text()
    header.append(f"Setting up '{template.server_id}' with ", style="bold cyan")
    header.append(f"'{template.name}'", style="bold yellow")
    header.append(" template", style="bold cyan")

    console.print(
        Panel(
            header,
            border_style="cyan",
            padding=(0, 1),
        )
    )
    console.print()

    # Show template notes if available
    if template.notes:
        console.print("[dim]" + template.notes + "[/dim]")
        console.print()

    # Collect values for each prompt
    values = {}

    for prompt_def in template.prompts:
        try:
            value = prompt_for_value(prompt_def)
            values[prompt_def.name] = value
        except KeyboardInterrupt:
            # Re-raise to let CLI handle it
            raise

    console.print()
    console.print("[green]✓ Configuration complete[/green]")
    console.print()

    return values
