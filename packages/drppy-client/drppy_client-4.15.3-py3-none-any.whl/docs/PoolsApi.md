# drppy_client.PoolsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pool**](PoolsApi.md#create_pool) | **POST** /pools | Create a Pool
[**delete_pool**](PoolsApi.md#delete_pool) | **DELETE** /pools/{id} | Delete a Pool
[**get_pool**](PoolsApi.md#get_pool) | **GET** /pools/{id} | Get a Pool
[**get_pool_action**](PoolsApi.md#get_pool_action) | **GET** /pools/{id}/actions/{cmd} | List specific action for a pools Pool
[**get_pool_actions**](PoolsApi.md#get_pool_actions) | **GET** /pools/{id}/actions | List pools actions Pool
[**get_pool_status**](PoolsApi.md#get_pool_status) | **GET** /pools/{id}/status | Returns the status of the machines in the pool
[**head_pool**](PoolsApi.md#head_pool) | **HEAD** /pools/{id} | See if a Pool exists
[**list_active_pools**](PoolsApi.md#list_active_pools) | **GET** /pools-active | Lists active Pools
[**list_pools**](PoolsApi.md#list_pools) | **GET** /pools | Lists Pools filtered by some parameters.
[**list_stats_pools**](PoolsApi.md#list_stats_pools) | **HEAD** /pools | Stats of the List Pools filtered by some parameters.
[**patch_pool**](PoolsApi.md#patch_pool) | **PATCH** /pools/{id} | Patch a Pool
[**post_pool_action**](PoolsApi.md#post_pool_action) | **POST** /pools/{id}/actions/{cmd} | Call an action on the node.
[**post_pool_add_machines**](PoolsApi.md#post_pool_add_machines) | **POST** /pools/{id}/addMachines | Add machines to this pool from default.
[**post_pool_allocate_machines**](PoolsApi.md#post_pool_allocate_machines) | **POST** /pools/{id}/allocateMachines | Allocate machines in this pool.
[**post_pool_release_machines**](PoolsApi.md#post_pool_release_machines) | **POST** /pools/{id}/releaseMachines | Release machines in this pool.
[**post_pool_remove_machines**](PoolsApi.md#post_pool_remove_machines) | **POST** /pools/{id}/removeMachines | Remove machines from this pool to default.
[**put_pool**](PoolsApi.md#put_pool) | **PUT** /pools/{id} | Put a Pool


# **create_pool**
> Pool create_pool(body)

Create a Pool

Create a Pool from the provided object

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Pool() # Pool | 

try:
    # Create a Pool
    api_response = api_instance.create_pool(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->create_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Pool**](Pool.md)|  | 

### Return type

[**Pool**](Pool.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_pool**
> Pool delete_pool(id, force=force, commented=commented, reduced=reduced)

Delete a Pool

Delete a Pool specified by {id}

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Pool
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a Pool
    api_response = api_instance.delete_pool(id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->delete_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Pool | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Pool**](Pool.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pool**
> Pool get_pool(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a Pool

Get the Pool specified by {id}  or return NotFound.

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Pool
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a Pool
    api_response = api_instance.get_pool(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->get_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Pool | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Pool**](Pool.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pool_action**
> AvailableAction get_pool_action(id, cmd, plugin=plugin)

List specific action for a pools Pool

List specific {cmd} action for a Pool specified by {id}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Pool
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a pools Pool
    api_response = api_instance.get_pool_action(id, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->get_pool_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Pool | 
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

# **get_pool_actions**
> list[AvailableAction] get_pool_actions(id, plugin=plugin)

List pools actions Pool

List Pool actions for a Pool specified by {id}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Pool
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List pools actions Pool
    api_response = api_instance.get_pool_actions(id, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->get_pool_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Pool | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pool_status**
> PoolStatus get_pool_status(id)

Returns the status of the machines in the pool

Returns the status of the machines in the pool

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Returns the status of the machines in the pool
    api_response = api_instance.get_pool_status(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->get_pool_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**PoolStatus**](PoolStatus.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_pool**
> head_pool(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a Pool exists

Return 200 if the Pool specifiec by {id} exists, or return NotFound.

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Pool
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a Pool exists
    api_instance.head_pool(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling PoolsApi->head_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Pool | 
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

# **list_active_pools**
> list[str] list_active_pools()

Lists active Pools

Returns the list of active pools

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))

try:
    # Lists active Pools
    api_response = api_instance.list_active_pools()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->list_active_pools: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**list[str]**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_pools**
> list[Pool] list_pools(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, allocate_actions=allocate_actions, auto_fill=auto_fill, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, enter_actions=enter_actions, errors=errors, exit_actions=exit_actions, id=id, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, parent_pool=parent_pool, read_only=read_only, release_actions=release_actions, validated=validated)

Lists Pools filtered by some parameters.

This will show all Pools by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Id=fred - returns items named fred<br/> Id=Lt(fred) - returns items that alphabetically less than fred.<br/> Id=Lt(fred)&Available=true - returns items with Id less than fred and Available is true<br/>

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
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
allocate_actions = 'allocate_actions_example' # str | AllocateActions defines a set of configuration for machines allocating in the pool. (optional)
auto_fill = 'auto_fill_example' # str | AutoFill defines configuration to handle Pool scaling. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
enter_actions = 'enter_actions_example' # str | EnterActions defines a set of configuration for machines entering the pool. (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
exit_actions = 'exit_actions_example' # str | ExitActions defines a set of configuration for machines exiting the pool. (optional)
id = 'id_example' # str | Id is the name of the pool (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
parent_pool = 'parent_pool_example' # str | ParentPool contains the pool that machines should Enter from and Exit to. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
release_actions = 'release_actions_example' # str | ReleaseActions defines a set of configuration for machines releasing in the pool. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Lists Pools filtered by some parameters.
    api_response = api_instance.list_pools(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, allocate_actions=allocate_actions, auto_fill=auto_fill, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, enter_actions=enter_actions, errors=errors, exit_actions=exit_actions, id=id, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, parent_pool=parent_pool, read_only=read_only, release_actions=release_actions, validated=validated)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->list_pools: %s\n" % e)
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
 **allocate_actions** | **str**| AllocateActions defines a set of configuration for machines allocating in the pool. | [optional] 
 **auto_fill** | **str**| AutoFill defines configuration to handle Pool scaling. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **enter_actions** | **str**| EnterActions defines a set of configuration for machines entering the pool. | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **exit_actions** | **str**| ExitActions defines a set of configuration for machines exiting the pool. | [optional] 
 **id** | **str**| Id is the name of the pool | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **parent_pool** | **str**| ParentPool contains the pool that machines should Enter from and Exit to. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **release_actions** | **str**| ReleaseActions defines a set of configuration for machines releasing in the pool. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

[**list[Pool]**](Pool.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_stats_pools**
> list_stats_pools(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, allocate_actions=allocate_actions, auto_fill=auto_fill, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, enter_actions=enter_actions, errors=errors, exit_actions=exit_actions, id=id, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, parent_pool=parent_pool, read_only=read_only, release_actions=release_actions, validated=validated)

Stats of the List Pools filtered by some parameters.

This will return headers with the stats of the list.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> range-only = returns only counts of the objects in the groups.<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Id=fred - returns items named fred<br/> Id=Lt(fred) - returns items that alphabetically less than fred.<br/> Id=Lt(fred)&Available=true - returns items with Id less than fred and Available is true<br/>

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
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
allocate_actions = 'allocate_actions_example' # str | AllocateActions defines a set of configuration for machines allocating in the pool. (optional)
auto_fill = 'auto_fill_example' # str | AutoFill defines configuration to handle Pool scaling. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
enter_actions = 'enter_actions_example' # str | EnterActions defines a set of configuration for machines entering the pool. (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
exit_actions = 'exit_actions_example' # str | ExitActions defines a set of configuration for machines exiting the pool. (optional)
id = 'id_example' # str | Id is the name of the pool (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
parent_pool = 'parent_pool_example' # str | ParentPool contains the pool that machines should Enter from and Exit to. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
release_actions = 'release_actions_example' # str | ReleaseActions defines a set of configuration for machines releasing in the pool. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Stats of the List Pools filtered by some parameters.
    api_instance.list_stats_pools(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, allocate_actions=allocate_actions, auto_fill=auto_fill, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, enter_actions=enter_actions, errors=errors, exit_actions=exit_actions, id=id, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, parent_pool=parent_pool, read_only=read_only, release_actions=release_actions, validated=validated)
except ApiException as e:
    print("Exception when calling PoolsApi->list_stats_pools: %s\n" % e)
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
 **allocate_actions** | **str**| AllocateActions defines a set of configuration for machines allocating in the pool. | [optional] 
 **auto_fill** | **str**| AutoFill defines configuration to handle Pool scaling. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **enter_actions** | **str**| EnterActions defines a set of configuration for machines entering the pool. | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **exit_actions** | **str**| ExitActions defines a set of configuration for machines exiting the pool. | [optional] 
 **id** | **str**| Id is the name of the pool | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **parent_pool** | **str**| ParentPool contains the pool that machines should Enter from and Exit to. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **release_actions** | **str**| ReleaseActions defines a set of configuration for machines releasing in the pool. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_pool**
> Pool patch_pool(body, id, force=force, commented=commented, reduced=reduced)

Patch a Pool

Update a Pool specified by {id} using a RFC6902 Patch structure

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
id = 'id_example' # str | Identity key of the Pool
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a Pool
    api_response = api_instance.patch_pool(body, id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->patch_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **id** | **str**| Identity key of the Pool | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Pool**](Pool.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_pool_action**
> object post_pool_action(id, cmd, body, plugin=plugin)

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Pool
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_pool_action(id, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->post_pool_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Pool | 
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

# **post_pool_add_machines**
> list[PoolResult] post_pool_add_machines(id, body, force=force, source_pool=source_pool)

Add machines to this pool from default.

Input is a map with the following fields.  These fields override the pool definitions if they exist on the pool. pool/workflow = workflow of to set on transition pool/add-profiles pool/add-parameters pool/remove-profiles pool/remove-parameters  These fields define what to operate. pool/count = how many nodes to change pool/minimum = minimum machnies to allocate or fail pool/filter = list of list-style filters (e.g. Runnable=Eq(true)) pool/wait-timeout = Time to delay in seconds or time string (30m) pool/machine-list - a list of machine UUID or Name:name pool/all-machines - boolean for all machines in pool

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | 
body = NULL # object | 
force = 'force_example' # str |  (optional)
source_pool = 'source_pool_example' # str |  (optional)

try:
    # Add machines to this pool from default.
    api_response = api_instance.post_pool_add_machines(id, body, force=force, source_pool=source_pool)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->post_pool_add_machines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | 
 **force** | **str**|  | [optional] 
 **source_pool** | **str**|  | [optional] 

### Return type

[**list[PoolResult]**](PoolResult.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_pool_allocate_machines**
> list[PoolResult] post_pool_allocate_machines(id, body, force=force, source_pool=source_pool)

Allocate machines in this pool.

Input is a map with the following fields.  These fields override the pool definitions if they exist on the pool. pool/workflow = workflow of to set on transition pool/add-profiles pool/add-parameters pool/remove-profiles pool/remove-parameters  These fields define what to operate. pool/count = how many nodes to change pool/minimum = minimum machnies to allocate or fail pool/filter = list of list-style filters (e.g. Runnable=Eq(true)) pool/wait-timeout = Time to delay in seconds or time string (30m) pool/machine-list - a list of machine UUID or Name:name pool/all-machines - boolean for all machines in pool

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | 
body = NULL # object | 
force = 'force_example' # str |  (optional)
source_pool = 'source_pool_example' # str |  (optional)

try:
    # Allocate machines in this pool.
    api_response = api_instance.post_pool_allocate_machines(id, body, force=force, source_pool=source_pool)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->post_pool_allocate_machines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | 
 **force** | **str**|  | [optional] 
 **source_pool** | **str**|  | [optional] 

### Return type

[**list[PoolResult]**](PoolResult.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_pool_release_machines**
> list[PoolResult] post_pool_release_machines(id, body, force=force, source_pool=source_pool)

Release machines in this pool.

Input is a map with the following fields.  These fields override the pool definitions if they exist on the pool. pool/workflow = workflow of to set on transition pool/add-profiles pool/add-parameters pool/remove-profiles pool/remove-parameters  These fields define what to operate. pool/count = how many nodes to change pool/minimum = minimum machnies to allocate or fail pool/filter = list of list-style filters (e.g. Runnable=Eq(true)) pool/wait-timeout = Time to delay in seconds or time string (30m) pool/machine-list - a list of machine UUID or Name:name pool/all-machines - boolean for all machines in pool

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | 
body = NULL # object | 
force = 'force_example' # str |  (optional)
source_pool = 'source_pool_example' # str |  (optional)

try:
    # Release machines in this pool.
    api_response = api_instance.post_pool_release_machines(id, body, force=force, source_pool=source_pool)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->post_pool_release_machines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | 
 **force** | **str**|  | [optional] 
 **source_pool** | **str**|  | [optional] 

### Return type

[**list[PoolResult]**](PoolResult.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_pool_remove_machines**
> list[PoolResult] post_pool_remove_machines(id, body, force=force, source_pool=source_pool)

Remove machines from this pool to default.

Input is a map with the following fields.  These fields override the pool definitions if they exist on the pool. pool/workflow = workflow of to set on transition pool/add-profiles pool/add-parameters pool/remove-profiles pool/remove-parameters  These fields define what to operate. pool/count = how many nodes to change pool/minimum = minimum machnies to allocate or fail pool/filter = list of list-style filters (e.g. Runnable=Eq(true)) pool/wait-timeout = Time to delay in seconds or time string (30m) pool/machine-list - a list of machine UUID or Name:name pool/all-machines - boolean for all machines in pool

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | 
body = NULL # object | 
force = 'force_example' # str |  (optional)
source_pool = 'source_pool_example' # str |  (optional)

try:
    # Remove machines from this pool to default.
    api_response = api_instance.post_pool_remove_machines(id, body, force=force, source_pool=source_pool)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->post_pool_remove_machines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | 
 **force** | **str**|  | [optional] 
 **source_pool** | **str**|  | [optional] 

### Return type

[**list[PoolResult]**](PoolResult.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_pool**
> Pool put_pool(body, id, force=force, commented=commented, reduced=reduced)

Put a Pool

Update a Pool specified by {id} using a JSON Pool

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
api_instance = drppy_client.PoolsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Pool() # Pool | 
id = 'id_example' # str | Identity key of the Pool
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a Pool
    api_response = api_instance.put_pool(body, id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->put_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Pool**](Pool.md)|  | 
 **id** | **str**| Identity key of the Pool | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Pool**](Pool.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

