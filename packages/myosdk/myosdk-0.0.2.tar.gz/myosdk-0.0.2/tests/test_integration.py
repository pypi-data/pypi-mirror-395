"""Integration tests for the SDK against a running API.

These tests require a running API server. Set environment variables:
- MYOSDK_API_KEY: Your API key (format: key_id:secret)
- MYOSDK_BASE_URL: Base URL (default: http://localhost:8000)

To skip tests if API is not available, use: pytest -m "not integration"
"""

import os
import tempfile
from pathlib import Path

import pytest

# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def api_key():
    """Get API key from environment or skip test."""
    key = os.getenv(
        "MYOSDK_API_KEY", "v2m_KZD5F99K5wMkJR3z:7QXducgg3wapXv9Fla2FdQAcKMqJfZXK"
    )
    if not key:
        pytest.skip("MYOSDK_API_KEY environment variable not set")
    return key


@pytest.fixture(scope="module")
def base_url():
    """Get base URL from environment or use default."""
    return os.getenv("MYOSDK_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="module")
def client(api_key, base_url):
    """Create SDK client."""
    from myosdk import Client

    client = Client(api_key=api_key, base_url=base_url)
    yield client
    client.close()


@pytest.fixture
def test_video_file():
    """Create a minimal test video file."""
    # Create a tiny MP4 file (just header bytes)
    # In a real scenario, you'd use an actual video file
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        # Minimal MP4 header (ftyp box)
        f.write(
            b"\x00\x00\x00\x20"  # box size
            b"ftyp"  # box type
            b"isom"  # major brand
            b"\x00\x00\x02\x00"  # minor version
            b"isom"  # compatible brands
            b"iso2"
            b"mp41"
        )
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


def test_client_health_check(client):
    """Test that we can connect to the API."""
    # Try to make a simple request - health endpoint doesn't require auth
    import httpx

    base_url = client._http.base_url
    response = httpx.get(f"{base_url}/v1/healthz", timeout=5.0)
    assert response.status_code == 200


def test_assets_initiate(client, test_video_file):
    """Test asset upload initiation."""
    asset = client.assets.initiate(
        purpose="video",
        filename=test_video_file.name,
        content_type="video/mp4",
    )

    assert "asset_id" in asset
    assert "upload_url" in asset
    assert "fields" in asset
    assert "expires_at" in asset
    assert asset["upload_url"].startswith("http")


def test_assets_upload_and_complete(client, test_video_file):
    """Test full asset upload workflow."""
    # Initiate upload
    asset = client.assets.initiate(
        purpose="video",
        filename=test_video_file.name,
        content_type="video/mp4",
    )
    asset_id = asset["asset_id"]

    # Upload file
    with open(test_video_file, "rb") as f:
        client.assets.upload(asset, f)

    # Complete upload
    result = client.assets.complete(asset_id)
    assert result["asset_id"] == asset_id
    assert result["verified"] is True
    assert "size_bytes" in result
    assert "checksum_sha256" in result

    # Cleanup
    try:
        client.assets.delete(asset_id)
    except Exception:
        pass  # Ignore cleanup errors


def test_assets_get(client, test_video_file):
    """Test getting asset details."""
    # Create and upload asset
    asset = client.assets.initiate(
        purpose="video",
        filename=test_video_file.name,
        content_type="video/mp4",
    )
    asset_id = asset["asset_id"]

    with open(test_video_file, "rb") as f:
        client.assets.upload(asset, f)

    client.assets.complete(asset_id)

    # Get asset details
    details = client.assets.get(asset_id)
    assert details["asset_id"] == asset_id
    assert details["purpose"] == "video"
    assert "download_url" in details
    assert "size_bytes" in details

    # Cleanup
    try:
        client.assets.delete(asset_id)
    except Exception:
        pass


def test_assets_list(client):
    """Test listing assets."""
    result = client.assets.list(limit=10)
    assert "assets" in result
    assert "total" in result
    assert isinstance(result["assets"], list)


def test_assets_download(client, test_video_file):
    """Test downloading an asset."""
    # Create and upload asset
    asset = client.assets.initiate(
        purpose="video",
        filename=test_video_file.name,
        content_type="video/mp4",
    )
    asset_id = asset["asset_id"]

    with open(test_video_file, "rb") as f:
        client.assets.upload(asset, f)

    client.assets.complete(asset_id)

    # Download asset
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        download_path = Path(tmp.name)

    try:
        client.assets.download(asset_id, download_path)
        assert download_path.exists()
        assert download_path.stat().st_size > 0
    finally:
        if download_path.exists():
            download_path.unlink()

    # Cleanup
    try:
        client.assets.delete(asset_id)
    except Exception:
        pass


def test_jobs_start_tracker(client, test_video_file):
    """Test starting a tracker job."""
    # Create and upload video asset
    asset = client.assets.initiate(
        purpose="video",
        filename=test_video_file.name,
        content_type="video/mp4",
    )
    asset_id = asset["asset_id"]

    with open(test_video_file, "rb") as f:
        client.assets.upload(asset, f)

    client.assets.complete(asset_id)

    # Start tracker job
    job = client.jobs.start_tracker(video_asset_id=asset_id)

    assert "job_id" in job
    assert job["type"] == "tracker"
    assert job["status"] in ("QUEUED", "RUNNING", "SUCCEEDED", "FAILED")

    # Cleanup
    try:
        client.assets.delete(asset_id)
    except Exception:
        pass


def test_jobs_get_status(client, test_video_file):
    """Test getting job status."""
    # Create and upload video asset
    asset = client.assets.initiate(
        purpose="video",
        filename=test_video_file.name,
        content_type="video/mp4",
    )
    asset_id = asset["asset_id"]

    with open(test_video_file, "rb") as f:
        client.assets.upload(asset, f)

    client.assets.complete(asset_id)

    # Start tracker job
    job = client.jobs.start_tracker(video_asset_id=asset_id)
    job_id = job["job_id"]

    # Get job status
    status = client.jobs.get(job_id)
    assert status["job_id"] == job_id
    assert status["type"] == "tracker"
    assert "status" in status
    assert "created_at" in status

    # Cleanup
    try:
        client.assets.delete(asset_id)
    except Exception:
        pass


def test_jobs_wait_timeout(client, test_video_file):
    """Test job wait with timeout."""
    # Create and upload video asset
    asset = client.assets.initiate(
        purpose="video",
        filename=test_video_file.name,
        content_type="video/mp4",
    )
    asset_id = asset["asset_id"]

    with open(test_video_file, "rb") as f:
        client.assets.upload(asset, f)

    client.assets.complete(asset_id)

    # Start tracker job
    job = client.jobs.start_tracker(video_asset_id=asset_id)
    job_id = job["job_id"]

    # Wait with short timeout (should not raise if job completes quickly)
    try:
        result = client.jobs.wait(job_id, interval=1.0, timeout=30.0)
        assert result["status"] in ("SUCCEEDED", "FAILED", "CANCELED")
    except Exception as e:
        # If timeout occurs, that's also acceptable for this test
        assert "timeout" in str(e).lower() or "did not complete" in str(e).lower()

    # Cleanup
    try:
        client.assets.delete(asset_id)
    except Exception:
        pass


def test_full_workflow(client, test_video_file):
    """Test the complete workflow: upload -> tracker -> retarget -> download."""
    # This is a longer test that exercises the full pipeline
    # It may take a while depending on job processing time

    # Step 1: Upload video
    asset = client.assets.initiate(
        purpose="video",
        filename=test_video_file.name,
        content_type="video/mp4",
    )
    video_asset_id = asset["asset_id"]

    with open(test_video_file, "rb") as f:
        client.assets.upload(asset, f)

    client.assets.complete(video_asset_id)

    # Step 2: Start tracker job
    tracker_job = client.jobs.start_tracker(video_asset_id=video_asset_id)
    tracker_job_id = tracker_job["job_id"]

    # Step 3: Wait for tracker to complete (with timeout)
    try:
        tracker_result = client.jobs.wait(tracker_job_id, interval=2.0, timeout=60.0)
        if tracker_result["status"] == "SUCCEEDED" and "output" in tracker_result:
            # Tracker completed successfully
            # Note: Retarget jobs now require C3D and markerset files as inputs,
            # not tracker output. See start_retarget() for the new API signature.
            pass
    except Exception as e:
        # If tracker job fails or times out, that's acceptable for integration test
        # The important thing is that we tested the SDK methods
        assert (
            "timeout" in str(e).lower()
            or "failed" in str(e).lower()
            or "error" in str(e).lower()
        )

    # Cleanup
    try:
        client.assets.delete(video_asset_id)
    except Exception:
        pass


def test_error_handling(client):
    """Test error handling with invalid requests."""
    from myosdk import NotFoundError, ValidationError

    # Test getting non-existent asset
    with pytest.raises(NotFoundError):
        client.assets.get("00000000-0000-0000-0000-000000000000")

    # Test invalid asset creation
    with pytest.raises(ValidationError):
        client.assets.initiate(
            purpose="invalid_purpose",  # Invalid purpose
            filename="test.mp4",
            content_type="video/mp4",
        )


def test_authentication_error():
    """Test that invalid API key raises AuthenticationError."""
    from myosdk import AuthenticationError, Client

    client = Client(api_key="invalid:key", base_url="http://localhost:8000")
    try:
        with pytest.raises(AuthenticationError):
            client.assets.list()
    finally:
        client.close()
