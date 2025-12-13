"""Configuration system for VizForge."""

import os
from typing import Optional, Dict, Any
import json


class Config:
    """
    Global configuration for VizForge.

    Manage default settings, themes, and preferences.
    """

    _instance = None
    _config = {
        # Display settings
        'default_theme': 'default',
        'auto_show': True,
        'figure_width': None,
        'figure_height': None,

        # Export settings
        'export_width': 1200,
        'export_height': 800,
        'export_scale': 1.0,
        'default_export_format': 'html',

        # Performance settings
        'max_points': 100000,
        'enable_webgl': True,
        'enable_caching': True,

        # Data settings
        'auto_clean_data': False,
        'fill_na_method': None,
        'drop_duplicates': False,

        # Dashboard settings
        'dashboard_rows': 2,
        'dashboard_cols': 2,
        'dashboard_height': 800,

        # Advanced settings
        'verbose': False,
        'strict_mode': False,
    }

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration."""
        self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_prefix = 'VIZFORGE_'

        for key in self._config.keys():
            env_key = f"{env_prefix}{key.upper()}"
            if env_key in os.environ:
                value = os.environ[env_key]

                # Type conversion
                if isinstance(self._config[key], bool):
                    value = value.lower() in ('true', '1', 'yes')
                elif isinstance(self._config[key], int):
                    value = int(value)
                elif isinstance(self._config[key], float):
                    value = float(value)

                self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value

    def update(self, **kwargs):
        """
        Update multiple configuration values.

        Args:
            **kwargs: Key-value pairs to update
        """
        self._config.update(kwargs)

    def reset(self):
        """Reset configuration to defaults."""
        self._config = self.__class__._config.copy()

    def load_from_file(self, filepath: str):
        """
        Load configuration from JSON file.

        Args:
            filepath: Path to JSON config file
        """
        with open(filepath, 'r') as f:
            config = json.load(f)
            self._config.update(config)

    def save_to_file(self, filepath: str):
        """
        Save configuration to JSON file.

        Args:
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            json.dump(self._config, f, indent=2)

    def __repr__(self) -> str:
        """String representation."""
        return f"VizForge Configuration:\n" + "\n".join(
            f"  {k}: {v}" for k, v in self._config.items()
        )


# Global configuration instance
_config = Config()


def get_config() -> Config:
    """
    Get global configuration instance.

    Returns:
        Config instance

    Examples:
        >>> import vizforge as vz
        >>> config = vz.get_config()
        >>> config.set('default_theme', 'dark')
    """
    return _config


def set_config(**kwargs):
    """
    Update global configuration.

    Args:
        **kwargs: Configuration key-value pairs

    Examples:
        >>> import vizforge as vz
        >>> vz.set_config(default_theme='dark', auto_show=False)
    """
    _config.update(**kwargs)


def reset_config():
    """
    Reset configuration to defaults.

    Examples:
        >>> import vizforge as vz
        >>> vz.reset_config()
    """
    _config.reset()
