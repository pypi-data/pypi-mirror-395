# drppy_client.FilesApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_file**](FilesApi.md#delete_file) | **DELETE** /files/{path} | Delete a file to a specific {path} in the tree under files.
[**get_file**](FilesApi.md#get_file) | **GET** /files/{path} | Get a specific File with {path}
[**head_file**](FilesApi.md#head_file) | **HEAD** /files/{path} | See if a file exists and return a checksum in the header
[**head_iso**](FilesApi.md#head_iso) | **HEAD** /isos/{path} | See if a iso exists and return a checksum in the header
[**list_files**](FilesApi.md#list_files) | **GET** /files | Lists files in files directory or subdirectory per query parameter
[**upload_file**](FilesApi.md#upload_file) | **POST** /files/{path} | Upload a file to a specific {path} in the tree under files.


# **delete_file**
> delete_file(path, explode=explode)

Delete a file to a specific {path} in the tree under files.

The file will be removed from the {path} in /files.

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
api_instance = drppy_client.FilesApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str | 
explode = 'explode_example' # str | in: explode (optional)

try:
    # Delete a file to a specific {path} in the tree under files.
    api_instance.delete_file(path, explode=explode)
except ApiException as e:
    print("Exception when calling FilesApi->delete_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | 
 **explode** | **str**| in: explode | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file**
> str get_file(path, explode=explode)

Get a specific File with {path}

Get a specific file specified by {path} under files.

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
api_instance = drppy_client.FilesApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str | 
explode = 'explode_example' # str | in: explode (optional)

try:
    # Get a specific File with {path}
    api_response = api_instance.get_file(path, explode=explode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->get_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | 
 **explode** | **str**| in: explode | [optional] 

### Return type

**str**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_file**
> head_file(path, explode=explode)

See if a file exists and return a checksum in the header

Return 200 if the file specified by {path} exists, or return NotFound.

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
api_instance = drppy_client.FilesApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str | 
explode = 'explode_example' # str | in: explode (optional)

try:
    # See if a file exists and return a checksum in the header
    api_instance.head_file(path, explode=explode)
except ApiException as e:
    print("Exception when calling FilesApi->head_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | 
 **explode** | **str**| in: explode | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_iso**
> head_iso(path)

See if a iso exists and return a checksum in the header

Return 200 if the iso specified by {path} exists, or return NotFound.

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
api_instance = drppy_client.FilesApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str | 

try:
    # See if a iso exists and return a checksum in the header
    api_instance.head_iso(path)
except ApiException as e:
    print("Exception when calling FilesApi->head_iso: %s\n" % e)
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

# **list_files**
> FilePaths list_files(path=path, all=all)

Lists files in files directory or subdirectory per query parameter

Lists the files in a directory under /files.  path=<path to return> Path defaults to /

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
api_instance = drppy_client.FilesApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str |  (optional)
all = true # bool |  (optional)

try:
    # Lists files in files directory or subdirectory per query parameter
    api_response = api_instance.list_files(path=path, all=all)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | [optional] 
 **all** | **bool**|  | [optional] 

### Return type

[**FilePaths**](FilePaths.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_file**
> BlobInfo upload_file(path, explode=explode, body=body)

Upload a file to a specific {path} in the tree under files.

The file will be uploaded to the {path} in /files.  The {path} will be created.

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
api_instance = drppy_client.FilesApi(drppy_client.ApiClient(configuration))
path = 'path_example' # str | 
explode = 'explode_example' # str | in: explode (optional)
body = NULL # object |  (optional)

try:
    # Upload a file to a specific {path} in the tree under files.
    api_response = api_instance.upload_file(path, explode=explode, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->upload_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | 
 **explode** | **str**| in: explode | [optional] 
 **body** | **object**|  | [optional] 

### Return type

[**BlobInfo**](BlobInfo.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

