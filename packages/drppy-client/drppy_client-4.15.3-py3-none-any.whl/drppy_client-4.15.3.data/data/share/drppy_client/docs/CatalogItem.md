# CatalogItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**actual_version** | **str** | ActualVersion is the fully expanded version for this item. | [optional] 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**content_type** | **str** | ContentType defines the type catalog item Possible options are:  DRP DRPUX DRPCLI ContentPackage PluginProvider | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**hot_fix** | **bool** | HotFix is true if this a hotfix entry. | [optional] 
**id** | **str** | Id is the unique ID for this catalog item. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**nojq_source** | **str** | NOJQSource is a greppable string to find an entry. | [optional] 
**name** | **str** | Name is the element in the catalog | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**shasum256** | **dict(str, str)** | Shasum256 is a map of checksums. The key of the map is any/any for the UX and ContentPackage elements. Otherwise the key is the arch/os.  e.g. amd64/linux | [optional] 
**source** | **str** | Source is a URL or path to the item  If the source is a URL, the base element is pulled from there. If the source has {{.ProvisionerURL}}, it will use the DRP Endpoint If the source is a path, the system will use the catalog source as the base. | [optional] 
**tip** | **bool** | Tip is true if this is a tip entry. | [optional] 
**type** | **str** | Type is the type of catalog item this is. | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 
**version** | **str** | Version is the processed/matched version.  It is either tip, stable, or the full version. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


