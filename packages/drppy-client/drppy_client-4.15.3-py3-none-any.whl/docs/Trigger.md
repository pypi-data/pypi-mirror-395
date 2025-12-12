# Trigger

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**all_in_filter** | **bool** | AllInFilter if true cause a work_order created for all machines in the filter | [optional] 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**blueprint** | **str** | Blueprint is template to apply | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**enabled** | **bool** | Enabled is this Trigger enabled | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**filter** | **str** | Filter is a \&quot;list\&quot;-style filter string to find machines to apply the cron too Filter is already assumed to have WorkOrderMode &#x3D;&#x3D; true &amp;&amp; Runnable &#x3D;&#x3D; true | [optional] 
**filter_count** | **int** | FilterCount defines the number of machines to apply the work_order to.  Only one work_order per trigger fire. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**merge_data_into_params** | **bool** | MergeDataIntoParams if true causes the data from the trigger to be merged into the Params of the work_order. | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**name** | **str** | Name is the key of this particular Trigger. | 
**params** | **dict(str, object)** | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
**profiles** | **list[str]** | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
**queue_mode** | **bool** | QueueMode if true causes work_orders to be created without a machine, but with a filter for delayed operation | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**store_data_in_parameter** | **str** | StoreDataInParameter if set tells the triggers data to be stored in the parameter in the Params of the work_order. | [optional] 
**trigger_provider** | **str** | TriggerProvider is the name of the method of this trigger | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 
**work_order_params** | **dict(str, object)** | WorkOrderParams that have been directly set on the Trigger and will be moved to the work order. | [optional] 
**work_order_profiles** | **list[str]** | WorkOrderProfiles to apply to this machine in order when looking for a parameter during rendering. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


