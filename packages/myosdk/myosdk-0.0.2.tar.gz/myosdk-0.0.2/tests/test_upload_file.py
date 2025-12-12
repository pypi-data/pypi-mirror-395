"""Test the convenience upload_file method."""

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def api_key():
    """Get API key from environment or skip test."""
    key = os.getenv(
        "MYOSDK_API_KEY", "v2m_KZD5F99K5wMkJR3z:7QXducgg3wapXv9Fla2FdQAcKMqJfZXK"
    )
    if not key:
        pytest.skip("MYOSDK_API_KEY environment variable not set")
    return key


@pytest.fixture
def base_url():
    """Get base URL from environment or use default."""
    return os.getenv("MYOSDK_BASE_URL", "http://localhost:8000")


@pytest.fixture
def client(api_key, base_url):
    """Create SDK client."""
    from myosdk import Client

    client = Client(api_key=api_key, base_url=base_url)
    yield client
    client.close()


@pytest.fixture
def test_video_file():
    """Create a minimal test video file."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        f.write(b"\x00\x00\x00\x20ftypisom\x00\x00\x02\x00isomiso2mp41")
        temp_path = Path(f.name)

    yield temp_path

    if temp_path.exists():
        temp_path.unlink()


@pytest.mark.integration
def test_upload_file_simple(client, test_video_file):
    """Test simple one-step upload."""
    # Upload in one step
    result = client.assets.upload_file(test_video_file)

    # Verify result
    assert "asset_id" in result
    assert result["verified"] is True
    assert result["size_bytes"] > 0
    assert "checksum_sha256" in result

    # Cleanup
    try:
        client.assets.delete(result["asset_id"])
    except Exception:
        pass


@pytest.mark.integration
def test_upload_file_with_metadata(client, test_video_file):
    """Test upload with custom metadata."""
    metadata = {"scene": "test", "duration": 5}

    result = client.assets.upload_file(test_video_file, metadata=metadata)

    assert "asset_id" in result
    assert result["verified"] is True

    # Verify metadata was stored
    asset = client.assets.get(result["asset_id"])
    assert asset.get("metadata", {}).get("scene") == "test"
    assert asset.get("metadata", {}).get("duration") == 5

    # Cleanup
    try:
        client.assets.delete(result["asset_id"])
    except Exception:
        pass


@pytest.mark.integration
def test_upload_file_explicit_purpose(client, test_video_file):
    """Test upload with explicit purpose override."""
    # Upload as trackers instead of video (for testing)
    result = client.assets.upload_file(test_video_file, purpose="trackers")

    assert "asset_id" in result
    assert result["verified"] is True

    # Verify purpose
    asset = client.assets.get(result["asset_id"])
    assert asset["purpose"] == "trackers"

    # Cleanup
    try:
        client.assets.delete(result["asset_id"])
    except Exception:
        pass


def test_upload_file_not_found(client):
    """Test upload with non-existent file."""
    with pytest.raises(FileNotFoundError):
        client.assets.upload_file("/nonexistent/file.mp4")


def test_detect_purpose():
    """Test purpose detection from file extensions."""
    from myosdk import Client

    client = Client(api_key="test", base_url="http://localhost:8000")

    # Video files
    assert client.assets._detect_purpose(Path("video.mp4")) == "video"
    assert client.assets._detect_purpose(Path("video.mov")) == "video"
    assert client.assets._detect_purpose(Path("video.avi")) == "video"
    assert client.assets._detect_purpose(Path("video.webm")) == "video"

    # Tracker files
    assert client.assets._detect_purpose(Path("trackers.pkl")) == "trackers"
    assert client.assets._detect_purpose(Path("data.pickle")) == "trackers"

    # Unknown defaults to video
    assert client.assets._detect_purpose(Path("unknown.xyz")) == "video"

    client.close()


def test_detect_content_type():
    """Test content type detection from file extensions."""
    from myosdk import Client

    client = Client(api_key="test", base_url="http://localhost:8000")

    # Common video types
    assert client.assets._detect_content_type(Path("video.mp4")) == "video/mp4"
    assert client.assets._detect_content_type(Path("video.mov")) == "video/quicktime"
    assert client.assets._detect_content_type(Path("video.avi")) == "video/x-msvideo"
    assert client.assets._detect_content_type(Path("video.webm")) == "video/webm"

    # Pickle files
    assert (
        client.assets._detect_content_type(Path("data.pkl"))
        == "application/octet-stream"
    )

    client.close()
