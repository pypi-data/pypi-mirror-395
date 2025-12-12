# Activity

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**arch** | **str** | Arch is the architecture of the machine e.g. amd64 | [optional] 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**cloud** | **str** | Cloud is the cloud it is running in if set. | [optional] 
**context** | **str** | Context is the context of the machine e.g. \&quot;\&quot; or drpcli-runner | [optional] 
**count** | **int** | Number of times for this entry | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**deleted** | **bool** | Deleted indicates if the entry was deleted. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**fingerprint** | **str** | Fingerprint indicates a unique machine specific identifier | [optional] 
**id** | **str** | Id of the activity entry. | [optional] 
**identity** | **str** | Identity is the uuid/identity of the record | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**os** | **str** | OS is the operating system of the machine - could be off | [optional] 
**object_type** | **str** | Object Type | [optional] 
**platform** | **str** | Platform is type of entry Usually: meta, physical, virtual, container | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**span** | **str** | Span is the time window | [optional] 
**type** | **str** | Type of the activity (from RawModel days) Should be set to activities if present | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


