"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .config._item import NodesQemuSnapshotConfigEndpoints
from .rollback._item import NodesQemuSnapshotRollbackEndpoints
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Snapshot_SnapnameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Snapshot_SnapnameDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Snapshot_SnapnameGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Snapshot_SnapnameGETResponse  # type: ignore

class NodesQemuSnapshotEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/snapshot/{snapname}
    """

    # Sub-endpoint properties
    @property
    def config(self) -> NodesQemuSnapshotConfigEndpoints:
        """Access config endpoints"""
        from .config._item import NodesQemuSnapshotConfigEndpoints  # type: ignore
        return NodesQemuSnapshotConfigEndpoints(self._client, self._build_path("config"))
    @property
    def rollback(self) -> NodesQemuSnapshotRollbackEndpoints:
        """Access rollback endpoints"""
        from .rollback._item import NodesQemuSnapshotRollbackEndpoints  # type: ignore
        return NodesQemuSnapshotRollbackEndpoints(self._client, self._build_path("rollback"))



    async def delete(self, params: Nodes_Node_Qemu_Vmid_Snapshot_SnapnameDELETERequest | None = None) -> Nodes_Node_Qemu_Vmid_Snapshot_SnapnameDELETEResponse:
        """
        Delete a VM snapshot.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Qemu_Vmid_Snapshot_SnapnameGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_Snapshot_SnapnameGETResponse:
        """
        GET operation

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

