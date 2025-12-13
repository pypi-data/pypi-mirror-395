"""
Error classes for Memory OS SDK
"""

from typing import Any, Optional


class MemoryStackError(Exception):
    """Base error class for Memory OS SDK"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class AuthenticationError(MemoryStackError):
    """Authentication error (401)"""

    def __init__(self, message: str = "Invalid or missing API key", details: Optional[Any] = None):
        super().__init__(message, 401, details)


class RateLimitError(MemoryStackError):
    """Rate limit exceeded error (429)"""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        limit: Optional[int] = None,
        remaining: Optional[int] = None,
        reset: Optional[int] = None,
    ):
        super().__init__(message, 429)
        self.limit = limit
        self.remaining = remaining
        self.reset = reset


class ValidationError(MemoryStackError):
    """Validation error (400)"""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message, 400, details)


class NotFoundError(MemoryStackError):
    """Not found error (404)"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class NetworkError(MemoryStackError):
    """Network error"""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message, details=original_error)
        self.original_error = original_error


