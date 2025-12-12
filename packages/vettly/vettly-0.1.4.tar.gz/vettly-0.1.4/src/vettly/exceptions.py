"""Vettly SDK exceptions."""

from typing import Any, Optional


class VettlyError(Exception):
    """Base exception for Vettly SDK errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class VettlyAPIError(VettlyError):
    """API request failed."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[Any] = None,
        code: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        self.code = code or "API_ERROR"
        super().__init__(message)


class VettlyAuthError(VettlyAPIError):
    """Authentication failed - invalid or missing API key."""

    def __init__(
        self,
        message: str = "Invalid API key",
        status_code: int = 401,
        response_body: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response_body, "AUTH_ERROR")


class VettlyRateLimitError(VettlyAPIError):
    """Rate limit exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int = 429,
        retry_after: Optional[int] = None,
        response_body: Optional[Any] = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code, response_body, "RATE_LIMIT_ERROR")


class VettlyQuotaError(VettlyAPIError):
    """Quota exceeded."""

    def __init__(
        self,
        message: str = "Quota exceeded",
        status_code: int = 429,
        quota: Optional[dict] = None,
        response_body: Optional[Any] = None,
    ) -> None:
        self.quota = quota
        super().__init__(message, status_code, response_body, "QUOTA_EXCEEDED")


class VettlyValidationError(VettlyAPIError):
    """Request validation failed."""

    def __init__(
        self,
        message: str = "Validation error",
        status_code: int = 422,
        errors: Optional[list] = None,
        response_body: Optional[Any] = None,
    ) -> None:
        self.errors = errors
        super().__init__(message, status_code, response_body, "VALIDATION_ERROR")


class VettlyServerError(VettlyAPIError):
    """Server error occurred."""

    def __init__(
        self,
        message: str = "Server error",
        status_code: int = 500,
        response_body: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response_body, "SERVER_ERROR")
