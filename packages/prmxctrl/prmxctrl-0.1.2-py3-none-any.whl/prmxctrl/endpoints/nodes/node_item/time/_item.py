"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_TimeGETRequest
from prmxctrl.models.nodes import Nodes_Node_TimeGETResponse
from prmxctrl.models.nodes import Nodes_Node_TimePUTRequest  # type: ignore

class NodesTimeEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/time
    """



    async def get(self, params: Nodes_Node_TimeGETRequest | None = None) -> Nodes_Node_TimeGETResponse:
        """
        Read server time and time zone settings.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def set_timezone(self, params: Nodes_Node_TimePUTRequest | None = None) -> Any:
        """
        Set time zone.

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

