"""
Common type aliases and custom Pydantic types for the prmxctrl SDK.

This module provides type definitions that are used throughout the SDK,
including custom Pydantic types for Proxmox-specific data formats.
"""

# Standard library imports for type annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

# Common type aliases for better readability
JSONValue = str | int | float | bool | None | dict[str, Any] | list[Any]
JSONObject = dict[str, JSONValue]
JSONArray = list[JSONValue]

# HTTP response types
HTTPStatusCode = int
HTTPHeaders = dict[str, str]

# Proxmox API response types
APIResponse = JSONObject
APIErrorResponse = dict[str, Any]  # Proxmox error response format

# Authentication types
AuthToken = str
Username = str
Password = str

# Common Proxmox data types
NodeName = str
VMID = int
StorageID = str
PoolID = str

# Custom Pydantic-compatible types for Proxmox formats
# These will be used in generated models to handle Proxmox-specific validation

# Note: These are type aliases for now. In the future, these could be
# enhanced with custom Pydantic validators for format-specific validation.

# Node-related types
ProxmoxNode = str  # Node name (e.g., "pve1", "pve-node-01")
ProxmoxNodeList = list[ProxmoxNode]

# Virtual machine types
ProxmoxVMID = int  # VM/Container ID (positive integer)
ProxmoxVMIDList = list[ProxmoxVMID]

# Storage types
ProxmoxStorageID = str  # Storage identifier
ProxmoxVolumeID = str  # Volume identifier with optional storage prefix
ProxmoxVolumeIDOrPath = ProxmoxVolumeID | str  # Volume ID or absolute path

# Network types
MACAddress = str  # MAC address in XX:XX:XX:XX:XX:XX format
IPAddress = str  # IPv4 or IPv6 address
CIDRNetwork = str  # CIDR notation network (e.g., "192.168.1.0/24")
IPv4Address = str  # IPv4 address
IPv6Address = str  # IPv6 address
PortNumber = int  # Network port (1-65535)

# Authentication types
ProxmoxUserID = str  # User identifier (e.g., "root@pam", "user@realm")
ProxmoxTokenID = str  # API token identifier

# Generic Proxmox types
ProxmoxConfigID = str  # Generic configuration identifier
ProxmoxConfigIDList = list[ProxmoxConfigID]

# Task and job types
ProxmoxTaskID = str  # Task identifier (UPID format)
ProxmoxJobID = str  # Job identifier

# Backup types
PruneBackupsConfig = dict[str, Any]  # Backup pruning configuration

# Certificate types
PEMString = str  # PEM-encoded certificate or key

# Utility types for internal use
PathSegment = str  # URL path segment
QueryParamValue = str | int | float | bool | list[str]
QueryParams = dict[str, QueryParamValue]

# Response parsing types
RawResponseData = bytes | str | JSONObject | JSONArray

# Context manager types for async operations
AsyncContextManager = Any  # Type hint for async context managers

# Configuration types
SSLVerifyMode = bool | str  # SSL verification: True, False, or path to CA bundle
TimeoutSeconds = float | int  # Timeout in seconds

# Internal SDK types
EndpointPath = str  # API endpoint path (e.g., "/nodes/{node}/qemu/{vmid}")
MethodName = str  # HTTP method name
ParameterName = str  # Parameter name
FieldName = str  # Model field name

# Type aliases for complex generic types
OptionalJSONObject = JSONObject | None
OptionalJSONArray = JSONArray | None
OptionalAPIResponse = APIResponse | None

# Union types for flexible parameters
StringOrInt = str | int
StringOrFloat = str | float
StringOrBool = str | bool

# List types for batch operations
NodeList = list[NodeName]
VMIDList = list[VMID]
StorageIDList = list[StorageID]

# Configuration object types
HTTPClientConfig = dict[str, Any]  # HTTP client configuration
AuthConfig = dict[str, Any]  # Authentication configuration

# Export all public types
__all__ = [
    # Basic JSON types
    "JSONValue",
    "JSONObject",
    "JSONArray",
    # HTTP types
    "HTTPStatusCode",
    "HTTPHeaders",
    # API response types
    "APIResponse",
    "APIErrorResponse",
    # Authentication types
    "AuthToken",
    "Username",
    "Password",
    # Proxmox data types
    "NodeName",
    "VMID",
    "StorageID",
    "PoolID",
    # Custom Proxmox types
    "ProxmoxNode",
    "ProxmoxNodeList",
    "ProxmoxVMID",
    "ProxmoxVMIDList",
    "ProxmoxStorageID",
    "ProxmoxVolumeID",
    "ProxmoxVolumeIDOrPath",
    "MACAddress",
    "IPAddress",
    "CIDRNetwork",
    "IPv4Address",
    "IPv6Address",
    "PortNumber",
    "ProxmoxUserID",
    "ProxmoxTokenID",
    "ProxmoxConfigID",
    "ProxmoxConfigIDList",
    "ProxmoxTaskID",
    "ProxmoxJobID",
    "PruneBackupsConfig",
    "PEMString",
    # Utility types
    "PathSegment",
    "QueryParamValue",
    "QueryParams",
    "RawResponseData",
    "AsyncContextManager",
    "SSLVerifyMode",
    "TimeoutSeconds",
    # Internal SDK types
    "EndpointPath",
    "MethodName",
    "ParameterName",
    "FieldName",
    # Optional types
    "OptionalJSONObject",
    "OptionalJSONArray",
    "OptionalAPIResponse",
    # Union types
    "StringOrInt",
    "StringOrFloat",
    "StringOrBool",
    # List types
    "NodeList",
    "VMIDList",
    "StorageIDList",
    # Configuration types
    "HTTPClientConfig",
    "AuthConfig",
]
