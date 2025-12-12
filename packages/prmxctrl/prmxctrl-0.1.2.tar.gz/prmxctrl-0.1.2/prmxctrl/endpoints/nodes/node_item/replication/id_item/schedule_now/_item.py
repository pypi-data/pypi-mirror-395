"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Replication_Id_Schedule_NowPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Replication_Id_Schedule_NowPOSTResponse  # type: ignore

class NodesReplicationSchedule_NowEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/replication/{id}/schedule_now
    """



    async def schedule_now(self, params: Nodes_Node_Replication_Id_Schedule_NowPOSTRequest | None = None) -> Nodes_Node_Replication_Id_Schedule_NowPOSTResponse:
        """
        Schedule replication job to start as soon as possible.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

