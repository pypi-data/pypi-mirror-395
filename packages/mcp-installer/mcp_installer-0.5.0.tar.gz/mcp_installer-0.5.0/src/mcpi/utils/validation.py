"""Validation utilities."""

import re
from pathlib import Path
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """Validate URL format.

    Args:
        url: URL to validate

    Returns:
        True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_path(path: str, must_exist: bool = False) -> bool:
    """Validate file path.

    Args:
        path: Path to validate
        must_exist: If True, path must exist

    Returns:
        True if path is valid, False otherwise
    """
    try:
        path_obj = Path(path).expanduser().resolve()

        if must_exist:
            return path_obj.exists()

        # Check if path is valid (parent directory exists or can be created)
        return path_obj.parent.exists() or path_obj.parent.parent.exists()

    except (OSError, ValueError):
        return False


def validate_server_id(server_id: str) -> bool:
    """Validate server ID format.

    ALL server IDs must be namespaced with exactly one '/' to indicate ownership.
    Optionally, verified accounts may prefix their namespace with '@'.

    Valid formats:
        - owner/server (standard namespace)
        - @owner/server (verified account)

    Examples:
        - anthropic/filesystem ✓
        - @anthropic/filesystem ✓ (verified)
        - r-huijts/xcode ✓
        - @modelcontextprotocol/github ✓ (verified)
        - filesystem ✗ (missing namespace)
        - owner/path/server ✗ (too many slashes)

    Args:
        server_id: Server ID to validate

    Returns:
        True if server ID is valid, False otherwise
    """
    if not server_id or not isinstance(server_id, str):
        return False

    # Pattern: optional '@', owner name, exactly one '/', server name
    # owner and server must be lowercase alphanumeric with hyphens
    # Must start and end with alphanumeric (not hyphen)
    pattern = r"^@?[a-z0-9]([a-z0-9-]*[a-z0-9])?/[a-z0-9]([a-z0-9-]*[a-z0-9])?$"

    # Count slashes - must be exactly 1
    if server_id.count('/') != 1:
        return False

    return bool(re.match(pattern, server_id))


def validate_package_name(package_name: str, method: str = "npm") -> bool:
    """Validate package name format for different installation methods.

    Args:
        package_name: Package name to validate
        method: Installation method (npm, pip, git)

    Returns:
        True if package name is valid, False otherwise
    """
    if not package_name or not isinstance(package_name, str):
        return False

    if method == "npm":
        # NPM package names can be scoped (@scope/package) or unscoped
        pattern = r"^(@[a-z0-9-~][a-z0-9-._~]*/)?[a-z0-9-~][a-z0-9-._~]*$"
        return bool(re.match(pattern, package_name))

    elif method == "pip":
        # PEP 508 name format
        pattern = r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$"
        return bool(re.match(pattern, package_name, re.IGNORECASE))

    elif method == "git":
        # Git URLs or repository paths
        if validate_url(package_name):
            return True
        # Could also be a local path
        return validate_path(package_name)

    return False


def validate_version(version: str) -> bool:
    """Validate semantic version format.

    Args:
        version: Version string to validate

    Returns:
        True if version is valid, False otherwise
    """
    if not version or not isinstance(version, str):
        return False

    # Basic semantic version pattern (major.minor.patch with optional pre-release/build)
    pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    return bool(re.match(pattern, version))


def validate_email(email: str) -> bool:
    """Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False

    # Basic email validation pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_license(license_name: str) -> bool:
    """Validate software license name.

    Args:
        license_name: License name to validate

    Returns:
        True if license name appears valid, False otherwise
    """
    if not license_name or not isinstance(license_name, str):
        return False

    # Common license identifiers (SPDX-style)
    common_licenses = {
        "MIT",
        "Apache-2.0",
        "GPL-3.0",
        "GPL-2.0",
        "BSD-3-Clause",
        "BSD-2-Clause",
        "ISC",
        "MPL-2.0",
        "LGPL-3.0",
        "LGPL-2.1",
        "CC0-1.0",
        "Unlicense",
        "Proprietary",
        "Commercial",
        "None",
    }

    # Check exact match or reasonable pattern
    if license_name in common_licenses:
        return True

    # Allow other reasonable license names
    return len(license_name) <= 50 and not any(c in license_name for c in '<>&"')


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """Sanitize filename by replacing invalid characters.

    Args:
        filename: Original filename
        replacement: Character to replace invalid characters with

    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed"

    # Remove or replace invalid filename characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    sanitized = re.sub(invalid_chars, replacement, filename)

    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip(". ")

    # Ensure not empty
    if not sanitized:
        return "unnamed"

    # Limit length
    if len(sanitized) > 255:
        name, ext = Path(sanitized).stem, Path(sanitized).suffix
        max_name_len = 255 - len(ext)
        sanitized = name[:max_name_len] + ext

    return sanitized
