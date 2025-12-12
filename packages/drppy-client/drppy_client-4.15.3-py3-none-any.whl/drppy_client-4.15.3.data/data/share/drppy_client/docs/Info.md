# Info

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cluster_state** | [**ClusterState**](ClusterState.md) |  | [optional] 
**license** | [**LicenseBundle**](LicenseBundle.md) |  | [optional] 
**address** | **str** |  | 
**api_port** | **int** | ApiPort is the TCP port that the API lives on.  Defaults to 8092 | 
**arch** | **str** | Arch is the system architecture of the running dr-provision endpoint. It is the same value that would be return by runtime.GOARCH | 
**binl_enabled** | **bool** | BinlEnabled is true if the BINL server is enabled. | 
**binl_port** | **int** |  | 
**dhcp_enabled** | **bool** | DhcpEnabled is true if the DHCP server is enabled. | 
**dhcp_port** | **int** | DhcpPort is the UDP port that the DHCPv4 server listens on. Defaults to 67 | 
**dns_enabled** | **bool** | Address is the IP address that the system appears to listen on. If a default address was assigned via environment variable or command line, it will be that address, otherwise it will be the IP address of the interface that has the default IPv4 route. | 
**dns_port** | **int** | BinlPort is the UDP port that the BINL server listens on. Defaults to 4011 | 
**errors** | **list[str]** | Errors returns the current system errors. | 
**extra_api_ports** | **list[int]** | ExtraApiPorts is any additional ports that the API is also acessible on.  If no extra ports are specified, this field will be omitted. | [optional] 
**extra_file_ports** | **list[int]** | ExtraFilePorts is any additional ports that static file HTTP server is also acessible on.  If no extra ports are specified, this field will be omitted. | [optional] 
**extra_secure_file_ports** | **list[int]** | ExtraSecureFilePorts is any additional ports that the static file HTTPS server is also acessible on.  If no extra ports are specified, this field will be omitted. | [optional] 
**features** | **list[str]** | Features is a list of features implemented in this dr-provision endpoint. Clients should use this field when determining what features are available on anu given dr-provision instance. | [optional] 
**file_port** | **int** | FilePort is the TCP port that the static file HTTP server lives on. Defaults to 8091 | 
**ha_active_id** | **str** | HaActiveId is the id of current active node | [optional] 
**ha_consensus_id** | **str** | ConsensusId is the system assigned high-availability ID for this endpoint. | 
**ha_enabled** | **bool** | HaEnabled indicates if High Availability is enabled | [optional] 
**ha_id** | **str** | HaId is the user-assigned high-availability ID for this endpoint. All endpoints in the same HA cluster must have the same HaId. | 
**ha_is_active** | **bool** | HaIsActive indicates Active (true) or Passive (false) | 
**ha_passive_state** | [**list[HaPassiveState]**](HaPassiveState.md) | HaPassiveState is a list of passive node&#39;s and their current state This is only valid from the Active node | [optional] 
**ha_status** | **str** | HaStatus indicates current state For Active, Up is the only value. For Passive, Connecting, Syncing, In-Sync | 
**ha_virtual_address** | **str** | HaVirtualAddress is the Virtual IP Address of the systems | [optional] 
**id** | **str** | Id is the local ID for this dr-provision.  If not overridden by an environment variable or a command line argument, it will be the lowest MAC address of all the physical nics attached to the system. | 
**local_id** | **str** | LocalId is the same as Id, except it is always the MAC address form. | 
**manager** | **bool** | Manager indicates whether this dr-provision can act as a manager of other dr-provision instances. | 
**os** | **str** | Os is the operating system the dr-provision endpoint is running on. It is the same value returned by runtime.GOARCH | 
**prov_enabled** | **bool** | ProvisionerEnabled is true if the static file HTTP server is enabled. | 
**scopes** | **dict(str, dict(str, object))** | Scopes lists all static permission scopes available. | [optional] 
**secure_file_port** | **int** | SecureFilePort is the TCP port that the static file HTTPS server lives on. Defaults to 8090 | 
**secure_prov_enabled** | **bool** | SecureProvisionerEnabled is true if the static file HTTPS server is enabled. | 
**server_hostname** | **str** | ServerHostname is the DNS name for the DRP endpoint that managed systems should use. If a default hostname was assigned via environment variable or command line, it will be that hostname, otherwise it will be an empty string | [optional] 
**stats** | [**list[Stat]**](Stat.md) | Stats lists some basic object statistics. | 
**tftp_enabled** | **bool** | TftpEnabled is true if the TFTP server is enabled. | 
**tftp_port** | **int** | TftpPort is the UDP port that the TFTP server listens on. Defaults to 69, dude. | 
**uuid** | **str** | Uuid is the same as uuid of the endpoint | 
**version** | **str** | Version is the full version of dr-provision. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


