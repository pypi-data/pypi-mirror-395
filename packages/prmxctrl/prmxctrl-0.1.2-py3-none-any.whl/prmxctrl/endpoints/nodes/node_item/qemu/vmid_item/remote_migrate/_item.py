"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Remote_MigratePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_Remote_MigratePOSTResponse  # type: ignore

class NodesQemuRemote_MigrateEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/remote_migrate
    """



    async def remote_migrate_vm(self, params: Nodes_Node_Qemu_Vmid_Remote_MigratePOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_Remote_MigratePOSTResponse:
        """
        Migrate virtual machine to a remote cluster. Creates a new migration task. EXPERIMENTAL feature!

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

