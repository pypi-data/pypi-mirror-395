# Stage

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**boot_env** | **str** | The BootEnv the machine should be in to run this stage. If the machine is not in this bootenv, the bootenv of the machine will be changed. | 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**name** | **str** | The name of the stage. | 
**optional_params** | **list[str]** | The list of extra optional parameters for this stage. They can be present as Machine.Params when the stage is applied to the machine.  These are more other consumers of the stage to know what parameters could additionally be applied to the stage by the renderer based upon the Machine.Params | [optional] 
**output_params** | **list[str]** | OutputParams are that parameters that are possibly set by the Task | [optional] 
**params** | **dict(str, object)** | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
**partial** | **bool** | Partial tracks if the object is not complete when returned. | [optional] 
**profiles** | **list[str]** | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**reboot** | **bool** | Flag to indicate if a node should be PXE booted on this transition into this Stage.  The nextbootpxe and reboot machine actions will be called if present and Reboot is true | [optional] 
**required_params** | **list[str]** | The list of extra required parameters for this stage. They should be present as Machine.Params when the stage is applied to the machine. | 
**runner_wait** | **bool** | This flag is deprecated and will always be TRUE. | [optional] 
**tasks** | **list[str]** | The list of initial machine tasks that the stage should run | [optional] 
**templates** | [**list[TemplateInfo]**](TemplateInfo.md) | The templates that should be expanded into files for the stage. | 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


