# ResourceBroker

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | **str** | The IPv4 address of the machine that should be used for PXE purposes.  Note that this field does not directly tie into DHCP leases or reservations -- the provisioner relies solely on this address when determining what to render for a specific machine. Address is updated automatically by the DHCP system if HardwareAddrs is filled out. | [optional] 
**arch** | **str** | Arch is the machine architecture. It should be an arch that can be fed into $GOARCH. | 
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**boot_env** | **str** | The boot environment that the machine should boot into.  This must be the name of a boot environment present in the backend. If this field is not present or blank, the global default bootenv will be used instead. | [optional] 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**context** | **str** | Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**current_job** | **str** | The UUID of the job that is currently running. | [optional] 
**current_task** | **int** | The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. | 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**fingerprint** | [**MachineFingerprint**](MachineFingerprint.md) |  | [optional] 
**hardware_addrs** | **list[str]** | HardwareAddrs is a list of MAC addresses we expect that the system might boot from. This must be filled out to enable MAC address based booting from the various bootenvs, and must be updated if the MAC addresses for a system change for whatever reason. | [optional] 
**job_exit_state** | **str** | The final disposition of the current job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
**job_result_errors** | **list[str]** | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
**job_state** | **str** | The state the current job is in.  Must be one of \&quot;created\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | [optional] 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**locked** | **bool** | Locked indicates that changes to the Machine by users are not allowed, except for unlocking the machine, which will always generate an Audit event. | 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**name** | **str** | The name of the machine.  This must be unique across all machines, and by convention it is the FQDN of the machine, although nothing enforces that. | 
**os** | **str** | OS is the operating system that the node is running in.  It is updated by Sledgehammer and by the various OS install tasks. | [optional] 
**params** | **dict(str, object)** | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
**partial** | **bool** | Partial tracks if the object is not complete when returned. | [optional] 
**pending_work_orders** | **int** | PendingWorkOrders is the number of work orders for this Machine that are in the &#39;created&#39; state. | [optional] 
**pool** | **str** | Pool contains the pool the machine is in. Unset machines will join the default Pool | [optional] 
**pool_allocated** | **bool** | PoolAllocated defines if the machine is allocated in this pool This is a calculated field. | [optional] 
**pool_status** | [**PoolStatus**](PoolStatus.md) |  | [optional] 
**profiles** | **list[str]** | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**retry_task_attempt** | **int** | This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. | [optional] 
**runnable** | **bool** | Runnable indicates that this is Runnable. | [optional] 
**running_work_orders** | **int** | RunningWorkOrders is the number of work orders for this Machine that are in the &#39;running&#39; state. | [optional] 
**secret** | **str** | Secret for machine token revocation.  Changing the secret will invalidate all existing tokens for this machine | [optional] 
**stage** | **str** | The stage that this is currently in. | [optional] 
**task_error_stacks** | [**list[TaskStack]**](TaskStack.md) | This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. | [optional] 
**tasks** | **list[str]** | The current tasks that are being processed. | [optional] 
**uuid** | **str** | The UUID of the machine. This is auto-created at Create time, and cannot change afterwards. | 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 
**work_order_mode** | **bool** | WorkOrderMode indicates if the machine is action mode | [optional] 
**workflow** | **str** | Workflow is the workflow that is currently responsible for processing machine tasks. | 
**workflow_complete** | **bool** | WorkflowComplete indicates if the workflow is complete | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


