"""
Pydantic models for nodes API endpoints.

This module contains auto-generated Pydantic v2 models for request and response
validation in the nodes API endpoints.
"""

from ..base.types import ProxmoxNode, ProxmoxVMID
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Literal

class NodesGETResponse(BaseModel):
    """
    Response model for /nodes GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_NodeGETRequest(BaseModel):
    """
    Request model for /nodes/{node} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_NodeGETResponse(BaseModel):
    """
    Response model for /nodes/{node} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_QemuGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu GET
    """
    full: bool | int | str | None = Field(
        description="Determine the full status of active VMs.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_QemuGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_QemuPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu POST
    """
    acpi: bool | int | str | None = Field(
        default=1,
        description="Enable/disable ACPI.",
    )
    affinity: str | None = Field(
        description="List of host cores used to execute guest processes, for example: 0,5,8-11",
    )
    agent: str | None = Field(
        description="Enable/disable communication with the QEMU Guest Agent and its properties.",
    )
    arch: Literal["aarch64", "x86_64"] | None = Field(
        description="Virtual processor architecture. Defaults to the host.",
    )
    archive: str | None = Field(
        max_length=255,
        description="The backup archive. Either the file system path to a .tar or .vma file (use \u0027-\u0027 to pipe data from stdin) or a proxmox storage backup volume identifier.",
    )
    args: str | None = Field(
        description="Arbitrary arguments passed to kvm.",
    )
    audio0: str | None = Field(
        description="Configure a audio device, useful in combination with QXL/Spice.",
    )
    autostart: bool | int | str | None = Field(
        default=0,
        description="Automatic restart after crash (currently ignored).",
    )
    balloon: int | str | None = Field(
        ge=0,
        description="Amount of target RAM for the VM in MiB. Using zero disables the ballon driver.",
    )
    bios: Literal["ovmf", "seabios"] | None = Field(
        default="seabios",
        description="Select BIOS implementation.",
    )
    boot: str | None = Field(
        description="Specify guest boot order. Use the \u0027order=\u0027 sub-property as usage with no key or \u0027legacy=\u0027 is deprecated.",
    )
    bootdisk: str | None = Field(
        description="Enable booting from specified disk. Deprecated: Use \u0027boot: order=foo;bar\u0027 instead.",
    )
    bwlimit: int | str | None = Field(
        default="restore limit from datacenter or storage config",
        ge=0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    cdrom: str | None = Field(
        description="This is an alias for option -ide2",
    )
    cicustom: str | None = Field(
        description="cloud-init: Specify custom files to replace the automatically generated ones at start.",
    )
    cipassword: str | None = Field(
        description="cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.",
    )
    citype: Literal["configdrive2", "nocloud", "opennebula"] | None = Field(
        description="Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.",
    )
    ciuser: str | None = Field(
        description="cloud-init: User name to change ssh keys and password for instead of the image\u0027s configured default user.",
    )
    cores: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of cores per socket.",
    )
    cpu: str | None = Field(
        description="Emulated CPU type.",
    )
    cpulimit: float | str | None = Field(
        default=0,
        ge=0.0,
        le=128.0,
        description="Limit of CPU usage.",
    )
    cpuunits: int | str | None = Field(
        default="cgroup v1: 1024, cgroup v2: 100",
        ge=1,
        le=262144,
        description="CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.",
    )
    description: str | None = Field(
        max_length=8192,
        description="Description for the VM. Shown in the web-interface VM\u0027s summary. This is saved as comment inside the configuration file.",
    )
    efidisk0: str | None = Field(
        description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
    )
    force: bool | int | str | None = Field(
        description="Allow to overwrite existing VM.",
    )
    freeze: bool | int | str | None = Field(
        description="Freeze CPU at startup (use \u0027c\u0027 monitor command to start execution).",
    )
    hookscript: str | None = Field(
        description="Script that will be executed during various steps in the vms lifetime.",
    )
    hostpci_n_: str | None = Field(
        description="Map host PCI devices into guest.",
        serialization_alias="hostpci[n]",
    )
    hotplug: str | None = Field(
        default="network,disk,usb",
        description="Selectively enable hotplug features. This is a comma separated list of hotplug features: \u0027network\u0027, \u0027disk\u0027, \u0027cpu\u0027, \u0027memory\u0027, \u0027usb\u0027 and \u0027cloudinit\u0027. Use \u00270\u0027 to disable hotplug completely. Using \u00271\u0027 as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version \u003e= 7.1 and ostype l26 or windows \u003e 7.",
    )
    hugepages: Literal["1024", "2", "any"] | None = Field(
        description="Enable/disable hugepages memory.",
    )
    ide_n_: str | None = Field(
        description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="ide[n]",
    )
    ipconfig_n_: str | None = Field(
        description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string \u0027dhcp\u0027 can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string \u0027auto\u0027 can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n",
        serialization_alias="ipconfig[n]",
    )
    ivshmem: str | None = Field(
        description="Inter-VM shared memory. Useful for direct communication between VMs, or to the host.",
    )
    keephugepages: bool | int | str | None = Field(
        default=0,
        description="Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.",
    )
    keyboard: str | None = Field(
        description="Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.",
    )
    kvm: bool | int | str | None = Field(
        default=1,
        description="Enable/disable KVM hardware virtualization.",
    )
    live_restore: bool | int | str | None = Field(
        description="Start the VM immediately from the backup and restore in background. PBS only.",
        serialization_alias="live-restore",
    )
    localtime: bool | int | str | None = Field(
        description="Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.",
    )
    lock: Literal["backup", "clone", "create", "migrate", "rollback", "snapshot", "snapshot-delete", "suspended", "suspending"] | None = Field(
        description="Lock/unlock the VM.",
    )
    machine: str | None = Field(
        max_length=40,
        description="Specifies the QEMU machine type.",
    )
    memory: int | str | None = Field(
        default=512,
        ge=16,
        description="Amount of RAM for the VM in MiB. This is the maximum available memory when you use the balloon device.",
    )
    migrate_downtime: float | str | None = Field(
        default=0.1,
        ge=0.0,
        description="Set maximum tolerated downtime (in seconds) for migrations.",
    )
    migrate_speed: int | str | None = Field(
        default=0,
        ge=0,
        description="Set maximum speed (in MB/s) for migrations. Value 0 is no limit.",
    )
    name: str | None = Field(
        description="Set a name for the VM. Only used on the configuration web interface.",
    )
    nameserver: str | None = Field(
        description="cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.",
    )
    net_n_: str | None = Field(
        description="Specify network devices.",
        serialization_alias="net[n]",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    numa: bool | int | str | None = Field(
        default=0,
        description="Enable/disable NUMA.",
    )
    numa_n_: str | None = Field(
        description="NUMA topology.",
        serialization_alias="numa[n]",
    )
    onboot: bool | int | str | None = Field(
        default=0,
        description="Specifies whether a VM will be started during system bootup.",
    )
    ostype: str | None = Field(
        description="Specify guest operating system.",
    )
    parallel_n_: str | None = Field(
        description="Map host parallel devices (n is 0 to 2).",
        serialization_alias="parallel[n]",
    )
    pool: str | None = Field(
        description="Add the VM to the specified pool.",
    )
    protection: bool | int | str | None = Field(
        default=0,
        description="Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.",
    )
    reboot: bool | int | str | None = Field(
        default=1,
        description="Allow reboot. If set to \u00270\u0027 the VM exit on reboot.",
    )
    rng0: str | None = Field(
        description="Configure a VirtIO-based Random Number Generator.",
    )
    sata_n_: str | None = Field(
        description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="sata[n]",
    )
    scsi_n_: str | None = Field(
        description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="scsi[n]",
    )
    scsihw: Literal["lsi", "lsi53c810", "megasas", "pvscsi", "virtio-scsi-pci", "virtio-scsi-single"] | None = Field(
        default="lsi",
        description="SCSI controller model",
    )
    searchdomain: str | None = Field(
        description="cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.",
    )
    serial_n_: str | None = Field(
        description="Create a serial device inside the VM (n is 0 to 3)",
        serialization_alias="serial[n]",
    )
    shares: int | str | None = Field(
        default=1000,
        ge=0,
        le=50000,
        description="Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.",
    )
    smbios1: str | None = Field(
        max_length=512,
        description="Specify SMBIOS type 1 fields.",
    )
    smp: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of CPUs. Please use option -sockets instead.",
    )
    sockets: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of CPU sockets.",
    )
    spice_enhancements: str | None = Field(
        description="Configure additional enhancements for SPICE.",
    )
    sshkeys: str | None = Field(
        description="cloud-init: Setup public SSH keys (one key per line, OpenSSH format).",
    )
    start: bool | int | str | None = Field(
        default=0,
        description="Start VM after it was created successfully.",
    )
    startdate: str | None = Field(
        default="now",
        description="Set the initial date of the real time clock. Valid format for date are:\u0027now\u0027 or \u00272006-06-17T16:01:21\u0027 or \u00272006-06-17\u0027.",
    )
    startup: str | None = Field(
        description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the \u0027up\u0027 or \u0027down\u0027 delay in seconds, which specifies a delay to wait before the next VM is started or stopped.",
    )
    storage: str | None = Field(
        description="Default storage.",
    )
    tablet: bool | int | str | None = Field(
        default=1,
        description="Enable/disable the USB tablet device.",
    )
    tags: str | None = Field(
        description="Tags of the VM. This is only meta information.",
    )
    tdf: bool | int | str | None = Field(
        default=0,
        description="Enable/disable time drift fix.",
    )
    template: bool | int | str | None = Field(
        default=0,
        description="Enable/disable Template.",
    )
    tpmstate0: str | None = Field(
        description="Configure a Disk for storing TPM state. The format is fixed to \u0027raw\u0027. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
    )
    unique: bool | int | str | None = Field(
        description="Assign a unique random ethernet address.",
    )
    unused_n_: str | None = Field(
        description="Reference to unused volumes. This is used internally, and should not be modified manually.",
        serialization_alias="unused[n]",
    )
    usb_n_: str | None = Field(
        description="Configure an USB device (n is 0 to 4, for machine version \u003e= 7.1 and ostype l26 or windows \u003e 7, n can be up to 14).",
        serialization_alias="usb[n]",
    )
    vcpus: int | str | None = Field(
        default=0,
        ge=1,
        description="Number of hotplugged vcpus.",
    )
    vga: str | None = Field(
        description="Configure the VGA hardware.",
    )
    virtio_n_: str | None = Field(
        description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="virtio[n]",
    )
    vmgenid: str | None = Field(
        default="1 (autogenerated)",
        description="Set VM Generation ID. Use \u00271\u0027 to autogenerate on create or update, pass \u00270\u0027 to disable explicitly.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    vmstatestorage: str | None = Field(
        description="Default storage for VM state volumes/files.",
    )
    watchdog: str | None = Field(
        description="Create a virtual hardware watchdog device.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_QemuPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_VmidDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid} DELETE
    """
    destroy_unreferenced_disks: bool | int | str | None = Field(
        default=0,
        description="If set, destroy additionally all disks not referenced in the config but with a matching VMID from all enabled storages.",
        serialization_alias="destroy-unreferenced-disks",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    purge: bool | int | str | None = Field(
        description="Remove VMID from configurations, like backup \u0026 replication jobs and HA.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_VmidDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_VmidGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_VmidGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_FirewallGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_FirewallGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_RulesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/rules GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_RulesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/rules GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_RulesPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/rules POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
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
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Rules_PosDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/rules/{pos} DELETE
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Rules_PosGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/rules/{pos} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Rules_PosGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/rules/{pos} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Rules_PosPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/rules/{pos} PUT
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
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
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_AliasesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/aliases GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_AliasesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/aliases GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_AliasesPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/aliases POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Aliases_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/aliases/{name} DELETE
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    name: str = Field(
        max_length=64,
        description="Alias name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Aliases_NameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/aliases/{name} GET
    """
    name: str = Field(
        max_length=64,
        description="Alias name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Aliases_NameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/aliases/{name} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Aliases_NamePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/aliases/{name} PUT
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    rename: str | None = Field(
        max_length=64,
        description="Rename an existing alias.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_IpsetGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/ipset GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_IpsetGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/ipset GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_IpsetPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/ipset POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    rename: str | None = Field(
        max_length=64,
        description="Rename an existing IPSet. You can set \u0027rename\u0027 to the same value as \u0027name\u0027 to update the \u0027comment\u0027 of an existing IPSet.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name} DELETE
    """
    force: bool | int | str | None = Field(
        description="Delete all members of the IPSet, if there are any.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name} GET
    """
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Ipset_NameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Ipset_NamePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name} POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    nomatch: bool | int | str | None = Field(
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}/{cidr} DELETE
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}/{cidr} GET
    """
    cidr: str = Field(
        description="Network/IP specification in CIDR format.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}/{cidr} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_Ipset_Name_CidrPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}/{cidr} PUT
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    nomatch: bool | int | str | None = Field(
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_OptionsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/options GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_OptionsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/options GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_OptionsPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/options PUT
    """
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    dhcp: bool | int | str | None = Field(
        default=0,
        description="Enable DHCP.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    enable: bool | int | str | None = Field(
        default=0,
        description="Enable/disable firewall rules.",
    )
    ipfilter: bool | int | str | None = Field(
        description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net\u003cid\u003e ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface\u0027s MAC address. For containers the configured IP addresses will be implicitly added.",
    )
    log_level_in: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for incoming traffic.",
    )
    log_level_out: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for outgoing traffic.",
    )
    macfilter: bool | int | str | None = Field(
        default=1,
        description="Enable/disable MAC address filter.",
    )
    ndp: bool | int | str | None = Field(
        default=0,
        description="Enable NDP (Neighbor Discovery Protocol).",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    policy_in: Literal["ACCEPT", "DROP", "REJECT"] | None = Field(
        description="Input policy.",
    )
    policy_out: Literal["ACCEPT", "DROP", "REJECT"] | None = Field(
        description="Output policy.",
    )
    radv: bool | int | str | None = Field(
        description="Allow sending Router Advertisement.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_LogGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/log GET
    """
    limit: int | str | None = Field(
        ge=0,
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    since: int | str | None = Field(
        ge=0,
        description="Display log since this UNIX epoch.",
    )
    start: int | str | None = Field(
        ge=0,
    )
    until: int | str | None = Field(
        ge=0,
        description="Display log until this UNIX epoch.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_LogGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/log GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_RefsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/firewall/refs GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    type: Literal["alias", "ipset"] | None = Field(
        description="Only list references of specified type.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Firewall_RefsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/firewall/refs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_AgentGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_AgentGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_AgentPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent POST
    """
    command: str = Field(
        description="The QGA command.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_AgentPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_FreezePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-freeze POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_FreezePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-freeze POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_StatusPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-status POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_StatusPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-status POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_ThawPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-thaw POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Fsfreeze_ThawPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/fsfreeze-thaw POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_FstrimPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/fstrim POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_FstrimPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/fstrim POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_FsinfoGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-fsinfo GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_FsinfoGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-fsinfo GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_Host_NameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-host-name GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_Host_NameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-host-name GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_Memory_Block_InfoGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-memory-block-info GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_Memory_Block_InfoGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-memory-block-info GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_Memory_BlocksGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-memory-blocks GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_Memory_BlocksGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-memory-blocks GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_OsinfoGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-osinfo GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_OsinfoGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-osinfo GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_TimeGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-time GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_TimeGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-time GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_TimezoneGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-timezone GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_TimezoneGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-timezone GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_UsersGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-users GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_UsersGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-users GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_VcpusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/get-vcpus GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Get_VcpusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/get-vcpus GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_InfoGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/info GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_InfoGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/info GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Network_Get_InterfacesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/network-get-interfaces GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Network_Get_InterfacesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/network-get-interfaces GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_PingPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/ping POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_PingPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/ping POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_ShutdownPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/shutdown POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_ShutdownPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/shutdown POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Suspend_DiskPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/suspend-disk POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Suspend_DiskPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/suspend-disk POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Suspend_HybridPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/suspend-hybrid POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Suspend_HybridPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/suspend-hybrid POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Suspend_RamPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/suspend-ram POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Suspend_RamPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/suspend-ram POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Set_User_PasswordPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/set-user-password POST
    """
    crypted: bool | int | str | None = Field(
        default=0,
        description="set to 1 if the password has already been passed through crypt()",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    password: str = Field(
        max_length=1024,
        description="The new password.",
    )
    username: str = Field(
        description="The user to set the password for.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Set_User_PasswordPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/set-user-password POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_ExecPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/exec POST
    """
    command: str | None = Field(
        description="The command as a list of program + arguments",
    )
    input_data: str | None = Field(
        max_length=65536,
        description="Data to pass as \u0027input-data\u0027 to the guest. Usually treated as STDIN to \u0027command\u0027.",
        serialization_alias="input-data",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_ExecPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/exec POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Exec_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/exec-status GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pid: int | str = Field(
        description="The PID to query",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_Exec_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/exec-status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_File_ReadGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/file-read GET
    """
    file: str = Field(
        description="The path to the file",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_File_ReadGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/agent/file-read GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Agent_File_WritePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/agent/file-write POST
    """
    content: str = Field(
        max_length=61440,
        description="The content to write into the file.",
    )
    encode: bool | int | str | None = Field(
        default=1,
        description="If set, the content will be encoded as base64 (required by QEMU).Otherwise the content needs to be encoded beforehand - defaults to true.",
    )
    file: str = Field(
        description="The path to the file.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_RrdGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/rrd GET
    """
    cf: Literal["AVERAGE", "MAX"] | None = Field(
        description="The RRD consolidation function",
    )
    ds: str = Field(
        description="The list of datasources you want to display.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeframe: Literal["day", "hour", "month", "week", "year"] = Field(
        description="Specify the time frame you are interested in.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_RrdGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/rrd GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_RrddataGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/rrddata GET
    """
    cf: Literal["AVERAGE", "MAX"] | None = Field(
        description="The RRD consolidation function",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeframe: Literal["day", "hour", "month", "week", "year"] = Field(
        description="Specify the time frame you are interested in.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_RrddataGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/rrddata GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_ConfigGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/config GET
    """
    current: bool | int | str | None = Field(
        default=0,
        description="Get current values (instead of pending values).",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapshot: str | None = Field(
        max_length=40,
        description="Fetch config values from given snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_ConfigGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/config GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_ConfigPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/config POST
    """
    acpi: bool | int | str | None = Field(
        default=1,
        description="Enable/disable ACPI.",
    )
    affinity: str | None = Field(
        description="List of host cores used to execute guest processes, for example: 0,5,8-11",
    )
    agent: str | None = Field(
        description="Enable/disable communication with the QEMU Guest Agent and its properties.",
    )
    arch: Literal["aarch64", "x86_64"] | None = Field(
        description="Virtual processor architecture. Defaults to the host.",
    )
    args: str | None = Field(
        description="Arbitrary arguments passed to kvm.",
    )
    audio0: str | None = Field(
        description="Configure a audio device, useful in combination with QXL/Spice.",
    )
    autostart: bool | int | str | None = Field(
        default=0,
        description="Automatic restart after crash (currently ignored).",
    )
    background_delay: int | str | None = Field(
        ge=1,
        le=30,
        description="Time to wait for the task to finish. We return \u0027null\u0027 if the task finish within that time.",
    )
    balloon: int | str | None = Field(
        ge=0,
        description="Amount of target RAM for the VM in MiB. Using zero disables the ballon driver.",
    )
    bios: Literal["ovmf", "seabios"] | None = Field(
        default="seabios",
        description="Select BIOS implementation.",
    )
    boot: str | None = Field(
        description="Specify guest boot order. Use the \u0027order=\u0027 sub-property as usage with no key or \u0027legacy=\u0027 is deprecated.",
    )
    bootdisk: str | None = Field(
        description="Enable booting from specified disk. Deprecated: Use \u0027boot: order=foo;bar\u0027 instead.",
    )
    cdrom: str | None = Field(
        description="This is an alias for option -ide2",
    )
    cicustom: str | None = Field(
        description="cloud-init: Specify custom files to replace the automatically generated ones at start.",
    )
    cipassword: str | None = Field(
        description="cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.",
    )
    citype: Literal["configdrive2", "nocloud", "opennebula"] | None = Field(
        description="Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.",
    )
    ciuser: str | None = Field(
        description="cloud-init: User name to change ssh keys and password for instead of the image\u0027s configured default user.",
    )
    cores: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of cores per socket.",
    )
    cpu: str | None = Field(
        description="Emulated CPU type.",
    )
    cpulimit: float | str | None = Field(
        default=0,
        ge=0.0,
        le=128.0,
        description="Limit of CPU usage.",
    )
    cpuunits: int | str | None = Field(
        default="cgroup v1: 1024, cgroup v2: 100",
        ge=1,
        le=262144,
        description="CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    description: str | None = Field(
        max_length=8192,
        description="Description for the VM. Shown in the web-interface VM\u0027s summary. This is saved as comment inside the configuration file.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    efidisk0: str | None = Field(
        description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
    )
    force: bool | int | str | None = Field(
        description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called \u0027unused[n]\u0027, which contains the volume ID. Unlink of unused[n] always cause physical removal.",
    )
    freeze: bool | int | str | None = Field(
        description="Freeze CPU at startup (use \u0027c\u0027 monitor command to start execution).",
    )
    hookscript: str | None = Field(
        description="Script that will be executed during various steps in the vms lifetime.",
    )
    hostpci_n_: str | None = Field(
        description="Map host PCI devices into guest.",
        serialization_alias="hostpci[n]",
    )
    hotplug: str | None = Field(
        default="network,disk,usb",
        description="Selectively enable hotplug features. This is a comma separated list of hotplug features: \u0027network\u0027, \u0027disk\u0027, \u0027cpu\u0027, \u0027memory\u0027, \u0027usb\u0027 and \u0027cloudinit\u0027. Use \u00270\u0027 to disable hotplug completely. Using \u00271\u0027 as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version \u003e= 7.1 and ostype l26 or windows \u003e 7.",
    )
    hugepages: Literal["1024", "2", "any"] | None = Field(
        description="Enable/disable hugepages memory.",
    )
    ide_n_: str | None = Field(
        description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="ide[n]",
    )
    ipconfig_n_: str | None = Field(
        description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string \u0027dhcp\u0027 can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string \u0027auto\u0027 can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n",
        serialization_alias="ipconfig[n]",
    )
    ivshmem: str | None = Field(
        description="Inter-VM shared memory. Useful for direct communication between VMs, or to the host.",
    )
    keephugepages: bool | int | str | None = Field(
        default=0,
        description="Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.",
    )
    keyboard: str | None = Field(
        description="Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.",
    )
    kvm: bool | int | str | None = Field(
        default=1,
        description="Enable/disable KVM hardware virtualization.",
    )
    localtime: bool | int | str | None = Field(
        description="Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.",
    )
    lock: Literal["backup", "clone", "create", "migrate", "rollback", "snapshot", "snapshot-delete", "suspended", "suspending"] | None = Field(
        description="Lock/unlock the VM.",
    )
    machine: str | None = Field(
        max_length=40,
        description="Specifies the QEMU machine type.",
    )
    memory: int | str | None = Field(
        default=512,
        ge=16,
        description="Amount of RAM for the VM in MiB. This is the maximum available memory when you use the balloon device.",
    )
    migrate_downtime: float | str | None = Field(
        default=0.1,
        ge=0.0,
        description="Set maximum tolerated downtime (in seconds) for migrations.",
    )
    migrate_speed: int | str | None = Field(
        default=0,
        ge=0,
        description="Set maximum speed (in MB/s) for migrations. Value 0 is no limit.",
    )
    name: str | None = Field(
        description="Set a name for the VM. Only used on the configuration web interface.",
    )
    nameserver: str | None = Field(
        description="cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.",
    )
    net_n_: str | None = Field(
        description="Specify network devices.",
        serialization_alias="net[n]",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    numa: bool | int | str | None = Field(
        default=0,
        description="Enable/disable NUMA.",
    )
    numa_n_: str | None = Field(
        description="NUMA topology.",
        serialization_alias="numa[n]",
    )
    onboot: bool | int | str | None = Field(
        default=0,
        description="Specifies whether a VM will be started during system bootup.",
    )
    ostype: str | None = Field(
        description="Specify guest operating system.",
    )
    parallel_n_: str | None = Field(
        description="Map host parallel devices (n is 0 to 2).",
        serialization_alias="parallel[n]",
    )
    protection: bool | int | str | None = Field(
        default=0,
        description="Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.",
    )
    reboot: bool | int | str | None = Field(
        default=1,
        description="Allow reboot. If set to \u00270\u0027 the VM exit on reboot.",
    )
    revert: str | None = Field(
        description="Revert a pending change.",
    )
    rng0: str | None = Field(
        description="Configure a VirtIO-based Random Number Generator.",
    )
    sata_n_: str | None = Field(
        description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="sata[n]",
    )
    scsi_n_: str | None = Field(
        description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="scsi[n]",
    )
    scsihw: Literal["lsi", "lsi53c810", "megasas", "pvscsi", "virtio-scsi-pci", "virtio-scsi-single"] | None = Field(
        default="lsi",
        description="SCSI controller model",
    )
    searchdomain: str | None = Field(
        description="cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.",
    )
    serial_n_: str | None = Field(
        description="Create a serial device inside the VM (n is 0 to 3)",
        serialization_alias="serial[n]",
    )
    shares: int | str | None = Field(
        default=1000,
        ge=0,
        le=50000,
        description="Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    smbios1: str | None = Field(
        max_length=512,
        description="Specify SMBIOS type 1 fields.",
    )
    smp: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of CPUs. Please use option -sockets instead.",
    )
    sockets: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of CPU sockets.",
    )
    spice_enhancements: str | None = Field(
        description="Configure additional enhancements for SPICE.",
    )
    sshkeys: str | None = Field(
        description="cloud-init: Setup public SSH keys (one key per line, OpenSSH format).",
    )
    startdate: str | None = Field(
        default="now",
        description="Set the initial date of the real time clock. Valid format for date are:\u0027now\u0027 or \u00272006-06-17T16:01:21\u0027 or \u00272006-06-17\u0027.",
    )
    startup: str | None = Field(
        description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the \u0027up\u0027 or \u0027down\u0027 delay in seconds, which specifies a delay to wait before the next VM is started or stopped.",
    )
    tablet: bool | int | str | None = Field(
        default=1,
        description="Enable/disable the USB tablet device.",
    )
    tags: str | None = Field(
        description="Tags of the VM. This is only meta information.",
    )
    tdf: bool | int | str | None = Field(
        default=0,
        description="Enable/disable time drift fix.",
    )
    template: bool | int | str | None = Field(
        default=0,
        description="Enable/disable Template.",
    )
    tpmstate0: str | None = Field(
        description="Configure a Disk for storing TPM state. The format is fixed to \u0027raw\u0027. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
    )
    unused_n_: str | None = Field(
        description="Reference to unused volumes. This is used internally, and should not be modified manually.",
        serialization_alias="unused[n]",
    )
    usb_n_: str | None = Field(
        description="Configure an USB device (n is 0 to 4, for machine version \u003e= 7.1 and ostype l26 or windows \u003e 7, n can be up to 14).",
        serialization_alias="usb[n]",
    )
    vcpus: int | str | None = Field(
        default=0,
        ge=1,
        description="Number of hotplugged vcpus.",
    )
    vga: str | None = Field(
        description="Configure the VGA hardware.",
    )
    virtio_n_: str | None = Field(
        description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="virtio[n]",
    )
    vmgenid: str | None = Field(
        default="1 (autogenerated)",
        description="Set VM Generation ID. Use \u00271\u0027 to autogenerate on create or update, pass \u00270\u0027 to disable explicitly.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    vmstatestorage: str | None = Field(
        description="Default storage for VM state volumes/files.",
    )
    watchdog: str | None = Field(
        description="Create a virtual hardware watchdog device.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_ConfigPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/config POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_ConfigPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/config PUT
    """
    acpi: bool | int | str | None = Field(
        default=1,
        description="Enable/disable ACPI.",
    )
    affinity: str | None = Field(
        description="List of host cores used to execute guest processes, for example: 0,5,8-11",
    )
    agent: str | None = Field(
        description="Enable/disable communication with the QEMU Guest Agent and its properties.",
    )
    arch: Literal["aarch64", "x86_64"] | None = Field(
        description="Virtual processor architecture. Defaults to the host.",
    )
    args: str | None = Field(
        description="Arbitrary arguments passed to kvm.",
    )
    audio0: str | None = Field(
        description="Configure a audio device, useful in combination with QXL/Spice.",
    )
    autostart: bool | int | str | None = Field(
        default=0,
        description="Automatic restart after crash (currently ignored).",
    )
    balloon: int | str | None = Field(
        ge=0,
        description="Amount of target RAM for the VM in MiB. Using zero disables the ballon driver.",
    )
    bios: Literal["ovmf", "seabios"] | None = Field(
        default="seabios",
        description="Select BIOS implementation.",
    )
    boot: str | None = Field(
        description="Specify guest boot order. Use the \u0027order=\u0027 sub-property as usage with no key or \u0027legacy=\u0027 is deprecated.",
    )
    bootdisk: str | None = Field(
        description="Enable booting from specified disk. Deprecated: Use \u0027boot: order=foo;bar\u0027 instead.",
    )
    cdrom: str | None = Field(
        description="This is an alias for option -ide2",
    )
    cicustom: str | None = Field(
        description="cloud-init: Specify custom files to replace the automatically generated ones at start.",
    )
    cipassword: str | None = Field(
        description="cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.",
    )
    citype: Literal["configdrive2", "nocloud", "opennebula"] | None = Field(
        description="Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.",
    )
    ciuser: str | None = Field(
        description="cloud-init: User name to change ssh keys and password for instead of the image\u0027s configured default user.",
    )
    cores: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of cores per socket.",
    )
    cpu: str | None = Field(
        description="Emulated CPU type.",
    )
    cpulimit: float | str | None = Field(
        default=0,
        ge=0.0,
        le=128.0,
        description="Limit of CPU usage.",
    )
    cpuunits: int | str | None = Field(
        default="cgroup v1: 1024, cgroup v2: 100",
        ge=1,
        le=262144,
        description="CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    description: str | None = Field(
        max_length=8192,
        description="Description for the VM. Shown in the web-interface VM\u0027s summary. This is saved as comment inside the configuration file.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    efidisk0: str | None = Field(
        description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
    )
    force: bool | int | str | None = Field(
        description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called \u0027unused[n]\u0027, which contains the volume ID. Unlink of unused[n] always cause physical removal.",
    )
    freeze: bool | int | str | None = Field(
        description="Freeze CPU at startup (use \u0027c\u0027 monitor command to start execution).",
    )
    hookscript: str | None = Field(
        description="Script that will be executed during various steps in the vms lifetime.",
    )
    hostpci_n_: str | None = Field(
        description="Map host PCI devices into guest.",
        serialization_alias="hostpci[n]",
    )
    hotplug: str | None = Field(
        default="network,disk,usb",
        description="Selectively enable hotplug features. This is a comma separated list of hotplug features: \u0027network\u0027, \u0027disk\u0027, \u0027cpu\u0027, \u0027memory\u0027, \u0027usb\u0027 and \u0027cloudinit\u0027. Use \u00270\u0027 to disable hotplug completely. Using \u00271\u0027 as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version \u003e= 7.1 and ostype l26 or windows \u003e 7.",
    )
    hugepages: Literal["1024", "2", "any"] | None = Field(
        description="Enable/disable hugepages memory.",
    )
    ide_n_: str | None = Field(
        description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="ide[n]",
    )
    ipconfig_n_: str | None = Field(
        description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string \u0027dhcp\u0027 can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string \u0027auto\u0027 can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n",
        serialization_alias="ipconfig[n]",
    )
    ivshmem: str | None = Field(
        description="Inter-VM shared memory. Useful for direct communication between VMs, or to the host.",
    )
    keephugepages: bool | int | str | None = Field(
        default=0,
        description="Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.",
    )
    keyboard: str | None = Field(
        description="Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.",
    )
    kvm: bool | int | str | None = Field(
        default=1,
        description="Enable/disable KVM hardware virtualization.",
    )
    localtime: bool | int | str | None = Field(
        description="Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.",
    )
    lock: Literal["backup", "clone", "create", "migrate", "rollback", "snapshot", "snapshot-delete", "suspended", "suspending"] | None = Field(
        description="Lock/unlock the VM.",
    )
    machine: str | None = Field(
        max_length=40,
        description="Specifies the QEMU machine type.",
    )
    memory: int | str | None = Field(
        default=512,
        ge=16,
        description="Amount of RAM for the VM in MiB. This is the maximum available memory when you use the balloon device.",
    )
    migrate_downtime: float | str | None = Field(
        default=0.1,
        ge=0.0,
        description="Set maximum tolerated downtime (in seconds) for migrations.",
    )
    migrate_speed: int | str | None = Field(
        default=0,
        ge=0,
        description="Set maximum speed (in MB/s) for migrations. Value 0 is no limit.",
    )
    name: str | None = Field(
        description="Set a name for the VM. Only used on the configuration web interface.",
    )
    nameserver: str | None = Field(
        description="cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.",
    )
    net_n_: str | None = Field(
        description="Specify network devices.",
        serialization_alias="net[n]",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    numa: bool | int | str | None = Field(
        default=0,
        description="Enable/disable NUMA.",
    )
    numa_n_: str | None = Field(
        description="NUMA topology.",
        serialization_alias="numa[n]",
    )
    onboot: bool | int | str | None = Field(
        default=0,
        description="Specifies whether a VM will be started during system bootup.",
    )
    ostype: str | None = Field(
        description="Specify guest operating system.",
    )
    parallel_n_: str | None = Field(
        description="Map host parallel devices (n is 0 to 2).",
        serialization_alias="parallel[n]",
    )
    protection: bool | int | str | None = Field(
        default=0,
        description="Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.",
    )
    reboot: bool | int | str | None = Field(
        default=1,
        description="Allow reboot. If set to \u00270\u0027 the VM exit on reboot.",
    )
    revert: str | None = Field(
        description="Revert a pending change.",
    )
    rng0: str | None = Field(
        description="Configure a VirtIO-based Random Number Generator.",
    )
    sata_n_: str | None = Field(
        description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="sata[n]",
    )
    scsi_n_: str | None = Field(
        description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="scsi[n]",
    )
    scsihw: Literal["lsi", "lsi53c810", "megasas", "pvscsi", "virtio-scsi-pci", "virtio-scsi-single"] | None = Field(
        default="lsi",
        description="SCSI controller model",
    )
    searchdomain: str | None = Field(
        description="cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.",
    )
    serial_n_: str | None = Field(
        description="Create a serial device inside the VM (n is 0 to 3)",
        serialization_alias="serial[n]",
    )
    shares: int | str | None = Field(
        default=1000,
        ge=0,
        le=50000,
        description="Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    smbios1: str | None = Field(
        max_length=512,
        description="Specify SMBIOS type 1 fields.",
    )
    smp: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of CPUs. Please use option -sockets instead.",
    )
    sockets: int | str | None = Field(
        default=1,
        ge=1,
        description="The number of CPU sockets.",
    )
    spice_enhancements: str | None = Field(
        description="Configure additional enhancements for SPICE.",
    )
    sshkeys: str | None = Field(
        description="cloud-init: Setup public SSH keys (one key per line, OpenSSH format).",
    )
    startdate: str | None = Field(
        default="now",
        description="Set the initial date of the real time clock. Valid format for date are:\u0027now\u0027 or \u00272006-06-17T16:01:21\u0027 or \u00272006-06-17\u0027.",
    )
    startup: str | None = Field(
        description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the \u0027up\u0027 or \u0027down\u0027 delay in seconds, which specifies a delay to wait before the next VM is started or stopped.",
    )
    tablet: bool | int | str | None = Field(
        default=1,
        description="Enable/disable the USB tablet device.",
    )
    tags: str | None = Field(
        description="Tags of the VM. This is only meta information.",
    )
    tdf: bool | int | str | None = Field(
        default=0,
        description="Enable/disable time drift fix.",
    )
    template: bool | int | str | None = Field(
        default=0,
        description="Enable/disable Template.",
    )
    tpmstate0: str | None = Field(
        description="Configure a Disk for storing TPM state. The format is fixed to \u0027raw\u0027. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
    )
    unused_n_: str | None = Field(
        description="Reference to unused volumes. This is used internally, and should not be modified manually.",
        serialization_alias="unused[n]",
    )
    usb_n_: str | None = Field(
        description="Configure an USB device (n is 0 to 4, for machine version \u003e= 7.1 and ostype l26 or windows \u003e 7, n can be up to 14).",
        serialization_alias="usb[n]",
    )
    vcpus: int | str | None = Field(
        default=0,
        ge=1,
        description="Number of hotplugged vcpus.",
    )
    vga: str | None = Field(
        description="Configure the VGA hardware.",
    )
    virtio_n_: str | None = Field(
        description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the \u0027import-from\u0027 parameter to import from an existing volume.",
        serialization_alias="virtio[n]",
    )
    vmgenid: str | None = Field(
        default="1 (autogenerated)",
        description="Set VM Generation ID. Use \u00271\u0027 to autogenerate on create or update, pass \u00270\u0027 to disable explicitly.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    vmstatestorage: str | None = Field(
        description="Default storage for VM state volumes/files.",
    )
    watchdog: str | None = Field(
        description="Create a virtual hardware watchdog device.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_PendingGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/pending GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_PendingGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/pending GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_CloudinitGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/cloudinit GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_CloudinitGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/cloudinit GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_CloudinitPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/cloudinit PUT
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Cloudinit_DumpGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/cloudinit/dump GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    type: Literal["meta", "network", "user"] = Field(
        description="Config type.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Cloudinit_DumpGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/cloudinit/dump GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_UnlinkPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/unlink PUT
    """
    force: bool | int | str | None = Field(
        description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called \u0027unused[n]\u0027, which contains the volume ID. Unlink of unused[n] always cause physical removal.",
    )
    idlist: str = Field(
        description="A list of disk IDs you want to delete.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_VncproxyPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/vncproxy POST
    """
    generate_password: bool | int | str | None = Field(
        default=0,
        description="Generates a random password to be used as ticket instead of the API ticket.",
        serialization_alias="generate-password",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    websocket: bool | int | str | None = Field(
        description="starts websockify instead of vncproxy",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_VncproxyPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/vncproxy POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_TermproxyPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/termproxy POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    serial: Literal["serial0", "serial1", "serial2", "serial3"] | None = Field(
        description="opens a serial terminal (defaults to display)",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_TermproxyPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/termproxy POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_VncwebsocketGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/vncwebsocket GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    port: int | str = Field(
        ge=5900,
        le=5999,
        description="Port number returned by previous vncproxy call.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    vncticket: str = Field(
        max_length=512,
        description="Ticket from previous call to vncproxy.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_VncwebsocketGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/vncwebsocket GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_SpiceproxyPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/spiceproxy POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    proxy: str | None = Field(
        description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs \u0027spiceproxy\u0027, so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_SpiceproxyPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/spiceproxy POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_CurrentGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status/current GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_CurrentGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status/current GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_StartPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status/start POST
    """
    force_cpu: str | None = Field(
        description="Override QEMU\u0027s -cpu argument with the given string.",
        serialization_alias="force-cpu",
    )
    machine: str | None = Field(
        max_length=40,
        description="Specifies the QEMU machine type.",
    )
    migratedfrom: ProxmoxNode | None = Field(
        description="The cluster node name.",
    )
    migration_network: str | None = Field(
        description="CIDR of the (sub) network that is used for migration.",
    )
    migration_type: Literal["insecure", "secure"] | None = Field(
        description="Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    stateuri: str | None = Field(
        max_length=128,
        description="Some command save/restore state from this location.",
    )
    targetstorage: str | None = Field(
        description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value \u00271\u0027 will map each source storage to itself.",
    )
    timeout: int | str | None = Field(
        default="max(30, vm memory in GiB)",
        ge=0,
        description="Wait maximal timeout seconds.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_StartPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status/start POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_StopPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status/stop POST
    """
    keepActive: bool | int | str | None = Field(
        default=0,
        description="Do not deactivate storage volumes.",
    )
    migratedfrom: ProxmoxNode | None = Field(
        description="The cluster node name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    timeout: int | str | None = Field(
        ge=0,
        description="Wait maximal timeout seconds.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_StopPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status/stop POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_ResetPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status/reset POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_ResetPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status/reset POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_ShutdownPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status/shutdown POST
    """
    forceStop: bool | int | str | None = Field(
        default=0,
        description="Make sure the VM stops.",
    )
    keepActive: bool | int | str | None = Field(
        default=0,
        description="Do not deactivate storage volumes.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    timeout: int | str | None = Field(
        ge=0,
        description="Wait maximal timeout seconds.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_ShutdownPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status/shutdown POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_RebootPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status/reboot POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeout: int | str | None = Field(
        ge=0,
        description="Wait maximal timeout seconds for the shutdown.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_RebootPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status/reboot POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_SuspendPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status/suspend POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    statestorage: str | None = Field(
        description="The storage for the VM state",
    )
    todisk: bool | int | str | None = Field(
        default=0,
        description="If set, suspends the VM to disk. Will be resumed on next VM start.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_SuspendPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status/suspend POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_ResumePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/status/resume POST
    """
    nocheck: bool | int | str | None = Field(
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Status_ResumePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/status/resume POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_SendkeyPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/sendkey PUT
    """
    key: str = Field(
        description="The key (qemu monitor encoding).",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_FeatureGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/feature GET
    """
    feature: Literal["clone", "copy", "snapshot"] = Field(
        description="Feature to check.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str | None = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_FeatureGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/feature GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_ClonePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/clone POST
    """
    bwlimit: int | str | None = Field(
        default="clone limit from datacenter or storage config",
        ge=0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    description: str | None = Field(
        description="Description for the new VM.",
    )
    format: Literal["qcow2", "raw", "vmdk"] | None = Field(
        description="Target format for file storage. Only valid for full clone.",
    )
    full: bool | int | str | None = Field(
        description="Create a full copy of all disks. This is always done when you clone a normal VM. For VM templates, we try to create a linked clone by default.",
    )
    name: str | None = Field(
        description="Set a name for the new VM.",
    )
    newid: ProxmoxVMID = Field(
        ge=1,
        description="VMID for the clone.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pool: str | None = Field(
        description="Add the new VM to the specified pool.",
    )
    snapname: str | None = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    storage: str | None = Field(
        description="Target storage for full clone.",
    )
    target: ProxmoxNode | None = Field(
        description="Target node. Only allowed if the original VM is on shared storage.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_ClonePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/clone POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Move_DiskPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/move_disk POST
    """
    bwlimit: int | str | None = Field(
        default="move limit from datacenter or storage config",
        ge=0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    delete: bool | int | str | None = Field(
        default=0,
        description="Delete the original disk after successful copy. By default the original disk is kept as unused disk.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1\"\n\t\t    .\" digest. This can be used to prevent concurrent modifications.",
    )
    disk: str = Field(
        description="The disk you want to move.",
    )
    format: Literal["qcow2", "raw", "vmdk"] | None = Field(
        description="Target Format.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str | None = Field(
        description="Target storage.",
    )
    target_digest: str | None = Field(
        max_length=40,
        description="Prevent changes if the current config file of the target VM has a\"\n\t\t    .\" different SHA1 digest. This can be used to detect concurrent modifications.",
        serialization_alias="target-digest",
    )
    target_disk: str | None = Field(
        description="The config key the disk will be moved to on the target VM (for example, ide0 or scsi1). Default is the source disk key.",
        serialization_alias="target-disk",
    )
    target_vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="The (unique) ID of the VM.",
        serialization_alias="target-vmid",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Move_DiskPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/move_disk POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MigrateGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/migrate GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    target: ProxmoxNode | None = Field(
        description="Target node.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MigrateGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/migrate GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MigratePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/migrate POST
    """
    bwlimit: int | str | None = Field(
        default="migrate limit from datacenter or storage config",
        ge=0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    force: bool | int | str | None = Field(
        description="Allow to migrate VMs which use local devices. Only root may use this option.",
    )
    migration_network: str | None = Field(
        description="CIDR of the (sub) network that is used for migration.",
    )
    migration_type: Literal["insecure", "secure"] | None = Field(
        description="Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    online: bool | int | str | None = Field(
        description="Use online/live migration if VM is running. Ignored if VM is stopped.",
    )
    target: ProxmoxNode = Field(
        description="Target node.",
    )
    targetstorage: str | None = Field(
        description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value \u00271\u0027 will map each source storage to itself.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    with_local_disks: bool | int | str | None = Field(
        description="Enable live storage migration for local disk",
        serialization_alias="with-local-disks",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MigratePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/migrate POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Remote_MigratePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/remote_migrate POST
    """
    bwlimit: int | str | None = Field(
        default="migrate limit from datacenter or storage config",
        ge=0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    delete: bool | int | str | None = Field(
        default=0,
        description="Delete the original VM and related data after successful migration. By default the original VM is kept on the source cluster in a stopped state.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    online: bool | int | str | None = Field(
        description="Use online/live migration if VM is running. Ignored if VM is stopped.",
    )
    target_bridge: str = Field(
        description="Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value \u00271\u0027 will map each source bridge to itself.",
        serialization_alias="target-bridge",
    )
    target_endpoint: str = Field(
        description="Remote target endpoint",
        serialization_alias="target-endpoint",
    )
    target_storage: str = Field(
        description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value \u00271\u0027 will map each source storage to itself.",
        serialization_alias="target-storage",
    )
    target_vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="The (unique) ID of the VM.",
        serialization_alias="target-vmid",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Remote_MigratePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/remote_migrate POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MonitorPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/monitor POST
    """
    command: str = Field(
        description="The monitor command.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MonitorPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/monitor POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_ResizePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/resize PUT
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    disk: str = Field(
        description="The disk you want to resize.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    size: str = Field(
        description="The new size. With the `+` sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_SnapshotGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/snapshot GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_SnapshotGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/snapshot GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_SnapshotPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/snapshot POST
    """
    description: str | None = Field(
        description="A textual description or comment.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    vmstate: bool | int | str | None = Field(
        description="Save the vmstate",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_SnapshotPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/snapshot POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_SnapnameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname} DELETE
    """
    force: bool | int | str | None = Field(
        description="For removal from config file, even if removing disk snapshots fails.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_SnapnameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_SnapnameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_SnapnameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_Snapname_ConfigGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/config GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_Snapname_ConfigGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/config GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_Snapname_ConfigPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/config PUT
    """
    description: str | None = Field(
        description="A textual description or comment.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_Snapname_RollbackPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    start: bool | int | str | None = Field(
        default=0,
        description="Whether the VM should get started after rolling back successfully. (Note: VMs will be automatically started if the snapshot includes RAM.)",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_Snapshot_Snapname_RollbackPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_TemplatePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/template POST
    """
    disk: str | None = Field(
        description="If you want to convert only 1 disk to base image.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_TemplatePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/template POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MtunnelPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/mtunnel POST
    """
    bridges: str | None = Field(
        description="List of network bridges to check availability. Will be checked again for actually used bridges during migration.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storages: list[str] | None = Field(
        description="List of storages to check permission and availability. Will be checked again for all actually used storages during migration.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MtunnelPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/mtunnel POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MtunnelwebsocketGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/qemu/{vmid}/mtunnelwebsocket GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    socket: str = Field(
        description="unix socket to forward to",
    )
    ticket: str = Field(
        description="ticket return by initial \u0027mtunnel\u0027 API call, or retrieved via \u0027ticket\u0027 tunnel command",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Qemu_Vmid_MtunnelwebsocketGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/qemu/{vmid}/mtunnelwebsocket GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_LxcGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_LxcGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_LxcPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc POST
    """
    arch: Literal["amd64", "arm64", "armhf", "i386", "riscv32", "riscv64"] | None = Field(
        default="amd64",
        description="OS architecture type.",
    )
    bwlimit: float | str | None = Field(
        default="restore limit from datacenter or storage config",
        ge=0.0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    cmode: Literal["console", "shell", "tty"] | None = Field(
        default="tty",
        description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to \u0027console\u0027 it tries to attach to /dev/console instead. If you set cmode to \u0027shell\u0027, it simply invokes a shell inside the container (no login).",
    )
    console: bool | int | str | None = Field(
        default=1,
        description="Attach a console device (/dev/console) to the container.",
    )
    cores: int | str | None = Field(
        ge=1,
        le=8192,
        description="The number of cores assigned to the container. A container can use all available cores by default.",
    )
    cpulimit: float | str | None = Field(
        default=0,
        ge=0.0,
        le=8192.0,
        description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of \u00272\u0027 CPU time. Value \u00270\u0027 indicates no CPU limit.",
    )
    cpuunits: int | str | None = Field(
        default="cgroup v1: 1024, cgroup v2: 100",
        ge=0,
        le=500000,
        description="CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.",
    )
    debug: bool | int | str | None = Field(
        default=0,
        description="Try to be more verbose. For now this only enables debug log-level on start.",
    )
    description: str | None = Field(
        max_length=8192,
        description="Description for the Container. Shown in the web-interface CT\u0027s summary. This is saved as comment inside the configuration file.",
    )
    features: str | None = Field(
        description="Allow containers access to advanced features.",
    )
    force: bool | int | str | None = Field(
        description="Allow to overwrite existing container.",
    )
    hookscript: str | None = Field(
        description="Script that will be exectued during various steps in the containers lifetime.",
    )
    hostname: str | None = Field(
        max_length=255,
        description="Set a host name for the container.",
    )
    ignore_unpack_errors: bool | int | str | None = Field(
        description="Ignore errors when extracting the template.",
        serialization_alias="ignore-unpack-errors",
    )
    lock: Literal["backup", "create", "destroyed", "disk", "fstrim", "migrate", "mounted", "rollback", "snapshot", "snapshot-delete"] | None = Field(
        description="Lock/unlock the container.",
    )
    memory: int | str | None = Field(
        default=512,
        ge=16,
        description="Amount of RAM for the container in MB.",
    )
    mp_n_: str | None = Field(
        description="Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.",
        serialization_alias="mp[n]",
    )
    nameserver: str | None = Field(
        description="Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.",
    )
    net_n_: str | None = Field(
        description="Specifies network interfaces for the container.",
        serialization_alias="net[n]",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    onboot: bool | int | str | None = Field(
        default=0,
        description="Specifies whether a container will be started during system bootup.",
    )
    ostemplate: str = Field(
        max_length=255,
        description="The OS template or backup file.",
    )
    ostype: str | None = Field(
        description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/\u003costype\u003e.common.conf. Value \u0027unmanaged\u0027 can be used to skip and OS specific setup.",
    )
    password: str | None = Field(
        description="Sets root password inside container.",
    )
    pool: str | None = Field(
        description="Add the VM to the specified pool.",
    )
    protection: bool | int | str | None = Field(
        default=0,
        description="Sets the protection flag of the container. This will prevent the CT or CT\u0027s disk remove/update operation.",
    )
    restore: bool | int | str | None = Field(
        description="Mark this as restore task.",
    )
    rootfs: str | None = Field(
        description="Use volume as container root.",
    )
    searchdomain: str | None = Field(
        description="Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.",
    )
    ssh_public_keys: str | None = Field(
        description="Setup public SSH keys (one key per line, OpenSSH format).",
        serialization_alias="ssh-public-keys",
    )
    start: bool | int | str | None = Field(
        default=0,
        description="Start the CT after its creation finished successfully.",
    )
    startup: str | None = Field(
        description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the \u0027up\u0027 or \u0027down\u0027 delay in seconds, which specifies a delay to wait before the next VM is started or stopped.",
    )
    storage: str | None = Field(
        default="local",
        description="Default Storage.",
    )
    swap: int | str | None = Field(
        default=512,
        ge=0,
        description="Amount of SWAP for the container in MB.",
    )
    tags: str | None = Field(
        description="Tags of the Container. This is only meta information.",
    )
    template: bool | int | str | None = Field(
        default=0,
        description="Enable/disable Template.",
    )
    timezone: str | None = Field(
        description="Time zone to use in the container. If option isn\u0027t set, then nothing will be done. Can be set to \u0027host\u0027 to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab",
    )
    tty: int | str | None = Field(
        default=2,
        ge=0,
        le=6,
        description="Specify the number of tty available to the container",
    )
    unique: bool | int | str | None = Field(
        description="Assign a unique random ethernet address.",
    )
    unprivileged: bool | int | str | None = Field(
        default=0,
        description="Makes the container run as unprivileged user. (Should not be modified manually.)",
    )
    unused_n_: str | None = Field(
        description="Reference to unused volumes. This is used internally, and should not be modified manually.",
        serialization_alias="unused[n]",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_LxcPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_VmidDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid} DELETE
    """
    destroy_unreferenced_disks: bool | int | str | None = Field(
        description="If set, destroy additionally all disks with the VMID from all enabled storages which are not referenced in the config.",
        serialization_alias="destroy-unreferenced-disks",
    )
    force: bool | int | str | None = Field(
        default=0,
        description="Force destroy, even if running.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    purge: bool | int | str | None = Field(
        default=0,
        description="Remove container from all related configurations. For example, backup jobs, replication jobs or HA. Related ACLs and Firewall entries will *always* be removed.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_VmidDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_VmidGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_VmidGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_ConfigGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/config GET
    """
    current: bool | int | str | None = Field(
        default=0,
        description="Get current values (instead of pending values).",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapshot: str | None = Field(
        max_length=40,
        description="Fetch config values from given snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_ConfigGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/config GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_ConfigPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/config PUT
    """
    arch: Literal["amd64", "arm64", "armhf", "i386", "riscv32", "riscv64"] | None = Field(
        default="amd64",
        description="OS architecture type.",
    )
    cmode: Literal["console", "shell", "tty"] | None = Field(
        default="tty",
        description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to \u0027console\u0027 it tries to attach to /dev/console instead. If you set cmode to \u0027shell\u0027, it simply invokes a shell inside the container (no login).",
    )
    console: bool | int | str | None = Field(
        default=1,
        description="Attach a console device (/dev/console) to the container.",
    )
    cores: int | str | None = Field(
        ge=1,
        le=8192,
        description="The number of cores assigned to the container. A container can use all available cores by default.",
    )
    cpulimit: float | str | None = Field(
        default=0,
        ge=0.0,
        le=8192.0,
        description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of \u00272\u0027 CPU time. Value \u00270\u0027 indicates no CPU limit.",
    )
    cpuunits: int | str | None = Field(
        default="cgroup v1: 1024, cgroup v2: 100",
        ge=0,
        le=500000,
        description="CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.",
    )
    debug: bool | int | str | None = Field(
        default=0,
        description="Try to be more verbose. For now this only enables debug log-level on start.",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    description: str | None = Field(
        max_length=8192,
        description="Description for the Container. Shown in the web-interface CT\u0027s summary. This is saved as comment inside the configuration file.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    features: str | None = Field(
        description="Allow containers access to advanced features.",
    )
    hookscript: str | None = Field(
        description="Script that will be exectued during various steps in the containers lifetime.",
    )
    hostname: str | None = Field(
        max_length=255,
        description="Set a host name for the container.",
    )
    lock: Literal["backup", "create", "destroyed", "disk", "fstrim", "migrate", "mounted", "rollback", "snapshot", "snapshot-delete"] | None = Field(
        description="Lock/unlock the container.",
    )
    memory: int | str | None = Field(
        default=512,
        ge=16,
        description="Amount of RAM for the container in MB.",
    )
    mp_n_: str | None = Field(
        description="Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.",
        serialization_alias="mp[n]",
    )
    nameserver: str | None = Field(
        description="Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.",
    )
    net_n_: str | None = Field(
        description="Specifies network interfaces for the container.",
        serialization_alias="net[n]",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    onboot: bool | int | str | None = Field(
        default=0,
        description="Specifies whether a container will be started during system bootup.",
    )
    ostype: str | None = Field(
        description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/\u003costype\u003e.common.conf. Value \u0027unmanaged\u0027 can be used to skip and OS specific setup.",
    )
    protection: bool | int | str | None = Field(
        default=0,
        description="Sets the protection flag of the container. This will prevent the CT or CT\u0027s disk remove/update operation.",
    )
    revert: str | None = Field(
        description="Revert a pending change.",
    )
    rootfs: str | None = Field(
        description="Use volume as container root.",
    )
    searchdomain: str | None = Field(
        description="Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.",
    )
    startup: str | None = Field(
        description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the \u0027up\u0027 or \u0027down\u0027 delay in seconds, which specifies a delay to wait before the next VM is started or stopped.",
    )
    swap: int | str | None = Field(
        default=512,
        ge=0,
        description="Amount of SWAP for the container in MB.",
    )
    tags: str | None = Field(
        description="Tags of the Container. This is only meta information.",
    )
    template: bool | int | str | None = Field(
        default=0,
        description="Enable/disable Template.",
    )
    timezone: str | None = Field(
        description="Time zone to use in the container. If option isn\u0027t set, then nothing will be done. Can be set to \u0027host\u0027 to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab",
    )
    tty: int | str | None = Field(
        default=2,
        ge=0,
        le=6,
        description="Specify the number of tty available to the container",
    )
    unprivileged: bool | int | str | None = Field(
        default=0,
        description="Makes the container run as unprivileged user. (Should not be modified manually.)",
    )
    unused_n_: str | None = Field(
        description="Reference to unused volumes. This is used internally, and should not be modified manually.",
        serialization_alias="unused[n]",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/status GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/status GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_CurrentGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/status/current GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_CurrentGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/status/current GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_StartPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/status/start POST
    """
    debug: bool | int | str | None = Field(
        default=0,
        description="If set, enables very verbose debug log-level on start.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_StartPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/status/start POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_StopPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/status/stop POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skiplock: bool | int | str | None = Field(
        description="Ignore locks - only root is allowed to use this option.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_StopPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/status/stop POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_ShutdownPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/status/shutdown POST
    """
    forceStop: bool | int | str | None = Field(
        default=0,
        description="Make sure the Container stops.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeout: int | str | None = Field(
        default=60,
        ge=0,
        description="Wait maximal timeout seconds.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_ShutdownPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/status/shutdown POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_SuspendPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/status/suspend POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_SuspendPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/status/suspend POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_ResumePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/status/resume POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_ResumePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/status/resume POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_RebootPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/status/reboot POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeout: int | str | None = Field(
        ge=0,
        description="Wait maximal timeout seconds for the shutdown.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Status_RebootPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/status/reboot POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_SnapshotGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/snapshot GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_SnapshotGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/snapshot GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_SnapshotPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/snapshot POST
    """
    description: str | None = Field(
        description="A textual description or comment.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_SnapshotPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/snapshot POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_SnapnameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname} DELETE
    """
    force: bool | int | str | None = Field(
        description="For removal from config file, even if removing disk snapshots fails.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_SnapnameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_SnapnameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_SnapnameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_Snapname_RollbackPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/rollback POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    start: bool | int | str | None = Field(
        default=0,
        description="Whether the container should get started after rolling back successfully",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_Snapname_RollbackPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/rollback POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/config GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/config GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Snapshot_Snapname_ConfigPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/config PUT
    """
    description: str | None = Field(
        description="A textual description or comment.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_FirewallGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_FirewallGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_RulesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/rules GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_RulesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/rules GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_RulesPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/rules POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
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
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Rules_PosDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/rules/{pos} DELETE
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Rules_PosGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/rules/{pos} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Rules_PosGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/rules/{pos} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Rules_PosPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/rules/{pos} PUT
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
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
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_AliasesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/aliases GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_AliasesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/aliases GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_AliasesPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/aliases POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Aliases_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/aliases/{name} DELETE
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    name: str = Field(
        max_length=64,
        description="Alias name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Aliases_NameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/aliases/{name} GET
    """
    name: str = Field(
        max_length=64,
        description="Alias name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Aliases_NameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/aliases/{name} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Aliases_NamePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/aliases/{name} PUT
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    rename: str | None = Field(
        max_length=64,
        description="Rename an existing alias.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_IpsetGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/ipset GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_IpsetGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/ipset GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_IpsetPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/ipset POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    rename: str | None = Field(
        max_length=64,
        description="Rename an existing IPSet. You can set \u0027rename\u0027 to the same value as \u0027name\u0027 to update the \u0027comment\u0027 of an existing IPSet.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Ipset_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/ipset/{name} DELETE
    """
    force: bool | int | str | None = Field(
        description="Delete all members of the IPSet, if there are any.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Ipset_NameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/ipset/{name} GET
    """
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Ipset_NameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/ipset/{name} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Ipset_NamePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/ipset/{name} POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    nomatch: bool | int | str | None = Field(
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Ipset_Name_CidrDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}/{cidr} DELETE
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Ipset_Name_CidrGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}/{cidr} GET
    """
    cidr: str = Field(
        description="Network/IP specification in CIDR format.",
    )
    name: str = Field(
        max_length=64,
        description="IP set name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Ipset_Name_CidrGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}/{cidr} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_Ipset_Name_CidrPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}/{cidr} PUT
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    nomatch: bool | int | str | None = Field(
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_OptionsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/options GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_OptionsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/options GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_OptionsPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/options PUT
    """
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    dhcp: bool | int | str | None = Field(
        default=0,
        description="Enable DHCP.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    enable: bool | int | str | None = Field(
        default=0,
        description="Enable/disable firewall rules.",
    )
    ipfilter: bool | int | str | None = Field(
        description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net\u003cid\u003e ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface\u0027s MAC address. For containers the configured IP addresses will be implicitly added.",
    )
    log_level_in: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for incoming traffic.",
    )
    log_level_out: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for outgoing traffic.",
    )
    macfilter: bool | int | str | None = Field(
        default=1,
        description="Enable/disable MAC address filter.",
    )
    ndp: bool | int | str | None = Field(
        default=0,
        description="Enable NDP (Neighbor Discovery Protocol).",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    policy_in: Literal["ACCEPT", "DROP", "REJECT"] | None = Field(
        description="Input policy.",
    )
    policy_out: Literal["ACCEPT", "DROP", "REJECT"] | None = Field(
        description="Output policy.",
    )
    radv: bool | int | str | None = Field(
        description="Allow sending Router Advertisement.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_LogGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/log GET
    """
    limit: int | str | None = Field(
        ge=0,
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    since: int | str | None = Field(
        ge=0,
        description="Display log since this UNIX epoch.",
    )
    start: int | str | None = Field(
        ge=0,
    )
    until: int | str | None = Field(
        ge=0,
        description="Display log until this UNIX epoch.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_LogGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/log GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_RefsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/firewall/refs GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    type: Literal["alias", "ipset"] | None = Field(
        description="Only list references of specified type.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Firewall_RefsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/firewall/refs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_RrdGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/rrd GET
    """
    cf: Literal["AVERAGE", "MAX"] | None = Field(
        description="The RRD consolidation function",
    )
    ds: str = Field(
        description="The list of datasources you want to display.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeframe: Literal["day", "hour", "month", "week", "year"] = Field(
        description="Specify the time frame you are interested in.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_RrdGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/rrd GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_RrddataGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/rrddata GET
    """
    cf: Literal["AVERAGE", "MAX"] | None = Field(
        description="The RRD consolidation function",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeframe: Literal["day", "hour", "month", "week", "year"] = Field(
        description="Specify the time frame you are interested in.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_RrddataGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/rrddata GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_VncproxyPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/vncproxy POST
    """
    height: int | str | None = Field(
        ge=16,
        le=2160,
        description="sets the height of the console in pixels.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    websocket: bool | int | str | None = Field(
        description="use websocket instead of standard VNC.",
    )
    width: int | str | None = Field(
        ge=16,
        le=4096,
        description="sets the width of the console in pixels.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_VncproxyPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/vncproxy POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_TermproxyPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/termproxy POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_TermproxyPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/termproxy POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_VncwebsocketGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/vncwebsocket GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    port: int | str = Field(
        ge=5900,
        le=5999,
        description="Port number returned by previous vncproxy call.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    vncticket: str = Field(
        max_length=512,
        description="Ticket from previous call to vncproxy.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_VncwebsocketGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/vncwebsocket GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_SpiceproxyPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/spiceproxy POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    proxy: str | None = Field(
        description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs \u0027spiceproxy\u0027, so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_SpiceproxyPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/spiceproxy POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Remote_MigratePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/remote_migrate POST
    """
    bwlimit: float | str | None = Field(
        default="migrate limit from datacenter or storage config",
        ge=0.0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    delete: bool | int | str | None = Field(
        default=0,
        description="Delete the original CT and related data after successful migration. By default the original CT is kept on the source cluster in a stopped state.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    online: bool | int | str | None = Field(
        description="Use online/live migration.",
    )
    restart: bool | int | str | None = Field(
        description="Use restart migration",
    )
    target_bridge: str = Field(
        description="Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value \u00271\u0027 will map each source bridge to itself.",
        serialization_alias="target-bridge",
    )
    target_endpoint: str = Field(
        description="Remote target endpoint",
        serialization_alias="target-endpoint",
    )
    target_storage: str = Field(
        description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value \u00271\u0027 will map each source storage to itself.",
        serialization_alias="target-storage",
    )
    target_vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="The (unique) ID of the VM.",
        serialization_alias="target-vmid",
    )
    timeout: int | str | None = Field(
        default=180,
        description="Timeout in seconds for shutdown for restart migration",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Remote_MigratePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/remote_migrate POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_MigratePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/migrate POST
    """
    bwlimit: float | str | None = Field(
        default="migrate limit from datacenter or storage config",
        ge=0.0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    online: bool | int | str | None = Field(
        description="Use online/live migration.",
    )
    restart: bool | int | str | None = Field(
        description="Use restart migration",
    )
    target: ProxmoxNode = Field(
        description="Target node.",
    )
    target_storage: str | None = Field(
        description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value \u00271\u0027 will map each source storage to itself.",
        serialization_alias="target-storage",
    )
    timeout: int | str | None = Field(
        default=180,
        description="Timeout in seconds for shutdown for restart migration",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_MigratePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/migrate POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_FeatureGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/feature GET
    """
    feature: Literal["clone", "copy", "snapshot"] = Field(
        description="Feature to check.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    snapname: str | None = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_FeatureGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/feature GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_TemplatePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/template POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_ClonePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/clone POST
    """
    bwlimit: float | str | None = Field(
        default="clone limit from datacenter or storage config",
        ge=0.0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    description: str | None = Field(
        description="Description for the new CT.",
    )
    full: bool | int | str | None = Field(
        description="Create a full copy of all disks. This is always done when you clone a normal CT. For CT templates, we try to create a linked clone by default.",
    )
    hostname: str | None = Field(
        description="Set a hostname for the new CT.",
    )
    newid: ProxmoxVMID = Field(
        ge=1,
        description="VMID for the clone.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pool: str | None = Field(
        description="Add the new CT to the specified pool.",
    )
    snapname: str | None = Field(
        max_length=40,
        description="The name of the snapshot.",
    )
    storage: str | None = Field(
        description="Target storage for full clone.",
    )
    target: ProxmoxNode | None = Field(
        description="Target node. Only allowed if the original VM is on shared storage.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_ClonePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/clone POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_ResizePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/resize PUT
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    disk: str = Field(
        description="The disk you want to resize.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    size: str = Field(
        description="The new size. With the \u0027+\u0027 sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_ResizePUTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/resize PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Move_VolumePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/move_volume POST
    """
    bwlimit: float | str | None = Field(
        default="clone limit from datacenter or storage config",
        ge=0.0,
        description="Override I/O bandwidth limit (in KiB/s).",
    )
    delete: bool | int | str | None = Field(
        default=0,
        description="Delete the original volume after successful copy. By default the original is kept as an unused volume entry.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 \" .\n\t\t    \"digest. This can be used to prevent concurrent modifications.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str | None = Field(
        description="Target Storage.",
    )
    target_digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file of the target \" .\n\t\t    \"container has a different SHA1 digest. This can be used to prevent \" .\n\t\t    \"concurrent modifications.",
        serialization_alias="target-digest",
    )
    target_vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="The (unique) ID of the VM.",
        serialization_alias="target-vmid",
    )
    target_volume: str | None = Field(
        description="The config key the volume will be moved to. Default is the source volume key.",
        serialization_alias="target-volume",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )
    volume: str = Field(
        description="Volume which will be moved.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_Move_VolumePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/move_volume POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_PendingGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/pending GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_PendingGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/pending GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_MtunnelPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/mtunnel POST
    """
    bridges: str | None = Field(
        description="List of network bridges to check availability. Will be checked again for actually used bridges during migration.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storages: list[str] | None = Field(
        description="List of storages to check permission and availability. Will be checked again for all actually used storages during migration.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_MtunnelPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/mtunnel POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_MtunnelwebsocketGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/lxc/{vmid}/mtunnelwebsocket GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    socket: str = Field(
        description="unix socket to forward to",
    )
    ticket: str = Field(
        description="ticket return by initial \u0027mtunnel\u0027 API call, or retrieved via \u0027ticket\u0027 tunnel command",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="The (unique) ID of the VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Lxc_Vmid_MtunnelwebsocketGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/lxc/{vmid}/mtunnelwebsocket GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_CephGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_CephGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_CfgGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/cfg GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_CfgGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/cfg GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Cfg_RawGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/cfg/raw GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Cfg_RawGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/cfg/raw GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Cfg_DbGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/cfg/db GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Cfg_DbGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/cfg/db GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_OsdGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_OsdGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/osd GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_OsdPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd POST
    """
    crush_device_class: str | None = Field(
        description="Set the device class of the OSD in crush.",
        serialization_alias="crush-device-class",
    )
    db_dev: str | None = Field(
        description="Block device name for block.db.",
    )
    db_dev_size: float | str | None = Field(
        default="bluestore_block_db_size or 10% of OSD size",
        ge=1.0,
        description="Size in GiB for block.db.",
    )
    dev: str = Field(
        description="Block device name.",
    )
    encrypted: bool | int | str | None = Field(
        default=0,
        description="Enables encryption of the OSD.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    wal_dev: str | None = Field(
        description="Block device name for block.wal.",
    )
    wal_dev_size: float | str | None = Field(
        default="bluestore_block_wal_size or 1% of OSD size",
        ge=0.5,
        description="Size in GiB for block.wal.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_OsdPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/osd POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_OsdidDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd/{osdid} DELETE
    """
    cleanup: bool | int | str | None = Field(
        default=0,
        description="If set, we remove partition table entries.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    osdid: int | str = Field(
        description="OSD ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_OsdidDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/osd/{osdid} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_OsdidGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd/{osdid} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    osdid: int | str = Field(
        description="OSD ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_OsdidGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/osd/{osdid} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_Osdid_MetadataGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd/{osdid}/metadata GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    osdid: int | str = Field(
        description="OSD ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_Osdid_MetadataGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/osd/{osdid}/metadata GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_Osdid_Lv_InfoGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd/{osdid}/lv-info GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    osdid: int | str = Field(
        description="OSD ID",
    )
    type: Literal["block", "db", "wal"] | None = Field(
        default="block",
        description="OSD device type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_Osdid_Lv_InfoGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/osd/{osdid}/lv-info GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_Osdid_InPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd/{osdid}/in POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    osdid: int | str = Field(
        description="OSD ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_Osdid_OutPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd/{osdid}/out POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    osdid: int | str = Field(
        description="OSD ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Osd_Osdid_ScrubPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/osd/{osdid}/scrub POST
    """
    deep: bool | int | str | None = Field(
        default=0,
        description="If set, instructs a deep scrub instead of a normal one.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    osdid: int | str = Field(
        description="OSD ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_MdsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mds GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_MdsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mds GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mds_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mds/{name} DELETE
    """
    name: str = Field(
        description="The name (ID) of the mds",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mds_NameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mds/{name} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mds_NamePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mds/{name} POST
    """
    hotstandby: bool | int | str | None = Field(
        default="0",
        description="Determines whether a ceph-mds daemon should poll and replay the log of an active MDS. Faster switch on MDS failure, but needs more idle resources.",
    )
    name: str | None = Field(
        default="nodename",
        max_length=200,
        description="The ID for the mds, when omitted the same as the nodename",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mds_NamePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mds/{name} POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_MgrGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mgr GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_MgrGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mgr GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mgr_IdDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mgr/{id} DELETE
    """
    id: str = Field(
        description="The ID of the manager",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mgr_IdDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mgr/{id} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mgr_IdPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mgr/{id} POST
    """
    id: str | None = Field(
        max_length=200,
        description="The ID for the manager, when omitted the same as the nodename",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mgr_IdPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mgr/{id} POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_MonGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mon GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_MonGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mon GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mon_MonidDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mon/{monid} DELETE
    """
    monid: str = Field(
        description="Monitor ID",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mon_MonidDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mon/{monid} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mon_MonidPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/mon/{monid} POST
    """
    mon_address: str | None = Field(
        description="Overwrites autodetected monitor IP address(es). Must be in the public network(s) of Ceph.",
        serialization_alias="mon-address",
    )
    monid: str | None = Field(
        max_length=200,
        description="The ID for the monitor, when omitted the same as the nodename",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Mon_MonidPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/mon/{monid} POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_FsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/fs GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_FsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/fs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Fs_NamePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/fs/{name} POST
    """
    add_storage: bool | int | str | None = Field(
        default=0,
        description="Configure the created CephFS as storage for this cluster.",
        serialization_alias="add-storage",
    )
    name: str | None = Field(
        default="cephfs",
        description="The ceph filesystem name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pg_num: int | str | None = Field(
        default=128,
        ge=8,
        le=32768,
        description="Number of placement groups for the backing data pool. The metadata pool will use a quarter of this.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Fs_NamePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/fs/{name} POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_PoolGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pool GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_PoolGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pool GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_PoolPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pool POST
    """
    add_storages: bool | int | str | None = Field(
        default="0; for erasure coded pools: 1",
        description="Configure VM and CT storage using the new pool.",
    )
    application: Literal["cephfs", "rbd", "rgw"] | None = Field(
        default="rbd",
        description="The application of the pool.",
    )
    crush_rule: str | None = Field(
        description="The rule to use for mapping object placement in the cluster.",
    )
    erasure_coding: str | None = Field(
        description="Create an erasure coded pool for RBD with an accompaning replicated pool for metadata storage. With EC, the common ceph options \u0027size\u0027, \u0027min_size\u0027 and \u0027crush_rule\u0027 parameters will be applied to the metadata pool.",
        serialization_alias="erasure-coding",
    )
    min_size: int | str | None = Field(
        default=2,
        ge=1,
        le=7,
        description="Minimum number of replicas per object",
    )
    name: str = Field(
        description="The name of the pool. It must be unique.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pg_autoscale_mode: Literal["off", "on", "warn"] | None = Field(
        default="warn",
        description="The automatic PG scaling mode of the pool.",
    )
    pg_num: int | str | None = Field(
        default=128,
        ge=1,
        le=32768,
        description="Number of placement groups.",
    )
    pg_num_min: int | str | None = Field(
        le=32768,
        description="Minimal number of placement groups.",
    )
    size: int | str | None = Field(
        default=3,
        ge=1,
        le=7,
        description="Number of replicas per object",
    )
    target_size: str | None = Field(
        description="The estimated target size of the pool for the PG autoscaler.",
    )
    target_size_ratio: float | str | None = Field(
        description="The estimated target ratio of the pool for the PG autoscaler.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_PoolPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pool POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pool_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pool/{name} DELETE
    """
    force: bool | int | str | None = Field(
        default=0,
        description="If true, destroys pool even if in use",
    )
    name: str = Field(
        description="The name of the pool. It must be unique.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    remove_ecprofile: bool | int | str | None = Field(
        default=1,
        description="Remove the erasure code profile. Defaults to true, if applicable.",
    )
    remove_storages: bool | int | str | None = Field(
        default=0,
        description="Remove all pveceph-managed storages configured for this pool",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pool_NameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pool/{name} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pool_NameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pool/{name} GET
    """
    name: str = Field(
        description="The name of the pool.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pool_NameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pool/{name} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pool_NamePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pool/{name} PUT
    """
    application: Literal["cephfs", "rbd", "rgw"] | None = Field(
        description="The application of the pool.",
    )
    crush_rule: str | None = Field(
        description="The rule to use for mapping object placement in the cluster.",
    )
    min_size: int | str | None = Field(
        ge=1,
        le=7,
        description="Minimum number of replicas per object",
    )
    name: str = Field(
        description="The name of the pool. It must be unique.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pg_autoscale_mode: Literal["off", "on", "warn"] | None = Field(
        description="The automatic PG scaling mode of the pool.",
    )
    pg_num: int | str | None = Field(
        ge=1,
        le=32768,
        description="Number of placement groups.",
    )
    pg_num_min: int | str | None = Field(
        le=32768,
        description="Minimal number of placement groups.",
    )
    size: int | str | None = Field(
        ge=1,
        le=7,
        description="Number of replicas per object",
    )
    target_size: str | None = Field(
        description="The estimated target size of the pool for the PG autoscaler.",
    )
    target_size_ratio: float | str | None = Field(
        description="The estimated target ratio of the pool for the PG autoscaler.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pool_NamePUTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pool/{name} PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pool_Name_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pool/{name}/status GET
    """
    name: str = Field(
        description="The name of the pool. It must be unique.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    verbose: bool | int | str | None = Field(
        default=0,
        description="If enabled, will display additional data(eg. statistics).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pool_Name_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pool/{name}/status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_PoolsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pools GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_PoolsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pools GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_PoolsPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pools POST
    """
    add_storages: bool | int | str | None = Field(
        default="0; for erasure coded pools: 1",
        description="Configure VM and CT storage using the new pool.",
    )
    application: Literal["cephfs", "rbd", "rgw"] | None = Field(
        default="rbd",
        description="The application of the pool.",
    )
    crush_rule: str | None = Field(
        description="The rule to use for mapping object placement in the cluster.",
    )
    erasure_coding: str | None = Field(
        description="Create an erasure coded pool for RBD with an accompaning replicated pool for metadata storage. With EC, the common ceph options \u0027size\u0027, \u0027min_size\u0027 and \u0027crush_rule\u0027 parameters will be applied to the metadata pool.",
        serialization_alias="erasure-coding",
    )
    min_size: int | str | None = Field(
        default=2,
        ge=1,
        le=7,
        description="Minimum number of replicas per object",
    )
    name: str = Field(
        description="The name of the pool. It must be unique.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pg_autoscale_mode: Literal["off", "on", "warn"] | None = Field(
        default="warn",
        description="The automatic PG scaling mode of the pool.",
    )
    pg_num: int | str | None = Field(
        default=128,
        ge=1,
        le=32768,
        description="Number of placement groups.",
    )
    pg_num_min: int | str | None = Field(
        le=32768,
        description="Minimal number of placement groups.",
    )
    size: int | str | None = Field(
        default=3,
        ge=1,
        le=7,
        description="Number of replicas per object",
    )
    target_size: str | None = Field(
        description="The estimated target size of the pool for the PG autoscaler.",
    )
    target_size_ratio: float | str | None = Field(
        description="The estimated target ratio of the pool for the PG autoscaler.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_PoolsPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pools POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pools_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pools/{name} DELETE
    """
    force: bool | int | str | None = Field(
        default=0,
        description="If true, destroys pool even if in use",
    )
    name: str = Field(
        description="The name of the pool. It must be unique.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    remove_ecprofile: bool | int | str | None = Field(
        default=1,
        description="Remove the erasure code profile. Defaults to true, if applicable.",
    )
    remove_storages: bool | int | str | None = Field(
        default=0,
        description="Remove all pveceph-managed storages configured for this pool",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pools_NameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pools/{name} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pools_NameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pools/{name} GET
    """
    name: str = Field(
        description="The name of the pool. It must be unique.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    verbose: bool | int | str | None = Field(
        default=0,
        description="If enabled, will display additional data(eg. statistics).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pools_NameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pools/{name} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pools_NamePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/pools/{name} PUT
    """
    application: Literal["cephfs", "rbd", "rgw"] | None = Field(
        description="The application of the pool.",
    )
    crush_rule: str | None = Field(
        description="The rule to use for mapping object placement in the cluster.",
    )
    min_size: int | str | None = Field(
        ge=1,
        le=7,
        description="Minimum number of replicas per object",
    )
    name: str = Field(
        description="The name of the pool. It must be unique.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pg_autoscale_mode: Literal["off", "on", "warn"] | None = Field(
        description="The automatic PG scaling mode of the pool.",
    )
    pg_num: int | str | None = Field(
        ge=1,
        le=32768,
        description="Number of placement groups.",
    )
    pg_num_min: int | str | None = Field(
        le=32768,
        description="Minimal number of placement groups.",
    )
    size: int | str | None = Field(
        ge=1,
        le=7,
        description="Number of replicas per object",
    )
    target_size: str | None = Field(
        description="The estimated target size of the pool for the PG autoscaler.",
    )
    target_size_ratio: float | str | None = Field(
        description="The estimated target ratio of the pool for the PG autoscaler.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Pools_NamePUTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/pools/{name} PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_ConfigGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/config GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_ConfigGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/config GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_ConfigdbGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/configdb GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_ConfigdbGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/configdb GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_InitPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/init POST
    """
    cluster_network: str | None = Field(
        max_length=128,
        description="Declare a separate cluster network, OSDs will routeheartbeat, object replication and recovery traffic over it",
        serialization_alias="cluster-network",
    )
    disable_cephx: bool | int | str | None = Field(
        default=0,
        description="Disable cephx authentication.\n\nWARNING: cephx is a security feature protecting against man-in-the-middle attacks. Only consider disabling cephx if your network is private!",
    )
    min_size: int | str | None = Field(
        default=2,
        ge=1,
        le=7,
        description="Minimum number of available replicas per object to allow I/O",
    )
    network: str | None = Field(
        max_length=128,
        description="Use specific network for all ceph related traffic",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pg_bits: int | str | None = Field(
        default=6,
        ge=6,
        le=14,
        description="Placement group bits, used to specify the default number of placement groups.\n\nNOTE: \u0027osd pool default pg num\u0027 does not work for default pools.",
    )
    size: int | str | None = Field(
        default=3,
        ge=1,
        le=7,
        description="Targeted number of replicas per object",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_StopPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/stop POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str | None = Field(
        default="ceph.target",
        description="Ceph service name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_StopPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/stop POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_StartPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/start POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str | None = Field(
        default="ceph.target",
        description="Ceph service name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_StartPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/start POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_RestartPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/restart POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str | None = Field(
        default="ceph.target",
        description="Ceph service name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_RestartPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/restart POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/status GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_CrushGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/crush GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_CrushGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/crush GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_LogGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/log GET
    """
    limit: int | str | None = Field(
        ge=0,
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    start: int | str | None = Field(
        ge=0,
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_LogGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/log GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_RulesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/rules GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_RulesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/rules GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Cmd_SafetyGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/ceph/cmd-safety GET
    """
    action: Literal["destroy", "stop"] = Field(
        description="Action to check",
    )
    id: str = Field(
        description="ID of the service",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: Literal["mds", "mon", "osd"] = Field(
        description="Service type",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Ceph_Cmd_SafetyGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/ceph/cmd-safety GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_VzdumpPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/vzdump POST
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
    compress: Literal["0", "1", "gzip", "lzo", "zstd"] | None = Field(
        default="0",
        description="Compress dump file.",
    )
    dumpdir: str | None = Field(
        description="Store resulting files to specified directory.",
    )
    exclude: list[ProxmoxVMID] | None = Field(
        description="Exclude specified guest systems (assumes --all)",
    )
    exclude_path: str | None = Field(
        description="Exclude certain files/directories (shell globs). Paths starting with \u0027/\u0027 are anchored to the container\u0027s root,  other paths match relative to each subdirectory.",
        serialization_alias="exclude-path",
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
    script: str | None = Field(
        description="Use specified hook script.",
    )
    stdexcludes: bool | int | str | None = Field(
        default=1,
        description="Exclude temporary files and logs.",
    )
    stdout: bool | int | str | None = Field(
        description="Write tar to stdout, not to a file.",
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

class Nodes_Node_VzdumpPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/vzdump POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Vzdump_DefaultsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/vzdump/defaults GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str | None = Field(
        description="The storage identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Vzdump_DefaultsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/vzdump/defaults GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Vzdump_ExtractconfigGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/vzdump/extractconfig GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    volume: str = Field(
        description="Volume identifier",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Vzdump_ExtractconfigGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/vzdump/extractconfig GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ServicesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/services GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ServicesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/services GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_ServiceGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/services/{service} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str = Field(
        description="Service ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_ServiceGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/services/{service} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_StateGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/services/{service}/state GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str = Field(
        description="Service ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_StateGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/services/{service}/state GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_StartPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/services/{service}/start POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str = Field(
        description="Service ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_StartPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/services/{service}/start POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_StopPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/services/{service}/stop POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str = Field(
        description="Service ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_StopPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/services/{service}/stop POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_RestartPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/services/{service}/restart POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str = Field(
        description="Service ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_RestartPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/services/{service}/restart POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_ReloadPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/services/{service}/reload POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str = Field(
        description="Service ID",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Services_Service_ReloadPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/services/{service}/reload POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SubscriptionDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/subscription DELETE
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SubscriptionGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/subscription GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SubscriptionGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/subscription GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SubscriptionPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/subscription POST
    """
    force: bool | int | str | None = Field(
        default=0,
        description="Always connect to server, even if we have up to date info inside local cache.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SubscriptionPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/subscription PUT
    """
    key: str = Field(
        max_length=32,
        description="Proxmox VE subscription key",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_NetworkDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/network DELETE
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_NetworkGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/network GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    type: Literal["OVSBond", "OVSBridge", "OVSIntPort", "OVSPort", "alias", "any_bridge", "bond", "bridge", "eth", "vlan"] | None = Field(
        description="Only list specific interface types.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_NetworkGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/network GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_NetworkPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/network POST
    """
    address: str | None = Field(
        description="IP address.",
    )
    address6: str | None = Field(
        description="IP address.",
    )
    autostart: bool | int | str | None = Field(
        description="Automatically start interface on boot.",
    )
    bond_primary: str | None = Field(
        description="Specify the primary interface for active-backup bond.",
        serialization_alias="bond-primary",
    )
    bond_mode: Literal["802.3ad", "active-backup", "balance-alb", "balance-rr", "balance-slb", "balance-tlb", "balance-xor", "broadcast", "lacp-balance-slb", "lacp-balance-tcp"] | None = Field(
        description="Bonding mode.",
    )
    bond_xmit_hash_policy: Literal["layer2", "layer2+3", "layer3+4"] | None = Field(
        description="Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.",
    )
    bridge_ports: str | None = Field(
        description="Specify the interfaces you want to add to your bridge.",
    )
    bridge_vlan_aware: bool | int | str | None = Field(
        description="Enable bridge vlan support.",
    )
    cidr: str | None = Field(
        description="IPv4 CIDR.",
    )
    cidr6: str | None = Field(
        description="IPv6 CIDR.",
    )
    comments: str | None = Field(
        description="Comments",
    )
    comments6: str | None = Field(
        description="Comments",
    )
    gateway: str | None = Field(
        description="Default gateway address.",
    )
    gateway6: str | None = Field(
        description="Default ipv6 gateway address.",
    )
    iface: str = Field(
        max_length=20,
        description="Network interface name.",
    )
    mtu: int | str | None = Field(
        ge=1280,
        le=65520,
        description="MTU.",
    )
    netmask: str | None = Field(
        description="Network mask.",
    )
    netmask6: int | str | None = Field(
        ge=0,
        le=128,
        description="Network mask.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    ovs_bonds: str | None = Field(
        description="Specify the interfaces used by the bonding device.",
    )
    ovs_bridge: str | None = Field(
        description="The OVS bridge associated with a OVS port. This is required when you create an OVS port.",
    )
    ovs_options: str | None = Field(
        max_length=1024,
        description="OVS interface options.",
    )
    ovs_ports: str | None = Field(
        description="Specify the interfaces you want to add to your bridge.",
    )
    ovs_tag: int | str | None = Field(
        ge=1,
        le=4094,
        description="Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)",
    )
    slaves: str | None = Field(
        description="Specify the interfaces used by the bonding device.",
    )
    type: Literal["OVSBond", "OVSBridge", "OVSIntPort", "OVSPort", "alias", "bond", "bridge", "eth", "unknown", "vlan"] = Field(
        description="Network interface type",
    )
    vlan_id: int | str | None = Field(
        ge=1,
        le=4094,
        description="vlan-id for a custom named vlan interface (ifupdown2 only).",
        serialization_alias="vlan-id",
    )
    vlan_raw_device: str | None = Field(
        description="Specify the raw interface for the vlan interface.",
        serialization_alias="vlan-raw-device",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_NetworkPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/network PUT
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_NetworkPUTResponse(BaseModel):
    """
    Response model for /nodes/{node}/network PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Network_IfaceDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/network/{iface} DELETE
    """
    iface: str = Field(
        max_length=20,
        description="Network interface name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Network_IfaceGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/network/{iface} GET
    """
    iface: str = Field(
        max_length=20,
        description="Network interface name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Network_IfaceGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/network/{iface} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Network_IfacePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/network/{iface} PUT
    """
    address: str | None = Field(
        description="IP address.",
    )
    address6: str | None = Field(
        description="IP address.",
    )
    autostart: bool | int | str | None = Field(
        description="Automatically start interface on boot.",
    )
    bond_primary: str | None = Field(
        description="Specify the primary interface for active-backup bond.",
        serialization_alias="bond-primary",
    )
    bond_mode: Literal["802.3ad", "active-backup", "balance-alb", "balance-rr", "balance-slb", "balance-tlb", "balance-xor", "broadcast", "lacp-balance-slb", "lacp-balance-tcp"] | None = Field(
        description="Bonding mode.",
    )
    bond_xmit_hash_policy: Literal["layer2", "layer2+3", "layer3+4"] | None = Field(
        description="Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.",
    )
    bridge_ports: str | None = Field(
        description="Specify the interfaces you want to add to your bridge.",
    )
    bridge_vlan_aware: bool | int | str | None = Field(
        description="Enable bridge vlan support.",
    )
    cidr: str | None = Field(
        description="IPv4 CIDR.",
    )
    cidr6: str | None = Field(
        description="IPv6 CIDR.",
    )
    comments: str | None = Field(
        description="Comments",
    )
    comments6: str | None = Field(
        description="Comments",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    gateway: str | None = Field(
        description="Default gateway address.",
    )
    gateway6: str | None = Field(
        description="Default ipv6 gateway address.",
    )
    iface: str = Field(
        max_length=20,
        description="Network interface name.",
    )
    mtu: int | str | None = Field(
        ge=1280,
        le=65520,
        description="MTU.",
    )
    netmask: str | None = Field(
        description="Network mask.",
    )
    netmask6: int | str | None = Field(
        ge=0,
        le=128,
        description="Network mask.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    ovs_bonds: str | None = Field(
        description="Specify the interfaces used by the bonding device.",
    )
    ovs_bridge: str | None = Field(
        description="The OVS bridge associated with a OVS port. This is required when you create an OVS port.",
    )
    ovs_options: str | None = Field(
        max_length=1024,
        description="OVS interface options.",
    )
    ovs_ports: str | None = Field(
        description="Specify the interfaces you want to add to your bridge.",
    )
    ovs_tag: int | str | None = Field(
        ge=1,
        le=4094,
        description="Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)",
    )
    slaves: str | None = Field(
        description="Specify the interfaces used by the bonding device.",
    )
    type: Literal["OVSBond", "OVSBridge", "OVSIntPort", "OVSPort", "alias", "bond", "bridge", "eth", "unknown", "vlan"] = Field(
        description="Network interface type",
    )
    vlan_id: int | str | None = Field(
        ge=1,
        le=4094,
        description="vlan-id for a custom named vlan interface (ifupdown2 only).",
        serialization_alias="vlan-id",
    )
    vlan_raw_device: str | None = Field(
        description="Specify the raw interface for the vlan interface.",
        serialization_alias="vlan-raw-device",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_TasksGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/tasks GET
    """
    errors: bool | int | str | None = Field(
        default=0,
        description="Only list tasks with a status of ERROR.",
    )
    limit: int | str | None = Field(
        default=50,
        ge=0,
        description="Only list this amount of tasks.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    since: int | str | None = Field(
        description="Only list tasks since this UNIX epoch.",
    )
    source: Literal["active", "all", "archive"] | None = Field(
        default="archive",
        description="List archived, active or all tasks.",
    )
    start: int | str | None = Field(
        default=0,
        ge=0,
        description="List tasks beginning from this offset.",
    )
    statusfilter: str | None = Field(
        description="List of Task States that should be returned.",
    )
    typefilter: str | None = Field(
        description="Only list tasks of this type (e.g., vzstart, vzdump).",
    )
    until: int | str | None = Field(
        description="Only list tasks until this UNIX epoch.",
    )
    userfilter: str | None = Field(
        description="Only list tasks from this user.",
    )
    vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="Only list tasks for this VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_TasksGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/tasks GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Tasks_UpidDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/tasks/{upid} DELETE
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    upid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Tasks_UpidGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/tasks/{upid} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    upid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Tasks_UpidGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/tasks/{upid} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Tasks_Upid_LogGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/tasks/{upid}/log GET
    """
    download: bool | int | str | None = Field(
        description="Whether the tasklog file should be downloaded. This parameter can\u0027t be used in conjunction with other parameters",
    )
    limit: int | str | None = Field(
        default=50,
        ge=0,
        description="The amount of lines to read from the tasklog.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    start: int | str | None = Field(
        default=0,
        ge=0,
        description="Start at this line when reading the tasklog",
    )
    upid: str = Field(
        description="The task\u0027s unique ID.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Tasks_Upid_LogGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/tasks/{upid}/log GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Tasks_Upid_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/tasks/{upid}/status GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    upid: str = Field(
        description="The task\u0027s unique ID.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Tasks_Upid_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/tasks/{upid}/status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ScanGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ScanGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_NfsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan/nfs GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    server: str = Field(
        description="The server address (name or IP).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_NfsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan/nfs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_CifsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan/cifs GET
    """
    domain: str | None = Field(
        description="SMB domain (Workgroup).",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    password: str | None = Field(
        description="User password.",
    )
    server: str = Field(
        description="The server address (name or IP).",
    )
    username: str | None = Field(
        description="User name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_CifsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan/cifs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_PbsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan/pbs GET
    """
    fingerprint: str | None = Field(
        description="Certificate SHA 256 fingerprint.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    password: str = Field(
        description="User password or API token secret.",
    )
    port: int | str | None = Field(
        default=8007,
        ge=1,
        le=65535,
        description="Optional port.",
    )
    server: str = Field(
        description="The server address (name or IP).",
    )
    username: str = Field(
        description="User-name or API token-ID.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_PbsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan/pbs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_GlusterfsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan/glusterfs GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    server: str = Field(
        description="The server address (name or IP).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_GlusterfsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan/glusterfs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_IscsiGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan/iscsi GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    portal: str = Field(
        description="The iSCSI portal (IP or DNS name with optional port).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_IscsiGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan/iscsi GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_LvmGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan/lvm GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_LvmGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan/lvm GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_LvmthinGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan/lvmthin GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vg: str = Field(
        max_length=100,
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_LvmthinGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan/lvmthin GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_ZfsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/scan/zfs GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Scan_ZfsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/scan/zfs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_HardwareGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/hardware GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_HardwareGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/hardware GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Hardware_PciGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/hardware/pci GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pci_class_blacklist: str | None = Field(
        default="05;06;0b",
        description="A list of blacklisted PCI classes, which will not be returned. Following are filtered by default: Memory Controller (05), Bridge (06) and Processor (0b).",
        serialization_alias="pci-class-blacklist",
    )
    verbose: bool | int | str | None = Field(
        default=1,
        description="If disabled, does only print the PCI IDs. Otherwise, additional information like vendor and device will be returned.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Hardware_PciGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/hardware/pci GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Hardware_Pci_PciidGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/hardware/pci/{pciid} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pciid: str = Field(
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Hardware_Pci_PciidGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/hardware/pci/{pciid} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Hardware_Pci_Pciid_MdevGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/hardware/pci/{pciid}/mdev GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pciid: str = Field(
        description="The PCI ID to list the mdev types for.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Hardware_Pci_Pciid_MdevGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/hardware/pci/{pciid}/mdev GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Hardware_UsbGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/hardware/usb GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Hardware_UsbGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/hardware/usb GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_CapabilitiesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/capabilities GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_CapabilitiesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/capabilities GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Capabilities_QemuGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/capabilities/qemu GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Capabilities_QemuGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/capabilities/qemu GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Capabilities_Qemu_CpuGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/capabilities/qemu/cpu GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Capabilities_Qemu_CpuGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/capabilities/qemu/cpu GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Capabilities_Qemu_MachinesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/capabilities/qemu/machines GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Capabilities_Qemu_MachinesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/capabilities/qemu/machines GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StorageGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage GET
    """
    content: str | None = Field(
        description="Only list stores which support this content type.",
    )
    enabled: bool | int | str | None = Field(
        default=0,
        description="Only list stores which are enabled (not disabled in config).",
    )
    format: bool | int | str | None = Field(
        default=0,
        description="Include information about formats",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str | None = Field(
        description="Only list status for  specified storage",
    )
    target: ProxmoxNode | None = Field(
        description="If target is different to \u0027node\u0027, we only lists shared storages which content is accessible on this \u0027node\u0027 and the specified \u0027target\u0027 node.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StorageGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_StorageGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_StorageGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_PrunebackupsDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/prunebackups DELETE
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    prune_backups: str | None = Field(
        description="Use these retention options instead of those from the storage configuration.",
        serialization_alias="prune-backups",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    type: Literal["lxc", "qemu"] | None = Field(
        description="Either \u0027qemu\u0027 or \u0027lxc\u0027. Only consider backups for guests of this type.",
    )
    vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="Only prune backups for this VM.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_PrunebackupsDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/prunebackups DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_PrunebackupsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/prunebackups GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    prune_backups: str | None = Field(
        description="Use these retention options instead of those from the storage configuration.",
        serialization_alias="prune-backups",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    type: Literal["lxc", "qemu"] | None = Field(
        description="Either \u0027qemu\u0027 or \u0027lxc\u0027. Only consider backups for guests of this type.",
    )
    vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="Only consider backups for this guest.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_PrunebackupsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/prunebackups GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_ContentGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/content GET
    """
    content: str | None = Field(
        description="Only list content of this type.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    vmid: ProxmoxVMID | None = Field(
        ge=1,
        description="Only list images for this VM",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_ContentGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/content GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_ContentPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/content POST
    """
    filename: str = Field(
        description="The name of the file to create.",
    )
    format: Literal["qcow2", "raw", "subvol"] | None = Field(
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    size: str = Field(
        description="Size in kilobyte (1024 bytes). Optional suffixes \u0027M\u0027 (megabyte, 1024K) and \u0027G\u0027 (gigabyte, 1024M)",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    vmid: ProxmoxVMID = Field(
        ge=1,
        description="Specify owner VM",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_ContentPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/content POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Content_VolumeDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/content/{volume} DELETE
    """
    delay: int | str | None = Field(
        ge=1,
        le=30,
        description="Time to wait for the task to finish. We return \u0027null\u0027 if the task finish within that time.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str | None = Field(
        description="The storage identifier.",
    )
    volume: str = Field(
        description="Volume identifier",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Content_VolumeDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/content/{volume} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Content_VolumeGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/content/{volume} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str | None = Field(
        description="The storage identifier.",
    )
    volume: str = Field(
        description="Volume identifier",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Content_VolumeGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/content/{volume} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Content_VolumePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/content/{volume} POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str | None = Field(
        description="The storage identifier.",
    )
    target: str = Field(
        description="Target volume identifier",
    )
    target_node: ProxmoxNode | None = Field(
        description="Target node. Default is local node.",
    )
    volume: str = Field(
        description="Source volume identifier",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Content_VolumePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/content/{volume} POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Content_VolumePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/content/{volume} PUT
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    notes: str | None = Field(
        description="The new notes.",
    )
    protected: bool | int | str | None = Field(
        description="Protection status. Currently only supported for backups.",
    )
    storage: str | None = Field(
        description="The storage identifier.",
    )
    volume: str = Field(
        description="Volume identifier",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_File_Restore_ListGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/file-restore/list GET
    """
    filepath: str = Field(
        description="base64-path to the directory or file being listed, or \"/\".",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    volume: str = Field(
        description="Backup volume ID or name. Currently only PBS snapshots are supported.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_File_Restore_ListGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/file-restore/list GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_File_Restore_DownloadGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/file-restore/download GET
    """
    filepath: str = Field(
        description="base64-path to the directory or file to download.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    volume: str = Field(
        description="Backup volume ID or name. Currently only PBS snapshots are supported.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_File_Restore_DownloadGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/file-restore/download GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/status GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_RrdGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/rrd GET
    """
    cf: Literal["AVERAGE", "MAX"] | None = Field(
        description="The RRD consolidation function",
    )
    ds: str = Field(
        description="The list of datasources you want to display.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    timeframe: Literal["day", "hour", "month", "week", "year"] = Field(
        description="Specify the time frame you are interested in.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_RrdGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/rrd GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_RrddataGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/rrddata GET
    """
    cf: Literal["AVERAGE", "MAX"] | None = Field(
        description="The RRD consolidation function",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    timeframe: Literal["day", "hour", "month", "week", "year"] = Field(
        description="Specify the time frame you are interested in.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_RrddataGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/rrddata GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_UploadPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/upload POST
    """
    checksum: str | None = Field(
        description="The expected checksum of the file.",
    )
    checksum_algorithm: Literal["md5", "sha1", "sha224", "sha256", "sha384", "sha512"] | None = Field(
        description="The algorithm to calculate the checksum of the file.",
        serialization_alias="checksum-algorithm",
    )
    content: Literal["iso", "vztmpl"] = Field(
        description="Content type.",
    )
    filename: str = Field(
        max_length=255,
        description="The name of the file to create. Caution: This will be normalized!",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    tmpfilename: str | None = Field(
        description="The source file name. This parameter is usually set by the REST handler. You can only overwrite it when connecting to the trusted port on localhost.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_UploadPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/upload POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Download_UrlPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/storage/{storage}/download-url POST
    """
    checksum: str | None = Field(
        description="The expected checksum of the file.",
    )
    checksum_algorithm: Literal["md5", "sha1", "sha224", "sha256", "sha384", "sha512"] | None = Field(
        description="The algorithm to calculate the checksum of the file.",
        serialization_alias="checksum-algorithm",
    )
    content: Literal["iso", "vztmpl"] = Field(
        description="Content type.",
    )
    filename: str = Field(
        max_length=255,
        description="The name of the file to create. Caution: This will be normalized!",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage identifier.",
    )
    url: str = Field(
        description="The URL to download the file from.",
    )
    verify_certificates: bool | int | str | None = Field(
        default=1,
        description="If false, no SSL/TLS certificates will be verified.",
        serialization_alias="verify-certificates",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Storage_Storage_Download_UrlPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/storage/{storage}/download-url POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_DisksGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_DisksGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_LvmGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/lvm GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_LvmGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/lvm GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_LvmPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/lvm POST
    """
    add_storage: bool | int | str | None = Field(
        default=0,
        description="Configure storage using the Volume Group",
    )
    device: str = Field(
        description="The block device you want to create the volume group on",
    )
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_LvmPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/lvm POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Lvm_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/lvm/{name} DELETE
    """
    cleanup_config: bool | int | str | None = Field(
        default=0,
        description="Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).",
        serialization_alias="cleanup-config",
    )
    cleanup_disks: bool | int | str | None = Field(
        default=0,
        description="Also wipe disks so they can be repurposed afterwards.",
        serialization_alias="cleanup-disks",
    )
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Lvm_NameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/lvm/{name} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_LvmthinGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/lvmthin GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_LvmthinGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/lvmthin GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_LvmthinPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/lvmthin POST
    """
    add_storage: bool | int | str | None = Field(
        default=0,
        description="Configure storage using the thinpool.",
    )
    device: str = Field(
        description="The block device you want to create the thinpool on.",
    )
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_LvmthinPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/lvmthin POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Lvmthin_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/lvmthin/{name} DELETE
    """
    cleanup_config: bool | int | str | None = Field(
        default=0,
        description="Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).",
        serialization_alias="cleanup-config",
    )
    cleanup_disks: bool | int | str | None = Field(
        default=0,
        description="Also wipe disks so they can be repurposed afterwards.",
        serialization_alias="cleanup-disks",
    )
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    volume_group: str = Field(
        description="The storage identifier.",
        serialization_alias="volume-group",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Lvmthin_NameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/lvmthin/{name} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_DirectoryGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/directory GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_DirectoryGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/directory GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_DirectoryPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/directory POST
    """
    add_storage: bool | int | str | None = Field(
        default=0,
        description="Configure storage using the directory.",
    )
    device: str = Field(
        description="The block device you want to create the filesystem on.",
    )
    filesystem: Literal["ext4", "xfs"] | None = Field(
        default="ext4",
        description="The desired filesystem.",
    )
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_DirectoryPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/directory POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Directory_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/directory/{name} DELETE
    """
    cleanup_config: bool | int | str | None = Field(
        default=0,
        description="Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).",
        serialization_alias="cleanup-config",
    )
    cleanup_disks: bool | int | str | None = Field(
        default=0,
        description="Also wipe disk so it can be repurposed afterwards.",
        serialization_alias="cleanup-disks",
    )
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Directory_NameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/directory/{name} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_ZfsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/zfs GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_ZfsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/zfs GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_ZfsPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/zfs POST
    """
    add_storage: bool | int | str | None = Field(
        default=0,
        description="Configure storage using the zpool.",
    )
    ashift: int | str | None = Field(
        default=12,
        ge=9,
        le=16,
        description="Pool sector size exponent.",
    )
    compression: Literal["gzip", "lz4", "lzjb", "off", "on", "zle", "zstd"] | None = Field(
        default="on",
        description="The compression algorithm to use.",
    )
    devices: str = Field(
        description="The block devices you want to create the zpool on.",
    )
    draid_config: str | None = Field(
        serialization_alias="draid-config",
    )
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    raidlevel: Literal["draid", "draid2", "draid3", "mirror", "raid10", "raidz", "raidz2", "raidz3", "single"] = Field(
        description="The RAID level to use.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_ZfsPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/zfs POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Zfs_NameDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/zfs/{name} DELETE
    """
    cleanup_config: bool | int | str | None = Field(
        default=0,
        description="Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).",
        serialization_alias="cleanup-config",
    )
    cleanup_disks: bool | int | str | None = Field(
        default=0,
        description="Also wipe disks so they can be repurposed afterwards.",
        serialization_alias="cleanup-disks",
    )
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Zfs_NameDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/zfs/{name} DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Zfs_NameGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/zfs/{name} GET
    """
    name: str = Field(
        description="The storage identifier.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_Zfs_NameGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/zfs/{name} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_ListGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/list GET
    """
    include_partitions: bool | int | str | None = Field(
        default=0,
        description="Also include partitions.",
        serialization_alias="include-partitions",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    skipsmart: bool | int | str | None = Field(
        default=0,
        description="Skip smart checks.",
    )
    type: Literal["journal_disks", "unused"] | None = Field(
        description="Only list specific types of disks.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_ListGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/list GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_SmartGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/smart GET
    """
    disk: str = Field(
        description="Block device name",
    )
    healthonly: bool | int | str | None = Field(
        description="If true returns only the health status",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_SmartGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/smart GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_InitgptPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/initgpt POST
    """
    disk: str = Field(
        description="Block device name",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    uuid: str | None = Field(
        max_length=36,
        description="UUID for the GPT table",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_InitgptPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/initgpt POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_WipediskPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/disks/wipedisk PUT
    """
    disk: str = Field(
        description="Block device name",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Disks_WipediskPUTResponse(BaseModel):
    """
    Response model for /nodes/{node}/disks/wipedisk PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_AptGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/apt GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_AptGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/apt GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_UpdateGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/apt/update GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_UpdateGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/apt/update GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_UpdatePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/apt/update POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    notify: bool | int | str | None = Field(
        default=0,
        description="Send notification mail about new packages (to email address specified for user \u0027root@pam\u0027).",
    )
    quiet: bool | int | str | None = Field(
        default=0,
        description="Only produces output suitable for logging, omitting progress indicators.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_UpdatePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/apt/update POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_ChangelogGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/apt/changelog GET
    """
    name: str = Field(
        description="Package name.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    version: str | None = Field(
        description="Package version.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_ChangelogGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/apt/changelog GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_RepositoriesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/apt/repositories GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_RepositoriesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/apt/repositories GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_RepositoriesPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/apt/repositories POST
    """
    digest: str | None = Field(
        max_length=80,
        description="Digest to detect modifications.",
    )
    enabled: bool | int | str | None = Field(
        description="Whether the repository should be enabled or not.",
    )
    index: int | str = Field(
        description="Index within the file (starting from 0).",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    path: str = Field(
        description="Path to the containing file.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_RepositoriesPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/apt/repositories PUT
    """
    digest: str | None = Field(
        max_length=80,
        description="Digest to detect modifications.",
    )
    handle: str = Field(
        description="Handle that identifies a repository.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_VersionsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/apt/versions GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Apt_VersionsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/apt/versions GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_FirewallGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_FirewallGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/firewall GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_RulesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall/rules GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_RulesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/firewall/rules GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_RulesPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall/rules POST
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
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

class Nodes_Node_Firewall_Rules_PosDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall/rules/{pos} DELETE
    """
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_Rules_PosGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall/rules/{pos} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    pos: int | str | None = Field(
        ge=0,
        description="Update rule at position \u003cpos\u003e.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_Rules_PosGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/firewall/rules/{pos} GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_Rules_PosPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall/rules/{pos} PUT
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
    node: ProxmoxNode = Field(
        description="The cluster node name.",
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

class Nodes_Node_Firewall_OptionsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall/options GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_OptionsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/firewall/options GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_OptionsPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall/options PUT
    """
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    enable: bool | int | str | None = Field(
        description="Enable host firewall rules.",
    )
    log_level_in: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for incoming traffic.",
    )
    log_level_out: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for outgoing traffic.",
    )
    log_nf_conntrack: bool | int | str | None = Field(
        default=0,
        description="Enable logging of conntrack information.",
    )
    ndp: bool | int | str | None = Field(
        default=0,
        description="Enable NDP (Neighbor Discovery Protocol).",
    )
    nf_conntrack_allow_invalid: bool | int | str | None = Field(
        default=0,
        description="Allow invalid packets on connection tracking.",
    )
    nf_conntrack_helpers: str | None = Field(
        default="",
        description="Enable conntrack helpers for specific protocols. Supported protocols: amanda, ftp, irc, netbios-ns, pptp, sane, sip, snmp, tftp",
    )
    nf_conntrack_max: int | str | None = Field(
        default=262144,
        ge=32768,
        description="Maximum number of tracked connections.",
    )
    nf_conntrack_tcp_timeout_established: int | str | None = Field(
        default=432000,
        ge=7875,
        description="Conntrack established timeout.",
    )
    nf_conntrack_tcp_timeout_syn_recv: int | str | None = Field(
        default=60,
        ge=30,
        le=60,
        description="Conntrack syn recv timeout.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    nosmurfs: bool | int | str | None = Field(
        description="Enable SMURFS filter.",
    )
    protection_synflood: bool | int | str | None = Field(
        default=0,
        description="Enable synflood protection",
    )
    protection_synflood_burst: int | str | None = Field(
        default=1000,
        description="Synflood protection rate burst by ip src.",
    )
    protection_synflood_rate: int | str | None = Field(
        default=200,
        description="Synflood protection rate syn/sec by ip src.",
    )
    smurf_log_level: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for SMURFS filter.",
    )
    tcp_flags_log_level: Literal["alert", "crit", "debug", "emerg", "err", "info", "nolog", "notice", "warning"] | None = Field(
        description="Log level for illegal tcp flags filter.",
    )
    tcpflags: bool | int | str | None = Field(
        default=0,
        description="Filter illegal combinations of TCP flags.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_LogGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/firewall/log GET
    """
    limit: int | str | None = Field(
        ge=0,
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    since: int | str | None = Field(
        ge=0,
        description="Display log since this UNIX epoch.",
    )
    start: int | str | None = Field(
        ge=0,
    )
    until: int | str | None = Field(
        ge=0,
        description="Display log until this UNIX epoch.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Firewall_LogGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/firewall/log GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ReplicationGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/replication GET
    """
    guest: ProxmoxVMID | None = Field(
        ge=1,
        description="Only list replication jobs for this guest.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ReplicationGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/replication GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Replication_IdGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/replication/{id} GET
    """
    id: str = Field(
        description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. \u0027\u003cGUEST\u003e-\u003cJOBNUM\u003e\u0027.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Replication_IdGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/replication/{id} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Replication_Id_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/replication/{id}/status GET
    """
    id: str = Field(
        description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. \u0027\u003cGUEST\u003e-\u003cJOBNUM\u003e\u0027.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Replication_Id_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/replication/{id}/status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Replication_Id_LogGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/replication/{id}/log GET
    """
    id: str = Field(
        description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. \u0027\u003cGUEST\u003e-\u003cJOBNUM\u003e\u0027.",
    )
    limit: int | str | None = Field(
        ge=0,
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    start: int | str | None = Field(
        ge=0,
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Replication_Id_LogGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/replication/{id}/log GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Replication_Id_Schedule_NowPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/replication/{id}/schedule_now POST
    """
    id: str = Field(
        description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. \u0027\u003cGUEST\u003e-\u003cJOBNUM\u003e\u0027.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Replication_Id_Schedule_NowPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/replication/{id}/schedule_now POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_CertificatesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/certificates GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_CertificatesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/certificates GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_AcmeGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/certificates/acme GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_AcmeGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/certificates/acme GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_Acme_CertificateDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/certificates/acme/certificate DELETE
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_Acme_CertificateDELETEResponse(BaseModel):
    """
    Response model for /nodes/{node}/certificates/acme/certificate DELETE
    """
    data: str = Field(
        description="Response data for DELETE",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_Acme_CertificatePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/certificates/acme/certificate POST
    """
    force: bool | int | str | None = Field(
        default=0,
        description="Overwrite existing custom certificate.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_Acme_CertificatePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/certificates/acme/certificate POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_Acme_CertificatePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/certificates/acme/certificate PUT
    """
    force: bool | int | str | None = Field(
        default=0,
        description="Force renewal even if expiry is more than 30 days away.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_Acme_CertificatePUTResponse(BaseModel):
    """
    Response model for /nodes/{node}/certificates/acme/certificate PUT
    """
    data: str = Field(
        description="Response data for PUT",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_InfoGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/certificates/info GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_InfoGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/certificates/info GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_CustomDELETERequest(BaseModel):
    """
    Request model for /nodes/{node}/certificates/custom DELETE
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    restart: bool | int | str | None = Field(
        default=0,
        description="Restart pveproxy.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_CustomPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/certificates/custom POST
    """
    certificates: str = Field(
        description="PEM encoded certificate (chain).",
    )
    force: bool | int | str | None = Field(
        default=0,
        description="Overwrite existing custom or ACME certificate files.",
    )
    key: str | None = Field(
        description="PEM encoded private key.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    restart: bool | int | str | None = Field(
        default=0,
        description="Restart pveproxy.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Certificates_CustomPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/certificates/custom POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ConfigGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/config GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    property: Literal["acme", "acmedomain0", "acmedomain1", "acmedomain2", "acmedomain3", "acmedomain4", "acmedomain5", "all", "description", "startall-onboot-delay", "wakeonlan"] | None = Field(
        default="all",
        description="Return only a specific property from the node configuration.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ConfigGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/config GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ConfigPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/config PUT
    """
    acme: str | None = Field(
        description="Node specific ACME settings.",
    )
    acmedomain_n_: str | None = Field(
        description="ACME domain and validation plugin",
        serialization_alias="acmedomain[n]",
    )
    delete: str | None = Field(
        description="A list of settings you want to delete.",
    )
    description: str | None = Field(
        max_length=65536,
        description="Description for the Node. Shown in the web-interface node notes panel. This is saved as comment inside the configuration file.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    startall_onboot_delay: int | str | None = Field(
        default=0,
        ge=0,
        le=300,
        description="Initial delay in seconds, before starting all the Virtual Guests with on-boot enabled.",
        serialization_alias="startall-onboot-delay",
    )
    wakeonlan: str | None = Field(
        description="MAC address for wake on LAN",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SdnGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/sdn GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SdnGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/sdn GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Sdn_ZonesGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/sdn/zones GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Sdn_ZonesGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/sdn/zones GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Sdn_Zones_ZoneGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/sdn/zones/{zone} GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    zone: str = Field(
        description="The SDN zone object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Sdn_Zones_ZoneGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/sdn/zones/{zone} GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Sdn_Zones_Zone_ContentGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/sdn/zones/{zone}/content GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    zone: str = Field(
        description="The SDN zone object identifier.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Sdn_Zones_Zone_ContentGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/sdn/zones/{zone}/content GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_VersionGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/version GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_VersionGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/version GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StatusGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/status GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StatusGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/status GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StatusPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/status POST
    """
    command: Literal["reboot", "shutdown"] = Field(
        description="Specify the command.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_NetstatGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/netstat GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_NetstatGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/netstat GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ExecutePOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/execute POST
    """
    commands: str = Field(
        description="JSON encoded array of commands.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ExecutePOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/execute POST
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_WakeonlanPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/wakeonlan POST
    """
    node: ProxmoxNode = Field(
        description="target node for wake on LAN packet",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_WakeonlanPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/wakeonlan POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_RrdGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/rrd GET
    """
    cf: Literal["AVERAGE", "MAX"] | None = Field(
        description="The RRD consolidation function",
    )
    ds: str = Field(
        description="The list of datasources you want to display.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeframe: Literal["day", "hour", "month", "week", "year"] = Field(
        description="Specify the time frame you are interested in.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_RrdGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/rrd GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_RrddataGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/rrddata GET
    """
    cf: Literal["AVERAGE", "MAX"] | None = Field(
        description="The RRD consolidation function",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeframe: Literal["day", "hour", "month", "week", "year"] = Field(
        description="Specify the time frame you are interested in.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_RrddataGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/rrddata GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SyslogGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/syslog GET
    """
    limit: int | str | None = Field(
        ge=0,
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    service: str | None = Field(
        max_length=128,
        description="Service ID",
    )
    since: str | None = Field(
        description="Display all log since this date-time string.",
    )
    start: int | str | None = Field(
        ge=0,
    )
    until: str | None = Field(
        description="Display all log until this date-time string.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SyslogGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/syslog GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_JournalGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/journal GET
    """
    endcursor: str | None = Field(
        description="End before the given Cursor. Conflicts with \u0027until\u0027",
    )
    lastentries: int | str | None = Field(
        ge=0,
        description="Limit to the last X lines. Conflicts with a range.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    since: int | str | None = Field(
        ge=0,
        description="Display all log since this UNIX epoch. Conflicts with \u0027startcursor\u0027.",
    )
    startcursor: str | None = Field(
        description="Start after the given Cursor. Conflicts with \u0027since\u0027",
    )
    until: int | str | None = Field(
        ge=0,
        description="Display all log until this UNIX epoch. Conflicts with \u0027endcursor\u0027.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_JournalGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/journal GET
    """
    data: list[str] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_VncshellPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/vncshell POST
    """
    cmd: Literal["ceph_install", "login", "upgrade"] | None = Field(
        default="login",
        description="Run specific command or default to login.",
    )
    cmd_opts: str | None = Field(
        default="",
        description="Add parameters to a command. Encoded as null terminated strings.",
        serialization_alias="cmd-opts",
    )
    height: int | str | None = Field(
        ge=16,
        le=2160,
        description="sets the height of the console in pixels.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    websocket: bool | int | str | None = Field(
        description="use websocket instead of standard vnc.",
    )
    width: int | str | None = Field(
        ge=16,
        le=4096,
        description="sets the width of the console in pixels.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_VncshellPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/vncshell POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_TermproxyPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/termproxy POST
    """
    cmd: Literal["ceph_install", "login", "upgrade"] | None = Field(
        default="login",
        description="Run specific command or default to login.",
    )
    cmd_opts: str | None = Field(
        default="",
        description="Add parameters to a command. Encoded as null terminated strings.",
        serialization_alias="cmd-opts",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_TermproxyPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/termproxy POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_VncwebsocketGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/vncwebsocket GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    port: int | str = Field(
        ge=5900,
        le=5999,
        description="Port number returned by previous vncproxy call.",
    )
    vncticket: str = Field(
        max_length=512,
        description="Ticket from previous call to vncproxy.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_VncwebsocketGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/vncwebsocket GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SpiceshellPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/spiceshell POST
    """
    cmd: Literal["ceph_install", "login", "upgrade"] | None = Field(
        default="login",
        description="Run specific command or default to login.",
    )
    cmd_opts: str | None = Field(
        default="",
        description="Add parameters to a command. Encoded as null terminated strings.",
        serialization_alias="cmd-opts",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    proxy: str | None = Field(
        description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs \u0027spiceproxy\u0027, so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_SpiceshellPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/spiceshell POST
    """
    data: dict[str, Any] = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_DnsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/dns GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_DnsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/dns GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_DnsPUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/dns PUT
    """
    dns1: str | None = Field(
        description="First name server IP address.",
    )
    dns2: str | None = Field(
        description="Second name server IP address.",
    )
    dns3: str | None = Field(
        description="Third name server IP address.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    search: str = Field(
        description="Search domain for host-name lookup.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_TimeGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/time GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_TimeGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/time GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_TimePUTRequest(BaseModel):
    """
    Request model for /nodes/{node}/time PUT
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timezone: str = Field(
        description="Time zone. The file \u0027/usr/share/zoneinfo/zone.tab\u0027 contains the list of valid names.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_AplinfoGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/aplinfo GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_AplinfoGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/aplinfo GET
    """
    data: list[dict[str, Any]] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_AplinfoPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/aplinfo POST
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    storage: str = Field(
        description="The storage where the template will be stored",
    )
    template: str = Field(
        max_length=255,
        description="The template which will downloaded",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_AplinfoPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/aplinfo POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Query_Url_MetadataGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/query-url-metadata GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    url: str = Field(
        description="The URL to query the metadata from.",
    )
    verify_certificates: bool | int | str | None = Field(
        default=1,
        description="If false, no SSL/TLS certificates will be verified.",
        serialization_alias="verify-certificates",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_Query_Url_MetadataGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/query-url-metadata GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ReportGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/report GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_ReportGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/report GET
    """
    data: str = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StartallPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/startall POST
    """
    force: bool | int | str | None = Field(
        default="off",
        description="Issue start command even if virtual guest have \u0027onboot\u0027 not set or set to off.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    vms: list[ProxmoxVMID] | None = Field(
        description="Only consider guests from this comma separated list of VMIDs.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StartallPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/startall POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StopallPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/stopall POST
    """
    force_stop: bool | int | str | None = Field(
        default=1,
        description="Force a hard-stop after the timeout.",
        serialization_alias="force-stop",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    timeout: int | str | None = Field(
        default=180,
        ge=0,
        le=7200,
        description="Timeout for each guest shutdown task. Depending on `force-stop`, the shutdown gets then simply aborted or a hard-stop is forced.",
    )
    vms: list[ProxmoxVMID] | None = Field(
        description="Only consider Guests with these IDs.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_StopallPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/stopall POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_MigrateallPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/migrateall POST
    """
    maxworkers: int | str | None = Field(
        ge=1,
        description="Maximal number of parallel migration job. If not set, uses\u0027max_workers\u0027 from datacenter.cfg. One of both must be set!",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )
    target: ProxmoxNode = Field(
        description="Target node.",
    )
    vms: list[ProxmoxVMID] | None = Field(
        description="Only consider Guests with these IDs.",
    )
    with_local_disks: bool | int | str | None = Field(
        description="Enable live storage migration for local disk",
        serialization_alias="with-local-disks",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_MigrateallPOSTResponse(BaseModel):
    """
    Response model for /nodes/{node}/migrateall POST
    """
    data: str = Field(
        description="Response data for POST",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_HostsGETRequest(BaseModel):
    """
    Request model for /nodes/{node}/hosts GET
    """
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_HostsGETResponse(BaseModel):
    """
    Response model for /nodes/{node}/hosts GET
    """
    data: dict[str, Any] = Field(
        description="Response data for GET",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

class Nodes_Node_HostsPOSTRequest(BaseModel):
    """
    Request model for /nodes/{node}/hosts POST
    """
    data: str = Field(
        description="The target content of /etc/hosts.",
    )
    digest: str | None = Field(
        max_length=40,
        description="Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.",
    )
    node: ProxmoxNode = Field(
        description="The cluster node name.",
    )

    model_config = ConfigDict(extra="forbid", validate_assignment=True, populate_by_name=True)

