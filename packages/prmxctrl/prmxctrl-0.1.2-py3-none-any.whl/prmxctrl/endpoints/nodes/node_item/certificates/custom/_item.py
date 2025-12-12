"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Certificates_CustomDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Certificates_CustomPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Certificates_CustomPOSTResponse  # type: ignore

class NodesCertificatesCustomEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/certificates/custom
    """



    async def delete(self, params: Nodes_Node_Certificates_CustomDELETERequest | None = None) -> Any:
        """
        DELETE custom certificate chain and key.

        HTTP Method: DELETE
        """
        return await self._delete()

    async def upload_custom_cert(self, params: Nodes_Node_Certificates_CustomPOSTRequest | None = None) -> Nodes_Node_Certificates_CustomPOSTResponse:
        """
        Upload or update custom certificate chain and key.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

