# drppy_client.ObjectsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_objects**](ObjectsApi.md#list_objects) | **GET** /objects | Lists the object types in the system


# **list_objects**
> ObjectPrefixes list_objects()

Lists the object types in the system

Lists the object types in the system

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
api_instance = drppy_client.ObjectsApi(drppy_client.ApiClient(configuration))

try:
    # Lists the object types in the system
    api_response = api_instance.list_objects()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectsApi->list_objects: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ObjectPrefixes**](ObjectPrefixes.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

