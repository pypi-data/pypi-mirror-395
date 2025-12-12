"""
Base class for all Proxmox API endpoints.

This module provides the EndpointBase class that all generated endpoint classes
inherit from. It handles path building, HTTP method delegation, and response parsing.
"""

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from .types import APIResponse, HTTPHeaders, QueryParams

if TYPE_CHECKING:
    from .http_client import HTTPClient


class EndpointBase:
    """
    Base class for all Proxmox API endpoints.

    Provides common functionality for path building, HTTP method delegation,
    and response parsing. All generated endpoint classes inherit from this.

    Example:
        class NodesEndpoint(EndpointBase):
            def __init__(self, client, path="/nodes"):
                super().__init__(client, path)

            def __call__(self, node: str) -> "NodeItemEndpoint":
                return NodeItemEndpoint(self._client, f"{self._path}/{quote(node)}")
    """

    def __init__(self, client: "HTTPClient", path: str) -> None:
        """
        Initialize the endpoint.

        Args:
            client: HTTP client instance for making requests
            path: API path for this endpoint (e.g., "/nodes")
        """
        self._client = client
        self._path = path.rstrip("/")

    def _build_path(self, *segments: str) -> str:
        """
        Build a complete path by appending segments to the base path.

        Args:
            *segments: Path segments to append

        Returns:
            Complete API path

        Example:
            endpoint._path = "/nodes"
            endpoint._build_path("pve1", "qemu", "100")  # "/nodes/pve1/qemu/100"
        """
        if not segments:
            return self._path

        # URL-encode each segment and join with "/"
        encoded_segments = [quote(str(segment), safe="") for segment in segments]
        return f"{self._path}/{'/'.join(encoded_segments)}"

    def _build_url(self, *segments: str) -> str:
        """
        Build a complete URL by appending segments to the base path.

        Args:
            *segments: Path segments to append

        Returns:
            Complete API URL path

        Example:
            endpoint._path = "/nodes"
            endpoint._build_url("pve1", "status")  # "/nodes/pve1/status"
        """
        return self._build_path(*segments)

    async def _get(
        self,
        path: str | None = None,
        params: QueryParams | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """
        Make a GET request.

        Args:
            path: Optional path to append to endpoint path
            params: Query parameters
            headers: Additional headers

        Returns:
            API response data
        """
        url = self._build_url(*(path.split("/") if path else []))
        return await self._client.get(url, params=params, headers=headers)

    async def _post(
        self,
        path: str | None = None,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """
        Make a POST request.

        Args:
            path: Optional path to append to endpoint path
            data: Form data
            json_data: JSON request body
            headers: Additional headers

        Returns:
            API response data
        """
        url = self._build_url(*(path.split("/") if path else []))
        return await self._client.post(url, data=data, json_data=json_data, headers=headers)

    async def _put(
        self,
        path: str | None = None,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """
        Make a PUT request.

        Args:
            path: Optional path to append to endpoint path
            data: Form data
            json_data: JSON request body
            headers: Additional headers

        Returns:
            API response data
        """
        url = self._build_url(*(path.split("/") if path else []))
        return await self._client.put(url, data=data, json_data=json_data, headers=headers)

    async def _delete(
        self,
        path: str | None = None,
        params: QueryParams | None = None,
        headers: HTTPHeaders | None = None,
    ) -> APIResponse:
        """
        Make a DELETE request.

        Args:
            path: Optional path to append to endpoint path
            params: Query parameters
            headers: Additional headers

        Returns:
            API response data
        """
        url = self._build_url(*(path.split("/") if path else []))
        return await self._client.delete(url, params=params, headers=headers)

    def _prepare_params(
        self, params_dict: dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Prepare parameters for API requests.

        This is a helper method that can be overridden by subclasses
        to customize parameter preparation (e.g., converting Pydantic models).

        Args:
            params_dict: Parameter dictionary
            **kwargs: Additional parameters

        Returns:
            Prepared parameter dictionary
        """
        result = params_dict or {}
        result.update(kwargs)
        return result

    def _convert_response(
        self, response: APIResponse, response_type: type | None = None
    ) -> APIResponse | Any:
        """
        Convert API response to the appropriate type.

        This is a helper method that can be overridden by subclasses
        to customize response conversion (e.g., creating Pydantic models).

        Args:
            response: Raw API response
            response_type: Expected response type (if known)

        Returns:
            Converted response
        """
        return response

    @property
    def path(self) -> str:
        """Get the current endpoint path."""
        return self._path

    @property
    def client(self) -> "HTTPClient":
        """Get the HTTP client instance."""
        return self._client
