# drppy_client.ClustersApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cleanup_cluster**](ClustersApi.md#cleanup_cluster) | **DELETE** /clusters/{uuid}/cleanup | Cleanup a Cluster
[**create_cluster**](ClustersApi.md#create_cluster) | **POST** /clusters | Create a Cluster
[**delete_cluster**](ClustersApi.md#delete_cluster) | **DELETE** /clusters/{uuid} | Delete a Cluster
[**delete_cluster_group_param**](ClustersApi.md#delete_cluster_group_param) | **DELETE** /clusters/{uuid}/group/params/{key} | Delete a single Cluster group profile parameter
[**delete_cluster_param**](ClustersApi.md#delete_cluster_param) | **DELETE** /clusters/{uuid}/params/{key} | Delete a single clusters parameter
[**get_cluster**](ClustersApi.md#get_cluster) | **GET** /clusters/{uuid} | Get a Cluster
[**get_cluster_action**](ClustersApi.md#get_cluster_action) | **GET** /clusters/{uuid}/actions/{cmd} | List specific action for a clusters Cluster
[**get_cluster_actions**](ClustersApi.md#get_cluster_actions) | **GET** /clusters/{uuid}/actions | List clusters actions Cluster
[**get_cluster_group_param**](ClustersApi.md#get_cluster_group_param) | **GET** /clusters/{uuid}/group/params/{key} | Get a single Cluster group profile parameter
[**get_cluster_group_params**](ClustersApi.md#get_cluster_group_params) | **GET** /clusters/{uuid}/group/params | List Cluster group profile params Cluster
[**get_cluster_group_pub_key**](ClustersApi.md#get_cluster_group_pub_key) | **GET** /clusters/{uuid}/group/pubkey | Get the public key for secure params on a Cluster group profile
[**get_cluster_param**](ClustersApi.md#get_cluster_param) | **GET** /clusters/{uuid}/params/{key} | Get a single clusters parameter
[**get_cluster_params**](ClustersApi.md#get_cluster_params) | **GET** /clusters/{uuid}/params | List clusters params Cluster
[**get_cluster_pub_key**](ClustersApi.md#get_cluster_pub_key) | **GET** /clusters/{uuid}/pubkey | Get the public key for secure params on a clusters
[**get_cluster_render**](ClustersApi.md#get_cluster_render) | **POST** /clusters/{uuid}/render | Render a blob on a machine
[**get_cluster_token**](ClustersApi.md#get_cluster_token) | **GET** /clusters/{uuid}/token | Get a Cluster Token
[**head_cluster**](ClustersApi.md#head_cluster) | **HEAD** /clusters/{uuid} | See if a Cluster exists
[**list_clusters**](ClustersApi.md#list_clusters) | **GET** /clusters | Lists Clusters filtered by some parameters.
[**list_stats_clusters**](ClustersApi.md#list_stats_clusters) | **HEAD** /clusters | Stats of the List Clusters filtered by some parameters.
[**patch_cluster**](ClustersApi.md#patch_cluster) | **PATCH** /clusters/{uuid} | Patch a Cluster
[**patch_cluster_group_params**](ClustersApi.md#patch_cluster_group_params) | **PATCH** /clusters/{uuid}/group/params | Update group profile parameters (merges with existing data)
[**patch_cluster_params**](ClustersApi.md#patch_cluster_params) | **PATCH** /clusters/{uuid}/params | Update all params on the object (merges with existing data)
[**post_cluster_action**](ClustersApi.md#post_cluster_action) | **POST** /clusters/{uuid}/actions/{cmd} | Call an action on the node.
[**post_cluster_group_param**](ClustersApi.md#post_cluster_group_param) | **POST** /clusters/{uuid}/group/params/{key} | Set a single Parameter in the group
[**post_cluster_group_params**](ClustersApi.md#post_cluster_group_params) | **POST** /clusters/{uuid}/group/params | Sets the group parameters (replaces)
[**post_cluster_param**](ClustersApi.md#post_cluster_param) | **POST** /clusters/{uuid}/params/{key} | Set a single parameter on an object
[**post_cluster_params**](ClustersApi.md#post_cluster_params) | **POST** /clusters/{uuid}/params | Replaces all parameters on the object
[**post_cluster_release_to_pool**](ClustersApi.md#post_cluster_release_to_pool) | **POST** /clusters/{uuid}/releaseToPool | Releases a cluster in this pool.
[**put_cluster**](ClustersApi.md#put_cluster) | **PUT** /clusters/{uuid} | Put a Cluster
[**start_cluster**](ClustersApi.md#start_cluster) | **PATCH** /clusters/{uuid}/start | Start a Cluster


# **cleanup_cluster**
> Cluster cleanup_cluster(uuid, force=force, commented=commented, reduced=reduced)

Cleanup a Cluster

Cleanup a Cluster specified by {uuid}.  If 202 is returned, the on-delete-workflow has been started.

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Cleanup a Cluster
    api_response = api_instance.cleanup_cluster(uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->cleanup_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Cluster**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_cluster**
> Cluster create_cluster(body)

Create a Cluster

Create a Cluster from the provided object

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Cluster() # Cluster | 

try:
    # Create a Cluster
    api_response = api_instance.create_cluster(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->create_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Cluster**](Cluster.md)|  | 

### Return type

[**Cluster**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cluster**
> Cluster delete_cluster(uuid, force=force, commented=commented, reduced=reduced)

Delete a Cluster

Delete a Cluster specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a Cluster
    api_response = api_instance.delete_cluster(uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->delete_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Cluster**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cluster_group_param**
> object delete_cluster_group_param()

Delete a single Cluster group profile parameter

Delete a single group profile parameter {key} for a Cluster specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))

try:
    # Delete a single Cluster group profile parameter
    api_response = api_instance.delete_cluster_group_param()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->delete_cluster_group_param: %s\n" % e)
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

# **delete_cluster_param**
> object delete_cluster_param()

Delete a single clusters parameter

Delete a single parameter {key} for a Cluster specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))

try:
    # Delete a single clusters parameter
    api_response = api_instance.delete_cluster_param()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->delete_cluster_param: %s\n" % e)
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

# **get_cluster**
> Cluster get_cluster(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a Cluster

Get the Cluster specified by {uuid}  or return NotFound.

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a Cluster
    api_response = api_instance.get_cluster(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Cluster**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cluster_action**
> AvailableAction get_cluster_action(uuid, cmd, plugin=plugin)

List specific action for a clusters Cluster

List specific {cmd} action for a Cluster specified by {uuid}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a clusters Cluster
    api_response = api_instance.get_cluster_action(uuid, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
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

# **get_cluster_actions**
> list[AvailableAction] get_cluster_actions(uuid, plugin=plugin)

List clusters actions Cluster

List Cluster actions for a Cluster specified by {uuid}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List clusters actions Cluster
    api_response = api_instance.get_cluster_actions(uuid, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cluster_group_param**
> object get_cluster_group_param(uuid, key, aggregate=aggregate, decode=decode)

Get a single Cluster group profile parameter

Get a single parameter {key} for a Cluster group profile specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
key = 'key_example' # str | Param name
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)

try:
    # Get a single Cluster group profile parameter
    api_response = api_instance.get_cluster_group_param(uuid, key, aggregate=aggregate, decode=decode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_group_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
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

# **get_cluster_group_params**
> dict(str, object) get_cluster_group_params(uuid, aggregate=aggregate, decode=decode, params=params)

List Cluster group profile params Cluster

List Cluster params for a Cluster group profile specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
params = 'params_example' # str |  (optional)

try:
    # List Cluster group profile params Cluster
    api_response = api_instance.get_cluster_group_params(uuid, aggregate=aggregate, decode=decode, params=params)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_group_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
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

# **get_cluster_group_pub_key**
> get_cluster_group_pub_key(uuid)

Get the public key for secure params on a Cluster group profile

Get the public key for a Cluster group profile specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster

try:
    # Get the public key for secure params on a Cluster group profile
    api_instance.get_cluster_group_pub_key(uuid)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_group_pub_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cluster_param**
> object get_cluster_param(uuid, key, aggregate=aggregate, decode=decode)

Get a single clusters parameter

Get a single parameter {key} for a Cluster specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
key = 'key_example' # str | Param name
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)

try:
    # Get a single clusters parameter
    api_response = api_instance.get_cluster_param(uuid, key, aggregate=aggregate, decode=decode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
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

# **get_cluster_params**
> dict(str, object) get_cluster_params(uuid, aggregate=aggregate, decode=decode, params=params)

List clusters params Cluster

List Cluster parms for a Cluster specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
params = 'params_example' # str |  (optional)

try:
    # List clusters params Cluster
    api_response = api_instance.get_cluster_params(uuid, aggregate=aggregate, decode=decode, params=params)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
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

# **get_cluster_pub_key**
> get_cluster_pub_key(uuid)

Get the public key for secure params on a clusters

Get the public key for a Cluster specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster

try:
    # Get the public key for secure params on a clusters
    api_instance.get_cluster_pub_key(uuid)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_pub_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cluster_render**
> str get_cluster_render(uuid, body=body)

Render a blob on a machine

Renders the data posted on the cluster specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 
body = 'body_example' # str |  (optional)

try:
    # Render a blob on a machine
    api_response = api_instance.get_cluster_render(uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_render: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 
 **body** | **str**|  | [optional] 

### Return type

**str**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cluster_token**
> UserToken get_cluster_token(uuid, ttl=ttl)

Get a Cluster Token

Get a Cluster Token specified by {uuid} or return NotFound.

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 
ttl = 789 # int |  (optional)

try:
    # Get a Cluster Token
    api_response = api_instance.get_cluster_token(uuid, ttl=ttl)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->get_cluster_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 
 **ttl** | **int**|  | [optional] 

### Return type

[**UserToken**](UserToken.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_cluster**
> head_cluster(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a Cluster exists

Return 200 if the Cluster specifiec by {uuid} exists, or return NotFound.

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a Cluster exists
    api_instance.head_cluster(uuid, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling ClustersApi->head_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
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

# **list_clusters**
> list[Cluster] list_clusters(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, address=address, arch=arch, available=available, boot_env=boot_env, bundle=bundle, context=context, created_at=created_at, created_by=created_by, current_job=current_job, current_task=current_task, description=description, endpoint=endpoint, errors=errors, fingerprint=fingerprint, hardware_addrs=hardware_addrs, job_exit_state=job_exit_state, job_result_errors=job_result_errors, job_state=job_state, last_modified_at=last_modified_at, last_modified_by=last_modified_by, locked=locked, meta=meta, name=name, os=os, params2=params2, partial=partial, pending_work_orders=pending_work_orders, pool=pool, pool_allocated=pool_allocated, pool_status=pool_status, profiles=profiles, read_only=read_only, retry_task_attempt=retry_task_attempt, runnable=runnable, running_work_orders=running_work_orders, secret=secret, stage=stage, task_error_stacks=task_error_stacks, tasks=tasks, uuid=uuid, validated=validated, work_order_mode=work_order_mode, workflow=workflow, workflow_complete=workflow_complete)

Lists Clusters filtered by some parameters.

This will show all Clusters by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Uuid=fred - returns items named fred<br/> Uuid=Lt(fred) - returns items that alphabetically less than fred.<br/> Uuid=Lt(fred)&Available=true - returns items with Uuid less than fred and Available is true<br/>

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
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
address = 'address_example' # str | The IPv4 address of the machine that should be used for PXE purposes.  Note that this field does not directly tie into DHCP leases or reservations -- the provisioner relies solely on this address when determining what to render for a specific machine. Address is updated automatically by the DHCP system if HardwareAddrs is filled out. (optional)
arch = 'arch_example' # str | Arch is the machine architecture. It should be an arch that can be fed into $GOARCH. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
boot_env = 'boot_env_example' # str | The boot environment that the machine should boot into.  This must be the name of a boot environment present in the backend. If this field is not present or blank, the global default bootenv will be used instead. (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
context = 'context_example' # str | Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
current_job = 'current_job_example' # str | The UUID of the job that is currently running. (optional)
current_task = 'current_task_example' # str | The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
fingerprint = 'fingerprint_example' # str | Fingerprint is a collection of data that can (in theory) be used to uniquely identify a machine based on various DMI information.  This (in conjunction with HardwareAddrs) is used to uniquely identify a Machine using a score based on how many total items in the Fingerprint match.  While marked readonly, it is writeable but should really only be written by the drp tooling. (optional)
hardware_addrs = 'hardware_addrs_example' # str | HardwareAddrs is a list of MAC addresses we expect that the system might boot from. This must be filled out to enable MAC address based booting from the various bootenvs, and must be updated if the MAC addresses for a system change for whatever reason. (optional)
job_exit_state = 'job_exit_state_example' # str | The final disposition of the current job. Can be one of \"reboot\",\"poweroff\",\"stop\", or \"complete\" Other substates may be added as time goes on (optional)
job_result_errors = 'job_result_errors_example' # str | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. (optional)
job_state = 'job_state_example' # str | The state the current job is in.  Must be one of \"created\", \"failed\", \"finished\", \"incomplete\" (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
locked = 'locked_example' # str | Locked indicates that changes to the Machine by users are not allowed, except for unlocking the machine, which will always generate an Audit event. (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | The name of the machine.  This must be unique across all machines, and by convention it is the FQDN of the machine, although nothing enforces that. (optional)
os = 'os_example' # str | OS is the operating system that the node is running in.  It is updated by Sledgehammer and by the various OS install tasks. (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
partial = 'partial_example' # str | Partial tracks if the object is not complete when returned. read only: true (optional)
pending_work_orders = 'pending_work_orders_example' # str | PendingWorkOrders is the number of work orders for this Machine that are in the 'created' state. (optional)
pool = 'pool_example' # str | Pool contains the pool the machine is in. Unset machines will join the default Pool (optional)
pool_allocated = 'pool_allocated_example' # str | PoolAllocated defines if the machine is allocated in this pool This is a calculated field. (optional)
pool_status = 'pool_status_example' # str | PoolStatus contains the status of this machine in the Pool. Values are defined in Pool.PoolStatuses (optional)
profiles = 'profiles_example' # str | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
retry_task_attempt = 'retry_task_attempt_example' # str | This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. (optional)
runnable = 'runnable_example' # str | Runnable indicates that this is Runnable. (optional)
running_work_orders = 'running_work_orders_example' # str | RunningWorkOrders is the number of work orders for this Machine that are in the 'running' state. (optional)
secret = 'secret_example' # str | Secret for machine token revocation.  Changing the secret will invalidate all existing tokens for this machine (optional)
stage = 'stage_example' # str | The stage that this is currently in. (optional)
task_error_stacks = 'task_error_stacks_example' # str | This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. (optional)
tasks = 'tasks_example' # str | The current tasks that are being processed. (optional)
uuid = 'uuid_example' # str | The UUID of the machine. This is auto-created at Create time, and cannot change afterwards. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)
work_order_mode = 'work_order_mode_example' # str | WorkOrderMode indicates if the machine is action mode (optional)
workflow = 'workflow_example' # str | Workflow is the workflow that is currently responsible for processing machine tasks. (optional)
workflow_complete = 'workflow_complete_example' # str | WorkflowComplete indicates if the workflow is complete (optional)

try:
    # Lists Clusters filtered by some parameters.
    api_response = api_instance.list_clusters(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, address=address, arch=arch, available=available, boot_env=boot_env, bundle=bundle, context=context, created_at=created_at, created_by=created_by, current_job=current_job, current_task=current_task, description=description, endpoint=endpoint, errors=errors, fingerprint=fingerprint, hardware_addrs=hardware_addrs, job_exit_state=job_exit_state, job_result_errors=job_result_errors, job_state=job_state, last_modified_at=last_modified_at, last_modified_by=last_modified_by, locked=locked, meta=meta, name=name, os=os, params2=params2, partial=partial, pending_work_orders=pending_work_orders, pool=pool, pool_allocated=pool_allocated, pool_status=pool_status, profiles=profiles, read_only=read_only, retry_task_attempt=retry_task_attempt, runnable=runnable, running_work_orders=running_work_orders, secret=secret, stage=stage, task_error_stacks=task_error_stacks, tasks=tasks, uuid=uuid, validated=validated, work_order_mode=work_order_mode, workflow=workflow, workflow_complete=workflow_complete)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->list_clusters: %s\n" % e)
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
 **address** | **str**| The IPv4 address of the machine that should be used for PXE purposes.  Note that this field does not directly tie into DHCP leases or reservations -- the provisioner relies solely on this address when determining what to render for a specific machine. Address is updated automatically by the DHCP system if HardwareAddrs is filled out. | [optional] 
 **arch** | **str**| Arch is the machine architecture. It should be an arch that can be fed into $GOARCH. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **boot_env** | **str**| The boot environment that the machine should boot into.  This must be the name of a boot environment present in the backend. If this field is not present or blank, the global default bootenv will be used instead. | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **context** | **str**| Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **current_job** | [**str**](.md)| The UUID of the job that is currently running. | [optional] 
 **current_task** | **str**| The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **fingerprint** | **str**| Fingerprint is a collection of data that can (in theory) be used to uniquely identify a machine based on various DMI information.  This (in conjunction with HardwareAddrs) is used to uniquely identify a Machine using a score based on how many total items in the Fingerprint match.  While marked readonly, it is writeable but should really only be written by the drp tooling. | [optional] 
 **hardware_addrs** | **str**| HardwareAddrs is a list of MAC addresses we expect that the system might boot from. This must be filled out to enable MAC address based booting from the various bootenvs, and must be updated if the MAC addresses for a system change for whatever reason. | [optional] 
 **job_exit_state** | **str**| The final disposition of the current job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
 **job_result_errors** | **str**| ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
 **job_state** | **str**| The state the current job is in.  Must be one of \&quot;created\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **locked** | **str**| Locked indicates that changes to the Machine by users are not allowed, except for unlocking the machine, which will always generate an Audit event. | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| The name of the machine.  This must be unique across all machines, and by convention it is the FQDN of the machine, although nothing enforces that. | [optional] 
 **os** | **str**| OS is the operating system that the node is running in.  It is updated by Sledgehammer and by the various OS install tasks. | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **partial** | **str**| Partial tracks if the object is not complete when returned. read only: true | [optional] 
 **pending_work_orders** | **str**| PendingWorkOrders is the number of work orders for this Machine that are in the &#39;created&#39; state. | [optional] 
 **pool** | **str**| Pool contains the pool the machine is in. Unset machines will join the default Pool | [optional] 
 **pool_allocated** | **str**| PoolAllocated defines if the machine is allocated in this pool This is a calculated field. | [optional] 
 **pool_status** | **str**| PoolStatus contains the status of this machine in the Pool. Values are defined in Pool.PoolStatuses | [optional] 
 **profiles** | **str**| Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **retry_task_attempt** | **str**| This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. | [optional] 
 **runnable** | **str**| Runnable indicates that this is Runnable. | [optional] 
 **running_work_orders** | **str**| RunningWorkOrders is the number of work orders for this Machine that are in the &#39;running&#39; state. | [optional] 
 **secret** | **str**| Secret for machine token revocation.  Changing the secret will invalidate all existing tokens for this machine | [optional] 
 **stage** | **str**| The stage that this is currently in. | [optional] 
 **task_error_stacks** | **str**| This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. | [optional] 
 **tasks** | **str**| The current tasks that are being processed. | [optional] 
 **uuid** | [**str**](.md)| The UUID of the machine. This is auto-created at Create time, and cannot change afterwards. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 
 **work_order_mode** | **str**| WorkOrderMode indicates if the machine is action mode | [optional] 
 **workflow** | **str**| Workflow is the workflow that is currently responsible for processing machine tasks. | [optional] 
 **workflow_complete** | **str**| WorkflowComplete indicates if the workflow is complete | [optional] 

### Return type

[**list[Cluster]**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_stats_clusters**
> list_stats_clusters(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, address=address, arch=arch, available=available, boot_env=boot_env, bundle=bundle, context=context, created_at=created_at, created_by=created_by, current_job=current_job, current_task=current_task, description=description, endpoint=endpoint, errors=errors, fingerprint=fingerprint, hardware_addrs=hardware_addrs, job_exit_state=job_exit_state, job_result_errors=job_result_errors, job_state=job_state, last_modified_at=last_modified_at, last_modified_by=last_modified_by, locked=locked, meta=meta, name=name, os=os, params2=params2, partial=partial, pending_work_orders=pending_work_orders, pool=pool, pool_allocated=pool_allocated, pool_status=pool_status, profiles=profiles, read_only=read_only, retry_task_attempt=retry_task_attempt, runnable=runnable, running_work_orders=running_work_orders, secret=secret, stage=stage, task_error_stacks=task_error_stacks, tasks=tasks, uuid=uuid, validated=validated, work_order_mode=work_order_mode, workflow=workflow, workflow_complete=workflow_complete)

Stats of the List Clusters filtered by some parameters.

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
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
address = 'address_example' # str | The IPv4 address of the machine that should be used for PXE purposes.  Note that this field does not directly tie into DHCP leases or reservations -- the provisioner relies solely on this address when determining what to render for a specific machine. Address is updated automatically by the DHCP system if HardwareAddrs is filled out. (optional)
arch = 'arch_example' # str | Arch is the machine architecture. It should be an arch that can be fed into $GOARCH. (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
boot_env = 'boot_env_example' # str | The boot environment that the machine should boot into.  This must be the name of a boot environment present in the backend. If this field is not present or blank, the global default bootenv will be used instead. (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
context = 'context_example' # str | Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
current_job = 'current_job_example' # str | The UUID of the job that is currently running. (optional)
current_task = 'current_task_example' # str | The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
fingerprint = 'fingerprint_example' # str | Fingerprint is a collection of data that can (in theory) be used to uniquely identify a machine based on various DMI information.  This (in conjunction with HardwareAddrs) is used to uniquely identify a Machine using a score based on how many total items in the Fingerprint match.  While marked readonly, it is writeable but should really only be written by the drp tooling. (optional)
hardware_addrs = 'hardware_addrs_example' # str | HardwareAddrs is a list of MAC addresses we expect that the system might boot from. This must be filled out to enable MAC address based booting from the various bootenvs, and must be updated if the MAC addresses for a system change for whatever reason. (optional)
job_exit_state = 'job_exit_state_example' # str | The final disposition of the current job. Can be one of \"reboot\",\"poweroff\",\"stop\", or \"complete\" Other substates may be added as time goes on (optional)
job_result_errors = 'job_result_errors_example' # str | ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. (optional)
job_state = 'job_state_example' # str | The state the current job is in.  Must be one of \"created\", \"failed\", \"finished\", \"incomplete\" (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
locked = 'locked_example' # str | Locked indicates that changes to the Machine by users are not allowed, except for unlocking the machine, which will always generate an Audit event. (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | The name of the machine.  This must be unique across all machines, and by convention it is the FQDN of the machine, although nothing enforces that. (optional)
os = 'os_example' # str | OS is the operating system that the node is running in.  It is updated by Sledgehammer and by the various OS install tasks. (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
partial = 'partial_example' # str | Partial tracks if the object is not complete when returned. read only: true (optional)
pending_work_orders = 'pending_work_orders_example' # str | PendingWorkOrders is the number of work orders for this Machine that are in the 'created' state. (optional)
pool = 'pool_example' # str | Pool contains the pool the machine is in. Unset machines will join the default Pool (optional)
pool_allocated = 'pool_allocated_example' # str | PoolAllocated defines if the machine is allocated in this pool This is a calculated field. (optional)
pool_status = 'pool_status_example' # str | PoolStatus contains the status of this machine in the Pool. Values are defined in Pool.PoolStatuses (optional)
profiles = 'profiles_example' # str | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
retry_task_attempt = 'retry_task_attempt_example' # str | This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. (optional)
runnable = 'runnable_example' # str | Runnable indicates that this is Runnable. (optional)
running_work_orders = 'running_work_orders_example' # str | RunningWorkOrders is the number of work orders for this Machine that are in the 'running' state. (optional)
secret = 'secret_example' # str | Secret for machine token revocation.  Changing the secret will invalidate all existing tokens for this machine (optional)
stage = 'stage_example' # str | The stage that this is currently in. (optional)
task_error_stacks = 'task_error_stacks_example' # str | This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. (optional)
tasks = 'tasks_example' # str | The current tasks that are being processed. (optional)
uuid = 'uuid_example' # str | The UUID of the machine. This is auto-created at Create time, and cannot change afterwards. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)
work_order_mode = 'work_order_mode_example' # str | WorkOrderMode indicates if the machine is action mode (optional)
workflow = 'workflow_example' # str | Workflow is the workflow that is currently responsible for processing machine tasks. (optional)
workflow_complete = 'workflow_complete_example' # str | WorkflowComplete indicates if the workflow is complete (optional)

try:
    # Stats of the List Clusters filtered by some parameters.
    api_instance.list_stats_clusters(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, address=address, arch=arch, available=available, boot_env=boot_env, bundle=bundle, context=context, created_at=created_at, created_by=created_by, current_job=current_job, current_task=current_task, description=description, endpoint=endpoint, errors=errors, fingerprint=fingerprint, hardware_addrs=hardware_addrs, job_exit_state=job_exit_state, job_result_errors=job_result_errors, job_state=job_state, last_modified_at=last_modified_at, last_modified_by=last_modified_by, locked=locked, meta=meta, name=name, os=os, params2=params2, partial=partial, pending_work_orders=pending_work_orders, pool=pool, pool_allocated=pool_allocated, pool_status=pool_status, profiles=profiles, read_only=read_only, retry_task_attempt=retry_task_attempt, runnable=runnable, running_work_orders=running_work_orders, secret=secret, stage=stage, task_error_stacks=task_error_stacks, tasks=tasks, uuid=uuid, validated=validated, work_order_mode=work_order_mode, workflow=workflow, workflow_complete=workflow_complete)
except ApiException as e:
    print("Exception when calling ClustersApi->list_stats_clusters: %s\n" % e)
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
 **address** | **str**| The IPv4 address of the machine that should be used for PXE purposes.  Note that this field does not directly tie into DHCP leases or reservations -- the provisioner relies solely on this address when determining what to render for a specific machine. Address is updated automatically by the DHCP system if HardwareAddrs is filled out. | [optional] 
 **arch** | **str**| Arch is the machine architecture. It should be an arch that can be fed into $GOARCH. | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **boot_env** | **str**| The boot environment that the machine should boot into.  This must be the name of a boot environment present in the backend. If this field is not present or blank, the global default bootenv will be used instead. | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **context** | **str**| Contexts contains the name of the current execution context. An empty string indicates that an agent running on a Machine should be executing tasks, and any other value means that an agent running with its context set for this value should be executing tasks. | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **current_job** | [**str**](.md)| The UUID of the job that is currently running. | [optional] 
 **current_task** | **str**| The index into the Tasks list for the task that is currently running (if a task is running) or the next task that will run (if no task is currently running).  If -1, then the first task will run next, and if it is equal to the length of the Tasks list then all the tasks have finished running. | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **fingerprint** | **str**| Fingerprint is a collection of data that can (in theory) be used to uniquely identify a machine based on various DMI information.  This (in conjunction with HardwareAddrs) is used to uniquely identify a Machine using a score based on how many total items in the Fingerprint match.  While marked readonly, it is writeable but should really only be written by the drp tooling. | [optional] 
 **hardware_addrs** | **str**| HardwareAddrs is a list of MAC addresses we expect that the system might boot from. This must be filled out to enable MAC address based booting from the various bootenvs, and must be updated if the MAC addresses for a system change for whatever reason. | [optional] 
 **job_exit_state** | **str**| The final disposition of the current job. Can be one of \&quot;reboot\&quot;,\&quot;poweroff\&quot;,\&quot;stop\&quot;, or \&quot;complete\&quot; Other substates may be added as time goes on | [optional] 
 **job_result_errors** | **str**| ResultErrors is a list of error from the task.  This is filled in by the task if it is written to do so.  This tracks results without requiring job logs. | [optional] 
 **job_state** | **str**| The state the current job is in.  Must be one of \&quot;created\&quot;, \&quot;failed\&quot;, \&quot;finished\&quot;, \&quot;incomplete\&quot; | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **locked** | **str**| Locked indicates that changes to the Machine by users are not allowed, except for unlocking the machine, which will always generate an Audit event. | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| The name of the machine.  This must be unique across all machines, and by convention it is the FQDN of the machine, although nothing enforces that. | [optional] 
 **os** | **str**| OS is the operating system that the node is running in.  It is updated by Sledgehammer and by the various OS install tasks. | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **partial** | **str**| Partial tracks if the object is not complete when returned. read only: true | [optional] 
 **pending_work_orders** | **str**| PendingWorkOrders is the number of work orders for this Machine that are in the &#39;created&#39; state. | [optional] 
 **pool** | **str**| Pool contains the pool the machine is in. Unset machines will join the default Pool | [optional] 
 **pool_allocated** | **str**| PoolAllocated defines if the machine is allocated in this pool This is a calculated field. | [optional] 
 **pool_status** | **str**| PoolStatus contains the status of this machine in the Pool. Values are defined in Pool.PoolStatuses | [optional] 
 **profiles** | **str**| Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **retry_task_attempt** | **str**| This tracks the number of retry attempts for the current task. When a task succeeds, the retry value is reset. | [optional] 
 **runnable** | **str**| Runnable indicates that this is Runnable. | [optional] 
 **running_work_orders** | **str**| RunningWorkOrders is the number of work orders for this Machine that are in the &#39;running&#39; state. | [optional] 
 **secret** | **str**| Secret for machine token revocation.  Changing the secret will invalidate all existing tokens for this machine | [optional] 
 **stage** | **str**| The stage that this is currently in. | [optional] 
 **task_error_stacks** | **str**| This list of previous task lists and current tasks to handle errors. Upon completing the list, the previous task list will be executed.  This will be capped to a depth of 1.  Error failures can not be handled. | [optional] 
 **tasks** | **str**| The current tasks that are being processed. | [optional] 
 **uuid** | [**str**](.md)| The UUID of the machine. This is auto-created at Create time, and cannot change afterwards. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 
 **work_order_mode** | **str**| WorkOrderMode indicates if the machine is action mode | [optional] 
 **workflow** | **str**| Workflow is the workflow that is currently responsible for processing machine tasks. | [optional] 
 **workflow_complete** | **str**| WorkflowComplete indicates if the workflow is complete | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_cluster**
> Cluster patch_cluster(body, uuid, force=force, commented=commented, reduced=reduced)

Patch a Cluster

Update a Cluster specified by {uuid} using a RFC6902 Patch structure

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
uuid = 'uuid_example' # str | Identity key of the Cluster
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a Cluster
    api_response = api_instance.patch_cluster(body, uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->patch_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Cluster**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_cluster_group_params**
> dict(str, object) patch_cluster_group_params(body)

Update group profile parameters (merges with existing data)

Update group profile params for Cluster {uuid} with the passed-in patch

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 

try:
    # Update group profile parameters (merges with existing data)
    api_response = api_instance.patch_cluster_group_params(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->patch_cluster_group_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_cluster_params**
> dict(str, object) patch_cluster_params(body, uuid)

Update all params on the object (merges with existing data)

Update params for Cluster {uuid} with the passed-in patch

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
uuid = 'uuid_example' # str | Identity key of the Cluster

try:
    # Update all params on the object (merges with existing data)
    api_response = api_instance.patch_cluster_params(body, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->patch_cluster_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **uuid** | [**str**](.md)| Identity key of the Cluster | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_cluster_action**
> object post_cluster_action(uuid, cmd, body, plugin=plugin)

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | Identity key of the Cluster
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_cluster_action(uuid, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->post_cluster_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
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

# **post_cluster_group_param**
> object post_cluster_group_param(body, uuid, key)

Set a single Parameter in the group

Set a single Parameter {key} for a Cluster group profile specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 
uuid = 'uuid_example' # str | Identity key of the Cluster
key = 'key_example' # str | Param name

try:
    # Set a single Parameter in the group
    api_response = api_instance.post_cluster_group_param(body, uuid, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->post_cluster_group_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
 **key** | **str**| Param name | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_cluster_group_params**
> dict(str, object) post_cluster_group_params(body)

Sets the group parameters (replaces)

Sets parameters for a Cluster group profile specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 

try:
    # Sets the group parameters (replaces)
    api_response = api_instance.post_cluster_group_params(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->post_cluster_group_params: %s\n" % e)
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

# **post_cluster_param**
> object post_cluster_param(body, uuid, key)

Set a single parameter on an object

Set as single Parameter {key} for a clusters specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 
uuid = 'uuid_example' # str | Identity key of the Cluster
key = 'key_example' # str | Param name

try:
    # Set a single parameter on an object
    api_response = api_instance.post_cluster_param(body, uuid, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->post_cluster_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
 **key** | **str**| Param name | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_cluster_params**
> dict(str, object) post_cluster_params(body)

Replaces all parameters on the object

Sets parameters for a clusters specified by {uuid}

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = NULL # object | 

try:
    # Replaces all parameters on the object
    api_response = api_instance.post_cluster_params(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->post_cluster_params: %s\n" % e)
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

# **post_cluster_release_to_pool**
> list[PoolResult] post_cluster_release_to_pool(uuid)

Releases a cluster in this pool.

No input.

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
uuid = 'uuid_example' # str | 

try:
    # Releases a cluster in this pool.
    api_response = api_instance.post_cluster_release_to_pool(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->post_cluster_release_to_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**|  | 

### Return type

[**list[PoolResult]**](PoolResult.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_cluster**
> Cluster put_cluster(body, uuid, force=force, commented=commented, reduced=reduced)

Put a Cluster

Update a Cluster specified by {uuid} using a JSON Cluster

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Cluster() # Cluster | 
uuid = 'uuid_example' # str | Identity key of the Cluster
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a Cluster
    api_response = api_instance.put_cluster(body, uuid, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->put_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Cluster**](Cluster.md)|  | 
 **uuid** | [**str**](.md)| Identity key of the Cluster | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Cluster**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_cluster**
> Cluster start_cluster(body, force=force)

Start a Cluster

Update a Cluster specified by {uuid} using a RFC6902 Patch structure after clearing Workflow and Runnable.

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
api_instance = drppy_client.ClustersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
force = true # bool | Attempt force the action with less validation (optional)

try:
    # Start a Cluster
    api_response = api_instance.start_cluster(body, force=force)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClustersApi->start_cluster: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 

### Return type

[**Cluster**](Cluster.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

