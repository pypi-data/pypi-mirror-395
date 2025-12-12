"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_StartPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_StartPOSTResponse  # type: ignore

class NodesCephStartEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/start
    """



    async def start(self, params: Nodes_Node_Ceph_StartPOSTRequest | None = None) -> Nodes_Node_Ceph_StartPOSTResponse:
        """
        Start ceph services.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

