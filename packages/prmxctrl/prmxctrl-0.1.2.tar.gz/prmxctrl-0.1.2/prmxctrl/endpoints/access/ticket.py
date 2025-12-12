"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import Access_TicketPOSTRequest
from prmxctrl.models.access import Access_TicketPOSTResponse  # type: ignore

class AccessTicketEndpoints(EndpointBase):
    """
    Endpoint class for /access/ticket
    """



    async def get(self, ) -> Any:
        """
        Dummy. Useful for formatters which want to provide a login page.

        HTTP Method: GET
        """
        return await self._get()

    async def create_ticket(self, params: Access_TicketPOSTRequest | None = None) -> Access_TicketPOSTResponse:
        """
        Create or verify authentication ticket.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

