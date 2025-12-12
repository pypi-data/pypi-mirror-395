"""
Generated endpoint classes for Proxmox VE API endpoints.

This module contains auto-generated endpoint classes for hierarchical
API access to Proxmox VE endpoints.
DO NOT EDIT MANUALLY
"""

from typing import Any
from prmxctrl.base.endpoint_base import EndpointBase
from .qemu._item import NodesQemuEndpoints
from .lxc._item import NodesLxcEndpoints
from .ceph._item import NodesCephEndpoints
from .vzdump._item import NodesVzdumpEndpoints
from .services._item import NodesServicesEndpoints
from .subscription._item import NodesSubscriptionEndpoints
from .network._item import NodesNetworkEndpoints
from .tasks._item import NodesTasksEndpoints
from .scan._item import NodesScanEndpoints
from .hardware._item import NodesHardwareEndpoints
from .capabilities._item import NodesCapabilitiesEndpoints
from .storage._item import NodesStorageEndpoints
from .disks._item import NodesDisksEndpoints
from .apt._item import NodesAptEndpoints
from .firewall._item import NodesFirewallEndpoints
from .replication._item import NodesReplicationEndpoints
from .certificates._item import NodesCertificatesEndpoints
from .config._item import NodesConfigEndpoints
from .sdn._item import NodesSdnEndpoints
from .version._item import NodesVersionEndpoints
from .status._item import NodesStatusEndpoints
from .netstat._item import NodesNetstatEndpoints
from .execute._item import NodesExecuteEndpoints
from .wakeonlan._item import NodesWakeonlanEndpoints
from .rrd._item import NodesRrdEndpoints
from .rrddata._item import NodesRrddataEndpoints
from .syslog._item import NodesSyslogEndpoints
from .journal._item import NodesJournalEndpoints
from .vncshell._item import NodesVncshellEndpoints
from .termproxy._item import NodesTermproxyEndpoints
from .vncwebsocket._item import NodesVncwebsocketEndpoints
from .spiceshell._item import NodesSpiceshellEndpoints
from .dns._item import NodesDnsEndpoints
from .time._item import NodesTimeEndpoints
from .aplinfo._item import NodesAplinfoEndpoints
from .query_url_metadata._item import NodesQuery_Url_MetadataEndpoints
from .report._item import NodesReportEndpoints
from .startall._item import NodesStartallEndpoints
from .stopall._item import NodesStopallEndpoints
from .migrateall._item import NodesMigrateallEndpoints
from .hosts._item import NodesHostsEndpoints
from prmxctrl.models.nodes import Nodes_NodeGETRequest
from prmxctrl.models.nodes import Nodes_NodeGETResponse  # type: ignore

class NodesEndpoints1(EndpointBase):
    """
    Endpoint class for /nodes/{node}
    """

    # Sub-endpoint properties
    @property
    def qemu(self) -> NodesQemuEndpoints:
        """Access qemu endpoints"""
        from .qemu._item import NodesQemuEndpoints  # type: ignore
        return NodesQemuEndpoints(self._client, self._build_path("qemu"))
    @property
    def lxc(self) -> NodesLxcEndpoints:
        """Access lxc endpoints"""
        from .lxc._item import NodesLxcEndpoints  # type: ignore
        return NodesLxcEndpoints(self._client, self._build_path("lxc"))
    @property
    def ceph(self) -> NodesCephEndpoints:
        """Access ceph endpoints"""
        from .ceph._item import NodesCephEndpoints  # type: ignore
        return NodesCephEndpoints(self._client, self._build_path("ceph"))
    @property
    def vzdump(self) -> NodesVzdumpEndpoints:
        """Access vzdump endpoints"""
        from .vzdump._item import NodesVzdumpEndpoints  # type: ignore
        return NodesVzdumpEndpoints(self._client, self._build_path("vzdump"))
    @property
    def services(self) -> NodesServicesEndpoints:
        """Access services endpoints"""
        from .services._item import NodesServicesEndpoints  # type: ignore
        return NodesServicesEndpoints(self._client, self._build_path("services"))
    @property
    def subscription(self) -> NodesSubscriptionEndpoints:
        """Access subscription endpoints"""
        from .subscription._item import NodesSubscriptionEndpoints  # type: ignore
        return NodesSubscriptionEndpoints(self._client, self._build_path("subscription"))
    @property
    def network(self) -> NodesNetworkEndpoints:
        """Access network endpoints"""
        from .network._item import NodesNetworkEndpoints  # type: ignore
        return NodesNetworkEndpoints(self._client, self._build_path("network"))
    @property
    def tasks(self) -> NodesTasksEndpoints:
        """Access tasks endpoints"""
        from .tasks._item import NodesTasksEndpoints  # type: ignore
        return NodesTasksEndpoints(self._client, self._build_path("tasks"))
    @property
    def scan(self) -> NodesScanEndpoints:
        """Access scan endpoints"""
        from .scan._item import NodesScanEndpoints  # type: ignore
        return NodesScanEndpoints(self._client, self._build_path("scan"))
    @property
    def hardware(self) -> NodesHardwareEndpoints:
        """Access hardware endpoints"""
        from .hardware._item import NodesHardwareEndpoints  # type: ignore
        return NodesHardwareEndpoints(self._client, self._build_path("hardware"))
    @property
    def capabilities(self) -> NodesCapabilitiesEndpoints:
        """Access capabilities endpoints"""
        from .capabilities._item import NodesCapabilitiesEndpoints  # type: ignore
        return NodesCapabilitiesEndpoints(self._client, self._build_path("capabilities"))
    @property
    def storage(self) -> NodesStorageEndpoints:
        """Access storage endpoints"""
        from .storage._item import NodesStorageEndpoints  # type: ignore
        return NodesStorageEndpoints(self._client, self._build_path("storage"))
    @property
    def disks(self) -> NodesDisksEndpoints:
        """Access disks endpoints"""
        from .disks._item import NodesDisksEndpoints  # type: ignore
        return NodesDisksEndpoints(self._client, self._build_path("disks"))
    @property
    def apt(self) -> NodesAptEndpoints:
        """Access apt endpoints"""
        from .apt._item import NodesAptEndpoints  # type: ignore
        return NodesAptEndpoints(self._client, self._build_path("apt"))
    @property
    def firewall(self) -> NodesFirewallEndpoints:
        """Access firewall endpoints"""
        from .firewall._item import NodesFirewallEndpoints  # type: ignore
        return NodesFirewallEndpoints(self._client, self._build_path("firewall"))
    @property
    def replication(self) -> NodesReplicationEndpoints:
        """Access replication endpoints"""
        from .replication._item import NodesReplicationEndpoints  # type: ignore
        return NodesReplicationEndpoints(self._client, self._build_path("replication"))
    @property
    def certificates(self) -> NodesCertificatesEndpoints:
        """Access certificates endpoints"""
        from .certificates._item import NodesCertificatesEndpoints  # type: ignore
        return NodesCertificatesEndpoints(self._client, self._build_path("certificates"))
    @property
    def config(self) -> NodesConfigEndpoints:
        """Access config endpoints"""
        from .config._item import NodesConfigEndpoints  # type: ignore
        return NodesConfigEndpoints(self._client, self._build_path("config"))
    @property
    def sdn(self) -> NodesSdnEndpoints:
        """Access sdn endpoints"""
        from .sdn._item import NodesSdnEndpoints  # type: ignore
        return NodesSdnEndpoints(self._client, self._build_path("sdn"))
    @property
    def version(self) -> NodesVersionEndpoints:
        """Access version endpoints"""
        from .version._item import NodesVersionEndpoints  # type: ignore
        return NodesVersionEndpoints(self._client, self._build_path("version"))
    @property
    def status(self) -> NodesStatusEndpoints:
        """Access status endpoints"""
        from .status._item import NodesStatusEndpoints  # type: ignore
        return NodesStatusEndpoints(self._client, self._build_path("status"))
    @property
    def netstat(self) -> NodesNetstatEndpoints:
        """Access netstat endpoints"""
        from .netstat._item import NodesNetstatEndpoints  # type: ignore
        return NodesNetstatEndpoints(self._client, self._build_path("netstat"))
    @property
    def execute(self) -> NodesExecuteEndpoints:
        """Access execute endpoints"""
        from .execute._item import NodesExecuteEndpoints  # type: ignore
        return NodesExecuteEndpoints(self._client, self._build_path("execute"))
    @property
    def wakeonlan(self) -> NodesWakeonlanEndpoints:
        """Access wakeonlan endpoints"""
        from .wakeonlan._item import NodesWakeonlanEndpoints  # type: ignore
        return NodesWakeonlanEndpoints(self._client, self._build_path("wakeonlan"))
    @property
    def rrd(self) -> NodesRrdEndpoints:
        """Access rrd endpoints"""
        from .rrd._item import NodesRrdEndpoints  # type: ignore
        return NodesRrdEndpoints(self._client, self._build_path("rrd"))
    @property
    def rrddata(self) -> NodesRrddataEndpoints:
        """Access rrddata endpoints"""
        from .rrddata._item import NodesRrddataEndpoints  # type: ignore
        return NodesRrddataEndpoints(self._client, self._build_path("rrddata"))
    @property
    def syslog(self) -> NodesSyslogEndpoints:
        """Access syslog endpoints"""
        from .syslog._item import NodesSyslogEndpoints  # type: ignore
        return NodesSyslogEndpoints(self._client, self._build_path("syslog"))
    @property
    def journal(self) -> NodesJournalEndpoints:
        """Access journal endpoints"""
        from .journal._item import NodesJournalEndpoints  # type: ignore
        return NodesJournalEndpoints(self._client, self._build_path("journal"))
    @property
    def vncshell(self) -> NodesVncshellEndpoints:
        """Access vncshell endpoints"""
        from .vncshell._item import NodesVncshellEndpoints  # type: ignore
        return NodesVncshellEndpoints(self._client, self._build_path("vncshell"))
    @property
    def termproxy(self) -> NodesTermproxyEndpoints:
        """Access termproxy endpoints"""
        from .termproxy._item import NodesTermproxyEndpoints  # type: ignore
        return NodesTermproxyEndpoints(self._client, self._build_path("termproxy"))
    @property
    def vncwebsocket(self) -> NodesVncwebsocketEndpoints:
        """Access vncwebsocket endpoints"""
        from .vncwebsocket._item import NodesVncwebsocketEndpoints  # type: ignore
        return NodesVncwebsocketEndpoints(self._client, self._build_path("vncwebsocket"))
    @property
    def spiceshell(self) -> NodesSpiceshellEndpoints:
        """Access spiceshell endpoints"""
        from .spiceshell._item import NodesSpiceshellEndpoints  # type: ignore
        return NodesSpiceshellEndpoints(self._client, self._build_path("spiceshell"))
    @property
    def dns(self) -> NodesDnsEndpoints:
        """Access dns endpoints"""
        from .dns._item import NodesDnsEndpoints  # type: ignore
        return NodesDnsEndpoints(self._client, self._build_path("dns"))
    @property
    def time(self) -> NodesTimeEndpoints:
        """Access time endpoints"""
        from .time._item import NodesTimeEndpoints  # type: ignore
        return NodesTimeEndpoints(self._client, self._build_path("time"))
    @property
    def aplinfo(self) -> NodesAplinfoEndpoints:
        """Access aplinfo endpoints"""
        from .aplinfo._item import NodesAplinfoEndpoints  # type: ignore
        return NodesAplinfoEndpoints(self._client, self._build_path("aplinfo"))
    @property
    def query_url_metadata(self) -> NodesQuery_Url_MetadataEndpoints:
        """Access query-url-metadata endpoints"""
        from .query_url_metadata._item import NodesQuery_Url_MetadataEndpoints  # type: ignore
        return NodesQuery_Url_MetadataEndpoints(self._client, self._build_path("query-url-metadata"))
    @property
    def report(self) -> NodesReportEndpoints:
        """Access report endpoints"""
        from .report._item import NodesReportEndpoints  # type: ignore
        return NodesReportEndpoints(self._client, self._build_path("report"))
    @property
    def startall(self) -> NodesStartallEndpoints:
        """Access startall endpoints"""
        from .startall._item import NodesStartallEndpoints  # type: ignore
        return NodesStartallEndpoints(self._client, self._build_path("startall"))
    @property
    def stopall(self) -> NodesStopallEndpoints:
        """Access stopall endpoints"""
        from .stopall._item import NodesStopallEndpoints  # type: ignore
        return NodesStopallEndpoints(self._client, self._build_path("stopall"))
    @property
    def migrateall(self) -> NodesMigrateallEndpoints:
        """Access migrateall endpoints"""
        from .migrateall._item import NodesMigrateallEndpoints  # type: ignore
        return NodesMigrateallEndpoints(self._client, self._build_path("migrateall"))
    @property
    def hosts(self) -> NodesHostsEndpoints:
        """Access hosts endpoints"""
        from .hosts._item import NodesHostsEndpoints  # type: ignore
        return NodesHostsEndpoints(self._client, self._build_path("hosts"))



    async def list(self, params: Nodes_NodeGETRequest | None = None) -> Nodes_NodeGETResponse:
        """
        Node index.

        HTTP Method: GET
        """
        return await self._get(params=params.model_dump(exclude_none=True, by_alias=True) if params else None)

