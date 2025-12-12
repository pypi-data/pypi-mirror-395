# ClusterState

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_uri** | **str** | ActiveUri is the API URL of cthe cluster as built from the virtual addr. | [optional] 
**consensus_enabled** | **bool** | ConsensusEnabled indicates that this cluster is operating on the Raft based replication protocol with automatic failover. | [optional] 
**consensus_join** | **str** | ConsensusJoin is the API URL of the current active node in a consensus cluster.  It may be unset if the cluster nodes cannot agree who should be the active node, or if the cluster is operating using the sync replication protocol. | [optional] 
**enabled** | **bool** | Enabled indicates whether either HA mode is operating on this cluster. If just Enabled is set, the cluster is using the synchronous replication protocol with manual failover. | [optional] 
**ha_id** | **str** | HaID is the ID of the cluster as a whole. | [optional] 
**load_balanced** | **bool** | LoadBalanced indicates that an external service is responsible for routing traffic destined to VirtAddr to a cluster node. | [optional] 
**nodes** | [**list[NodeInfo]**](NodeInfo.md) |  | [optional] 
**roots** | [**list[Cert]**](Cert.md) | Roots is a list of self-signed trust roots that consensus nodes will use to verify communication.  These roots are automatically created and rotated on a regular basis. | [optional] 
**server_hostname** | **str** | ServerHostname is the DNS name for the DRP endpoint that managed systems should use. | [optional] 
**token** | **str** | Token is an API authentication token that can be sued to perform cluster operations. | [optional] 
**valid** | **bool** | Valid indicates that this state is valid and has been consistency checked. | [optional] 
**virt_addr** | **str** | VirtAddr is the IP address that the cluster should appear to have from the perspective of clients and third parties. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


