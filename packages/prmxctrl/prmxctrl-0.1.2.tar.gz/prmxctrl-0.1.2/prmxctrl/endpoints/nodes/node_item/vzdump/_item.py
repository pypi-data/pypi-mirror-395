"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .defaults._item import NodesVzdumpDefaultsEndpoints
from .extractconfig._item import NodesVzdumpExtractconfigEndpoints
from prmxctrl.models.nodes import Nodes_Node_VzdumpPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_VzdumpPOSTResponse  # type: ignore

class NodesVzdumpEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/vzdump
    """

    # Sub-endpoint properties
    @property
    def defaults(self) -> NodesVzdumpDefaultsEndpoints:
        """Access defaults endpoints"""
        from .defaults._item import NodesVzdumpDefaultsEndpoints  # type: ignore
        return NodesVzdumpDefaultsEndpoints(self._client, self._build_path("defaults"))
    @property
    def extractconfig(self) -> NodesVzdumpExtractconfigEndpoints:
        """Access extractconfig endpoints"""
        from .extractconfig._item import NodesVzdumpExtractconfigEndpoints  # type: ignore
        return NodesVzdumpExtractconfigEndpoints(self._client, self._build_path("extractconfig"))



    async def vzdump(self, params: Nodes_Node_VzdumpPOSTRequest | None = None) -> Nodes_Node_VzdumpPOSTResponse:
        """
        Create backup.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

