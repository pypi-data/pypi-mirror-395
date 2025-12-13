"""
Authentication handling for RedenLab ML SDK.

Manages API key retrieval from multiple sources and generates
authentication headers for API requests.
"""

from typing import Optional, Dict

from .config import get_merged_config
from .utils import validate_api_key_format
from .exceptions import AuthenticationError


def get_api_key(
    api_key: Optional[str] = None,
    config_path: Optional[str] = None
) -> str:
    """
    Get API key from the highest priority available source.

    Priority order:
    1. api_key parameter (explicit override)
    2. REDENLAB_ML_API_KEY environment variable
    3. Config file (~/.redenlab-ml/config.yaml)

    Args:
        api_key: Explicit API key (highest priority)
        config_path: Optional path to config file

    Returns:
        API key string

    Raises:
        AuthenticationError: If no API key is found in any source
    """
    # If provided directly, use it
    if api_key is not None:
        return api_key

    # Otherwise, try to get from config (env vars or file)
    config = get_merged_config(config_path=config_path)

    if 'api_key' in config and config['api_key']:
        return config['api_key']

    # No API key found anywhere
    raise AuthenticationError(
        "No API key found. Please provide an API key via:\n"
        "1. InferenceClient(api_key='sk_live_...')\n"
        "2. Environment variable: REDENLAB_ML_API_KEY\n"
        "3. Config file: ~/.redenlab-ml/config.yaml"
    )


def validate_api_key(api_key: str) -> None:
    """
    Validate that the API key is properly formatted.

    Args:
        api_key: API key to validate

    Raises:
        AuthenticationError: If API key format is invalid
    """
    try:
        validate_api_key_format(api_key)
    except Exception as e:
        raise AuthenticationError(f"Invalid API key format: {e}")


def get_auth_headers(api_key: str) -> Dict[str, str]:
    """
    Generate authentication headers for API requests.

    Args:
        api_key: API key to use for authentication

    Returns:
        Dictionary of HTTP headers including authentication

    Note:
        The API Gateway expects the API key in the 'X-Api-Key' header.
    """
    return {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }


def mask_api_key(api_key: str) -> str:
    """
    Mask an API key for safe logging/display.

    Shows only the first 7 characters (e.g., 'sk_live') and last 4 characters,
    replacing the middle with asterisks.

    Args:
        api_key: API key to mask

    Returns:
        Masked API key string (e.g., 'sk_live***1234')

    Example:
        >>> mask_api_key('sk_live_1234567890abcdef')
        'sk_live***cdef'
    """
    if not api_key or len(api_key) < 12:
        return '***'

    # Show first 7 chars and last 4 chars
    return f"{api_key[:7]}***{api_key[-4:]}"
