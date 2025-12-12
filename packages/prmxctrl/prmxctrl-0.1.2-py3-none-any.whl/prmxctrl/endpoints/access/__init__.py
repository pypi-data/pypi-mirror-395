"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.access import AccessGETResponse  # type: ignore

class AccessEndpoints(EndpointBase):
    """
    Root endpoint class for access API endpoints.
    """



    async def list(self, ) -> AccessGETResponse:
        """
        Directory index.

        HTTP Method: GET
        """
        return await self._get()

