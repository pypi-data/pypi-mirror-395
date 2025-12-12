"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_RestartPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_RestartPOSTResponse  # type: ignore

class NodesCephRestartEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/restart
    """



    async def restart(self, params: Nodes_Node_Ceph_RestartPOSTRequest | None = None) -> Nodes_Node_Ceph_RestartPOSTResponse:
        """
        Restart ceph services.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

