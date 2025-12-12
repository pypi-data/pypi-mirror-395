# drppy_client.SubnetsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**allocate_subnet**](SubnetsApi.md#allocate_subnet) | **POST** /subnets/{name}/allocate | Allocate or reserve an address in the subnet
[**create_subnet**](SubnetsApi.md#create_subnet) | **POST** /subnets | Create a Subnet
[**del_subnet_release**](SubnetsApi.md#del_subnet_release) | **DELETE** /subnets/{name}/release/{ip} | Release IP address from the Subnet name
[**delete_subnet**](SubnetsApi.md#delete_subnet) | **DELETE** /subnets/{name} | Delete a Subnet
[**delete_subnet_param**](SubnetsApi.md#delete_subnet_param) | **DELETE** /subnets/{name}/params/{key} | Delete a single subnets parameter
[**get_subnet**](SubnetsApi.md#get_subnet) | **GET** /subnets/{name} | Get a Subnet
[**get_subnet_action**](SubnetsApi.md#get_subnet_action) | **GET** /subnets/{name}/actions/{cmd} | List specific action for a subnets Subnet
[**get_subnet_actions**](SubnetsApi.md#get_subnet_actions) | **GET** /subnets/{name}/actions | List subnets actions Subnet
[**get_subnet_param**](SubnetsApi.md#get_subnet_param) | **GET** /subnets/{name}/params/{key} | Get a single subnets parameter
[**get_subnet_params**](SubnetsApi.md#get_subnet_params) | **GET** /subnets/{name}/params | List subnets params Subnet
[**get_subnet_pub_key**](SubnetsApi.md#get_subnet_pub_key) | **GET** /subnets/{name}/pubkey | Get the public key for secure params on a subnets
[**head_subnet**](SubnetsApi.md#head_subnet) | **HEAD** /subnets/{name} | See if a Subnet exists
[**list_stats_subnets**](SubnetsApi.md#list_stats_subnets) | **HEAD** /subnets | Stats of the List Subnets filtered by some parameters.
[**list_subnets**](SubnetsApi.md#list_subnets) | **GET** /subnets | Lists Subnets filtered by some parameters.
[**patch_subnet**](SubnetsApi.md#patch_subnet) | **PATCH** /subnets/{name} | Patch a Subnet
[**patch_subnet_params**](SubnetsApi.md#patch_subnet_params) | **PATCH** /subnets/{name}/params | Update all params on the object (merges with existing data)
[**post_subnet_action**](SubnetsApi.md#post_subnet_action) | **POST** /subnets/{name}/actions/{cmd} | Call an action on the node.
[**post_subnet_param**](SubnetsApi.md#post_subnet_param) | **POST** /subnets/{name}/params/{key} | Set a single parameter on an object
[**post_subnet_params**](SubnetsApi.md#post_subnet_params) | **POST** /subnets/{name}/params | Replaces all parameters on the object
[**put_subnet**](SubnetsApi.md#put_subnet) | **PUT** /subnets/{name} | Put a Subnet


# **allocate_subnet**
> Reservation allocate_subnet(name, body, commented=commented, reduced=reduced)

Allocate or reserve an address in the subnet

Input is a reservation object.  It can me empty and unfilled.  These fields configure the reservation (only) Addr - optional address to reserve Machine - optional machine to reserve for Parameter - opttional parameter to place the address for the machine Token     - optional mac address to reserve

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Key of the object
body = drppy_client.Reservation() # Reservation | Reservation Object to define the allocation requirements (IP or MAC Address)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Allocate or reserve an address in the subnet
    api_response = api_instance.allocate_subnet(name, body, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->allocate_subnet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Key of the object | 
 **body** | [**Reservation**](Reservation.md)| Reservation Object to define the allocation requirements (IP or MAC Address) | 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Reservation**](Reservation.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_subnet**
> Subnet create_subnet(body)

Create a Subnet

Create a Subnet from the provided object

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Subnet() # Subnet | 

try:
    # Create a Subnet
    api_response = api_instance.create_subnet(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->create_subnet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Subnet**](Subnet.md)|  | 

### Return type

[**Subnet**](Subnet.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **del_subnet_release**
> Reservation del_subnet_release(name, ip, commented=commented, reduced=reduced)

Release IP address from the Subnet name

Release IP address from the Subnet name

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Key of the object
ip = 'ip_example' # str | IP to release
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Release IP address from the Subnet name
    api_response = api_instance.del_subnet_release(name, ip, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->del_subnet_release: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Key of the object | 
 **ip** | **str**| IP to release | 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Reservation**](Reservation.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_subnet**
> Subnet delete_subnet(name, force=force, commented=commented, reduced=reduced)

Delete a Subnet

Delete a Subnet specified by {name}

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a Subnet
    api_response = api_instance.delete_subnet(name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->delete_subnet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Subnet**](Subnet.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_subnet_param**
> object delete_subnet_param()

Delete a single subnets parameter

Delete a single parameter {key} for a Subnet specified by {name}

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))

try:
    # Delete a single subnets parameter
    api_response = api_instance.delete_subnet_param()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->delete_subnet_param: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subnet**
> Subnet get_subnet(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a Subnet

Get the Subnet specified by {name}  or return NotFound.

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a Subnet
    api_response = api_instance.get_subnet(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->get_subnet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Subnet**](Subnet.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subnet_action**
> AvailableAction get_subnet_action(name, cmd, plugin=plugin)

List specific action for a subnets Subnet

List specific {cmd} action for a Subnet specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a subnets Subnet
    api_response = api_instance.get_subnet_action(name, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->get_subnet_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 
 **cmd** | **str**| The action to run on the plugin | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**AvailableAction**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subnet_actions**
> list[AvailableAction] get_subnet_actions(name, plugin=plugin)

List subnets actions Subnet

List Subnet actions for a Subnet specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List subnets actions Subnet
    api_response = api_instance.get_subnet_actions(name, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->get_subnet_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subnet_param**
> object get_subnet_param(name, key, aggregate=aggregate, decode=decode)

Get a single subnets parameter

Get a single parameter {key} for a Subnet specified by {name}

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet
key = 'key_example' # str | Param name
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)

try:
    # Get a single subnets parameter
    api_response = api_instance.get_subnet_param(name, key, aggregate=aggregate, decode=decode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->get_subnet_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 
 **key** | **str**| Param name | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subnet_params**
> dict(str, object) get_subnet_params(name, aggregate=aggregate, decode=decode, params=params)

List subnets params Subnet

List Subnet parms for a Subnet specified by {name}

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
params = 'params_example' # str |  (optional)

try:
    # List subnets params Subnet
    api_response = api_instance.get_subnet_params(name, aggregate=aggregate, decode=decode, params=params)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->get_subnet_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **params** | **str**|  | [optional] 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subnet_pub_key**
> get_subnet_pub_key(name)

Get the public key for secure params on a subnets

Get the public key for a Subnet specified by {name}

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet

try:
    # Get the public key for secure params on a subnets
    api_instance.get_subnet_pub_key(name)
except ApiException as e:
    print("Exception when calling SubnetsApi->get_subnet_pub_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_subnet**
> head_subnet(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a Subnet exists

Return 200 if the Subnet specifiec by {name} exists, or return NotFound.

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a Subnet exists
    api_instance.head_subnet(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling SubnetsApi->head_subnet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_stats_subnets**
> list_stats_subnets(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, active_end=active_end, active_lease_time=active_lease_time, active_start=active_start, allocate_end=allocate_end, allocate_start=allocate_start, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, enabled=enabled, endpoint=endpoint, errors=errors, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, name=name, next_server=next_server, only_reservations=only_reservations, options=options, params2=params2, pickers=pickers, prefix_parameter=prefix_parameter, profiles=profiles, proxy=proxy, read_only=read_only, reserved_lease_time=reserved_lease_time, skip_dad=skip_dad, strategy=strategy, subnet=subnet, unmanaged=unmanaged, validated=validated)

Stats of the List Subnets filtered by some parameters.

This will return headers with the stats of the list.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> range-only = returns only counts of the objects in the groups.<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
offset = 789 # int | The page offset (0-based) into limit per page pages (optional)
limit = 789 # int | The number of objects to return (optional)
filter = 'filter_example' # str | A named filter to user in restricting the query (optional)
raw = 'raw_example' # str | A raw query string to proess (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
group_by = 'group_by_example' # str | A field generate groups from. Can be specified multiple times (optional)
params = 'params_example' # str | A comma separated list of parameters to include in the Params field (optional)
range_only = true # bool | Indicates that only the counts of the objects should be returned for a group-by field (optional)
reverse = true # bool | Indicates that the reverse order of the sort. (optional)
slim = 'slim_example' # str | A comma separated list of fields to remove from the returned objects (optional)
sort = 'sort_example' # str | A field to sort the results by. Multiple can be specified Searches are applied in order across all results. (optional)
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)
active_end = 'active_end_example' # str | ActiveEnd is the last non-reserved IP address we will hand non-reserved leases from. (optional)
active_lease_time = 'active_lease_time_example' # str | ActiveLeaseTime is the default lease duration in seconds we will hand out to leases that do not have a reservation. (optional)
active_start = 'active_start_example' # str | ActiveStart is the first non-reserved IP address we will hand non-reserved leases from. (optional)
allocate_end = 'allocate_end_example' # str | AllocateEnd is the last IP address we will hand out on allocation calls 0.0.0.0/unset means last address in CIDR (optional)
allocate_start = 'allocate_start_example' # str | AllocateStart is the first IP address we will hand out on allocation calls 0.0.0.0/unset means first address in CIDR (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
enabled = 'enabled_example' # str | Enabled indicates if the subnet should hand out leases or continue operating leases if already running. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | Name is the name of the subnet. Subnet names must be unique (optional)
next_server = 'next_server_example' # str | NextServer is the IP address of next server to use in the bootstrap process. The next server address is returned in DHCPOFFER, DHCPACK by the DHCP server. (optional)
only_reservations = 'only_reservations_example' # str | OnlyReservations indicates that we will only allow leases for which there is a preexisting reservation. (optional)
options = 'options_example' # str | Additional options to send to DHCP clients (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
pickers = 'pickers_example' # str | Pickers is list of methods that will allocate IP addresses. Each string must refer to a valid address picking strategy.  The current ones are:  \"none\", which will refuse to hand out an address and refuse to try any remaining strategies.  \"hint\", which will try to reuse the address that the DHCP packet is requesting, if it has one.  If the request does not have a requested address, \"hint\" will fall through to the next strategy. Otherwise, it will refuse to try any remaining strategies whether or not it can satisfy the request.  This should force the client to fall back to DHCPDISCOVER with no requsted IP address. \"hint\" will reuse expired leases and unexpired leases that match on the requested address, strategy, and token.  \"nextFree\", which will try to create a Lease with the next free address in the subnet active range.  It will fall through to the next strategy if it cannot find a free IP. \"nextFree\" only considers addresses that do not have a lease, whether or not the lease is expired.  \"mostExpired\" will try to recycle the most expired lease in the subnet's active range.  All of the address allocation strategies do not consider any addresses that are reserved, as lease creation will be handled by the reservation instead.  We will consider adding more address allocation strategies in the future. (optional)
prefix_parameter = 'prefix_parameter_example' # str | PrefixParameter a string that should be the beginning of a set of option-based parameters (optional)
profiles = 'profiles_example' # str | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. (optional)
proxy = 'proxy_example' # str | Proxy indicates if the subnet should act as a proxy DHCP server. If true, the subnet will not manage ip addresses but will send offers to requests.  It is an error for Proxy and Unmanaged to be true. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
reserved_lease_time = 'reserved_lease_time_example' # str | ReservedLeasTime is the default lease time we will hand out to leases created from a reservation in our subnet. (optional)
skip_dad = 'skip_dad_example' # str | SkipDAD will cause the DHCP server to skip duplicate address detection via ping testing when in discovery phase.  Only set this if you know nothing in this subnet will ever have address conflicts with any other system. (optional)
strategy = 'strategy_example' # str | Strategy is the leasing strategy that will be used determine what to use from the DHCP packet to handle lease management. (optional)
subnet = 'subnet_example' # str | Subnet is the network address in CIDR form that all leases acquired in its range will use for options, lease times, and NextServer settings by default (optional)
unmanaged = 'unmanaged_example' # str | Unmanaged indicates that dr-provision will never send boot-related options to machines that get leases from this subnet.  If false, dr-provision will send whatever boot-related options it would normally send.  It is an error for Unmanaged and Proxy to both be true. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Stats of the List Subnets filtered by some parameters.
    api_instance.list_stats_subnets(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, active_end=active_end, active_lease_time=active_lease_time, active_start=active_start, allocate_end=allocate_end, allocate_start=allocate_start, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, enabled=enabled, endpoint=endpoint, errors=errors, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, name=name, next_server=next_server, only_reservations=only_reservations, options=options, params2=params2, pickers=pickers, prefix_parameter=prefix_parameter, profiles=profiles, proxy=proxy, read_only=read_only, reserved_lease_time=reserved_lease_time, skip_dad=skip_dad, strategy=strategy, subnet=subnet, unmanaged=unmanaged, validated=validated)
except ApiException as e:
    print("Exception when calling SubnetsApi->list_stats_subnets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| The page offset (0-based) into limit per page pages | [optional] 
 **limit** | **int**| The number of objects to return | [optional] 
 **filter** | **str**| A named filter to user in restricting the query | [optional] 
 **raw** | **str**| A raw query string to proess | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **group_by** | **str**| A field generate groups from. Can be specified multiple times | [optional] 
 **params** | **str**| A comma separated list of parameters to include in the Params field | [optional] 
 **range_only** | **bool**| Indicates that only the counts of the objects should be returned for a group-by field | [optional] 
 **reverse** | **bool**| Indicates that the reverse order of the sort. | [optional] 
 **slim** | **str**| A comma separated list of fields to remove from the returned objects | [optional] 
 **sort** | **str**| A field to sort the results by. Multiple can be specified Searches are applied in order across all results. | [optional] 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 
 **active_end** | **str**| ActiveEnd is the last non-reserved IP address we will hand non-reserved leases from. | [optional] 
 **active_lease_time** | **str**| ActiveLeaseTime is the default lease duration in seconds we will hand out to leases that do not have a reservation. | [optional] 
 **active_start** | **str**| ActiveStart is the first non-reserved IP address we will hand non-reserved leases from. | [optional] 
 **allocate_end** | **str**| AllocateEnd is the last IP address we will hand out on allocation calls 0.0.0.0/unset means last address in CIDR | [optional] 
 **allocate_start** | **str**| AllocateStart is the first IP address we will hand out on allocation calls 0.0.0.0/unset means first address in CIDR | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **enabled** | **str**| Enabled indicates if the subnet should hand out leases or continue operating leases if already running. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| Name is the name of the subnet. Subnet names must be unique | [optional] 
 **next_server** | **str**| NextServer is the IP address of next server to use in the bootstrap process. The next server address is returned in DHCPOFFER, DHCPACK by the DHCP server. | [optional] 
 **only_reservations** | **str**| OnlyReservations indicates that we will only allow leases for which there is a preexisting reservation. | [optional] 
 **options** | **str**| Additional options to send to DHCP clients | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **pickers** | **str**| Pickers is list of methods that will allocate IP addresses. Each string must refer to a valid address picking strategy.  The current ones are:  \&quot;none\&quot;, which will refuse to hand out an address and refuse to try any remaining strategies.  \&quot;hint\&quot;, which will try to reuse the address that the DHCP packet is requesting, if it has one.  If the request does not have a requested address, \&quot;hint\&quot; will fall through to the next strategy. Otherwise, it will refuse to try any remaining strategies whether or not it can satisfy the request.  This should force the client to fall back to DHCPDISCOVER with no requsted IP address. \&quot;hint\&quot; will reuse expired leases and unexpired leases that match on the requested address, strategy, and token.  \&quot;nextFree\&quot;, which will try to create a Lease with the next free address in the subnet active range.  It will fall through to the next strategy if it cannot find a free IP. \&quot;nextFree\&quot; only considers addresses that do not have a lease, whether or not the lease is expired.  \&quot;mostExpired\&quot; will try to recycle the most expired lease in the subnet&#39;s active range.  All of the address allocation strategies do not consider any addresses that are reserved, as lease creation will be handled by the reservation instead.  We will consider adding more address allocation strategies in the future. | [optional] 
 **prefix_parameter** | **str**| PrefixParameter a string that should be the beginning of a set of option-based parameters | [optional] 
 **profiles** | **str**| Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
 **proxy** | **str**| Proxy indicates if the subnet should act as a proxy DHCP server. If true, the subnet will not manage ip addresses but will send offers to requests.  It is an error for Proxy and Unmanaged to be true. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **reserved_lease_time** | **str**| ReservedLeasTime is the default lease time we will hand out to leases created from a reservation in our subnet. | [optional] 
 **skip_dad** | **str**| SkipDAD will cause the DHCP server to skip duplicate address detection via ping testing when in discovery phase.  Only set this if you know nothing in this subnet will ever have address conflicts with any other system. | [optional] 
 **strategy** | **str**| Strategy is the leasing strategy that will be used determine what to use from the DHCP packet to handle lease management. | [optional] 
 **subnet** | **str**| Subnet is the network address in CIDR form that all leases acquired in its range will use for options, lease times, and NextServer settings by default | [optional] 
 **unmanaged** | **str**| Unmanaged indicates that dr-provision will never send boot-related options to machines that get leases from this subnet.  If false, dr-provision will send whatever boot-related options it would normally send.  It is an error for Unmanaged and Proxy to both be true. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_subnets**
> list[Subnet] list_subnets(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, active_end=active_end, active_lease_time=active_lease_time, active_start=active_start, allocate_end=allocate_end, allocate_start=allocate_start, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, enabled=enabled, endpoint=endpoint, errors=errors, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, name=name, next_server=next_server, only_reservations=only_reservations, options=options, params2=params2, pickers=pickers, prefix_parameter=prefix_parameter, profiles=profiles, proxy=proxy, read_only=read_only, reserved_lease_time=reserved_lease_time, skip_dad=skip_dad, strategy=strategy, subnet=subnet, unmanaged=unmanaged, validated=validated)

Lists Subnets filtered by some parameters.

This will show all Subnets by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object. Functions can also be applied against values in the Params field as well. e.g. Params.ipmi/enabled=Eq(true)  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
offset = 789 # int | The page offset (0-based) into limit per page pages (optional)
limit = 789 # int | The number of objects to return (optional)
filter = 'filter_example' # str | A named filter to user in restricting the query (optional)
raw = 'raw_example' # str | A raw query string to proess (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
group_by = 'group_by_example' # str | A field generate groups from. Can be specified multiple times (optional)
params = 'params_example' # str | A comma separated list of parameters to include in the Params field (optional)
range_only = true # bool | Indicates that only the counts of the objects should be returned for a group-by field (optional)
reverse = true # bool | Indicates that the reverse order of the sort. (optional)
slim = 'slim_example' # str | A comma separated list of fields to remove from the returned objects (optional)
sort = 'sort_example' # str | A field to sort the results by. Multiple can be specified Searches are applied in order across all results. (optional)
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)
active_end = 'active_end_example' # str | ActiveEnd is the last non-reserved IP address we will hand non-reserved leases from. (optional)
active_lease_time = 'active_lease_time_example' # str | ActiveLeaseTime is the default lease duration in seconds we will hand out to leases that do not have a reservation. (optional)
active_start = 'active_start_example' # str | ActiveStart is the first non-reserved IP address we will hand non-reserved leases from. (optional)
allocate_end = 'allocate_end_example' # str | AllocateEnd is the last IP address we will hand out on allocation calls 0.0.0.0/unset means last address in CIDR (optional)
allocate_start = 'allocate_start_example' # str | AllocateStart is the first IP address we will hand out on allocation calls 0.0.0.0/unset means first address in CIDR (optional)
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
enabled = 'enabled_example' # str | Enabled indicates if the subnet should hand out leases or continue operating leases if already running. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | Name is the name of the subnet. Subnet names must be unique (optional)
next_server = 'next_server_example' # str | NextServer is the IP address of next server to use in the bootstrap process. The next server address is returned in DHCPOFFER, DHCPACK by the DHCP server. (optional)
only_reservations = 'only_reservations_example' # str | OnlyReservations indicates that we will only allow leases for which there is a preexisting reservation. (optional)
options = 'options_example' # str | Additional options to send to DHCP clients (optional)
params2 = 'params_example' # str | Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn't reference a parameter, the type of the object can be anything.  The system will enforce the named parameter's value's type.  Go calls the \"anything\" parameters as \"interface {}\".  Hence, the type of this field is a map[string]interface{}. (optional)
pickers = 'pickers_example' # str | Pickers is list of methods that will allocate IP addresses. Each string must refer to a valid address picking strategy.  The current ones are:  \"none\", which will refuse to hand out an address and refuse to try any remaining strategies.  \"hint\", which will try to reuse the address that the DHCP packet is requesting, if it has one.  If the request does not have a requested address, \"hint\" will fall through to the next strategy. Otherwise, it will refuse to try any remaining strategies whether or not it can satisfy the request.  This should force the client to fall back to DHCPDISCOVER with no requsted IP address. \"hint\" will reuse expired leases and unexpired leases that match on the requested address, strategy, and token.  \"nextFree\", which will try to create a Lease with the next free address in the subnet active range.  It will fall through to the next strategy if it cannot find a free IP. \"nextFree\" only considers addresses that do not have a lease, whether or not the lease is expired.  \"mostExpired\" will try to recycle the most expired lease in the subnet's active range.  All of the address allocation strategies do not consider any addresses that are reserved, as lease creation will be handled by the reservation instead.  We will consider adding more address allocation strategies in the future. (optional)
prefix_parameter = 'prefix_parameter_example' # str | PrefixParameter a string that should be the beginning of a set of option-based parameters (optional)
profiles = 'profiles_example' # str | Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. (optional)
proxy = 'proxy_example' # str | Proxy indicates if the subnet should act as a proxy DHCP server. If true, the subnet will not manage ip addresses but will send offers to requests.  It is an error for Proxy and Unmanaged to be true. (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
reserved_lease_time = 'reserved_lease_time_example' # str | ReservedLeasTime is the default lease time we will hand out to leases created from a reservation in our subnet. (optional)
skip_dad = 'skip_dad_example' # str | SkipDAD will cause the DHCP server to skip duplicate address detection via ping testing when in discovery phase.  Only set this if you know nothing in this subnet will ever have address conflicts with any other system. (optional)
strategy = 'strategy_example' # str | Strategy is the leasing strategy that will be used determine what to use from the DHCP packet to handle lease management. (optional)
subnet = 'subnet_example' # str | Subnet is the network address in CIDR form that all leases acquired in its range will use for options, lease times, and NextServer settings by default (optional)
unmanaged = 'unmanaged_example' # str | Unmanaged indicates that dr-provision will never send boot-related options to machines that get leases from this subnet.  If false, dr-provision will send whatever boot-related options it would normally send.  It is an error for Unmanaged and Proxy to both be true. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Lists Subnets filtered by some parameters.
    api_response = api_instance.list_subnets(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, active_end=active_end, active_lease_time=active_lease_time, active_start=active_start, allocate_end=allocate_end, allocate_start=allocate_start, available=available, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, enabled=enabled, endpoint=endpoint, errors=errors, last_modified_at=last_modified_at, last_modified_by=last_modified_by, meta=meta, name=name, next_server=next_server, only_reservations=only_reservations, options=options, params2=params2, pickers=pickers, prefix_parameter=prefix_parameter, profiles=profiles, proxy=proxy, read_only=read_only, reserved_lease_time=reserved_lease_time, skip_dad=skip_dad, strategy=strategy, subnet=subnet, unmanaged=unmanaged, validated=validated)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->list_subnets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| The page offset (0-based) into limit per page pages | [optional] 
 **limit** | **int**| The number of objects to return | [optional] 
 **filter** | **str**| A named filter to user in restricting the query | [optional] 
 **raw** | **str**| A raw query string to proess | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **group_by** | **str**| A field generate groups from. Can be specified multiple times | [optional] 
 **params** | **str**| A comma separated list of parameters to include in the Params field | [optional] 
 **range_only** | **bool**| Indicates that only the counts of the objects should be returned for a group-by field | [optional] 
 **reverse** | **bool**| Indicates that the reverse order of the sort. | [optional] 
 **slim** | **str**| A comma separated list of fields to remove from the returned objects | [optional] 
 **sort** | **str**| A field to sort the results by. Multiple can be specified Searches are applied in order across all results. | [optional] 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 
 **active_end** | **str**| ActiveEnd is the last non-reserved IP address we will hand non-reserved leases from. | [optional] 
 **active_lease_time** | **str**| ActiveLeaseTime is the default lease duration in seconds we will hand out to leases that do not have a reservation. | [optional] 
 **active_start** | **str**| ActiveStart is the first non-reserved IP address we will hand non-reserved leases from. | [optional] 
 **allocate_end** | **str**| AllocateEnd is the last IP address we will hand out on allocation calls 0.0.0.0/unset means last address in CIDR | [optional] 
 **allocate_start** | **str**| AllocateStart is the first IP address we will hand out on allocation calls 0.0.0.0/unset means first address in CIDR | [optional] 
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **enabled** | **str**| Enabled indicates if the subnet should hand out leases or continue operating leases if already running. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| Name is the name of the subnet. Subnet names must be unique | [optional] 
 **next_server** | **str**| NextServer is the IP address of next server to use in the bootstrap process. The next server address is returned in DHCPOFFER, DHCPACK by the DHCP server. | [optional] 
 **only_reservations** | **str**| OnlyReservations indicates that we will only allow leases for which there is a preexisting reservation. | [optional] 
 **options** | **str**| Additional options to send to DHCP clients | [optional] 
 **params2** | **str**| Params holds the values of parameters on the object.  The field is a key / value store of the parameters. The key is the name of a parameter.  The key is of type string. The value is the value of the parameter.  The type of the value is defined by the parameter object.  If the key doesn&#39;t reference a parameter, the type of the object can be anything.  The system will enforce the named parameter&#39;s value&#39;s type.  Go calls the \&quot;anything\&quot; parameters as \&quot;interface {}\&quot;.  Hence, the type of this field is a map[string]interface{}. | [optional] 
 **pickers** | **str**| Pickers is list of methods that will allocate IP addresses. Each string must refer to a valid address picking strategy.  The current ones are:  \&quot;none\&quot;, which will refuse to hand out an address and refuse to try any remaining strategies.  \&quot;hint\&quot;, which will try to reuse the address that the DHCP packet is requesting, if it has one.  If the request does not have a requested address, \&quot;hint\&quot; will fall through to the next strategy. Otherwise, it will refuse to try any remaining strategies whether or not it can satisfy the request.  This should force the client to fall back to DHCPDISCOVER with no requsted IP address. \&quot;hint\&quot; will reuse expired leases and unexpired leases that match on the requested address, strategy, and token.  \&quot;nextFree\&quot;, which will try to create a Lease with the next free address in the subnet active range.  It will fall through to the next strategy if it cannot find a free IP. \&quot;nextFree\&quot; only considers addresses that do not have a lease, whether or not the lease is expired.  \&quot;mostExpired\&quot; will try to recycle the most expired lease in the subnet&#39;s active range.  All of the address allocation strategies do not consider any addresses that are reserved, as lease creation will be handled by the reservation instead.  We will consider adding more address allocation strategies in the future. | [optional] 
 **prefix_parameter** | **str**| PrefixParameter a string that should be the beginning of a set of option-based parameters | [optional] 
 **profiles** | **str**| Profiles is an array of profiles to apply to this object in order when looking for a parameter during rendering. | [optional] 
 **proxy** | **str**| Proxy indicates if the subnet should act as a proxy DHCP server. If true, the subnet will not manage ip addresses but will send offers to requests.  It is an error for Proxy and Unmanaged to be true. | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **reserved_lease_time** | **str**| ReservedLeasTime is the default lease time we will hand out to leases created from a reservation in our subnet. | [optional] 
 **skip_dad** | **str**| SkipDAD will cause the DHCP server to skip duplicate address detection via ping testing when in discovery phase.  Only set this if you know nothing in this subnet will ever have address conflicts with any other system. | [optional] 
 **strategy** | **str**| Strategy is the leasing strategy that will be used determine what to use from the DHCP packet to handle lease management. | [optional] 
 **subnet** | **str**| Subnet is the network address in CIDR form that all leases acquired in its range will use for options, lease times, and NextServer settings by default | [optional] 
 **unmanaged** | **str**| Unmanaged indicates that dr-provision will never send boot-related options to machines that get leases from this subnet.  If false, dr-provision will send whatever boot-related options it would normally send.  It is an error for Unmanaged and Proxy to both be true. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

[**list[Subnet]**](Subnet.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_subnet**
> Subnet patch_subnet(body, name, force=force, commented=commented, reduced=reduced)

Patch a Subnet

Update a Subnet specified by {name} using a RFC6902 Patch structure

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
name = 'name_example' # str | Identity key of the Subnet
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a Subnet
    api_response = api_instance.patch_subnet(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->patch_subnet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **name** | **str**| Identity key of the Subnet | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Subnet**](Subnet.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_subnet_params**
> dict(str, object) patch_subnet_params(body, name)

Update all params on the object (merges with existing data)

Update params for Subnet {name} with the passed-in patch

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
name = 'name_example' # str | Identity key of the Subnet

try:
    # Update all params on the object (merges with existing data)
    api_response = api_instance.patch_subnet_params(body, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->patch_subnet_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **name** | **str**| Identity key of the Subnet | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_subnet_action**
> object post_subnet_action(name, cmd, body, plugin=plugin)

Call an action on the node.

Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the Subnet
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_subnet_action(name, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->post_subnet_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the Subnet | 
 **cmd** | **str**| The action to run on the plugin | 
 **body** | **object**| Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {} | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_subnet_param**
> object post_subnet_param(body, name, key)

Set a single parameter on an object

Set as single Parameter {key} for a subnets specified by {name}

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
body = NULL # object | 
name = 'name_example' # str | Identity key of the Subnet
key = 'key_example' # str | Param name

try:
    # Set a single parameter on an object
    api_response = api_instance.post_subnet_param(body, name, key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->post_subnet_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 
 **name** | **str**| Identity key of the Subnet | 
 **key** | **str**| Param name | 

### Return type

**object**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_subnet_params**
> dict(str, object) post_subnet_params(body)

Replaces all parameters on the object

Sets parameters for a subnets specified by {name}

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
body = NULL # object | 

try:
    # Replaces all parameters on the object
    api_response = api_instance.post_subnet_params(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->post_subnet_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 

### Return type

**dict(str, object)**

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_subnet**
> Subnet put_subnet(body, name, force=force, commented=commented, reduced=reduced)

Put a Subnet

Update a Subnet specified by {name} using a JSON Subnet

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
api_instance = drppy_client.SubnetsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Subnet() # Subnet | 
name = 'name_example' # str | Identity key of the Subnet
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a Subnet
    api_response = api_instance.put_subnet(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SubnetsApi->put_subnet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Subnet**](Subnet.md)|  | 
 **name** | **str**| Identity key of the Subnet | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**Subnet**](Subnet.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

