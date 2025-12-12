"""Tests for installer base module."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from mcpi.installer.base import (
    BaseInstaller,
    InstallationResult,
    InstallationStatus,
)
from mcpi.registry.catalog import MCPServer


class TestInstallationStatus:
    """Tests for InstallationStatus enum."""

    def test_status_values(self):
        """Test status enum values."""
        assert InstallationStatus.SUCCESS == "success"
        assert InstallationStatus.FAILED == "failed"
        assert InstallationStatus.PARTIAL == "partial"
        assert InstallationStatus.SKIPPED == "skipped"


class TestInstallationResult:
    """Tests for InstallationResult dataclass."""

    def test_basic_creation(self):
        """Test basic result creation."""
        result = InstallationResult(
            status=InstallationStatus.SUCCESS,
            message="Install completed",
            server_id="test_server",
        )

        assert result.status == InstallationStatus.SUCCESS
        assert result.message == "Install completed"
        assert result.server_id == "test_server"
        assert result.config_path is None
        assert result.backup_path is None
        assert result.details == {}

    def test_creation_with_all_fields(self):
        """Test result creation with all fields."""
        config_path = Path("/test/config.json")
        backup_path = Path("/test/backup.json")
        details = {"key": "value"}

        result = InstallationResult(
            status=InstallationStatus.FAILED,
            message="Install failed",
            server_id="test_server",
            config_path=config_path,
            backup_path=backup_path,
            details=details,
        )

        assert result.status == InstallationStatus.FAILED
        assert result.message == "Install failed"
        assert result.server_id == "test_server"
        assert result.config_path == config_path
        assert result.backup_path == backup_path
        assert result.details == details

    def test_post_init_details_initialization(self):
        """Test that details is initialized if None."""
        result = InstallationResult(
            status=InstallationStatus.SUCCESS,
            message="Test",
            server_id="test",
            details=None,
        )

        assert result.details == {}

    def test_success_property(self):
        """Test success property."""
        success_result = InstallationResult(InstallationStatus.SUCCESS, "msg", "id")
        failed_result = InstallationResult(InstallationStatus.FAILED, "msg", "id")
        partial_result = InstallationResult(InstallationStatus.PARTIAL, "msg", "id")

        assert success_result.success is True
        assert failed_result.success is False
        assert partial_result.success is False

    def test_failed_property(self):
        """Test failed property."""
        success_result = InstallationResult(InstallationStatus.SUCCESS, "msg", "id")
        failed_result = InstallationResult(InstallationStatus.FAILED, "msg", "id")
        partial_result = InstallationResult(InstallationStatus.PARTIAL, "msg", "id")

        assert success_result.failed is False
        assert failed_result.failed is True
        assert partial_result.failed is False


class ConcreteInstaller(BaseInstaller):
    """Concrete implementation for testing."""

    def __init__(self, supports_method_result=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supports_method_result = supports_method_result

    def install(
        self, server: MCPServer, server_id: str, config_params=None
    ) -> InstallationResult:
        return self._create_success_result(server_id, "Installed")

    def uninstall(self, server_id: str) -> InstallationResult:
        return self._create_success_result(server_id, "Uninstalled")

    def is_installed(self, server_id: str) -> bool:
        return True

    def get_installed_servers(self):
        return ["server1", "server2"]

    def _supports_method(self, method: str) -> bool:
        return self.supports_method_result


class TestBaseInstaller:
    """Tests for BaseInstaller base class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.installer = ConcreteInstaller()
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            import shutil

            shutil.rmtree(self.temp_dir)

    def test_initialization_defaults(self):
        """Test installer initialization with defaults."""
        installer = ConcreteInstaller()

        assert installer.config_path is None
        assert installer.dry_run is False
        assert installer._backup_paths == []

    def test_initialization_with_params(self):
        """Test installer initialization with parameters."""
        config_path = Path("/test/config.json")
        installer = ConcreteInstaller(config_path=config_path, dry_run=True)

        assert installer.config_path == config_path
        assert installer.dry_run is True
        assert installer._backup_paths == []

    def create_mock_server(self, server_id="test_server", method="npm", sys_deps=None):
        """Create a mock MCPServer for testing."""
        if sys_deps is None:
            sys_deps = []

        mock_server = Mock(spec=MCPServer)
        mock_server.id = server_id
        mock_server.installation = Mock()
        mock_server.installation.method = method
        mock_server.installation.system_dependencies = sys_deps

        return mock_server

    @pytest.mark.skip(
        "Validation simplified - system dependency checking removed with simplified schema"
    )
    def test_validate_installation_no_errors(self):
        """Test validation with no errors."""
        server = self.create_mock_server()

        errors = self.installer.validate_installation(server, "test_server")

        assert errors == []

    @pytest.mark.skip(
        "Validation simplified - system dependency checking removed with simplified schema"
    )
    def test_validate_installation_missing_system_dependency(self):
        """Test validation with missing system dependency."""
        server = self.create_mock_server(sys_deps=["nonexistent_command"])

        with patch.object(
            self.installer, "_check_system_dependency", return_value=False
        ):
            errors = self.installer.validate_installation(server, "test_server")

        assert len(errors) == 1
        assert "Missing system dependency: nonexistent_command" in errors[0]

    @pytest.mark.skip(
        "Validation simplified - system dependency checking removed with simplified schema"
    )
    def test_validate_installation_unsupported_method(self):
        """Test validation with unsupported installation method."""
        server = self.create_mock_server(method="unsupported")
        installer = ConcreteInstaller(supports_method_result=False)

        errors = installer.validate_installation(server, "test_server")

        assert len(errors) == 1
        assert "Installation method not supported: unsupported" in errors[0]

    @pytest.mark.skip(
        "Validation simplified - system dependency checking removed with simplified schema"
    )
    def test_validate_installation_multiple_errors(self):
        """Test validation with multiple errors."""
        server = self.create_mock_server(method="unsupported", sys_deps=["missing_cmd"])
        installer = ConcreteInstaller(supports_method_result=False)

        with patch.object(installer, "_check_system_dependency", return_value=False):
            errors = installer.validate_installation(server, "test_server")

        assert len(errors) == 2
        assert any("Missing system dependency" in error for error in errors)
        assert any("Installation method not supported" in error for error in errors)

    @patch("shutil.which")
    @pytest.mark.skip(
        "Validation simplified - system dependency checking removed with simplified schema"
    )
    def test_check_system_dependency_available(self, mock_which):
        """Test system dependency check when dependency is available."""
        mock_which.return_value = "/usr/bin/dependency"

        result = self.installer._check_system_dependency("dependency")

        assert result is True
        mock_which.assert_called_once_with("dependency")

    @patch("shutil.which")
    @pytest.mark.skip(
        "Validation simplified - system dependency checking removed with simplified schema"
    )
    def test_check_system_dependency_missing(self, mock_which):
        """Test system dependency check when dependency is missing."""
        mock_which.return_value = None

        result = self.installer._check_system_dependency("missing_dependency")

        assert result is False
        mock_which.assert_called_once_with("missing_dependency")

    def test_create_backup_nonexistent_file(self):
        """Test backup creation for non-existent file."""
        non_existent = self.temp_dir / "nonexistent.txt"

        backup_path = self.installer.create_backup(non_existent)

        assert backup_path is None

    @patch("datetime.datetime")
    def test_create_backup_success(self, mock_datetime):
        """Test successful backup creation."""
        # Create a test file
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test content")

        # Mock datetime for predictable backup name
        mock_datetime.now.return_value.strftime.return_value = "20240101_120000"

        backup_path = self.installer.create_backup(test_file)

        assert backup_path is not None
        assert backup_path.name == "test.backup_20240101_120000"
        assert backup_path.exists()
        assert backup_path.read_text() == "test content"
        assert backup_path in self.installer._backup_paths

    @patch("shutil.copy2")
    def test_create_backup_failure(self, mock_copy2):
        """Test backup creation failure."""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test content")

        mock_copy2.side_effect = OSError("Permission denied")

        backup_path = self.installer.create_backup(test_file)

        assert backup_path is None

    def test_restore_backup_nonexistent_backup(self):
        """Test restore from non-existent backup."""
        backup_path = self.temp_dir / "nonexistent_backup.txt"
        target_path = self.temp_dir / "target.txt"

        result = self.installer.restore_backup(backup_path, target_path)

        assert result is False

    def test_restore_backup_success(self):
        """Test successful backup restore."""
        # Create backup and target files
        backup_path = self.temp_dir / "backup.txt"
        target_path = self.temp_dir / "target.txt"

        backup_path.write_text("backup content")
        target_path.write_text("original content")

        result = self.installer.restore_backup(backup_path, target_path)

        assert result is True
        assert target_path.read_text() == "backup content"

    @patch("shutil.copy2")
    def test_restore_backup_failure(self, mock_copy2):
        """Test backup restore failure."""
        backup_path = self.temp_dir / "backup.txt"
        target_path = self.temp_dir / "target.txt"
        backup_path.write_text("backup content")

        mock_copy2.side_effect = OSError("Permission denied")

        result = self.installer.restore_backup(backup_path, target_path)

        assert result is False

    def test_cleanup_backups_empty_list(self):
        """Test cleanup with empty backup list."""
        # Should not raise any exceptions
        self.installer.cleanup_backups()
        assert self.installer._backup_paths == []

    def test_cleanup_backups_success(self):
        """Test successful backup cleanup."""
        # Create backup files
        backup1 = self.temp_dir / "backup1.txt"
        backup2 = self.temp_dir / "backup2.txt"
        backup1.write_text("backup1")
        backup2.write_text("backup2")

        # Add to backup paths
        self.installer._backup_paths = [backup1, backup2]

        self.installer.cleanup_backups()

        assert not backup1.exists()
        assert not backup2.exists()
        assert self.installer._backup_paths == []

    def test_cleanup_backups_with_errors(self):
        """Test backup cleanup when some files can't be deleted."""
        # Create one real backup and one fake path
        backup1 = self.temp_dir / "backup1.txt"
        backup1.write_text("backup1")
        backup2 = Path("/nonexistent/backup2.txt")  # Will cause error

        self.installer._backup_paths = [backup1, backup2]

        # Should not raise exception despite error with backup2
        self.installer.cleanup_backups()

        assert not backup1.exists()
        assert self.installer._backup_paths == []

    def test_cleanup_backups_unlink_exception(self):
        """Test cleanup_backups when unlink raises an exception."""
        # Create a backup file
        backup_file = self.temp_dir / "backup.txt"
        backup_file.write_text("backup content")
        self.installer._backup_paths = [backup_file]

        # Mock unlink to raise an exception
        with patch.object(Path, "unlink", side_effect=OSError("Permission denied")):
            # This should not raise an exception - it should be caught and ignored
            self.installer.cleanup_backups()

        # The backup list should still be cleared even if unlink fails
        assert self.installer._backup_paths == []

    def test_create_success_result_basic(self):
        """Test creating basic success result."""
        result = self.installer._create_success_result("server1", "Success message")

        assert result.status == InstallationStatus.SUCCESS
        assert result.message == "Success message"
        assert result.server_id == "server1"
        assert result.config_path is None
        assert result.details == {}

    def test_create_success_result_with_details(self):
        """Test creating success result with details."""
        config_path = Path("/test/config.json")

        result = self.installer._create_success_result(
            "server1",
            "Success message",
            config_path=config_path,
            custom_detail="value",
            another_detail=123,
        )

        assert result.status == InstallationStatus.SUCCESS
        assert result.message == "Success message"
        assert result.server_id == "server1"
        assert result.config_path == config_path
        assert result.details == {"custom_detail": "value", "another_detail": 123}

    def test_create_failure_result_basic(self):
        """Test creating basic failure result."""
        result = self.installer._create_failure_result("server1", "Error message")

        assert result.status == InstallationStatus.FAILED
        assert result.message == "Error message"
        assert result.server_id == "server1"
        assert result.details == {}

    def test_create_failure_result_with_details(self):
        """Test creating failure result with details."""
        result = self.installer._create_failure_result(
            "server1", "Error message", error_code=500, exception="SomeException"
        )

        assert result.status == InstallationStatus.FAILED
        assert result.message == "Error message"
        assert result.server_id == "server1"
        assert result.details == {"error_code": 500, "exception": "SomeException"}

    def test_abstract_methods_implemented(self):
        """Test that concrete implementation provides abstract methods."""
        server = self.create_mock_server()

        # These should work since ConcreteInstaller implements them
        install_result = self.installer.install(server, "test_server")
        uninstall_result = self.installer.uninstall("server1")
        is_installed = self.installer.is_installed("server1")
        installed_servers = self.installer.get_installed_servers()

        assert install_result.success
        assert uninstall_result.success
        assert is_installed is True
        assert installed_servers == ["server1", "server2"]

    def test_installer_abstract_base_class(self):
        """Test that BaseInstaller cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseInstaller()


class TestBaseInstallerIntegration:
    """Integration tests for BaseInstaller functionality."""

    @pytest.mark.skip(
        "Validation simplified - system dependency checking removed with simplified schema"
    )
    def test_full_validation_workflow(self):
        """Test complete validation workflow with real-like scenario."""
        installer = ConcreteInstaller()

        # Create a server that needs git and python
        server = Mock(spec=MCPServer)
        server.id = "test_server"
        server.installation = Mock()
        server.installation.method = "git"
        server.installation.system_dependencies = ["git", "python3"]

        with patch.object(installer, "_check_system_dependency") as mock_check:
            # Mock that git is available but python3 is not
            mock_check.side_effect = lambda dep: dep == "git"

            errors = installer.validate_installation(server, "test_server")

        # Should have error for missing python3 but not git
        assert len(errors) == 1
        assert "Missing system dependency: python3" in errors[0]

    def test_backup_and_restore_workflow(self):
        """Test complete backup and restore workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            installer = ConcreteInstaller()

            # Create original file
            original_file = temp_path / "config.json"
            original_file.write_text('{"original": "content"}')

            # Create backup
            backup_path = installer.create_backup(original_file)
            assert backup_path is not None
            assert backup_path.exists()

            # Modify original file
            original_file.write_text('{"modified": "content"}')

            # Restore from backup
            result = installer.restore_backup(backup_path, original_file)
            assert result is True
            assert original_file.read_text() == '{"original": "content"}'

            # Cleanup
            installer.cleanup_backups()
            assert not backup_path.exists()


class TestResultMethods:
    """Test helper methods for creating results."""

    def test_result_helper_methods_return_correct_types(self):
        """Test that result helper methods return correct types."""
        installer = ConcreteInstaller()

        success_result = installer._create_success_result("id", "msg")
        failure_result = installer._create_failure_result("id", "msg")

        assert isinstance(success_result, InstallationResult)
        assert isinstance(failure_result, InstallationResult)
        assert success_result.success is True
        assert failure_result.failed is True
