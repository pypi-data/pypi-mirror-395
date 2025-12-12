"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .prunebackups._item import NodesStoragePrunebackupsEndpoints
from .content._item import NodesStorageContentEndpoints
from .file_restore._item import NodesStorageFile_RestoreEndpoints
from .status._item import NodesStorageStatusEndpoints
from .rrd._item import NodesStorageRrdEndpoints
from .rrddata._item import NodesStorageRrddataEndpoints
from .upload._item import NodesStorageUploadEndpoints
from .download_url._item import NodesStorageDownload_UrlEndpoints
from prmxctrl.models.nodes import Nodes_Node_Storage_StorageGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_StorageGETResponse  # type: ignore

class NodesStorageEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}
    """

    # Sub-endpoint properties
    @property
    def prunebackups(self) -> NodesStoragePrunebackupsEndpoints:
        """Access prunebackups endpoints"""
        from .prunebackups._item import NodesStoragePrunebackupsEndpoints  # type: ignore
        return NodesStoragePrunebackupsEndpoints(self._client, self._build_path("prunebackups"))
    @property
    def content(self) -> NodesStorageContentEndpoints:
        """Access content endpoints"""
        from .content._item import NodesStorageContentEndpoints  # type: ignore
        return NodesStorageContentEndpoints(self._client, self._build_path("content"))
    @property
    def file_restore(self) -> NodesStorageFile_RestoreEndpoints:
        """Access file-restore endpoints"""
        from .file_restore._item import NodesStorageFile_RestoreEndpoints  # type: ignore
        return NodesStorageFile_RestoreEndpoints(self._client, self._build_path("file-restore"))
    @property
    def status(self) -> NodesStorageStatusEndpoints:
        """Access status endpoints"""
        from .status._item import NodesStorageStatusEndpoints  # type: ignore
        return NodesStorageStatusEndpoints(self._client, self._build_path("status"))
    @property
    def rrd(self) -> NodesStorageRrdEndpoints:
        """Access rrd endpoints"""
        from .rrd._item import NodesStorageRrdEndpoints  # type: ignore
        return NodesStorageRrdEndpoints(self._client, self._build_path("rrd"))
    @property
    def rrddata(self) -> NodesStorageRrddataEndpoints:
        """Access rrddata endpoints"""
        from .rrddata._item import NodesStorageRrddataEndpoints  # type: ignore
        return NodesStorageRrddataEndpoints(self._client, self._build_path("rrddata"))
    @property
    def upload(self) -> NodesStorageUploadEndpoints:
        """Access upload endpoints"""
        from .upload._item import NodesStorageUploadEndpoints  # type: ignore
        return NodesStorageUploadEndpoints(self._client, self._build_path("upload"))
    @property
    def download_url(self) -> NodesStorageDownload_UrlEndpoints:
        """Access download-url endpoints"""
        from .download_url._item import NodesStorageDownload_UrlEndpoints  # type: ignore
        return NodesStorageDownload_UrlEndpoints(self._client, self._build_path("download-url"))



    async def list(self, params: Nodes_Node_Storage_StorageGETRequest | None = None) -> Nodes_Node_Storage_StorageGETResponse:
        """
        GET operation

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

