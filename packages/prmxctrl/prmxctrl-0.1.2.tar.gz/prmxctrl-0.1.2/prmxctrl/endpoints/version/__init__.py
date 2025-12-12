"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from prmxctrl.models.version import VersionGETResponse  # type: ignore

class VersionEndpoints(EndpointBase):
    """
    Root endpoint class for version API endpoints.
    """



    async def get(self, ) -> VersionGETResponse:
        """
        API version details, including some parts of the global datacenter config.

        HTTP Method: GET
        """
        return await self._get()

