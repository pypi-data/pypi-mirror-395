# JobAction

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** | Content is the rendered version of the Template on the Task corresponding to this JobAction. | 
**meta** | **dict(str, str)** | Meta is a copt of the Meta field of the corresponding Template from the Task this Job was built from. | 
**name** | **str** | Name is the name of this particular JobAction.  It is taken from the name of the corresponding Template on the Task this Action was rendered from. | 
**path** | **str** | Path is the location that Content should be written to on disk.  If Path is absolute, it will be written in that location.  If Path is relative, it will be written relative to the temporary direcory created for running the Job in.  If Path is empty, then Content is interpreted as a script to be run. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


