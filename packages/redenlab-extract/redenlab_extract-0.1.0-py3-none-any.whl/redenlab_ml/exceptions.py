"""
Custom exceptions for RedenLab ML SDK.

All exceptions inherit from RedenLabMLError for easy catching.
"""


class RedenLabMLError(Exception):
    """
    Base exception for all RedenLab ML SDK errors.

    All custom exceptions inherit from this class, allowing users to catch
    all SDK-specific errors with a single except clause.
    """
    pass


class AuthenticationError(RedenLabMLError):
    """
    Raised when authentication fails.

    This can occur when:
    - API key is missing
    - API key format is invalid
    - API key is rejected by the server (401/403 responses)
    """
    pass


class InferenceError(RedenLabMLError):
    """
    Raised when an inference job fails.

    This indicates the ML model inference failed, either during:
    - Job submission
    - Processing (model execution)
    - Result retrieval

    The error message will contain details about the failure.
    """
    pass


class TimeoutError(RedenLabMLError):
    """
    Raised when an operation times out.

    This can occur when:
    - Inference job exceeds the configured timeout
    - Polling for results takes longer than expected
    - Network request times out
    """
    pass


class APIError(RedenLabMLError):
    """
    Raised when an API request fails.

    This is a general error for API communication issues, including:
    - Network errors
    - Server errors (5xx responses)
    - Malformed responses
    - Rate limiting

    Check the error message for specific details.
    """
    pass


class UploadError(RedenLabMLError):
    """
    Raised when file upload to S3 fails.

    This can occur when:
    - File cannot be read
    - Upload to presigned URL fails
    - Network issues during upload
    """
    pass


class ValidationError(RedenLabMLError):
    """
    Raised when input validation fails.

    This can occur when:
    - File path doesn't exist
    - File type is not supported
    - Invalid configuration values
    - Missing required parameters
    """
    pass


class ConfigurationError(RedenLabMLError):
    """
    Raised when configuration is invalid or missing.

    This can occur when:
    - Config file is malformed
    - Required configuration is missing
    - Invalid configuration values
    """
    pass
