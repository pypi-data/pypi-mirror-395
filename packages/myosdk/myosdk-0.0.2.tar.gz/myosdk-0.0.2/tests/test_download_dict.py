"""Test that download accepts both string ID and dict."""

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
def test_download_with_asset_dict(client, test_video_file):
    """Test that download works when passing asset dict instead of just ID."""
    # Upload asset
    asset = client.assets.upload_file(test_video_file)
    asset_id = asset["asset_id"]

    # Get full asset details
    asset_details = client.assets.get(asset_id)

    # Download using dict (this is what was failing before)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        download_path = Path(tmp.name)

    try:
        # This should work now - passing dict instead of string
        client.assets.download(asset_details, download_path)
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


@pytest.mark.integration
def test_download_with_asset_id_string(client, test_video_file):
    """Test that download still works with string ID (backward compatibility)."""
    # Upload asset
    asset = client.assets.upload_file(test_video_file)
    asset_id = asset["asset_id"]

    # Download using string ID (traditional way)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        download_path = Path(tmp.name)

    try:
        # This should still work - passing string
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


