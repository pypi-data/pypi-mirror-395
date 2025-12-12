"""Filesystem utilities."""

import shutil
from pathlib import Path
from typing import Optional


def ensure_directory(path: Path, mode: int = 0o755) -> bool:
    """Ensure directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure
        mode: Directory permissions

    Returns:
        True if directory exists or was created, False otherwise
    """
    try:
        path.mkdir(parents=True, exist_ok=True, mode=mode)
        return True
    except (OSError, PermissionError):
        return False


def safe_remove(path: Path, missing_ok: bool = True) -> bool:
    """Safely remove file or directory.

    Args:
        path: Path to remove
        missing_ok: If True, don't raise error if path doesn't exist

    Returns:
        True if removal successful, False otherwise
    """
    try:
        if not path.exists():
            return missing_ok

        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        else:
            return False

        return True

    except (OSError, PermissionError):
        return False


def get_file_size(path: Path) -> Optional[int]:
    """Get file size in bytes.

    Args:
        path: Path to file

    Returns:
        File size in bytes or None if file doesn't exist
    """
    try:
        if path.exists() and path.is_file():
            return path.stat().st_size
        return None
    except (OSError, PermissionError):
        return None


def is_executable(path: Path) -> bool:
    """Check if file is executable.

    Args:
        path: Path to check

    Returns:
        True if file is executable, False otherwise
    """
    try:
        return path.exists() and path.is_file() and bool(path.stat().st_mode & 0o111)
    except (OSError, PermissionError):
        return False


def copy_file(src: Path, dest: Path, backup: bool = False) -> bool:
    """Copy file from source to destination.

    Args:
        src: Source file path
        dest: Destination file path
        backup: If True, backup destination file if it exists

    Returns:
        True if copy successful, False otherwise
    """
    try:
        if not src.exists():
            return False

        # Create backup if requested
        if backup and dest.exists():
            backup_path = dest.with_suffix(dest.suffix + ".backup")
            shutil.copy2(dest, backup_path)

        # Ensure destination directory exists
        ensure_directory(dest.parent)

        # Copy file
        shutil.copy2(src, dest)
        return True

    except (OSError, PermissionError, shutil.Error):
        return False
