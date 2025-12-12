"""Custom exceptions for Lenco SDK"""

from typing import Any


class LencoError(Exception):
    """Base exception for Lenco SDK errors"""

    def __init__(
        self,
        message: str,
        status_code: int = 0,
        error_code: str = "UNKNOWN_ERROR",
        response: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.response = response


class AuthenticationError(LencoError):
    """Raised when API authentication fails"""

    def __init__(self, message: str = "Invalid API key or unauthorized request") -> None:
        super().__init__(message, status_code=401, error_code="AUTHENTICATION_ERROR")


class ValidationError(LencoError):
    """Raised when request validation fails"""

    def __init__(
        self, message: str, response: dict[str, Any] | None = None
    ) -> None:
        error_code = response.get("errorCode", "VALIDATION_ERROR") if response else "VALIDATION_ERROR"
        super().__init__(message, status_code=400, error_code=error_code, response=response)


class NotFoundError(LencoError):
    """Raised when a resource is not found"""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class RateLimitError(LencoError):
    """Raised when rate limit is exceeded"""

    def __init__(
        self, message: str = "Rate limit exceeded", retry_after: int | None = None
    ) -> None:
        super().__init__(message, status_code=429, error_code="RATE_LIMIT")
        self.retry_after = retry_after


class ServerError(LencoError):
    """Raised when server returns 5xx error"""

    def __init__(self, message: str = "Internal server error") -> None:
        super().__init__(message, status_code=500, error_code="SERVER_ERROR")


class NetworkError(LencoError):
    """Raised when network error occurs"""

    def __init__(self, message: str = "Network error occurred") -> None:
        super().__init__(message, status_code=0, error_code="NETWORK_ERROR")
