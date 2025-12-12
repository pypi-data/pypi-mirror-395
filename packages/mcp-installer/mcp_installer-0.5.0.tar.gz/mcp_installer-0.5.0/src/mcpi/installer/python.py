"""Python package installer for MCP servers."""

import subprocess
import sys
from typing import Any, Dict, List, Optional

from mcpi.installer.base import BaseInstaller, InstallationResult, check_command_available
from mcpi.registry.catalog import InstallationMethod, MCPServer


class PythonInstaller(BaseInstaller):
    """Installer for Python-based MCP servers."""

    def __init__(
        self,
        python_path: Optional[str] = None,
        use_uv: bool = True,
        dry_run: bool = False,
    ):
        """Initialize Python installer.

        Args:
            python_path: Path to Python executable
            use_uv: If True, prefer uv over pip
            dry_run: If True, simulate installation without making changes
        """
        super().__init__(dry_run=dry_run)
        self.python_path = python_path or sys.executable
        self.use_uv = use_uv
        self._package_manager = self._detect_package_manager()

    def _detect_package_manager(self) -> str:
        """Detect available Python package manager.

        Returns:
            Package manager to use ('uv' or 'pip')
        """
        if self.use_uv and self._check_uv_available():
            return "uv"
        else:
            return "pip"

    def install(
        self, server: MCPServer, config_params: Optional[Dict[str, Any]] = None
    ) -> InstallationResult:
        """Install Python package.

        Args:
            server: MCP server to install
            config_params: Configuration parameters (unused for Python)

        Returns:
            Installation result
        """
        if server.installation.method != InstallationMethod.PIP:
            return self._create_failure_result(
                server.id, f"Server {server.id} is not a Python package"
            )

        # Check if Python is available
        if not self._check_python_available():
            return self._create_failure_result(
                server.id, f"Python is not available at {self.python_path}"
            )

        # Install Python dependencies first
        if server.installation.python_dependencies:
            deps_result = self._install_dependencies(
                server.installation.python_dependencies
            )
            if not deps_result.success:
                return self._create_failure_result(
                    server.id,
                    f"Failed to install Python dependencies: {deps_result.message}",
                    dependency_error=deps_result.message,
                )

        # Install the main package
        try:
            if self._package_manager == "uv":
                result = self._run_uv_command(["add", server.installation.package])
            else:
                result = self._run_pip_command(["install", server.installation.package])

            if result.returncode == 0:
                # Get installation details
                install_details = self._get_install_details(server.installation.package)

                return self._create_success_result(
                    server.id,
                    f"Successfully installed {server.installation.package}",
                    package_name=server.installation.package,
                    install_method=self._package_manager,
                    python_path=self.python_path,
                    module_path=server.installation.package,
                    **install_details,
                )
            else:
                return self._create_failure_result(
                    server.id,
                    f"Python installation failed: {result.stderr}",
                    install_error=result.stderr,
                    return_code=result.returncode,
                )

        except Exception as e:
            return self._create_failure_result(
                server.id, f"Python installation error: {str(e)}", exception=str(e)
            )

    def _install_dependencies(self, dependencies: List[str]) -> InstallationResult:
        """Install Python dependencies.

        Args:
            dependencies: List of dependency packages

        Returns:
            Installation result
        """
        try:
            if self._package_manager == "uv":
                result = self._run_uv_command(["add"] + dependencies)
            else:
                result = self._run_pip_command(["install"] + dependencies)

            if result.returncode == 0:
                return InstallationResult(
                    status="success",
                    message=f"Successfully installed dependencies: {', '.join(dependencies)}",
                    server_id="dependencies",
                )
            else:
                return InstallationResult(
                    status="failed",
                    message=f"Failed to install dependencies: {result.stderr}",
                    server_id="dependencies",
                )

        except Exception as e:
            return InstallationResult(
                status="failed",
                message=f"Error installing dependencies: {str(e)}",
                server_id="dependencies",
            )

    def uninstall(self, server_id: str) -> InstallationResult:
        """Uninstall Python package.

        Args:
            server_id: Package name to uninstall

        Returns:
            Installation result
        """
        if not self._check_python_available():
            return self._create_failure_result(server_id, "Python is not available")

        try:
            if self._package_manager == "uv":
                result = self._run_uv_command(["remove", server_id])
            else:
                result = self._run_pip_command(["uninstall", "-y", server_id])

            if result.returncode == 0:
                return self._create_success_result(
                    server_id,
                    f"Successfully uninstalled {server_id}",
                    package_name=server_id,
                )
            else:
                return self._create_failure_result(
                    server_id,
                    f"Python uninstallation failed: {result.stderr}",
                    uninstall_error=result.stderr,
                    return_code=result.returncode,
                )

        except Exception as e:
            return self._create_failure_result(
                server_id, f"Python uninstallation error: {str(e)}", exception=str(e)
            )

    def is_installed(self, package_name: str) -> bool:
        """Check if Python package is installed.

        Args:
            package_name: Package name to check

        Returns:
            True if installed, False otherwise
        """
        if not self._check_python_available():
            return False

        try:
            if self._package_manager == "uv":
                # For uv, check if package is in pyproject.toml dependencies
                result = self._run_uv_command(["pip", "list"])
                return package_name in result.stdout
            else:
                result = self._run_pip_command(["show", package_name])
                return result.returncode == 0
        except Exception:
            return False

    def get_installed_servers(self) -> List[str]:
        """Get list of installed Python packages.

        Returns:
            List of installed package names
        """
        if not self._check_python_available():
            return []

        try:
            if self._package_manager == "uv":
                result = self._run_uv_command(["pip", "list", "--format=json"])
            else:
                result = self._run_pip_command(["list", "--format=json"])

            if result.returncode == 0:
                import json

                packages = json.loads(result.stdout)
                return [pkg["name"] for pkg in packages]
            else:
                return []

        except Exception:
            return []

    def get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a Python package.

        Args:
            package_name: Package name

        Returns:
            Package information or None if not found
        """
        if not self._check_python_available():
            return None

        try:
            if self._package_manager == "uv":
                result = self._run_uv_command(["pip", "show", package_name])
            else:
                result = self._run_pip_command(["show", package_name])

            if result.returncode == 0:
                # Parse pip show output
                info = {}
                for line in result.stdout.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        info[key.strip().lower()] = value.strip()
                return info
            else:
                return None

        except Exception:
            return None

    def update_package(self, package_name: str) -> InstallationResult:
        """Update Python package to latest version.

        Args:
            package_name: Package name to update

        Returns:
            Installation result
        """
        if not self._check_python_available():
            return self._create_failure_result(package_name, "Python is not available")

        if not self.is_installed(package_name):
            return self._create_failure_result(
                package_name, f"Package {package_name} is not installed"
            )

        try:
            if self._package_manager == "uv":
                # For uv, we need to update the package
                result = self._run_uv_command(["add", f"{package_name}@latest"])
            else:
                result = self._run_pip_command(["install", "--upgrade", package_name])

            if result.returncode == 0:
                return self._create_success_result(
                    package_name,
                    f"Successfully updated {package_name}",
                    package_name=package_name,
                )
            else:
                return self._create_failure_result(
                    package_name,
                    f"Python update failed: {result.stderr}",
                    update_error=result.stderr,
                    return_code=result.returncode,
                )

        except Exception as e:
            return self._create_failure_result(
                package_name, f"Python update error: {str(e)}", exception=str(e)
            )

    def _get_install_details(self, package_name: str) -> Dict[str, Any]:
        """Get details about installed package.

        Args:
            package_name: Package name

        Returns:
            Installation details
        """
        details = {}

        # Try to get package info
        package_info = self.get_package_info(package_name)
        if package_info:
            details["version"] = package_info.get("version", "unknown")
            details["location"] = package_info.get("location", "")

        return details

    def _check_python_available(self) -> bool:
        """Check if Python executable is available."""
        return check_command_available(self.python_path)

    def _check_uv_available(self) -> bool:
        """Check if uv command is available."""
        return check_command_available("uv")

    def _run_pip_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run pip command with given arguments.

        Args:
            args: Pip command arguments

        Returns:
            Completed process result
        """
        if self.dry_run:
            return subprocess.CompletedProcess(
                args=[self.python_path, "-m", "pip"] + args,
                returncode=0,
                stdout=f"[DRY RUN] Would execute: {self.python_path} -m pip {' '.join(args)}",
                stderr="",
            )

        return subprocess.run(
            [self.python_path, "-m", "pip"] + args,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

    def _run_uv_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run uv command with given arguments.

        Args:
            args: UV command arguments

        Returns:
            Completed process result
        """
        if self.dry_run:
            return subprocess.CompletedProcess(
                args=["uv"] + args,
                returncode=0,
                stdout=f"[DRY RUN] Would execute: uv {' '.join(args)}",
                stderr="",
            )

        return subprocess.run(
            ["uv"] + args,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

    def _supports_method(self, method: str) -> bool:
        """Check if installer supports the given method.

        Args:
            method: Installation method

        Returns:
            True if supported, False otherwise
        """
        return method == InstallationMethod.PIP
