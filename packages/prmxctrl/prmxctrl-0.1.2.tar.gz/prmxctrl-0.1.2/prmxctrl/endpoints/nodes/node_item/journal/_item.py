"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.nodes import Nodes_Node_JournalGETRequest
from prmxctrl.models.nodes import Nodes_Node_JournalGETResponse  # type: ignore

class NodesJournalEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/journal
    """



    async def list(self, params: Nodes_Node_JournalGETRequest | None = None) -> Nodes_Node_JournalGETResponse:
        """
        Read Journal

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

