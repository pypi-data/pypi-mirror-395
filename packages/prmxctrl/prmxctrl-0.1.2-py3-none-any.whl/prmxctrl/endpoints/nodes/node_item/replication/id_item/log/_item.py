"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Replication_Id_LogGETRequest
from prmxctrl.models.nodes import Nodes_Node_Replication_Id_LogGETResponse  # type: ignore

class NodesReplicationLogEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/replication/{id}/log
    """



    async def list(self, params: Nodes_Node_Replication_Id_LogGETRequest | None = None) -> Nodes_Node_Replication_Id_LogGETResponse:
        """
        Read replication job log.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

