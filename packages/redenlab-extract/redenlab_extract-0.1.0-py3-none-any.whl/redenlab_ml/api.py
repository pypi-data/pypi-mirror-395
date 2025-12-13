"""
API communication layer for RedenLab ML SDK.

Handles all HTTP requests to the backend API with retry logic,
error handling, and response parsing.
"""

import json
from typing import Dict, Any, Optional, Tuple
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from .auth import get_auth_headers
from .exceptions import APIError, AuthenticationError, InferenceError


# Default timeout for HTTP requests (in seconds)
DEFAULT_REQUEST_TIMEOUT = 30


def _handle_error_response(response: requests.Response) -> None:
    """
    Handle error responses from the API.

    Args:
        response: HTTP response object

    Raises:
        AuthenticationError: For 401/403 responses
        InferenceError: For 400/422 responses (validation errors)
        APIError: For other error responses
    """
    try:
        error_data = response.json()
        error_message = error_data.get('error', response.text)
    except (json.JSONDecodeError, ValueError):
        error_message = response.text or f"HTTP {response.status_code}"

    # Authentication errors
    if response.status_code in (401, 403):
        raise AuthenticationError(
            f"Authentication failed: {error_message}. "
            "Please check your API key."
        )

    # Validation errors
    if response.status_code in (400, 422):
        raise InferenceError(f"Invalid request: {error_message}")

    # Not found
    if response.status_code == 404:
        raise APIError(f"Resource not found: {error_message}")

    # Rate limiting
    if response.status_code == 429:
        raise APIError(
            f"Rate limit exceeded: {error_message}. "
            "Please wait before making more requests."
        )

    # Server errors
    if response.status_code >= 500:
        raise APIError(
            f"Server error (HTTP {response.status_code}): {error_message}. "
            "Please try again later."
        )

    # Other errors
    raise APIError(f"API error (HTTP {response.status_code}): {error_message}")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ConnectionError, Timeout)),
    reraise=True,
)
def _make_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    json_data: Optional[Dict[str, Any]] = None,
    timeout: int = DEFAULT_REQUEST_TIMEOUT,
) -> requests.Response:
    """
    Make an HTTP request with retry logic.

    Retries on network errors (connection issues, timeouts) up to 3 times
    with exponential backoff (2s, 4s, 8s).

    Args:
        method: HTTP method (GET, POST, etc.)
        url: Full URL to request
        headers: HTTP headers
        json_data: Optional JSON body for POST requests
        timeout: Request timeout in seconds

    Returns:
        Response object

    Raises:
        APIError: For network or request errors
        AuthenticationError: For authentication failures
        InferenceError: For validation errors
    """
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json_data,
            timeout=timeout,
        )

        # Check for HTTP errors
        if not response.ok:
            _handle_error_response(response)

        return response

    except Timeout as e:
        raise APIError(f"Request timed out after {timeout} seconds: {e}")
    except ConnectionError as e:
        raise APIError(f"Connection error: {e}")
    except RequestException as e:
        raise APIError(f"Request failed: {e}")


def request_presigned_url(
    base_url: str,
    api_key: str,
    filename: str,
    content_type: str = 'audio/wav',
) -> Tuple[str, str, str, int]:
    """
    Request a presigned S3 URL for file upload.

    Calls: POST /upload-url

    Args:
        base_url: API base URL
        api_key: API key for authentication
        filename: Name of the file to upload
        content_type: MIME type of the file

    Returns:
        Tuple of (job_id, upload_url, file_key, expires_in)

    Raises:
        APIError: If the request fails
        AuthenticationError: If authentication fails
    """
    url = f"{base_url.rstrip('/')}/upload-url"
    headers = get_auth_headers(api_key)

    body = {
        'filename': filename,
        'content_type': content_type,
    }

    response = _make_request('POST', url, headers, json_data=body)

    try:
        data = response.json()
    except (json.JSONDecodeError, ValueError) as e:
        raise APIError(f"Invalid JSON response from /upload-url: {e}")

    # Validate response structure
    required_fields = ['job_id', 'upload_url', 'file_key', 'expires_in']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise APIError(
            f"Invalid response from /upload-url: missing fields {missing_fields}"
        )

    return (
        data['job_id'],
        data['upload_url'],
        data['file_key'],
        data['expires_in'],
    )


def submit_inference_job(
    base_url: str,
    api_key: str,
    job_id: str,
    file_key: str,
    model_name: str,
) -> Dict[str, Any]:
    """
    Submit an inference job to the backend.

    Calls: POST /{model_name}/predict

    Args:
        base_url: API base URL
        api_key: API key for authentication
        job_id: Job ID from presigned URL request
        file_key: S3 file key from presigned URL request
        model_name: Name of the model to use

    Returns:
        Response data with job_id, status, message

    Raises:
        APIError: If the request fails
        AuthenticationError: If authentication fails
        InferenceError: If job submission fails
    """
    url = f"{base_url.rstrip('/')}/{model_name}/predict"
    headers = get_auth_headers(api_key)

    body = {
        'job_id': job_id,
        'file_key': file_key,
    }

    response = _make_request('POST', url, headers, json_data=body)

    try:
        data = response.json()
    except (json.JSONDecodeError, ValueError) as e:
        raise APIError(f"Invalid JSON response from /{model_name}/predict: {e}")

    return data


def get_job_status(
    base_url: str,
    api_key: str,
    job_id: str,
    model_name: str,
) -> Dict[str, Any]:
    """
    Get the status of an inference job.

    Calls: GET /result/{job_id}?model={model_name}

    Args:
        base_url: API base URL
        api_key: API key for authentication
        job_id: Job ID to check
        model_name: Model name (used as query parameter)

    Returns:
        Job status data including:
        - job_id: Job identifier
        - status: Job status (upload_pending, processing, completed, failed)
        - result: Inference result (if completed)
        - error: Error message (if failed)
        - created_at: Job creation timestamp
        - completed_at: Job completion timestamp (if completed)

    Raises:
        APIError: If the request fails
        AuthenticationError: If authentication fails
    """
    url = f"{base_url.rstrip('/')}/result/{job_id}"
    headers = get_auth_headers(api_key)

    # Add model name as query parameter
    params = {'model': model_name}

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=DEFAULT_REQUEST_TIMEOUT,
        )

        if not response.ok:
            _handle_error_response(response)

        data = response.json()
        return data

    except Timeout as e:
        raise APIError(f"Request timed out: {e}")
    except ConnectionError as e:
        raise APIError(f"Connection error: {e}")
    except RequestException as e:
        raise APIError(f"Request failed: {e}")
    except (json.JSONDecodeError, ValueError) as e:
        raise APIError(f"Invalid JSON response from /result/{job_id}: {e}")
