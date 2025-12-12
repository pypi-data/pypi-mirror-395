"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .rollback._item import NodesLxcSnapshotRollbackEndpoints
from .config._item import NodesLxcSnapshotConfigEndpoints
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_SnapnameDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_SnapnameDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_SnapnameGETRequest
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_Snapshot_SnapnameGETResponse  # type: ignore

class NodesLxcSnapshotEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/snapshot/{snapname}
    """

    # Sub-endpoint properties
    @property
    def rollback(self) -> NodesLxcSnapshotRollbackEndpoints:
        """Access rollback endpoints"""
        from .rollback._item import NodesLxcSnapshotRollbackEndpoints  # type: ignore
        return NodesLxcSnapshotRollbackEndpoints(self._client, self._build_path("rollback"))
    @property
    def config(self) -> NodesLxcSnapshotConfigEndpoints:
        """Access config endpoints"""
        from .config._item import NodesLxcSnapshotConfigEndpoints  # type: ignore
        return NodesLxcSnapshotConfigEndpoints(self._client, self._build_path("config"))



    async def delete(self, params: Nodes_Node_Lxc_Vmid_Snapshot_SnapnameDELETERequest | None = None) -> Nodes_Node_Lxc_Vmid_Snapshot_SnapnameDELETEResponse:
        """
        Delete a LXC snapshot.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Lxc_Vmid_Snapshot_SnapnameGETRequest | None = None) -> Nodes_Node_Lxc_Vmid_Snapshot_SnapnameGETResponse:
        """
        GET operation

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

