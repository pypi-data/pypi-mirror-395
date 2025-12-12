# Filter

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregate** | **bool** | Aggregate indicates if parameters should be aggregate for search and return | [optional] 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**decode** | **bool** | Decode indicates if the parameters should be decoded before returning the object | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**exclude_self** | **bool** | ExcludeSelf removes self runners from the list (machines/clusters/resource_brokers) | [optional] 
**group_by** | **list[str]** | GroupBy is a list of Fields or Parameters to generate groups of objects in a return list. | [optional] 
**id** | **str** | Id is the Name of the Filter | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**object** | **str** | Object is the name of the set of objects this filter applies to. | [optional] 
**param_set** | **str** | ParamSet defines a comma-separated list of Fields or Parameters to return (can be complex functions) | [optional] 
**params** | **dict(str, object)** | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
**queries** | [**list[Query]**](Query.md) | Queries are the tests to apply to the machine. | [optional] 
**range_only** | **bool** | RangeOnly indicates that counts should be returned of group-bys and no objects. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**reduced** | **bool** | Reduced indicates if the objects should have ReadOnly fields removed | [optional] 
**reverse** | **bool** | Reverse the returned list | [optional] 
**slim** | **str** | Slim defines if meta, params, or specific parameters should be excluded from the object | [optional] 
**sort** | **list[str]** | Sort is a list of fields / parameters that should scope the list | [optional] 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


