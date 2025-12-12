# Reservation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**addr** | **str** | Addr is the IP address permanently assigned to the strategy/token combination. | 
**allocated** | **bool** | Allocated indicates this is a reapable reservation | [optional] 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**duration** | **int** | Duration is the time in seconds for which a lease can be valid. ExpireTime is calculated from Duration. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**machine** | **str** | Machine is the associated machine | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**next_server** | **str** | NextServer is the address the server should contact next. You should only set this if you want to talk to a DHCP or TFTP server other than the one provided by dr-provision. | [optional] 
**options** | [**list[DhcpOption]**](DhcpOption.md) | Options is the list of DHCP options that apply to this Reservation | [optional] 
**parameter** | **str** | Parameter is the parameter that this address should be stored in for the machine if specified | [optional] 
**params** | **dict(str, object)** | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
**prefix_parameter** | **str** | PrefixParameter a string that should be the beginning of a set of option-based parameters | [optional] 
**profiles** | **list[str]** | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**scoped** | **bool** | Scoped indicates that this reservation is tied to a particular Subnet, as determined by the reservation&#39;s Addr. | 
**skip_dad** | **bool** | SkipDAD will cause the DHCP server to skip duplicate address detection via ping testing when in discovery phase.  Only set this if you know this reservation can never conflict with any other system. | [optional] 
**strategy** | **str** | Strategy is the leasing strategy that will be used determine what to use from the DHCP packet to handle lease management. | 
**subnet** | **str** | Subnet is the name of the Subnet that this Reservation is associated with. This property is read-only. | [optional] 
**token** | **str** | Token is the unique identifier that the strategy for this Reservation should use. | 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


