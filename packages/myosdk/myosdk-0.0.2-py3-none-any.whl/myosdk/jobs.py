"""Jobs resource for managing retarget jobs."""

import time
from collections.abc import Iterable
from datetime import datetime
from typing import Any, Literal

from myosdk.http import HTTPClient


class Jobs:
    """Jobs resource for managing retarget jobs."""

    def __init__(self, http_client: HTTPClient):
        """Initialize Jobs resource.

        Args:
            http_client: HTTP client instance
        """
        self._http = http_client

    def start_retarget(
        self,
        c3d_asset_id: str | None = None,
        c3d_s3: str | None = None,
        markerset_asset_id: str | None = None,
        markerset_s3: str | None = None,
        character_id: str | None = "0199e278-06e6-7726-a6ba-9929f79005e8",
        character_version: str | None = "v1.0.0",
        enable_scaling: bool = True,
        subject_gender: Literal["male", "female"] = "male",
        subject_height: float | None = None,
        subject_weight: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict:
        """Start a retarget job.

        Args:
            c3d_asset_id: Asset ID of the C3D motion capture file (either this or c3d_s3 required)
            c3d_s3: Direct S3 key of the C3D file (either this or c3d_asset_id required)
            markerset_asset_id: Asset ID of the markerset XML file (either this or markerset_s3 required)
            markerset_s3: Direct S3 key of the markerset XML file (either this or markerset_asset_id required)
            character_id: Character identifier (default: "0199e278-06e6-7726-a6ba-9929f79005e8")
            character_version: Character version (default: "v1.0.0")
            enable_scaling: Whether to enable body scaling during retargeting (default: True)
            subject_gender: Subject gender for anthropometric scaling (default: "male")
            subject_height: Subject height in meters for anthropometric scaling (default: None)
            subject_weight: Subject weight in kilograms for anthropometric scaling (default: None)
            metadata: Optional metadata dict

        Returns:
            Dict with job_id, type, status, message, estimated_wait_time_seconds

        Raises:
            ValueError: If required inputs are not provided
        """
        if not c3d_asset_id and not c3d_s3:
            raise ValueError("Either c3d_asset_id or c3d_s3 must be provided")
        if not markerset_asset_id and not markerset_s3:
            raise ValueError(
                "Either markerset_asset_id or markerset_s3 must be provided"
            )

        payload: dict[str, Any] = {}
        if c3d_asset_id:
            payload["c3d_asset_id"] = c3d_asset_id
        if c3d_s3:
            payload["c3d_s3"] = c3d_s3
        if markerset_asset_id:
            payload["markerset_asset_id"] = markerset_asset_id
        if markerset_s3:
            payload["markerset_s3"] = markerset_s3
        if character_id:
            payload["character_id"] = character_id
        if character_version:
            payload["character_version"] = character_version
        payload["enable_scaling"] = enable_scaling
        payload["subject_gender"] = subject_gender
        if subject_height is not None:
            payload["subject_height"] = subject_height
        if subject_weight is not None:
            payload["subject_weight"] = subject_weight
        if metadata:
            payload["metadata"] = metadata

        return self._http.post("/v1/runs/retarget", json=payload)

    def get(self, job_id: str) -> dict:
        """Get job status.

        Args:
            job_id: Job identifier

        Returns:
            Dict with job status and results
        """
        return self._http.get(f"/v1/jobs/{job_id}")

    def wait(
        self,
        job_id: str,
        interval: float = 2.0,
        timeout: float | None = None,
    ) -> dict:
        """Wait for a job to complete.

        Args:
            job_id: Job identifier
            interval: Polling interval in seconds (default: 2.0)
            timeout: Maximum time to wait in seconds (None = no timeout)

        Returns:
            Final job status dict

        Raises:
            TimeoutError: If timeout is exceeded
        """
        start_time = time.time()
        wait_interval = interval

        while True:
            job = self.get(job_id)
            status = job.get("status", "").upper()

            # Check if job is in a terminal state
            if status in ("SUCCEEDED", "FAILED", "CANCELED"):
                return job

            # Check timeout
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    raise TimeoutError(
                        f"Job {job_id} did not complete within {timeout} seconds"
                    )

            # Use the specified interval (in a real implementation, we'd check Retry-After header)
            # For MVP, we use the fixed interval
            time.sleep(wait_interval)

    def cancel(self, job_id: str) -> dict:
        """Cancel a job.

        Args:
            job_id: Job identifier

        Returns:
            Dict with job_id, status, message
        """
        response = self._http.delete(f"/v1/jobs/{job_id}")
        # DELETE returns JSON body according to the API
        if response is None:
            return {"job_id": job_id, "status": "CANCELED", "message": "Job canceled"}
        return response

    def list(
        self,
        status: str | Iterable[str] | None = None,
        job_type: str | Iterable[str] | None = None,
        created_after: datetime | str | None = None,
        created_before: datetime | str | None = None,
        run_id: str | None = None,
        has_output: bool | None = None,
        input_asset_id: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        """List jobs with optional filters.

        Args:
            status: Status or list of statuses (e.g., \"SUCCEEDED\", [\"RUNNING\", \"QUEUED\"])
            job_type: Job type(s) to include (\"retarget\")
            created_after: ISO 8601 timestamp or datetime for lower bound
            created_before: ISO 8601 timestamp or datetime for upper bound
            run_id: Filter by run identifier
            has_output: Filter jobs that have (or do not have) output assets
            input_asset_id: Filter jobs that used a given input asset
            limit: Items per page
            offset: Items to skip

        Returns:
            Dict with jobs list and pagination info
        """

        def _as_list(value: str | Iterable[str] | None) -> list[str] | None:
            if value is None:
                return None
            if isinstance(value, (list, tuple, set)):
                return [str(v) for v in value]
            return [str(value)]

        def _format_dt(value: datetime | str | None) -> str | None:
            if value is None:
                return None
            if isinstance(value, datetime):
                return value.isoformat()
            return value

        params: dict[str, Any] = {"limit": limit, "offset": offset}

        statuses = _as_list(status)
        types = _as_list(job_type)

        if statuses:
            params["status"] = statuses
        if types:
            params["type"] = types

        created_after_str = _format_dt(created_after)
        created_before_str = _format_dt(created_before)

        if created_after_str:
            params["created_after"] = created_after_str
        if created_before_str:
            params["created_before"] = created_before_str
        if run_id:
            params["run_id"] = run_id
        if has_output is not None:
            params["has_output"] = has_output
        if input_asset_id:
            params["input_asset_id"] = input_asset_id

        return self._http.get("/v1/jobs", params=params)
