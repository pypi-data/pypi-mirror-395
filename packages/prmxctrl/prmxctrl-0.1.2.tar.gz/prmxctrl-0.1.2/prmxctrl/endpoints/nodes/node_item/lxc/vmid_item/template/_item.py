"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Lxc_Vmid_TemplatePOSTRequest  # type: ignore

class NodesLxcTemplateEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/lxc/{vmid}/template
    """



    async def template(self, params: Nodes_Node_Lxc_Vmid_TemplatePOSTRequest | None = None) -> Any:
        """
        Create a Template.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

