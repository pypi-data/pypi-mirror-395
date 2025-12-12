"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Services_Service_RestartPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Services_Service_RestartPOSTResponse  # type: ignore

class NodesServicesRestartEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/services/{service}/restart
    """



    async def service_restart(self, params: Nodes_Node_Services_Service_RestartPOSTRequest | None = None) -> Nodes_Node_Services_Service_RestartPOSTResponse:
        """
        Hard restart service. Use reload if you want to reduce interruptions.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

