"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_AplinfoGETRequest
from prmxctrl.models.nodes import Nodes_Node_AplinfoGETResponse
from prmxctrl.models.nodes import Nodes_Node_AplinfoPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_AplinfoPOSTResponse  # type: ignore

class NodesAplinfoEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/aplinfo
    """



    async def list(self, params: Nodes_Node_AplinfoGETRequest | None = None) -> Nodes_Node_AplinfoGETResponse:
        """
        Get list of appliances.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def apl_download(self, params: Nodes_Node_AplinfoPOSTRequest | None = None) -> Nodes_Node_AplinfoPOSTResponse:
        """
        Download appliance templates.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

