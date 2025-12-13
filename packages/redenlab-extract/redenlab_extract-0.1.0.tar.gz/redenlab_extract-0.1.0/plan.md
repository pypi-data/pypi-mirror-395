API Specification (Backend Analysis)

  I've analyzed the backend and identified the following API endpoints:

  1. POST /upload-url (Generate Presigned URL)

  - Authentication: API key required
  - Request Body:
  {
    "filename": "audio.wav",
    "content_type": "audio/wav"  // optional
  }
  - Response:
  {
    "job_id": "uuid",
    "upload_url": "https://...",
    "file_key": "uploads/uuid/filename.wav",
    "expires_in": 900
  }

  2. POST /{model_name}/predict (Submit Inference Job)

  - Authentication: API key required
  - Path: /intelligibility/predict, /speaker_diarisation_workflow/predict, etc.
  - Request Body:
  {
    "job_id": "uuid",
    "file_key": "uploads/uuid/filename.wav"
  }
  - Response:
  {
    "job_id": "uuid",
    "status": "processing",
    "message": "Inference job submitted successfully",
    "output_location": "s3://..."
  }

  3. GET /result/{job_id} (Get Results)

  - Authentication: API key required
  - Query Parameters: ?model=intelligibility (optional)
  - Response (intelligibility model):
  {
    "job_id": "uuid",
    "status": "completed|processing|failed|upload_pending",
    "result": {...},  // if completed
    "created_at": "...",
    "completed_at": "..."
  }

⏺ SDK Architecture Design

  High-Level Flow

  User Code → Client → [Auth] → API Module → Backend API
                  ↓
              Polling Module ← Job Status
                  ↓
              Result Handler

  Module Breakdown

  1. client.py - Main Entry Point

  Responsibilities:
  - InferenceClient class with predict() method
  - Orchestrates the entire workflow
  - High-level API for users

  Methods:
  - __init__(api_key, base_url, model_name)
  - predict(file_path=None, s3_uri=None) - Main prediction method
  - get_job_status(job_id) - Check status
  - get_result(job_id) - Get completed result
  - _upload_file(local_path, presigned_url) - Internal upload helper

  2. auth.py - Authentication

  Responsibilities:
  - API key management and validation
  - Header generation for requests

  Functions:
  - get_api_key() - Priority: param > env var > config file
  - validate_api_key(key) - Check format
  - get_auth_headers(api_key) - Return headers dict

  3. api.py - HTTP Communication

  Responsibilities:
  - All HTTP requests to backend
  - Request/response handling
  - Retry logic

  Functions:
  - request_presigned_url(base_url, auth_headers, filename, content_type)
  - submit_inference_job(base_url, auth_headers, job_id, file_key, model_name)
  - get_job_status(base_url, auth_headers, job_id, model_name)
  - _make_request(method, url, headers, body, retry_config) - Base request handler

  4. polling.py - Status Polling

  Responsibilities:
  - Poll job status until complete/failed/timeout
  - Exponential backoff

  Functions:
  - poll_until_complete(client, job_id, timeout, initial_interval, max_interval)
  - calculate_next_interval(current_interval, max_interval) - Exponential backoff

  5. upload.py - File Upload Handler

  Responsibilities:
  - Upload files to S3 via presigned URLs
  - Progress tracking (optional)

  Functions:
  - upload_to_presigned_url(file_path, presigned_url, content_type)
  - _get_file_size(file_path)

  6. config.py - Configuration Management

  Responsibilities:
  - Load config from file
  - Default values

  Functions:
  - load_config(config_path) - Read YAML config
  - get_default_base_url() - Return default API endpoint
  - get_config_path() - Resolve ~/.redenlab-ml/config.yaml

  7. exceptions.py - Custom Exceptions

  class RedenLabMLError(Exception): pass
  class AuthenticationError(RedenLabMLError): pass
  class InferenceError(RedenLabMLError): pass
  class TimeoutError(RedenLabMLError): pass
  class APIError(RedenLabMLError): pass
  class UploadError(RedenLabMLError): pass

⏺ Project Structure

  redenlab-ml-sdk/
  ├── src/
  │   └── redenlab_ml/
  │       ├── __init__.py              # Export InferenceClient
  │       ├── client.py                # Main client class
  │       ├── auth.py                  # Authentication handling
  │       ├── api.py                   # API communication layer
  │       ├── upload.py                # File upload to S3 presigned URLs
  │       ├── polling.py               # Status polling logic
  │       ├── exceptions.py            # Custom exceptions
  │       ├── config.py                # Configuration management
  │       └── utils.py                 # Helper functions (validation, etc.)
  │
  ├── tests/
  │   ├── __init__.py
  │   ├── conftest.py                  # Pytest fixtures
  │   ├── test_client.py               # Client integration tests
  │   ├── test_auth.py                 # Auth unit tests
  │   ├── test_api.py                  # API unit tests (mocked)
  │   ├── test_upload.py               # Upload unit tests
  │   ├── test_polling.py              # Polling unit tests
  │   └── test_config.py               # Config unit tests
  │
  ├── examples/
  │   ├── quickstart.py                # Basic usage example
  │   ├── batch_inference.py           # Batch processing example
  │   └── advanced_config.py           # Advanced configuration example
  │
  ├── docs/
  │   ├── quickstart.md                # Getting started guide
  │   ├── api_reference.md             # API documentation
  │   └── configuration.md             # Configuration guide
  │
  ├── .github/
  │   └── workflows/
  │       ├── test.yml                 # CI/CD for tests
  │       └── publish.yml              # PyPI publishing
  │
  ├── pyproject.toml                   # Package metadata (PEP 517/518)
  ├── setup.py                         # Backward compatibility (optional)
  ├── README.md                        # Main documentation
  ├── LICENSE                          # License file
  ├── .env.example                     # Example environment variables
  ├── .gitignore                       # Git ignore rules
  └── CHANGELOG.md                     # Version history

⏺ Implementation Plan by Module

  Phase 1.1: Foundation Setup

  Step 1: Project Scaffolding

  1. Create directory structure
  2. Initialize pyproject.toml with basic metadata
  3. Create .gitignore
  4. Create README.md with installation instructions

  Step 2: Exception Classes (exceptions.py)

  # Define all custom exceptions with clear docstrings
  # Keep it simple - no complex logic

  Step 3: Configuration Module (config.py)

  # Priority order for API key:
  # 1. Constructor parameter
  # 2. Environment variable: REDENLAB_ML_API_KEY
  # 3. Config file: ~/.redenlab-ml/config.yaml

  def load_config(config_path=None):
      """Load config from YAML file"""
      # Use PyYAML
      # Return dict with api_key, base_url, etc.

  def get_default_base_url():
      """Return default API endpoint"""
      return "https://your-api-gateway-url.amazonaws.com/prod"

  Step 4: Authentication Module (auth.py)

  def get_api_key(api_key_param=None):
      """Get API key from param, env var, or config file"""
      # Priority: param > env var > config file

  def validate_api_key(api_key):
      """Validate API key format"""
      # Check it starts with expected prefix
      # Check length constraints

  def get_auth_headers(api_key):
      """Return headers dict for API requests"""
      return {
          'X-Api-Key': api_key,
          'Content-Type': 'application/json'
      }

  Phase 1.2: Core Communication

  Step 5: API Module (api.py)

  import requests
  from tenacity import retry, stop_after_attempt, wait_exponential

  @retry(
      stop=stop_after_attempt(3),
      wait=wait_exponential(multiplier=1, min=2, max=10)
  )
  def _make_request(method, url, headers, json_data=None):
      """Base request handler with retry logic"""
      # Use requests library
      # Handle exceptions, convert to custom exceptions

  def request_presigned_url(base_url, api_key, filename, content_type='audio/wav'):
      """POST /upload-url"""
      # Returns: (job_id, upload_url, file_key, expires_in)

  def submit_inference_job(base_url, api_key, job_id, file_key, model_name):
      """POST /{model_name}/predict"""
      # Returns: (job_id, status, message)

  def get_job_status(base_url, api_key, job_id, model_name):
      """GET /result/{job_id}?model={model_name}"""
      # Returns: job status dict

  Step 6: Upload Module (upload.py)

  def upload_to_presigned_url(file_path, presigned_url, content_type):
      """Upload file to S3 via presigned URL"""
      # Use requests.put()
      # Include Content-Type header
      # Handle upload errors
      # Optional: progress callback

  Step 7: Polling Module (polling.py)

  import time

  def poll_until_complete(
      get_status_func,  # Function to call for status
      job_id,
      model_name,
      timeout=3600,
      initial_interval=5,
      max_interval=60
  ):
      """Poll job status until complete/failed/timeout"""
      # Exponential backoff: 5s, 10s, 20s, 40s, 60s, 60s...
      # Check for terminal states: completed, failed
      # Raise TimeoutError if exceeded
      # Return final status dict

  Phase 1.3: Main Client

  Step 8: Client Class (client.py)

  class InferenceClient:
      def __init__(
          self,
          api_key=None,
          base_url=None,
          model_name='intelligibility',
          timeout=3600
      ):
          """Initialize client"""
          self.api_key = get_api_key(api_key)
          validate_api_key(self.api_key)
          self.base_url = base_url or get_default_base_url()
          self.model_name = model_name
          self.timeout = timeout

      def predict(self, file_path=None, s3_uri=None):
          """
          Run inference on file
          
          For Phase 1: only s3_uri supported
          For Phase 2: file_path support added
          
          Returns: result dict when complete
          """
          if file_path and not s3_uri:
              # Phase 1.4 (file upload flow)
              job_id = self._predict_with_upload(file_path)
          elif s3_uri:
              # Phase 1 (S3 URI flow) - NOT IMPLEMENTED YET
              # This requires different backend flow
              raise NotImplementedError("S3 URI not yet supported")
          else:
              raise ValueError("Must provide either file_path or s3_uri")

          # Poll until complete
          result = poll_until_complete(
              lambda: api.get_job_status(
                  self.base_url, self.api_key, job_id, self.model_name
              ),
              job_id,
              self.model_name,
              timeout=self.timeout
          )

          return result

      def _predict_with_upload(self, file_path):
          """Internal: Handle file upload flow"""
          # 1. Request presigned URL
          job_id, upload_url, file_key, expires_in = api.request_presigned_url(
              self.base_url, self.api_key,
              filename=os.path.basename(file_path),
              content_type='audio/wav'
          )

          # 2. Upload file to S3
          upload_to_presigned_url(file_path, upload_url, 'audio/wav')

          # 3. Submit inference job
          api.submit_inference_job(
              self.base_url, self.api_key, job_id, file_key, self.model_name
          )

          return job_id

      def get_status(self, job_id):
          """Get current job status"""
          return api.get_job_status(
              self.base_url, self.api_key, job_id, self.model_name
          )

  Step 9: Package Init (__init__.py)

  from .client import InferenceClient
  from .exceptions import (
      RedenLabMLError,
      AuthenticationError,
      InferenceError,
      TimeoutError,
      APIError,
      UploadError
  )

  __version__ = "0.1.0"
  __all__ = [
      "InferenceClient",
      "RedenLabMLError",
      "AuthenticationError",
      "InferenceError",
      "TimeoutError",
      "APIError",
      "UploadError"
  ]

⏺ Dependencies & Requirements

  Core Dependencies (pyproject.toml)

  [project]
  name = "redenlab-ml"
  version = "0.1.0"
  description = "Python SDK for RedenLab ML inference service"
  authors = [
      {name = "Your Name", email = "your.email@example.com"}
  ]
  requires-python = ">=3.8"
  dependencies = [
      "requests>=2.31.0",          # HTTP client
      "tenacity>=8.2.0",           # Retry logic with exponential backoff
      "pyyaml>=6.0",               # Config file parsing
      "typing-extensions>=4.5.0",  # For Python 3.8-3.10 compatibility
  ]

  [project.optional-dependencies]
  dev = [
      "pytest>=7.4.0",             # Testing framework
      "pytest-cov>=4.1.0",         # Coverage reporting
      "pytest-mock>=3.11.0",       # Mocking utilities
      "black>=23.7.0",             # Code formatting
      "ruff>=0.0.285",             # Linting
      "mypy>=1.5.0",               # Type checking
      "responses>=0.23.0",         # HTTP mocking for tests
  ]

  [build-system]
  requires = ["hatchling"]
  build-backend = "hatchling.build"

  [tool.hatch.build.targets.wheel]
  packages = ["src/redenlab_ml"]

  Dependency Rationale

  1. requests: Industry standard for HTTP - simple, reliable, well-documented
  2. tenacity: Elegant retry/backoff logic - declarative, flexible
  3. pyyaml: Standard YAML parser for config files
  4. typing-extensions: Backward compatibility for type hints

  Development Dependencies

  1. pytest: Most popular Python testing framework
  2. pytest-cov: Coverage reporting for tests
  3. pytest-mock: Easy mocking/patching
  4. black: Opinionated code formatter (PEP 8 compliant)
  5. ruff: Fast Python linter (replaces flake8, isort, etc.)
  6. mypy: Static type checker
  7. responses: Mock HTTP requests in tests

⏺ Testing Strategy

  Test Layers

  1. Unit Tests (Isolated component testing)

  test_auth.py
  def test_get_api_key_from_param():
      """Test API key from constructor parameter"""

  def test_get_api_key_from_env():
      """Test API key from environment variable"""

  def test_get_api_key_from_config_file():
      """Test API key from config file"""

  def test_validate_api_key_valid():
      """Test valid API key passes validation"""

  def test_validate_api_key_invalid():
      """Test invalid API key raises error"""

  test_config.py
  def test_load_config_from_file():
      """Test loading config from YAML file"""

  def test_load_config_file_not_found():
      """Test graceful handling of missing config file"""

  def test_get_default_base_url():
      """Test default base URL returns correct value"""

  test_api.py
  import responses

  @responses.activate
  def test_request_presigned_url_success():
      """Test successful presigned URL request"""
      responses.add(
          responses.POST,
          "https://api.example.com/upload-url",
          json={"job_id": "123", "upload_url": "https://s3..."},
          status=200
      )

  @responses.activate
  def test_request_presigned_url_auth_error():
      """Test authentication error handling"""

  @responses.activate
  def test_submit_inference_job_success():
      """Test successful job submission"""

  @responses.activate
  def test_get_job_status_completed():
      """Test getting completed job status"""

  test_upload.py
  @responses.activate
  def test_upload_to_presigned_url_success():
      """Test successful file upload"""

  @responses.activate
  def test_upload_to_presigned_url_failure():
      """Test upload failure handling"""

  test_polling.py
  def test_poll_until_complete_immediate():
      """Test polling when job is already complete"""

  def test_poll_until_complete_multiple_attempts():
      """Test polling with exponential backoff"""

  def test_poll_until_complete_timeout():
      """Test timeout handling"""

  def test_poll_until_complete_failure():
      """Test job failure handling"""

  2. Integration Tests (End-to-end flow)

  test_client.py
  @responses.activate
  def test_predict_with_file_upload_success():
      """Test complete predict flow with file upload"""
      # Mock all 3 API calls:
      # 1. POST /upload-url
      # 2. PUT S3 presigned URL
      # 3. POST /predict
      # 4. GET /result (polling)

  @responses.activate
  def test_predict_authentication_error():
      """Test authentication error propagation"""

  @responses.activate
  def test_predict_inference_failure():
      """Test handling of inference job failure"""

  @responses.activate
  def test_get_status():
      """Test get_status method"""

  3. Test Fixtures (conftest.py)

  import pytest
  import tempfile
  import os

  @pytest.fixture
  def temp_audio_file():
      """Create temporary audio file for testing"""
      with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.wav') as f:
          f.write(b'fake audio data')
          filepath = f.name
      yield filepath
      os.unlink(filepath)

  @pytest.fixture
  def mock_api_key():
      """Return mock API key"""
      return "sk_test_1234567890"

  @pytest.fixture
  def mock_base_url():
      """Return mock base URL"""
      return "https://api.example.com"

  @pytest.fixture
  def client(mock_api_key, mock_base_url):
      """Return configured InferenceClient"""
      from redenlab_ml import InferenceClient
      return InferenceClient(api_key=mock_api_key, base_url=mock_base_url)

  Test Coverage Goals

  - Unit tests: >90% coverage
  - Integration tests: Cover all main user flows
  - Edge cases: Authentication failures, network errors, timeouts, malformed responses

  CI/CD Pipeline (.github/workflows/test.yml)

  name: Tests

  on: [push, pull_request]

  jobs:
    test:
      runs-on: ubuntu-latest
      strategy:
        matrix:
          python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']

      steps:
        - uses: actions/checkout@v3
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: ${{ matrix.python-version }}
        - name: Install dependencies
          run: |
            pip install -e ".[dev]"
        - name: Run tests
          run: |
            pytest tests/ --cov=src/redenlab_ml --cov-report=xml
        - name: Upload coverage
          uses: codecov/codecov-action@v3

⏺ Complete Implementation Plan Summary

  ---
  PHASE 1: Minimal Core - File Upload & Inference

  Goal: Single file inference with local file upload

  Implementation Order

  Week 1: Foundation

  1. Project scaffolding
    - Create directory structure
    - Initialize pyproject.toml
    - Create .gitignore, README.md, .env.example
    - Set up Git repository
  2. Core modules (no external dependencies)
    - exceptions.py - All custom exception classes
    - utils.py - Validation helpers, file type detection
    - config.py - Configuration loading logic
  3. Authentication
    - auth.py - API key management, validation, header generation
    - Unit tests for auth module

  Week 2: API Communication

  4. API layer
    - api.py - All HTTP communication with retry logic
    - Unit tests with mocked responses
  5. File upload
    - upload.py - S3 presigned URL upload logic
    - Unit tests with mocked S3
  6. Polling
    - polling.py - Status polling with exponential backoff
    - Unit tests with mocked status responses

  Week 3: Client & Integration

  7. Main client
    - client.py - InferenceClient class
    - Orchestrate all modules
    - __init__.py - Package exports
  8. Integration testing
    - End-to-end tests
    - Example scripts
    - Documentation
  9. Polish
    - Error message improvements
    - Logging
    - README with usage examples

  ---
  Key Design Decisions

  1. Authentication Priority

  1. Constructor parameter (explicit override)
  2. Environment variable REDENLAB_ML_API_KEY
  3. Config file ~/.redenlab-ml/config.yaml

  2. Error Handling

  - All backend errors converted to custom exceptions
  - Clear, actionable error messages
  - Preserve original error context for debugging

  3. Retry Strategy

  - API calls: 3 retries with exponential backoff (2s, 4s, 8s)
  - Polling: Start at 5s, max 60s, exponential growth
  - Upload: No automatic retry (large files - user should handle)

  4. Timeout Defaults

  - Presigned URL expiration: 15 minutes (backend default)
  - Inference timeout: 1 hour (configurable)
  - HTTP request timeout: 30 seconds

  5. File Support (Phase 1)

  - Accept local file paths
  - Auto-detect content type (default: audio/wav)
  - Validate file exists before starting

  ---
  Example Usage (Target API)

  from redenlab_ml import InferenceClient

  # Initialize client
  client = InferenceClient(
      api_key="sk_live_...",  # or use env var
      model_name="intelligibility"
  )

  # Run inference on local file
  result = client.predict(file_path="audio.wav")

  print(result)
  # {
  #   'job_id': 'uuid',
  #   'status': 'completed',
  #   'result': {'intelligibility_score': 0.85},
  #   'created_at': '2025-01-15T10:30:00Z',
  #   'completed_at': '2025-01-15T10:35:00Z'
  # }

  # Or check status separately
  job_id = "existing-job-uuid"
  status = client.get_status(job_id)
  print(status['status'])  # 'processing', 'completed', 'failed'

  ---
  Future Enhancements (Post-Phase 1)

  Phase 2: Advanced Features

  - Batch processing support
  - Progress callbacks for uploads
  - Async/await support (asyncio)
  - Result caching
  - Resume interrupted jobs

  Phase 3: Production Readiness

  - Structured logging
  - Metrics/telemetry
  - Rate limit handling
  - Webhook support for job completion
  - CLI tool wrapper

  ---
  Documentation Plan

  README.md

  - Quick start (5 min to first inference)
  - Installation instructions
  - Basic usage example
  - Configuration options
  - Links to full docs

  docs/quickstart.md

  - Detailed getting started guide
  - Multiple examples
  - Common pitfalls

  docs/api_reference.md

  - Full API documentation
  - All methods, parameters, return values
  - Exception reference

  docs/configuration.md

  - All configuration options
  - Environment variables
  - Config file format
  - Best practices

  examples/

  - quickstart.py - Minimal example
  - batch_inference.py - Process multiple files
  - error_handling.py - Robust error handling
  - custom_config.py - Advanced configuration

  ---
  Package Naming

  Recommended: redenlab-ml (PyPI package name)
  - Import name: redenlab_ml
  - Config directory: ~/.redenlab-ml/
  - Env var: REDENLAB_ML_API_KEY

  ---
  Summary

  This plan provides:
  1. Clear module boundaries and responsibilities
  2. Testable architecture with mocked dependencies
  3. Incremental implementation path
  4. Production-ready error handling and retry logic
  5. Extensible design for future features

  The SDK will provide a simple, Pythonic interface while handling all the complexity of:
  - File uploads to S3
  - SageMaker job submission
  - Status polling with backoff
  - Error handling and retries
  - Authentication and configuration

  Next Steps: Ready to implement when you are! Start with project scaffolding and work through modules in order.
