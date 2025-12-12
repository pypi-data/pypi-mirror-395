# drppy_client.FiltersApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_filter**](FiltersApi.md#create_filter) | **POST** /filters | Create a Filter
[**delete_filter**](FiltersApi.md#delete_filter) | **DELETE** /filters/{id} | Delete a Filter
[**delete_filter_param**](FiltersApi.md#delete_filter_param) | **DELETE** /filters/{id}/params/{key} | Delete a single filters parameter
[**get_filter**](FiltersApi.md#get_filter) | **GET** /filters/{id} | Get a Filter
[**get_filter_action**](FiltersApi.md#get_filter_action) | **GET** /filters/{id}/actions/{cmd} | List specific action for a filters Filter
[**get_filter_actions**](FiltersApi.md#get_filter_actions) | **GET** /filters/{id}/actions | List filters actions Filter
[**get_filter_param**](FiltersApi.md#get_filter_param) | **GET** /filters/{id}/params/{key} | Get a single filters parameter
[**get_filter_params**](FiltersApi.md#get_filter_params) | **GET** /filters/{id}/params | List filters params Filter
[**get_filter_pub_key**](FiltersApi.md#get_filter_pub_key) | **GET** /filters/{id}/pubkey | Get the public key for secure params on a filters
[**head_filter**](FiltersApi.md#head_filter) | **HEAD** /filters/{id} | See if a Filter exists
[**list_filters**](FiltersApi.md#list_filters) | **GET** /filters | Lists Filters filtered by some parameters.
[**list_stats_filters**](FiltersApi.md#list_stats_filters) | **HEAD** /filters | Stats of the List Filters filtered by some parameters.
[**patch_filter**](FiltersApi.md#patch_filter) | **PATCH** /filters/{id} | Patch a Filter
[**patch_filter_params**](FiltersApi.md#patch_filter_params) | **PATCH** /filters/{id}/params | Update all params on the object (merges with existing data)
[**post_filter_action**](FiltersApi.md#post_filter_action) | **POST** /filters/{id}/actions/{cmd} | Call an action on the node.
[**post_filter_param**](FiltersApi.md#post_filter_param) | **POST** /filters/{id}/params/{key} | Set a single parameter on an object
[**post_filter_params**](FiltersApi.md#post_filter_params) | **POST** /filters/{id}/params | Replaces all parameters on the object
[**put_filter**](FiltersApi.md#put_filter) | **PUT** /filters/{id} | Put a Filter


# **create_filter**
> Filter create_filter(body)

Create a Filter

Create a Filter from the provided object

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Filter() # Filter | 

try:
    # Create a Filter
    api_response = api_instance.create_filter(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->create_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Filter**](Filter.md)|  | 

### Return type

[**Filter**](Filter.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_filter**
> Filter delete_filter(id, force=force, commented=commented, reduced=reduced)

Delete a Filter

Delete a Filter specified by {id}

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a Filter
    api_response = api_instance.delete_filter(id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->delete_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Filter**](Filter.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_filter_param**
> object delete_filter_param()

Delete a single filters parameter

Delete a single parameter {key} for a Filter specified by {id}

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))

try:
    # Delete a single filters parameter
    api_response = api_instance.delete_filter_param()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->delete_filter_param: %s\n" % e)
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

# **get_filter**
> Filter get_filter(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a Filter

Get the Filter specified by {id}  or return NotFound.

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a Filter
    api_response = api_instance.get_filter(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->get_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Filter**](Filter.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_filter_action**
> AvailableAction get_filter_action(id, cmd, plugin=plugin)

List specific action for a filters Filter

List specific {cmd} action for a Filter specified by {id}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a filters Filter
    api_response = api_instance.get_filter_action(id, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->get_filter_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 
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

# **get_filter_actions**
> list[AvailableAction] get_filter_actions(id, plugin=plugin)

List filters actions Filter

List Filter actions for a Filter specified by {id}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List filters actions Filter
    api_response = api_instance.get_filter_actions(id, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->get_filter_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_filter_param**
> object get_filter_param(id, key, aggregate=aggregate, decode=decode)

Get a single filters parameter

Get a single parameter {key} for a Filter specified by {id}

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter
key = 'key_example' # str | Param name
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)

try:
    # Get a single filters parameter
    api_response = api_instance.get_filter_param(id, key, aggregate=aggregate, decode=decode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->get_filter_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 
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

# **get_filter_params**
> dict(str, object) get_filter_params(id, aggregate=aggregate, decode=decode, params=params)

List filters params Filter

List Filter parms for a Filter specified by {id}

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
params = 'params_example' # str |  (optional)

try:
    # List filters params Filter
    api_response = api_instance.get_filter_params(id, aggregate=aggregate, decode=decode, params=params)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->get_filter_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 
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

# **get_filter_pub_key**
> get_filter_pub_key(id)

Get the public key for secure params on a filters

Get the public key for a Filter specified by {id}

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter

try:
    # Get the public key for secure params on a filters
    api_instance.get_filter_pub_key(id)
except ApiException as e:
    print("Exception when calling FiltersApi->get_filter_pub_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_filter**
> head_filter(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a Filter exists

Return 200 if the Filter specifiec by {id} exists, or return NotFound.

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a Filter exists
    api_instance.head_filter(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling FiltersApi->head_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 
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

# **list_filters**
> list[Filter] list_filters(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, aggregate2=aggregate2, available=available, bundle=bundle, created_at=created_at, created_by=created_by, decode2=decode2, description=description, documentation=documentation, endpoint=endpoint, errors=errors, exclude_self=exclude_self, group_by2=group_by2, id=id, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, object=object, param_set=param_set, params2=params2, queries=queries, range_only2=range_only2, read_only=read_only, reduced2=reduced2, reverse2=reverse2, slim2=slim2, sort2=sort2, validated=validated)

Lists Filters filtered by some parameters.

This will show all Filters by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Id=fred - returns items named fred<br/> Id=Lt(fred) - returns items that alphabetically less than fred.<br/> Id=Lt(fred)&Available=true - returns items with Id less than fred and Available is true<br/>

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
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
aggregate2 = 'aggregate_example' # str | Aggregate indicates if parameters should be aggregate for search and return (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
decode2 = 'decode_example' # str | Decode indicates if the parameters should be decoded before returning the object (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
exclude_self = 'exclude_self_example' # str | ExcludeSelf removes self runners from the list (machines/clusters/resource_brokers) (optional)
group_by2 = 'group_by_example' # str | GroupBy is a list of Fields or Parameters to generate groups of objects in a return list. (optional)
id = 'id_example' # str | Id is the Name of the Filter (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
object = 'object_example' # str | Object is the name of the set of objects this filter applies to. (optional)
param_set = 'param_set_example' # str | ParamSet defines a comma-separated list of Fields or Parameters to return (can be complex functions) (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
queries = 'queries_example' # str | Queries are the tests to apply to the machine. (optional)
range_only2 = 'range_only_example' # str | RangeOnly indicates that counts should be returned of group-bys and no objects. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
reduced2 = 'reduced_example' # str | Reduced indicates if the objects should have ReadOnly fields removed (optional)
reverse2 = 'reverse_example' # str | Reverse the returned list (optional)
slim2 = 'slim_example' # str | Slim defines if meta, params, or specific parameters should be excluded from the object (optional)
sort2 = 'sort_example' # str | Sort is a list of fields / parameters that should scope the list (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Lists Filters filtered by some parameters.
    api_response = api_instance.list_filters(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, aggregate2=aggregate2, available=available, bundle=bundle, created_at=created_at, created_by=created_by, decode2=decode2, description=description, documentation=documentation, endpoint=endpoint, errors=errors, exclude_self=exclude_self, group_by2=group_by2, id=id, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, object=object, param_set=param_set, params2=params2, queries=queries, range_only2=range_only2, read_only=read_only, reduced2=reduced2, reverse2=reverse2, slim2=slim2, sort2=sort2, validated=validated)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->list_filters: %s\n" % e)
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
 **aggregate2** | **str**| Aggregate indicates if parameters should be aggregate for search and return | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **decode2** | **str**| Decode indicates if the parameters should be decoded before returning the object | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **exclude_self** | **str**| ExcludeSelf removes self runners from the list (machines/clusters/resource_brokers) | [optional] 
 **group_by2** | **str**| GroupBy is a list of Fields or Parameters to generate groups of objects in a return list. | [optional] 
 **id** | **str**| Id is the Name of the Filter | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **object** | **str**| Object is the name of the set of objects this filter applies to. | [optional] 
 **param_set** | **str**| ParamSet defines a comma-separated list of Fields or Parameters to return (can be complex functions) | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **queries** | **str**| Queries are the tests to apply to the machine. | [optional] 
 **range_only2** | **str**| RangeOnly indicates that counts should be returned of group-bys and no objects. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **reduced2** | **str**| Reduced indicates if the objects should have ReadOnly fields removed | [optional] 
 **reverse2** | **str**| Reverse the returned list | [optional] 
 **slim2** | **str**| Slim defines if meta, params, or specific parameters should be excluded from the object | [optional] 
 **sort2** | **str**| Sort is a list of fields / parameters that should scope the list | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

[**list[Filter]**](Filter.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_stats_filters**
> list_stats_filters(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, aggregate2=aggregate2, available=available, bundle=bundle, created_at=created_at, created_by=created_by, decode2=decode2, description=description, documentation=documentation, endpoint=endpoint, errors=errors, exclude_self=exclude_self, group_by2=group_by2, id=id, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, object=object, param_set=param_set, params2=params2, queries=queries, range_only2=range_only2, read_only=read_only, reduced2=reduced2, reverse2=reverse2, slim2=slim2, sort2=sort2, validated=validated)

Stats of the List Filters filtered by some parameters.

This will return headers with the stats of the list.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> range-only = returns only counts of the objects in the groups.<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Id=fred - returns items named fred<br/> Id=Lt(fred) - returns items that alphabetically less than fred.<br/> Id=Lt(fred)&Available=true - returns items with Id less than fred and Available is true<br/>

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
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
aggregate2 = 'aggregate_example' # str | Aggregate indicates if parameters should be aggregate for search and return (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
decode2 = 'decode_example' # str | Decode indicates if the parameters should be decoded before returning the object (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
exclude_self = 'exclude_self_example' # str | ExcludeSelf removes self runners from the list (machines/clusters/resource_brokers) (optional)
group_by2 = 'group_by_example' # str | GroupBy is a list of Fields or Parameters to generate groups of objects in a return list. (optional)
id = 'id_example' # str | Id is the Name of the Filter (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
object = 'object_example' # str | Object is the name of the set of objects this filter applies to. (optional)
param_set = 'param_set_example' # str | ParamSet defines a comma-separated list of Fields or Parameters to return (can be complex functions) (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
queries = 'queries_example' # str | Queries are the tests to apply to the machine. (optional)
range_only2 = 'range_only_example' # str | RangeOnly indicates that counts should be returned of group-bys and no objects. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
reduced2 = 'reduced_example' # str | Reduced indicates if the objects should have ReadOnly fields removed (optional)
reverse2 = 'reverse_example' # str | Reverse the returned list (optional)
slim2 = 'slim_example' # str | Slim defines if meta, params, or specific parameters should be excluded from the object (optional)
sort2 = 'sort_example' # str | Sort is a list of fields / parameters that should scope the list (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Stats of the List Filters filtered by some parameters.
    api_instance.list_stats_filters(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, aggregate2=aggregate2, available=available, bundle=bundle, created_at=created_at, created_by=created_by, decode2=decode2, description=description, documentation=documentation, endpoint=endpoint, errors=errors, exclude_self=exclude_self, group_by2=group_by2, id=id, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, object=object, param_set=param_set, params2=params2, queries=queries, range_only2=range_only2, read_only=read_only, reduced2=reduced2, reverse2=reverse2, slim2=slim2, sort2=sort2, validated=validated)
except ApiException as e:
    print("Exception when calling FiltersApi->list_stats_filters: %s\n" % e)
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
 **aggregate2** | **str**| Aggregate indicates if parameters should be aggregate for search and return | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **decode2** | **str**| Decode indicates if the parameters should be decoded before returning the object | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **exclude_self** | **str**| ExcludeSelf removes self runners from the list (machines/clusters/resource_brokers) | [optional] 
 **group_by2** | **str**| GroupBy is a list of Fields or Parameters to generate groups of objects in a return list. | [optional] 
 **id** | **str**| Id is the Name of the Filter | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **object** | **str**| Object is the name of the set of objects this filter applies to. | [optional] 
 **param_set** | **str**| ParamSet defines a comma-separated list of Fields or Parameters to return (can be complex functions) | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **queries** | **str**| Queries are the tests to apply to the machine. | [optional] 
 **range_only2** | **str**| RangeOnly indicates that counts should be returned of group-bys and no objects. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **reduced2** | **str**| Reduced indicates if the objects should have ReadOnly fields removed | [optional] 
 **reverse2** | **str**| Reverse the returned list | [optional] 
 **slim2** | **str**| Slim defines if meta, params, or specific parameters should be excluded from the object | [optional] 
 **sort2** | **str**| Sort is a list of fields / parameters that should scope the list | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_filter**
> Filter patch_filter(body, id, force=force, commented=commented, reduced=reduced)

Patch a Filter

Update a Filter specified by {id} using a RFC6902 Patch structure

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
id = 'id_example' # str | Identity key of the Filter
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a Filter
    api_response = api_instance.patch_filter(body, id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->patch_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **id** | **str**| Identity key of the Filter | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Filter**](Filter.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_filter_params**
> dict(str, object) patch_filter_params(body, id)

Update all params on the object (merges with existing data)

Update params for Filter {id} with the passed-in patch

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
id = 'id_example' # str | Identity key of the Filter

try:
    # Update all params on the object (merges with existing data)
    api_response = api_instance.patch_filter_params(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->patch_filter_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **id** | **str**| Identity key of the Filter | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_filter_action**
> object post_filter_action(id, cmd, body, plugin=plugin)

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the Filter
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_filter_action(id, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->post_filter_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the Filter | 
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

# **post_filter_param**
> object post_filter_param(body, id, key)

Set a single parameter on an object

Set as single Parameter {key} for a filters specified by {id}

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 
id = 'id_example' # str | Identity key of the Filter
key = 'key_example' # str | Param name

try:
    # Set a single parameter on an object
    api_response = api_instance.post_filter_param(body, id, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->post_filter_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 
 **id** | **str**| Identity key of the Filter | 
 **key** | **str**| Param name | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_filter_params**
> dict(str, object) post_filter_params(body)

Replaces all parameters on the object

Sets parameters for a filters specified by {id}

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 

try:
    # Replaces all parameters on the object
    api_response = api_instance.post_filter_params(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->post_filter_params: %s\n" % e)
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

# **put_filter**
> Filter put_filter(body, id, force=force, commented=commented, reduced=reduced)

Put a Filter

Update a Filter specified by {id} using a JSON Filter

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
api_instance = drppy_client.FiltersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Filter() # Filter | 
id = 'id_example' # str | Identity key of the Filter
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a Filter
    api_response = api_instance.put_filter(body, id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FiltersApi->put_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Filter**](Filter.md)|  | 
 **id** | **str**| Identity key of the Filter | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Filter**](Filter.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

