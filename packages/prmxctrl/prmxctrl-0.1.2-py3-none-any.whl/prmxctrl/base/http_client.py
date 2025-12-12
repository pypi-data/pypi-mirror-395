"""
HTTP Client for Proxmox API communication.

This module provides the HTTPClient class that handles all communication
with the Proxmox VE API, including authentication, connection pooling,
and error handling.
"""

import asyncio
import json
from typing import Any, cast

import httpx

from .exceptions import (
    ProxmoxAPIError,
    ProxmoxAuthError,
    ProxmoxConnectionError,
)
from .types import (
    APIResponse,
    AuthToken,
    HTTPHeaders,
    Password,
    QueryParams,
    SSLVerifyMode,
    TimeoutSeconds,
    Username,
)


class HTTPClient:
    """
    Async HTTP client for Proxmox VE API communication.

    Handles authentication, connection pooling, CSRF tokens, and error handling.
    Designed as an async context manager for proper resource cleanup.

    Example:
        async with HTTPClient("https://proxmox:8006", "root@pam", "password") as client:
            response = await client.get("/nodes")
    """

    def __init__(
        self,
        host: str,
        user: Username,
        password: Password | None = None,
        token_name: str | None = None,
        token_value: AuthToken | None = None,
        verify_ssl: SSLVerifyMode = True,
        timeout: TimeoutSeconds = 30.0,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the HTTP client.

        Args:
            host: Proxmox server URL (e.g., "https://proxmox:8006")
            user: Username for authentication (required for both password and token auth)
            password: Password for authentication (for password auth)
            token_name: API token name (for token auth)
            token_value: API token value (for token auth)
            verify_ssl: SSL verification mode (True, False, or CA bundle path)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests

        Raises:
            ValueError: If authentication parameters are invalid
        """
        self.host = host.rstrip("/")
        self.user = user
        self.password = password
        self.token_name = token_name
        self.token_value = token_value
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.max_retries = max_retries

        # Validate authentication parameters
        self._validate_auth_params()

        # Internal state
        self._client: httpx.AsyncClient | None = None
        self._csrf_token: str | None = None
        self._ticket: str | None = None
        self._is_authenticated = False

    def _validate_auth_params(self) -> None:
        """Validate authentication parameters."""
        # User is required for both authentication methods
        if not self.user:
            raise ValueError("User is required for authentication")

        # Check password auth
        has_password_auth = self.password is not None
        # Check token auth
        has_token_auth = self.token_name is not None and self.token_value is not None

        if not (has_password_auth or has_token_auth):
            raise ValueError(
                "Must provide either password or (token_name + token_value) for authentication"
            )

        if has_password_auth and has_token_auth:
            raise ValueError("Cannot use both password and token authentication simultaneously")

    async def __aenter__(self) -> "HTTPClient":
        """Async context manager entry."""
        await self._setup_client()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self._cleanup_client()

    async def _setup_client(self) -> None:
        """Set up the HTTP client and authenticate."""
        # Create httpx client with connection pooling
        self._client = httpx.AsyncClient(
            base_url=self.host,
            verify=self.verify_ssl,
            timeout=self.timeout,
            follow_redirects=True,
        )

        # Authenticate
        await self._authenticate()

    async def _cleanup_client(self) -> None:
        """Clean up the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

        # Reset authentication state
        self._csrf_token = None
        self._ticket = None
        self._is_authenticated = False

    async def _authenticate(self) -> None:
        """Authenticate with the Proxmox server."""
        if self.user and self.password:
            await self._authenticate_ticket()
        elif self.token_name and self.token_value:
            await self._authenticate_token()
        else:
            raise ProxmoxAuthError("No valid authentication method configured")

        self._is_authenticated = True

    async def _authenticate_ticket(self) -> None:
        """Authenticate using username/password (ticket method)."""
        if not self._client or not self.user or not self.password:
            raise ProxmoxAuthError("Client not initialized or missing credentials")

        try:
            response = await self._client.post(
                "/api2/json/access/ticket",
                data={
                    "username": self.user,
                    "password": self.password,
                },
            )

            response.raise_for_status()
            data = response.json()

            if "data" not in data or "ticket" not in data["data"]:
                raise ProxmoxAuthError("Invalid authentication response")

            self._ticket = data["data"]["ticket"]
            self._csrf_token = data["data"].get("CSRFPreventionToken")

            # Set authentication cookie - let httpx handle domain/path matching automatically
            assert self._ticket is not None  # Should be set above
            self._client.cookies.set("PVEAuthCookie", self._ticket)

        except Exception as e:
            if hasattr(e, "response"):
                # HTTP error with response
                raise ProxmoxAuthError(
                    f"Authentication failed: {e.response.status_code}",
                    auth_method="password",
                    cause=e,
                ) from e
            else:
                raise ProxmoxAuthError(
                    "Authentication request failed", auth_method="password", cause=e
                ) from e

    async def _authenticate_token(self) -> None:
        """Authenticate using API token."""
        if not self._client or not self.token_name or not self.token_value:
            raise ProxmoxAuthError("Client not initialized or missing token")

        # For token auth, we set the Authorization header
        # Format: "PVEAPIToken=USER@REALM!TOKENID=UUID"
        # We need to extract realm from user if provided, otherwise assume 'pam'
        if self.user:
            # Extract realm from user (format: user@realm)
            if "@" in self.user:
                user_part, realm = self.user.split("@", 1)
            else:
                user_part = self.user
                realm = "pam"
        else:
            raise ProxmoxAuthError("User must be provided for token authentication")

        auth_header = f"PVEAPIToken={user_part}@{realm}!{self.token_name}={self.token_value}"
        self._client.headers["Authorization"] = auth_header

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: QueryParams | None = None,
        data: dict[str, Any] | str | None = None,
        json_data: dict[str, Any] | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """
        Make an HTTP request to the Proxmox API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path (without /api2/json prefix)
            params: Query parameters
            data: Form data
            json_data: JSON data to send
            headers: Additional headers

        Returns:
            APIResponse: Parsed response data

        Raises:
            ProxmoxConnectionError: Connection/network errors
            ProxmoxAuthError: Authentication errors
            ProxmoxAPIError: API errors (4xx/5xx)
            ProxmoxTimeoutError: Timeout errors
        """
        if not self._client:
            raise ProxmoxConnectionError("HTTP client not initialized", host=self.host)

        # Ensure path starts with /
        if not path.startswith("/"):
            path = "/" + path

        # Build full API path
        api_path = f"/api2/json{path}"

        # Prepare request data
        request_kwargs: dict[str, Any] = {
            "method": method,
            "url": api_path,
            "params": params,
            "headers": headers or {},
        }

        if json_data is not None:
            request_kwargs["json"] = json_data
        elif data is not None:
            if isinstance(data, dict):
                request_kwargs["data"] = data
            else:
                request_kwargs["content"] = data

        # Add CSRF token for non-GET requests if available
        if self._csrf_token:
            request_kwargs["headers"]["CSRFPreventionToken"] = self._csrf_token

        last_exception: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.request(**request_kwargs)
                return await self._handle_response(response)

            except Exception as e:
                if hasattr(e, "response"):
                    # HTTP error with response
                    return await self._handle_response(e.response)
                else:
                    # Non-HTTP error
                    last_exception = e
                    if attempt < self.max_retries:
                        await asyncio.sleep(2**attempt)  # Exponential backoff
                        continue
                    raise ProxmoxConnectionError(
                        f"Request failed after {self.max_retries + 1} attempts",
                        host=self.host,
                        cause=e,
                    ) from e

        # This should never be reached, but for type safety
        assert last_exception is not None
        raise ProxmoxConnectionError(
            f"Request failed after {self.max_retries + 1} attempts",
            host=self.host,
            cause=last_exception,
        )

    async def _handle_response(self, response: httpx.Response) -> APIResponse:
        """
        Handle HTTP response and parse JSON data.

        Args:
            response: HTTP response object

        Returns:
            APIResponse: Parsed response data

        Raises:
            ProxmoxAPIError: For API errors (4xx/5xx)
            ProxmoxAuthError: For authentication errors (401)
        """
        try:
            # Try to parse JSON response
            data = cast(dict[str, Any], response.json())
        except json.JSONDecodeError as err:
            # Non-JSON response
            if response.is_success:
                # Success but no JSON - return empty dict
                return {}
            else:
                # Error without JSON
                raise ProxmoxAPIError(
                    f"API returned {response.status_code} with non-JSON response",
                    status_code=response.status_code,
                    response_body=response.text,
                ) from err

        # Check for API errors
        if not response.is_success:
            # Extract error details from response
            error_data = data.get("data", {})
            error_message = error_data.get("message", f"API error: {response.status_code}")

            if response.status_code == 401:
                raise ProxmoxAuthError(
                    f"Authentication failed: {error_message}",
                    status_code=response.status_code,
                    response_data=error_data,
                )
            else:
                raise ProxmoxAPIError(
                    error_message,
                    status_code=response.status_code,
                    response_data=error_data,
                )

        # Success response
        return cast(APIResponse, data.get("data", {}))

    # Convenience methods
    async def get(
        self,
        path: str,
        *,
        params: QueryParams | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """Make a GET request."""
        return await self.request("GET", path, params=params, headers=headers)

    async def post(
        self,
        path: str,
        *,
        params: QueryParams | None = None,
        data: dict[str, Any] | str | None = None,
        json_data: dict[str, Any] | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """Make a POST request."""
        return await self.request(
            "POST", path, params=params, data=data, json_data=json_data, headers=headers
        )

    async def put(
        self,
        path: str,
        *,
        params: QueryParams | None = None,
        data: dict[str, Any] | str | None = None,
        json_data: dict[str, Any] | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """Make a PUT request."""
        return await self.request(
            "PUT", path, params=params, data=data, json_data=json_data, headers=headers
        )

    async def delete(
        self,
        path: str,
        *,
        params: QueryParams | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """Make a DELETE request."""
        return await self.request("DELETE", path, params=params, headers=headers)
