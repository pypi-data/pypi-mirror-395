"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .zones._item import NodesSdnZonesEndpoints
from prmxctrl.models.nodes import Nodes_Node_SdnGETRequest
from prmxctrl.models.nodes import Nodes_Node_SdnGETResponse  # type: ignore

class NodesSdnEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/sdn
    """

    # Sub-endpoint properties
    @property
    def zones(self) -> NodesSdnZonesEndpoints:
        """Access zones endpoints"""
        from .zones._item import NodesSdnZonesEndpoints  # type: ignore
        return NodesSdnZonesEndpoints(self._client, self._build_path("zones"))



    async def list(self, params: Nodes_Node_SdnGETRequest | None = None) -> Nodes_Node_SdnGETResponse:
        """
        SDN index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

