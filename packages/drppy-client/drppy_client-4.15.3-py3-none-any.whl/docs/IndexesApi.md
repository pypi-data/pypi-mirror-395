# drppy_client.IndexesApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_index**](IndexesApi.md#get_index) | **GET** /indexes/{prefix} | Get static indexes for a specific object type
[**get_single_index**](IndexesApi.md#get_single_index) | **GET** /indexes/{prefix}/{param} | Get information on a specific index for a specific object type.
[**list_indexes**](IndexesApi.md#list_indexes) | **GET** /indexes | List all static indexes for objects


# **get_index**
> dict(str, Index) get_index(prefix)

Get static indexes for a specific object type

Get static indexes for a specific object type

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
api_instance = drppy_client.IndexesApi(drppy_client.ApiClient(configuration))
prefix = 'prefix_example' # str | 

try:
    # Get static indexes for a specific object type
    api_response = api_instance.get_index(prefix)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IndexesApi->get_index: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prefix** | **str**|  | 

### Return type

[**dict(str, Index)**](Index.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_single_index**
> dict(str, Index) get_single_index(prefix, param)

Get information on a specific index for a specific object type.

Unlike the other routes, you can probe for parameter-defined indexes using this route.

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
api_instance = drppy_client.IndexesApi(drppy_client.ApiClient(configuration))
prefix = 'prefix_example' # str | 
param = 'param_example' # str | 

try:
    # Get information on a specific index for a specific object type.
    api_response = api_instance.get_single_index(prefix, param)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IndexesApi->get_single_index: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prefix** | **str**|  | 
 **param** | **str**|  | 

### Return type

[**dict(str, Index)**](Index.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_indexes**
> dict(str, dict(str, Index)) list_indexes()

List all static indexes for objects

List all static indexes for objects

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
api_instance = drppy_client.IndexesApi(drppy_client.ApiClient(configuration))

try:
    # List all static indexes for objects
    api_response = api_instance.list_indexes()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IndexesApi->list_indexes: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**dict(str, dict(str, Index))**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

