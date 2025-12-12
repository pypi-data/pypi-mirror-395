"""Custom exceptions for the OpenDota API wrapper."""

from typing import Optional


class OpenDotaError(Exception):
    """Base exception for OpenDota API errors."""
    pass


class OpenDotaAPIError(OpenDotaError):
    """Exception raised for API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class OpenDotaRateLimitError(OpenDotaAPIError):
    """Exception raised when rate limit is exceeded."""
    pass


class OpenDotaNotFoundError(OpenDotaAPIError):
    """Exception raised when resource is not found."""
    pass
