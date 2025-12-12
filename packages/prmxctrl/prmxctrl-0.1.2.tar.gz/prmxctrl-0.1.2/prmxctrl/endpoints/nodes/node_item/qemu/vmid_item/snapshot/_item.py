"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .snapname_item._item import NodesQemuSnapshotEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_SnapshotGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_SnapshotGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_SnapshotPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_SnapshotPOSTResponse  # type: ignore

class NodesQemuSnapshotEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/snapshot
    """


    def __call__(self, snapname: str) -> NodesQemuSnapshotEndpoints1:
        """Access specific snapname"""
        from .snapname_item._item import NodesQemuSnapshotEndpoints1  # type: ignore
        return NodesQemuSnapshotEndpoints1(
            self._client,
            self._build_path(str(snapname))
        )


    async def list(self, params: Nodes_Node_Qemu_Vmid_SnapshotGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_SnapshotGETResponse:
        """
        List all snapshots.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def snapshot(self, params: Nodes_Node_Qemu_Vmid_SnapshotPOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_SnapshotPOSTResponse:
        """
        Snapshot a VM.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

