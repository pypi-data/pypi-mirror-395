"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .list._item import NodesStorageFile_RestoreListEndpoints
from .download._item import NodesStorageFile_RestoreDownloadEndpoints  # type: ignore

class NodesStorageFile_RestoreEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/file-restore
    """

    # Sub-endpoint properties
    @property
    def list(self) -> NodesStorageFile_RestoreListEndpoints:
        """Access list endpoints"""
        from .list._item import NodesStorageFile_RestoreListEndpoints  # type: ignore
        return NodesStorageFile_RestoreListEndpoints(self._client, self._build_path("list"))
    @property
    def download(self) -> NodesStorageFile_RestoreDownloadEndpoints:
        """Access download endpoints"""
        from .download._item import NodesStorageFile_RestoreDownloadEndpoints  # type: ignore
        return NodesStorageFile_RestoreDownloadEndpoints(self._client, self._build_path("download"))



