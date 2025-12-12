# UxView

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**airgap** | **bool** | Airgap is not used.  Moved to license. Deprecated | [optional] 
**applicable_roles** | **list[str]** | ApplicableRoles defines the roles that this view shows up for. e.g. superuser means that it will be available for users with the superuser role. | [optional] 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**branding_image** | **str** | BrandingImage defines a files API path that should point to an image file. This replaces the RackN logo. | [optional] 
**bulk_tabs** | **list[str]** | BulkTabs defines the tabs for this view | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**classifiers** | [**list[Classifier]**](Classifier.md) | Classifiers is deprecated | [optional] 
**columns** | **dict(str, list[str])** | Columns defines the custom colums for a MenuItem Id | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**hide_edit_objects** | **list[str]** | HideEditObject defines a list of fields to hide when editting | [optional] 
**id** | **str** | Id is the Name of the Filter | [optional] 
**landing_page** | **str** | LandingPage defines the default navigation route None or \&quot;\&quot; will open the system page. if it starts with http, it will navigate to the Overiew page. Otherwise, it will go to the machine&#39;s page. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**machine_fields** | **list[str]** | MachineFields defines the fields for this view | [optional] 
**menu** | [**list[MenuGroup]**](MenuGroup.md) | Menu defines the menu elements. | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**params** | **dict(str, object)** | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
**params_restriction** | **list[str]** | ParmsRestriction defines a list of restrictions for the parameter list | [optional] 
**profiles_restriction** | **list[str]** | ProfilesRestriction defines a list of restrictions for the profile list | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**show_activiation** | **bool** | ShowActiviation is not used.  Moved to license. Deprecated | [optional] 
**stages_restriction** | **list[str]** | StagesRestriction defines a list of restrictions for the stage list | [optional] 
**tasks_restriction** | **list[str]** | TasksRestriction defines a list of restrictions for the task list | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 
**workflows_restriction** | **list[str]** | WorkflowRestriction defines a list of restrictions for the workflow list | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


