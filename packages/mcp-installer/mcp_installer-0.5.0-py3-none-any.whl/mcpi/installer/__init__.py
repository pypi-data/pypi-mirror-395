"""Installation module for MCP servers."""

from mcpi.installer.base import BaseInstaller, InstallationResult, check_command_available
from mcpi.installer.claude_code import ClaudeCodeInstaller
from mcpi.installer.git import GitInstaller
from mcpi.installer.npm import NPMInstaller
from mcpi.installer.python import PythonInstaller

__all__ = [
    "BaseInstaller",
    "InstallationResult",
    "check_command_available",
    "ClaudeCodeInstaller",
    "NPMInstaller",
    "PythonInstaller",
    "GitInstaller",
]
