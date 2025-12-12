"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .content._item import NodesSdnZonesContentEndpoints
from prmxctrl.models.nodes import Nodes_Node_Sdn_Zones_ZoneGETRequest
from prmxctrl.models.nodes import Nodes_Node_Sdn_Zones_ZoneGETResponse  # type: ignore

class NodesSdnZonesEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/sdn/zones/{zone}
    """

    # Sub-endpoint properties
    @property
    def content(self) -> NodesSdnZonesContentEndpoints:
        """Access content endpoints"""
        from .content._item import NodesSdnZonesContentEndpoints  # type: ignore
        return NodesSdnZonesContentEndpoints(self._client, self._build_path("content"))



    async def list(self, params: Nodes_Node_Sdn_Zones_ZoneGETRequest | None = None) -> Nodes_Node_Sdn_Zones_ZoneGETResponse:
        """
        GET operation

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

