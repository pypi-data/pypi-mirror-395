"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_MigrateallPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_MigrateallPOSTResponse  # type: ignore

class NodesMigrateallEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/migrateall
    """



    async def migrateall(self, params: Nodes_Node_MigrateallPOSTRequest | None = None) -> Nodes_Node_MigrateallPOSTResponse:
        """
        Migrate all VMs and Containers.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

