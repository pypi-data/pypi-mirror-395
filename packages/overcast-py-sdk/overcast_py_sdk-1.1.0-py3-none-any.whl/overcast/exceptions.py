"""
Overcast SDK Exceptions
Custom exceptions for better error handling and debugging.
"""


class OvercastError(Exception):
    """Base exception for all Overcast SDK errors."""
    pass


class OvercastAuthError(OvercastError):
    """Raised when authentication fails (invalid API key)."""
    pass


class OvercastConnectionError(OvercastError):
    """Raised when there's a connection issue with Overcast API."""
    pass


class OvercastValidationError(OvercastError):
    """Raised when request validation fails."""
    pass
