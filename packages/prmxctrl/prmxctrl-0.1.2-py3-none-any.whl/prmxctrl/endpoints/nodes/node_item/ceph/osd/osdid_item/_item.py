"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .metadata._item import NodesCephOsdMetadataEndpoints
from .lv_info._item import NodesCephOsdLv_InfoEndpoints
from .in_._item import NodesCephOsdInEndpoints
from .out._item import NodesCephOsdOutEndpoints
from .scrub._item import NodesCephOsdScrubEndpoints
from prmxctrl.models.nodes import Nodes_Node_Ceph_Osd_OsdidDELETERequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Osd_OsdidDELETEResponse
from prmxctrl.models.nodes import Nodes_Node_Ceph_Osd_OsdidGETRequest
from prmxctrl.models.nodes import Nodes_Node_Ceph_Osd_OsdidGETResponse  # type: ignore

class NodesCephOsdEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}/ceph/osd/{osdid}
    """

    # Sub-endpoint properties
    @property
    def metadata(self) -> NodesCephOsdMetadataEndpoints:
        """Access metadata endpoints"""
        from .metadata._item import NodesCephOsdMetadataEndpoints  # type: ignore
        return NodesCephOsdMetadataEndpoints(self._client, self._build_path("metadata"))
    @property
    def lv_info(self) -> NodesCephOsdLv_InfoEndpoints:
        """Access lv-info endpoints"""
        from .lv_info._item import NodesCephOsdLv_InfoEndpoints  # type: ignore
        return NodesCephOsdLv_InfoEndpoints(self._client, self._build_path("lv-info"))
    @property
    def in_(self) -> NodesCephOsdInEndpoints:
        """Access in endpoints"""
        from .in_._item import NodesCephOsdInEndpoints  # type: ignore
        return NodesCephOsdInEndpoints(self._client, self._build_path("in"))
    @property
    def out(self) -> NodesCephOsdOutEndpoints:
        """Access out endpoints"""
        from .out._item import NodesCephOsdOutEndpoints  # type: ignore
        return NodesCephOsdOutEndpoints(self._client, self._build_path("out"))
    @property
    def scrub(self) -> NodesCephOsdScrubEndpoints:
        """Access scrub endpoints"""
        from .scrub._item import NodesCephOsdScrubEndpoints  # type: ignore
        return NodesCephOsdScrubEndpoints(self._client, self._build_path("scrub"))



    async def delete(self, params: Nodes_Node_Ceph_Osd_OsdidDELETERequest | None = None) -> Nodes_Node_Ceph_Osd_OsdidDELETEResponse:
        """
        Destroy OSD

        HTTP Method: DELETE
        """
        return await self._delete()

    async def list(self, params: Nodes_Node_Ceph_Osd_OsdidGETRequest | None = None) -> Nodes_Node_Ceph_Osd_OsdidGETResponse:
        """
        OSD index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

