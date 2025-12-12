"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Apt_UpdateGETRequest
from prmxctrl.models.nodes import Nodes_Node_Apt_UpdateGETResponse
from prmxctrl.models.nodes import Nodes_Node_Apt_UpdatePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Apt_UpdatePOSTResponse  # type: ignore

class NodesAptUpdateEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/apt/update
    """



    async def list(self, params: Nodes_Node_Apt_UpdateGETRequest | None = None) -> Nodes_Node_Apt_UpdateGETResponse:
        """
        List available updates.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def update_database(self, params: Nodes_Node_Apt_UpdatePOSTRequest | None = None) -> Nodes_Node_Apt_UpdatePOSTResponse:
        """
        This is used to resynchronize the package index files from their sources (apt-get update).

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

