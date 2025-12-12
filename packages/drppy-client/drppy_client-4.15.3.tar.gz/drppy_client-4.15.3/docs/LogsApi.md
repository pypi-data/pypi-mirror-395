# drppy_client.LogsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_logs**](LogsApi.md#get_logs) | **GET** /logs | Return current contents of the log buffer


# **get_logs**
> list[Line] get_logs()

Return current contents of the log buffer

Return current contents of the log buffer

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
api_instance = drppy_client.LogsApi(drppy_client.ApiClient(configuration))

try:
    # Return current contents of the log buffer
    api_response = api_instance.get_logs()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LogsApi->get_logs: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Line]**](Line.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

