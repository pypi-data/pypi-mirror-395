"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Query_Url_MetadataGETRequest
from prmxctrl.models.nodes import Nodes_Node_Query_Url_MetadataGETResponse  # type: ignore

class NodesQuery_Url_MetadataEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/query-url-metadata
    """



    async def get(self, params: Nodes_Node_Query_Url_MetadataGETRequest | None = None) -> Nodes_Node_Query_Url_MetadataGETResponse:
        """
        Query metadata of an URL: file size, file name and mime type.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

