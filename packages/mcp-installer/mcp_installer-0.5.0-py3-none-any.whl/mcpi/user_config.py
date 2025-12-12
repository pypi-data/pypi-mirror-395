"""Configuration management for MCPI.

Handles reading and writing configuration files following XDG Base Directory Specification.
Configuration file location: $XDG_CONFIG_HOME/mcpi/config.toml (default: ~/.config/mcpi/config.toml)
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import tomllib  # Python 3.11+

    # For writing, we need toml library even in Python 3.11+
    import toml as toml_writer  # type: ignore
except ImportError:
    import toml as tomllib  # type: ignore
    import toml as toml_writer  # type: ignore


class MCPIConfig:
    """Configuration manager for MCPI.

    Handles loading and accessing configuration from XDG-compliant config file.

    Example config.toml:
        [defaults]
        scope = "user-global"
        client = "claude-code"
    """

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.

        Args:
            config_path: Optional custom config path. If None, uses XDG standard location.
        """
        self.config_path = config_path or self._get_default_config_path()
        self._config: Dict[str, Any] = {}
        self._load()

    @staticmethod
    def _get_default_config_path() -> Path:
        """Get default config file path following XDG Base Directory Specification.

        Returns:
            Path to config file: $XDG_CONFIG_HOME/mcpi/config.toml or ~/.config/mcpi/config.toml
        """
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_dir = Path(xdg_config_home)
        else:
            config_dir = Path.home() / ".config"

        return config_dir / "mcpi" / "config.toml"

    def _load(self) -> None:
        """Load configuration from file.

        If file doesn't exist, returns empty config (no error).
        """
        if not self.config_path.exists():
            self._config = {}
            return

        try:
            with open(self.config_path, "rb") as f:
                self._config = tomllib.load(f)
        except Exception as e:
            # Log warning but don't fail - gracefully degrade to no config
            import warnings

            warnings.warn(
                f"Failed to load config from {self.config_path}: {e}. Using defaults."
            )
            self._config = {}

    @property
    def default_scope(self) -> Optional[str]:
        """Get default scope from config.

        Returns:
            Default scope name or None if not configured
        """
        return self._config.get("defaults", {}).get("scope")

    @property
    def default_client(self) -> Optional[str]:
        """Get default client from config.

        Returns:
            Default client name or None if not configured
        """
        return self._config.get("defaults", {}).get("client")

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            section: Config section (e.g., "defaults")
            key: Config key within section
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        return self._config.get(section, {}).get(key, default)

    @property
    def is_loaded(self) -> bool:
        """Check if config file was successfully loaded.

        Returns:
            True if config file exists and was loaded
        """
        return bool(self._config)

    def set(self, section: str, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            section: Config section (e.g., "defaults")
            key: Config key within section
            value: Value to set
        """
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value

    def save(self) -> None:
        """Save configuration to file.

        Creates parent directories if they don't exist.
        """
        # Ensure parent directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Write TOML file
        with open(self.config_path, "w") as f:
            toml_writer.dump(self._config, f)

    def to_dict(self) -> Dict[str, Any]:
        """Get full config as dictionary.

        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()

    def __repr__(self) -> str:
        """String representation of config."""
        return f"MCPIConfig(path={self.config_path}, loaded={self.is_loaded})"


# Factory functions for dependency injection


def create_default_config() -> MCPIConfig:
    """Create config using default XDG-compliant path.

    Returns:
        MCPIConfig instance
    """
    return MCPIConfig()


def create_test_config(config_path: Path) -> MCPIConfig:
    """Create config for testing with custom path.

    Args:
        config_path: Custom path to config file

    Returns:
        MCPIConfig instance
    """
    return MCPIConfig(config_path=config_path)
