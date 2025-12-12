# Batch

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**end_time** | **datetime** | EndTime is the time the batch failed or finished. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**post_work_order** | **str** | SetupWorkOrder is the scheduling work order that was created at create time. | [optional] 
**post_work_order_template** | [**WorkOrder**](WorkOrder.md) |  | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**setup_work_order** | **str** | SetupWorkOrder is the scheduling work order that was created at create time. | [optional] 
**setup_work_order_template** | [**WorkOrder**](WorkOrder.md) |  | 
**start_time** | **datetime** | StartTime is the time the batch started running. | [optional] 
**state** | **str** | State the batch is in.  Must be one of \&quot;created\&quot;, \&quot;setup\&quot;, \&quot;running\&quot;, \&quot;post\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;cancelled\&quot; | 
**status** | **str** | Status is the reason for things | [optional] 
**uuid** | **str** | UUID of the batch.  The primary key. | 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 
**work_order_counts** | **dict(str, int)** | WorkOrderCounts addresses the state of the workorders - this is calculated | [optional] 
**work_order_template** | [**WorkOrder**](WorkOrder.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


