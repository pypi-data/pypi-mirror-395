"""Custom exceptions for Mogu SDK"""

from typing import Any, Optional


class MoguAPIError(Exception):
    """Base exception for all Mogu API errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(MoguAPIError):
    """Raised when authentication fails (401)"""

    def __init__(self, message: str = "Authentication failed", **kwargs: Any) -> None:
        super().__init__(message, status_code=401, **kwargs)


class PermissionDeniedError(MoguAPIError):
    """Raised when user lacks required permissions (403)"""

    def __init__(
        self, message: str = "Permission denied", **kwargs: Any
    ) -> None:
        super().__init__(message, status_code=403, **kwargs)


class NotFoundError(MoguAPIError):
    """Raised when resource is not found (404)"""

    def __init__(self, message: str = "Resource not found", **kwargs: Any) -> None:
        super().__init__(message, status_code=404, **kwargs)


class ValidationError(MoguAPIError):
    """Raised when request validation fails (422)"""

    def __init__(self, message: str = "Validation error", **kwargs: Any) -> None:
        super().__init__(message, status_code=422, **kwargs)


class RateLimitError(MoguAPIError):
    """Raised when rate limit is exceeded (429)"""

    def __init__(
        self, message: str = "Rate limit exceeded", **kwargs: Any
    ) -> None:
        super().__init__(message, status_code=429, **kwargs)


class ServerError(MoguAPIError):
    """Raised when server encounters an error (5xx)"""

    def __init__(
        self, message: str = "Server error", status_code: int = 500, **kwargs: Any
    ) -> None:
        super().__init__(message, status_code=status_code, **kwargs)


class NetworkError(MoguAPIError):
    """Raised when network connection fails"""

    def __init__(
        self, message: str = "Network error occurred", **kwargs: Any
    ) -> None:
        super().__init__(message, **kwargs)


class TimeoutError(MoguAPIError):
    """Raised when request times out"""

    def __init__(self, message: str = "Request timed out", **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
