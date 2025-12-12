"""Characters resource for browsing available characters and versions."""

from typing import Any

from myosdk.http import HTTPClient


class Characters:
    """Read-only character catalog."""

    def __init__(self, http_client: HTTPClient):
        """Initialize Characters resource."""
        self._http = http_client

    def list(
        self,
        name_contains: str | None = None,
        has_ready_versions: bool | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List available characters with optional filtering.

        Args:
            name_contains: Filter by substring match on name
            has_ready_versions: Only include characters that have READY versions
            limit: Items per page
            offset: Items to skip

        Returns:
            Dict containing character list and pagination info
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if name_contains:
            params["name_contains"] = name_contains
        if has_ready_versions is not None:
            params["has_ready_versions"] = has_ready_versions

        return self._http.get("/v1/characters", params=params)

    def get(self, character_id: str) -> dict[str, Any]:
        """Get details for a single character."""
        return self._http.get(f"/v1/characters/{character_id}")

    def validate_manifest(self, character_id: str, version: str) -> dict[str, Any]:
        """Validate that a character manifest exists in storage."""
        if not version:
            raise ValueError("version is required")

        return self._http.post(
            f"/v1/characters/{character_id}/validate-manifest",
            params={"version": version},
        )
