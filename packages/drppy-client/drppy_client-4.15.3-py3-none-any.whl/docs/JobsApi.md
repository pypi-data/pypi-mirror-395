# drppy_client.JobsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_job**](JobsApi.md#create_job) | **POST** /jobs | Create a Job
[**delete_job**](JobsApi.md#delete_job) | **DELETE** /jobs/{uuid} | Delete a Job
[**get_job**](JobsApi.md#get_job) | **GET** /jobs/{uuid} | Get a Job
[**get_job_action**](JobsApi.md#get_job_action) | **GET** /jobs/{uuid}/plugin_actions/{cmd} | List specific action for a job Job
[**get_job_actions**](JobsApi.md#get_job_actions) | **GET** /jobs/{uuid}/actions | Get actions for this job
[**get_job_log**](JobsApi.md#get_job_log) | **GET** /jobs/{uuid}/log | Get the log for this job
[**get_job_log_archive**](JobsApi.md#get_job_log_archive) | **GET** /jobs/{uuid}/archive | Get the log archive entry for this job
[**get_job_plugin_actions**](JobsApi.md#get_job_plugin_actions) | **GET** /jobs/{uuid}/plugin_actions | List job plugin_actions Job
[**head_job**](JobsApi.md#head_job) | **HEAD** /jobs/{uuid} | See if a Job exists
[**head_job_log**](JobsApi.md#head_job_log) | **HEAD** /jobs/{uuid}/log | Get the log for this job
[**list_jobs**](JobsApi.md#list_jobs) | **GET** /jobs | Lists Jobs filtered by some parameters.
[**list_stats_jobs**](JobsApi.md#list_stats_jobs) | **HEAD** /jobs | Stats of the List Jobs filtered by some parameters.
[**patch_job**](JobsApi.md#patch_job) | **PATCH** /jobs/{uuid} | Patch a Job
[**post_job_action**](JobsApi.md#post_job_action) | **POST** /jobs/{uuid}/plugin_actions/{cmd} | Call an action on the node.
[**put_job**](JobsApi.md#put_job) | **PUT** /jobs/{uuid} | Put a Job
[**put_job_log**](JobsApi.md#put_job_log) | **PUT** /jobs/{uuid}/log | Append the string to the end of the job&#39;s log.


# **create_job**
> Job create_job(body)

Create a Job

Create a Job from the provided object, Only Machine and UUID are used.

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Job() # Job | 

try:
    # Create a Job
    api_response = api_instance.create_job(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->create_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Job**](Job.md)|  | 

### Return type

[**Job**](Job.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_job**
> Job delete_job(uuid, force=force, commented=commented, reduced=reduced)

Delete a Job

Delete a Job specified by {uuid}

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Job
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a Job
    api_response = api_instance.delete_job(uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->delete_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Job | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Job**](Job.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job**
> Job get_job(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a Job

Get the Job specified by {uuid}  or return NotFound.

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Job
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a Job
    api_response = api_instance.get_job(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->get_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Job | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Job**](Job.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_action**
> AvailableAction get_job_action(uuid)

List specific action for a job Job

List specific {cmd} action for a Job specified by {uuid}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # List specific action for a job Job
    api_response = api_instance.get_job_action(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->get_job_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

[**AvailableAction**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_actions**
> get_job_actions(uuid)

Get actions for this job

Get actions for the Job specified by {uuid} or return NotFound.

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # Get actions for this job
    api_instance.get_job_actions(uuid)
except ApiException as e:
    print("Exception when calling JobsApi->get_job_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_log**
> str get_job_log(uuid)

Get the log for this job

Get log for the Job specified by {uuid} or return NotFound.

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # Get the log for this job
    api_response = api_instance.get_job_log(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->get_job_log: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

**str**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_log_archive**
> str get_job_log_archive(uuid)

Get the log archive entry for this job

Get log archive entry for the Job specified by {uuid} or return NotFound.

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # Get the log archive entry for this job
    api_response = api_instance.get_job_log_archive(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->get_job_log_archive: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

**str**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_plugin_actions**
> list[AvailableAction] get_job_plugin_actions(uuid)

List job plugin_actions Job

List Job plugin_actions for a Job specified by {uuid}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # List job plugin_actions Job
    api_response = api_instance.get_job_plugin_actions(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->get_job_plugin_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_job**
> head_job(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a Job exists

Return 200 if the Job specifiec by {uuid} exists, or return NotFound.

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Job
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a Job exists
    api_instance.head_job(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling JobsApi->head_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Job | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_job_log**
> str head_job_log(uuid)

Get the log for this job

Get log for the Job specified by {uuid} or return NotFound.

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # Get the log for this job
    api_response = api_instance.head_job_log(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->head_job_log: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

**str**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_jobs**
> list[Job] list_jobs(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, action=action, archived=archived, available=available, boot_env=boot_env, bundle=bundle, context=context, created_at=created_at, created_by=created_by, current=current, current_index=current_index, end_time=end_time, endpoint=endpoint, errors=errors, exit_state=exit_state, extra_claims=extra_claims, independent=independent, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine=machine, meta=meta, next_index=next_index, previous=previous, read_only=read_only, result_errors=result_errors, stage=stage, start_time=start_time, state=state, target_key=target_key, target_prefix=target_prefix, task=task, token=token, uuid=uuid, validated=validated, work_order=work_order, workflow=workflow)

Lists Jobs filtered by some parameters.

This will show all Jobs by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Uuid=fred - returns items named fred<br/> Uuid=Lt(fred) - returns items that alphabetically less than fred.<br/> Uuid=Lt(fred)&Available=true - returns items with Uuid less than fred and Available is true<br/>

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
offset = 789 # int | The page offset (0-based) into limit per page pages (optional)
limit = 789 # int | The number of objects to return (optional)
filter = 'filter_example' # str | A named filter to user in restricting the query (optional)
raw = 'raw_example' # str | A raw query string to proess (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
group_by = 'group_by_example' # str | A field generate groups from. Can be specified multiple times (optional)
params = 'params_example' # str | A comma separated list of parameters to include in the Params field (optional)
range_only = true # bool | Indicates that only the counts of the objects should be returned for a group-by field (optional)
reverse = true # bool | Indicates that the reverse order of the sort. (optional)
slim = 'slim_example' # str | A comma separated list of fields to remove from the returned objects (optional)
sort = 'sort_example' # str | A field to sort the results by. Multiple can be specified Searches are applied in order across all results. (optional)
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)
action = 'action_example' # str | Action contains the expanded Action information if this Job was created as part of Action processing. (optional)
archived = 'archived_example' # str | Archived indicates whether the complete log for the job can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
boot_env = 'boot_env_example' # str | The bootenv that the task was created in. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
context = 'context_example' # str | Context is the context the job was created to run in. (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
current = 'current_example' # str | Whether the job is the \"current one\" for the machine or if it has been superceded. (optional)
current_index = 'current_index_example' # str | The current index is the machine CurrentTask that created this job.  read only: true (optional)
end_time = 'end_time_example' # str | The time the job failed or finished. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
exit_state = 'exit_state_example' # str | The final disposition of the job. Can be one of \"reboot\",\"poweroff\",\"stop\", or \"complete\" Other substates may be added as time goes on (optional)
extra_claims = 'extra_claims_example' # str | ExtraClaims is the expanded list of extra Claims that were added to the default machine Claims via the ExtraRoles field on the Task that the Job was created to run. (optional)
independent = 'independent_example' # str | Independent indicates that this Job was created to track something besides a task being executed by an agent.  Most of the task state sanity checking performed by the job lifecycle checking will be skipped -- in particular, the job need not be associated with a Workorder or a Machine, it will be permitted to have multiple simultaneous Jobs in flight for the same Target, and State will be ignored for job cleanup purposes. (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
machine = 'machine_example' # str | The machine the job was created for.  This field must be the UUID of the machine. It must be set if Independent is false. (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
next_index = 'next_index_example' # str | The next task index that should be run when this job finishes.  It is used in conjunction with the machine CurrentTask to implement the server side of the machine agent state machine.  read only: true (optional)
previous = 'previous_example' # str | The UUID of the previous job to run on this machine. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
result_errors = 'result_errors_example' # str | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. (optional)
stage = 'stage_example' # str | The stage that the task was created in. read only: true (optional)
start_time = 'start_time_example' # str | The time the job started running. (optional)
state = 'state_example' # str | The state the job is in.  Must be one of \"created\", \"running\", \"failed\", \"finished\", \"incomplete\" (optional)
target_key = 'target_key_example' # str | TargetKey is the Key of the Object that an Independent job was invoked against. It may be empty if TargetPrefix is \"system\". (optional)
target_prefix = 'target_prefix_example' # str | TargetPrefix is the Prefix of the Object that an Independent job was invoked against. It must be set if Independent is true. (optional)
task = 'task_example' # str | The task the job was created for.  This will be the name of the task. read only: true (optional)
token = 'token_example' # str | Token is the JWT token that should be used when running this Job.  If not present or empty, the Agent running the Job will use its ambient Token instead.  If set, the Token will only be valid for the current Job. (optional)
uuid = 'uuid_example' # str | The UUID of the job.  The primary key. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)
work_order = 'work_order_example' # str | The work order the job was created for.  This field must be the UUID of the work order. It must be set if Independent is false and the job is being run on behalf of a WorkOrder. (optional)
workflow = 'workflow_example' # str | The workflow that the task was created in. read only: true (optional)

try:
    # Lists Jobs filtered by some parameters.
    api_response = api_instance.list_jobs(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, action=action, archived=archived, available=available, boot_env=boot_env, bundle=bundle, context=context, created_at=created_at, created_by=created_by, current=current, current_index=current_index, end_time=end_time, endpoint=endpoint, errors=errors, exit_state=exit_state, extra_claims=extra_claims, independent=independent, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine=machine, meta=meta, next_index=next_index, previous=previous, read_only=read_only, result_errors=result_errors, stage=stage, start_time=start_time, state=state, target_key=target_key, target_prefix=target_prefix, task=task, token=token, uuid=uuid, validated=validated, work_order=work_order, workflow=workflow)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->list_jobs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| The page offset (0-based) into limit per page pages | [optional] 
 **limit** | **int**| The number of objects to return | [optional] 
 **filter** | **str**| A named filter to user in restricting the query | [optional] 
 **raw** | **str**| A raw query string to proess | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **group_by** | **str**| A field generate groups from. Can be specified multiple times | [optional] 
 **params** | **str**| A comma separated list of parameters to include in the Params field | [optional] 
 **range_only** | **bool**| Indicates that only the counts of the objects should be returned for a group-by field | [optional] 
 **reverse** | **bool**| Indicates that the reverse order of the sort. | [optional] 
 **slim** | **str**| A comma separated list of fields to remove from the returned objects | [optional] 
 **sort** | **str**| A field to sort the results by. Multiple can be specified Searches are applied in order across all results. | [optional] 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 
 **action** | **str**| Action contains the expanded Action information if this Job was created as part of Action processing. | [optional] 
 **archived** | **str**| Archived indicates whether the complete log for the job can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **boot_env** | **str**| The bootenv that the task was created in. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **context** | **str**| Context is the context the job was created to run in. | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **current** | **str**| Whether the job is the \&quot;current one\&quot; for the machine or if it has been superceded. | [optional] 
 **current_index** | **str**| The current index is the machine CurrentTask that created this job.  read only: true | [optional] 
 **end_time** | **str**| The time the job failed or finished. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **exit_state** | **str**| The final disposition of the job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
 **extra_claims** | **str**| ExtraClaims is the expanded list of extra Claims that were added to the default machine Claims via the ExtraRoles field on the Task that the Job was created to run. | [optional] 
 **independent** | **str**| Independent indicates that this Job was created to track something besides a task being executed by an agent.  Most of the task state sanity checking performed by the job lifecycle checking will be skipped -- in particular, the job need not be associated with a Workorder or a Machine, it will be permitted to have multiple simultaneous Jobs in flight for the same Target, and State will be ignored for job cleanup purposes. | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **machine** | [**str**](.md)| The machine the job was created for.  This field must be the UUID of the machine. It must be set if Independent is false. | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **next_index** | **str**| The next task index that should be run when this job finishes.  It is used in conjunction with the machine CurrentTask to implement the server side of the machine agent state machine.  read only: true | [optional] 
 **previous** | [**str**](.md)| The UUID of the previous job to run on this machine. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **result_errors** | **str**| ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
 **stage** | **str**| The stage that the task was created in. read only: true | [optional] 
 **start_time** | **str**| The time the job started running. | [optional] 
 **state** | **str**| The state the job is in.  Must be one of \&quot;created\&quot;, \&quot;running\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | [optional] 
 **target_key** | **str**| TargetKey is the Key of the Object that an Independent job was invoked against. It may be empty if TargetPrefix is \&quot;system\&quot;. | [optional] 
 **target_prefix** | **str**| TargetPrefix is the Prefix of the Object that an Independent job was invoked against. It must be set if Independent is true. | [optional] 
 **task** | **str**| The task the job was created for.  This will be the name of the task. read only: true | [optional] 
 **token** | **str**| Token is the JWT token that should be used when running this Job.  If not present or empty, the Agent running the Job will use its ambient Token instead.  If set, the Token will only be valid for the current Job. | [optional] 
 **uuid** | [**str**](.md)| The UUID of the job.  The primary key. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 
 **work_order** | [**str**](.md)| The work order the job was created for.  This field must be the UUID of the work order. It must be set if Independent is false and the job is being run on behalf of a WorkOrder. | [optional] 
 **workflow** | **str**| The workflow that the task was created in. read only: true | [optional] 

### Return type

[**list[Job]**](Job.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_stats_jobs**
> list_stats_jobs(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, action=action, archived=archived, available=available, boot_env=boot_env, bundle=bundle, context=context, created_at=created_at, created_by=created_by, current=current, current_index=current_index, end_time=end_time, endpoint=endpoint, errors=errors, exit_state=exit_state, extra_claims=extra_claims, independent=independent, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine=machine, meta=meta, next_index=next_index, previous=previous, read_only=read_only, result_errors=result_errors, stage=stage, start_time=start_time, state=state, target_key=target_key, target_prefix=target_prefix, task=task, token=token, uuid=uuid, validated=validated, work_order=work_order, workflow=workflow)

Stats of the List Jobs filtered by some parameters.

This will return headers with the stats of the list.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> range-only = returns only counts of the objects in the groups.<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Uuid=fred - returns items named fred<br/> Uuid=Lt(fred) - returns items that alphabetically less than fred.<br/> Uuid=Lt(fred)&Available=true - returns items with Uuid less than fred and Available is true<br/>

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
offset = 789 # int | The page offset (0-based) into limit per page pages (optional)
limit = 789 # int | The number of objects to return (optional)
filter = 'filter_example' # str | A named filter to user in restricting the query (optional)
raw = 'raw_example' # str | A raw query string to proess (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
group_by = 'group_by_example' # str | A field generate groups from. Can be specified multiple times (optional)
params = 'params_example' # str | A comma separated list of parameters to include in the Params field (optional)
range_only = true # bool | Indicates that only the counts of the objects should be returned for a group-by field (optional)
reverse = true # bool | Indicates that the reverse order of the sort. (optional)
slim = 'slim_example' # str | A comma separated list of fields to remove from the returned objects (optional)
sort = 'sort_example' # str | A field to sort the results by. Multiple can be specified Searches are applied in order across all results. (optional)
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)
action = 'action_example' # str | Action contains the expanded Action information if this Job was created as part of Action processing. (optional)
archived = 'archived_example' # str | Archived indicates whether the complete log for the job can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
boot_env = 'boot_env_example' # str | The bootenv that the task was created in. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
context = 'context_example' # str | Context is the context the job was created to run in. (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
current = 'current_example' # str | Whether the job is the \"current one\" for the machine or if it has been superceded. (optional)
current_index = 'current_index_example' # str | The current index is the machine CurrentTask that created this job.  read only: true (optional)
end_time = 'end_time_example' # str | The time the job failed or finished. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
exit_state = 'exit_state_example' # str | The final disposition of the job. Can be one of \"reboot\",\"poweroff\",\"stop\", or \"complete\" Other substates may be added as time goes on (optional)
extra_claims = 'extra_claims_example' # str | ExtraClaims is the expanded list of extra Claims that were added to the default machine Claims via the ExtraRoles field on the Task that the Job was created to run. (optional)
independent = 'independent_example' # str | Independent indicates that this Job was created to track something besides a task being executed by an agent.  Most of the task state sanity checking performed by the job lifecycle checking will be skipped -- in particular, the job need not be associated with a Workorder or a Machine, it will be permitted to have multiple simultaneous Jobs in flight for the same Target, and State will be ignored for job cleanup purposes. (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
machine = 'machine_example' # str | The machine the job was created for.  This field must be the UUID of the machine. It must be set if Independent is false. (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
next_index = 'next_index_example' # str | The next task index that should be run when this job finishes.  It is used in conjunction with the machine CurrentTask to implement the server side of the machine agent state machine.  read only: true (optional)
previous = 'previous_example' # str | The UUID of the previous job to run on this machine. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
result_errors = 'result_errors_example' # str | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. (optional)
stage = 'stage_example' # str | The stage that the task was created in. read only: true (optional)
start_time = 'start_time_example' # str | The time the job started running. (optional)
state = 'state_example' # str | The state the job is in.  Must be one of \"created\", \"running\", \"failed\", \"finished\", \"incomplete\" (optional)
target_key = 'target_key_example' # str | TargetKey is the Key of the Object that an Independent job was invoked against. It may be empty if TargetPrefix is \"system\". (optional)
target_prefix = 'target_prefix_example' # str | TargetPrefix is the Prefix of the Object that an Independent job was invoked against. It must be set if Independent is true. (optional)
task = 'task_example' # str | The task the job was created for.  This will be the name of the task. read only: true (optional)
token = 'token_example' # str | Token is the JWT token that should be used when running this Job.  If not present or empty, the Agent running the Job will use its ambient Token instead.  If set, the Token will only be valid for the current Job. (optional)
uuid = 'uuid_example' # str | The UUID of the job.  The primary key. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)
work_order = 'work_order_example' # str | The work order the job was created for.  This field must be the UUID of the work order. It must be set if Independent is false and the job is being run on behalf of a WorkOrder. (optional)
workflow = 'workflow_example' # str | The workflow that the task was created in. read only: true (optional)

try:
    # Stats of the List Jobs filtered by some parameters.
    api_instance.list_stats_jobs(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, action=action, archived=archived, available=available, boot_env=boot_env, bundle=bundle, context=context, created_at=created_at, created_by=created_by, current=current, current_index=current_index, end_time=end_time, endpoint=endpoint, errors=errors, exit_state=exit_state, extra_claims=extra_claims, independent=independent, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine=machine, meta=meta, next_index=next_index, previous=previous, read_only=read_only, result_errors=result_errors, stage=stage, start_time=start_time, state=state, target_key=target_key, target_prefix=target_prefix, task=task, token=token, uuid=uuid, validated=validated, work_order=work_order, workflow=workflow)
except ApiException as e:
    print("Exception when calling JobsApi->list_stats_jobs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| The page offset (0-based) into limit per page pages | [optional] 
 **limit** | **int**| The number of objects to return | [optional] 
 **filter** | **str**| A named filter to user in restricting the query | [optional] 
 **raw** | **str**| A raw query string to proess | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **group_by** | **str**| A field generate groups from. Can be specified multiple times | [optional] 
 **params** | **str**| A comma separated list of parameters to include in the Params field | [optional] 
 **range_only** | **bool**| Indicates that only the counts of the objects should be returned for a group-by field | [optional] 
 **reverse** | **bool**| Indicates that the reverse order of the sort. | [optional] 
 **slim** | **str**| A comma separated list of fields to remove from the returned objects | [optional] 
 **sort** | **str**| A field to sort the results by. Multiple can be specified Searches are applied in order across all results. | [optional] 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 
 **action** | **str**| Action contains the expanded Action information if this Job was created as part of Action processing. | [optional] 
 **archived** | **str**| Archived indicates whether the complete log for the job can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **boot_env** | **str**| The bootenv that the task was created in. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **context** | **str**| Context is the context the job was created to run in. | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **current** | **str**| Whether the job is the \&quot;current one\&quot; for the machine or if it has been superceded. | [optional] 
 **current_index** | **str**| The current index is the machine CurrentTask that created this job.  read only: true | [optional] 
 **end_time** | **str**| The time the job failed or finished. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **exit_state** | **str**| The final disposition of the job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
 **extra_claims** | **str**| ExtraClaims is the expanded list of extra Claims that were added to the default machine Claims via the ExtraRoles field on the Task that the Job was created to run. | [optional] 
 **independent** | **str**| Independent indicates that this Job was created to track something besides a task being executed by an agent.  Most of the task state sanity checking performed by the job lifecycle checking will be skipped -- in particular, the job need not be associated with a Workorder or a Machine, it will be permitted to have multiple simultaneous Jobs in flight for the same Target, and State will be ignored for job cleanup purposes. | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **machine** | [**str**](.md)| The machine the job was created for.  This field must be the UUID of the machine. It must be set if Independent is false. | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **next_index** | **str**| The next task index that should be run when this job finishes.  It is used in conjunction with the machine CurrentTask to implement the server side of the machine agent state machine.  read only: true | [optional] 
 **previous** | [**str**](.md)| The UUID of the previous job to run on this machine. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **result_errors** | **str**| ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
 **stage** | **str**| The stage that the task was created in. read only: true | [optional] 
 **start_time** | **str**| The time the job started running. | [optional] 
 **state** | **str**| The state the job is in.  Must be one of \&quot;created\&quot;, \&quot;running\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | [optional] 
 **target_key** | **str**| TargetKey is the Key of the Object that an Independent job was invoked against. It may be empty if TargetPrefix is \&quot;system\&quot;. | [optional] 
 **target_prefix** | **str**| TargetPrefix is the Prefix of the Object that an Independent job was invoked against. It must be set if Independent is true. | [optional] 
 **task** | **str**| The task the job was created for.  This will be the name of the task. read only: true | [optional] 
 **token** | **str**| Token is the JWT token that should be used when running this Job.  If not present or empty, the Agent running the Job will use its ambient Token instead.  If set, the Token will only be valid for the current Job. | [optional] 
 **uuid** | [**str**](.md)| The UUID of the job.  The primary key. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 
 **work_order** | [**str**](.md)| The work order the job was created for.  This field must be the UUID of the work order. It must be set if Independent is false and the job is being run on behalf of a WorkOrder. | [optional] 
 **workflow** | **str**| The workflow that the task was created in. read only: true | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_job**
> Job patch_job(body, uuid, force=force, commented=commented, reduced=reduced)

Patch a Job

Update a Job specified by {uuid} using a RFC6902 Patch structure

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
uuid = 'uuid_example' # str | Identity key of the Job
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a Job
    api_response = api_instance.patch_job(body, uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->patch_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **uuid** | [**str**](.md)| Identity key of the Job | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Job**](Job.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_job_action**
> object post_job_action(uuid)

Call an action on the node.

Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # Call an action on the node.
    api_response = api_instance.post_job_action(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->post_job_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_job**
> Job put_job(body, uuid, force=force, commented=commented, reduced=reduced)

Put a Job

Update a Job specified by {uuid} using a JSON Job

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Job() # Job | 
uuid = 'uuid_example' # str | Identity key of the Job
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a Job
    api_response = api_instance.put_job(body, uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsApi->put_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Job**](Job.md)|  | 
 **uuid** | [**str**](.md)| Identity key of the Job | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Job**](Job.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_job_log**
> put_job_log(uuid)

Append the string to the end of the job's log.

### Example
```python
from __future__ import print_function
import time
import drppy_client
from drppy_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Bearer
configuration = drppy_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: basicAuth
configuration = drppy_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = drppy_client.JobsApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # Append the string to the end of the job's log.
    api_instance.put_job_log(uuid)
except ApiException as e:
    print("Exception when calling JobsApi->put_job_log: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

