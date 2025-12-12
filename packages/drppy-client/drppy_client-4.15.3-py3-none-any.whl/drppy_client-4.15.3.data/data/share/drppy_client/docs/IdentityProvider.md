# IdentityProvider

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**default_role** | **str** | DefaultRole - defines the default role to give these users | [optional] 
**deny_if_no_groups** | **bool** | DenyIfNoGroups - defines if the auth should fail if no groups are found in the GroupAttribute | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**display_name** | **str** | DisplayName - The name to display to user | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**group_attribute** | **str** | GroupAttribute - specifies the attribute in the Assertions to use as group memberships | [optional] 
**group_to_roles** | **dict(str, list[str])** | GroupToRoles - defines the group names that map to DRP Roles | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**logo_path** | **str** | LogoPath - The path on DRP or the URL to the logo icon | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**meta_data_blob** | **str** | MetaDataBlob - String form of the metadata - instead of MetaDataUrl | [optional] 
**meta_data_url** | **str** | MetaDataUrl - URL to get the metadata for this IdP - instead of MetaDataBlob | [optional] 
**name** | **str** | Name is the name of this identity provider | 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**user_attribute** | **str** | UserAttribute - specifies the attribute in the Assertions to use as username | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


