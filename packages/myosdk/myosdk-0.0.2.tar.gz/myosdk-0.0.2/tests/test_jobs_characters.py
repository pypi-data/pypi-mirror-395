"""Unit tests for Jobs.list and Characters resource wiring."""

from datetime import datetime


class DummyHTTPClient:
    """Minimal HTTP client stand-in to capture requests."""

    def __init__(self):
        self.calls = []

    def get(self, url, params=None, **kwargs):
        self.calls.append(("GET", url, params, kwargs))
        return {"url": url, "params": params}

    def post(self, url, params=None, **kwargs):
        self.calls.append(("POST", url, params, kwargs))
        return {"url": url, "params": params}


def test_jobs_list_builds_query_params():
    """Ensure list() passes through filters and pagination."""
    from myosdk.jobs import Jobs

    dummy = DummyHTTPClient()
    jobs = Jobs(dummy)

    created_after = datetime(2024, 1, 2, 3, 4, 5)

    result = jobs.list(
        status=["queued", "SUCCEEDED"],
        job_type="retarget",
        created_after=created_after,
        created_before="2024-02-01T00:00:00Z",
        run_id="run-123",
        has_output=True,
        input_asset_id="asset-123",
        limit=10,
        offset=5,
    )

    assert result["url"] == "/v1/jobs"
    params = result["params"]
    assert params["status"] == ["queued", "SUCCEEDED"]
    assert params["type"] == ["retarget"]
    assert params["created_after"] == created_after.isoformat()
    assert params["created_before"] == "2024-02-01T00:00:00Z"
    assert params["run_id"] == "run-123"
    assert params["has_output"] is True
    assert params["input_asset_id"] == "asset-123"
    assert params["limit"] == 10
    assert params["offset"] == 5


def test_characters_endpoints():
    """Verify characters resource routes and params."""
    from myosdk.characters import Characters

    dummy = DummyHTTPClient()
    characters = Characters(dummy)

    list_result = characters.list(name_contains="hero", has_ready_versions=True, limit=25)
    assert list_result["url"] == "/v1/characters"
    assert list_result["params"]["name_contains"] == "hero"
    assert list_result["params"]["has_ready_versions"] is True
    assert list_result["params"]["limit"] == 25

    detail = characters.get("char-123")
    assert detail["url"] == "/v1/characters/char-123"

    validate = characters.validate_manifest("char-123", "v1.0.0")
    assert validate["url"] == "/v1/characters/char-123/validate-manifest"
    assert validate["params"]["version"] == "v1.0.0"
