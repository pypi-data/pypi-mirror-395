"""Basic tests for the SDK client."""


# Note: These are placeholder tests. Real integration tests would require
# a running API server and proper test fixtures.


def test_client_initialization():
    """Test that client can be initialized."""
    from myosdk import Client

    client = Client(api_key="test_key", base_url="http://localhost:8000")
    assert client._http.api_key == "test_key"
    assert client._http.base_url == "http://localhost:8000"
    assert client.assets is not None
    assert client.jobs is not None
    assert client.characters is not None
    client.close()


def test_client_context_manager():
    """Test that client works as a context manager."""
    from myosdk import Client

    with Client(api_key="test_key") as client:
        assert client._http is not None
    # Client should be closed after context


def test_exceptions():
    """Test that exceptions are importable."""
    from myosdk import (
        APIError,
        AuthenticationError,
        NotFoundError,
        RateLimitError,
        ServerError,
        ValidationError,
    )

    assert issubclass(AuthenticationError, APIError)
    assert issubclass(NotFoundError, APIError)
    assert issubclass(ValidationError, APIError)
    assert issubclass(RateLimitError, APIError)
    assert issubclass(ServerError, APIError)
