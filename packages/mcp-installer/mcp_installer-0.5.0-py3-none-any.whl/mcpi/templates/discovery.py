"""Project detection system for template recommendations.

This module provides functionality to analyze project directories and detect
characteristics that can inform template recommendations (Docker usage, language,
databases, etc.).
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class ProjectContext:
    """Detected characteristics of a project directory.

    This data class holds all the detected characteristics that will be used
    by the recommendation engine to score and rank templates.

    Attributes:
        has_docker: Whether the project uses Docker (Dockerfile exists)
        has_docker_compose: Whether the project uses Docker Compose (docker-compose.yml exists)
        docker_services: List of service names from docker-compose.yml
        language: Detected primary programming language (nodejs, python, go, etc.)
        databases: List of detected database systems (postgres, mysql, redis, etc.)
        project_path: Path to the analyzed project directory
    """

    has_docker: bool = False
    has_docker_compose: bool = False
    docker_services: list[str] = field(default_factory=list)
    language: Optional[str] = None
    databases: list[str] = field(default_factory=list)
    project_path: Optional[Path] = None


class ProjectDetector:
    """Analyzes project directories to detect characteristics for template recommendations.

    The detector examines project files (docker-compose.yml, package.json, requirements.txt,
    etc.) to build a ProjectContext that describes the project's technology stack and
    infrastructure requirements.

    Example:
        ```python
        detector = ProjectDetector()
        context = detector.detect(Path("/path/to/project"))

        if context.has_docker_compose and "postgres" in context.docker_services:
            # Recommend Docker-based postgres template
            pass
        ```

    Methods:
        detect: Analyze a project directory and return detected characteristics
    """

    # Known database service names and image patterns
    DATABASE_PATTERNS = {
        "postgres": ["postgres", "postgresql"],
        "mysql": ["mysql", "mariadb"],
        "redis": ["redis"],
        "mongodb": ["mongo", "mongodb"],
        "sqlite": ["sqlite"],
    }

    def detect(self, project_path: Path) -> ProjectContext:
        """Analyze project directory and detect characteristics.

        Examines the project directory for files and patterns that indicate:
        - Docker usage (Dockerfile, docker-compose.yml)
        - Programming language (package.json, requirements.txt, go.mod, etc.)
        - Database services (from docker-compose, environment files, config files)

        Args:
            project_path: Path to the project directory to analyze

        Returns:
            ProjectContext with detected characteristics

        Note:
            Handles errors gracefully:
            - Corrupted YAML files → return empty services list
            - Missing files → return empty/False values
            - Invalid project path → return empty context
        """
        context = ProjectContext(project_path=project_path)

        if not project_path.exists() or not project_path.is_dir():
            return context

        # Detect Docker usage
        context.has_docker = self._detect_docker(project_path)
        context.has_docker_compose = self._detect_docker_compose(project_path)

        # Docker Compose implies Docker usage
        if context.has_docker_compose:
            context.has_docker = True

        # Parse docker-compose.yml for services
        if context.has_docker_compose:
            context.docker_services = self._parse_docker_compose_services(project_path)

        # Detect language
        context.language = self._detect_language(project_path)

        # Detect databases
        context.databases = self._detect_databases(project_path, context)

        return context

    def _detect_docker(self, project_path: Path) -> bool:
        """Check if project uses Docker (Dockerfile exists).

        Args:
            project_path: Path to project directory

        Returns:
            True if Dockerfile exists
        """
        return (project_path / "Dockerfile").exists()

    def _detect_docker_compose(self, project_path: Path) -> bool:
        """Check if project uses Docker Compose.

        Args:
            project_path: Path to project directory

        Returns:
            True if docker-compose.yml or docker-compose.yaml exists
        """
        return (
            (project_path / "docker-compose.yml").exists()
            or (project_path / "docker-compose.yaml").exists()
        )

    def _parse_docker_compose_services(self, project_path: Path) -> list[str]:
        """Parse docker-compose.yml and extract service names.

        Args:
            project_path: Path to project directory

        Returns:
            List of service names, empty list if parsing fails
        """
        compose_files = ["docker-compose.yml", "docker-compose.yaml"]

        for filename in compose_files:
            compose_path = project_path / filename
            if not compose_path.exists():
                continue

            try:
                with open(compose_path, "r") as f:
                    data = yaml.safe_load(f)

                if data and "services" in data:
                    return list(data["services"].keys())
            except (yaml.YAMLError, IOError, TypeError):
                # Gracefully handle corrupted YAML or read errors
                return []

        return []

    def _detect_language(self, project_path: Path) -> Optional[str]:
        """Detect primary programming language from marker files.

        Checks for language-specific files in priority order:
        1. package.json → nodejs
        2. requirements.txt or pyproject.toml → python
        3. go.mod → go
        4. Cargo.toml → rust
        5. pom.xml or build.gradle → java

        Args:
            project_path: Path to project directory

        Returns:
            Language name (lowercase) or None if not detected
        """
        # Node.js
        if (project_path / "package.json").exists():
            return "nodejs"

        # Python
        if (project_path / "requirements.txt").exists() or (
            project_path / "pyproject.toml"
        ).exists():
            return "python"

        # Go
        if (project_path / "go.mod").exists():
            return "go"

        # Rust
        if (project_path / "Cargo.toml").exists():
            return "rust"

        # Java
        if (project_path / "pom.xml").exists() or (
            project_path / "build.gradle"
        ).exists():
            return "java"

        return None

    def _detect_databases(
        self, project_path: Path, context: ProjectContext
    ) -> list[str]:
        """Detect database systems in use.

        Checks multiple sources:
        1. Docker Compose services (service names and images)
        2. .env file DATABASE_URL patterns
        3. Configuration files

        Args:
            project_path: Path to project directory
            context: Current project context (for docker_services)

        Returns:
            List of detected database types
        """
        databases = set()

        # Check Docker Compose services
        for service_name in context.docker_services:
            for db_type, patterns in self.DATABASE_PATTERNS.items():
                if any(
                    pattern in service_name.lower() for pattern in patterns
                ):
                    databases.add(db_type)

        # Check .env file for DATABASE_URL
        env_file = project_path / ".env"
        if env_file.exists():
            try:
                env_content = env_file.read_text()
                databases.update(self._extract_databases_from_env(env_content))
            except (IOError, UnicodeDecodeError):
                pass

        return sorted(list(databases))

    def _extract_databases_from_env(self, env_content: str) -> set[str]:
        """Extract database types from environment file content.

        Looks for DATABASE_URL patterns like:
        - postgresql://... → postgres
        - mysql://... → mysql
        - redis://... → redis

        Args:
            env_content: Content of .env file

        Returns:
            Set of detected database types
        """
        databases = set()

        # Look for DATABASE_URL patterns
        url_patterns = {
            "postgres": [r"postgresql://", r"postgres://"],
            "mysql": [r"mysql://"],
            "redis": [r"redis://"],
            "mongodb": [r"mongodb://", r"mongodb\+srv://"],
        }

        for db_type, patterns in url_patterns.items():
            for pattern in patterns:
                if re.search(pattern, env_content, re.IGNORECASE):
                    databases.add(db_type)
                    break

        return databases
