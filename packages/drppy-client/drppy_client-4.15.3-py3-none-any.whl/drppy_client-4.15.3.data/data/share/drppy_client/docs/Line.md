# Line

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **list[object]** | Data is any auxillary data that was captured. | [optional] 
**file** | **str** | File is the source file that generated the line | [optional] 
**group** | **int** | Group is an abstract number used to group Lines together | [optional] 
**ignore_publish** | **bool** | Should the line be published or not as an event. | [optional] 
**level** | [**Level**](Level.md) |  | [optional] 
**line** | **int** | Line is the line number of the line that generated the line. | [optional] 
**message** | **str** | Message is the message that was logged. | [optional] 
**principal** | **str** | Principal is the user or system that caused the log line to be emitted | [optional] 
**seq** | **int** | Seq is the sequence number that the Line was emitted in. Sequence numbers are globally unique. | [optional] 
**service** | **str** | Service is the name of the log. | [optional] 
**time** | **datetime** | Time is when the Line was created. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


