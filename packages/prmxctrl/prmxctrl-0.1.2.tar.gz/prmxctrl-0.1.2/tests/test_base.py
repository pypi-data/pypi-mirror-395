"""
Basic tests for the base framework components.

This module contains unit tests for the exception classes, types, HTTP client,
and endpoint base classes.
"""

import pytest

from prmxctrl.base.endpoint_base import EndpointBase

# Test imports
from prmxctrl.base.exceptions import (
    ProxmoxAPIError,
    ProxmoxAuthError,
    ProxmoxConnectionError,
    ProxmoxError,
    ProxmoxTimeoutError,
    ProxmoxValidationError,
)
from prmxctrl.base.http_client import HTTPClient
from prmxctrl.base.types import (
    APIResponse,
    AuthToken,
    JSONValue,
    Password,
    ProxmoxNode,
    ProxmoxVMID,
    Username,
)


class TestExceptions:
    """Test the custom exception hierarchy."""

    def test_proxmox_error_creation(self):
        """Test basic ProxmoxError creation."""
        error = ProxmoxError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"

    def test_proxmox_auth_error(self):
        """Test ProxmoxAuthError with auth method."""
        error = ProxmoxAuthError("Auth failed", auth_method="password")
        assert "Auth failed" in str(error)
        assert error.auth_method == "password"

    def test_proxmox_api_error(self):
        """Test ProxmoxAPIError with status code."""
        error = ProxmoxAPIError("API error", status_code=404)
        assert "API error" in str(error)
        assert error.status_code == 404

    def test_proxmox_connection_error(self):
        """Test ProxmoxConnectionError with host."""
        error = ProxmoxConnectionError("Connection failed", host="example.com")
        assert "Connection failed" in str(error)
        assert error.host == "example.com"

    def test_proxmox_timeout_error(self):
        """Test ProxmoxTimeoutError with timeout."""
        error = ProxmoxTimeoutError("Timeout", timeout_seconds=30.0)
        assert "Timeout" in str(error)
        assert error.timeout_seconds == 30.0

    def test_proxmox_validation_error(self):
        """Test ProxmoxValidationError with field errors."""
        field_errors = {"name": ["Required field"], "age": ["Must be positive"]}
        error = ProxmoxValidationError("Validation failed", field_errors=field_errors)
        assert "Validation failed" in str(error)
        assert error.field_errors == field_errors


class TestTypes:
    """Test type aliases and validation."""

    def test_type_aliases(self):
        """Test that type aliases work as expected."""
        # These should not raise type errors
        node: ProxmoxNode = "node1"
        vmid: ProxmoxVMID = 100
        username: Username = "root@pam"
        password: Password = "secret"
        token: AuthToken = "token123"

        assert node == "node1"
        assert vmid == 100
        assert username == "root@pam"
        assert password == "secret"
        assert token == "token123"

    def test_api_response_type(self):
        """Test APIResponse type structure."""
        response: APIResponse = {"data": {"key": "value"}}
        assert response["data"]["key"] == "value"

    def test_json_value_type(self):
        """Test JSONValue type accepts various JSON-compatible values."""
        values: list[JSONValue] = [
            "string",
            42,
            3.14,
            True,
            None,
            ["list", "of", "values"],
            {"key": "value", "number": 123},
        ]
        assert len(values) == 7


class TestHTTPClient:
    """Test HTTPClient initialization and basic functionality."""

    def test_http_client_init_password_auth(self):
        """Test HTTPClient initialization with password auth."""
        client = HTTPClient(
            host="https://proxmox:8006",
            user="root@pam",
            password="secret",
            verify_ssl=True,
            timeout=30.0,
            max_retries=3,
        )

        assert client.host == "https://proxmox:8006"
        assert client.user == "root@pam"
        assert client.password == "secret"
        assert client.verify_ssl is True
        assert client.timeout == 30.0
        assert client.max_retries == 3

    def test_http_client_init_token_auth(self):
        """Test HTTPClient initialization with token auth."""
        client = HTTPClient(
            host="https://proxmox:8006",
            user="root@pam",
            token_name="mytoken",
            token_value="token123",
        )

        assert client.host == "https://proxmox:8006"
        assert client.user == "root@pam"
        assert client.token_name == "mytoken"
        assert client.token_value == "token123"

    def test_http_client_invalid_auth(self):
        """Test HTTPClient rejects invalid auth combinations."""
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'user'"):
            HTTPClient(host="https://proxmox:8006")

        with pytest.raises(ValueError, match="Cannot use both"):
            HTTPClient(
                host="https://proxmox:8006",
                user="root@pam",
                password="secret",
                token_name="mytoken",
                token_value="token123",
            )


class TestEndpointBase:
    """Test EndpointBase functionality."""

    def test_endpoint_base_init(self):
        """Test EndpointBase initialization."""

        # Mock HTTPClient
        class MockClient:
            pass

        client = MockClient()
        endpoint = EndpointBase(client, "/test")

        assert endpoint._client == client
        assert endpoint._path == "/test"

    def test_build_path_no_params(self):
        """Test path building without parameters."""

        class MockClient:
            pass

        client = MockClient()
        endpoint = EndpointBase(client, "/nodes")

        path = endpoint._build_path()
        assert path == "/nodes"

    def test_build_path_with_params(self):
        """Test path building with parameters using current API."""

        class MockClient:
            pass

        client = MockClient()
        # Test the current API: _build_path appends segments to base path
        endpoint = EndpointBase(client, "/nodes")

        path = endpoint._build_path("node1", "qemu", "100")
        assert path == "/nodes/node1/qemu/100"

    def test_build_path_missing_params(self):
        """Test path building with empty segments."""

        class MockClient:
            pass

        client = MockClient()
        endpoint = EndpointBase(client, "/nodes")

        # Test with empty segments (should just return base path)
        path = endpoint._build_path()
        assert path == "/nodes"


if __name__ == "__main__":
    # Run basic smoke tests
    print("Running basic smoke tests...")

    # Test imports
    try:
        from prmxctrl.base import endpoint_base, exceptions, http_client

        print("✓ All imports successful")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        exit(1)

    # Test exception creation
    try:
        error = exceptions.ProxmoxError("test")
        assert str(error) == "test"
        print("✓ Exception creation works")
    except Exception as e:
        print(f"✗ Exception test failed: {e}")
        exit(1)

    # Test HTTPClient creation
    try:
        client = http_client.HTTPClient(
            host="https://test:8006", token_name="test", token_value="test"
        )
        assert client.host == "https://test:8006"
        print("✓ HTTPClient creation works")
    except Exception as e:
        print(f"✗ HTTPClient test failed: {e}")
        exit(1)

    # Test EndpointBase creation
    try:
        endpoint = endpoint_base.EndpointBase(client, "/test")
        assert endpoint._base_path == "/test"
        print("✓ EndpointBase creation works")
    except Exception as e:
        print(f"✗ EndpointBase test failed: {e}")
        exit(1)

    print("All smoke tests passed! ✓")
