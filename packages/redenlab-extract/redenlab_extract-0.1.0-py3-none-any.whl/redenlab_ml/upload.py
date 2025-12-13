"""
File upload functionality for RedenLab ML SDK.

Handles uploading files to S3 via presigned URLs.
"""

from pathlib import Path
from typing import Optional, Callable
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from .exceptions import UploadError
from .utils import get_file_size, format_file_size


# Default timeout for upload requests (in seconds)
# Larger than API requests since we're uploading potentially large files
DEFAULT_UPLOAD_TIMEOUT = 300  # 5 minutes


def upload_to_presigned_url(
    file_path: str,
    presigned_url: str,
    content_type: str,
    timeout: int = DEFAULT_UPLOAD_TIMEOUT,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> None:
    """
    Upload a file to S3 using a presigned URL.

    Args:
        file_path: Path to the file to upload
        presigned_url: Presigned S3 URL from the API
        content_type: MIME type of the file (e.g., 'audio/wav')
        timeout: Upload timeout in seconds
        progress_callback: Optional callback function(bytes_uploaded, total_bytes)
                          called during upload to report progress

    Raises:
        UploadError: If upload fails for any reason

    Example:
        >>> def progress(uploaded, total):
        ...     percent = (uploaded / total) * 100
        ...     print(f"Upload progress: {percent:.1f}%")
        >>> upload_to_presigned_url(
        ...     'audio.wav',
        ...     'https://s3.amazonaws.com/...',
        ...     'audio/wav',
        ...     progress_callback=progress
        ... )
    """
    path = Path(file_path)

    # Validate file exists
    if not path.exists():
        raise UploadError(f"File does not exist: {file_path}")

    if not path.is_file():
        raise UploadError(f"Path is not a file: {file_path}")

    # Get file size for progress tracking
    try:
        file_size = get_file_size(file_path)
    except Exception as e:
        raise UploadError(f"Cannot read file: {e}")

    # Create progress tracking wrapper if callback provided
    if progress_callback:
        data = _ProgressTrackingFile(file_path, progress_callback, file_size)
    else:
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except OSError as e:
            raise UploadError(f"Cannot read file: {e}")

    # Prepare headers
    headers = {
        'Content-Type': content_type,
    }

    # Upload file
    try:
        response = requests.put(
            presigned_url,
            data=data,
            headers=headers,
            timeout=timeout,
        )

        # Check for errors
        if not response.ok:
            error_message = response.text or f"HTTP {response.status_code}"
            raise UploadError(
                f"Upload failed (HTTP {response.status_code}): {error_message}"
            )

    except Timeout:
        raise UploadError(
            f"Upload timed out after {timeout} seconds. "
            f"File size: {format_file_size(file_size)}. "
            "Try increasing the timeout or checking your network connection."
        )
    except ConnectionError as e:
        raise UploadError(f"Connection error during upload: {e}")
    except RequestException as e:
        raise UploadError(f"Upload failed: {e}")
    except Exception as e:
        raise UploadError(f"Unexpected error during upload: {e}")
    finally:
        # Close the file if we opened it for progress tracking
        if progress_callback and hasattr(data, 'close'):
            data.close()


class _ProgressTrackingFile:
    """
    File-like object that reports upload progress via callback.

    This wrapper reads the file in chunks and calls the progress callback
    after each chunk is read.
    """

    def __init__(
        self,
        file_path: str,
        callback: Callable[[int, int], None],
        total_size: int,
        chunk_size: int = 8192,
    ):
        """
        Initialize progress tracking file wrapper.

        Args:
            file_path: Path to the file
            callback: Function to call with (bytes_read, total_bytes)
            total_size: Total file size in bytes
            chunk_size: Size of chunks to read (default 8KB)
        """
        self.file_path = file_path
        self.callback = callback
        self.total_size = total_size
        self.chunk_size = chunk_size
        self.bytes_read = 0
        self._file = None

    def __enter__(self):
        """Open the file when entering context."""
        self._file = open(self.file_path, 'rb')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the file when exiting context."""
        if self._file:
            self._file.close()

    def read(self, size: int = -1) -> bytes:
        """
        Read from the file and report progress.

        Args:
            size: Number of bytes to read (-1 for all)

        Returns:
            Bytes read from file
        """
        if self._file is None:
            self._file = open(self.file_path, 'rb')

        # Determine how much to read
        if size == -1:
            chunk_size = self.chunk_size
        else:
            chunk_size = min(size, self.chunk_size)

        # Read chunk
        chunk = self._file.read(chunk_size)

        if chunk:
            # Update progress
            self.bytes_read += len(chunk)

            # Call progress callback
            try:
                self.callback(self.bytes_read, self.total_size)
            except Exception:
                # Don't let callback errors break the upload
                pass

        return chunk

    def __iter__(self):
        """Make this object iterable for requests library."""
        return self

    def __next__(self):
        """Read next chunk for iteration."""
        chunk = self.read(self.chunk_size)
        if not chunk:
            raise StopIteration
        return chunk

    def close(self):
        """Close the underlying file."""
        if self._file:
            self._file.close()
            self._file = None
