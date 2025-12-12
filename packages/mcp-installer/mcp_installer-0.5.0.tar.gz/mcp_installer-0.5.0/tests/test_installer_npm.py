"""Tests for NPM installer module."""

import json
import subprocess
from unittest.mock import Mock, patch

from mcpi.installer.npm import NPMInstaller
from mcpi.registry.catalog import InstallationMethod, MCPServer


class TestNPMInstaller:
    """Tests for NPMInstaller class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.installer = NPMInstaller(global_install=True, dry_run=False)
        self.installer_local = NPMInstaller(global_install=False, dry_run=False)
        self.installer_dry_run = NPMInstaller(global_install=True, dry_run=True)

    def create_mock_server(
        self,
        server_id="test_server",
        package="test-package",
        method=InstallationMethod.NPM,
    ):
        """Create a mock MCPServer for testing."""
        mock_server = Mock(spec=MCPServer)
        mock_server.id = server_id
        mock_server.name = f"Test {server_id}"
        mock_server.installation = Mock()
        mock_server.installation.method = method
        mock_server.installation.package = package

        return mock_server

    def test_initialization_defaults(self):
        """Test NPM installer initialization with defaults."""
        installer = NPMInstaller()

        assert installer.global_install is True
        assert installer.dry_run is False

    def test_initialization_with_params(self):
        """Test NPM installer initialization with parameters."""
        installer = NPMInstaller(global_install=False, dry_run=True)

        assert installer.global_install is False
        assert installer.dry_run is True

    @patch("mcpi.installer.npm.subprocess.run")
    def test_check_npm_available_success(self, mock_run):
        """Test npm availability check when npm is available."""
        mock_run.return_value.returncode = 0

        result = self.installer._check_npm_available()

        assert result is True
        mock_run.assert_called_once_with(
            ["npm", "--version"], capture_output=True, text=True, timeout=10
        )

    @patch("mcpi.installer.npm.subprocess.run")
    def test_check_npm_available_not_found(self, mock_run):
        """Test npm availability check when npm is not found."""
        mock_run.side_effect = FileNotFoundError()

        result = self.installer._check_npm_available()

        assert result is False

    @patch("mcpi.installer.npm.subprocess.run")
    def test_check_npm_available_subprocess_error(self, mock_run):
        """Test npm availability check when subprocess error occurs."""
        mock_run.side_effect = subprocess.SubprocessError()

        result = self.installer._check_npm_available()

        assert result is False

    @patch("mcpi.installer.npm.subprocess.run")
    def test_check_npm_available_non_zero_return(self, mock_run):
        """Test npm availability check when npm returns non-zero exit code."""
        mock_run.return_value.returncode = 1

        result = self.installer._check_npm_available()

        assert result is False

    def test_get_install_flags_global(self):
        """Test install flags for global installation."""
        flags = self.installer._get_install_flags()

        assert flags == ["-g"]

    def test_get_install_flags_local(self):
        """Test install flags for local installation."""
        flags = self.installer_local._get_install_flags()

        assert flags == []

    def test_run_npm_command_dry_run(self):
        """Test npm command execution in dry run mode."""
        result = self.installer_dry_run._run_npm_command(["install", "test-package"])

        assert result.args == ["npm", "install", "test-package"]
        assert result.returncode == 0
        assert result.stdout == "[DRY RUN] Would execute: npm install test-package"
        assert result.stderr == ""

    @patch("mcpi.installer.npm.subprocess.run")
    def test_run_npm_command_real(self, mock_run):
        """Test real npm command execution."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "success output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = self.installer._run_npm_command(["install", "test-package"])

        assert result == mock_result
        mock_run.assert_called_once_with(
            ["npm", "install", "test-package"],
            capture_output=True,
            text=True,
            timeout=300,
        )

    def test_supports_method_npm(self):
        """Test method support check for NPM method."""
        result = self.installer._supports_method(InstallationMethod.NPM)

        assert result is True

    def test_supports_method_other(self):
        """Test method support check for other methods."""
        result = self.installer._supports_method(InstallationMethod.PIP)

        assert result is False

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "is_installed")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_install_success(self, mock_run_npm, mock_is_installed, mock_check_npm):
        """Test successful package installation."""
        server = self.create_mock_server()
        mock_check_npm.return_value = True
        mock_is_installed.return_value = False

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "package installed successfully"
        mock_result.stderr = ""
        mock_run_npm.return_value = mock_result

        result = self.installer.install(server)

        assert result.success is True
        assert result.server_id == "test_server"
        assert "Successfully installed test-package" in result.message
        assert result.details["package_name"] == "test-package"
        assert result.details["global_install"] is True
        mock_run_npm.assert_called_once_with(["install", "-g", "test-package"])

    def test_install_wrong_method(self):
        """Test installation with wrong method."""
        server = self.create_mock_server(method=InstallationMethod.PIP)

        result = self.installer.install(server)

        assert result.failed is True
        assert "not an NPM package" in result.message

    @patch.object(NPMInstaller, "_check_npm_available")
    def test_install_npm_not_available(self, mock_check_npm):
        """Test installation when npm is not available."""
        server = self.create_mock_server()
        mock_check_npm.return_value = False

        result = self.installer.install(server)

        assert result.failed is True
        assert "npm is not available" in result.message

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "is_installed")
    def test_install_already_installed(self, mock_is_installed, mock_check_npm):
        """Test installation when package is already installed."""
        server = self.create_mock_server()
        mock_check_npm.return_value = True
        mock_is_installed.return_value = True

        result = self.installer.install(server)

        assert result.failed is True
        assert "already installed" in result.message

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "is_installed")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_install_npm_failure(self, mock_run_npm, mock_is_installed, mock_check_npm):
        """Test installation when npm command fails."""
        server = self.create_mock_server()
        mock_check_npm.return_value = True
        mock_is_installed.return_value = False

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "package not found"
        mock_run_npm.return_value = mock_result

        result = self.installer.install(server)

        assert result.failed is True
        assert "NPM installation failed" in result.message
        assert result.details["npm_error"] == "package not found"
        assert result.details["return_code"] == 1

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "is_installed")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_install_exception(self, mock_run_npm, mock_is_installed, mock_check_npm):
        """Test installation when exception occurs."""
        server = self.create_mock_server()
        mock_check_npm.return_value = True
        mock_is_installed.return_value = False
        mock_run_npm.side_effect = Exception("Network error")

        result = self.installer.install(server)

        assert result.failed is True
        assert "NPM installation error" in result.message
        assert result.details["exception"] == "Network error"

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_uninstall_success(self, mock_run_npm, mock_check_npm):
        """Test successful package uninstallation."""
        mock_check_npm.return_value = True

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "package uninstalled"
        mock_result.stderr = ""
        mock_run_npm.return_value = mock_result

        result = self.installer.uninstall("test-package")

        assert result.success is True
        assert "Successfully uninstalled test-package" in result.message
        assert result.details["package_name"] == "test-package"
        mock_run_npm.assert_called_once_with(["uninstall", "-g", "test-package"])

    @patch.object(NPMInstaller, "_check_npm_available")
    def test_uninstall_npm_not_available(self, mock_check_npm):
        """Test uninstallation when npm is not available."""
        mock_check_npm.return_value = False

        result = self.installer.uninstall("test-package")

        assert result.failed is True
        assert "npm is not available" in result.message

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_uninstall_failure(self, mock_run_npm, mock_check_npm):
        """Test uninstallation when npm command fails."""
        mock_check_npm.return_value = True

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "package not found"
        mock_run_npm.return_value = mock_result

        result = self.installer.uninstall("test-package")

        assert result.failed is True
        assert "NPM uninstallation failed" in result.message
        assert result.details["npm_error"] == "package not found"

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_uninstall_exception(self, mock_run_npm, mock_check_npm):
        """Test uninstallation when exception occurs."""
        mock_check_npm.return_value = True
        mock_run_npm.side_effect = Exception("Permission denied")

        result = self.installer.uninstall("test-package")

        assert result.failed is True
        assert "NPM uninstallation error" in result.message
        assert result.details["exception"] == "Permission denied"

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_is_installed_true(self, mock_run_npm, mock_check_npm):
        """Test package installation check when package is installed."""
        mock_check_npm.return_value = True

        mock_result = Mock()
        mock_result.returncode = 0
        mock_run_npm.return_value = mock_result

        result = self.installer.is_installed("test-package")

        assert result is True
        mock_run_npm.assert_called_once_with(
            ["list", "-g", "test-package", "--depth=0"]
        )

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_is_installed_false(self, mock_run_npm, mock_check_npm):
        """Test package installation check when package is not installed."""
        mock_check_npm.return_value = True

        mock_result = Mock()
        mock_result.returncode = 1
        mock_run_npm.return_value = mock_result

        result = self.installer.is_installed("test-package")

        assert result is False

    @patch.object(NPMInstaller, "_check_npm_available")
    def test_is_installed_npm_not_available(self, mock_check_npm):
        """Test package installation check when npm is not available."""
        mock_check_npm.return_value = False

        result = self.installer.is_installed("test-package")

        assert result is False

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_is_installed_exception(self, mock_run_npm, mock_check_npm):
        """Test package installation check when exception occurs."""
        mock_check_npm.return_value = True
        mock_run_npm.side_effect = Exception("Network error")

        result = self.installer.is_installed("test-package")

        assert result is False

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_get_installed_servers_success(self, mock_run_npm, mock_check_npm):
        """Test getting list of installed packages."""
        mock_check_npm.return_value = True

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps(
            {
                "dependencies": {
                    "package1": {"version": "1.0.0"},
                    "package2": {"version": "2.0.0"},
                }
            }
        )
        mock_run_npm.return_value = mock_result

        result = self.installer.get_installed_servers()

        assert result == ["package1", "package2"]
        mock_run_npm.assert_called_once_with(["list", "-g", "--json", "--depth=0"])

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_get_installed_servers_no_dependencies(self, mock_run_npm, mock_check_npm):
        """Test getting installed packages when no dependencies exist."""
        mock_check_npm.return_value = True

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({})
        mock_run_npm.return_value = mock_result

        result = self.installer.get_installed_servers()

        assert result == []

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_get_installed_servers_command_failure(self, mock_run_npm, mock_check_npm):
        """Test getting installed packages when npm command fails."""
        mock_check_npm.return_value = True

        mock_result = Mock()
        mock_result.returncode = 1
        mock_run_npm.return_value = mock_result

        result = self.installer.get_installed_servers()

        assert result == []

    @patch.object(NPMInstaller, "_check_npm_available")
    def test_get_installed_servers_npm_not_available(self, mock_check_npm):
        """Test getting installed packages when npm is not available."""
        mock_check_npm.return_value = False

        result = self.installer.get_installed_servers()

        assert result == []

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_get_installed_servers_exception(self, mock_run_npm, mock_check_npm):
        """Test getting installed packages when exception occurs."""
        mock_check_npm.return_value = True
        mock_run_npm.side_effect = Exception("JSON parse error")

        result = self.installer.get_installed_servers()

        assert result == []

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_get_package_info_success(self, mock_run_npm, mock_check_npm):
        """Test getting package information successfully."""
        mock_check_npm.return_value = True

        package_info = {
            "name": "test-package",
            "version": "1.2.3",
            "description": "A test package",
        }

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps(package_info)
        mock_run_npm.return_value = mock_result

        result = self.installer.get_package_info("test-package")

        assert result == package_info
        mock_run_npm.assert_called_once_with(["view", "test-package", "--json"])

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_get_package_info_not_found(self, mock_run_npm, mock_check_npm):
        """Test getting package information when package not found."""
        mock_check_npm.return_value = True

        mock_result = Mock()
        mock_result.returncode = 1
        mock_run_npm.return_value = mock_result

        result = self.installer.get_package_info("nonexistent-package")

        assert result is None

    @patch.object(NPMInstaller, "_check_npm_available")
    def test_get_package_info_npm_not_available(self, mock_check_npm):
        """Test getting package information when npm is not available."""
        mock_check_npm.return_value = False

        result = self.installer.get_package_info("test-package")

        assert result is None

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_get_package_info_exception(self, mock_run_npm, mock_check_npm):
        """Test getting package information when exception occurs."""
        mock_check_npm.return_value = True
        mock_run_npm.side_effect = Exception("Network error")

        result = self.installer.get_package_info("test-package")

        assert result is None

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "is_installed")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_update_package_success(
        self, mock_run_npm, mock_is_installed, mock_check_npm
    ):
        """Test successful package update."""
        mock_check_npm.return_value = True
        mock_is_installed.return_value = True

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "package updated"
        mock_result.stderr = ""
        mock_run_npm.return_value = mock_result

        result = self.installer.update_package("test-package")

        assert result.success is True
        assert "Successfully updated test-package" in result.message
        mock_run_npm.assert_called_once_with(["update", "-g", "test-package"])

    @patch.object(NPMInstaller, "_check_npm_available")
    def test_update_package_npm_not_available(self, mock_check_npm):
        """Test package update when npm is not available."""
        mock_check_npm.return_value = False

        result = self.installer.update_package("test-package")

        assert result.failed is True
        assert "npm is not available" in result.message

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "is_installed")
    def test_update_package_not_installed(self, mock_is_installed, mock_check_npm):
        """Test package update when package is not installed."""
        mock_check_npm.return_value = True
        mock_is_installed.return_value = False

        result = self.installer.update_package("test-package")

        assert result.failed is True
        assert "not installed" in result.message

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "is_installed")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_update_package_failure(
        self, mock_run_npm, mock_is_installed, mock_check_npm
    ):
        """Test package update when npm command fails."""
        mock_check_npm.return_value = True
        mock_is_installed.return_value = True

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "update failed"
        mock_run_npm.return_value = mock_result

        result = self.installer.update_package("test-package")

        assert result.failed is True
        assert "NPM update failed" in result.message
        assert result.details["npm_error"] == "update failed"

    @patch.object(NPMInstaller, "_check_npm_available")
    @patch.object(NPMInstaller, "is_installed")
    @patch.object(NPMInstaller, "_run_npm_command")
    def test_update_package_exception(
        self, mock_run_npm, mock_is_installed, mock_check_npm
    ):
        """Test package update when exception occurs."""
        mock_check_npm.return_value = True
        mock_is_installed.return_value = True
        mock_run_npm.side_effect = Exception("Permission error")

        result = self.installer.update_package("test-package")

        assert result.failed is True
        assert "NPM update error" in result.message
        assert result.details["exception"] == "Permission error"

    def test_is_installed_local_installer(self):
        """Test that local installer uses correct flags."""
        with (
            patch.object(
                self.installer_local, "_check_npm_available", return_value=True
            ),
            patch.object(self.installer_local, "_run_npm_command") as mock_run_npm,
        ):

            mock_result = Mock()
            mock_result.returncode = 0
            mock_run_npm.return_value = mock_result

            self.installer_local.is_installed("test-package")

            mock_run_npm.assert_called_once_with(["list", "test-package", "--depth=0"])

    def test_get_installed_servers_local_installer(self):
        """Test that local installer uses correct flags for listing packages."""
        with (
            patch.object(
                self.installer_local, "_check_npm_available", return_value=True
            ),
            patch.object(self.installer_local, "_run_npm_command") as mock_run_npm,
        ):

            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = json.dumps({"dependencies": {}})
            mock_run_npm.return_value = mock_result

            self.installer_local.get_installed_servers()

            mock_run_npm.assert_called_once_with(["list", "--json", "--depth=0"])


class TestNPMInstallerIntegration:
    """Integration tests for NPM installer functionality."""

    def test_full_installation_workflow(self):
        """Test complete installation workflow."""
        installer = NPMInstaller(dry_run=True)
        server = Mock(spec=MCPServer)
        server.id = "test-server"
        server.name = "Test Server"
        server.installation = Mock()
        server.installation.method = InstallationMethod.NPM
        server.installation.package = "test-package"

        with (
            patch.object(installer, "_check_npm_available", return_value=True),
            patch.object(installer, "is_installed", return_value=False),
        ):

            result = installer.install(server)

            assert result.success is True
            assert "test-package" in result.message
            assert result.details["package_name"] == "test-package"

    def test_method_validation(self):
        """Test that installer validates installation method."""
        installer = NPMInstaller()

        # Test with correct method
        assert installer._supports_method(InstallationMethod.NPM) is True

        # Test with incorrect methods
        assert installer._supports_method(InstallationMethod.PIP) is False
        assert installer._supports_method(InstallationMethod.GIT) is False
