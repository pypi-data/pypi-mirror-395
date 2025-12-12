"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Ceph_Osd_Osdid_ScrubPOSTRequest  # type: ignore

class NodesCephOsdScrubEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/osd/{osdid}/scrub
    """



    async def scrub(self, params: Nodes_Node_Ceph_Osd_Osdid_ScrubPOSTRequest | None = None) -> Any:
        """
        Instruct the OSD to scrub.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

