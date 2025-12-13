"""Custom exceptions for the VERDICT SDK."""


class VerdictAPIError(Exception):
    """Base exception for all VERDICT API errors."""
    pass


class VerdictAuthError(VerdictAPIError):
    """Raised when authentication fails (invalid API keys)."""
    pass


class VerdictRateLimitError(VerdictAPIError):
    """Raised when rate limit is exceeded."""
    pass


class VerdictValidationError(VerdictAPIError):
    """Raised when request validation fails."""
    pass


class VerdictConnectionError(VerdictAPIError):
    """Raised when connection to VERDICT API fails."""
    pass
