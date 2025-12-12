# drppy_client.ConnectionsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_connection**](ConnectionsApi.md#get_connection) | **GET** /connections/{id} | Close a websocket Connection
[**get_connection_0**](ConnectionsApi.md#get_connection_0) | **DELETE** /connections/{remoteaddr} | Close a websocket Connection
[**list_connections**](ConnectionsApi.md#list_connections) | **GET** /clusters/:uuid/connections | Lists Connections filtered by some parameters.
[**list_connections_0**](ConnectionsApi.md#list_connections_0) | **GET** /connections | Lists Connections filtered by some parameters
[**list_connections_1**](ConnectionsApi.md#list_connections_1) | **GET** /machines/:uuid/connections | Lists Connections filtered by some parameters.
[**list_connections_2**](ConnectionsApi.md#list_connections_2) | **GET** /resource_brokers/:uuid/connections | Lists Connections filtered by some parameters.


# **get_connection**
> Connection get_connection(id)

Close a websocket Connection

Close a websocket Connection specified by {remoteaddr} or return NotFound.

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
api_instance = drppy_client.ConnectionsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Close a websocket Connection
    api_response = api_instance.get_connection(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->get_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**Connection**](Connection.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connection_0**
> Connection get_connection_0(id)

Close a websocket Connection

Close a websocket Connection specified by {remoteaddr} or return NotFound.

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
api_instance = drppy_client.ConnectionsApi(drppy_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Close a websocket Connection
    api_response = api_instance.get_connection_0(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->get_connection_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**Connection**](Connection.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connections**
> list[Connection] list_connections()

Lists Connections filtered by some parameters.

This will show Connections with principal filtered by runner:<:uuid> by default.  Functional Indexs: RemoteAddr = IP Address with Port Type = string Principal = string CreateTime = datetime  Functions: Eq(value) = Return items that are equal to value Lt(value) = Return items that are less than value Lte(value) = Return items that less than or equal to value Gt(value) = Return items that are greater than value Gte(value) = Return items that greater than or equal to value Between(lower,upper) = Return items that are inclusively between lower and upper Except(lower,upper) = Return items that are not inclusively between lower and upper  Example: Type=api - returns items typed api RemoteAddr=Lt(192.168.1.255:0) - returns that have an ip less than 192.168.1.255:0 RemoteAddr=Lt(192.168.1.255:0)&Type=websocket - returns items with Type websocket and an IP that is less than 192.168.1.255:0

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
api_instance = drppy_client.ConnectionsApi(drppy_client.ApiClient(configuration))

try:
    # Lists Connections filtered by some parameters.
    api_response = api_instance.list_connections()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->list_connections: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Connection]**](Connection.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connections_0**
> list[Connection] list_connections_0()

Lists Connections filtered by some parameters

This will show Connections without unknown principal by default.  Functional Indexs: RemoteAddr = IP Address with Port Type = string Principal = string CreateTime = datetime  Functions: Eq(value) = Return items that are equal to value Lt(value) = Return items that are less than value Lte(value) = Return items that less than or equal to value Gt(value) = Return items that are greater than value Gte(value) = Return items that greater than or equal to value Between(lower,upper) = Return items that are inclusively between lower and upper Except(lower,upper) = Return items that are not inclusively between lower and upper  Example: Type=api - returns items typed api RemoteAddr=Lt(192.168.1.255:0) - returns that have an ip less than 192.168.1.255:0 RemoteAddr=Lt(192.168.1.255:0)&Type=websocket - returns items with Type websocket and an IP that is less than 192.168.1.255:0

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
api_instance = drppy_client.ConnectionsApi(drppy_client.ApiClient(configuration))

try:
    # Lists Connections filtered by some parameters
    api_response = api_instance.list_connections_0()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->list_connections_0: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Connection]**](Connection.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connections_1**
> list[Connection] list_connections_1()

Lists Connections filtered by some parameters.

This will show Connections with principal filtered by runner:<:uuid> by default.  Functional Indexs: RemoteAddr = IP Address with Port Type = string Principal = string CreateTime = datetime  Functions: Eq(value) = Return items that are equal to value Lt(value) = Return items that are less than value Lte(value) = Return items that less than or equal to value Gt(value) = Return items that are greater than value Gte(value) = Return items that greater than or equal to value Between(lower,upper) = Return items that are inclusively between lower and upper Except(lower,upper) = Return items that are not inclusively between lower and upper  Example: Type=api - returns items typed api RemoteAddr=Lt(192.168.1.255:0) - returns that have an ip less than 192.168.1.255:0 RemoteAddr=Lt(192.168.1.255:0)&Type=websocket - returns items with Type websocket and an IP that is less than 192.168.1.255:0

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
api_instance = drppy_client.ConnectionsApi(drppy_client.ApiClient(configuration))

try:
    # Lists Connections filtered by some parameters.
    api_response = api_instance.list_connections_1()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->list_connections_1: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Connection]**](Connection.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connections_2**
> list[Connection] list_connections_2()

Lists Connections filtered by some parameters.

This will show Connections with principal filtered by runner:<:uuid> by default.  Functional Indexs: RemoteAddr = IP Address with Port Type = string Principal = string CreateTime = datetime  Functions: Eq(value) = Return items that are equal to value Lt(value) = Return items that are less than value Lte(value) = Return items that less than or equal to value Gt(value) = Return items that are greater than value Gte(value) = Return items that greater than or equal to value Between(lower,upper) = Return items that are inclusively between lower and upper Except(lower,upper) = Return items that are not inclusively between lower and upper  Example: Type=api - returns items typed api RemoteAddr=Lt(192.168.1.255:0) - returns that have an ip less than 192.168.1.255:0 RemoteAddr=Lt(192.168.1.255:0)&Type=websocket - returns items with Type websocket and an IP that is less than 192.168.1.255:0

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
api_instance = drppy_client.ConnectionsApi(drppy_client.ApiClient(configuration))

try:
    # Lists Connections filtered by some parameters.
    api_response = api_instance.list_connections_2()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsApi->list_connections_2: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Connection]**](Connection.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

