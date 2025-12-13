"""
Configuration management for RedenLab ML SDK.

Handles loading configuration from multiple sources:
1. Environment variables
2. Config file (~/.redenlab-ml/config.yaml)
3. Default values
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

from .exceptions import ConfigurationError


# Default configuration values
DEFAULT_CONFIG = {
    'base_url': None,  # Will be set when we have the production URL
    'model_name': 'intelligibility',
    'timeout': 3600,  # 1 hour in seconds
}

# Environment variable prefix
ENV_PREFIX = 'REDENLAB_ML_'


def get_config_path() -> Path:
    """
    Get the path to the user config file.

    Returns:
        Path to ~/.redenlab-ml/config.yaml
    """
    return Path.home() / '.redenlab-ml' / 'config.yaml'


def load_config_file(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config file (default: ~/.redenlab-ml/config.yaml)

    Returns:
        Dictionary of configuration values (empty dict if file doesn't exist)

    Raises:
        ConfigurationError: If config file exists but is malformed
    """
    if config_path is None:
        config_path = get_config_path()

    if not config_path.exists():
        return {}

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        if config is None:
            return {}

        if not isinstance(config, dict):
            raise ConfigurationError(
                f"Config file must contain a YAML dictionary, got {type(config)}"
            )

        return config

    except yaml.YAMLError as e:
        raise ConfigurationError(f"Failed to parse config file: {e}")
    except OSError as e:
        raise ConfigurationError(f"Failed to read config file: {e}")


def load_env_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables.

    Environment variables should be prefixed with REDENLAB_ML_
    For example: REDENLAB_ML_API_KEY, REDENLAB_ML_BASE_URL

    Returns:
        Dictionary of configuration values from environment
    """
    config = {}

    # Map environment variables to config keys
    env_mappings = {
        'API_KEY': 'api_key',
        'BASE_URL': 'base_url',
        'MODEL': 'model_name',
        'TIMEOUT': 'timeout',
    }

    for env_suffix, config_key in env_mappings.items():
        env_var = f"{ENV_PREFIX}{env_suffix}"
        value = os.environ.get(env_var)

        if value is not None:
            # Convert timeout to integer if present
            if config_key == 'timeout':
                try:
                    config[config_key] = int(value)
                except ValueError:
                    raise ConfigurationError(
                        f"Invalid timeout value in {env_var}: {value} (must be an integer)"
                    )
            else:
                config[config_key] = value

    return config


def get_merged_config(
    config_path: Optional[Path] = None,
    **overrides
) -> Dict[str, Any]:
    """
    Get merged configuration from all sources.

    Priority order (highest to lowest):
    1. Keyword arguments (overrides)
    2. Environment variables
    3. Config file
    4. Default values

    Args:
        config_path: Optional path to config file
        **overrides: Explicit configuration overrides

    Returns:
        Merged configuration dictionary

    Raises:
        ConfigurationError: If configuration is invalid
    """
    # Start with defaults
    config = DEFAULT_CONFIG.copy()

    # Layer in config file values
    file_config = load_config_file(config_path)
    config.update(file_config)

    # Layer in environment variables
    env_config = load_env_config()
    config.update(env_config)

    # Layer in explicit overrides (remove None values)
    for key, value in overrides.items():
        if value is not None:
            config[key] = value

    return config


def get_default_base_url() -> Optional[str]:
    """
    Get the default API base URL.

    Returns:
        Default API endpoint URL, or None if not configured

    Note:
        This should be updated with the actual production API Gateway URL
        once the backend is deployed.
    """
    # TODO: Update this with actual production URL after backend deployment
    # For now, can be overridden via environment variable or config file
    return os.environ.get(f"{ENV_PREFIX}BASE_URL")


def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration values.

    Args:
        config: Configuration dictionary to validate

    Raises:
        ConfigurationError: If configuration is invalid
    """
    # Validate timeout if present
    if 'timeout' in config:
        timeout = config['timeout']
        if not isinstance(timeout, int) or timeout <= 0:
            raise ConfigurationError(
                f"Invalid timeout value: {timeout} (must be a positive integer)"
            )

    # Validate base_url if present
    if 'base_url' in config and config['base_url'] is not None:
        base_url = config['base_url']
        if not isinstance(base_url, str):
            raise ConfigurationError(
                f"Invalid base_url: {base_url} (must be a string)"
            )
        if not base_url.startswith(('http://', 'https://')):
            raise ConfigurationError(
                f"Invalid base_url: {base_url} (must start with http:// or https://)"
            )

    # Validate model_name if present
    if 'model_name' in config:
        model_name = config['model_name']
        if not isinstance(model_name, str):
            raise ConfigurationError(
                f"Invalid model_name: {model_name} (must be a string)"
            )


def create_default_config_file(config_path: Optional[Path] = None) -> Path:
    """
    Create a default config file with example values.

    Args:
        config_path: Path where to create the config file (default: ~/.redenlab-ml/config.yaml)

    Returns:
        Path to the created config file

    Raises:
        ConfigurationError: If file cannot be created
    """
    if config_path is None:
        config_path = get_config_path()

    # Create directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Don't overwrite existing config
    if config_path.exists():
        raise ConfigurationError(f"Config file already exists: {config_path}")

    default_content = """# RedenLab ML SDK Configuration
#
# This file provides default configuration for the SDK.
# You can also set these values via environment variables (REDENLAB_ML_*)
# or pass them directly to the InferenceClient constructor.

# Your API key (required)
# Get this from the RedenLab dashboard
api_key: sk_live_your_api_key_here

# API base URL (optional)
# Leave commented to use the default production endpoint
# base_url: https://your-api-gateway-url.amazonaws.com/prod

# Default model name (optional)
# Options: intelligibility, speaker_diarisation_workflow, ataxia-naturalness, ataxia-intelligibility
model_name: intelligibility

# Default timeout in seconds (optional)
# Maximum time to wait for inference to complete
timeout: 3600
"""

    try:
        with open(config_path, 'w') as f:
            f.write(default_content)
        return config_path
    except OSError as e:
        raise ConfigurationError(f"Failed to create config file: {e}")
