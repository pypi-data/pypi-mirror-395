# drppy_client.ContentsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_content**](ContentsApi.md#create_content) | **POST** /contents | Create content into Digital Rebar Provision
[**delete_content**](ContentsApi.md#delete_content) | **DELETE** /contents/{name} | Delete a content set.
[**get_content**](ContentsApi.md#get_content) | **GET** /contents/{name} | Get a specific content with {name}
[**list_contents**](ContentsApi.md#list_contents) | **GET** /contents | Lists possible contents on the system to serve DHCP
[**upload_content**](ContentsApi.md#upload_content) | **PUT** /contents/{name} | Replace content in Digital Rebar Provision


# **create_content**
> ContentSummary create_content(replace_writable=replace_writable, body=body)

Create content into Digital Rebar Provision

Create content into Digital Rebar Provision

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
api_instance = drppy_client.ContentsApi(drppy_client.ApiClient(configuration))
replace_writable = 'replace_writable_example' # str |  (optional)
body = drppy_client.Content() # Content |  (optional)

try:
    # Create content into Digital Rebar Provision
    api_response = api_instance.create_content(replace_writable=replace_writable, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContentsApi->create_content: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **replace_writable** | **str**|  | [optional] 
 **body** | [**Content**](Content.md)|  | [optional] 

### Return type

[**ContentSummary**](ContentSummary.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_content**
> delete_content(name)

Delete a content set.

Delete a content set.

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
api_instance = drppy_client.ContentsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 

try:
    # Delete a content set.
    api_instance.delete_content(name)
except ApiException as e:
    print("Exception when calling ContentsApi->delete_content: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_content**
> Content get_content(name)

Get a specific content with {name}

Get a specific content specified by {name}.

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
api_instance = drppy_client.ContentsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 

try:
    # Get a specific content with {name}
    api_response = api_instance.get_content(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContentsApi->get_content: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

[**Content**](Content.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_contents**
> list[ContentSummary] list_contents()

Lists possible contents on the system to serve DHCP

Lists possible contents on the system to serve DHCP

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
api_instance = drppy_client.ContentsApi(drppy_client.ApiClient(configuration))

try:
    # Lists possible contents on the system to serve DHCP
    api_response = api_instance.list_contents()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContentsApi->list_contents: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ContentSummary]**](ContentSummary.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_content**
> ContentSummary upload_content(name, replace_writable=replace_writable, body=body)

Replace content in Digital Rebar Provision

Replace content in Digital Rebar Provision

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
api_instance = drppy_client.ContentsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | 
replace_writable = 'replace_writable_example' # str |  (optional)
body = drppy_client.Content() # Content |  (optional)

try:
    # Replace content in Digital Rebar Provision
    api_response = api_instance.upload_content(name, replace_writable=replace_writable, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContentsApi->upload_content: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **replace_writable** | **str**|  | [optional] 
 **body** | [**Content**](Content.md)|  | [optional] 

### Return type

[**ContentSummary**](ContentSummary.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

