# drppy_client.WorkflowsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_workflow**](WorkflowsApi.md#create_workflow) | **POST** /workflows | Create a Workflow
[**delete_workflow**](WorkflowsApi.md#delete_workflow) | **DELETE** /workflows/{name} | Delete a Workflow
[**get_workflow**](WorkflowsApi.md#get_workflow) | **GET** /workflows/{name} | Get a Workflow
[**get_workflow_action**](WorkflowsApi.md#get_workflow_action) | **GET** /workflows/{name}/actions/{cmd} | List specific action for a workflows Workflow
[**get_workflow_actions**](WorkflowsApi.md#get_workflow_actions) | **GET** /workflows/{name}/actions | List workflows actions Workflow
[**head_workflow**](WorkflowsApi.md#head_workflow) | **HEAD** /workflows/{name} | See if a Workflow exists
[**list_stats_workflows**](WorkflowsApi.md#list_stats_workflows) | **HEAD** /workflows | Stats of the List Workflows filtered by some parameters.
[**list_workflows**](WorkflowsApi.md#list_workflows) | **GET** /workflows | Lists Workflows filtered by some parameters.
[**patch_workflow**](WorkflowsApi.md#patch_workflow) | **PATCH** /workflows/{name} | Patch a Workflow
[**post_workflow_action**](WorkflowsApi.md#post_workflow_action) | **POST** /workflows/{name}/actions/{cmd} | Call an action on the node.
[**put_workflow**](WorkflowsApi.md#put_workflow) | **PUT** /workflows/{name} | Put a Workflow


# **create_workflow**
> Workflow create_workflow(body)

Create a Workflow

Create a Workflow from the provided object

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Workflow() # Workflow | 

try:
    # Create a Workflow
    api_response = api_instance.create_workflow(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->create_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Workflow**](Workflow.md)|  | 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_workflow**
> Workflow delete_workflow(name, force=force, commented=commented, reduced=reduced)

Delete a Workflow

Delete a Workflow specified by {name}

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Workflow
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a Workflow
    api_response = api_instance.delete_workflow(name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->delete_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Workflow | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workflow**
> Workflow get_workflow(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a Workflow

Get the Workflow specified by {name}  or return NotFound.

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Workflow
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a Workflow
    api_response = api_instance.get_workflow(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->get_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Workflow | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workflow_action**
> AvailableAction get_workflow_action(name, cmd, plugin=plugin)

List specific action for a workflows Workflow

List specific {cmd} action for a Workflow specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Workflow
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a workflows Workflow
    api_response = api_instance.get_workflow_action(name, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->get_workflow_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Workflow | 
 **cmd** | **str**| The action to run on the plugin | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**AvailableAction**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workflow_actions**
> list[AvailableAction] get_workflow_actions(name, plugin=plugin)

List workflows actions Workflow

List Workflow actions for a Workflow specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Workflow
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List workflows actions Workflow
    api_response = api_instance.get_workflow_actions(name, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->get_workflow_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Workflow | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_workflow**
> head_workflow(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a Workflow exists

Return 200 if the Workflow specifiec by {name} exists, or return NotFound.

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Workflow
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a Workflow exists
    api_instance.head_workflow(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling WorkflowsApi->head_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Workflow | 
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

# **list_stats_workflows**
> list_stats_workflows(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, errors=errors, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, name=name, read_only=read_only, stages=stages, validated=validated)

Stats of the List Workflows filtered by some parameters.

This will return headers with the stats of the list.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> range-only = returns only counts of the objects in the groups.<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
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
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | Name defines the name of the workflow (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
stages = 'stages_example' # str | Stages contains the list of stages that make up the workflow.  Additionally, tasks can be directly specified by prepending `task:` to the task name. Additionally, actions can be directly specified by prepending `action:` to the action name. Additionally, context changes can be directly specified by prepending `context:` to the context name. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Stats of the List Workflows filtered by some parameters.
    api_instance.list_stats_workflows(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, errors=errors, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, name=name, read_only=read_only, stages=stages, validated=validated)
except ApiException as e:
    print("Exception when calling WorkflowsApi->list_stats_workflows: %s\n" % e)
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
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| Name defines the name of the workflow | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **stages** | **str**| Stages contains the list of stages that make up the workflow.  Additionally, tasks can be directly specified by prepending &#x60;task:&#x60; to the task name. Additionally, actions can be directly specified by prepending &#x60;action:&#x60; to the action name. Additionally, context changes can be directly specified by prepending &#x60;context:&#x60; to the context name. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workflows**
> list[Workflow] list_workflows(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, errors=errors, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, name=name, read_only=read_only, stages=stages, validated=validated)

Lists Workflows filtered by some parameters.

This will show all Workflows by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
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
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | Name defines the name of the workflow (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
stages = 'stages_example' # str | Stages contains the list of stages that make up the workflow.  Additionally, tasks can be directly specified by prepending `task:` to the task name. Additionally, actions can be directly specified by prepending `action:` to the action name. Additionally, context changes can be directly specified by prepending `context:` to the context name. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Lists Workflows filtered by some parameters.
    api_response = api_instance.list_workflows(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, errors=errors, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, name=name, read_only=read_only, stages=stages, validated=validated)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->list_workflows: %s\n" % e)
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
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| Name defines the name of the workflow | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **stages** | **str**| Stages contains the list of stages that make up the workflow.  Additionally, tasks can be directly specified by prepending &#x60;task:&#x60; to the task name. Additionally, actions can be directly specified by prepending &#x60;action:&#x60; to the action name. Additionally, context changes can be directly specified by prepending &#x60;context:&#x60; to the context name. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

[**list[Workflow]**](Workflow.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_workflow**
> Workflow patch_workflow(body, name, force=force, commented=commented, reduced=reduced)

Patch a Workflow

Update a Workflow specified by {name} using a RFC6902 Patch structure

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
name = 'name_example' # str | Identity key of the Workflow
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a Workflow
    api_response = api_instance.patch_workflow(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->patch_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **name** | **str**| Identity key of the Workflow | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_workflow_action**
> object post_workflow_action(name, cmd, body, plugin=plugin)

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Workflow
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_workflow_action(name, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->post_workflow_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Workflow | 
 **cmd** | **str**| The action to run on the plugin | 
 **body** | **object**| Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {} | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_workflow**
> Workflow put_workflow(body, name, force=force, commented=commented, reduced=reduced)

Put a Workflow

Update a Workflow specified by {name} using a JSON Workflow

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
api_instance = drppy_client.WorkflowsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Workflow() # Workflow | 
name = 'name_example' # str | Identity key of the Workflow
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a Workflow
    api_response = api_instance.put_workflow(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowsApi->put_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Workflow**](Workflow.md)|  | 
 **name** | **str**| Identity key of the Workflow | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Workflow**](Workflow.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

