"""Custom exceptions for the SDK."""


class APIError(Exception):
    """Base exception for all API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(APIError):
    """Raised when authentication fails (401)."""

    def __init__(
        self, message: str = "Authentication failed", response_data: dict | None = None
    ):
        super().__init__(message, status_code=401, response_data=response_data)


class NotFoundError(APIError):
    """Raised when a resource is not found (404)."""

    def __init__(
        self, message: str = "Resource not found", response_data: dict | None = None
    ):
        super().__init__(message, status_code=404, response_data=response_data)


class ValidationError(APIError):
    """Raised when request validation fails (400)."""

    def __init__(
        self, message: str = "Validation error", response_data: dict | None = None
    ):
        super().__init__(message, status_code=400, response_data=response_data)


class RateLimitError(APIError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
        response_data: dict | None = None,
    ):
        super().__init__(message, status_code=429, response_data=response_data)
        self.retry_after = retry_after


class ServerError(APIError):
    """Raised when server returns 5xx error."""

    def __init__(
        self,
        message: str = "Server error",
        status_code: int = 500,
        response_data: dict | None = None,
    ):
        super().__init__(message, status_code=status_code, response_data=response_data)
