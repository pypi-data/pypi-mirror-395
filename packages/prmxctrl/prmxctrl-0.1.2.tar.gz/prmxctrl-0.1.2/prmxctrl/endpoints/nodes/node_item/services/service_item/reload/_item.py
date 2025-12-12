"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Services_Service_ReloadPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Services_Service_ReloadPOSTResponse  # type: ignore

class NodesServicesReloadEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/services/{service}/reload
    """



    async def service_reload(self, params: Nodes_Node_Services_Service_ReloadPOSTRequest | None = None) -> Nodes_Node_Services_Service_ReloadPOSTResponse:
        """
        Reload service. Falls back to restart if service cannot be reloaded.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

