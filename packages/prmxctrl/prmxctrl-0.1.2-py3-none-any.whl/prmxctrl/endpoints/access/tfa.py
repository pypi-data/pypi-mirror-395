"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .userid_item._item import AccessTfaEndpoints1
from prmxctrl.models.access import Access_TfaGETResponse
from prmxctrl.models.access import Access_TfaPOSTRequest
from prmxctrl.models.access import Access_TfaPOSTResponse  # type: ignore

class AccessTfaEndpoints(EndpointBase):
    """
    Endpoint class for /access/tfa
    """


    def __call__(self, userid: int) -> AccessTfaEndpoints1:
        """Access specific userid"""
        from .userid_item._item import AccessTfaEndpoints1  # type: ignore
        return AccessTfaEndpoints1(
            self._client,
            self._build_path(str(userid))
        )


    async def list(self, ) -> Access_TfaGETResponse:
        """
        List TFA configurations of users.

        HTTP Method: GET
        """
        return await self._get()

    async def verify_tfa(self, params: Access_TfaPOSTRequest | None = None) -> Access_TfaPOSTResponse:
        """
        Finish a u2f challenge.

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

