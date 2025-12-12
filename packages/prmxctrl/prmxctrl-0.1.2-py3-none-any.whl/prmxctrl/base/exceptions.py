"""
Proxmox SDK Exception Hierarchy

Custom exceptions for the prmxctrl SDK to provide clear error handling
and debugging information for Proxmox API interactions.
"""

from typing import Any


class ProxmoxError(Exception):
    """
    Base exception for all prmxctrl SDK errors.

    This is the root exception that all other SDK exceptions inherit from,
    allowing users to catch all SDK-related errors with a single except block.
    """

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        """
        Initialize the base Proxmox error.

        Args:
            message: Human-readable error description
            cause: Original exception that caused this error (if any)
        """
        super().__init__(message)
        self.message = message
        self.cause = cause

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.cause:
            return f"{self.message} (caused by: {self.cause})"
        return self.message


class ProxmoxAuthError(ProxmoxError):
    """
    Authentication-related errors.

    Raised when authentication fails, tokens expire, or credentials are invalid.
    This includes both password-based authentication and API token authentication.
    """

    def __init__(
        self,
        message: str = "Authentication failed",
        auth_method: str | None = None,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize authentication error.

        Args:
            message: Error description
            auth_method: Authentication method that failed ('password' or 'token')
            status_code: HTTP status code from the API response (if applicable)
            response_data: Parsed JSON response data containing error details (if applicable)
            cause: Original exception that caused this error
        """
        super().__init__(message, cause)
        self.auth_method = auth_method
        self.status_code = status_code
        self.response_data = response_data or {}


class ProxmoxConnectionError(ProxmoxError):
    """
    Network connection errors.

    Raised when unable to establish or maintain connection to Proxmox server.
    This includes DNS resolution failures, network timeouts, and SSL errors.
    """

    def __init__(
        self,
        message: str = "Connection failed",
        host: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize connection error.

        Args:
            message: Error description
            host: Proxmox server hostname/IP that failed to connect
            cause: Original exception that caused this error
        """
        super().__init__(message, cause)
        self.host = host


class ProxmoxTimeoutError(ProxmoxConnectionError):
    """
    Request timeout errors.

    Raised when API requests exceed the configured timeout limit.
    This is a subclass of ProxmoxConnectionError for more specific handling.
    """

    def __init__(
        self,
        message: str = "Request timed out",
        timeout_seconds: float | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize timeout error.

        Args:
            message: Error description
            timeout_seconds: Timeout value that was exceeded
            cause: Original exception that caused this error
        """
        super().__init__(message, host=None, cause=cause)
        self.timeout_seconds = timeout_seconds


class ProxmoxAPIError(ProxmoxError):
    """
    Proxmox API response errors.

    Raised when the Proxmox API returns an error response (4xx or 5xx status codes).
    Contains the HTTP status code and any error details from the API response.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: dict[str, Any] | None = None,
        response_body: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize API error.

        Args:
            message: Error description
            status_code: HTTP status code from the API response
            response_data: Parsed JSON response data containing error details
            response_body: Raw response body text (for non-JSON responses)
            cause: Original exception that caused this error
        """
        super().__init__(message, cause)
        self.status_code = status_code
        self.response_data = response_data or {}
        self.response_body = response_body

    @property
    def is_client_error(self) -> bool:
        """Return True if this is a 4xx client error."""
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        """Return True if this is a 5xx server error."""
        return 500 <= self.status_code < 600


class ProxmoxValidationError(ProxmoxError):
    """
    Data validation errors.

    Raised when input parameters fail Pydantic validation before sending to API.
    This helps catch invalid data early in the request pipeline.
    """

    def __init__(
        self,
        message: str,
        field_errors: list[Any] | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize validation error.

        Args:
            message: Error description
            field_errors: List of field-specific validation errors from Pydantic
            cause: Original exception that caused this error
        """
        super().__init__(message, cause)
        self.field_errors = field_errors or []

    @property
    def has_field_errors(self) -> bool:
        """Return True if there are specific field validation errors."""
        return len(self.field_errors) > 0
