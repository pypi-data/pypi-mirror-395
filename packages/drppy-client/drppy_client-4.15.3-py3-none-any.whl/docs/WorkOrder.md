# WorkOrder

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived** | **bool** | Archived indicates whether the complete log for the async action can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. | 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**blueprint** | **str** | Blueprint defines the tasks and base parameters for this action | 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**context** | **str** | Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. | [optional] 
**create_time** | **datetime** | CreateTime is the time the work order was created.  This is distinct from StartTime, as there may be a significant delay before the workorder starts running. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**current_job** | **str** | The UUID of the job that is currently running. | [optional] 
**current_task** | **int** | The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. | 
**end_time** | **datetime** | EndTime The time the async action failed or finished or cancelled. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**filter** | **str** | Filter is a list filter for this WorkOrder | [optional] 
**job_exit_state** | **str** | The final disposition of the current job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
**job_result_errors** | **list[str]** | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
**job_state** | **str** | The state the current job is in.  Must be one of \&quot;created\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**machine** | **str** | Machine is the key of the machine running the WorkOrder | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**params** | **dict(str, object)** | Params that have been directly set on the Machine. | [optional] 
**profiles** | **list[str]** | Profiles An array of profiles to apply to this machine in order when looking for a parameter during rendering. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**retry_task_attempt** | **int** | This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. | [optional] 
**runnable** | **bool** | Runnable indicates that this is Runnable. | [optional] 
**stage** | **str** | The stage that this is currently in. | [optional] 
**start_time** | **datetime** | StartTime The time the async action started running. | [optional] 
**state** | **str** | State The state the async action is in.  Must be one of \&quot;created\&quot;, \&quot;running\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;cancelled\&quot; | 
**status** | **str** | Status is a short text snippet for humans explaining the current state. | [optional] 
**task_error_stacks** | [**list[TaskStack]**](TaskStack.md) | This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. | [optional] 
**tasks** | **list[str]** | The current tasks that are being processed. | [optional] 
**uuid** | **str** | Uuid is the key of this particular WorkOrder. | 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


