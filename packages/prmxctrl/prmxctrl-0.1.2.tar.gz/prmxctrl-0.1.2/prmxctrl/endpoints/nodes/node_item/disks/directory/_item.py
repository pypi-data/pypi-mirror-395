"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .name_item._item import NodesDisksDirectoryEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Disks_DirectoryGETRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_DirectoryGETResponse
from prmxctrl.models.nodes import Nodes_Node_Disks_DirectoryPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Disks_DirectoryPOSTResponse  # type: ignore

class NodesDisksDirectoryEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/disks/directory
    """


    def __call__(self, name: str) -> NodesDisksDirectoryEndpoints1:
        """Access specific name"""
        from .name_item._item import NodesDisksDirectoryEndpoints1  # type: ignore
        return NodesDisksDirectoryEndpoints1(
            self._client,
            self._build_path(str(name))
        )


    async def list(self, params: Nodes_Node_Disks_DirectoryGETRequest | None = None) -> Nodes_Node_Disks_DirectoryGETResponse:
        """
        PVE Managed Directory storages.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def create(self, params: Nodes_Node_Disks_DirectoryPOSTRequest | None = None) -> Nodes_Node_Disks_DirectoryPOSTResponse:
        """
        Create a Filesystem on an unused disk. Will be mounted under '/mnt/pve/NAME'.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

