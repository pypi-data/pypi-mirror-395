# Job

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | [**Action**](Action.md) |  | [optional] 
**archived** | **bool** | Archived indicates whether the complete log for the job can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. | 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**boot_env** | **str** | The bootenv that the task was created in. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**context** | **str** | Context is the context the job was created to run in. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**current** | **bool** | Whether the job is the \&quot;current one\&quot; for the machine or if it has been superceded. | 
**current_index** | **int** | The current index is the machine CurrentTask that created this job. | 
**end_time** | **datetime** | The time the job failed or finished. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**exit_state** | **str** | The final disposition of the job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
**extra_claims** | [**list[Claim]**](Claim.md) | ExtraClaims is the expanded list of extra Claims that were added to the default machine Claims via the ExtraRoles field on the Task that the Job was created to run. | [optional] 
**independent** | **bool** | Independent indicates that this Job was created to track something besides a task being executed by an agent.  Most of the task state sanity checking performed by the job lifecycle checking will be skipped -- in particular, the job need not be associated with a Workorder or a Machine, it will be permitted to have multiple simultaneous Jobs in flight for the same Target, and State will be ignored for job cleanup purposes. | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**machine** | **str** | The machine the job was created for.  This field must be the UUID of the machine. It must be set if Independent is false. | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**next_index** | **int** | The next task index that should be run when this job finishes.  It is used in conjunction with the machine CurrentTask to implement the server side of the machine agent state machine. | 
**previous** | **str** | The UUID of the previous job to run on this machine. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**result_errors** | **list[str]** | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
**stage** | **str** | The stage that the task was created in. | [optional] 
**start_time** | **datetime** | The time the job started running. | [optional] 
**state** | **str** | The state the job is in.  Must be one of \&quot;created\&quot;, \&quot;running\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | 
**target_key** | **str** | TargetKey is the Key of the Object that an Independent job was invoked against. It may be empty if TargetPrefix is \&quot;system\&quot;. | [optional] 
**target_prefix** | **str** | TargetPrefix is the Prefix of the Object that an Independent job was invoked against. It must be set if Independent is true. | [optional] 
**task** | **str** | The task the job was created for.  This will be the name of the task. | [optional] 
**token** | **str** | Token is the JWT token that should be used when running this Job.  If not present or empty, the Agent running the Job will use its ambient Token instead.  If set, the Token will only be valid for the current Job. | [optional] 
**uuid** | **str** | The UUID of the job.  The primary key. | 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 
**work_order** | **str** | The work order the job was created for.  This field must be the UUID of the work order. It must be set if Independent is false and the job is being run on behalf of a WorkOrder. | [optional] 
**workflow** | **str** | The workflow that the task was created in. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


