"""Assets resource for managing file uploads and downloads."""

import mimetypes
from io import BufferedReader
from pathlib import Path
from typing import Any, BinaryIO

from myosdk.http import HTTPClient


class Assets:
    """Assets resource for managing file uploads and downloads."""

    def __init__(self, http_client: HTTPClient):
        """Initialize Assets resource.

        Args:
            http_client: HTTP client instance
        """
        self._http = http_client

    def initiate(
        self,
        purpose: str,
        filename: str,
        content_type: str = "application/octet-stream",
        expected_size_bytes: int | None = None,
        metadata: dict | None = None,
    ) -> dict:
        """Initiate an asset upload.

        Args:
            purpose: Asset purpose (e.g., "video", "trackers")
            filename: Original filename
            content_type: MIME type of the file
            expected_size_bytes: Optional expected file size
            metadata: Optional metadata dict

        Returns:
            Dict with asset_id, upload_url, fields, expires_at
        """
        payload = {
            "purpose": purpose,
            "filename": filename,
            "content_type": content_type,
        }
        if expected_size_bytes is not None:
            payload["expected_size_bytes"] = expected_size_bytes
        if metadata is not None:
            payload["metadata"] = metadata

        return self._http.post("/v1/assets/initiate", json=payload)

    def upload(
        self, asset: dict | str, file_like: BinaryIO | BufferedReader | Path | str
    ) -> None:
        """Upload a file to a presigned URL.

        Args:
            asset: Asset dict from initiate() (must contain upload_url and fields)
            file_like: File-like object, Path, or file path string

        Raises:
            ValueError: If asset dict is missing required fields
        """
        # Asset dict from initiate() should have upload_url and fields directly
        if isinstance(asset, str):
            raise ValueError(
                "upload() requires asset dict from initiate(), not asset_id. Use initiate() first."
            )

        upload_url = asset.get("upload_url")
        fields = asset.get("fields", {})

        if not upload_url:
            raise ValueError(
                "Asset dict missing upload_url. Make sure to use the dict returned by initiate()."
            )

        # Handle file input
        if isinstance(file_like, str | Path):
            file_path = Path(file_like)
            file_obj = open(file_path, "rb")
            filename = file_path.name
            should_close = True
        else:
            file_obj = file_like
            filename = getattr(file_obj, "name", "file")
            should_close = False

        try:
            # Upload to presigned POST URL
            # For presigned POST, we need to send fields + file as multipart/form-data
            # httpx accepts files in format: {"file": (filename, file_obj, content_type)} or {"file": (filename, file_obj)}
            content_type = (
                getattr(file_obj, "content_type", None) or "application/octet-stream"
            )
            files = {"file": (filename, file_obj, content_type)}
            response = self._http.post_multipart(upload_url, data=fields, files=files)
            # Presigned POST typically returns 204 or 201, but we don't need to parse JSON
            # Just verify it was successful
            if response.status_code not in (200, 201, 204):
                raise ValueError(f"Upload failed with status {response.status_code}")
        finally:
            if should_close:
                file_obj.close()

    def complete(self, asset_id: str) -> dict:
        """Complete an asset upload.

        Args:
            asset_id: Asset identifier

        Returns:
            Dict with asset_id, verified, size_bytes, checksum_sha256, message
        """
        return self._http.post(f"/v1/assets/{asset_id}/complete")

    def get(self, asset_id: str) -> dict:
        """Get asset details.

        Args:
            asset_id: Asset identifier

        Returns:
            Dict with asset details including download_url
        """
        return self._http.get(f"/v1/assets/{asset_id}")

    def download(self, asset: str | dict, destination: str | Path) -> None:
        """Download an asset to a local file.

        Args:
            asset: Asset identifier (string) or asset dict from get()
            destination: Destination file path

        Raises:
            ValueError: If asset doesn't have a download_url
        """
        # Accept either asset_id string or asset dict for convenience
        if isinstance(asset, dict):
            asset_data = asset
            asset_id = asset.get("asset_id")
        else:
            asset_id = asset
            asset_data = self.get(asset_id)

        download_url = asset_data.get("download_url")

        if not download_url:
            raise ValueError(
                f"Asset {asset_id} does not have a download_url (might not be ready yet)"
            )

        # Download from presigned URL
        response = self._http.get_raw(download_url)
        response.raise_for_status()

        # Write to file
        destination_path = Path(destination)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        with open(destination_path, "wb") as f:
            f.write(response.content)

    def list(
        self,
        purpose: str | None = None,
        reference_count: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        """List assets.

        Args:
            purpose: Filter by purpose
            reference_count: Filter by reference count
            limit: Items per page
            offset: Items to skip

        Returns:
            Dict with assets list and pagination info
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if purpose is not None:
            params["purpose"] = purpose
        if reference_count is not None:
            params["reference_count"] = reference_count

        return self._http.get("/v1/assets", params=params)

    def delete(self, asset_id: str) -> None:
        """Delete an asset.

        Args:
            asset_id: Asset identifier
        """
        self._http.delete(f"/v1/assets/{asset_id}")

    def upload_file(
        self,
        file_path: str | Path,
        purpose: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict:
        """Upload a file in one step (convenience method).

        This is a high-level method that handles initiate → upload → complete automatically.
        It auto-detects filename, content_type, and purpose from the file.

        Args:
            file_path: Path to the file to upload
            purpose: Asset purpose (auto-detected if not provided: video files → "video", .pkl → "trackers")
            metadata: Optional metadata dict

        Returns:
            Dict with completed asset details including asset_id, verified, size_bytes, checksum_sha256

        Example:
            >>> asset = client.assets.upload_file("walk.mp4")
            >>> print(asset["asset_id"])
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Auto-detect purpose from file extension if not provided
        if purpose is None:
            purpose = self._detect_purpose(path)

        # Auto-detect content type from file extension
        content_type = self._detect_content_type(path)

        # Get file size for validation
        file_size = path.stat().st_size

        # Step 1: Initiate upload
        asset = self.initiate(
            purpose=purpose,
            filename=path.name,
            content_type=content_type,
            expected_size_bytes=file_size,
            metadata=metadata,
        )

        # Step 2: Upload file
        with open(path, "rb") as f:
            self.upload(asset, f)

        # Step 3: Complete upload and return result
        return self.complete(asset["asset_id"])

    def _detect_purpose(self, path: Path) -> str:
        """Detect asset purpose from file extension.

        Args:
            path: File path

        Returns:
            Purpose string ("video", "trackers", or "retarget")
        """
        extension = path.suffix.lower()

        # Video extensions
        video_extensions = {".mp4", ".mov", ".avi", ".webm", ".mkv", ".flv", ".wmv"}
        if extension in video_extensions:
            return "video"

        # Tracker/pickle files
        tracker_extensions = {".pkl", ".pickle"}
        if extension in tracker_extensions:
            return "trackers"

        # Retarget input files (C3D motion capture, markerset XML)
        retarget_extensions = {".c3d", ".xml"}
        if extension in retarget_extensions:
            return "retarget"

        # Default to video for unknown types (conservative choice)
        return "video"

    def _detect_content_type(self, path: Path) -> str:
        """Detect MIME type from file extension.

        Args:
            path: File path

        Returns:
            MIME type string
        """
        # Try to guess from extension
        content_type, _ = mimetypes.guess_type(str(path))

        if content_type:
            return content_type

        # Fallback for common cases
        extension = path.suffix.lower()
        fallback_types = {
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo",
            ".webm": "video/webm",
            ".pkl": "application/octet-stream",
            ".pickle": "application/octet-stream",
        }

        return fallback_types.get(extension, "application/octet-stream")
