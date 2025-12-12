"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .osdid_item._item import NodesCephOsdEndpoints1
from prmxctrl.models.nodes import Nodes_Node_Ceph_OsdGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_OsdGETResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_OsdPOSTRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_OsdPOSTResponse  # type: ignore

class NodesCephOsdEndpoints(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/osd
    """


    def __call__(self, osdid: int) -> NodesCephOsdEndpoints1:
        """Access specific osdid"""
        from .osdid_item._item import NodesCephOsdEndpoints1  # type: ignore
        return NodesCephOsdEndpoints1(
            self._client,
            self._build_path(str(osdid))
        )


    async def get(self, params: Nodes_Node_Ceph_OsdGETRequest | None = None) -> Nodes_Node_Ceph_OsdGETResponse:
        """
        Get Ceph osd list/tree.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

    async def createosd(self, params: Nodes_Node_Ceph_OsdPOSTRequest | None = None) -> Nodes_Node_Ceph_OsdPOSTResponse:
        """
        Create OSD

        HTTP Method: POST
        """
        return await self._post(data=params.model_dump(exclude_none=True, by_alias=True) if params else None)

