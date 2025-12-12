# swagger_client.ConnectionApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**by**](ConnectionApi.md#by) | **GET** /connections/{remoteaddr} | Get a Connection


# **by**
> Connection by()

Get a Connection

Get the Connection specified by {remoteaddr} or return NotFound.

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
api_instance = drppy_client.ConnectionApi(drppy_client.ApiClient(configuration))

try:
    # Get a Connection
    api_response = api_instance.by()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionApi->by: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Connection**](Connection.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

