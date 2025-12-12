"""Tests for validation utilities."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from mcpi.utils.validation import (
    sanitize_filename,
    validate_email,
    validate_license,
    validate_package_name,
    validate_path,
    validate_server_id,
    validate_url,
    validate_version,
)


class TestValidationUtils:
    """Tests for validation utility functions."""

    def test_validate_url_valid_http(self):
        """Test validate_url with valid HTTP URL."""
        result = validate_url("http://example.com")
        assert result is True

    def test_validate_url_valid_https(self):
        """Test validate_url with valid HTTPS URL."""
        result = validate_url("https://github.com/user/repo")
        assert result is True

    def test_validate_url_valid_with_path(self):
        """Test validate_url with valid URL including path."""
        result = validate_url("https://example.com/path/to/resource")
        assert result is True

    def test_validate_url_valid_with_query(self):
        """Test validate_url with valid URL including query parameters."""
        result = validate_url("https://api.example.com/v1/data?key=value")
        assert result is True

    def test_validate_url_invalid_no_scheme(self):
        """Test validate_url with invalid URL (no scheme)."""
        result = validate_url("example.com")
        assert result is False

    def test_validate_url_invalid_no_netloc(self):
        """Test validate_url with invalid URL (no network location)."""
        result = validate_url("http://")
        assert result is False

    def test_validate_url_invalid_empty(self):
        """Test validate_url with empty string."""
        result = validate_url("")
        assert result is False

    def test_validate_url_invalid_none(self):
        """Test validate_url with None."""
        result = validate_url(None)
        assert result is False

    @patch("mcpi.utils.validation.urlparse")
    def test_validate_url_exception_handling(self, mock_urlparse):
        """Test validate_url handles exceptions."""
        mock_urlparse.side_effect = ValueError("Invalid URL")

        result = validate_url("malformed-url")

        assert result is False

    def test_validate_path_valid_existing_file(self):
        """Test validate_path with existing file."""
        with tempfile.NamedTemporaryFile() as temp_file:
            result = validate_path(temp_file.name, must_exist=True)
            assert result is True

    def test_validate_path_valid_existing_directory(self):
        """Test validate_path with existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_path(temp_dir, must_exist=True)
            assert result is True

    def test_validate_path_invalid_non_existing_must_exist(self):
        """Test validate_path with non-existing path when must_exist=True."""
        result = validate_path("/non/existent/path", must_exist=True)
        assert result is False

    def test_validate_path_valid_non_existing_parent_exists(self):
        """Test validate_path with non-existing path but existing parent."""
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existing_file = str(Path(temp_dir) / "new_file.txt")
            result = validate_path(non_existing_file, must_exist=False)
            assert result is True

    def test_validate_path_valid_grandparent_exists(self):
        """Test validate_path with non-existing path but existing grandparent."""
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existing_path = str(Path(temp_dir) / "new_dir" / "file.txt")
            result = validate_path(non_existing_path, must_exist=False)
            assert result is True

    def test_validate_path_expanduser(self):
        """Test validate_path expands user home directory."""
        result = validate_path("~/test_file", must_exist=False)
        # Should not raise exception and return reasonable result
        assert isinstance(result, bool)

    @patch("pathlib.Path.expanduser")
    def test_validate_path_os_error(self, mock_expanduser):
        """Test validate_path handles OS errors."""
        mock_expanduser.side_effect = OSError("System error")

        result = validate_path("/some/path")

        assert result is False

    @patch("pathlib.Path.expanduser")
    def test_validate_path_value_error(self, mock_expanduser):
        """Test validate_path handles value errors."""
        mock_expanduser.side_effect = ValueError("Invalid path")

        result = validate_path("invalid\\path")

        assert result is False

    # === Namespaced Server ID Tests (New Format) ===
    # All server IDs must be namespaced with exactly one '/'
    # Optional '@' prefix for verified accounts

    def test_validate_server_id_valid_namespaced(self):
        """Test validate_server_id with valid namespaced format."""
        assert validate_server_id("anthropic/filesystem") is True
        assert validate_server_id("modelcontextprotocol/github") is True
        assert validate_server_id("r-huijts/xcode") is True

    def test_validate_server_id_valid_verified(self):
        """Test validate_server_id with verified account prefix."""
        assert validate_server_id("@anthropic/filesystem") is True
        assert validate_server_id("@modelcontextprotocol/github") is True

    def test_validate_server_id_valid_single_char_parts(self):
        """Test validate_server_id with single character owner/server."""
        assert validate_server_id("a/b") is True
        assert validate_server_id("@a/b") is True

    def test_validate_server_id_valid_with_hyphens(self):
        """Test validate_server_id with hyphens in namespace and server."""
        assert validate_server_id("my-org/my-server") is True
        assert validate_server_id("@my-org/my-server") is True

    def test_validate_server_id_valid_with_numbers(self):
        """Test validate_server_id with numbers."""
        assert validate_server_id("org123/server456") is True
        assert validate_server_id("@org-2024/server-v2") is True

    def test_validate_server_id_invalid_no_namespace(self):
        """Test validate_server_id without namespace (missing '/')."""
        assert validate_server_id("filesystem") is False
        assert validate_server_id("my-server") is False
        assert validate_server_id("@filesystem") is False  # @ without /

    def test_validate_server_id_invalid_too_many_slashes(self):
        """Test validate_server_id with too many slashes."""
        assert validate_server_id("owner/repo/server") is False
        assert validate_server_id("@owner/repo/server") is False

    def test_validate_server_id_invalid_empty(self):
        """Test validate_server_id with empty string."""
        assert validate_server_id("") is False

    def test_validate_server_id_invalid_none(self):
        """Test validate_server_id with None."""
        assert validate_server_id(None) is False

    def test_validate_server_id_invalid_not_string(self):
        """Test validate_server_id with non-string input."""
        assert validate_server_id(123) is False

    def test_validate_server_id_invalid_uppercase(self):
        """Test validate_server_id with uppercase characters."""
        assert validate_server_id("Owner/Server") is False
        assert validate_server_id("@Owner/Server") is False

    def test_validate_server_id_invalid_starts_with_hyphen(self):
        """Test validate_server_id starting with hyphen."""
        assert validate_server_id("-owner/server") is False
        assert validate_server_id("owner/-server") is False

    def test_validate_server_id_invalid_ends_with_hyphen(self):
        """Test validate_server_id ending with hyphen."""
        assert validate_server_id("owner-/server") is False
        assert validate_server_id("owner/server-") is False

    def test_validate_server_id_invalid_special_chars(self):
        """Test validate_server_id with invalid special characters."""
        assert validate_server_id("owner/server@test") is False
        assert validate_server_id("owner_test/server") is False  # underscore not allowed
        assert validate_server_id("owner.test/server") is False  # dot not allowed

    def test_validate_server_id_invalid_empty_parts(self):
        """Test validate_server_id with empty owner or server."""
        assert validate_server_id("/server") is False
        assert validate_server_id("owner/") is False
        assert validate_server_id("/") is False

    def test_validate_package_name_npm_valid_unscoped(self):
        """Test validate_package_name for valid unscoped npm package."""
        result = validate_package_name("express", "npm")
        assert result is True

    def test_validate_package_name_npm_valid_scoped(self):
        """Test validate_package_name for valid scoped npm package."""
        result = validate_package_name("@types/node", "npm")
        assert result is True

    def test_validate_package_name_npm_invalid_uppercase(self):
        """Test validate_package_name for invalid npm package with uppercase."""
        result = validate_package_name("Express", "npm")
        assert result is False

    def test_validate_package_name_pip_valid(self):
        """Test validate_package_name for valid pip package."""
        result = validate_package_name("requests", "pip")
        assert result is True

    def test_validate_package_name_pip_valid_with_hyphens(self):
        """Test validate_package_name for valid pip package with hyphens."""
        result = validate_package_name("beautifulsoup4", "pip")
        assert result is True

    def test_validate_package_name_pip_invalid_special_chars(self):
        """Test validate_package_name for invalid pip package."""
        result = validate_package_name("package@version", "pip")
        assert result is False

    def test_validate_package_name_git_valid_url(self):
        """Test validate_package_name for valid git URL."""
        result = validate_package_name("https://github.com/user/repo.git", "git")
        assert result is True

    def test_validate_package_name_git_valid_path(self):
        """Test validate_package_name for valid git local path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_package_name(temp_dir, "git")
            assert result is True

    def test_validate_package_name_empty(self):
        """Test validate_package_name with empty string."""
        result = validate_package_name("", "npm")
        assert result is False

    def test_validate_package_name_none(self):
        """Test validate_package_name with None."""
        result = validate_package_name(None, "npm")
        assert result is False

    def test_validate_package_name_not_string(self):
        """Test validate_package_name with non-string input."""
        result = validate_package_name(123, "npm")
        assert result is False

    def test_validate_package_name_unknown_method(self):
        """Test validate_package_name with unknown method."""
        result = validate_package_name("package", "unknown")
        assert result is False

    def test_validate_version_valid_basic(self):
        """Test validate_version with valid basic semantic version."""
        result = validate_version("1.2.3")
        assert result is True

    def test_validate_version_valid_with_prerelease(self):
        """Test validate_version with valid version including pre-release."""
        result = validate_version("1.0.0-alpha.1")
        assert result is True

    def test_validate_version_valid_with_build(self):
        """Test validate_version with valid version including build metadata."""
        result = validate_version("1.0.0+20130313144700")
        assert result is True

    def test_validate_version_valid_with_both(self):
        """Test validate_version with valid version including both pre-release and build."""
        result = validate_version("1.0.0-beta+exp.sha.5114f85")
        assert result is True

    def test_validate_version_invalid_missing_patch(self):
        """Test validate_version with invalid version missing patch number."""
        result = validate_version("1.2")
        assert result is False

    def test_validate_version_invalid_leading_zeros(self):
        """Test validate_version with invalid version with leading zeros."""
        result = validate_version("01.2.3")
        assert result is False

    def test_validate_version_empty(self):
        """Test validate_version with empty string."""
        result = validate_version("")
        assert result is False

    def test_validate_version_none(self):
        """Test validate_version with None."""
        result = validate_version(None)
        assert result is False

    def test_validate_version_not_string(self):
        """Test validate_version with non-string input."""
        result = validate_version(123)
        assert result is False

    def test_validate_email_valid_basic(self):
        """Test validate_email with valid basic email."""
        result = validate_email("user@example.com")
        assert result is True

    def test_validate_email_valid_with_dots(self):
        """Test validate_email with valid email containing dots."""
        result = validate_email("first.last@example.com")
        assert result is True

    def test_validate_email_valid_with_plus(self):
        """Test validate_email with valid email containing plus."""
        result = validate_email("user+tag@example.com")
        assert result is True

    def test_validate_email_valid_subdomain(self):
        """Test validate_email with valid email on subdomain."""
        result = validate_email("user@mail.example.com")
        assert result is True

    def test_validate_email_invalid_no_at(self):
        """Test validate_email with invalid email (no @ symbol)."""
        result = validate_email("userexample.com")
        assert result is False

    def test_validate_email_invalid_no_domain(self):
        """Test validate_email with invalid email (no domain)."""
        result = validate_email("user@")
        assert result is False

    def test_validate_email_invalid_no_tld(self):
        """Test validate_email with invalid email (no TLD)."""
        result = validate_email("user@example")
        assert result is False

    def test_validate_email_empty(self):
        """Test validate_email with empty string."""
        result = validate_email("")
        assert result is False

    def test_validate_email_none(self):
        """Test validate_email with None."""
        result = validate_email(None)
        assert result is False

    def test_validate_email_not_string(self):
        """Test validate_email with non-string input."""
        result = validate_email(123)
        assert result is False

    def test_validate_license_valid_common(self):
        """Test validate_license with valid common license."""
        result = validate_license("MIT")
        assert result is True

    def test_validate_license_valid_apache(self):
        """Test validate_license with Apache license."""
        result = validate_license("Apache-2.0")
        assert result is True

    def test_validate_license_valid_gpl(self):
        """Test validate_license with GPL license."""
        result = validate_license("GPL-3.0")
        assert result is True

    def test_validate_license_valid_custom_reasonable(self):
        """Test validate_license with valid custom license."""
        result = validate_license("Custom License v1.0")
        assert result is True

    def test_validate_license_invalid_too_long(self):
        """Test validate_license with invalid license (too long)."""
        long_license = "A" * 51
        result = validate_license(long_license)
        assert result is False

    def test_validate_license_invalid_dangerous_chars(self):
        """Test validate_license with invalid license (dangerous characters)."""
        result = validate_license("License<script>")
        assert result is False

    def test_validate_license_empty(self):
        """Test validate_license with empty string."""
        result = validate_license("")
        assert result is False

    def test_validate_license_none(self):
        """Test validate_license with None."""
        result = validate_license(None)
        assert result is False

    def test_validate_license_not_string(self):
        """Test validate_license with non-string input."""
        result = validate_license(123)
        assert result is False

    def test_sanitize_filename_basic(self):
        """Test sanitize_filename with basic valid filename."""
        result = sanitize_filename("document.txt")
        assert result == "document.txt"

    def test_sanitize_filename_with_invalid_chars(self):
        """Test sanitize_filename with invalid characters."""
        result = sanitize_filename("file<name>with:invalid|chars.txt")
        assert result == "file_name_with_invalid_chars.txt"

    def test_sanitize_filename_with_spaces(self):
        """Test sanitize_filename with leading/trailing spaces."""
        result = sanitize_filename("  filename.txt  ")
        assert result == "filename.txt"

    def test_sanitize_filename_with_dots(self):
        """Test sanitize_filename with leading/trailing dots."""
        result = sanitize_filename("..filename.txt..")
        assert result == "filename.txt"

    def test_sanitize_filename_empty_after_sanitization(self):
        """Test sanitize_filename that becomes empty after sanitization."""
        result = sanitize_filename("...")
        assert result == "unnamed"

    def test_sanitize_filename_empty_input(self):
        """Test sanitize_filename with empty input."""
        result = sanitize_filename("")
        assert result == "unnamed"

    def test_sanitize_filename_too_long(self):
        """Test sanitize_filename with filename too long."""
        long_name = "a" * 250
        extension = ".txt"
        long_filename = long_name + extension

        result = sanitize_filename(long_filename)

        assert len(result) <= 255
        assert result.endswith(extension)

    def test_sanitize_filename_custom_replacement(self):
        """Test sanitize_filename with custom replacement character."""
        result = sanitize_filename("file:name", replacement="-")
        assert result == "file-name"

    def test_sanitize_filename_control_chars(self):
        """Test sanitize_filename with control characters."""
        filename_with_control = "file\x00name\x1f.txt"
        result = sanitize_filename(filename_with_control)
        assert result == "file_name_.txt"
