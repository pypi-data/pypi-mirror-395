"""Exception classes for MemoryStack SDK"""


class MemoryStackError(Exception):
    """Base exception for MemoryStack SDK"""
    
    def __init__(self, message: str, status_code: int = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class AuthenticationError(MemoryStackError):
    """Raised when authentication fails"""
    pass


class RateLimitError(MemoryStackError):
    """Raised when rate limit is exceeded"""
    
    def __init__(self, message: str, status_code: int = None, details: dict = None,
                 limit: int = None, remaining: int = None, reset: int = None):
        super().__init__(message, status_code, details)
        self.limit = limit
        self.remaining = remaining
        self.reset = reset


class ValidationError(MemoryStackError):
    """Raised when request validation fails"""
    pass


class NotFoundError(MemoryStackError):
    """Raised when a resource is not found (404)"""
    pass


class NetworkError(MemoryStackError):
    """Raised when a network error occurs"""
    
    def __init__(self, message: str, status_code: int = None, details: dict = None,
                 original_error: Exception = None):
        super().__init__(message, status_code, details)
        self.original_error = original_error


