# Context

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**engine** | **str** | Engine is the name of the Plugin that provides the functionality needed to manage the execution environment that Tasks run in on behalf of a given Machine in the Context.  An Engine could be a Plugin that interfaces with Docker or Podman locally, Kubernetes, Rancher, vSphere, AWS, or any number of other things. | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**image** | **str** | Image is the name of the prebuilt execution environment that the Engine should use to create specific execution environments for this Context when Tasks should run on behalf of a Machine.  Images must contain all the tools needed to run the Tasks that are designed to run in them, as well as a version of drpcli with a context-aware &#x60;machines processjobs&#x60; command. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**name** | **str** | Name is the name of this Context.  It must be unique. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


