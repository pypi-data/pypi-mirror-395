# Lease

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**addr** | **str** | Addr is the IP address that the lease handed out. | 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**duration** | **int** | Duration is the time in seconds for which a lease can be valid. ExpireTime is calculated from Duration. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**expire_time** | **datetime** | ExpireTime is the time at which the lease expires and is no longer valid The DHCP renewal time will be half this, and the DHCP rebind time will be three quarters of this. | 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**machine_uuid** | **str** | MachineUuid is set when the lease is created on a machine object only. | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**next_server** | **str** | NextServer is the IP address that we should have the machine talk to next.  In most cases, this will be our address. | [optional] 
**options** | [**list[DhcpOption]**](DhcpOption.md) | Options are the DHCP options that the Lease is running with. | [optional] 
**provided_options** | [**list[DhcpOption]**](DhcpOption.md) | ProvidedOptions are the DHCP options the last Discover or Offer packet for this lease provided to us. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**skip_boot** | **bool** | SkipBoot indicates that the DHCP system is allowed to offer boot options for whatever boot protocol the machine wants to use. | [optional] 
**state** | **str** | State is the current state of the lease.  This field is for informational purposes only. | 
**strategy** | **str** | Strategy is the leasing strategy that will be used determine what to use from the DHCP packet to handle lease management. | 
**token** | **str** | Token is the unique token for this lease based on the Strategy this lease used. | 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 
**via** | **str** | Via is the IP address used to select which subnet the lease belongs to. It is either an address present on a local interface that dr-provision is listening on, or the GIADDR field of the DHCP request. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


