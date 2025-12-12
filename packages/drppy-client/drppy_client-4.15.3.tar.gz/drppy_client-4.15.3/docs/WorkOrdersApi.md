# drppy_client.WorkOrdersApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_work_order**](WorkOrdersApi.md#create_work_order) | **POST** /work_orders | Create a WorkOrder
[**delete_work_order**](WorkOrdersApi.md#delete_work_order) | **DELETE** /work_orders/{uuid} | Delete a WorkOrder
[**delete_work_order_param**](WorkOrdersApi.md#delete_work_order_param) | **DELETE** /work_orders/{uuid}/params/{key} | Delete a single work_orders parameter
[**delete_work_orders**](WorkOrdersApi.md#delete_work_orders) | **DELETE** /work_orders | Delete WorkOrders that reference removed machines.
[**get_work_order**](WorkOrdersApi.md#get_work_order) | **GET** /work_orders/{uuid} | Get a WorkOrder
[**get_work_order_action**](WorkOrdersApi.md#get_work_order_action) | **GET** /work_orders/{uuid}/actions/{cmd} | List specific action for a work_orders WorkOrder
[**get_work_order_actions**](WorkOrdersApi.md#get_work_order_actions) | **GET** /work_orders/{uuid}/actions | List work_orders actions WorkOrder
[**get_work_order_param**](WorkOrdersApi.md#get_work_order_param) | **GET** /work_orders/{uuid}/params/{key} | Get a single work_orders parameter
[**get_work_order_params**](WorkOrdersApi.md#get_work_order_params) | **GET** /work_orders/{uuid}/params | List work_orders params WorkOrder
[**get_work_order_pub_key**](WorkOrdersApi.md#get_work_order_pub_key) | **GET** /work_orders/{uuid}/pubkey | Get the public key for secure params on a work_orders
[**head_work_order**](WorkOrdersApi.md#head_work_order) | **HEAD** /work_orders/{uuid} | See if a WorkOrder exists
[**list_stats_work_orders**](WorkOrdersApi.md#list_stats_work_orders) | **HEAD** /work_orders | Stats of the List WorkOrders filtered by some parameters.
[**list_work_orders**](WorkOrdersApi.md#list_work_orders) | **GET** /work_orders | Lists WorkOrders filtered by some parameters.
[**patch_work_order**](WorkOrdersApi.md#patch_work_order) | **PATCH** /work_orders/{uuid} | Patch a WorkOrder
[**patch_work_order_params**](WorkOrdersApi.md#patch_work_order_params) | **PATCH** /work_orders/{uuid}/params | Update all params on the object (merges with existing data)
[**post_work_order_action**](WorkOrdersApi.md#post_work_order_action) | **POST** /work_orders/{uuid}/actions/{cmd} | Call an action on the node.
[**post_work_order_param**](WorkOrdersApi.md#post_work_order_param) | **POST** /work_orders/{uuid}/params/{key} | Set a single parameter on an object
[**post_work_order_params**](WorkOrdersApi.md#post_work_order_params) | **POST** /work_orders/{uuid}/params | Replaces all parameters on the object
[**put_work_order**](WorkOrdersApi.md#put_work_order) | **PUT** /work_orders/{uuid} | Put a WorkOrder


# **create_work_order**
> WorkOrder create_work_order(body)

Create a WorkOrder

The provided WorkOrder object will be injected into the system.  The UUID field is optional and will be filled if not provided.  One of the Machine field or the Filter field must be provided.  The Machine is the UUID of a machine to run the WorkOrder.  The Filter is a List filter that should be used to find a Machine to run this WorkOrder.  One of the Blueprint field or the Tasks field must be provided to define what should be run by the Machine/Filter.  State should not be provided or set to \"created\".  It will be set to \"created\".

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
body = drppy_client.WorkOrder() # WorkOrder | 

try:
    # Create a WorkOrder
    api_response = api_instance.create_work_order(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->create_work_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WorkOrder**](WorkOrder.md)|  | 

### Return type

[**WorkOrder**](WorkOrder.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_work_order**
> WorkOrder delete_work_order(uuid, force=force, commented=commented, reduced=reduced)

Delete a WorkOrder

Delete a WorkOrder specified by {uuid}

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a WorkOrder
    api_response = api_instance.delete_work_order(uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->delete_work_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**WorkOrder**](WorkOrder.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_work_order_param**
> object delete_work_order_param()

Delete a single work_orders parameter

Delete a single parameter {key} for a WorkOrder specified by {uuid}

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))

try:
    # Delete a single work_orders parameter
    api_response = api_instance.delete_work_order_param()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->delete_work_order_param: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_work_orders**
> delete_work_orders()

Delete WorkOrders that reference removed machines.

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))

try:
    # Delete WorkOrders that reference removed machines.
    api_instance.delete_work_orders()
except ApiException as e:
    print("Exception when calling WorkOrdersApi->delete_work_orders: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_work_order**
> WorkOrder get_work_order(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a WorkOrder

Get the WorkOrder specified by {uuid}  or return NotFound.

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a WorkOrder
    api_response = api_instance.get_work_order(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->get_work_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**WorkOrder**](WorkOrder.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_work_order_action**
> AvailableAction get_work_order_action(uuid, cmd, plugin=plugin)

List specific action for a work_orders WorkOrder

List specific {cmd} action for a WorkOrder specified by {uuid}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a work_orders WorkOrder
    api_response = api_instance.get_work_order_action(uuid, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->get_work_order_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
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

# **get_work_order_actions**
> list[AvailableAction] get_work_order_actions(uuid, plugin=plugin)

List work_orders actions WorkOrder

List WorkOrder actions for a WorkOrder specified by {uuid}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List work_orders actions WorkOrder
    api_response = api_instance.get_work_order_actions(uuid, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->get_work_order_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_work_order_param**
> object get_work_order_param(uuid, key, aggregate=aggregate, decode=decode)

Get a single work_orders parameter

Get a single parameter {key} for a WorkOrder specified by {uuid}

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder
key = 'key_example' # str | Param name
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)

try:
    # Get a single work_orders parameter
    api_response = api_instance.get_work_order_param(uuid, key, aggregate=aggregate, decode=decode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->get_work_order_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
 **key** | **str**| Param name | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_work_order_params**
> dict(str, object) get_work_order_params(uuid, aggregate=aggregate, decode=decode, params=params)

List work_orders params WorkOrder

List WorkOrder parms for a WorkOrder specified by {uuid}

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
params = 'params_example' # str |  (optional)

try:
    # List work_orders params WorkOrder
    api_response = api_instance.get_work_order_params(uuid, aggregate=aggregate, decode=decode, params=params)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->get_work_order_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **params** | **str**|  | [optional] 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_work_order_pub_key**
> get_work_order_pub_key(uuid)

Get the public key for secure params on a work_orders

Get the public key for a WorkOrder specified by {uuid}

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder

try:
    # Get the public key for secure params on a work_orders
    api_instance.get_work_order_pub_key(uuid)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->get_work_order_pub_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_work_order**
> head_work_order(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a WorkOrder exists

Return 200 if the WorkOrder specifiec by {uuid} exists, or return NotFound.

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a WorkOrder exists
    api_instance.head_work_order(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->head_work_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
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

# **list_stats_work_orders**
> list_stats_work_orders(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, archived=archived, available=available, blueprint=blueprint, bundle=bundle, context=context, create_time=create_time, created_at=created_at, created_by=created_by, current_job=current_job, current_task=current_task, end_time=end_time, endpoint=endpoint, errors=errors, filter2=filter2, job_exit_state=job_exit_state, job_result_errors=job_result_errors, job_state=job_state, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine=machine, meta=meta, params2=params2, profiles=profiles, read_only=read_only, retry_task_attempt=retry_task_attempt, runnable=runnable, stage=stage, start_time=start_time, state=state, status=status, task_error_stacks=task_error_stacks, tasks=tasks, uuid=uuid, validated=validated)

Stats of the List WorkOrders filtered by some parameters.

This will return headers with the stats of the list.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> range-only = returns only counts of the objects in the groups.<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Uuid=fred - returns items named fred<br/> Uuid=Lt(fred) - returns items that alphabetically less than fred.<br/> Uuid=Lt(fred)&Available=true - returns items with Uuid less than fred and Available is true<br/>

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
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
archived = 'archived_example' # str | Archived indicates whether the complete log for the async action can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
blueprint = 'blueprint_example' # str | Blueprint defines the tasks and base parameters for this action (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
context = 'context_example' # str | Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. (optional)
create_time = 'create_time_example' # str | CreateTime is the time the work order was created.  This is distinct from StartTime, as there may be a significant delay before the workorder starts running. (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
current_job = 'current_job_example' # str | The UUID of the job that is currently running. (optional)
current_task = 'current_task_example' # str | The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. (optional)
end_time = 'end_time_example' # str | EndTime The time the async action failed or finished or cancelled. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
filter2 = 'filter_example' # str | Filter is a list filter for this WorkOrder (optional)
job_exit_state = 'job_exit_state_example' # str | The final disposition of the current job. Can be one of \"reboot\",\"poweroff\",\"stop\", or \"complete\" Other substates may be added as time goes on (optional)
job_result_errors = 'job_result_errors_example' # str | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. (optional)
job_state = 'job_state_example' # str | The state the current job is in.  Must be one of \"created\", \"failed\", \"finished\", \"incomplete\" (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
machine = 'machine_example' # str | Machine is the key of the machine running the WorkOrder (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
params2 = 'params_example' # str | Params that have been directly set on the Machine. (optional)
profiles = 'profiles_example' # str | Profiles An array of profiles to apply to this machine in order when looking for a parameter during rendering. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
retry_task_attempt = 'retry_task_attempt_example' # str | This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. (optional)
runnable = 'runnable_example' # str | Runnable indicates that this is Runnable. (optional)
stage = 'stage_example' # str | The stage that this is currently in. (optional)
start_time = 'start_time_example' # str | StartTime The time the async action started running. (optional)
state = 'state_example' # str | State The state the async action is in.  Must be one of \"created\", \"running\", \"failed\", \"finished\", \"cancelled\" (optional)
status = 'status_example' # str | Status is a short text snippet for humans explaining the current state. (optional)
task_error_stacks = 'task_error_stacks_example' # str | This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. (optional)
tasks = 'tasks_example' # str | The current tasks that are being processed. (optional)
uuid = 'uuid_example' # str | Uuid is the key of this particular WorkOrder. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Stats of the List WorkOrders filtered by some parameters.
    api_instance.list_stats_work_orders(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, archived=archived, available=available, blueprint=blueprint, bundle=bundle, context=context, create_time=create_time, created_at=created_at, created_by=created_by, current_job=current_job, current_task=current_task, end_time=end_time, endpoint=endpoint, errors=errors, filter2=filter2, job_exit_state=job_exit_state, job_result_errors=job_result_errors, job_state=job_state, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine=machine, meta=meta, params2=params2, profiles=profiles, read_only=read_only, retry_task_attempt=retry_task_attempt, runnable=runnable, stage=stage, start_time=start_time, state=state, status=status, task_error_stacks=task_error_stacks, tasks=tasks, uuid=uuid, validated=validated)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->list_stats_work_orders: %s\n" % e)
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
 **archived** | **str**| Archived indicates whether the complete log for the async action can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **blueprint** | **str**| Blueprint defines the tasks and base parameters for this action | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **context** | **str**| Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. | [optional] 
 **create_time** | **str**| CreateTime is the time the work order was created.  This is distinct from StartTime, as there may be a significant delay before the workorder starts running. | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **current_job** | [**str**](.md)| The UUID of the job that is currently running. | [optional] 
 **current_task** | **str**| The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. | [optional] 
 **end_time** | **str**| EndTime The time the async action failed or finished or cancelled. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **filter2** | **str**| Filter is a list filter for this WorkOrder | [optional] 
 **job_exit_state** | **str**| The final disposition of the current job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
 **job_result_errors** | **str**| ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
 **job_state** | **str**| The state the current job is in.  Must be one of \&quot;created\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **machine** | [**str**](.md)| Machine is the key of the machine running the WorkOrder | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **params2** | **str**| Params that have been directly set on the Machine. | [optional] 
 **profiles** | **str**| Profiles An array of profiles to apply to this machine in order when looking for a parameter during rendering. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **retry_task_attempt** | **str**| This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. | [optional] 
 **runnable** | **str**| Runnable indicates that this is Runnable. | [optional] 
 **stage** | **str**| The stage that this is currently in. | [optional] 
 **start_time** | **str**| StartTime The time the async action started running. | [optional] 
 **state** | **str**| State The state the async action is in.  Must be one of \&quot;created\&quot;, \&quot;running\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;cancelled\&quot; | [optional] 
 **status** | **str**| Status is a short text snippet for humans explaining the current state. | [optional] 
 **task_error_stacks** | **str**| This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. | [optional] 
 **tasks** | **str**| The current tasks that are being processed. | [optional] 
 **uuid** | [**str**](.md)| Uuid is the key of this particular WorkOrder. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_work_orders**
> list[WorkOrder] list_work_orders(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, archived=archived, available=available, blueprint=blueprint, bundle=bundle, context=context, create_time=create_time, created_at=created_at, created_by=created_by, current_job=current_job, current_task=current_task, end_time=end_time, endpoint=endpoint, errors=errors, filter2=filter2, job_exit_state=job_exit_state, job_result_errors=job_result_errors, job_state=job_state, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine=machine, meta=meta, params2=params2, profiles=profiles, read_only=read_only, retry_task_attempt=retry_task_attempt, runnable=runnable, stage=stage, start_time=start_time, state=state, status=status, task_error_stacks=task_error_stacks, tasks=tasks, uuid=uuid, validated=validated)

Lists WorkOrders filtered by some parameters.

This will show all WorkOrders by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Uuid=fred - returns items named fred<br/> Uuid=Lt(fred) - returns items that alphabetically less than fred.<br/> Uuid=Lt(fred)&Available=true - returns items with Uuid less than fred and Available is true<br/>

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
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
archived = 'archived_example' # str | Archived indicates whether the complete log for the async action can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
blueprint = 'blueprint_example' # str | Blueprint defines the tasks and base parameters for this action (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
context = 'context_example' # str | Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. (optional)
create_time = 'create_time_example' # str | CreateTime is the time the work order was created.  This is distinct from StartTime, as there may be a significant delay before the workorder starts running. (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
current_job = 'current_job_example' # str | The UUID of the job that is currently running. (optional)
current_task = 'current_task_example' # str | The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. (optional)
end_time = 'end_time_example' # str | EndTime The time the async action failed or finished or cancelled. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
filter2 = 'filter_example' # str | Filter is a list filter for this WorkOrder (optional)
job_exit_state = 'job_exit_state_example' # str | The final disposition of the current job. Can be one of \"reboot\",\"poweroff\",\"stop\", or \"complete\" Other substates may be added as time goes on (optional)
job_result_errors = 'job_result_errors_example' # str | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. (optional)
job_state = 'job_state_example' # str | The state the current job is in.  Must be one of \"created\", \"failed\", \"finished\", \"incomplete\" (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
machine = 'machine_example' # str | Machine is the key of the machine running the WorkOrder (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
params2 = 'params_example' # str | Params that have been directly set on the Machine. (optional)
profiles = 'profiles_example' # str | Profiles An array of profiles to apply to this machine in order when looking for a parameter during rendering. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
retry_task_attempt = 'retry_task_attempt_example' # str | This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. (optional)
runnable = 'runnable_example' # str | Runnable indicates that this is Runnable. (optional)
stage = 'stage_example' # str | The stage that this is currently in. (optional)
start_time = 'start_time_example' # str | StartTime The time the async action started running. (optional)
state = 'state_example' # str | State The state the async action is in.  Must be one of \"created\", \"running\", \"failed\", \"finished\", \"cancelled\" (optional)
status = 'status_example' # str | Status is a short text snippet for humans explaining the current state. (optional)
task_error_stacks = 'task_error_stacks_example' # str | This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. (optional)
tasks = 'tasks_example' # str | The current tasks that are being processed. (optional)
uuid = 'uuid_example' # str | Uuid is the key of this particular WorkOrder. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Lists WorkOrders filtered by some parameters.
    api_response = api_instance.list_work_orders(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, archived=archived, available=available, blueprint=blueprint, bundle=bundle, context=context, create_time=create_time, created_at=created_at, created_by=created_by, current_job=current_job, current_task=current_task, end_time=end_time, endpoint=endpoint, errors=errors, filter2=filter2, job_exit_state=job_exit_state, job_result_errors=job_result_errors, job_state=job_state, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine=machine, meta=meta, params2=params2, profiles=profiles, read_only=read_only, retry_task_attempt=retry_task_attempt, runnable=runnable, stage=stage, start_time=start_time, state=state, status=status, task_error_stacks=task_error_stacks, tasks=tasks, uuid=uuid, validated=validated)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->list_work_orders: %s\n" % e)
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
 **archived** | **str**| Archived indicates whether the complete log for the async action can be retrieved via the API.  If Archived is true, then the log cannot be retrieved. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **blueprint** | **str**| Blueprint defines the tasks and base parameters for this action | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **context** | **str**| Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. | [optional] 
 **create_time** | **str**| CreateTime is the time the work order was created.  This is distinct from StartTime, as there may be a significant delay before the workorder starts running. | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **current_job** | [**str**](.md)| The UUID of the job that is currently running. | [optional] 
 **current_task** | **str**| The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. | [optional] 
 **end_time** | **str**| EndTime The time the async action failed or finished or cancelled. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **filter2** | **str**| Filter is a list filter for this WorkOrder | [optional] 
 **job_exit_state** | **str**| The final disposition of the current job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
 **job_result_errors** | **str**| ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
 **job_state** | **str**| The state the current job is in.  Must be one of \&quot;created\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **machine** | [**str**](.md)| Machine is the key of the machine running the WorkOrder | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **params2** | **str**| Params that have been directly set on the Machine. | [optional] 
 **profiles** | **str**| Profiles An array of profiles to apply to this machine in order when looking for a parameter during rendering. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **retry_task_attempt** | **str**| This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. | [optional] 
 **runnable** | **str**| Runnable indicates that this is Runnable. | [optional] 
 **stage** | **str**| The stage that this is currently in. | [optional] 
 **start_time** | **str**| StartTime The time the async action started running. | [optional] 
 **state** | **str**| State The state the async action is in.  Must be one of \&quot;created\&quot;, \&quot;running\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;cancelled\&quot; | [optional] 
 **status** | **str**| Status is a short text snippet for humans explaining the current state. | [optional] 
 **task_error_stacks** | **str**| This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. | [optional] 
 **tasks** | **str**| The current tasks that are being processed. | [optional] 
 **uuid** | [**str**](.md)| Uuid is the key of this particular WorkOrder. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

[**list[WorkOrder]**](WorkOrder.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_work_order**
> WorkOrder patch_work_order(body, uuid, force=force, commented=commented, reduced=reduced)

Patch a WorkOrder

Update a WorkOrder specified by {uuid} using a RFC6902 Patch structure

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
uuid = 'uuid_example' # str | Identity key of the WorkOrder
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a WorkOrder
    api_response = api_instance.patch_work_order(body, uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->patch_work_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**WorkOrder**](WorkOrder.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_work_order_params**
> dict(str, object) patch_work_order_params(body, uuid)

Update all params on the object (merges with existing data)

Update params for WorkOrder {uuid} with the passed-in patch

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
uuid = 'uuid_example' # str | Identity key of the WorkOrder

try:
    # Update all params on the object (merges with existing data)
    api_response = api_instance.patch_work_order_params(body, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->patch_work_order_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_work_order_action**
> object post_work_order_action(uuid, cmd, body, plugin=plugin)

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the WorkOrder
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_work_order_action(uuid, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->post_work_order_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
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

# **post_work_order_param**
> object post_work_order_param(body, uuid, key)

Set a single parameter on an object

Set as single Parameter {key} for a work_orders specified by {uuid}

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 
uuid = 'uuid_example' # str | Identity key of the WorkOrder
key = 'key_example' # str | Param name

try:
    # Set a single parameter on an object
    api_response = api_instance.post_work_order_param(body, uuid, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->post_work_order_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
 **key** | **str**| Param name | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_work_order_params**
> dict(str, object) post_work_order_params(body)

Replaces all parameters on the object

Sets parameters for a work_orders specified by {uuid}

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 

try:
    # Replaces all parameters on the object
    api_response = api_instance.post_work_order_params(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->post_work_order_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_work_order**
> WorkOrder put_work_order(body, uuid, force=force, commented=commented, reduced=reduced)

Put a WorkOrder

Update a WorkOrder specified by {uuid} using a JSON WorkOrder

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
api_instance = drppy_client.WorkOrdersApi(drppy_client.ApiClient(configuration))
body = drppy_client.WorkOrder() # WorkOrder | 
uuid = 'uuid_example' # str | Identity key of the WorkOrder
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a WorkOrder
    api_response = api_instance.put_work_order(body, uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkOrdersApi->put_work_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WorkOrder**](WorkOrder.md)|  | 
 **uuid** | [**str**](.md)| Identity key of the WorkOrder | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**WorkOrder**](WorkOrder.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

