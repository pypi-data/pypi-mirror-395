"""
Exception Classes Unit Tests
"""

import pytest
from memorystack.exceptions import (
    MemoryStackError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    NetworkError,
)


class TestMemoryStackError:
    """Test MemoryStackError base class"""

    def test_error_with_message(self):
        """Test error creation with message only"""
        error = MemoryStackError("Test error")
        assert isinstance(error, Exception)
        assert error.message == "Test error"
        assert error.status_code is None
        assert error.details is None

    def test_error_with_status_code(self):
        """Test error creation with status code"""
        error = MemoryStackError("Test error", status_code=500)
        assert error.status_code == 500

    def test_error_with_details(self):
        """Test error creation with details"""
        error = MemoryStackError("Test error", details={"field": "value"})
        assert error.details == {"field": "value"}


class TestAuthenticationError:
    """Test AuthenticationError class"""

    def test_authentication_error(self):
        """Test authentication error creation"""
        error = AuthenticationError("Invalid API key")
        assert isinstance(error, MemoryStackError)
        assert error.message == "Invalid API key"


class TestRateLimitError:
    """Test RateLimitError class"""

    def test_rate_limit_error_with_headers(self):
        """Test rate limit error with headers"""
        error = RateLimitError(
            "Rate limit exceeded",
            limit=100,
            remaining=0,
            reset=1234567890,
        )
        assert isinstance(error, MemoryStackError)
        assert error.limit == 100
        assert error.remaining == 0
        assert error.reset == 1234567890

    def test_rate_limit_error_without_headers(self):
        """Test rate limit error without headers"""
        error = RateLimitError("Rate limit exceeded")
        assert error.limit is None
        assert error.remaining is None
        assert error.reset is None


class TestValidationError:
    """Test ValidationError class"""

    def test_validation_error(self):
        """Test validation error creation"""
        error = ValidationError("Validation failed", details={"field": "content"})
        assert isinstance(error, MemoryStackError)
        assert error.details == {"field": "content"}


class TestNotFoundError:
    """Test NotFoundError class"""

    def test_not_found_error(self):
        """Test not found error creation"""
        error = NotFoundError("Resource not found")
        assert isinstance(error, MemoryStackError)
        assert error.message == "Resource not found"


class TestNetworkError:
    """Test NetworkError class"""

    def test_network_error(self):
        """Test network error creation"""
        original_error = Exception("Connection failed")
        error = NetworkError("Network request failed", original_error=original_error)
        assert isinstance(error, MemoryStackError)
        assert error.original_error == original_error

    def test_network_error_without_original(self):
        """Test network error without original error"""
        error = NetworkError("Network request failed")
        assert error.original_error is None





