"""Base installer interface and common utilities."""

import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcpi.registry.catalog import MCPServer


def check_command_available(command: str, timeout: int = 10) -> bool:
    """Check if a command is available on the system.

    This is a shared utility for checking tool availability (npm, pip, uv, git, etc.)

    Args:
        command: Command name to check (e.g., "npm", "git", "python")
        timeout: Maximum time to wait for version check in seconds

    Returns:
        True if command is available and responds to --version, False otherwise
    """
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


class InstallationStatus(str, Enum):
    """Installation status enumeration."""

    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    SKIPPED = "skipped"


@dataclass
class InstallationResult:
    """Result of an installation operation."""

    status: InstallationStatus
    message: str
    server_id: str
    config_path: Optional[Path] = None
    backup_path: Optional[Path] = None
    details: Dict[str, Any] = None

    def __post_init__(self) -> None:
        """Initialize details if not provided."""
        if self.details is None:
            self.details = {}

    @property
    def success(self) -> bool:
        """Check if installation was successful."""
        return self.status == InstallationStatus.SUCCESS

    @property
    def failed(self) -> bool:
        """Check if installation failed."""
        return self.status == InstallationStatus.FAILED


class BaseInstaller(ABC):
    """Base class for MCP server installers.

    Note: With the simplified MCPServer catalog format (command + args),
    this installer no longer handles package installation. Servers in the
    catalog are assumed to be runnable as-is (e.g., via npx).

    The installer's job is simply to add server configurations to client
    config files.
    """

    def __init__(self, config_path: Optional[Path] = None, dry_run: bool = False):
        """Initialize the installer.

        Args:
            config_path: Path to configuration file
            dry_run: If True, simulate installation without making changes
        """
        self.config_path = config_path
        self.dry_run = dry_run
        self._backup_paths: List[Path] = []

    @abstractmethod
    def install(
        self,
        server: MCPServer,
        server_id: str,
        config_params: Optional[Dict[str, Any]] = None,
    ) -> InstallationResult:
        """Install an MCP server.

        Args:
            server: MCP server to install
            server_id: Server ID (since MCPServer doesn't have id field)
            config_params: Configuration parameters

        Returns:
            Installation result
        """
        pass

    @abstractmethod
    def uninstall(self, server_id: str) -> InstallationResult:
        """Uninstall an MCP server.

        Args:
            server_id: ID of server to uninstall

        Returns:
            Installation result
        """
        pass

    @abstractmethod
    def is_installed(self, server_id: str) -> bool:
        """Check if server is installed.

        Args:
            server_id: Server ID to check

        Returns:
            True if installed, False otherwise
        """
        pass

    @abstractmethod
    def get_installed_servers(self) -> List[str]:
        """Get list of installed server IDs.

        Returns:
            List of installed server IDs
        """
        pass

    def validate_installation(self, server: MCPServer, server_id: str) -> List[str]:
        """Validate installation requirements.

        With the simplified catalog format, validation is minimal - we just
        check that the server has a valid command.

        Args:
            server: Server to validate
            server_id: Server ID (since MCPServer doesn't have id field)

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Basic validation - ensure command exists
        if not server.command or not server.command.strip():
            errors.append("Server has no command specified")

        return errors

    def create_backup(self, file_path: Path) -> Optional[Path]:
        """Create backup of configuration file.

        Args:
            file_path: Path to file to backup

        Returns:
            Path to backup file or None if backup failed
        """
        if not file_path.exists():
            return None

        import datetime
        import shutil

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = file_path.with_suffix(f".backup_{timestamp}")

        try:
            shutil.copy2(file_path, backup_path)
            self._backup_paths.append(backup_path)
            return backup_path
        except Exception:
            return None

    def restore_backup(self, backup_path: Path, target_path: Path) -> bool:
        """Restore from backup.

        Args:
            backup_path: Path to backup file
            target_path: Path to restore to

        Returns:
            True if restore successful, False otherwise
        """
        if not backup_path.exists():
            return False

        try:
            import shutil

            shutil.copy2(backup_path, target_path)
            return True
        except Exception:
            return False

    def cleanup_backups(self) -> None:
        """Clean up created backup files."""
        for backup_path in self._backup_paths:
            try:
                if backup_path.exists():
                    backup_path.unlink()
            except Exception:
                pass  # Ignore cleanup errors
        self._backup_paths.clear()

    def _create_success_result(
        self,
        server_id: str,
        message: str,
        config_path: Optional[Path] = None,
        **details: Any,
    ) -> InstallationResult:
        """Create a success result.

        Args:
            server_id: Server ID
            message: Success message
            config_path: Path to configuration file
            **details: Additional details

        Returns:
            Success installation result
        """
        return InstallationResult(
            status=InstallationStatus.SUCCESS,
            message=message,
            server_id=server_id,
            config_path=config_path,
            details=details,
        )

    def _create_failure_result(
        self, server_id: str, message: str, **details: Any
    ) -> InstallationResult:
        """Create a failure result.

        Args:
            server_id: Server ID
            message: Error message
            **details: Additional details

        Returns:
            Failure installation result
        """
        return InstallationResult(
            status=InstallationStatus.FAILED,
            message=message,
            server_id=server_id,
            details=details,
        )
