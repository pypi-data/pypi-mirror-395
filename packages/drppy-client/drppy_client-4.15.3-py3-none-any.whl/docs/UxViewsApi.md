# drppy_client.UxViewsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_ux_view**](UxViewsApi.md#create_ux_view) | **POST** /ux_views | Create a UxView
[**delete_ux_view**](UxViewsApi.md#delete_ux_view) | **DELETE** /ux_views/{id} | Delete a UxView
[**delete_ux_view_param**](UxViewsApi.md#delete_ux_view_param) | **DELETE** /ux_views/{id}/params/{key} | Delete a single ux_views parameter
[**get_ux_view**](UxViewsApi.md#get_ux_view) | **GET** /ux_views/{id} | Get a UxView
[**get_ux_view_action**](UxViewsApi.md#get_ux_view_action) | **GET** /ux_views/{id}/actions/{cmd} | List specific action for a ux_views UxView
[**get_ux_view_actions**](UxViewsApi.md#get_ux_view_actions) | **GET** /ux_views/{id}/actions | List ux_views actions UxView
[**get_ux_view_param**](UxViewsApi.md#get_ux_view_param) | **GET** /ux_views/{id}/params/{key} | Get a single ux_views parameter
[**get_ux_view_params**](UxViewsApi.md#get_ux_view_params) | **GET** /ux_views/{id}/params | List ux_views params UxView
[**get_ux_view_pub_key**](UxViewsApi.md#get_ux_view_pub_key) | **GET** /ux_views/{id}/pubkey | Get the public key for secure params on a ux_views
[**head_ux_view**](UxViewsApi.md#head_ux_view) | **HEAD** /ux_views/{id} | See if a UxView exists
[**list_stats_ux_views**](UxViewsApi.md#list_stats_ux_views) | **HEAD** /ux_views | Stats of the List UxViews filtered by some parameters.
[**list_ux_views**](UxViewsApi.md#list_ux_views) | **GET** /ux_views | Lists UxViews filtered by some parameters.
[**patch_ux_view**](UxViewsApi.md#patch_ux_view) | **PATCH** /ux_views/{id} | Patch a UxView
[**patch_ux_view_params**](UxViewsApi.md#patch_ux_view_params) | **PATCH** /ux_views/{id}/params | Update all params on the object (merges with existing data)
[**post_ux_view_action**](UxViewsApi.md#post_ux_view_action) | **POST** /ux_views/{id}/actions/{cmd} | Call an action on the node.
[**post_ux_view_param**](UxViewsApi.md#post_ux_view_param) | **POST** /ux_views/{id}/params/{key} | Set a single parameter on an object
[**post_ux_view_params**](UxViewsApi.md#post_ux_view_params) | **POST** /ux_views/{id}/params | Replaces all parameters on the object
[**put_ux_view**](UxViewsApi.md#put_ux_view) | **PUT** /ux_views/{id} | Put a UxView


# **create_ux_view**
> UxView create_ux_view(body)

Create a UxView

Create a UxView from the provided object

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
body = drppy_client.UxView() # UxView | 

try:
    # Create a UxView
    api_response = api_instance.create_ux_view(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->create_ux_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UxView**](UxView.md)|  | 

### Return type

[**UxView**](UxView.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_ux_view**
> UxView delete_ux_view(id, force=force, commented=commented, reduced=reduced)

Delete a UxView

Delete a UxView specified by {id}

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a UxView
    api_response = api_instance.delete_ux_view(id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->delete_ux_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**UxView**](UxView.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_ux_view_param**
> object delete_ux_view_param()

Delete a single ux_views parameter

Delete a single parameter {key} for a UxView specified by {id}

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))

try:
    # Delete a single ux_views parameter
    api_response = api_instance.delete_ux_view_param()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->delete_ux_view_param: %s\n" % e)
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

# **get_ux_view**
> UxView get_ux_view(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a UxView

Get the UxView specified by {id}  or return NotFound.

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a UxView
    api_response = api_instance.get_ux_view(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->get_ux_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**UxView**](UxView.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ux_view_action**
> AvailableAction get_ux_view_action(id, cmd, plugin=plugin)

List specific action for a ux_views UxView

List specific {cmd} action for a UxView specified by {id}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a ux_views UxView
    api_response = api_instance.get_ux_view_action(id, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->get_ux_view_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 
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

# **get_ux_view_actions**
> list[AvailableAction] get_ux_view_actions(id, plugin=plugin)

List ux_views actions UxView

List UxView actions for a UxView specified by {id}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List ux_views actions UxView
    api_response = api_instance.get_ux_view_actions(id, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->get_ux_view_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ux_view_param**
> object get_ux_view_param(id, key, aggregate=aggregate, decode=decode)

Get a single ux_views parameter

Get a single parameter {key} for a UxView specified by {id}

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView
key = 'key_example' # str | Param name
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)

try:
    # Get a single ux_views parameter
    api_response = api_instance.get_ux_view_param(id, key, aggregate=aggregate, decode=decode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->get_ux_view_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 
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

# **get_ux_view_params**
> dict(str, object) get_ux_view_params(id, aggregate=aggregate, decode=decode, params=params)

List ux_views params UxView

List UxView parms for a UxView specified by {id}

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
params = 'params_example' # str |  (optional)

try:
    # List ux_views params UxView
    api_response = api_instance.get_ux_view_params(id, aggregate=aggregate, decode=decode, params=params)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->get_ux_view_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 
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

# **get_ux_view_pub_key**
> get_ux_view_pub_key(id)

Get the public key for secure params on a ux_views

Get the public key for a UxView specified by {id}

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView

try:
    # Get the public key for secure params on a ux_views
    api_instance.get_ux_view_pub_key(id)
except ApiException as e:
    print("Exception when calling UxViewsApi->get_ux_view_pub_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_ux_view**
> head_ux_view(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a UxView exists

Return 200 if the UxView specifiec by {id} exists, or return NotFound.

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a UxView exists
    api_instance.head_ux_view(id, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling UxViewsApi->head_ux_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 
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

# **list_stats_ux_views**
> list_stats_ux_views(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, airgap=airgap, applicable_roles=applicable_roles, available=available, branding_image=branding_image, bulk_tabs=bulk_tabs, bundle=bundle, classifiers=classifiers, columns=columns, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, errors=errors, hide_edit_objects=hide_edit_objects, id=id, landing_page=landing_page, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine_fields=machine_fields, menu=menu, meta=meta, params2=params2, params_restriction=params_restriction, profiles_restriction=profiles_restriction, read_only=read_only, show_activiation=show_activiation, stages_restriction=stages_restriction, tasks_restriction=tasks_restriction, validated=validated, workflows_restriction=workflows_restriction)

Stats of the List UxViews filtered by some parameters.

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
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
airgap = 'airgap_example' # str | Airgap is not used.  Moved to license. Deprecated (optional)
applicable_roles = 'applicable_roles_example' # str | ApplicableRoles defines the roles that this view shows up for. e.g. superuser means that it will be available for users with the superuser role. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
branding_image = 'branding_image_example' # str | BrandingImage defines a files API path that should point to an image file. This replaces the RackN logo. (optional)
bulk_tabs = 'bulk_tabs_example' # str | BulkTabs defines the tabs for this view (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
classifiers = 'classifiers_example' # str | Classifiers is deprecated (optional)
columns = 'columns_example' # str | Columns defines the custom colums for a MenuItem Id (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
hide_edit_objects = 'hide_edit_objects_example' # str | HideEditObject defines a list of fields to hide when editting (optional)
id = 'id_example' # str | Id is the Name of the Filter (optional)
landing_page = 'landing_page_example' # str | LandingPage defines the default navigation route None or \"\" will open the system page. if it starts with http, it will navigate to the Overiew page. Otherwise, it will go to the machine's page. (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
machine_fields = 'machine_fields_example' # str | MachineFields defines the fields for this view (optional)
menu = 'menu_example' # str | Menu defines the menu elements. (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
params_restriction = 'params_restriction_example' # str | ParmsRestriction defines a list of restrictions for the parameter list (optional)
profiles_restriction = 'profiles_restriction_example' # str | ProfilesRestriction defines a list of restrictions for the profile list (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
show_activiation = 'show_activiation_example' # str | ShowActiviation is not used.  Moved to license. Deprecated (optional)
stages_restriction = 'stages_restriction_example' # str | StagesRestriction defines a list of restrictions for the stage list (optional)
tasks_restriction = 'tasks_restriction_example' # str | TasksRestriction defines a list of restrictions for the task list (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)
workflows_restriction = 'workflows_restriction_example' # str | WorkflowRestriction defines a list of restrictions for the workflow list (optional)

try:
    # Stats of the List UxViews filtered by some parameters.
    api_instance.list_stats_ux_views(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, airgap=airgap, applicable_roles=applicable_roles, available=available, branding_image=branding_image, bulk_tabs=bulk_tabs, bundle=bundle, classifiers=classifiers, columns=columns, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, errors=errors, hide_edit_objects=hide_edit_objects, id=id, landing_page=landing_page, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine_fields=machine_fields, menu=menu, meta=meta, params2=params2, params_restriction=params_restriction, profiles_restriction=profiles_restriction, read_only=read_only, show_activiation=show_activiation, stages_restriction=stages_restriction, tasks_restriction=tasks_restriction, validated=validated, workflows_restriction=workflows_restriction)
except ApiException as e:
    print("Exception when calling UxViewsApi->list_stats_ux_views: %s\n" % e)
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
 **airgap** | **str**| Airgap is not used.  Moved to license. Deprecated | [optional] 
 **applicable_roles** | **str**| ApplicableRoles defines the roles that this view shows up for. e.g. superuser means that it will be available for users with the superuser role. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **branding_image** | **str**| BrandingImage defines a files API path that should point to an image file. This replaces the RackN logo. | [optional] 
 **bulk_tabs** | **str**| BulkTabs defines the tabs for this view | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **classifiers** | **str**| Classifiers is deprecated | [optional] 
 **columns** | **str**| Columns defines the custom colums for a MenuItem Id | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **hide_edit_objects** | **str**| HideEditObject defines a list of fields to hide when editting | [optional] 
 **id** | **str**| Id is the Name of the Filter | [optional] 
 **landing_page** | **str**| LandingPage defines the default navigation route None or \&quot;\&quot; will open the system page. if it starts with http, it will navigate to the Overiew page. Otherwise, it will go to the machine&#39;s page. | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **machine_fields** | **str**| MachineFields defines the fields for this view | [optional] 
 **menu** | **str**| Menu defines the menu elements. | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **params_restriction** | **str**| ParmsRestriction defines a list of restrictions for the parameter list | [optional] 
 **profiles_restriction** | **str**| ProfilesRestriction defines a list of restrictions for the profile list | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **show_activiation** | **str**| ShowActiviation is not used.  Moved to license. Deprecated | [optional] 
 **stages_restriction** | **str**| StagesRestriction defines a list of restrictions for the stage list | [optional] 
 **tasks_restriction** | **str**| TasksRestriction defines a list of restrictions for the task list | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 
 **workflows_restriction** | **str**| WorkflowRestriction defines a list of restrictions for the workflow list | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ux_views**
> list[UxView] list_ux_views(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, airgap=airgap, applicable_roles=applicable_roles, available=available, branding_image=branding_image, bulk_tabs=bulk_tabs, bundle=bundle, classifiers=classifiers, columns=columns, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, errors=errors, hide_edit_objects=hide_edit_objects, id=id, landing_page=landing_page, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine_fields=machine_fields, menu=menu, meta=meta, params2=params2, params_restriction=params_restriction, profiles_restriction=profiles_restriction, read_only=read_only, show_activiation=show_activiation, stages_restriction=stages_restriction, tasks_restriction=tasks_restriction, validated=validated, workflows_restriction=workflows_restriction)

Lists UxViews filtered by some parameters.

This will show all UxViews by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Id=fred - returns items named fred<br/> Id=Lt(fred) - returns items that alphabetically less than fred.<br/> Id=Lt(fred)&Available=true - returns items with Id less than fred and Available is true<br/>

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
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
airgap = 'airgap_example' # str | Airgap is not used.  Moved to license. Deprecated (optional)
applicable_roles = 'applicable_roles_example' # str | ApplicableRoles defines the roles that this view shows up for. e.g. superuser means that it will be available for users with the superuser role. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
branding_image = 'branding_image_example' # str | BrandingImage defines a files API path that should point to an image file. This replaces the RackN logo. (optional)
bulk_tabs = 'bulk_tabs_example' # str | BulkTabs defines the tabs for this view (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
classifiers = 'classifiers_example' # str | Classifiers is deprecated (optional)
columns = 'columns_example' # str | Columns defines the custom colums for a MenuItem Id (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
hide_edit_objects = 'hide_edit_objects_example' # str | HideEditObject defines a list of fields to hide when editting (optional)
id = 'id_example' # str | Id is the Name of the Filter (optional)
landing_page = 'landing_page_example' # str | LandingPage defines the default navigation route None or \"\" will open the system page. if it starts with http, it will navigate to the Overiew page. Otherwise, it will go to the machine's page. (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
machine_fields = 'machine_fields_example' # str | MachineFields defines the fields for this view (optional)
menu = 'menu_example' # str | Menu defines the menu elements. (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
params_restriction = 'params_restriction_example' # str | ParmsRestriction defines a list of restrictions for the parameter list (optional)
profiles_restriction = 'profiles_restriction_example' # str | ProfilesRestriction defines a list of restrictions for the profile list (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
show_activiation = 'show_activiation_example' # str | ShowActiviation is not used.  Moved to license. Deprecated (optional)
stages_restriction = 'stages_restriction_example' # str | StagesRestriction defines a list of restrictions for the stage list (optional)
tasks_restriction = 'tasks_restriction_example' # str | TasksRestriction defines a list of restrictions for the task list (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)
workflows_restriction = 'workflows_restriction_example' # str | WorkflowRestriction defines a list of restrictions for the workflow list (optional)

try:
    # Lists UxViews filtered by some parameters.
    api_response = api_instance.list_ux_views(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, airgap=airgap, applicable_roles=applicable_roles, available=available, branding_image=branding_image, bulk_tabs=bulk_tabs, bundle=bundle, classifiers=classifiers, columns=columns, created_at=created_at, created_by=created_by, description=description, documentation=documentation, endpoint=endpoint, errors=errors, hide_edit_objects=hide_edit_objects, id=id, landing_page=landing_page, last_modified_at=last_modified_at, last_modified_by=last_modified_by, machine_fields=machine_fields, menu=menu, meta=meta, params2=params2, params_restriction=params_restriction, profiles_restriction=profiles_restriction, read_only=read_only, show_activiation=show_activiation, stages_restriction=stages_restriction, tasks_restriction=tasks_restriction, validated=validated, workflows_restriction=workflows_restriction)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->list_ux_views: %s\n" % e)
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
 **airgap** | **str**| Airgap is not used.  Moved to license. Deprecated | [optional] 
 **applicable_roles** | **str**| ApplicableRoles defines the roles that this view shows up for. e.g. superuser means that it will be available for users with the superuser role. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **branding_image** | **str**| BrandingImage defines a files API path that should point to an image file. This replaces the RackN logo. | [optional] 
 **bulk_tabs** | **str**| BulkTabs defines the tabs for this view | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **classifiers** | **str**| Classifiers is deprecated | [optional] 
 **columns** | **str**| Columns defines the custom colums for a MenuItem Id | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **hide_edit_objects** | **str**| HideEditObject defines a list of fields to hide when editting | [optional] 
 **id** | **str**| Id is the Name of the Filter | [optional] 
 **landing_page** | **str**| LandingPage defines the default navigation route None or \&quot;\&quot; will open the system page. if it starts with http, it will navigate to the Overiew page. Otherwise, it will go to the machine&#39;s page. | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **machine_fields** | **str**| MachineFields defines the fields for this view | [optional] 
 **menu** | **str**| Menu defines the menu elements. | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **params_restriction** | **str**| ParmsRestriction defines a list of restrictions for the parameter list | [optional] 
 **profiles_restriction** | **str**| ProfilesRestriction defines a list of restrictions for the profile list | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **show_activiation** | **str**| ShowActiviation is not used.  Moved to license. Deprecated | [optional] 
 **stages_restriction** | **str**| StagesRestriction defines a list of restrictions for the stage list | [optional] 
 **tasks_restriction** | **str**| TasksRestriction defines a list of restrictions for the task list | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 
 **workflows_restriction** | **str**| WorkflowRestriction defines a list of restrictions for the workflow list | [optional] 

### Return type

[**list[UxView]**](UxView.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_ux_view**
> UxView patch_ux_view(body, id, force=force, commented=commented, reduced=reduced)

Patch a UxView

Update a UxView specified by {id} using a RFC6902 Patch structure

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
id = 'id_example' # str | Identity key of the UxView
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a UxView
    api_response = api_instance.patch_ux_view(body, id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->patch_ux_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **id** | **str**| Identity key of the UxView | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**UxView**](UxView.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_ux_view_params**
> dict(str, object) patch_ux_view_params(body, id)

Update all params on the object (merges with existing data)

Update params for UxView {id} with the passed-in patch

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
id = 'id_example' # str | Identity key of the UxView

try:
    # Update all params on the object (merges with existing data)
    api_response = api_instance.patch_ux_view_params(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->patch_ux_view_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **id** | **str**| Identity key of the UxView | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_ux_view_action**
> object post_ux_view_action(id, cmd, body, plugin=plugin)

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | Identity key of the UxView
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_ux_view_action(id, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->post_ux_view_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identity key of the UxView | 
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

# **post_ux_view_param**
> object post_ux_view_param(body, id, key)

Set a single parameter on an object

Set as single Parameter {key} for a ux_views specified by {id}

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
body = NULL # object | 
id = 'id_example' # str | Identity key of the UxView
key = 'key_example' # str | Param name

try:
    # Set a single parameter on an object
    api_response = api_instance.post_ux_view_param(body, id, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->post_ux_view_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 
 **id** | **str**| Identity key of the UxView | 
 **key** | **str**| Param name | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_ux_view_params**
> dict(str, object) post_ux_view_params(body)

Replaces all parameters on the object

Sets parameters for a ux_views specified by {id}

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
body = NULL # object | 

try:
    # Replaces all parameters on the object
    api_response = api_instance.post_ux_view_params(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->post_ux_view_params: %s\n" % e)
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

# **put_ux_view**
> UxView put_ux_view(body, id, force=force, commented=commented, reduced=reduced)

Put a UxView

Update a UxView specified by {id} using a JSON UxView

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
api_instance = drppy_client.UxViewsApi(drppy_client.ApiClient(configuration))
body = drppy_client.UxView() # UxView | 
id = 'id_example' # str | Identity key of the UxView
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a UxView
    api_response = api_instance.put_ux_view(body, id, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UxViewsApi->put_ux_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UxView**](UxView.md)|  | 
 **id** | **str**| Identity key of the UxView | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**UxView**](UxView.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

