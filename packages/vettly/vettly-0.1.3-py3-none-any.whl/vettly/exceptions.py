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
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class VettlyAuthError(VettlyAPIError):
    """Authentication failed - invalid or missing API key."""

    pass


class VettlyRateLimitError(VettlyAPIError):
    """Rate limit exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, **kwargs)


class VettlyValidationError(VettlyAPIError):
    """Request validation failed."""

    pass
