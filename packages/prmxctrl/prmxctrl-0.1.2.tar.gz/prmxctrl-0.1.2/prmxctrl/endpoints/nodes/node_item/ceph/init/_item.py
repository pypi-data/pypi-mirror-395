"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_InitPOSTRequest  # type: ignore

class NodesCephInitEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/init
    """



    async def init(self, params: Nodes_Node_Ceph_InitPOSTRequest | None = None) -> Any:
        """
        Create initial ceph default configuration and setup symlinks.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

