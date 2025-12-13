"""
Main client for RedenLab ML SDK.

Provides the high-level InferenceClient class for running ML inference.
"""

import os
from typing import Optional, Dict, Any, Callable
from pathlib import Path

from . import api
from .auth import get_api_key, validate_api_key, mask_api_key
from .config import get_merged_config, get_default_base_url
from .upload import upload_to_presigned_url
from .polling import poll_until_complete, poll_with_callback
from .utils import (
    validate_file_path,
    get_content_type,
    validate_model_name,
    validate_timeout,
)
from .exceptions import ValidationError, ConfigurationError


class InferenceClient:
    """
    Client for RedenLab ML inference service.

    This is the main entry point for running ML inference on audio files.
    Handles authentication, file upload, job submission, and result retrieval.

    Example:
        >>> client = InferenceClient(api_key="sk_live_...")
        >>> result = client.predict(file_path="audio.wav")
        >>> print(result['result'])

    Args:
        api_key: API key for authentication (optional, can use env var or config file)
        base_url: API base URL (optional, defaults to production endpoint)
        model_name: Model to use for inference (default: 'intelligibility')
        timeout: Maximum time to wait for inference in seconds (default: 3600)
        config_path: Path to config file (optional)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: str = 'intelligibility',
        timeout: int = 3600,
        config_path: Optional[str] = None,
    ):
        """
        Initialize the inference client.

        Raises:
            AuthenticationError: If no API key is found
            ValidationError: If parameters are invalid
            ConfigurationError: If configuration is invalid
        """
        # Load configuration from all sources
        config = get_merged_config(
            config_path=config_path,
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            timeout=timeout,
        )

        # Get and validate API key
        self.api_key = get_api_key(api_key=api_key, config_path=config_path)
        validate_api_key(self.api_key)

        # Set base URL (use provided, or from config, or default)
        self.base_url = base_url or config.get('base_url') or get_default_base_url()
        if not self.base_url:
            raise ConfigurationError(
                "No API base URL configured. Please set via:\n"
                "1. InferenceClient(base_url='https://...')\n"
                "2. Environment variable: REDENLAB_ML_BASE_URL\n"
                "3. Config file: ~/.redenlab-ml/config.yaml"
            )

        # Validate and set model name
        self.model_name = validate_model_name(model_name or config.get('model_name', 'intelligibility'))

        # Validate and set timeout
        self.timeout = validate_timeout(timeout if timeout != 3600 else config.get('timeout', 3600))

    def predict(
        self,
        file_path: str,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run inference on an audio file.

        This method handles the complete inference workflow:
        1. Request presigned URL for upload
        2. Upload file to S3
        3. Submit inference job
        4. Poll for completion
        5. Return results

        Args:
            file_path: Path to the audio file to process
            progress_callback: Optional callback function that receives status updates
                             during polling. Called with status dict after each check.

        Returns:
            Dictionary containing inference results:
            - job_id: Job identifier
            - status: 'completed'
            - result: Inference result data (model-specific)
            - created_at: Job creation timestamp
            - completed_at: Job completion timestamp

        Raises:
            ValidationError: If file path is invalid or file type not supported
            AuthenticationError: If API key is invalid
            UploadError: If file upload fails
            InferenceError: If inference job fails
            TimeoutError: If inference doesn't complete within timeout
            APIError: If API communication fails

        Example:
            >>> def on_progress(status):
            ...     print(f"Status: {status['status']}")
            >>> result = client.predict(
            ...     file_path="audio.wav",
            ...     progress_callback=on_progress
            ... )
            >>> print(result['result'])
        """
        # Validate file path
        file_path_obj = validate_file_path(file_path)

        # Get content type from file extension
        content_type = get_content_type(file_path)

        # Get filename
        filename = file_path_obj.name

        # Step 1: Request presigned URL
        job_id, upload_url, file_key, expires_in = api.request_presigned_url(
            base_url=self.base_url,
            api_key=self.api_key,
            filename=filename,
            content_type=content_type,
        )

        # Step 2: Upload file to S3
        upload_to_presigned_url(
            file_path=str(file_path_obj),
            presigned_url=upload_url,
            content_type=content_type,
        )

        # Step 3: Submit inference job
        api.submit_inference_job(
            base_url=self.base_url,
            api_key=self.api_key,
            job_id=job_id,
            file_key=file_key,
            model_name=self.model_name,
        )

        # Step 4: Poll for completion
        if progress_callback:
            result = poll_with_callback(
                get_status_func=lambda: self.get_status(job_id),
                job_id=job_id,
                progress_callback=progress_callback,
                timeout=self.timeout,
            )
        else:
            result = poll_until_complete(
                get_status_func=lambda: self.get_status(job_id),
                job_id=job_id,
                timeout=self.timeout,
            )

        return result

    def get_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the current status of an inference job.

        Args:
            job_id: Job ID to check

        Returns:
            Dictionary containing job status:
            - job_id: Job identifier
            - status: Current status (upload_pending, processing, completed, failed)
            - result: Inference result (if completed)
            - error: Error message (if failed)
            - created_at: Job creation timestamp
            - completed_at: Job completion timestamp (if completed)

        Raises:
            APIError: If status check fails
            AuthenticationError: If API key is invalid

        Example:
            >>> status = client.get_status(job_id="abc-123")
            >>> print(status['status'])
            'processing'
        """
        return api.get_job_status(
            base_url=self.base_url,
            api_key=self.api_key,
            job_id=job_id,
            model_name=self.model_name,
        )

    def __repr__(self) -> str:
        """Return string representation of the client."""
        return (
            f"InferenceClient("
            f"api_key='{mask_api_key(self.api_key)}', "
            f"base_url='{self.base_url}', "
            f"model_name='{self.model_name}', "
            f"timeout={self.timeout}"
            f")"
        )
