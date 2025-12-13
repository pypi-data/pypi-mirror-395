"""Custom exceptions for the pyine package."""


class PyINEError(Exception):
    """Base exception for all pyine errors."""

    pass


class APIError(PyINEError):
    """Raised when the INE API returns an error response."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(APIError):
    """Raised when a requested resource is not found (404)."""

    pass


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""

    pass


class ValidationError(PyINEError):
    """Raised when input validation fails."""

    pass


class DataParsingError(PyINEError):
    """Raised when response data cannot be parsed."""

    pass
