# drppy_client.MetaApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_meta**](MetaApi.md#get_meta) | **GET** /meta/{type}/{id} | Get Metadata for an Object of {type} idendified by {id}
[**patch_meta**](MetaApi.md#patch_meta) | **PATCH** /meta/{type}/{id} | Patch metadata on an Object of {type} with an ID of {id}


# **get_meta**
> Meta get_meta(type, id)

Get Metadata for an Object of {type} idendified by {id}

Get the appropriate Metadata or return NotFound.

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
api_instance = drppy_client.MetaApi(drppy_client.ApiClient(configuration))
type = 'type_example' # str | 
id = 'id_example' # str | 

try:
    # Get Metadata for an Object of {type} idendified by {id}
    api_response = api_instance.get_meta(type, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MetaApi->get_meta: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**Meta**](Meta.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_meta**
> Meta patch_meta(type, id)

Patch metadata on an Object of {type} with an ID of {id}

Update metadata on a specific Object using a RFC6902 Patch structure

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
api_instance = drppy_client.MetaApi(drppy_client.ApiClient(configuration))
type = 'type_example' # str | 
id = 'id_example' # str | 

try:
    # Patch metadata on an Object of {type} with an ID of {id}
    api_response = api_instance.patch_meta(type, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MetaApi->patch_meta: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**Meta**](Meta.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

