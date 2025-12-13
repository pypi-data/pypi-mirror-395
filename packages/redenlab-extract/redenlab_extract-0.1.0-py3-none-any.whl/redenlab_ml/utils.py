"""
Utility functions for RedenLab ML SDK.

Provides validation, file handling, and other helper functions.
"""

import os
from pathlib import Path
from typing import Optional

from .exceptions import ValidationError


# Supported audio file extensions and their MIME types
SUPPORTED_AUDIO_FORMATS = {
    '.wav': 'audio/wav',
    '.wave': 'audio/wav',
    '.mp3': 'audio/mpeg',
    '.m4a': 'audio/mp4',
    '.flac': 'audio/flac',
    '.ogg': 'audio/ogg',
    '.opus': 'audio/opus',
}


def validate_file_path(file_path: str) -> Path:
    """
    Validate that a file path exists and is readable.

    Args:
        file_path: Path to the file to validate

    Returns:
        Path object for the validated file

    Raises:
        ValidationError: If file doesn't exist or is not readable
    """
    if not file_path:
        raise ValidationError("File path cannot be empty")

    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise ValidationError(f"File does not exist: {file_path}")

    if not path.is_file():
        raise ValidationError(f"Path is not a file: {file_path}")

    if not os.access(path, os.R_OK):
        raise ValidationError(f"File is not readable: {file_path}")

    return path


def get_content_type(file_path: str) -> str:
    """
    Determine the content type (MIME type) for a file based on its extension.

    Args:
        file_path: Path to the file

    Returns:
        Content type string (e.g., 'audio/wav')

    Raises:
        ValidationError: If file extension is not supported
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in SUPPORTED_AUDIO_FORMATS:
        supported = ', '.join(SUPPORTED_AUDIO_FORMATS.keys())
        raise ValidationError(
            f"Unsupported file format: {extension}. "
            f"Supported formats: {supported}"
        )

    return SUPPORTED_AUDIO_FORMATS[extension]


def validate_model_name(model_name: str) -> str:
    """
    Validate that the model name is valid.

    Args:
        model_name: Name of the model

    Returns:
        Validated model name

    Raises:
        ValidationError: If model name is invalid
    """
    if not model_name:
        raise ValidationError("Model name cannot be empty")

    if not isinstance(model_name, str):
        raise ValidationError(f"Model name must be a string, got {type(model_name)}")

    # Model names should be lowercase with hyphens or underscores
    valid_chars = set('abcdefghijklmnopqrstuvwxyz0123456789-_')
    if not all(c in valid_chars for c in model_name):
        raise ValidationError(
            f"Invalid model name: {model_name}. "
            "Model names must contain only lowercase letters, numbers, hyphens, and underscores."
        )

    return model_name


def validate_timeout(timeout: Optional[int]) -> int:
    """
    Validate and normalize timeout value.

    Args:
        timeout: Timeout in seconds (None for default)

    Returns:
        Validated timeout in seconds

    Raises:
        ValidationError: If timeout is invalid
    """
    if timeout is None:
        return 3600  # Default: 1 hour

    if not isinstance(timeout, int):
        raise ValidationError(f"Timeout must be an integer, got {type(timeout)}")

    if timeout <= 0:
        raise ValidationError(f"Timeout must be positive, got {timeout}")

    if timeout > 86400:  # 24 hours
        raise ValidationError(
            f"Timeout cannot exceed 24 hours (86400 seconds), got {timeout}"
        )

    return timeout


def validate_api_key_format(api_key: str) -> None:
    """
    Validate API key format.

    Args:
        api_key: API key to validate

    Raises:
        ValidationError: If API key format is invalid
    """
    if not api_key:
        raise ValidationError("API key cannot be empty")

    if not isinstance(api_key, str):
        raise ValidationError(f"API key must be a string, got {type(api_key)}")

    # API keys should start with 'sk_' prefix (common convention)
    # and have reasonable length
    if len(api_key) < 10:
        raise ValidationError(
            f"API key is too short (minimum 10 characters), got {len(api_key)} characters"
        )

    if len(api_key) > 500:
        raise ValidationError(
            f"API key is too long (maximum 500 characters), got {len(api_key)} characters"
        )

    # Check for common mistakes
    if api_key.startswith(' ') or api_key.endswith(' '):
        raise ValidationError("API key contains leading or trailing whitespace")


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes

    Raises:
        ValidationError: If file cannot be accessed
    """
    try:
        path = Path(file_path)
        return path.stat().st_size
    except OSError as e:
        raise ValidationError(f"Cannot get file size: {e}")
