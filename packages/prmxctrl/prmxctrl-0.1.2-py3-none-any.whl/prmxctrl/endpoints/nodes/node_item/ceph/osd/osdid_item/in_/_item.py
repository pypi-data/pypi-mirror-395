"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Osd_Osdid_InPOSTRequest  # type: ignore

class NodesCephOsdInEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/osd/{osdid}/in
    """



    async def in_(self, params: Nodes_Node_Ceph_Osd_Osdid_InPOSTRequest | None = None) -> Any:
        """
        ceph osd in

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

