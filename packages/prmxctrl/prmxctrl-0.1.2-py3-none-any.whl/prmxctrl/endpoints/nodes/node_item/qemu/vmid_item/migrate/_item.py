"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_MigrateGETRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_MigrateGETResponse
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_MigratePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Qemu_Vmid_MigratePOSTResponse  # type: ignore

class NodesQemuMigrateEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/qemu/{vmid}/migrate
    """



    async def get(self, params: Nodes_Node_Qemu_Vmid_MigrateGETRequest | None = None) -> Nodes_Node_Qemu_Vmid_MigrateGETResponse:
        """
        Get preconditions for migration.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def migrate_vm(self, params: Nodes_Node_Qemu_Vmid_MigratePOSTRequest | None = None) -> Nodes_Node_Qemu_Vmid_MigratePOSTResponse:
        """
        Migrate virtual machine. Creates a new migration task.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

