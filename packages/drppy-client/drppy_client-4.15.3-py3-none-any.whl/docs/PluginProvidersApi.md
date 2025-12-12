# drppy_client.PluginProvidersApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_plugin_provider**](PluginProvidersApi.md#delete_plugin_provider) | **DELETE** /plugin_providers/{name} | Delete a plugin provider
[**get_plugin_provider**](PluginProvidersApi.md#get_plugin_provider) | **GET** /plugin_providers/{name} | Get a specific plugin with {name}
[**get_plugin_provider_binary**](PluginProvidersApi.md#get_plugin_provider_binary) | **GET** /plugin_providers/{name}/binary | Get the binary for a specific plugin provider by {name}
[**head_plugin_provider**](PluginProvidersApi.md#head_plugin_provider) | **HEAD** /plugin_providers/{name} | See if a Plugin Provider exists
[**head_plugin_providers**](PluginProvidersApi.md#head_plugin_providers) | **HEAD** /plugin_providers | Stats of the list of plugin_provider on the system to create plugins
[**list_plugin_providers**](PluginProvidersApi.md#list_plugin_providers) | **GET** /plugin_providers | Lists possible plugin_provider on the system to create plugins
[**upload_plugin_provider**](PluginProvidersApi.md#upload_plugin_provider) | **POST** /plugin_providers/{name} | Upload a plugin provider to a specific {name}.


# **delete_plugin_provider**
> delete_plugin_provider(name)

Delete a plugin provider

The plugin provider will be removed from the system.

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
api_instance = drppy_client.PluginProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 

try:
    # Delete a plugin provider
    api_instance.delete_plugin_provider(name)
except ApiException as e:
    print("Exception when calling PluginProvidersApi->delete_plugin_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_plugin_provider**
> PluginProvider get_plugin_provider(name)

Get a specific plugin with {name}

Get a specific plugin specified by {name}.

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
api_instance = drppy_client.PluginProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 

try:
    # Get a specific plugin with {name}
    api_response = api_instance.get_plugin_provider(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PluginProvidersApi->get_plugin_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

[**PluginProvider**](PluginProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_plugin_provider_binary**
> object get_plugin_provider_binary(name)

Get the binary for a specific plugin provider by {name}

Get a specific plugin provider binary specified by {name}

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
api_instance = drppy_client.PluginProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 

try:
    # Get the binary for a specific plugin provider by {name}
    api_response = api_instance.get_plugin_provider_binary(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PluginProvidersApi->get_plugin_provider_binary: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_plugin_provider**
> head_plugin_provider()

See if a Plugin Provider exists

Return 200 if the Plugin Provider specified by {name} exists, or return NotFound.

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
api_instance = drppy_client.PluginProvidersApi(drppy_client.ApiClient(configuration))

try:
    # See if a Plugin Provider exists
    api_instance.head_plugin_provider()
except ApiException as e:
    print("Exception when calling PluginProvidersApi->head_plugin_provider: %s\n" % e)
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

# **head_plugin_providers**
> list[PluginProvider] head_plugin_providers(name)

Stats of the list of plugin_provider on the system to create plugins

Stats of the list of plugin_provider on the system to create plugins

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
api_instance = drppy_client.PluginProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 

try:
    # Stats of the list of plugin_provider on the system to create plugins
    api_response = api_instance.head_plugin_providers(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PluginProvidersApi->head_plugin_providers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

[**list[PluginProvider]**](PluginProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_plugin_providers**
> list[PluginProvider] list_plugin_providers()

Lists possible plugin_provider on the system to create plugins

Lists possible plugin_provider on the system to create plugins

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
api_instance = drppy_client.PluginProvidersApi(drppy_client.ApiClient(configuration))

try:
    # Lists possible plugin_provider on the system to create plugins
    api_response = api_instance.list_plugin_providers()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PluginProvidersApi->list_plugin_providers: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[PluginProvider]**](PluginProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_plugin_provider**
> PluginProviderUploadInfo upload_plugin_provider(name, replace_writable=replace_writable, body=body)

Upload a plugin provider to a specific {name}.

Upload a plugin provider to a specific {name}.

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
api_instance = drppy_client.PluginProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 
replace_writable = 'replace_writable_example' # str |  (optional)
body = NULL # object |  (optional)

try:
    # Upload a plugin provider to a specific {name}.
    api_response = api_instance.upload_plugin_provider(name, replace_writable=replace_writable, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PluginProvidersApi->upload_plugin_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **replace_writable** | **str**|  | [optional] 
 **body** | **object**|  | [optional] 

### Return type

[**PluginProviderUploadInfo**](PluginProviderUploadInfo.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

