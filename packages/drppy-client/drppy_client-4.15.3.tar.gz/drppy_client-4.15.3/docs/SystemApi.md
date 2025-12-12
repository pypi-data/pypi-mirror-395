# drppy_client.SystemApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_system_action**](SystemApi.md#get_system_action) | **GET** /system/actions/{cmd} | List specific action for System
[**get_system_actions**](SystemApi.md#get_system_actions) | **GET** /system/actions | List system actions System
[**post_system_action**](SystemApi.md#post_system_action) | **POST** /system/actions/{cmd} | Call an action on the system.
[**system_status**](SystemApi.md#system_status) | **GET** /system/upgrade/status | Returns the status profile of the system upgrade.
[**system_update**](SystemApi.md#system_update) | **POST** /system/upgrade | Upload a file to upgrade the DRP system
[**system_update_exec**](SystemApi.md#system_update_exec) | **POST** /system/upgrade/exec | Execute a previously staged upgrade
[**system_update_run**](SystemApi.md#system_update_run) | **POST** /system/upgrade/run | Perform a rolling upgrade of a dr-provision cluster.
[**system_update_stage**](SystemApi.md#system_update_stage) | **POST** /system/upgrade/stage | Upload a file to perform a staged upgrade of a dr-provision cluster
[**system_update_unstage**](SystemApi.md#system_update_unstage) | **DELETE** /system/upgrade/stage | Unstage a pending staged update.  This will fail if an update us running.


# **get_system_action**
> AvailableAction get_system_action(cmd, plugin=plugin)

List specific action for System

List specific {cmd} action for System  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))
cmd = 'cmd_example' # str | 
plugin = 'plugin_example' # str |  (optional)

try:
    # List specific action for System
    api_response = api_instance.get_system_action(cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->get_system_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cmd** | **str**|  | 
 **plugin** | **str**|  | [optional] 

### Return type

[**AvailableAction**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_system_actions**
> list[AvailableAction] get_system_actions(plugin=plugin)

List system actions System

List System actions  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))
plugin = 'plugin_example' # str |  (optional)

try:
    # List system actions System
    api_response = api_instance.get_system_actions(plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->get_system_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plugin** | **str**|  | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_system_action**
> object post_system_action(cmd, body, plugin=plugin)

Call an action on the system.

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))
cmd = 'cmd_example' # str | 
body = NULL # object | 
plugin = 'plugin_example' # str |  (optional)

try:
    # Call an action on the system.
    api_response = api_instance.post_system_action(cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->post_system_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cmd** | **str**|  | 
 **body** | **object**|  | 
 **plugin** | **str**|  | [optional] 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **system_status**
> Profile system_status()

Returns the status profile of the system upgrade.

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))

try:
    # Returns the status profile of the system upgrade.
    api_response = api_instance.system_status()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->system_status: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Profile**](Profile.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **system_update**
> BlobInfo system_update()

Upload a file to upgrade the DRP system

The file will be uploaded and used to replace the running DRP instance.

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))

try:
    # Upload a file to upgrade the DRP system
    api_response = api_instance.system_update()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->system_update: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BlobInfo**](BlobInfo.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **system_update_exec**
> system_update_exec()

Execute a previously staged upgrade

The system will attempt to replace the current dr-provision and drpcli binaries with the ones staged by /system/upgrade/stage.  If the staged upgrade matches the running binary (based on SHA256sums), this will return 204, and no further action will be taken.  If the staged upgrade does not match the running binary, this will swap binaries, return 202, and restart 2 seconds after the API call finishes.

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))

try:
    # Execute a previously staged upgrade
    api_instance.system_update_exec()
except ApiException as e:
    print("Exception when calling SystemApi->system_update_exec: %s\n" % e)
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

# **system_update_run**
> system_update_run()

Perform a rolling upgrade of a dr-provision cluster.

The upgrade must already be staged.  All the nodes of the cluster will be upgraded by calling their /system/upgrade/exec API endpoint and then waiting on that node to restart and update its version in the consensus metadata.  Once that happens, the update process will move on to the next node.  All other nodes will be updated before the cluster leader.

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))

try:
    # Perform a rolling upgrade of a dr-provision cluster.
    api_instance.system_update_run()
except ApiException as e:
    print("Exception when calling SystemApi->system_update_run: %s\n" % e)
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

# **system_update_stage**
> BlobInfo system_update_stage()

Upload a file to perform a staged upgrade of a dr-provision cluster

The file will be uploaded and used to replace the running DRP instance.

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))

try:
    # Upload a file to perform a staged upgrade of a dr-provision cluster
    api_response = api_instance.system_update_stage()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->system_update_stage: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BlobInfo**](BlobInfo.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **system_update_unstage**
> system_update_unstage()

Unstage a pending staged update.  This will fail if an update us running.

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
api_instance = drppy_client.SystemApi(drppy_client.ApiClient(configuration))

try:
    # Unstage a pending staged update.  This will fail if an update us running.
    api_instance.system_update_unstage()
except ApiException as e:
    print("Exception when calling SystemApi->system_update_unstage: %s\n" % e)
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

