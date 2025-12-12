"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_Apt_RepositoriesGETRequest
from prmxctrl.models.nodes import Nodes_Node_Apt_RepositoriesGETResponse
from prmxctrl.models.nodes import Nodes_Node_Apt_RepositoriesPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Apt_RepositoriesPUTRequest  # type: ignore

class NodesAptRepositoriesEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/apt/repositories
    """



    async def get(self, params: Nodes_Node_Apt_RepositoriesGETRequest | None = None) -> Nodes_Node_Apt_RepositoriesGETResponse:
        """
        Get APT repository information.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def change_repository(self, params: Nodes_Node_Apt_RepositoriesPOSTRequest | None = None) -> Any:
        """
        Change the properties of a repository. Currently only allows enabling/disabling.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def add_repository(self, params: Nodes_Node_Apt_RepositoriesPUTRequest | None = None) -> Any:
        """
        Add a standard repository to the configuration

        HTTP Method: PUT
        """
        return await self._put(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

