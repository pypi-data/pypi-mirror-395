"""
Pydantic models for cluster API endpoints.

This module contains auto-generated Pydantic v2 models for request and response
validation in the cluster API endpoints.
"""

from ..base.types import ProxmoxNode, ProxmoxVMID
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Literal

class ClusterGETResponse(BaseModel):
    """
    Response model for /cluster GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_ReplicationGETResponse(BaseModel):
    """
    Response model for /cluster/replication GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_ReplicationPOSTRequest(BaseModel):
    """
    Request model for /cluster/replication POST
    """
    comment: str | None = Field(
        max_length=4096,
        description="Description.",
    )
    disable: bool | int | str | None = Field(
        description="Flag to disable/deactivate the entry.",
    )
    id: str = Field(
        description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. \u0027\u003cGUEST\u003e-\u003cJOBNUM\u003e\u0027.",
    )
    rate: float | str | None = Field(
        ge=1.0,
        description="Rate limit in mbps (megabytes per second) as floating point number.",
    )
    remove_job: Literal["full", "local"] | None = Field(
        description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to \u0027full\u0027, it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.",
    )
    schedule: str | None = Field(
        default="*/15",
        max_length=128,
        description="Storage replication schedule. The format is a subset of `systemd` calendar events.",
    )
    source: ProxmoxNode | None = Field(
        description="For internal use, to detect if the guest was stolen.",
    )
    target: ProxmoxNode = Field(
        description="Target node.",
    )
    type: Literal["local"] = Field(
        description="Section type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Replication_IdDELETERequest(BaseModel):
    """
    Request model for /cluster/replication/{id} DELETE
    """
    force: bool | int | str | None = Field(
        default=0,
        description="Will remove the jobconfig entry, but will not cleanup.",
    )
    id: str = Field(
        description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. \u0027\u003cGUEST\u003e-\u003cJOBNUM\u003e\u0027.",
    )
    keep: bool | int | str | None = Field(
        default=0,
        description="Keep replicated data at target (do not remove).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Replication_IdGETRequest(BaseModel):
    """
    Request model for /cluster/replication/{id} GET
    """
    id: str = Field(
        description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. \u0027\u003cGUEST\u003e-\u003cJOBNUM\u003e\u0027.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Replication_IdGETResponse(BaseModel):
    """
    Response model for /cluster/replication/{id} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Replication_IdPUTRequest(BaseModel):
    """
    Request model for /cluster/replication/{id} PUT
    """
    comment: str | None = Field(
        max_length=4096,
        description="Description.",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    disable: bool | int | str | None = Field(
        description="Flag to disable/deactivate the entry.",
    )
    id: str = Field(
        description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. \u0027\u003cGUEST\u003e-\u003cJOBNUM\u003e\u0027.",
    )
    rate: float | str | None = Field(
        ge=1.0,
        description="Rate limit in mbps (megabytes per second) as floating point number.",
    )
    remove_job: Literal["full", "local"] | None = Field(
        description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to \u0027full\u0027, it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.",
    )
    schedule: str | None = Field(
        default="*/15",
        max_length=128,
        description="Storage replication schedule. The format is a subset of `systemd` calendar events.",
    )
    source: ProxmoxNode | None = Field(
        description="For internal use, to detect if the guest was stolen.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_MetricsGETResponse(BaseModel):
    """
    Response model for /cluster/metrics GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Metrics_ServerGETResponse(BaseModel):
    """
    Response model for /cluster/metrics/server GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Metrics_Server_IdDELETERequest(BaseModel):
    """
    Request model for /cluster/metrics/server/{id} DELETE
    """
    id: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Metrics_Server_IdGETRequest(BaseModel):
    """
    Request model for /cluster/metrics/server/{id} GET
    """
    id: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Metrics_Server_IdGETResponse(BaseModel):
    """
    Response model for /cluster/metrics/server/{id} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Metrics_Server_IdPOSTRequest(BaseModel):
    """
    Request model for /cluster/metrics/server/{id} POST
    """
    api_path_prefix: str | None = Field(
        description="An API path prefix inserted between \u0027\u003chost\u003e:\u003cport\u003e/\u0027 and \u0027/api2/\u0027. Can be useful if the InfluxDB service runs behind a reverse proxy.",
        serialization_alias="api-path-prefix",
    )
    bucket: str | None = Field(
        description="The InfluxDB bucket/db. Only necessary when using the http v2 api.",
    )
    disable: bool | int | str | None = Field(
        description="Flag to disable the plugin.",
    )
    id: str = Field(
        description="The ID of the entry.",
    )
    influxdbproto: Literal["http", "https", "udp"] | None = Field(
        default="udp",
    )
    max_body_size: int | str | None = Field(
        default=25000000,
        ge=1,
        description="InfluxDB max-body-size in bytes. Requests are batched up to this size.",
        serialization_alias="max-body-size",
    )
    mtu: int | str | None = Field(
        default=1500,
        ge=512,
        le=65536,
        description="MTU for metrics transmission over UDP",
    )
    organization: str | None = Field(
        description="The InfluxDB organization. Only necessary when using the http v2 api. Has no meaning when using v2 compatibility api.",
    )
    path: str | None = Field(
        description="root graphite path (ex: proxmox.mycluster.mykey)",
    )
    port: int | str = Field(
        ge=1,
        le=65536,
        description="server network port",
    )
    proto: Literal["tcp", "udp"] | None = Field(
        description="Protocol to send graphite data. TCP or UDP (default)",
    )
    server: str = Field(
        description="server dns name or IP address",
    )
    timeout: int | str | None = Field(
        default=1,
        ge=0,
        description="graphite TCP socket timeout (default=1)",
    )
    token: str | None = Field(
        description="The InfluxDB access token. Only necessary when using the http v2 api. If the v2 compatibility api is used, use \u0027user:password\u0027 instead.",
    )
    type: Literal["graphite", "influxdb"] = Field(
        description="Plugin type.",
    )
    verify_certificate: bool | int | str | None = Field(
        default=1,
        description="Set to 0 to disable certificate verification for https endpoints.",
        serialization_alias="verify-certificate",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Metrics_Server_IdPUTRequest(BaseModel):
    """
    Request model for /cluster/metrics/server/{id} PUT
    """
    api_path_prefix: str | None = Field(
        description="An API path prefix inserted between \u0027\u003chost\u003e:\u003cport\u003e/\u0027 and \u0027/api2/\u0027. Can be useful if the InfluxDB service runs behind a reverse proxy.",
        serialization_alias="api-path-prefix",
    )
    bucket: str | None = Field(
        description="The InfluxDB bucket/db. Only necessary when using the http v2 api.",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    disable: bool | int | str | None = Field(
        description="Flag to disable the plugin.",
    )
    id: str = Field(
        description="The ID of the entry.",
    )
    influxdbproto: Literal["http", "https", "udp"] | None = Field(
        default="udp",
    )
    max_body_size: int | str | None = Field(
        default=25000000,
        ge=1,
        description="InfluxDB max-body-size in bytes. Requests are batched up to this size.",
        serialization_alias="max-body-size",
    )
    mtu: int | str | None = Field(
        default=1500,
        ge=512,
        le=65536,
        description="MTU for metrics transmission over UDP",
    )
    organization: str | None = Field(
        description="The InfluxDB organization. Only necessary when using the http v2 api. Has no meaning when using v2 compatibility api.",
    )
    path: str | None = Field(
        description="root graphite path (ex: proxmox.mycluster.mykey)",
    )
    port: int | str = Field(
        ge=1,
        le=65536,
        description="server network port",
    )
    proto: Literal["tcp", "udp"] | None = Field(
        description="Protocol to send graphite data. TCP or UDP (default)",
    )
    server: str = Field(
        description="server dns name or IP address",
    )
    timeout: int | str | None = Field(
        default=1,
        ge=0,
        description="graphite TCP socket timeout (default=1)",
    )
    token: str | None = Field(
        description="The InfluxDB access token. Only necessary when using the http v2 api. If the v2 compatibility api is used, use \u0027user:password\u0027 instead.",
    )
    verify_certificate: bool | int | str | None = Field(
        default=1,
        description="Set to 0 to disable certificate verification for https endpoints.",
        serialization_alias="verify-certificate",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_ConfigGETResponse(BaseModel):
    """
    Response model for /cluster/config GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_ConfigPOSTRequest(BaseModel):
    """
    Request model for /cluster/config POST
    """
    clustername: ProxmoxNode = Field(
        max_length=15,
        description="The name of the cluster.",
    )
    link_n_: str | None = Field(
        description="Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)",
        serialization_alias="link[n]",
    )
    nodeid: int | str | None = Field(
        ge=1,
        description="Node id for this node.",
    )
    votes: int | str | None = Field(
        ge=1,
        description="Number of votes for this node.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_ConfigPOSTResponse(BaseModel):
    """
    Response model for /cluster/config POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_ApiversionGETResponse(BaseModel):
    """
    Response model for /cluster/config/apiversion GET
    """
    data: int | str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_NodesGETResponse(BaseModel):
    """
    Response model for /cluster/config/nodes GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_Nodes_NodeDELETERequest(BaseModel):
    """
    Request model for /cluster/config/nodes/{node} DELETE
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_Nodes_NodePOSTRequest(BaseModel):
    """
    Request model for /cluster/config/nodes/{node} POST
    """
    apiversion: int | str | None = Field(
        description="The JOIN_API_VERSION of the new node.",
    )
    force: bool | int | str | None = Field(
        description="Do not throw error if node already exists.",
    )
    link_n_: str | None = Field(
        description="Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)",
        serialization_alias="link[n]",
    )
    new_node_ip: str | None = Field(
        description="IP Address of node to add. Used as fallback if no links are given.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    nodeid: int | str | None = Field(
        ge=1,
        description="Node id for this node.",
    )
    votes: int | str | None = Field(
        ge=0,
        description="Number of votes for this node",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_Nodes_NodePOSTResponse(BaseModel):
    """
    Response model for /cluster/config/nodes/{node} POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_JoinGETRequest(BaseModel):
    """
    Request model for /cluster/config/join GET
    """
    node: ProxmoxNode | None = Field(
        default="current connected node",
        description="The node for which the joinee gets the nodeinfo. ",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_JoinGETResponse(BaseModel):
    """
    Response model for /cluster/config/join GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_JoinPOSTRequest(BaseModel):
    """
    Request model for /cluster/config/join POST
    """
    fingerprint: str = Field(
        description="Certificate SHA 256 fingerprint.",
    )
    force: bool | int | str | None = Field(
        description="Do not throw error if node already exists.",
    )
    hostname: str = Field(
        description="Hostname (or IP) of an existing cluster member.",
    )
    link_n_: str | None = Field(
        description="Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)",
        serialization_alias="link[n]",
    )
    nodeid: int | str | None = Field(
        ge=1,
        description="Node id for this node.",
    )
    password: str = Field(
        max_length=128,
        description="Superuser (root) password of peer node.",
    )
    votes: int | str | None = Field(
        ge=0,
        description="Number of votes for this node",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_JoinPOSTResponse(BaseModel):
    """
    Response model for /cluster/config/join POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_TotemGETResponse(BaseModel):
    """
    Response model for /cluster/config/totem GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Config_QdeviceGETResponse(BaseModel):
    """
    Response model for /cluster/config/qdevice GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_FirewallGETResponse(BaseModel):
    """
    Response model for /cluster/firewall GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_GroupsGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/groups GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_GroupsPOSTRequest(BaseModel):
    """
    Request model for /cluster/firewall/groups POST
    """
    comment: str | None = Field(
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    group: str = Field(
        max_length=18,
        description="Security Group name.",
    )
    rename: str | None = Field(
        max_length=18,
        description="Rename/update an existing security group. You can set \u0027rename\u0027 to the same value as \u0027name\u0027 to update the \u0027comment\u0027 of an existing group.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Groups_GroupDELETERequest(BaseModel):
    """
    Request model for /cluster/firewall/groups/{group} DELETE
    """
    group: str = Field(
        max_length=18,
        description="Security Group name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Groups_GroupGETRequest(BaseModel):
    """
    Request model for /cluster/firewall/groups/{group} GET
    """
    group: str = Field(
        max_length=18,
        description="Security Group name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Groups_GroupGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/groups/{group} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Groups_GroupPOSTRequest(BaseModel):
    """
    Request model for /cluster/firewall/groups/{group} POST
    """
    action: str = Field(
        max_length=20,
        description="Rule action (\u0027ACCEPT\u0027, \u0027DROP\u0027, \u0027REJECT\u0027) or security group name.",
    )
    comment: str | None = Field(
        description="Descriptive comment.",
    )
    dest: str | None = Field(
        max_length=512,
        description="Restrict packet destination address. This can refer to a single IP address, an IP set (\u0027+ipsetname\u0027) or an IP alias definition. You can also specify an address range like \u002720.34.101.207-201.3.9.99\u0027, or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    dport: str | None = Field(
        description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in \u0027/etc/services\u0027. Port ranges can be specified with \u0027\\d+:\\d+\u0027, for example \u002780:85\u0027, and you can use comma separated list to match several ports or ranges.",
    )
    enable: int | str | None = Field(
        ge=0,
        description="Flag to enable/disable a rule.",
    )
    group: str = Field(
        max_length=18,
        description="Security Group name.",
    )
    icmp_type: str | None = Field(
        description="Specify icmp-type. Only valid if proto equals \u0027icmp\u0027.",
        serialization_alias="icmp-type",
    )
    iface: str | None = Field(
        max_length=20,
        description="Network interface name. You have to use network configuration key names for VMs and containers (\u0027net\\d+\u0027). Host related rules can use arbitrary strings.",
    )
    log: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for firewall rule.",
    )
    macro: str | None = Field(
        max_length=128,
        description="Use predefined standard macro.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )
    proto: str | None = Field(
        description="IP protocol. You can use protocol names (\u0027tcp\u0027/\u0027udp\u0027) or simple numbers, as defined in \u0027/etc/protocols\u0027.",
    )
    source: str | None = Field(
        max_length=512,
        description="Restrict packet source address. This can refer to a single IP address, an IP set (\u0027+ipsetname\u0027) or an IP alias definition. You can also specify an address range like \u002720.34.101.207-201.3.9.99\u0027, or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.",
    )
    sport: str | None = Field(
        description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in \u0027/etc/services\u0027. Port ranges can be specified with \u0027\\d+:\\d+\u0027, for example \u002780:85\u0027, and you can use comma separated list to match several ports or ranges.",
    )
    type: Literal["group", "in", "out"] = Field(
        description="Rule type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Groups_Group_PosDELETERequest(BaseModel):
    """
    Request model for /cluster/firewall/groups/{group}/{pos} DELETE
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    group: str = Field(
        max_length=18,
        description="Security Group name.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Groups_Group_PosGETRequest(BaseModel):
    """
    Request model for /cluster/firewall/groups/{group}/{pos} GET
    """
    group: str = Field(
        max_length=18,
        description="Security Group name.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Groups_Group_PosGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/groups/{group}/{pos} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Groups_Group_PosPUTRequest(BaseModel):
    """
    Request model for /cluster/firewall/groups/{group}/{pos} PUT
    """
    action: str | None = Field(
        max_length=20,
        description="Rule action (\u0027ACCEPT\u0027, \u0027DROP\u0027, \u0027REJECT\u0027) or security group name.",
    )
    comment: str | None = Field(
        description="Descriptive comment.",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    dest: str | None = Field(
        max_length=512,
        description="Restrict packet destination address. This can refer to a single IP address, an IP set (\u0027+ipsetname\u0027) or an IP alias definition. You can also specify an address range like \u002720.34.101.207-201.3.9.99\u0027, or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    dport: str | None = Field(
        description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in \u0027/etc/services\u0027. Port ranges can be specified with \u0027\\d+:\\d+\u0027, for example \u002780:85\u0027, and you can use comma separated list to match several ports or ranges.",
    )
    enable: int | str | None = Field(
        ge=0,
        description="Flag to enable/disable a rule.",
    )
    group: str = Field(
        max_length=18,
        description="Security Group name.",
    )
    icmp_type: str | None = Field(
        description="Specify icmp-type. Only valid if proto equals \u0027icmp\u0027.",
        serialization_alias="icmp-type",
    )
    iface: str | None = Field(
        max_length=20,
        description="Network interface name. You have to use network configuration key names for VMs and containers (\u0027net\\d+\u0027). Host related rules can use arbitrary strings.",
    )
    log: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for firewall rule.",
    )
    macro: str | None = Field(
        max_length=128,
        description="Use predefined standard macro.",
    )
    moveto: int | str | None = Field(
        ge=0,
        description="Move rule to new position \u003cmoveto\u003e. Other arguments are ignored.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )
    proto: str | None = Field(
        description="IP protocol. You can use protocol names (\u0027tcp\u0027/\u0027udp\u0027) or simple numbers, as defined in \u0027/etc/protocols\u0027.",
    )
    source: str | None = Field(
        max_length=512,
        description="Restrict packet source address. This can refer to a single IP address, an IP set (\u0027+ipsetname\u0027) or an IP alias definition. You can also specify an address range like \u002720.34.101.207-201.3.9.99\u0027, or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.",
    )
    sport: str | None = Field(
        description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in \u0027/etc/services\u0027. Port ranges can be specified with \u0027\\d+:\\d+\u0027, for example \u002780:85\u0027, and you can use comma separated list to match several ports or ranges.",
    )
    type: Literal["group", "in", "out"] | None = Field(
        description="Rule type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_RulesGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/rules GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_RulesPOSTRequest(BaseModel):
    """
    Request model for /cluster/firewall/rules POST
    """
    action: str = Field(
        max_length=20,
        description="Rule action (\u0027ACCEPT\u0027, \u0027DROP\u0027, \u0027REJECT\u0027) or security group name.",
    )
    comment: str | None = Field(
        description="Descriptive comment.",
    )
    dest: str | None = Field(
        max_length=512,
        description="Restrict packet destination address. This can refer to a single IP address, an IP set (\u0027+ipsetname\u0027) or an IP alias definition. You can also specify an address range like \u002720.34.101.207-201.3.9.99\u0027, or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    dport: str | None = Field(
        description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in \u0027/etc/services\u0027. Port ranges can be specified with \u0027\\d+:\\d+\u0027, for example \u002780:85\u0027, and you can use comma separated list to match several ports or ranges.",
    )
    enable: int | str | None = Field(
        ge=0,
        description="Flag to enable/disable a rule.",
    )
    icmp_type: str | None = Field(
        description="Specify icmp-type. Only valid if proto equals \u0027icmp\u0027.",
        serialization_alias="icmp-type",
    )
    iface: str | None = Field(
        max_length=20,
        description="Network interface name. You have to use network configuration key names for VMs and containers (\u0027net\\d+\u0027). Host related rules can use arbitrary strings.",
    )
    log: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for firewall rule.",
    )
    macro: str | None = Field(
        max_length=128,
        description="Use predefined standard macro.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )
    proto: str | None = Field(
        description="IP protocol. You can use protocol names (\u0027tcp\u0027/\u0027udp\u0027) or simple numbers, as defined in \u0027/etc/protocols\u0027.",
    )
    source: str | None = Field(
        max_length=512,
        description="Restrict packet source address. This can refer to a single IP address, an IP set (\u0027+ipsetname\u0027) or an IP alias definition. You can also specify an address range like \u002720.34.101.207-201.3.9.99\u0027, or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.",
    )
    sport: str | None = Field(
        description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in \u0027/etc/services\u0027. Port ranges can be specified with \u0027\\d+:\\d+\u0027, for example \u002780:85\u0027, and you can use comma separated list to match several ports or ranges.",
    )
    type: Literal["group", "in", "out"] = Field(
        description="Rule type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Rules_PosDELETERequest(BaseModel):
    """
    Request model for /cluster/firewall/rules/{pos} DELETE
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Rules_PosGETRequest(BaseModel):
    """
    Request model for /cluster/firewall/rules/{pos} GET
    """
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Rules_PosGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/rules/{pos} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Rules_PosPUTRequest(BaseModel):
    """
    Request model for /cluster/firewall/rules/{pos} PUT
    """
    action: str | None = Field(
        max_length=20,
        description="Rule action (\u0027ACCEPT\u0027, \u0027DROP\u0027, \u0027REJECT\u0027) or security group name.",
    )
    comment: str | None = Field(
        description="Descriptive comment.",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    dest: str | None = Field(
        max_length=512,
        description="Restrict packet destination address. This can refer to a single IP address, an IP set (\u0027+ipsetname\u0027) or an IP alias definition. You can also specify an address range like \u002720.34.101.207-201.3.9.99\u0027, or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    dport: str | None = Field(
        description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in \u0027/etc/services\u0027. Port ranges can be specified with \u0027\\d+:\\d+\u0027, for example \u002780:85\u0027, and you can use comma separated list to match several ports or ranges.",
    )
    enable: int | str | None = Field(
        ge=0,
        description="Flag to enable/disable a rule.",
    )
    icmp_type: str | None = Field(
        description="Specify icmp-type. Only valid if proto equals \u0027icmp\u0027.",
        serialization_alias="icmp-type",
    )
    iface: str | None = Field(
        max_length=20,
        description="Network interface name. You have to use network configuration key names for VMs and containers (\u0027net\\d+\u0027). Host related rules can use arbitrary strings.",
    )
    log: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for firewall rule.",
    )
    macro: str | None = Field(
        max_length=128,
        description="Use predefined standard macro.",
    )
    moveto: int | str | None = Field(
        ge=0,
        description="Move rule to new position \u003cmoveto\u003e. Other arguments are ignored.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )
    proto: str | None = Field(
        description="IP protocol. You can use protocol names (\u0027tcp\u0027/\u0027udp\u0027) or simple numbers, as defined in \u0027/etc/protocols\u0027.",
    )
    source: str | None = Field(
        max_length=512,
        description="Restrict packet source address. This can refer to a single IP address, an IP set (\u0027+ipsetname\u0027) or an IP alias definition. You can also specify an address range like \u002720.34.101.207-201.3.9.99\u0027, or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.",
    )
    sport: str | None = Field(
        description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in \u0027/etc/services\u0027. Port ranges can be specified with \u0027\\d+:\\d+\u0027, for example \u002780:85\u0027, and you can use comma separated list to match several ports or ranges.",
    )
    type: Literal["group", "in", "out"] | None = Field(
        description="Rule type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_IpsetGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/ipset GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_IpsetPOSTRequest(BaseModel):
    """
    Request model for /cluster/firewall/ipset POST
    """
    comment: str | None = Field(
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    rename: str | None = Field(
        max_length=64,
        description="Rename an existing IPSet. You can set \u0027rename\u0027 to the same value as \u0027name\u0027 to update the \u0027comment\u0027 of an existing IPSet.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Ipset_NameDELETERequest(BaseModel):
    """
    Request model for /cluster/firewall/ipset/{name} DELETE
    """
    force: bool | int | str | None = Field(
        description="Delete all members of the IPSet, if there are any.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Ipset_NameGETRequest(BaseModel):
    """
    Request model for /cluster/firewall/ipset/{name} GET
    """
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Ipset_NameGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/ipset/{name} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Ipset_NamePOSTRequest(BaseModel):
    """
    Request model for /cluster/firewall/ipset/{name} POST
    """
    cidr: str = Field(
        description="Network/IP specification in CIDR format.",
    )
    comment: str | None = Field(
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    nomatch: bool | int | str | None = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Ipset_Name_CidrDELETERequest(BaseModel):
    """
    Request model for /cluster/firewall/ipset/{name}/{cidr} DELETE
    """
    cidr: str = Field(
        description="Network/IP specification in CIDR format.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Ipset_Name_CidrGETRequest(BaseModel):
    """
    Request model for /cluster/firewall/ipset/{name}/{cidr} GET
    """
    cidr: str = Field(
        description="Network/IP specification in CIDR format.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Ipset_Name_CidrGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/ipset/{name}/{cidr} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Ipset_Name_CidrPUTRequest(BaseModel):
    """
    Request model for /cluster/firewall/ipset/{name}/{cidr} PUT
    """
    cidr: str = Field(
        description="Network/IP specification in CIDR format.",
    )
    comment: str | None = Field(
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    nomatch: bool | int | str | None = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_AliasesGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/aliases GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_AliasesPOSTRequest(BaseModel):
    """
    Request model for /cluster/firewall/aliases POST
    """
    cidr: str = Field(
        description="Network/IP specification in CIDR format.",
    )
    comment: str | None = Field(
    )
    name: str = Field(
        max_length=64,
        description="Alias name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Aliases_NameDELETERequest(BaseModel):
    """
    Request model for /cluster/firewall/aliases/{name} DELETE
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    name: str = Field(
        max_length=64,
        description="Alias name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Aliases_NameGETRequest(BaseModel):
    """
    Request model for /cluster/firewall/aliases/{name} GET
    """
    name: str = Field(
        max_length=64,
        description="Alias name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Aliases_NameGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/aliases/{name} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_Aliases_NamePUTRequest(BaseModel):
    """
    Request model for /cluster/firewall/aliases/{name} PUT
    """
    cidr: str = Field(
        description="Network/IP specification in CIDR format.",
    )
    comment: str | None = Field(
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    name: str = Field(
        max_length=64,
        description="Alias name.",
    )
    rename: str | None = Field(
        max_length=64,
        description="Rename an existing alias.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_OptionsGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/options GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_OptionsPUTRequest(BaseModel):
    """
    Request model for /cluster/firewall/options PUT
    """
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    ebtables: bool | int | str | None = Field(
        default=1,
        description="Enable ebtables rules cluster wide.",
    )
    enable: int | str | None = Field(
        ge=0,
        description="Enable or disable the firewall cluster wide.",
    )
    log_ratelimit: str | None = Field(
        description="Log ratelimiting settings",
    )
    policy_in: Literal["ACCEPT", "DROP", "REJECT"] | None = Field(
        description="Input policy.",
    )
    policy_out: Literal["ACCEPT", "DROP", "REJECT"] | None = Field(
        description="Output policy.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_MacrosGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/macros GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_RefsGETRequest(BaseModel):
    """
    Request model for /cluster/firewall/refs GET
    """
    type: Literal["alias", "ipset"] | None = Field(
        description="Only list references of specified type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Firewall_RefsGETResponse(BaseModel):
    """
    Response model for /cluster/firewall/refs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_BackupGETResponse(BaseModel):
    """
    Response model for /cluster/backup GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_BackupPOSTRequest(BaseModel):
    """
    Request model for /cluster/backup POST
    """
    all: bool | int | str | None = Field(
        default=0,
        description="Backup all known guest systems on this host.",
    )
    bwlimit: int | str | None = Field(
        default=0,
        ge=0,
        description="Limit I/O bandwidth (KBytes per second).",
    )
    comment: str | None = Field(
        max_length=512,
        description="Description for the Job.",
    )
    compress: Literal["0", "1", "gzip", "lzo", "zstd"] | None = Field(
        default="0",
        description="Compress dump file.",
    )
    dow: str | None = Field(
        default="mon,tue,wed,thu,fri,sat,sun",
        description="Day of week selection.",
    )
    dumpdir: str | None = Field(
        description="Store resulting files to specified directory.",
    )
    enabled: bool | int | str | None = Field(
        default="1",
        description="Enable or disable the job.",
    )
    exclude: list[ProxmoxVMID] | None = Field(
        description="Exclude specified guest systems (assumes --all)",
    )
    exclude_path: str | None = Field(
        description="Exclude certain files/directories (shell globs). Paths starting with \u0027/\u0027 are anchored to the container\u0027s root,  other paths match relative to each subdirectory.",
        serialization_alias="exclude-path",
    )
    id: str | None = Field(
        description="Job ID (will be autogenerated).",
    )
    ionice: int | str | None = Field(
        default=7,
        ge=0,
        le=8,
        description="Set CFQ ionice priority.",
    )
    lockwait: int | str | None = Field(
        default=180,
        ge=0,
        description="Maximal time to wait for the global lock (minutes).",
    )
    mailnotification: Literal["always", "failure"] | None = Field(
        default="always",
        description="Specify when to send an email",
    )
    mailto: str | None = Field(
        description="Comma-separated list of email addresses or users that should receive email notifications.",
    )
    maxfiles: int | str | None = Field(
        ge=1,
        description="Deprecated: use \u0027prune-backups\u0027 instead. Maximal number of backup files per guest system.",
    )
    mode: Literal["snapshot", "stop", "suspend"] | None = Field(
        default="snapshot",
        description="Backup mode.",
    )
    node: ProxmoxNode | None = Field(
        description="Only run if executed on this node.",
    )
    notes_template: str | None = Field(
        max_length=1024,
        description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as \u0027\\n\u0027 and \u0027\\\\\u0027 respectively.",
        serialization_alias="notes-template",
    )
    performance: str | None = Field(
        description="Other performance-related settings.",
    )
    pigz: int | str | None = Field(
        default=0,
        description="Use pigz instead of gzip when N\u003e0. N=1 uses half of cores, N\u003e1 uses N as thread count.",
    )
    pool: str | None = Field(
        description="Backup all known guest systems included in the specified pool.",
    )
    protected: bool | int | str | None = Field(
        description="If true, mark backup(s) as protected.",
    )
    prune_backups: str | None = Field(
        default="keep-all=1",
        description="Use these retention options instead of those from the storage configuration.",
        serialization_alias="prune-backups",
    )
    quiet: bool | int | str | None = Field(
        default=0,
        description="Be quiet.",
    )
    remove: bool | int | str | None = Field(
        default=1,
        description="Prune older backups according to \u0027prune-backups\u0027.",
    )
    repeat_missed: bool | int | str | None = Field(
        default=0,
        description="If true, the job will be run as soon as possible if it was missed while the scheduler was not running.",
        serialization_alias="repeat-missed",
    )
    schedule: str | None = Field(
        max_length=128,
        description="Backup schedule. The format is a subset of `systemd` calendar events.",
    )
    script: str | None = Field(
        description="Use specified hook script.",
    )
    starttime: str | None = Field(
        description="Job Start time.",
    )
    stdexcludes: bool | int | str | None = Field(
        default=1,
        description="Exclude temporary files and logs.",
    )
    stop: bool | int | str | None = Field(
        default=0,
        description="Stop running backup jobs on this host.",
    )
    stopwait: int | str | None = Field(
        default=10,
        ge=0,
        description="Maximal time to wait until a guest system is stopped (minutes).",
    )
    storage: str | None = Field(
        description="Store resulting file to this storage.",
    )
    tmpdir: str | None = Field(
        description="Store temporary files to specified directory.",
    )
    vmid: list[ProxmoxVMID] | None = Field(
        description="The ID of the guest system you want to backup.",
    )
    zstd: int | str | None = Field(
        default=1,
        description="Zstd threads. N=0 uses half of the available cores, N\u003e0 uses N as thread count.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Backup_IdDELETERequest(BaseModel):
    """
    Request model for /cluster/backup/{id} DELETE
    """
    id: str = Field(
        max_length=50,
        description="The job ID.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Backup_IdGETRequest(BaseModel):
    """
    Request model for /cluster/backup/{id} GET
    """
    id: str = Field(
        max_length=50,
        description="The job ID.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Backup_IdGETResponse(BaseModel):
    """
    Response model for /cluster/backup/{id} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Backup_IdPUTRequest(BaseModel):
    """
    Request model for /cluster/backup/{id} PUT
    """
    all: bool | int | str | None = Field(
        default=0,
        description="Backup all known guest systems on this host.",
    )
    bwlimit: int | str | None = Field(
        default=0,
        ge=0,
        description="Limit I/O bandwidth (KBytes per second).",
    )
    comment: str | None = Field(
        max_length=512,
        description="Description for the Job.",
    )
    compress: Literal["0", "1", "gzip", "lzo", "zstd"] | None = Field(
        default="0",
        description="Compress dump file.",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    dow: str | None = Field(
        description="Day of week selection.",
    )
    dumpdir: str | None = Field(
        description="Store resulting files to specified directory.",
    )
    enabled: bool | int | str | None = Field(
        default="1",
        description="Enable or disable the job.",
    )
    exclude: list[ProxmoxVMID] | None = Field(
        description="Exclude specified guest systems (assumes --all)",
    )
    exclude_path: str | None = Field(
        description="Exclude certain files/directories (shell globs). Paths starting with \u0027/\u0027 are anchored to the container\u0027s root,  other paths match relative to each subdirectory.",
        serialization_alias="exclude-path",
    )
    id: str = Field(
        max_length=50,
        description="The job ID.",
    )
    ionice: int | str | None = Field(
        default=7,
        ge=0,
        le=8,
        description="Set CFQ ionice priority.",
    )
    lockwait: int | str | None = Field(
        default=180,
        ge=0,
        description="Maximal time to wait for the global lock (minutes).",
    )
    mailnotification: Literal["always", "failure"] | None = Field(
        default="always",
        description="Specify when to send an email",
    )
    mailto: str | None = Field(
        description="Comma-separated list of email addresses or users that should receive email notifications.",
    )
    maxfiles: int | str | None = Field(
        ge=1,
        description="Deprecated: use \u0027prune-backups\u0027 instead. Maximal number of backup files per guest system.",
    )
    mode: Literal["snapshot", "stop", "suspend"] | None = Field(
        default="snapshot",
        description="Backup mode.",
    )
    node: ProxmoxNode | None = Field(
        description="Only run if executed on this node.",
    )
    notes_template: str | None = Field(
        max_length=1024,
        description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as \u0027\\n\u0027 and \u0027\\\\\u0027 respectively.",
        serialization_alias="notes-template",
    )
    performance: str | None = Field(
        description="Other performance-related settings.",
    )
    pigz: int | str | None = Field(
        default=0,
        description="Use pigz instead of gzip when N\u003e0. N=1 uses half of cores, N\u003e1 uses N as thread count.",
    )
    pool: str | None = Field(
        description="Backup all known guest systems included in the specified pool.",
    )
    protected: bool | int | str | None = Field(
        description="If true, mark backup(s) as protected.",
    )
    prune_backups: str | None = Field(
        default="keep-all=1",
        description="Use these retention options instead of those from the storage configuration.",
        serialization_alias="prune-backups",
    )
    quiet: bool | int | str | None = Field(
        default=0,
        description="Be quiet.",
    )
    remove: bool | int | str | None = Field(
        default=1,
        description="Prune older backups according to \u0027prune-backups\u0027.",
    )
    repeat_missed: bool | int | str | None = Field(
        default=0,
        description="If true, the job will be run as soon as possible if it was missed while the scheduler was not running.",
        serialization_alias="repeat-missed",
    )
    schedule: str | None = Field(
        max_length=128,
        description="Backup schedule. The format is a subset of `systemd` calendar events.",
    )
    script: str | None = Field(
        description="Use specified hook script.",
    )
    starttime: str | None = Field(
        description="Job Start time.",
    )
    stdexcludes: bool | int | str | None = Field(
        default=1,
        description="Exclude temporary files and logs.",
    )
    stop: bool | int | str | None = Field(
        default=0,
        description="Stop running backup jobs on this host.",
    )
    stopwait: int | str | None = Field(
        default=10,
        ge=0,
        description="Maximal time to wait until a guest system is stopped (minutes).",
    )
    storage: str | None = Field(
        description="Store resulting file to this storage.",
    )
    tmpdir: str | None = Field(
        description="Store temporary files to specified directory.",
    )
    vmid: list[ProxmoxVMID] | None = Field(
        description="The ID of the guest system you want to backup.",
    )
    zstd: int | str | None = Field(
        default=1,
        description="Zstd threads. N=0 uses half of the available cores, N\u003e0 uses N as thread count.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Backup_Id_Included_VolumesGETRequest(BaseModel):
    """
    Request model for /cluster/backup/{id}/included_volumes GET
    """
    id: str = Field(
        max_length=50,
        description="The job ID.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Backup_Id_Included_VolumesGETResponse(BaseModel):
    """
    Response model for /cluster/backup/{id}/included_volumes GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Backup_InfoGETResponse(BaseModel):
    """
    Response model for /cluster/backup-info GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Backup_Info_Not_Backed_UpGETResponse(BaseModel):
    """
    Response model for /cluster/backup-info/not-backed-up GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_HaGETResponse(BaseModel):
    """
    Response model for /cluster/ha GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_ResourcesGETRequest(BaseModel):
    """
    Request model for /cluster/ha/resources GET
    """
    type: Literal["ct", "vm"] | None = Field(
        description="Only list resources of specific type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_ResourcesGETResponse(BaseModel):
    """
    Response model for /cluster/ha/resources GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_ResourcesPOSTRequest(BaseModel):
    """
    Request model for /cluster/ha/resources POST
    """
    comment: str | None = Field(
        max_length=4096,
        description="Description.",
    )
    group: str | None = Field(
        description="The HA group identifier.",
    )
    max_relocate: int | str | None = Field(
        default=1,
        ge=0,
        description="Maximal number of service relocate tries when a service failes to start.",
    )
    max_restart: int | str | None = Field(
        default=1,
        ge=0,
        description="Maximal number of tries to restart the service on a node after its start failed.",
    )
    sid: str = Field(
        description="HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).",
    )
    state: Literal["disabled", "enabled", "ignored", "started", "stopped"] | None = Field(
        default="started",
        description="Requested resource state.",
    )
    type: Literal["ct", "vm"] | None = Field(
        description="Resource type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Resources_SidDELETERequest(BaseModel):
    """
    Request model for /cluster/ha/resources/{sid} DELETE
    """
    sid: str = Field(
        description="HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Resources_SidGETRequest(BaseModel):
    """
    Request model for /cluster/ha/resources/{sid} GET
    """
    sid: str = Field(
        description="HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Resources_SidGETResponse(BaseModel):
    """
    Response model for /cluster/ha/resources/{sid} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Resources_SidPUTRequest(BaseModel):
    """
    Request model for /cluster/ha/resources/{sid} PUT
    """
    comment: str | None = Field(
        max_length=4096,
        description="Description.",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    group: str | None = Field(
        description="The HA group identifier.",
    )
    max_relocate: int | str | None = Field(
        default=1,
        ge=0,
        description="Maximal number of service relocate tries when a service failes to start.",
    )
    max_restart: int | str | None = Field(
        default=1,
        ge=0,
        description="Maximal number of tries to restart the service on a node after its start failed.",
    )
    sid: str = Field(
        description="HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).",
    )
    state: Literal["disabled", "enabled", "ignored", "started", "stopped"] | None = Field(
        default="started",
        description="Requested resource state.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Resources_Sid_MigratePOSTRequest(BaseModel):
    """
    Request model for /cluster/ha/resources/{sid}/migrate POST
    """
    node: ProxmoxNode = Field(
        description="Target node.",
    )
    sid: str = Field(
        description="HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Resources_Sid_RelocatePOSTRequest(BaseModel):
    """
    Request model for /cluster/ha/resources/{sid}/relocate POST
    """
    node: ProxmoxNode = Field(
        description="Target node.",
    )
    sid: str = Field(
        description="HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_GroupsGETResponse(BaseModel):
    """
    Response model for /cluster/ha/groups GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_GroupsPOSTRequest(BaseModel):
    """
    Request model for /cluster/ha/groups POST
    """
    comment: str | None = Field(
        max_length=4096,
        description="Description.",
    )
    group: str = Field(
        description="The HA group identifier.",
    )
    nodes: str = Field(
        description="List of cluster node names with optional priority.",
    )
    nofailback: bool | int | str | None = Field(
        default=0,
        description="The CRM tries to run services on the node with the highest priority. If a node with higher priority comes online, the CRM migrates the service to that node. Enabling nofailback prevents that behavior.",
    )
    restricted: bool | int | str | None = Field(
        default=0,
        description="Resources bound to restricted groups may only run on nodes defined by the group.",
    )
    type: Literal["group"] | None = Field(
        description="Group type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Groups_GroupDELETERequest(BaseModel):
    """
    Request model for /cluster/ha/groups/{group} DELETE
    """
    group: str = Field(
        description="The HA group identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Groups_GroupGETRequest(BaseModel):
    """
    Request model for /cluster/ha/groups/{group} GET
    """
    group: str = Field(
        description="The HA group identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Groups_GroupGETResponse(BaseModel):
    """
    Response model for /cluster/ha/groups/{group} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Groups_GroupPUTRequest(BaseModel):
    """
    Request model for /cluster/ha/groups/{group} PUT
    """
    comment: str | None = Field(
        max_length=4096,
        description="Description.",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    group: str = Field(
        description="The HA group identifier.",
    )
    nodes: str | None = Field(
        description="List of cluster node names with optional priority.",
    )
    nofailback: bool | int | str | None = Field(
        default=0,
        description="The CRM tries to run services on the node with the highest priority. If a node with higher priority comes online, the CRM migrates the service to that node. Enabling nofailback prevents that behavior.",
    )
    restricted: bool | int | str | None = Field(
        default=0,
        description="Resources bound to restricted groups may only run on nodes defined by the group.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_StatusGETResponse(BaseModel):
    """
    Response model for /cluster/ha/status GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Status_CurrentGETResponse(BaseModel):
    """
    Response model for /cluster/ha/status/current GET
    """
    data: list[Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ha_Status_Manager_StatusGETResponse(BaseModel):
    """
    Response model for /cluster/ha/status/manager_status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_AcmeGETResponse(BaseModel):
    """
    Response model for /cluster/acme GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_PluginsGETRequest(BaseModel):
    """
    Request model for /cluster/acme/plugins GET
    """
    type: Literal["dns", "standalone"] | None = Field(
        description="Only list ACME plugins of a specific type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_PluginsGETResponse(BaseModel):
    """
    Response model for /cluster/acme/plugins GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_PluginsPOSTRequest(BaseModel):
    """
    Request model for /cluster/acme/plugins POST
    """
    api: str | None = Field(
        description="API plugin name",
    )
    data: str | None = Field(
        description="DNS plugin data. (base64 encoded)",
    )
    disable: bool | int | str | None = Field(
        description="Flag to disable the config.",
    )
    id: str = Field(
        description="ACME Plugin ID name",
    )
    nodes: list[ProxmoxNode] | None = Field(
        description="List of cluster node names.",
    )
    type: Literal["dns", "standalone"] = Field(
        description="ACME challenge type.",
    )
    validation_delay: int | str | None = Field(
        default=30,
        ge=0,
        le=172800,
        description="Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.",
        serialization_alias="validation-delay",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Plugins_IdDELETERequest(BaseModel):
    """
    Request model for /cluster/acme/plugins/{id} DELETE
    """
    id: str = Field(
        description="Unique identifier for ACME plugin instance.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Plugins_IdGETRequest(BaseModel):
    """
    Request model for /cluster/acme/plugins/{id} GET
    """
    id: str = Field(
        description="Unique identifier for ACME plugin instance.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Plugins_IdGETResponse(BaseModel):
    """
    Response model for /cluster/acme/plugins/{id} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Plugins_IdPUTRequest(BaseModel):
    """
    Request model for /cluster/acme/plugins/{id} PUT
    """
    api: str | None = Field(
        description="API plugin name",
    )
    data: str | None = Field(
        description="DNS plugin data. (base64 encoded)",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    disable: bool | int | str | None = Field(
        description="Flag to disable the config.",
    )
    id: str = Field(
        description="ACME Plugin ID name",
    )
    nodes: list[ProxmoxNode] | None = Field(
        description="List of cluster node names.",
    )
    validation_delay: int | str | None = Field(
        default=30,
        ge=0,
        le=172800,
        description="Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.",
        serialization_alias="validation-delay",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_AccountGETResponse(BaseModel):
    """
    Response model for /cluster/acme/account GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_AccountPOSTRequest(BaseModel):
    """
    Request model for /cluster/acme/account POST
    """
    contact: str = Field(
        description="Contact email addresses.",
    )
    directory: str | None = Field(
        default="https://acme-v02.api.letsencrypt.org/directory",
        description="URL of ACME CA directory endpoint.",
    )
    name: str | None = Field(
        default="default",
        description="ACME account config file name.",
    )
    tos_url: str | None = Field(
        description="URL of CA TermsOfService - setting this indicates agreement.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_AccountPOSTResponse(BaseModel):
    """
    Response model for /cluster/acme/account POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Account_NameDELETERequest(BaseModel):
    """
    Request model for /cluster/acme/account/{name} DELETE
    """
    name: str | None = Field(
        default="default",
        description="ACME account config file name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Account_NameDELETEResponse(BaseModel):
    """
    Response model for /cluster/acme/account/{name} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Account_NameGETRequest(BaseModel):
    """
    Request model for /cluster/acme/account/{name} GET
    """
    name: str | None = Field(
        default="default",
        description="ACME account config file name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Account_NameGETResponse(BaseModel):
    """
    Response model for /cluster/acme/account/{name} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Account_NamePUTRequest(BaseModel):
    """
    Request model for /cluster/acme/account/{name} PUT
    """
    contact: str | None = Field(
        description="Contact email addresses.",
    )
    name: str | None = Field(
        default="default",
        description="ACME account config file name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Account_NamePUTResponse(BaseModel):
    """
    Response model for /cluster/acme/account/{name} PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_TosGETRequest(BaseModel):
    """
    Request model for /cluster/acme/tos GET
    """
    directory: str | None = Field(
        default="https://acme-v02.api.letsencrypt.org/directory",
        description="URL of ACME CA directory endpoint.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_TosGETResponse(BaseModel):
    """
    Response model for /cluster/acme/tos GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_DirectoriesGETResponse(BaseModel):
    """
    Response model for /cluster/acme/directories GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Acme_Challenge_SchemaGETResponse(BaseModel):
    """
    Response model for /cluster/acme/challenge-schema GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_CephGETResponse(BaseModel):
    """
    Response model for /cluster/ceph GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_MetadataGETRequest(BaseModel):
    """
    Request model for /cluster/ceph/metadata GET
    """
    scope: Literal["all", "versions"] | None = Field(
        default="all",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_MetadataGETResponse(BaseModel):
    """
    Response model for /cluster/ceph/metadata GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_StatusGETResponse(BaseModel):
    """
    Response model for /cluster/ceph/status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_FlagsGETResponse(BaseModel):
    """
    Response model for /cluster/ceph/flags GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_FlagsPUTRequest(BaseModel):
    """
    Request model for /cluster/ceph/flags PUT
    """
    nobackfill: bool | int | str | None = Field(
        description="Backfilling of PGs is suspended.",
    )
    nodeep_scrub: bool | int | str | None = Field(
        description="Deep Scrubbing is disabled.",
        serialization_alias="nodeep-scrub",
    )
    nodown: bool | int | str | None = Field(
        description="OSD failure reports are being ignored, such that the monitors will not mark OSDs down.",
    )
    noin: bool | int | str | None = Field(
        description="OSDs that were previously marked out will not be marked back in when they start.",
    )
    noout: bool | int | str | None = Field(
        description="OSDs will not automatically be marked out after the configured interval.",
    )
    norebalance: bool | int | str | None = Field(
        description="Rebalancing of PGs is suspended.",
    )
    norecover: bool | int | str | None = Field(
        description="Recovery of PGs is suspended.",
    )
    noscrub: bool | int | str | None = Field(
        description="Scrubbing is disabled.",
    )
    notieragent: bool | int | str | None = Field(
        description="Cache tiering activity is suspended.",
    )
    noup: bool | int | str | None = Field(
        description="OSDs are not allowed to start.",
    )
    pause: bool | int | str | None = Field(
        description="Pauses read and writes.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_FlagsPUTResponse(BaseModel):
    """
    Response model for /cluster/ceph/flags PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_Flags_FlagGETRequest(BaseModel):
    """
    Request model for /cluster/ceph/flags/{flag} GET
    """
    flag: str = Field(
        description="The name of the flag name to get.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_Flags_FlagGETResponse(BaseModel):
    """
    Response model for /cluster/ceph/flags/{flag} GET
    """
    data: bool | int | str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Ceph_Flags_FlagPUTRequest(BaseModel):
    """
    Request model for /cluster/ceph/flags/{flag} PUT
    """
    flag: str = Field(
        description="The ceph flag to update",
    )
    value: bool | int | str = Field(
        description="The new value of the flag",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_JobsGETResponse(BaseModel):
    """
    Response model for /cluster/jobs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Jobs_Schedule_AnalyzeGETRequest(BaseModel):
    """
    Request model for /cluster/jobs/schedule-analyze GET
    """
    iterations: int | str | None = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of event-iteration to simulate and return.",
    )
    schedule: str = Field(
        max_length=128,
        description="Job schedule. The format is a subset of `systemd` calendar events.",
    )
    starttime: int | str | None = Field(
        description="UNIX timestamp to start the calculation from. Defaults to the current time.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Jobs_Schedule_AnalyzeGETResponse(BaseModel):
    """
    Response model for /cluster/jobs/schedule-analyze GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_SdnGETResponse(BaseModel):
    """
    Response model for /cluster/sdn GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_SdnPUTResponse(BaseModel):
    """
    Response model for /cluster/sdn PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_VnetsGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets GET
    """
    pending: bool | int | str | None = Field(
        description="Display pending config.",
    )
    running: bool | int | str | None = Field(
        description="Display running config.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_VnetsGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/vnets GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_VnetsPOSTRequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets POST
    """
    alias: str | None = Field(
        max_length=256,
        description="alias name of the vnet",
    )
    tag: int | str | None = Field(
        description="vlan or vxlan id",
    )
    type: Literal["vnet"] | None = Field(
        description="Type",
    )
    vlanaware: bool | int | str | None = Field(
        description="Allow vm VLANs to pass through this vnet.",
    )
    vnet: str = Field(
        description="The SDN vnet object identifier.",
    )
    zone: str = Field(
        description="zone id",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_VnetDELETERequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets/{vnet} DELETE
    """
    vnet: str = Field(
        description="The SDN vnet object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_VnetGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets/{vnet} GET
    """
    pending: bool | int | str | None = Field(
        description="Display pending config.",
    )
    running: bool | int | str | None = Field(
        description="Display running config.",
    )
    vnet: str = Field(
        description="The SDN vnet object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_VnetGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/vnets/{vnet} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_VnetPUTRequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets/{vnet} PUT
    """
    alias: str | None = Field(
        max_length=256,
        description="alias name of the vnet",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    tag: int | str | None = Field(
        description="vlan or vxlan id",
    )
    vlanaware: bool | int | str | None = Field(
        description="Allow vm VLANs to pass through this vnet.",
    )
    vnet: str = Field(
        description="The SDN vnet object identifier.",
    )
    zone: str | None = Field(
        description="zone id",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_Vnet_SubnetsGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets/{vnet}/subnets GET
    """
    pending: bool | int | str | None = Field(
        description="Display pending config.",
    )
    running: bool | int | str | None = Field(
        description="Display running config.",
    )
    vnet: str = Field(
        description="The SDN vnet object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_Vnet_SubnetsGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/vnets/{vnet}/subnets GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_Vnet_SubnetsPOSTRequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets/{vnet}/subnets POST
    """
    dnszoneprefix: str | None = Field(
        description="dns domain zone prefix  ex: \u0027adm\u0027 -\u003e \u003chostname\u003e.adm.mydomain.com",
    )
    gateway: str | None = Field(
        description="Subnet Gateway: Will be assign on vnet for layer3 zones",
    )
    snat: bool | int | str | None = Field(
        description="enable masquerade for this subnet if pve-firewall",
    )
    subnet: str = Field(
        description="The SDN subnet object identifier.",
    )
    type: Literal["subnet"] = Field(
    )
    vnet: str = Field(
        description="associated vnet",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_Vnet_Subnets_SubnetDELETERequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets/{vnet}/subnets/{subnet} DELETE
    """
    subnet: str = Field(
        description="The SDN subnet object identifier.",
    )
    vnet: str = Field(
        description="The SDN vnet object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_Vnet_Subnets_SubnetGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets/{vnet}/subnets/{subnet} GET
    """
    pending: bool | int | str | None = Field(
        description="Display pending config.",
    )
    running: bool | int | str | None = Field(
        description="Display running config.",
    )
    subnet: str = Field(
        description="The SDN subnet object identifier.",
    )
    vnet: str = Field(
        description="The SDN vnet object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_Vnet_Subnets_SubnetGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/vnets/{vnet}/subnets/{subnet} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Vnets_Vnet_Subnets_SubnetPUTRequest(BaseModel):
    """
    Request model for /cluster/sdn/vnets/{vnet}/subnets/{subnet} PUT
    """
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    dnszoneprefix: str | None = Field(
        description="dns domain zone prefix  ex: \u0027adm\u0027 -\u003e \u003chostname\u003e.adm.mydomain.com",
    )
    gateway: str | None = Field(
        description="Subnet Gateway: Will be assign on vnet for layer3 zones",
    )
    snat: bool | int | str | None = Field(
        description="enable masquerade for this subnet if pve-firewall",
    )
    subnet: str = Field(
        description="The SDN subnet object identifier.",
    )
    vnet: str | None = Field(
        description="associated vnet",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_ZonesGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/zones GET
    """
    pending: bool | int | str | None = Field(
        description="Display pending config.",
    )
    running: bool | int | str | None = Field(
        description="Display running config.",
    )
    type: Literal["evpn", "faucet", "qinq", "simple", "vlan", "vxlan"] | None = Field(
        description="Only list SDN zones of specific type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_ZonesGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/zones GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_ZonesPOSTRequest(BaseModel):
    """
    Request model for /cluster/sdn/zones POST
    """
    advertise_subnets: bool | int | str | None = Field(
        description="Advertise evpn subnets if you have silent hosts",
        serialization_alias="advertise-subnets",
    )
    bridge: str | None = Field(
    )
    bridge_disable_mac_learning: bool | int | str | None = Field(
        description="Disable auto mac learning.",
        serialization_alias="bridge-disable-mac-learning",
    )
    controller: str | None = Field(
        description="Frr router name",
    )
    disable_arp_nd_suppression: bool | int | str | None = Field(
        description="Disable ipv4 arp \u0026\u0026 ipv6 neighbour discovery suppression",
        serialization_alias="disable-arp-nd-suppression",
    )
    dns: str | None = Field(
        description="dns api server",
    )
    dnszone: str | None = Field(
        description="dns domain zone  ex: mydomain.com",
    )
    dp_id: int | str | None = Field(
        description="Faucet dataplane id",
        serialization_alias="dp-id",
    )
    exitnodes: list[ProxmoxNode] | None = Field(
        description="List of cluster node names.",
    )
    exitnodes_local_routing: bool | int | str | None = Field(
        description="Allow exitnodes to connect to evpn guests",
        serialization_alias="exitnodes-local-routing",
    )
    exitnodes_primary: ProxmoxNode | None = Field(
        description="Force traffic to this exitnode first.",
        serialization_alias="exitnodes-primary",
    )
    ipam: str | None = Field(
        description="use a specific ipam",
    )
    mac: str | None = Field(
        description="Anycast logical router mac address",
    )
    mtu: int | str | None = Field(
        description="MTU",
    )
    nodes: list[ProxmoxNode] | None = Field(
        description="List of cluster node names.",
    )
    peers: str | None = Field(
        description="peers address list.",
    )
    reversedns: str | None = Field(
        description="reverse dns api server",
    )
    rt_import: str | None = Field(
        description="Route-Target import",
        serialization_alias="rt-import",
    )
    tag: int | str | None = Field(
        ge=0,
        description="Service-VLAN Tag",
    )
    type: Literal["evpn", "faucet", "qinq", "simple", "vlan", "vxlan"] = Field(
        description="Plugin type.",
    )
    vlan_protocol: Literal["802.1ad", "802.1q"] | None = Field(
        default="802.1q",
        serialization_alias="vlan-protocol",
    )
    vrf_vxlan: int | str | None = Field(
        description="l3vni.",
        serialization_alias="vrf-vxlan",
    )
    zone: str = Field(
        description="The SDN zone object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Zones_ZoneDELETERequest(BaseModel):
    """
    Request model for /cluster/sdn/zones/{zone} DELETE
    """
    zone: str = Field(
        description="The SDN zone object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Zones_ZoneGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/zones/{zone} GET
    """
    pending: bool | int | str | None = Field(
        description="Display pending config.",
    )
    running: bool | int | str | None = Field(
        description="Display running config.",
    )
    zone: str = Field(
        description="The SDN zone object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Zones_ZoneGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/zones/{zone} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Zones_ZonePUTRequest(BaseModel):
    """
    Request model for /cluster/sdn/zones/{zone} PUT
    """
    advertise_subnets: bool | int | str | None = Field(
        description="Advertise evpn subnets if you have silent hosts",
        serialization_alias="advertise-subnets",
    )
    bridge: str | None = Field(
    )
    bridge_disable_mac_learning: bool | int | str | None = Field(
        description="Disable auto mac learning.",
        serialization_alias="bridge-disable-mac-learning",
    )
    controller: str | None = Field(
        description="Frr router name",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    disable_arp_nd_suppression: bool | int | str | None = Field(
        description="Disable ipv4 arp \u0026\u0026 ipv6 neighbour discovery suppression",
        serialization_alias="disable-arp-nd-suppression",
    )
    dns: str | None = Field(
        description="dns api server",
    )
    dnszone: str | None = Field(
        description="dns domain zone  ex: mydomain.com",
    )
    dp_id: int | str | None = Field(
        description="Faucet dataplane id",
        serialization_alias="dp-id",
    )
    exitnodes: list[ProxmoxNode] | None = Field(
        description="List of cluster node names.",
    )
    exitnodes_local_routing: bool | int | str | None = Field(
        description="Allow exitnodes to connect to evpn guests",
        serialization_alias="exitnodes-local-routing",
    )
    exitnodes_primary: ProxmoxNode | None = Field(
        description="Force traffic to this exitnode first.",
        serialization_alias="exitnodes-primary",
    )
    ipam: str | None = Field(
        description="use a specific ipam",
    )
    mac: str | None = Field(
        description="Anycast logical router mac address",
    )
    mtu: int | str | None = Field(
        description="MTU",
    )
    nodes: list[ProxmoxNode] | None = Field(
        description="List of cluster node names.",
    )
    peers: str | None = Field(
        description="peers address list.",
    )
    reversedns: str | None = Field(
        description="reverse dns api server",
    )
    rt_import: str | None = Field(
        description="Route-Target import",
        serialization_alias="rt-import",
    )
    tag: int | str | None = Field(
        ge=0,
        description="Service-VLAN Tag",
    )
    vlan_protocol: Literal["802.1ad", "802.1q"] | None = Field(
        default="802.1q",
        serialization_alias="vlan-protocol",
    )
    vrf_vxlan: int | str | None = Field(
        description="l3vni.",
        serialization_alias="vrf-vxlan",
    )
    zone: str = Field(
        description="The SDN zone object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_ControllersGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/controllers GET
    """
    pending: bool | int | str | None = Field(
        description="Display pending config.",
    )
    running: bool | int | str | None = Field(
        description="Display running config.",
    )
    type: Literal["bgp", "evpn", "faucet"] | None = Field(
        description="Only list sdn controllers of specific type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_ControllersGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/controllers GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_ControllersPOSTRequest(BaseModel):
    """
    Request model for /cluster/sdn/controllers POST
    """
    asn: int | str | None = Field(
        ge=0,
        le=4294967296,
        description="autonomous system number",
    )
    bgp_multipath_as_path_relax: bool | int | str | None = Field(
        serialization_alias="bgp-multipath-as-path-relax",
    )
    controller: str = Field(
        description="The SDN controller object identifier.",
    )
    ebgp: bool | int | str | None = Field(
        description="Enable ebgp. (remote-as external)",
    )
    ebgp_multihop: int | str | None = Field(
        serialization_alias="ebgp-multihop",
    )
    loopback: str | None = Field(
        description="source loopback interface.",
    )
    node: ProxmoxNode | None = Field(
        description="The cluster node name.",
    )
    peers: str | None = Field(
        description="peers address list.",
    )
    type: Literal["bgp", "evpn", "faucet"] = Field(
        description="Plugin type.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Controllers_ControllerDELETERequest(BaseModel):
    """
    Request model for /cluster/sdn/controllers/{controller} DELETE
    """
    controller: str = Field(
        description="The SDN controller object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Controllers_ControllerGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/controllers/{controller} GET
    """
    controller: str = Field(
        description="The SDN controller object identifier.",
    )
    pending: bool | int | str | None = Field(
        description="Display pending config.",
    )
    running: bool | int | str | None = Field(
        description="Display running config.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Controllers_ControllerGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/controllers/{controller} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Controllers_ControllerPUTRequest(BaseModel):
    """
    Request model for /cluster/sdn/controllers/{controller} PUT
    """
    asn: int | str | None = Field(
        ge=0,
        le=4294967296,
        description="autonomous system number",
    )
    bgp_multipath_as_path_relax: bool | int | str | None = Field(
        serialization_alias="bgp-multipath-as-path-relax",
    )
    controller: str = Field(
        description="The SDN controller object identifier.",
    )
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    ebgp: bool | int | str | None = Field(
        description="Enable ebgp. (remote-as external)",
    )
    ebgp_multihop: int | str | None = Field(
        serialization_alias="ebgp-multihop",
    )
    loopback: str | None = Field(
        description="source loopback interface.",
    )
    node: ProxmoxNode | None = Field(
        description="The cluster node name.",
    )
    peers: str | None = Field(
        description="peers address list.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_IpamsGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/ipams GET
    """
    type: Literal["netbox", "phpipam", "pve"] | None = Field(
        description="Only list sdn ipams of specific type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_IpamsGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/ipams GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_IpamsPOSTRequest(BaseModel):
    """
    Request model for /cluster/sdn/ipams POST
    """
    ipam: str = Field(
        description="The SDN ipam object identifier.",
    )
    section: int | str | None = Field(
    )
    token: str | None = Field(
    )
    type: Literal["netbox", "phpipam", "pve"] = Field(
        description="Plugin type.",
    )
    url: str | None = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Ipams_IpamDELETERequest(BaseModel):
    """
    Request model for /cluster/sdn/ipams/{ipam} DELETE
    """
    ipam: str = Field(
        description="The SDN ipam object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Ipams_IpamGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/ipams/{ipam} GET
    """
    ipam: str = Field(
        description="The SDN ipam object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Ipams_IpamGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/ipams/{ipam} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Ipams_IpamPUTRequest(BaseModel):
    """
    Request model for /cluster/sdn/ipams/{ipam} PUT
    """
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    ipam: str = Field(
        description="The SDN ipam object identifier.",
    )
    section: int | str | None = Field(
    )
    token: str | None = Field(
    )
    url: str | None = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_DnsGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/dns GET
    """
    type: Literal["powerdns"] | None = Field(
        description="Only list sdn dns of specific type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_DnsGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/dns GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_DnsPOSTRequest(BaseModel):
    """
    Request model for /cluster/sdn/dns POST
    """
    dns: str = Field(
        description="The SDN dns object identifier.",
    )
    key: str = Field(
    )
    reversemaskv6: int | str | None = Field(
    )
    reversev6mask: int | str | None = Field(
    )
    ttl: int | str | None = Field(
    )
    type: Literal["powerdns"] = Field(
        description="Plugin type.",
    )
    url: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Dns_DnsDELETERequest(BaseModel):
    """
    Request model for /cluster/sdn/dns/{dns} DELETE
    """
    dns: str = Field(
        description="The SDN dns object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Dns_DnsGETRequest(BaseModel):
    """
    Request model for /cluster/sdn/dns/{dns} GET
    """
    dns: str = Field(
        description="The SDN dns object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Dns_DnsGETResponse(BaseModel):
    """
    Response model for /cluster/sdn/dns/{dns} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_Sdn_Dns_DnsPUTRequest(BaseModel):
    """
    Request model for /cluster/sdn/dns/{dns} PUT
    """
    delete: str | None = Field(
        max_length=4096,
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    dns: str = Field(
        description="The SDN dns object identifier.",
    )
    key: str | None = Field(
    )
    reversemaskv6: int | str | None = Field(
    )
    ttl: int | str | None = Field(
    )
    url: str | None = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_LogGETRequest(BaseModel):
    """
    Request model for /cluster/log GET
    """
    max: int | str | None = Field(
        ge=1,
        description="Maximum number of entries.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_LogGETResponse(BaseModel):
    """
    Response model for /cluster/log GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_ResourcesGETRequest(BaseModel):
    """
    Request model for /cluster/resources GET
    """
    type: Literal["node", "sdn", "storage", "vm"] | None = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_ResourcesGETResponse(BaseModel):
    """
    Response model for /cluster/resources GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_TasksGETResponse(BaseModel):
    """
    Response model for /cluster/tasks GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_OptionsGETResponse(BaseModel):
    """
    Response model for /cluster/options GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_OptionsPUTRequest(BaseModel):
    """
    Request model for /cluster/options PUT
    """
    bwlimit: str | None = Field(
        description="Set bandwidth/io limits various operations.",
    )
    console: Literal["applet", "html5", "vv", "xtermjs"] | None = Field(
        description="Select the default Console viewer. You can either use the builtin java applet (VNC; deprecated and maps to html5), an external virt-viewer comtatible application (SPICE), an HTML5 based vnc viewer (noVNC), or an HTML5 based console client (xtermjs). If the selected viewer is not available (e.g. SPICE not activated for the VM), the fallback is noVNC.",
    )
    crs: str | None = Field(
        description="Cluster resource scheduling settings.",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    description: str | None = Field(
        max_length=65536,
        description="Datacenter description. Shown in the web-interface datacenter notes panel. This is saved as comment inside the configuration file.",
    )
    email_from: str | None = Field(
        description="Specify email address to send notification from (default is root@$hostname)",
    )
    fencing: Literal["both", "hardware", "watchdog"] | None = Field(
        default="watchdog",
        description="Set the fencing mode of the HA cluster. Hardware mode needs a valid configuration of fence devices in /etc/pve/ha/fence.cfg. With both all two modes are used.\n\nWARNING: \u0027hardware\u0027 and \u0027both\u0027 are EXPERIMENTAL \u0026 WIP",
    )
    ha: str | None = Field(
        description="Cluster wide HA settings.",
    )
    http_proxy: str | None = Field(
        description="Specify external http proxy which is used for downloads (example: \u0027http://username:password@host:port/\u0027)",
    )
    keyboard: str | None = Field(
        description="Default keybord layout for vnc server.",
    )
    language: str | None = Field(
        description="Default GUI language.",
    )
    mac_prefix: str | None = Field(
        description="Prefix for autogenerated MAC addresses.",
    )
    max_workers: int | str | None = Field(
        ge=1,
        description="Defines how many workers (per node) are maximal started  on actions like \u0027stopall VMs\u0027 or task from the ha-manager.",
    )
    migration: str | None = Field(
        description="For cluster wide migration settings.",
    )
    migration_unsecure: bool | int | str | None = Field(
        description="Migration is secure using SSH tunnel by default. For secure private networks you can disable it to speed up migration. Deprecated, use the \u0027migration\u0027 property instead!",
    )
    next_id: str | None = Field(
        description="Control the range for the free VMID auto-selection pool.",
        serialization_alias="next-id",
    )
    notify: str | None = Field(
        description="Cluster-wide notification settings.",
    )
    registered_tags: str | None = Field(
        description="A list of tags that require a `Sys.Modify` on \u0027/\u0027 to set and delete. Tags set here that are also in \u0027user-tag-access\u0027 also require `Sys.Modify`.",
        serialization_alias="registered-tags",
    )
    tag_style: str | None = Field(
        description="Tag style options.",
        serialization_alias="tag-style",
    )
    u2f: str | None = Field(
        description="u2f",
    )
    user_tag_access: str | None = Field(
        description="Privilege options for user-settable tags",
        serialization_alias="user-tag-access",
    )
    webauthn: str | None = Field(
        description="webauthn configuration",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_StatusGETResponse(BaseModel):
    """
    Response model for /cluster/status GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_NextidGETRequest(BaseModel):
    """
    Request model for /cluster/nextid GET
    """
    vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Cluster_NextidGETResponse(BaseModel):
    """
    Response model for /cluster/nextid GET
    """
    data: int | str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

