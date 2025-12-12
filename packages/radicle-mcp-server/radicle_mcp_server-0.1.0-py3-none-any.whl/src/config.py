"""Configuration for Radicle MCP Server."""

from __future__ import annotations


from typing import Any
from pathlib import Path
import copy
import yaml


DEFAULT_CONFIG = {
    "server": {"host": "localhost", "port": 8000, "transport": "stdio"},
    "radicle": {"timeout": 30, "definitions_dir": None},
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    },
}


class Config:
    """Configuration manager for Radicle MCP Server."""

    config_file: Path
    _config: dict[str, Any]  # pyright: ignore[reportExplicitAny]  # YAML config data

    def __init__(self, config_file: Path | None = None):
        """Initialize configuration.

        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file or Path.home() / ".radicle-mcp-server.yaml"
        self._config = copy.deepcopy(DEFAULT_CONFIG)
        self.load()

    def load(self):
        """Load configuration from YAML file, merging with defaults.

        Safely loads YAML config from self.config_file, merging found settings
        with DEFAULT_CONFIG using dict update. Prints warnings for file errors
        but continues with defaults. Called automatically during __init__.

        No exceptions raised - errors logged as warnings and defaults used.
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    file_config = yaml.safe_load(f)  # YAML parsing

                self._merge_config(self._config, file_config)

            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")

    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                yaml.dump(self._config, f, default_flow_style=False)

        except Exception as e:
            print(f"Error saving config file {self.config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:  # pyright: ignore[reportExplicitAny]  # Config value access
        """Get configuration value.

        Args:
            key: Configuration key (supports dot notation like 'server.host')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:  # pyright: ignore[reportExplicitAny]  # Config value setting
        """Set configuration value.

        Args:
            key: Configuration key (supports dot notation like 'server.host')
            value: Value to set
        """
        keys = key.split(".")
        config: dict[str, Any] = self._config  # pyright: ignore[reportExplicitAny]  # Config data

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            next_config = config[k]
            if not isinstance(next_config, dict):
                config[k] = {}
                next_config = config[k]
            config = next_config

        config[keys[-1]] = value

    def _merge_config(
        self,
        base: dict[str, Any],  # pyright: ignore[reportExplicitAny]  # Config data
        override: dict[str, Any],  # pyright: ignore[reportExplicitAny]  # YAML data
    ):
        """Recursively merge configuration dictionaries.

        Args:
            base: Base configuration dictionary
            override: Override dictionary
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)  # Recursive config merge
            else:
                base[key] = value
