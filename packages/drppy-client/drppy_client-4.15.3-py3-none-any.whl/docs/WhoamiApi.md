# drppy_client.WhoamiApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**fill_whoami**](WhoamiApi.md#fill_whoami) | **POST** /whoami | Fills a Whoami with the closest matching Machine


# **fill_whoami**
> Whoami fill_whoami(body=body)

Fills a Whoami with the closest matching Machine

This will fill the Result section of the passed-in Whoami with the Machine information that most closely matches the Fingerprint and MacAddrs fields.  If there were no close enough matches, Score will stay at zero, the Uuid field will not be valid, and no Token will be present.

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
api_instance = drppy_client.WhoamiApi(drppy_client.ApiClient(configuration))
body = drppy_client.Whoami() # Whoami |  (optional)

try:
    # Fills a Whoami with the closest matching Machine
    api_response = api_instance.fill_whoami(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WhoamiApi->fill_whoami: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Whoami**](Whoami.md)|  | [optional] 

### Return type

[**Whoami**](Whoami.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

