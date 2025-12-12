"""
Base classes and utilities for the prmxctrl SDK.

This module contains the hand-written base classes that support all generated code.
"""

from .endpoint_base import EndpointBase
from .exceptions import (
    ProxmoxAPIError,
    ProxmoxAuthError,
    ProxmoxConnectionError,
    ProxmoxError,
    ProxmoxTimeoutError,
    ProxmoxValidationError,
)
from .http_client import HTTPClient
from .types import (
    VMID,
    APIErrorResponse,
    APIResponse,
    JSONArray,
    JSONObject,
    JSONValue,
    MACAddress,
    NodeList,
    NodeName,
    PEMString,
    PortNumber,
    ProxmoxConfigID,
    ProxmoxConfigIDList,
    ProxmoxJobID,
    ProxmoxNode,
    ProxmoxNodeList,
    ProxmoxStorageID,
    ProxmoxTaskID,
    ProxmoxTokenID,
    ProxmoxUserID,
    ProxmoxVMID,
    ProxmoxVMIDList,
    ProxmoxVolumeID,
    ProxmoxVolumeIDOrPath,
    PruneBackupsConfig,
    StorageID,
    StorageIDList,
    VMIDList,
)

__all__ = [
    # HTTP Client
    "HTTPClient",
    # Endpoint Base
    "EndpointBase",
    # Exceptions
    "ProxmoxError",
    "ProxmoxAuthError",
    "ProxmoxConnectionError",
    "ProxmoxTimeoutError",
    "ProxmoxAPIError",
    "ProxmoxValidationError",
    # Basic types
    "JSONValue",
    "JSONObject",
    "JSONArray",
    "APIResponse",
    "APIErrorResponse",
    # Proxmox data types
    "NodeName",
    "VMID",
    "StorageID",
    "MACAddress",
    "PortNumber",
    "PEMString",
    # Custom Proxmox types
    "ProxmoxNode",
    "ProxmoxNodeList",
    "ProxmoxVMID",
    "ProxmoxVMIDList",
    "ProxmoxStorageID",
    "ProxmoxVolumeID",
    "ProxmoxVolumeIDOrPath",
    "ProxmoxUserID",
    "ProxmoxTokenID",
    "ProxmoxConfigID",
    "ProxmoxConfigIDList",
    "ProxmoxTaskID",
    "ProxmoxJobID",
    "PruneBackupsConfig",
    # List types
    "NodeList",
    "VMIDList",
    "StorageIDList",
]
