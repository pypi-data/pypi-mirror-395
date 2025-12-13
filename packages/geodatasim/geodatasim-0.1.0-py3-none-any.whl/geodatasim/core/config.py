"""Configuration management for GeoDataSim."""

import os
from typing import Optional, Dict, Any
import json
from pathlib import Path


class Config:
    """
    Global configuration for GeoDataSim.

    Manages API keys, cache settings, and data sources.
    """

    _instance = None
    _config = {
        # API Keys (all optional)
        'api_keys': {
            'openweather': None,
            'worldbank': None,  # Not needed, but can be set for rate limit increase
        },

        # Cache settings
        'cache_enabled': True,
        'cache_dir': str(Path.home() / '.geodatasim' / 'cache'),
        'cache_ttl_days': 90,  # Cache API responses for 90 days

        # Data sources
        'worldbank_api_url': 'https://api.worldbank.org/v2',
        'openweather_api_url': 'https://api.openweathermap.org/data/2.5',
        'openmeteo_api_url': 'https://api.open-meteo.com/v1',

        # Performance
        'max_retries': 3,
        'timeout_seconds': 10,
        'enable_parallel_requests': True,

        # Similarity
        'similarity_weights': {
            'population': 0.2,
            'gdp_per_capita': 0.3,
            'climate': 0.2,
            'geographic': 0.15,
            'development': 0.15,
        },

        # Display
        'verbose': False,
        'show_warnings': True,
    }

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration."""
        self._load_from_env()
        self._ensure_cache_dir()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_prefix = 'GEODATASIM_'

        # API keys
        for api_name in self._config['api_keys'].keys():
            env_key = f"{env_prefix}{api_name.upper()}_API_KEY"
            if env_key in os.environ:
                self._config['api_keys'][api_name] = os.environ[env_key]

        # Other settings
        if f"{env_prefix}CACHE_ENABLED" in os.environ:
            self._config['cache_enabled'] = os.environ[f"{env_prefix}CACHE_ENABLED"].lower() in ('true', '1', 'yes')

        if f"{env_prefix}VERBOSE" in os.environ:
            self._config['verbose'] = os.environ[f"{env_prefix}VERBOSE"].lower() in ('true', '1', 'yes')

    def _ensure_cache_dir(self):
        """Ensure cache directory exists."""
        if self._config['cache_enabled']:
            cache_dir = Path(self._config['cache_dir'])
            cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key (can be nested like 'api_keys.openweather')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set configuration value.

        Args:
            key: Configuration key (can be nested)
            value: Configuration value
        """
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def set_api_key(self, api_name: str, api_key: str):
        """
        Set API key for a specific service.

        Args:
            api_name: API service name ('openweather', 'worldbank')
            api_key: API key value
        """
        if api_name in self._config['api_keys']:
            self._config['api_keys'][api_name] = api_key
        else:
            raise ValueError(f"Unknown API: {api_name}. Valid options: {list(self._config['api_keys'].keys())}")

    def get_api_key(self, api_name: str) -> Optional[str]:
        """
        Get API key for a specific service.

        Args:
            api_name: API service name

        Returns:
            API key or None if not set
        """
        return self._config['api_keys'].get(api_name)

    def load_from_file(self, filepath: str):
        """
        Load configuration from JSON file.

        Args:
            filepath: Path to JSON config file
        """
        with open(filepath, 'r') as f:
            config = json.load(f)
            self._deep_update(self._config, config)

    def save_to_file(self, filepath: str):
        """
        Save configuration to JSON file.

        Args:
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            json.dump(self._config, f, indent=2)

    def _deep_update(self, base: dict, update: dict):
        """Deep update dictionary."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value

    def reset(self):
        """Reset configuration to defaults."""
        self._config = self.__class__._config.copy()

    def __repr__(self) -> str:
        """String representation."""
        config_display = {k: v for k, v in self._config.items() if k != 'api_keys'}
        api_keys_status = {k: '***' if v else None for k, v in self._config['api_keys'].items()}
        config_display['api_keys'] = api_keys_status

        return f"GeoDataSim Configuration:\n" + "\n".join(
            f"  {k}: {v}" for k, v in config_display.items()
        )


# Global configuration instance
_config = Config()


def get_config() -> Config:
    """
    Get global configuration instance.

    Returns:
        Config instance

    Examples:
        >>> from geodatasim import get_config
        >>> config = get_config()
        >>> config.set_api_key('openweather', 'your_key')
    """
    return _config


def set_config(**kwargs):
    """
    Update global configuration.

    Args:
        **kwargs: Configuration key-value pairs

    Examples:
        >>> from geodatasim import set_config
        >>> set_config(verbose=True, cache_enabled=False)
    """
    for key, value in kwargs.items():
        _config.set(key, value)
