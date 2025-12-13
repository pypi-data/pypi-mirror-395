"""
Status polling functionality for RedenLab ML SDK.

Handles polling inference job status with exponential backoff
until the job reaches a terminal state (completed or failed).
"""

import time
from typing import Dict, Any, Callable, Optional

from .exceptions import TimeoutError as SDKTimeoutError, InferenceError


# Job status constants
STATUS_UPLOAD_PENDING = 'upload_pending'
STATUS_PROCESSING = 'processing'
STATUS_COMPLETED = 'completed'
STATUS_FAILED = 'failed'

# Terminal states (job is done)
TERMINAL_STATES = {STATUS_COMPLETED, STATUS_FAILED}


def poll_until_complete(
    get_status_func: Callable[[], Dict[str, Any]],
    job_id: str,
    timeout: int = 3600,
    initial_interval: int = 5,
    max_interval: int = 60,
    backoff_multiplier: float = 2.0,
) -> Dict[str, Any]:
    """
    Poll job status until it reaches a terminal state.

    Uses exponential backoff to reduce API calls:
    - Starts at initial_interval (default 5s)
    - Doubles after each attempt (configurable via backoff_multiplier)
    - Caps at max_interval (default 60s)

    Example progression with defaults: 5s, 10s, 20s, 40s, 60s, 60s, ...

    Args:
        get_status_func: Function that returns current job status (no arguments)
        job_id: Job ID being polled
        timeout: Maximum time to wait in seconds (default 1 hour)
        initial_interval: Starting poll interval in seconds
        max_interval: Maximum poll interval in seconds
        backoff_multiplier: Multiplier for exponential backoff

    Returns:
        Final job status dictionary with result or error

    Raises:
        TimeoutError: If job doesn't complete within timeout
        InferenceError: If job fails during processing

    Example:
        >>> status = poll_until_complete(
        ...     lambda: api.get_job_status(base_url, api_key, job_id, model),
        ...     job_id='123',
        ...     timeout=3600
        ... )
        >>> print(status['result'])
    """
    start_time = time.time()
    current_interval = initial_interval
    attempt = 0

    while True:
        attempt += 1
        elapsed = time.time() - start_time

        # Check timeout
        if elapsed >= timeout:
            raise SDKTimeoutError(
                f"Job {job_id} did not complete within {timeout} seconds "
                f"({attempt} status checks). "
                f"The job may still be processing on the server. "
                f"You can check its status later using get_status('{job_id}')."
            )

        # Get current status
        try:
            status_data = get_status_func()
        except Exception as e:
            # If we can't get status, wait and retry
            # (API errors are already converted to custom exceptions)
            raise

        current_status = status_data.get('status', 'unknown')

        # Check if job is complete
        if current_status == STATUS_COMPLETED:
            return status_data

        # Check if job failed
        if current_status == STATUS_FAILED:
            error_message = status_data.get('error', 'Unknown error')
            raise InferenceError(
                f"Inference job {job_id} failed: {error_message}"
            )

        # Job is still processing or waiting - continue polling
        # Calculate time remaining
        time_remaining = timeout - elapsed

        # Determine next wait interval
        wait_time = min(current_interval, time_remaining, max_interval)

        if wait_time > 0:
            time.sleep(wait_time)

        # Update interval for next iteration (exponential backoff)
        current_interval = min(current_interval * backoff_multiplier, max_interval)


def poll_with_callback(
    get_status_func: Callable[[], Dict[str, Any]],
    job_id: str,
    progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    timeout: int = 3600,
    initial_interval: int = 5,
    max_interval: int = 60,
    backoff_multiplier: float = 2.0,
) -> Dict[str, Any]:
    """
    Poll job status with progress callback.

    Similar to poll_until_complete but calls a callback function
    after each status check, allowing for custom progress reporting.

    Args:
        get_status_func: Function that returns current job status
        job_id: Job ID being polled
        progress_callback: Optional function to call with status data after each check
        timeout: Maximum time to wait in seconds
        initial_interval: Starting poll interval in seconds
        max_interval: Maximum poll interval in seconds
        backoff_multiplier: Multiplier for exponential backoff

    Returns:
        Final job status dictionary

    Raises:
        TimeoutError: If job doesn't complete within timeout
        InferenceError: If job fails during processing

    Example:
        >>> def on_progress(status_data):
        ...     print(f"Status: {status_data['status']}")
        >>> status = poll_with_callback(
        ...     lambda: api.get_job_status(base_url, api_key, job_id, model),
        ...     job_id='123',
        ...     progress_callback=on_progress
        ... )
    """
    start_time = time.time()
    current_interval = initial_interval
    attempt = 0

    while True:
        attempt += 1
        elapsed = time.time() - start_time

        # Check timeout
        if elapsed >= timeout:
            raise SDKTimeoutError(
                f"Job {job_id} did not complete within {timeout} seconds "
                f"({attempt} status checks)."
            )

        # Get current status
        status_data = get_status_func()
        current_status = status_data.get('status', 'unknown')

        # Call progress callback if provided
        if progress_callback:
            try:
                progress_callback(status_data)
            except Exception:
                # Don't let callback errors break the polling
                pass

        # Check terminal states
        if current_status == STATUS_COMPLETED:
            return status_data

        if current_status == STATUS_FAILED:
            error_message = status_data.get('error', 'Unknown error')
            raise InferenceError(f"Inference job {job_id} failed: {error_message}")

        # Continue polling
        time_remaining = timeout - elapsed
        wait_time = min(current_interval, time_remaining, max_interval)

        if wait_time > 0:
            time.sleep(wait_time)

        current_interval = min(current_interval * backoff_multiplier, max_interval)


def calculate_next_interval(
    current_interval: int,
    max_interval: int,
    multiplier: float = 2.0,
) -> int:
    """
    Calculate the next polling interval using exponential backoff.

    Args:
        current_interval: Current interval in seconds
        max_interval: Maximum allowed interval
        multiplier: Backoff multiplier (default 2.0 for doubling)

    Returns:
        Next interval in seconds (capped at max_interval)

    Example:
        >>> calculate_next_interval(5, 60, 2.0)
        10
        >>> calculate_next_interval(40, 60, 2.0)
        60
    """
    next_interval = int(current_interval * multiplier)
    return min(next_interval, max_interval)
