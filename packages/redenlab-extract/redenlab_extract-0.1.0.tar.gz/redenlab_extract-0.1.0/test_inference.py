#!/usr/bin/env python3
"""
Test script for RedenLab ML SDK - Local inference test

This script tests the SDK by making a real inference call to the backend.
"""

import os
import sys
from pathlib import Path

# Import the SDK
try:
    from redenlab_ml import InferenceClient
except ImportError as e:
    print(f"Error: Could not import redenlab_ml. Did you install it?")
    print(f"Run: pip install -e .")
    print(f"Error details: {e}")
    sys.exit(1)


def test_inference():
    """Test inference with a local audio file."""

    # Configuration
    API_KEY = os.environ.get('REDENLAB_ML_API_KEY')
    if not API_KEY:
        print("Error: REDENLAB_ML_API_KEY environment variable not set")
        print("Set it with: export REDENLAB_ML_API_KEY='your-api-key'")
        sys.exit(1)

    BASE_URL = "https://16y6zoptl8.execute-api.us-west-2.amazonaws.com/prod"
    TEST_AUDIO = "/Users/ayushranjan/Documents/Redenlab/Git_projects/Intelligens-ML-Endpoints/test_data/medum_file/ActiveMS_Reading_1.wav"
    MODEL_NAME = "intelligibility"

    # Validate test file exists
    if not Path(TEST_AUDIO).exists():
        print(f"Error: Test audio file not found: {TEST_AUDIO}")
        sys.exit(1)

    print("=" * 70)
    print("RedenLab ML SDK - Inference Test")
    print("=" * 70)
    print(f"API URL: {BASE_URL}")
    print(f"Model: {MODEL_NAME}")
    print(f"Test file: {TEST_AUDIO}")
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    print("=" * 70)
    print()

    try:
        # Initialize client
        print("Initializing client...")
        client = InferenceClient(
            api_key=API_KEY,
            base_url=BASE_URL,
            model_name=MODEL_NAME,
            timeout=3600  # 1 hour timeout
        )
        print(f"✓ Client initialized: {client}")
        print()

        # Define progress callback
        def on_progress(status_data):
            status = status_data.get('status', 'unknown')
            print(f"  Status: {status}")
            if status == 'processing':
                submitted_at = status_data.get('submitted_at', 'N/A')
                print(f"    Submitted at: {submitted_at}")

        # Run inference
        print("Starting inference...")
        print("This will:")
        print("  1. Request presigned URL")
        print("  2. Upload file to S3")
        print("  3. Submit inference job")
        print("  4. Poll for completion")
        print()

        result = client.predict(
            file_path=TEST_AUDIO,
            progress_callback=on_progress
        )

        # Display results
        print()
        print("=" * 70)
        print("INFERENCE COMPLETE!")
        print("=" * 70)
        print(f"Job ID: {result.get('job_id')}")
        print(f"Status: {result.get('status')}")
        print(f"Created at: {result.get('created_at')}")
        print(f"Completed at: {result.get('completed_at')}")
        print()
        print("Result:")
        print("-" * 70)

        # Pretty print the result
        inference_result = result.get('result', {})
        if isinstance(inference_result, dict):
            for key, value in inference_result.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {inference_result}")

        print("=" * 70)
        print("✓ Test completed successfully!")

        return result

    except Exception as e:
        print()
        print("=" * 70)
        print("ERROR!")
        print("=" * 70)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_inference()
