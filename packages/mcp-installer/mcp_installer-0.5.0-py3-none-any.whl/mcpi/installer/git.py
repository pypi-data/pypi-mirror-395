"""Git repository installer for MCP servers."""

import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcpi.installer.base import BaseInstaller, InstallationResult, check_command_available
from mcpi.registry.catalog import InstallationMethod, MCPServer

# Configuration constants
DEFAULT_INSTALL_DIR = ".mcpi/servers"
GIT_TIMEOUT = 300  # 5 minutes for git operations
GIT_VERSION_TIMEOUT = 10  # 10 seconds for git version check
DEPENDENCY_TIMEOUT = 300  # 5 minutes for dependency installation


class GitInstaller(BaseInstaller):
    """Installer for Git-based MCP servers."""

    def __init__(self, install_dir: Optional[Path] = None, dry_run: bool = False):
        """Initialize Git installer.

        Args:
            install_dir: Directory to install Git repositories
            dry_run: If True, simulate installation without making changes
        """
        super().__init__(dry_run=dry_run)
        if install_dir is None:
            install_dir = Path.home() / DEFAULT_INSTALL_DIR
        self.install_dir = install_dir

    def install(
        self, server: MCPServer, config_params: Optional[Dict[str, Any]] = None
    ) -> InstallationResult:
        """Install MCP server from Git repository.

        Args:
            server: MCP server to install
            config_params: Configuration parameters

        Returns:
            Installation result
        """
        if server.installation.method != InstallationMethod.GIT:
            return self._create_failure_result(
                server.id, f"Server {server.id} is not a Git repository"
            )

        if config_params is None:
            config_params = {}

        # Check if git is available
        if not self._check_git_available():
            return self._create_failure_result(
                server.id, "git is not available. Please install Git."
            )

        # Determine repository URL
        repo_url = server.installation.package
        if not repo_url.startswith(("http://", "https://", "git@")):
            # If it's not a full URL, assume it's a GitHub repository
            if server.repository:
                repo_url = str(server.repository)
            else:
                return self._create_failure_result(
                    server.id, f"Invalid repository URL: {repo_url}"
                )

        # Determine installation path
        install_path = self.install_dir / server.id

        # Check if already installed
        if install_path.exists():
            return self._create_failure_result(
                server.id, f"Server {server.id} is already installed at {install_path}"
            )

        try:
            # Ensure install directory exists
            if not self.dry_run:
                self.install_dir.mkdir(parents=True, exist_ok=True)

            # Clone the repository
            clone_result = self._clone_repository(
                repo_url, install_path, config_params.get("branch")
            )
            if not clone_result.success:
                return clone_result

            # Install dependencies if needed
            deps_result = self._install_repository_dependencies(install_path, server)
            if not deps_result.success:
                # Clean up failed installation
                if install_path.exists() and not self.dry_run:
                    shutil.rmtree(install_path)
                return deps_result

            # Find executable script
            script_path = self._find_executable_script(install_path)

            return self._create_success_result(
                server.id,
                f"Successfully installed {server.name} from Git",
                repository_url=repo_url,
                install_path=str(install_path),
                script_path=str(script_path) if script_path else None,
                branch=config_params.get("branch", "main"),
            )

        except Exception as e:
            # Clean up on failure
            if install_path.exists() and not self.dry_run:
                shutil.rmtree(install_path, ignore_errors=True)

            return self._create_failure_result(
                server.id, f"Git installation error: {str(e)}", exception=str(e)
            )

    def uninstall(self, server_id: str) -> InstallationResult:
        """Uninstall Git-based MCP server.

        Args:
            server_id: ID of server to uninstall

        Returns:
            Installation result
        """
        install_path = self.install_dir / server_id

        if not install_path.exists():
            return self._create_failure_result(
                server_id, f"Server {server_id} is not installed"
            )

        try:
            if not self.dry_run:
                shutil.rmtree(install_path)

            return self._create_success_result(
                server_id,
                f"Successfully uninstalled {server_id}",
                install_path=str(install_path),
            )

        except Exception as e:
            return self._create_failure_result(
                server_id, f"Git uninstallation error: {str(e)}", exception=str(e)
            )

    def is_installed(self, server_id: str) -> bool:
        """Check if Git-based server is installed.

        Args:
            server_id: Server ID to check

        Returns:
            True if installed, False otherwise
        """
        install_path = self.install_dir / server_id
        return install_path.exists() and (install_path / ".git").exists()

    def get_installed_servers(self) -> List[str]:
        """Get list of installed Git-based server IDs.

        Returns:
            List of installed server IDs
        """
        if not self.install_dir.exists():
            return []

        installed = []
        for item in self.install_dir.iterdir():
            if item.is_dir() and (item / ".git").exists():
                installed.append(item.name)

        return sorted(installed)

    def update_server(
        self, server_id: str, branch: Optional[str] = None
    ) -> InstallationResult:
        """Update Git-based server by pulling latest changes.

        Args:
            server_id: Server ID to update
            branch: Branch to update to (if different from current)

        Returns:
            Installation result
        """
        install_path = self.install_dir / server_id

        if not self.is_installed(server_id):
            return self._create_failure_result(
                server_id, f"Server {server_id} is not installed"
            )

        try:
            # Switch branch if requested
            if branch:
                checkout_result = self._run_git_command(
                    ["checkout", branch], cwd=install_path
                )
                if checkout_result.returncode != 0:
                    return self._create_failure_result(
                        server_id,
                        f"Failed to checkout branch {branch}: {checkout_result.stderr}",
                        git_error=checkout_result.stderr,
                    )

            # Pull latest changes
            pull_result = self._run_git_command(["pull"], cwd=install_path)

            if pull_result.returncode == 0:
                return self._create_success_result(
                    server_id,
                    f"Successfully updated {server_id}",
                    install_path=str(install_path),
                    git_output=pull_result.stdout,
                )
            else:
                return self._create_failure_result(
                    server_id,
                    f"Git pull failed: {pull_result.stderr}",
                    git_error=pull_result.stderr,
                    return_code=pull_result.returncode,
                )

        except Exception as e:
            return self._create_failure_result(
                server_id, f"Git update error: {str(e)}", exception=str(e)
            )

    def get_server_info(self, server_id: str) -> Optional[Dict[str, Any]]:
        """Get information about installed Git server.

        Args:
            server_id: Server ID

        Returns:
            Server information or None if not found
        """
        install_path = self.install_dir / server_id

        if not self.is_installed(server_id):
            return None

        try:
            # Get current branch
            branch_result = self._run_git_command(
                ["branch", "--show-current"], cwd=install_path
            )
            current_branch = (
                branch_result.stdout.strip()
                if branch_result.returncode == 0
                else "unknown"
            )

            # Get remote URL
            remote_result = self._run_git_command(
                ["remote", "get-url", "origin"], cwd=install_path
            )
            remote_url = (
                remote_result.stdout.strip()
                if remote_result.returncode == 0
                else "unknown"
            )

            # Get latest commit
            commit_result = self._run_git_command(
                ["log", "-1", "--format=%H %s"], cwd=install_path
            )
            latest_commit = (
                commit_result.stdout.strip()
                if commit_result.returncode == 0
                else "unknown"
            )

            return {
                "install_path": str(install_path),
                "current_branch": current_branch,
                "remote_url": remote_url,
                "latest_commit": latest_commit,
            }

        except Exception:
            return None

    def _clone_repository(
        self, repo_url: str, install_path: Path, branch: Optional[str] = None
    ) -> InstallationResult:
        """Clone Git repository.

        Args:
            repo_url: Repository URL
            install_path: Path to install repository
            branch: Branch to clone

        Returns:
            Installation result
        """
        clone_args = ["clone"]
        if branch:
            clone_args.extend(["-b", branch])
        clone_args.extend([repo_url, str(install_path)])

        try:
            result = self._run_git_command(clone_args)

            if result.returncode == 0:
                return InstallationResult(
                    status="success",
                    message=f"Successfully cloned {repo_url}",
                    server_id="git_clone",
                )
            else:
                return InstallationResult(
                    status="failed",
                    message=f"Git clone failed: {result.stderr}",
                    server_id="git_clone",
                )

        except Exception as e:
            return InstallationResult(
                status="failed",
                message=f"Git clone error: {str(e)}",
                server_id="git_clone",
            )

    def _install_repository_dependencies(
        self, install_path: Path, server: MCPServer
    ) -> InstallationResult:
        """Install repository dependencies.

        Args:
            install_path: Path to repository
            server: Server information

        Returns:
            Installation result
        """
        # Check for requirements.txt (Python)
        requirements_txt = install_path / "requirements.txt"
        if requirements_txt.exists():
            try:
                if not self.dry_run:
                    subprocess.run(
                        ["pip", "install", "-r", str(requirements_txt)],
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=DEPENDENCY_TIMEOUT,
                    )
                return InstallationResult(
                    status="success",
                    message="Successfully installed Python dependencies",
                    server_id=server.id,
                )
            except subprocess.SubprocessError as e:
                return InstallationResult(
                    status="failed",
                    message=f"Failed to install Python dependencies: {str(e)}",
                    server_id=server.id,
                )

        # Check for package.json (Node.js)
        package_json = install_path / "package.json"
        if package_json.exists():
            try:
                if not self.dry_run:
                    subprocess.run(
                        ["npm", "install"],
                        cwd=install_path,
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=DEPENDENCY_TIMEOUT,
                    )
                return InstallationResult(
                    status="success",
                    message="Successfully installed Node.js dependencies",
                    server_id=server.id,
                )
            except subprocess.SubprocessError as e:
                return InstallationResult(
                    status="failed",
                    message=f"Failed to install Node.js dependencies: {str(e)}",
                    server_id=server.id,
                )

        # No dependencies to install
        return InstallationResult(
            status="success", message="No dependencies to install", server_id=server.id
        )

    def _find_executable_script(self, install_path: Path) -> Optional[Path]:
        """Find executable script in repository.

        Args:
            install_path: Path to repository

        Returns:
            Path to executable script or None
        """
        # Common executable names and patterns
        executable_names = [
            "main.py",
            "server.py",
            "app.py",
            "run.py",
            "start.py",
            "index.js",
            "server.js",
            "main.js",
        ]

        # Check for executable files
        for name in executable_names:
            script_path = install_path / name
            if script_path.exists():
                return script_path

        # Check in common directories
        for subdir in ["src", "app", "bin"]:
            subdir_path = install_path / subdir
            if subdir_path.exists():
                for name in executable_names:
                    script_path = subdir_path / name
                    if script_path.exists():
                        return script_path

        return None

    def _check_git_available(self) -> bool:
        """Check if git command is available."""
        return check_command_available("git", timeout=GIT_VERSION_TIMEOUT)

    def _run_git_command(
        self, args: List[str], cwd: Optional[Path] = None
    ) -> subprocess.CompletedProcess:
        """Run git command with given arguments.

        Args:
            args: Git command arguments
            cwd: Working directory for command

        Returns:
            Completed process result
        """
        if self.dry_run:
            return subprocess.CompletedProcess(
                args=["git"] + args,
                returncode=0,
                stdout=f"[DRY RUN] Would execute: git {' '.join(args)}",
                stderr="",
            )

        return subprocess.run(
            ["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=GIT_TIMEOUT
        )

    def _supports_method(self, method: str) -> bool:
        """Check if installer supports the given method.

        Args:
            method: Installation method

        Returns:
            True if supported, False otherwise
        """
        return method == InstallationMethod.GIT
