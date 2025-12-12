"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_PrunebackupsDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_PrunebackupsDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_PrunebackupsGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_PrunebackupsGETResponse  # type: ignore

class NodesStoragePrunebackupsEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/prunebackups
    """



    async def delete(self, params: Nodes_Node_Storage_Storage_PrunebackupsDELETERequest | None = None) -> Nodes_Node_Storage_Storage_PrunebackupsDELETEResponse:
        """
        Prune backups. Only those using the standard naming scheme are considered.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Storage_Storage_PrunebackupsGETRequest | None = None) -> Nodes_Node_Storage_Storage_PrunebackupsGETResponse:
        """
        Get prune information for backups. NOTE: this is only a preview and might not be what a subsequent prune call does if backups are removed/added in the meantime.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

