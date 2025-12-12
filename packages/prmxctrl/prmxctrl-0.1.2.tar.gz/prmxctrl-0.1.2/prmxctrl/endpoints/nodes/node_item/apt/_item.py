"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .update._item import NodesAptUpdateEndpoints
from .changelog._item import NodesAptChangelogEndpoints
from .repositories._item import NodesAptRepositoriesEndpoints
from .versions._item import NodesAptVersionsEndpoints
from prmxctrl.models.nodes import Nodes_Node_AptGETRequest
from prmxctrl.models.nodes import Nodes_Node_AptGETResponse  # type: ignore

class NodesAptEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/apt
    """

    # Sub-endpoint properties
    @property
    def update(self) -> NodesAptUpdateEndpoints:
        """Access update endpoints"""
        from .update._item import NodesAptUpdateEndpoints  # type: ignore
        return NodesAptUpdateEndpoints(self._client, self._build_path("update"))
    @property
    def changelog(self) -> NodesAptChangelogEndpoints:
        """Access changelog endpoints"""
        from .changelog._item import NodesAptChangelogEndpoints  # type: ignore
        return NodesAptChangelogEndpoints(self._client, self._build_path("changelog"))
    @property
    def repositories(self) -> NodesAptRepositoriesEndpoints:
        """Access repositories endpoints"""
        from .repositories._item import NodesAptRepositoriesEndpoints  # type: ignore
        return NodesAptRepositoriesEndpoints(self._client, self._build_path("repositories"))
    @property
    def versions(self) -> NodesAptVersionsEndpoints:
        """Access versions endpoints"""
        from .versions._item import NodesAptVersionsEndpoints  # type: ignore
        return NodesAptVersionsEndpoints(self._client, self._build_path("versions"))



    async def list(self, params: Nodes_Node_AptGETRequest | None = None) -> Nodes_Node_AptGETResponse:
        """
        Directory index for apt (Advanced Package Tool).

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

