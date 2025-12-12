"""HTTP client with retry logic and exception handling."""

import time
from typing import Any

import httpx

from myosdk.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class HTTPClient:
    """HTTP client with retry logic and exception mapping."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:8000",
        timeout: float = 30.0,
    ):
        """Initialize HTTP client.

        Args:
            api_key: API key for authentication
            base_url: Base URL of the API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "X-Api-Key": api_key,
                "Content-Type": "application/json",
            },
        )

    def _parse_retry_after(self, headers: dict) -> int | None:
        """Parse Retry-After header value.

        Args:
            headers: Response headers

        Returns:
            Seconds to wait, or None if header not present
        """
        retry_after = headers.get("Retry-After")
        if retry_after is None:
            return None
        try:
            return int(retry_after)
        except (ValueError, TypeError):
            return None

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Raise appropriate exception based on status code.

        Args:
            response: HTTP response

        Raises:
            APIError: Appropriate exception based on status code
        """
        if response.is_success:
            return

        try:
            response_data = response.json()
        except Exception:
            response_data = {"detail": response.text}

        status_code = response.status_code
        message = response_data.get(
            "detail", response_data.get("message", f"HTTP {status_code}")
        )

        if status_code == 401:
            raise AuthenticationError(message, response_data)
        elif status_code == 404:
            raise NotFoundError(message, response_data)
        elif status_code in (
            400,
            422,
        ):  # 422 is Unprocessable Entity (validation error)
            raise ValidationError(message, response_data)
        elif status_code == 429:
            retry_after = self._parse_retry_after(response.headers)
            raise RateLimitError(
                message, retry_after=retry_after, response_data=response_data
            )
        elif 500 <= status_code < 600:
            raise ServerError(
                message, status_code=status_code, response_data=response_data
            )
        else:
            raise APIError(
                message, status_code=status_code, response_data=response_data
            )

    def _request_with_retry(
        self,
        method: str,
        url: str,
        max_retries: int = 3,
        initial_backoff: float = 1.0,
        max_backoff: float = 60.0,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make HTTP request with retry logic.

        Args:
            method: HTTP method
            url: Request URL
            max_retries: Maximum number of retries
            initial_backoff: Initial backoff time in seconds
            max_backoff: Maximum backoff time in seconds
            **kwargs: Additional arguments to pass to httpx request

        Returns:
            HTTP response

        Raises:
            APIError: If request fails after retries
        """
        last_exception: Exception | None = None

        for attempt in range(max_retries + 1):
            try:
                response = self.client.request(method, url, **kwargs)
                self._raise_for_status(response)
                return response
            except RateLimitError as e:
                last_exception = e
                if attempt < max_retries:
                    wait_time = e.retry_after or min(
                        initial_backoff * (2**attempt), max_backoff
                    )
                    time.sleep(wait_time)
                    continue
                raise
            except (ServerError, httpx.NetworkError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt < max_retries:
                    wait_time = min(initial_backoff * (2**attempt), max_backoff)
                    time.sleep(wait_time)
                    continue
                raise
            except APIError:
                # Don't retry on client errors (4xx except 429)
                raise

        # Should never reach here, but just in case
        if last_exception:
            raise last_exception
        raise APIError("Request failed after retries")

    def get(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """Make GET request.

        Args:
            url: Request URL
            **kwargs: Additional arguments

        Returns:
            JSON response as dict
        """
        response = self._request_with_retry("GET", url, **kwargs)
        return response.json()

    def post(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """Make POST request.

        Args:
            url: Request URL
            **kwargs: Additional arguments

        Returns:
            JSON response as dict
        """
        response = self._request_with_retry("POST", url, **kwargs)
        return response.json()

    def delete(self, url: str, **kwargs: Any) -> dict[str, Any] | None:
        """Make DELETE request.

        Args:
            url: Request URL
            **kwargs: Additional arguments

        Returns:
            JSON response as dict if available, None otherwise
        """
        response = self._request_with_retry("DELETE", url, **kwargs)
        # Some DELETE endpoints return JSON (e.g., job cancellation), others return 204 No Content (e.g., asset deletion)
        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except Exception:
            return None

    def post_multipart(
        self, url: str, data: dict[str, str], files: dict[str, Any]
    ) -> httpx.Response:
        """Make multipart POST request (for file uploads).

        Args:
            url: Request URL (presigned POST URL - no auth needed)
            data: Form data fields (from presigned POST - includes key, policy, signature, etc.)
            files: File data (dict with file tuples like {"file": (filename, file_obj, content_type)})

        Returns:
            HTTP response
        """
        # For presigned POST URLs, we should NOT send auth headers or use the authenticated client
        # The presigned URL itself contains the authentication in the form fields
        # We need to use a clean httpx client without default headers

        # Ensure file pointer is at the beginning for all files
        for file_tuple in files.values():
            if isinstance(file_tuple, tuple) and len(file_tuple) >= 2:
                file_obj = file_tuple[1]
                if hasattr(file_obj, "seek"):
                    file_obj.seek(0)

        # Use httpx directly without auth headers (presigned URLs don't need them)
        # Don't use retry mechanism here as presigned URLs expire quickly
        response = httpx.post(
            url,
            data=data,
            files=files,
            timeout=self.timeout,
            follow_redirects=False,
        )

        # Raise for status if not successful
        self._raise_for_status(response)
        return response

    def get_raw(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make GET request and return raw response (for downloads).

        Args:
            url: Request URL (may be presigned GET URL)
            **kwargs: Additional arguments

        Returns:
            Raw HTTP response
        """
        # If this is a presigned URL (contains signature in query params),
        # don't use authenticated client as it will break the signature
        is_presigned = "signature" in url.lower() or "x-amz-signature" in url.lower()

        if is_presigned:
            # Use httpx directly without auth headers for presigned URLs
            response = httpx.get(
                url, timeout=self.timeout, follow_redirects=True, **kwargs
            )
            self._raise_for_status(response)
            return response
        else:
            response = self._request_with_retry("GET", url, **kwargs)
            return response

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
