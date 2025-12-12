# Operation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**_from** | **str** | From is a JSON pointer indicating where a value should be copied/moved from.  From is only used by copy and move operations. | [optional] 
**op** | **str** | Op can be one of: \&quot;add\&quot; \&quot;remove\&quot; \&quot;replace\&quot; \&quot;move\&quot; \&quot;copy\&quot; \&quot;test\&quot; All Operations must have an Op. | [optional] 
**path** | **str** | Path is a JSON Pointer as defined in RFC 6901 All Operations must have a Path | [optional] 
**value** | **object** | Value is the Value to be used for add, replace, and test operations. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


