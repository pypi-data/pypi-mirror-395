# VersionSet

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply** | **bool** | Apply indicates if this VersionSet should be applied to the endpoints it is attached to. | [optional] 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**components** | [**list[Element]**](Element.md) | Compnents is a list of elements that should be applied to the system. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**drpux_version** | **str** | DRPUXVersion is the version of UX to apply to the system. This can be tip, stable, or a full version. | [optional] 
**drp_version** | **str** | DRPVersion is the version of DRP to apply to the system. This can be tip, stable, or a full version. | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**files** | [**list[FileData]**](FileData.md) | Files defines files to apply to the endpoint through the files API. | [optional] 
**_global** | **dict(str, object)** | Global defines parameters for the endpoint&#39;s global profile. | [optional] 
**id** | **str** | Id is the name of the version set | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**plugins** | [**list[Plugin]**](Plugin.md) | Plugins is a list of Plugin objects that should be applied to the system. | [optional] 
**prefs** | **dict(str, str)** | Prefs is a map of preferences that should be applied to the system. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


