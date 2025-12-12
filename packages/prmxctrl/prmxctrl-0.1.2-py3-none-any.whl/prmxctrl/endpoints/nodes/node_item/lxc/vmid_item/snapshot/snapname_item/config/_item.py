"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigGETRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigGETResponse
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigPUTRequest  # type: ignore

class NodesLxcSnapshotConfigEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/config
    """



    async def get(self, params: Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigGETRequest | None = None) -> Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigGETResponse:
        """
        Get snapshot configuration

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_snapshot_config(self, params: Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigPUTRequest | None = None) -> Any:
        """
        Update snapshot metadata.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

