"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_Snapname_RollbackPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_Snapname_RollbackPOSTResponse  # type: ignore

class NodesLxcSnapshotRollbackEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/rollback
    """



    async def rollback(self, params: Nodes_Node_Lxc_Vmid_Snapshot_Snapname_RollbackPOSTRequest | None = None) -> Nodes_Node_Lxc_Vmid_Snapshot_Snapname_RollbackPOSTResponse:
        """
        Rollback LXC state to specified snapshot.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

