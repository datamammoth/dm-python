"""Exception classes for the DataMammoth SDK."""

from typing import Optional


class DataMammothError(Exception):
    """Base exception for all DataMammoth API errors."""

    def __init__(self, code: str, message: str, status: int, details: Optional[dict] = None):
        self.code = code
        self.message = message
        self.status = status
        self.details = details or {}
        super().__init__(f"[{code}] {message}")


class AuthError(DataMammothError):
    """Raised when authentication fails (401)."""

    pass


class NotFoundError(DataMammothError):
    """Raised when a resource is not found (404)."""

    pass


class ValidationError(DataMammothError):
    """Raised when request validation fails (422)."""

    def __init__(self, code: str, message: str, status: int, details: Optional[dict] = None):
        super().__init__(code, message, status, details)
        self.field_errors = details.get("errors", {}) if details else {}


class RateLimitError(DataMammothError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        code: str,
        message: str,
        status: int,
        details: Optional[dict] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(code, message, status, details)
        self.retry_after = retry_after


class PermissionError(DataMammothError):
    """Raised when the user lacks permission (403)."""

    pass


class ServerError(DataMammothError):
    """Raised on server-side errors (5xx)."""

    pass


def map_error(status: int, body: dict, retry_after: Optional[int] = None) -> DataMammothError:
    """Map an HTTP error status to the appropriate exception class."""
    error_data = body.get("error", {})
    code = error_data.get("code", "UNKNOWN_ERROR")
    message = error_data.get("message", "An unknown error occurred")
    details = error_data.get("details", {})

    if status == 401:
        return AuthError(code, message, status, details)
    elif status == 403:
        return PermissionError(code, message, status, details)
    elif status == 404:
        return NotFoundError(code, message, status, details)
    elif status == 422:
        return ValidationError(code, message, status, details)
    elif status == 429:
        return RateLimitError(code, message, status, details, retry_after=retry_after)
    elif status >= 500:
        return ServerError(code, message, status, details)
    else:
        return DataMammothError(code, message, status, details)
