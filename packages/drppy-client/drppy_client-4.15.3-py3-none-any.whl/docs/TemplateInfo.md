# TemplateInfo

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contents** | **str** | Contents that should be used when this template needs to be expanded.  Either this or ID should be set. | [optional] 
**end_delimiter** | **str** | EndDelimiter is an optional end delimiter. | [optional] 
**id** | **str** | ID of the template that should be expanded.  Either this or Contents should be set | [optional] 
**link** | **str** | Link optionally references another file to put at the path location. | [optional] 
**meta** | **dict(str, str)** | Meta for the TemplateInfo.  This can be used by the job running system and the bootenvs to handle OS, arch, and firmware differences. | [optional] 
**name** | **str** | Name of the template | 
**path** | **str** | A text/template that specifies how to create the final path the template should be written to. | 
**start_delimiter** | **str** | StartDelimiter is an optional start delimiter. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


