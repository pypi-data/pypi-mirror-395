# Endpoint

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action_error_count** | **int** | ActionErrorCount is the number of failed actions in the action list If the whole list is tried and no progress is made the apply will stop. | [optional] 
**actions** | [**list[ElementAction]**](ElementAction.md) | Actions is the list of actions to take to make the endpoint match the version sets on in the endpoint object. | [optional] 
**apply** | **bool** | Apply toggles whether the manager should update the endpoint. | [optional] 
**arch** | **str** | Arch is the arch of the endpoint - Golang arch format. | [optional] 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**components** | [**list[Element]**](Element.md) | Components is the list of ContentPackages and PluginProviders installed and their versions | [optional] 
**connection_status** | **str** | ConnectionStatus reflects the manager&#39;s state of interaction with the endpoint | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**drpux_version** | **str** | DRPUXVersion is the version of the ux installed on the endpoint. | [optional] 
**drp_version** | **str** | DRPVersion is the version of the drp endpoint running. | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**_global** | **dict(str, object)** | Global is the Parameters of the global profile. | [optional] 
**ha_id** | **str** | HaId is the HaId of the endpoint | [optional] 
**id** | **str** | Id is the name of the DRP endpoint this should match the HA pair&#39;s ID or the DRP ID of a single node. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**os** | **str** | Os is the os of the endpoint - Golang os format. | [optional] 
**params** | **dict(str, object)** | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
**plugins** | [**list[Plugin]**](Plugin.md) | Plugins is the list of Plugins configured on the endpoint. | [optional] 
**prefs** | **dict(str, str)** | Prefs is the value of all the prefs on the endpoint. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 
**version_set** | **str** | VersionSet - Deprecated - was a single version set. This should be specified within the VersionSets list | [optional] 
**version_sets** | **list[str]** | VersionSets replaces VersionSet - code processes both This is the list of version sets to apply.  These are merged with the first in the list having priority over later elements in the list. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


