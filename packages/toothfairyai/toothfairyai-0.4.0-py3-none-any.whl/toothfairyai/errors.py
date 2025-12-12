"""Custom error classes for the ToothFairyAI SDK."""

from typing import Any, Optional


class ToothFairyError(Exception):
    """Base exception for ToothFairyAI SDK errors."""

    def __init__(
        self,
        message: str,
        code: str = "UNKNOWN_ERROR",
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ):
        """Initialize a ToothFairyError.

        Args:
            message: Human-readable error message.
            code: Error code identifying the type of error.
            status_code: HTTP status code if applicable.
            response: Full API response data if available.
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        """Return string representation of the error."""
        parts = [self.message]
        if self.code:
            parts.append(f"(code: {self.code})")
        if self.status_code:
            parts.append(f"(status: {self.status_code})")
        return " ".join(parts)

    def __repr__(self) -> str:
        """Return detailed representation of the error."""
        return (
            f"ToothFairyError("
            f"message={self.message!r}, "
            f"code={self.code!r}, "
            f"status_code={self.status_code!r})"
        )


class MissingApiKeyError(ToothFairyError):
    """Raised when the API key is not provided."""

    def __init__(self, message: str = "API key is required"):
        super().__init__(message, code="MISSING_API_KEY")


class MissingWorkspaceIdError(ToothFairyError):
    """Raised when the workspace ID is not provided."""

    def __init__(self, message: str = "Workspace ID is required"):
        super().__init__(message, code="MISSING_WORKSPACE_ID")


class ApiError(ToothFairyError):
    """Raised when an API request fails."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ):
        super().__init__(
            message,
            code="API_ERROR",
            status_code=status_code,
            response=response,
        )


class NetworkError(ToothFairyError):
    """Raised when a network error occurs."""

    def __init__(self, message: str, response: Optional[Any] = None):
        super().__init__(message, code="NETWORK_ERROR", response=response)


class ValidationError(ToothFairyError):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class StreamError(ToothFairyError):
    """Raised when a streaming error occurs."""

    def __init__(self, message: str, response: Optional[Any] = None):
        super().__init__(message, code="STREAM_ERROR", response=response)


class JsonDecodeError(ToothFairyError):
    """Raised when JSON decoding fails."""

    def __init__(self, message: str, response: Optional[Any] = None):
        super().__init__(message, code="JSON_DECODE_ERROR", response=response)


class FileSizeError(ToothFairyError):
    """Raised when a file exceeds the maximum size limit."""

    def __init__(self, filename: str, size_mb: float, max_size_mb: float = 15):
        message = (
            f"File '{filename}' ({size_mb:.2f} MB) exceeds "
            f"the maximum allowed size of {max_size_mb} MB"
        )
        super().__init__(message, code="FILE_SIZE_ERROR")


class FileNotFoundError(ToothFairyError):
    """Raised when a file is not found."""

    def __init__(self, filename: str):
        message = f"File not found: {filename}"
        super().__init__(message, code="FILE_NOT_FOUND")
