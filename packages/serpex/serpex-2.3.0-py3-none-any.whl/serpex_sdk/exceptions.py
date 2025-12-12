"""
Exceptions for the Serpex SERP API Python SDK.
"""


class SerpApiException(Exception):
    """Base exception for SERP API errors."""

    def __init__(self, message: str, status_code: int = None, details: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}

    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {super().__str__()}"
        return super().__str__()


class AuthenticationError(SerpApiException):
    """Raised when authentication fails."""
    pass


class RateLimitError(SerpApiException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class InsufficientCreditsError(SerpApiException):
    """Raised when there are insufficient credits."""
    pass


class ValidationError(SerpApiException):
    """Raised when request validation fails."""
    pass