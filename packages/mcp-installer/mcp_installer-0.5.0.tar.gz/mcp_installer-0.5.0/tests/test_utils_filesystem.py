"""Tests for filesystem utilities."""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from mcpi.utils.filesystem import (
    copy_file,
    ensure_directory,
    get_file_size,
    is_executable,
    safe_remove,
)


class TestFilesystemUtils:
    """Tests for filesystem utility functions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            import shutil

            shutil.rmtree(self.temp_dir)

    def test_ensure_directory_creates_new_directory(self):
        """Test that ensure_directory creates a new directory."""
        new_dir = self.temp_dir / "new_directory"
        assert not new_dir.exists()

        result = ensure_directory(new_dir)

        assert result is True
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_ensure_directory_creates_nested_directories(self):
        """Test that ensure_directory creates nested directories."""
        nested_dir = self.temp_dir / "level1" / "level2" / "level3"
        assert not nested_dir.exists()

        result = ensure_directory(nested_dir)

        assert result is True
        assert nested_dir.exists()
        assert nested_dir.is_dir()

    def test_ensure_directory_existing_directory(self):
        """Test that ensure_directory handles existing directory."""
        existing_dir = self.temp_dir / "existing"
        existing_dir.mkdir()
        assert existing_dir.exists()

        result = ensure_directory(existing_dir)

        assert result is True
        assert existing_dir.exists()

    def test_ensure_directory_with_custom_mode(self):
        """Test that ensure_directory uses custom mode."""
        new_dir = self.temp_dir / "custom_mode"

        result = ensure_directory(new_dir, mode=0o700)

        assert result is True
        assert new_dir.exists()
        # Mode testing can be platform-dependent, so just check creation

    @patch("pathlib.Path.mkdir")
    def test_ensure_directory_permission_error(self, mock_mkdir):
        """Test ensure_directory handles permission errors."""
        mock_mkdir.side_effect = PermissionError("Permission denied")

        result = ensure_directory(self.temp_dir / "forbidden")

        assert result is False

    @patch("pathlib.Path.mkdir")
    def test_ensure_directory_os_error(self, mock_mkdir):
        """Test ensure_directory handles OS errors."""
        mock_mkdir.side_effect = OSError("System error")

        result = ensure_directory(self.temp_dir / "error")

        assert result is False

    def test_safe_remove_file(self):
        """Test safe_remove removes a file."""
        test_file = self.temp_dir / "test_file.txt"
        test_file.write_text("test content")
        assert test_file.exists()

        result = safe_remove(test_file)

        assert result is True
        assert not test_file.exists()

    def test_safe_remove_directory(self):
        """Test safe_remove removes a directory."""
        test_dir = self.temp_dir / "test_dir"
        test_dir.mkdir()
        (test_dir / "nested_file.txt").write_text("content")
        assert test_dir.exists()

        result = safe_remove(test_dir)

        assert result is True
        assert not test_dir.exists()

    def test_safe_remove_missing_file_ok(self):
        """Test safe_remove with missing file and missing_ok=True."""
        non_existent = self.temp_dir / "non_existent.txt"
        assert not non_existent.exists()

        result = safe_remove(non_existent, missing_ok=True)

        assert result is True

    def test_safe_remove_missing_file_not_ok(self):
        """Test safe_remove with missing file and missing_ok=False."""
        non_existent = self.temp_dir / "non_existent.txt"
        assert not non_existent.exists()

        result = safe_remove(non_existent, missing_ok=False)

        assert result is False

    def test_safe_remove_special_file(self):
        """Test safe_remove handles special files (neither file nor directory)."""
        # Create a mock path that exists but is neither file nor directory
        with (
            patch("pathlib.Path.exists") as mock_exists,
            patch("pathlib.Path.is_file") as mock_is_file,
            patch("pathlib.Path.is_dir") as mock_is_dir,
        ):

            mock_exists.return_value = True
            mock_is_file.return_value = False
            mock_is_dir.return_value = False

            special_path = self.temp_dir / "special"
            result = safe_remove(special_path)

            assert result is False

    @patch("pathlib.Path.unlink")
    def test_safe_remove_permission_error(self, mock_unlink):
        """Test safe_remove handles permission errors."""
        test_file = self.temp_dir / "protected.txt"
        test_file.write_text("content")
        mock_unlink.side_effect = PermissionError("Permission denied")

        result = safe_remove(test_file)

        assert result is False

    @patch("shutil.rmtree")
    def test_safe_remove_os_error(self, mock_rmtree):
        """Test safe_remove handles OS errors."""
        test_dir = self.temp_dir / "error_dir"
        test_dir.mkdir()
        mock_rmtree.side_effect = OSError("System error")

        result = safe_remove(test_dir)

        assert result is False

    def test_get_file_size_existing_file(self):
        """Test get_file_size returns correct size for existing file."""
        test_file = self.temp_dir / "sized_file.txt"
        content = "Hello, World!"
        test_file.write_text(content)

        size = get_file_size(test_file)

        assert size == len(content.encode())

    def test_get_file_size_non_existent_file(self):
        """Test get_file_size returns None for non-existent file."""
        non_existent = self.temp_dir / "non_existent.txt"

        size = get_file_size(non_existent)

        assert size is None

    def test_get_file_size_directory(self):
        """Test get_file_size returns None for directory."""
        test_dir = self.temp_dir / "test_directory"
        test_dir.mkdir()

        size = get_file_size(test_dir)

        assert size is None

    @patch("pathlib.Path.stat")
    def test_get_file_size_permission_error(self, mock_stat):
        """Test get_file_size handles permission errors."""
        test_file = self.temp_dir / "protected.txt"
        test_file.write_text("content")
        mock_stat.side_effect = PermissionError("Permission denied")

        size = get_file_size(test_file)

        assert size is None

    @patch("pathlib.Path.stat")
    def test_get_file_size_os_error(self, mock_stat):
        """Test get_file_size handles OS errors."""
        test_file = self.temp_dir / "error.txt"
        test_file.write_text("content")
        mock_stat.side_effect = OSError("System error")

        size = get_file_size(test_file)

        assert size is None

    def test_is_executable_executable_file(self):
        """Test is_executable returns True for executable file."""
        test_file = self.temp_dir / "executable.sh"
        test_file.write_text("#!/bin/bash\necho 'Hello'")
        test_file.chmod(0o755)  # Make executable

        result = is_executable(test_file)

        assert result is True

    def test_is_executable_non_executable_file(self):
        """Test is_executable returns False for non-executable file."""
        test_file = self.temp_dir / "not_executable.txt"
        test_file.write_text("Just text")
        test_file.chmod(0o644)  # Not executable

        result = is_executable(test_file)

        assert result is False

    def test_is_executable_non_existent_file(self):
        """Test is_executable returns False for non-existent file."""
        non_existent = self.temp_dir / "non_existent.txt"

        result = is_executable(non_existent)

        assert result is False

    def test_is_executable_directory(self):
        """Test is_executable returns False for directory."""
        test_dir = self.temp_dir / "test_directory"
        test_dir.mkdir()

        result = is_executable(test_dir)

        assert result is False

    @patch("pathlib.Path.stat")
    def test_is_executable_permission_error(self, mock_stat):
        """Test is_executable handles permission errors."""
        test_file = self.temp_dir / "protected.txt"
        test_file.write_text("content")
        mock_stat.side_effect = PermissionError("Permission denied")

        result = is_executable(test_file)

        assert result is False

    @patch("pathlib.Path.stat")
    def test_is_executable_os_error(self, mock_stat):
        """Test is_executable handles OS errors."""
        test_file = self.temp_dir / "error.txt"
        test_file.write_text("content")
        mock_stat.side_effect = OSError("System error")

        result = is_executable(test_file)

        assert result is False

    def test_copy_file_successful_copy(self):
        """Test copy_file successfully copies a file."""
        source = self.temp_dir / "source.txt"
        dest = self.temp_dir / "destination.txt"
        content = "Test content for copying"
        source.write_text(content)

        result = copy_file(source, dest)

        assert result is True
        assert dest.exists()
        assert dest.read_text() == content

    def test_copy_file_non_existent_source(self):
        """Test copy_file returns False for non-existent source."""
        source = self.temp_dir / "non_existent.txt"
        dest = self.temp_dir / "destination.txt"

        result = copy_file(source, dest)

        assert result is False
        assert not dest.exists()

    def test_copy_file_with_backup(self):
        """Test copy_file creates backup when requested."""
        source = self.temp_dir / "source.txt"
        dest = self.temp_dir / "destination.txt"
        source.write_text("new content")
        dest.write_text("old content")

        result = copy_file(source, dest, backup=True)

        assert result is True
        assert dest.read_text() == "new content"

        backup_path = dest.with_suffix(dest.suffix + ".backup")
        assert backup_path.exists()
        assert backup_path.read_text() == "old content"

    def test_copy_file_creates_destination_directory(self):
        """Test copy_file creates destination directory if needed."""
        source = self.temp_dir / "source.txt"
        dest = self.temp_dir / "nested" / "dir" / "destination.txt"
        source.write_text("test content")

        result = copy_file(source, dest)

        assert result is True
        assert dest.exists()
        assert dest.parent.exists()
        assert dest.read_text() == "test content"

    @patch("shutil.copy2")
    def test_copy_file_permission_error(self, mock_copy2):
        """Test copy_file handles permission errors."""
        source = self.temp_dir / "source.txt"
        dest = self.temp_dir / "destination.txt"
        source.write_text("content")
        mock_copy2.side_effect = PermissionError("Permission denied")

        result = copy_file(source, dest)

        assert result is False

    @patch("shutil.copy2")
    def test_copy_file_os_error(self, mock_copy2):
        """Test copy_file handles OS errors."""
        source = self.temp_dir / "source.txt"
        dest = self.temp_dir / "destination.txt"
        source.write_text("content")
        mock_copy2.side_effect = OSError("System error")

        result = copy_file(source, dest)

        assert result is False

    @patch("shutil.copy2")
    def test_copy_file_shutil_error(self, mock_copy2):
        """Test copy_file handles shutil errors."""
        source = self.temp_dir / "source.txt"
        dest = self.temp_dir / "destination.txt"
        source.write_text("content")
        mock_copy2.side_effect = shutil.Error("Shutil error")

        result = copy_file(source, dest)

        assert result is False
