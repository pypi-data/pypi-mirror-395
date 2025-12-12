# drppy_client.InterfacesApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_interface**](InterfacesApi.md#get_interface) | **GET** /interfaces/{name} | Get a specific interface with {name}
[**list_interfaces**](InterfacesApi.md#list_interfaces) | **GET** /interfaces | Lists possible interfaces on the system to serve DHCP


# **get_interface**
> Interface get_interface(name)

Get a specific interface with {name}

Get a specific interface specified by {name}.

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
api_instance = drppy_client.InterfacesApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 

try:
    # Get a specific interface with {name}
    api_response = api_instance.get_interface(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InterfacesApi->get_interface: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

[**Interface**](Interface.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_interfaces**
> list[Interface] list_interfaces()

Lists possible interfaces on the system to serve DHCP

Lists possible interfaces on the system to serve DHCP

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
api_instance = drppy_client.InterfacesApi(drppy_client.ApiClient(configuration))

try:
    # Lists possible interfaces on the system to serve DHCP
    api_response = api_instance.list_interfaces()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InterfacesApi->list_interfaces: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Interface]**](Interface.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

