"""NPM package installer for MCP servers."""

import json
import subprocess
from typing import Any, Dict, List, Optional

from mcpi.installer.base import BaseInstaller, InstallationResult, check_command_available
from mcpi.registry.catalog import InstallationMethod, MCPServer


class NPMInstaller(BaseInstaller):
    """Installer for NPM-based MCP servers."""

    def __init__(self, global_install: bool = True, dry_run: bool = False):
        """Initialize NPM installer.

        Args:
            global_install: If True, install packages globally
            dry_run: If True, simulate installation without making changes
        """
        super().__init__(dry_run=dry_run)
        self.global_install = global_install

    def install(
        self, server: MCPServer, config_params: Optional[Dict[str, Any]] = None
    ) -> InstallationResult:
        """Install NPM package.

        Args:
            server: MCP server to install
            config_params: Configuration parameters (unused for NPM)

        Returns:
            Installation result
        """
        if server.installation.method != InstallationMethod.NPM:
            return self._create_failure_result(
                server.id, f"Server {server.id} is not an NPM package"
            )

        # Check if npm is available
        if not self._check_npm_available():
            return self._create_failure_result(
                server.id, "npm is not available. Please install Node.js and npm."
            )

        # Check if package is already installed
        if self.is_installed(server.installation.package):
            return self._create_failure_result(
                server.id, f"Package {server.installation.package} is already installed"
            )

        # Install the package
        try:
            result = self._run_npm_command(
                ["install"] + self._get_install_flags() + [server.installation.package]
            )

            if result.returncode == 0:
                return self._create_success_result(
                    server.id,
                    f"Successfully installed {server.installation.package}",
                    package_name=server.installation.package,
                    install_method="npm",
                    global_install=self.global_install,
                    npm_output=result.stdout,
                )
            else:
                return self._create_failure_result(
                    server.id,
                    f"NPM installation failed: {result.stderr}",
                    npm_error=result.stderr,
                    return_code=result.returncode,
                )

        except Exception as e:
            return self._create_failure_result(
                server.id, f"NPM installation error: {str(e)}", exception=str(e)
            )

    def uninstall(self, server_id: str) -> InstallationResult:
        """Uninstall NPM package.

        Args:
            server_id: ID of server to uninstall (used as package name)

        Returns:
            Installation result
        """
        if not self._check_npm_available():
            return self._create_failure_result(server_id, "npm is not available")

        try:
            result = self._run_npm_command(
                ["uninstall"] + self._get_install_flags() + [server_id]
            )

            if result.returncode == 0:
                return self._create_success_result(
                    server_id,
                    f"Successfully uninstalled {server_id}",
                    package_name=server_id,
                    npm_output=result.stdout,
                )
            else:
                return self._create_failure_result(
                    server_id,
                    f"NPM uninstallation failed: {result.stderr}",
                    npm_error=result.stderr,
                    return_code=result.returncode,
                )

        except Exception as e:
            return self._create_failure_result(
                server_id, f"NPM uninstallation error: {str(e)}", exception=str(e)
            )

    def is_installed(self, package_name: str) -> bool:
        """Check if NPM package is installed.

        Args:
            package_name: Package name to check

        Returns:
            True if installed, False otherwise
        """
        if not self._check_npm_available():
            return False

        try:
            flags = ["-g"] if self.global_install else []
            result = self._run_npm_command(
                ["list"] + flags + [package_name, "--depth=0"]
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_installed_servers(self) -> List[str]:
        """Get list of installed NPM packages.

        Returns:
            List of installed package names
        """
        if not self._check_npm_available():
            return []

        try:
            flags = ["-g"] if self.global_install else []
            result = self._run_npm_command(["list"] + flags + ["--json", "--depth=0"])

            if result.returncode == 0:
                data = json.loads(result.stdout)
                dependencies = data.get("dependencies", {})
                return list(dependencies.keys())
            else:
                return []

        except Exception:
            return []

    def get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Get information about an NPM package.

        Args:
            package_name: Package name

        Returns:
            Package information or None if not found
        """
        if not self._check_npm_available():
            return None

        try:
            result = self._run_npm_command(["view", package_name, "--json"])

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return None

        except Exception:
            return None

    def update_package(self, package_name: str) -> InstallationResult:
        """Update NPM package to latest version.

        Args:
            package_name: Package name to update

        Returns:
            Installation result
        """
        if not self._check_npm_available():
            return self._create_failure_result(package_name, "npm is not available")

        if not self.is_installed(package_name):
            return self._create_failure_result(
                package_name, f"Package {package_name} is not installed"
            )

        try:
            result = self._run_npm_command(
                ["update"] + self._get_install_flags() + [package_name]
            )

            if result.returncode == 0:
                return self._create_success_result(
                    package_name,
                    f"Successfully updated {package_name}",
                    package_name=package_name,
                    npm_output=result.stdout,
                )
            else:
                return self._create_failure_result(
                    package_name,
                    f"NPM update failed: {result.stderr}",
                    npm_error=result.stderr,
                    return_code=result.returncode,
                )

        except Exception as e:
            return self._create_failure_result(
                package_name, f"NPM update error: {str(e)}", exception=str(e)
            )

    def _check_npm_available(self) -> bool:
        """Check if npm command is available."""
        return check_command_available("npm")

    def _get_install_flags(self) -> List[str]:
        """Get NPM install flags.

        Returns:
            List of NPM flags
        """
        flags = []
        if self.global_install:
            flags.append("-g")
        return flags

    def _run_npm_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run npm command with given arguments.

        Args:
            args: NPM command arguments

        Returns:
            Completed process result
        """
        if self.dry_run:
            # Simulate successful execution in dry run mode
            return subprocess.CompletedProcess(
                args=["npm"] + args,
                returncode=0,
                stdout=f"[DRY RUN] Would execute: npm {' '.join(args)}",
                stderr="",
            )

        return subprocess.run(
            ["npm"] + args,
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
        return method == InstallationMethod.NPM
