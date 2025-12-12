# drppy_client.IsosApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_iso**](IsosApi.md#delete_iso) | **DELETE** /isos/{path} | Delete an iso to a specific {path} in the tree under isos.
[**get_iso**](IsosApi.md#get_iso) | **GET** /isos/{path} | Get a specific Iso with {path}
[**list_isos**](IsosApi.md#list_isos) | **GET** /isos | Lists isos in isos directory
[**upload_iso**](IsosApi.md#upload_iso) | **POST** /isos/{path} | Upload an iso to a specific {path} in the tree under isos.


# **delete_iso**
> delete_iso(path)

Delete an iso to a specific {path} in the tree under isos.

The iso will be removed from the {path} in /isos.

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
api_instance = drppy_client.IsosApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str | 

try:
    # Delete an iso to a specific {path} in the tree under isos.
    api_instance.delete_iso(path)
except ApiException as e:
    print("Exception when calling IsosApi->delete_iso: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_iso**
> object get_iso(path)

Get a specific Iso with {path}

Get a specific iso specified by {path} under isos.

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
api_instance = drppy_client.IsosApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str | 

try:
    # Get a specific Iso with {path}
    api_response = api_instance.get_iso(path)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IsosApi->get_iso: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_isos**
> IsoPaths list_isos()

Lists isos in isos directory

Lists the isos in a directory under /isos.

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
api_instance = drppy_client.IsosApi(drppy_client.ApiClient(configuration))

try:
    # Lists isos in isos directory
    api_response = api_instance.list_isos()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IsosApi->list_isos: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**IsoPaths**](IsoPaths.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_iso**
> BlobInfo upload_iso(path, body=body)

Upload an iso to a specific {path} in the tree under isos.

The iso will be uploaded to the {path} in /isos.  The {path} will be created.

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
api_instance = drppy_client.IsosApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str | 
body = NULL # object |  (optional)

try:
    # Upload an iso to a specific {path} in the tree under isos.
    api_response = api_instance.upload_iso(path, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IsosApi->upload_iso: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

[**BlobInfo**](BlobInfo.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

