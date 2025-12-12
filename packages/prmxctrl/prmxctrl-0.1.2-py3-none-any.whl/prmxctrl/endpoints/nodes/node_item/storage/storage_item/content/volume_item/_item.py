"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Content_VolumeDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Content_VolumeDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Content_VolumeGETRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Content_VolumeGETResponse
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Content_VolumePOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Content_VolumePOSTResponse
from prmxctrl.models.nodes import Nodes_Node_Storage_Storage_Content_VolumePUTRequest  # type: ignore

class NodesStorageContentEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/storage/{storage}/content/{volume}
    """



    async def delete(self, params: Nodes_Node_Storage_Storage_Content_VolumeDELETERequest | None = None) -> Nodes_Node_Storage_Storage_Content_VolumeDELETEResponse:
        """
        Delete volume

        HTTP Method: DELETE
        """
        return await self._delete()

    async def get(self, params: Nodes_Node_Storage_Storage_Content_VolumeGETRequest | None = None) -> Nodes_Node_Storage_Storage_Content_VolumeGETResponse:
        """
        Get volume attributes

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def copy(self, params: Nodes_Node_Storage_Storage_Content_VolumePOSTRequest | None = None) -> Nodes_Node_Storage_Storage_Content_VolumePOSTResponse:
        """
        Copy a volume. This is experimental code - do not use.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def updateattributes(self, params: Nodes_Node_Storage_Storage_Content_VolumePUTRequest | None = None) -> Any:
        """
        Update volume attributes

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

