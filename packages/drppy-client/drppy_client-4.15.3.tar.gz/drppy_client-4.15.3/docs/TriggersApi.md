# drppy_client.TriggersApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_trigger**](TriggersApi.md#create_trigger) | **POST** /triggers | Create a Trigger
[**delete_trigger**](TriggersApi.md#delete_trigger) | **DELETE** /triggers/{name} | Delete a Trigger
[**delete_trigger_param**](TriggersApi.md#delete_trigger_param) | **DELETE** /triggers/{name}/params/{key} | Delete a single triggers parameter
[**get_trigger**](TriggersApi.md#get_trigger) | **GET** /triggers/{name} | Get a Trigger
[**get_trigger_action**](TriggersApi.md#get_trigger_action) | **GET** /triggers/{name}/actions/{cmd} | List specific action for a triggers Trigger
[**get_trigger_actions**](TriggersApi.md#get_trigger_actions) | **GET** /triggers/{name}/actions | List triggers actions Trigger
[**get_trigger_param**](TriggersApi.md#get_trigger_param) | **GET** /triggers/{name}/params/{key} | Get a single triggers parameter
[**get_trigger_params**](TriggersApi.md#get_trigger_params) | **GET** /triggers/{name}/params | List triggers params Trigger
[**get_trigger_pub_key**](TriggersApi.md#get_trigger_pub_key) | **GET** /triggers/{name}/pubkey | Get the public key for secure params on a triggers
[**head_trigger**](TriggersApi.md#head_trigger) | **HEAD** /triggers/{name} | See if a Trigger exists
[**list_stats_triggers**](TriggersApi.md#list_stats_triggers) | **HEAD** /triggers | Stats of the List Triggers filtered by some parameters.
[**list_triggers**](TriggersApi.md#list_triggers) | **GET** /triggers | Lists Triggers filtered by some parameters.
[**patch_trigger**](TriggersApi.md#patch_trigger) | **PATCH** /triggers/{name} | Patch a Trigger
[**patch_trigger_params**](TriggersApi.md#patch_trigger_params) | **PATCH** /triggers/{name}/params | Update all params on the object (merges with existing data)
[**post_trigger_action**](TriggersApi.md#post_trigger_action) | **POST** /triggers/{name}/actions/{cmd} | Call an action on the node.
[**post_trigger_param**](TriggersApi.md#post_trigger_param) | **POST** /triggers/{name}/params/{key} | Set a single parameter on an object
[**post_trigger_params**](TriggersApi.md#post_trigger_params) | **POST** /triggers/{name}/params | Replaces all parameters on the object
[**put_trigger**](TriggersApi.md#put_trigger) | **PUT** /triggers/{name} | Put a Trigger


# **create_trigger**
> Trigger create_trigger(body)

Create a Trigger

Create a Trigger from the provided object

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Trigger() # Trigger | 

try:
    # Create a Trigger
    api_response = api_instance.create_trigger(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->create_trigger: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Trigger**](Trigger.md)|  | 

### Return type

[**Trigger**](Trigger.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_trigger**
> Trigger delete_trigger(name, force=force, commented=commented, reduced=reduced)

Delete a Trigger

Delete a Trigger specified by {name}

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a Trigger
    api_response = api_instance.delete_trigger(name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->delete_trigger: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Trigger**](Trigger.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_trigger_param**
> object delete_trigger_param()

Delete a single triggers parameter

Delete a single parameter {key} for a Trigger specified by {name}

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))

try:
    # Delete a single triggers parameter
    api_response = api_instance.delete_trigger_param()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->delete_trigger_param: %s\n" % e)
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

# **get_trigger**
> Trigger get_trigger(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a Trigger

Get the Trigger specified by {name}  or return NotFound.

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a Trigger
    api_response = api_instance.get_trigger(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->get_trigger: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Trigger**](Trigger.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trigger_action**
> AvailableAction get_trigger_action(name, cmd, plugin=plugin)

List specific action for a triggers Trigger

List specific {cmd} action for a Trigger specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a triggers Trigger
    api_response = api_instance.get_trigger_action(name, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->get_trigger_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 
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

# **get_trigger_actions**
> list[AvailableAction] get_trigger_actions(name, plugin=plugin)

List triggers actions Trigger

List Trigger actions for a Trigger specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List triggers actions Trigger
    api_response = api_instance.get_trigger_actions(name, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->get_trigger_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trigger_param**
> object get_trigger_param(name, key, aggregate=aggregate, decode=decode)

Get a single triggers parameter

Get a single parameter {key} for a Trigger specified by {name}

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger
key = 'key_example' # str | Param name
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)

try:
    # Get a single triggers parameter
    api_response = api_instance.get_trigger_param(name, key, aggregate=aggregate, decode=decode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->get_trigger_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 
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

# **get_trigger_params**
> dict(str, object) get_trigger_params(name, aggregate=aggregate, decode=decode, params=params)

List triggers params Trigger

List Trigger parms for a Trigger specified by {name}

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
params = 'params_example' # str |  (optional)

try:
    # List triggers params Trigger
    api_response = api_instance.get_trigger_params(name, aggregate=aggregate, decode=decode, params=params)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->get_trigger_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 
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

# **get_trigger_pub_key**
> get_trigger_pub_key(name)

Get the public key for secure params on a triggers

Get the public key for a Trigger specified by {name}

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger

try:
    # Get the public key for secure params on a triggers
    api_instance.get_trigger_pub_key(name)
except ApiException as e:
    print("Exception when calling TriggersApi->get_trigger_pub_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_trigger**
> head_trigger(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a Trigger exists

Return 200 if the Trigger specifiec by {name} exists, or return NotFound.

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a Trigger exists
    api_instance.head_trigger(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling TriggersApi->head_trigger: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 
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

# **list_stats_triggers**
> list_stats_triggers(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, all_in_filter=all_in_filter, available=available, blueprint=blueprint, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, enabled=enabled, endpoint=endpoint, errors=errors, filter2=filter2, filter_count=filter_count, last_modified_at=last_modified_at, last_modified_by=last_modified_by, merge_data_into_params=merge_data_into_params, meta=meta, name=name, params2=params2, profiles=profiles, queue_mode=queue_mode, read_only=read_only, store_data_in_parameter=store_data_in_parameter, trigger_provider=trigger_provider, validated=validated, work_order_params=work_order_params, work_order_profiles=work_order_profiles)

Stats of the List Triggers filtered by some parameters.

This will return headers with the stats of the list.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> range-only = returns only counts of the objects in the groups.<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
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
all_in_filter = 'all_in_filter_example' # str | AllInFilter if true cause a work_order created for all machines in the filter (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
blueprint = 'blueprint_example' # str | Blueprint is template to apply (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
enabled = 'enabled_example' # str | Enabled is this Trigger enabled (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
filter2 = 'filter_example' # str | Filter is a \"list\"-style filter string to find machines to apply the cron too Filter is already assumed to have WorkOrderMode == true && Runnable == true (optional)
filter_count = 'filter_count_example' # str | FilterCount defines the number of machines to apply the work_order to.  Only one work_order per trigger fire. (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
merge_data_into_params = 'merge_data_into_params_example' # str | MergeDataIntoParams if true causes the data from the trigger to be merged into the Params of the work_order. (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | Name is the key of this particular Trigger. (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
profiles = 'profiles_example' # str | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. (optional)
queue_mode = 'queue_mode_example' # str | QueueMode if true causes work_orders to be created without a machine, but with a filter for delayed operation (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
store_data_in_parameter = 'store_data_in_parameter_example' # str | StoreDataInParameter if set tells the triggers data to be stored in the parameter in the Params of the work_order. (optional)
trigger_provider = 'trigger_provider_example' # str | TriggerProvider is the name of the method of this trigger (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)
work_order_params = 'work_order_params_example' # str | WorkOrderParams that have been directly set on the Trigger and will be moved to the work order. (optional)
work_order_profiles = 'work_order_profiles_example' # str | WorkOrderProfiles to apply to this machine in order when looking for a parameter during rendering. (optional)

try:
    # Stats of the List Triggers filtered by some parameters.
    api_instance.list_stats_triggers(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, all_in_filter=all_in_filter, available=available, blueprint=blueprint, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, enabled=enabled, endpoint=endpoint, errors=errors, filter2=filter2, filter_count=filter_count, last_modified_at=last_modified_at, last_modified_by=last_modified_by, merge_data_into_params=merge_data_into_params, meta=meta, name=name, params2=params2, profiles=profiles, queue_mode=queue_mode, read_only=read_only, store_data_in_parameter=store_data_in_parameter, trigger_provider=trigger_provider, validated=validated, work_order_params=work_order_params, work_order_profiles=work_order_profiles)
except ApiException as e:
    print("Exception when calling TriggersApi->list_stats_triggers: %s\n" % e)
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
 **all_in_filter** | **str**| AllInFilter if true cause a work_order created for all machines in the filter | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **blueprint** | **str**| Blueprint is template to apply | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **enabled** | **str**| Enabled is this Trigger enabled | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **filter2** | **str**| Filter is a \&quot;list\&quot;-style filter string to find machines to apply the cron too Filter is already assumed to have WorkOrderMode &#x3D;&#x3D; true &amp;&amp; Runnable &#x3D;&#x3D; true | [optional] 
 **filter_count** | **str**| FilterCount defines the number of machines to apply the work_order to.  Only one work_order per trigger fire. | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **merge_data_into_params** | **str**| MergeDataIntoParams if true causes the data from the trigger to be merged into the Params of the work_order. | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| Name is the key of this particular Trigger. | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **profiles** | **str**| Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
 **queue_mode** | **str**| QueueMode if true causes work_orders to be created without a machine, but with a filter for delayed operation | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **store_data_in_parameter** | **str**| StoreDataInParameter if set tells the triggers data to be stored in the parameter in the Params of the work_order. | [optional] 
 **trigger_provider** | **str**| TriggerProvider is the name of the method of this trigger | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 
 **work_order_params** | **str**| WorkOrderParams that have been directly set on the Trigger and will be moved to the work order. | [optional] 
 **work_order_profiles** | **str**| WorkOrderProfiles to apply to this machine in order when looking for a parameter during rendering. | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_triggers**
> list[Trigger] list_triggers(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, all_in_filter=all_in_filter, available=available, blueprint=blueprint, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, enabled=enabled, endpoint=endpoint, errors=errors, filter2=filter2, filter_count=filter_count, last_modified_at=last_modified_at, last_modified_by=last_modified_by, merge_data_into_params=merge_data_into_params, meta=meta, name=name, params2=params2, profiles=profiles, queue_mode=queue_mode, read_only=read_only, store_data_in_parameter=store_data_in_parameter, trigger_provider=trigger_provider, validated=validated, work_order_params=work_order_params, work_order_profiles=work_order_profiles)

Lists Triggers filtered by some parameters.

This will show all Triggers by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
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
all_in_filter = 'all_in_filter_example' # str | AllInFilter if true cause a work_order created for all machines in the filter (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
blueprint = 'blueprint_example' # str | Blueprint is template to apply (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
enabled = 'enabled_example' # str | Enabled is this Trigger enabled (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
filter2 = 'filter_example' # str | Filter is a \"list\"-style filter string to find machines to apply the cron too Filter is already assumed to have WorkOrderMode == true && Runnable == true (optional)
filter_count = 'filter_count_example' # str | FilterCount defines the number of machines to apply the work_order to.  Only one work_order per trigger fire. (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
merge_data_into_params = 'merge_data_into_params_example' # str | MergeDataIntoParams if true causes the data from the trigger to be merged into the Params of the work_order. (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | Name is the key of this particular Trigger. (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
profiles = 'profiles_example' # str | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. (optional)
queue_mode = 'queue_mode_example' # str | QueueMode if true causes work_orders to be created without a machine, but with a filter for delayed operation (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
store_data_in_parameter = 'store_data_in_parameter_example' # str | StoreDataInParameter if set tells the triggers data to be stored in the parameter in the Params of the work_order. (optional)
trigger_provider = 'trigger_provider_example' # str | TriggerProvider is the name of the method of this trigger (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)
work_order_params = 'work_order_params_example' # str | WorkOrderParams that have been directly set on the Trigger and will be moved to the work order. (optional)
work_order_profiles = 'work_order_profiles_example' # str | WorkOrderProfiles to apply to this machine in order when looking for a parameter during rendering. (optional)

try:
    # Lists Triggers filtered by some parameters.
    api_response = api_instance.list_triggers(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, all_in_filter=all_in_filter, available=available, blueprint=blueprint, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, enabled=enabled, endpoint=endpoint, errors=errors, filter2=filter2, filter_count=filter_count, last_modified_at=last_modified_at, last_modified_by=last_modified_by, merge_data_into_params=merge_data_into_params, meta=meta, name=name, params2=params2, profiles=profiles, queue_mode=queue_mode, read_only=read_only, store_data_in_parameter=store_data_in_parameter, trigger_provider=trigger_provider, validated=validated, work_order_params=work_order_params, work_order_profiles=work_order_profiles)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->list_triggers: %s\n" % e)
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
 **all_in_filter** | **str**| AllInFilter if true cause a work_order created for all machines in the filter | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **blueprint** | **str**| Blueprint is template to apply | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **enabled** | **str**| Enabled is this Trigger enabled | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **filter2** | **str**| Filter is a \&quot;list\&quot;-style filter string to find machines to apply the cron too Filter is already assumed to have WorkOrderMode &#x3D;&#x3D; true &amp;&amp; Runnable &#x3D;&#x3D; true | [optional] 
 **filter_count** | **str**| FilterCount defines the number of machines to apply the work_order to.  Only one work_order per trigger fire. | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **merge_data_into_params** | **str**| MergeDataIntoParams if true causes the data from the trigger to be merged into the Params of the work_order. | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| Name is the key of this particular Trigger. | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **profiles** | **str**| Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
 **queue_mode** | **str**| QueueMode if true causes work_orders to be created without a machine, but with a filter for delayed operation | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **store_data_in_parameter** | **str**| StoreDataInParameter if set tells the triggers data to be stored in the parameter in the Params of the work_order. | [optional] 
 **trigger_provider** | **str**| TriggerProvider is the name of the method of this trigger | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 
 **work_order_params** | **str**| WorkOrderParams that have been directly set on the Trigger and will be moved to the work order. | [optional] 
 **work_order_profiles** | **str**| WorkOrderProfiles to apply to this machine in order when looking for a parameter during rendering. | [optional] 

### Return type

[**list[Trigger]**](Trigger.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_trigger**
> Trigger patch_trigger(body, name, force=force, commented=commented, reduced=reduced)

Patch a Trigger

Update a Trigger specified by {name} using a RFC6902 Patch structure

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
name = 'name_example' # str | Identity key of the Trigger
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a Trigger
    api_response = api_instance.patch_trigger(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->patch_trigger: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **name** | **str**| Identity key of the Trigger | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Trigger**](Trigger.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_trigger_params**
> dict(str, object) patch_trigger_params(body, name)

Update all params on the object (merges with existing data)

Update params for Trigger {name} with the passed-in patch

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
name = 'name_example' # str | Identity key of the Trigger

try:
    # Update all params on the object (merges with existing data)
    api_response = api_instance.patch_trigger_params(body, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->patch_trigger_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **name** | **str**| Identity key of the Trigger | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_trigger_action**
> object post_trigger_action(name, cmd, body, plugin=plugin)

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Trigger
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_trigger_action(name, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->post_trigger_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Trigger | 
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

# **post_trigger_param**
> object post_trigger_param(body, name, key)

Set a single parameter on an object

Set as single Parameter {key} for a triggers specified by {name}

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 
name = 'name_example' # str | Identity key of the Trigger
key = 'key_example' # str | Param name

try:
    # Set a single parameter on an object
    api_response = api_instance.post_trigger_param(body, name, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->post_trigger_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 
 **name** | **str**| Identity key of the Trigger | 
 **key** | **str**| Param name | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_trigger_params**
> dict(str, object) post_trigger_params(body)

Replaces all parameters on the object

Sets parameters for a triggers specified by {name}

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 

try:
    # Replaces all parameters on the object
    api_response = api_instance.post_trigger_params(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->post_trigger_params: %s\n" % e)
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

# **put_trigger**
> Trigger put_trigger(body, name, force=force, commented=commented, reduced=reduced)

Put a Trigger

Update a Trigger specified by {name} using a JSON Trigger

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
api_instance = drppy_client.TriggersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Trigger() # Trigger | 
name = 'name_example' # str | Identity key of the Trigger
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a Trigger
    api_response = api_instance.put_trigger(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TriggersApi->put_trigger: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Trigger**](Trigger.md)|  | 
 **name** | **str**| Identity key of the Trigger | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Trigger**](Trigger.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

