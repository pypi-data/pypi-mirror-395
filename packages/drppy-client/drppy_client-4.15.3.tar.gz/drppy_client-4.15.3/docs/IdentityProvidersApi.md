# drppy_client.IdentityProvidersApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_identity_provider**](IdentityProvidersApi.md#create_identity_provider) | **POST** /identity_providers | Create a IdentityProvider
[**delete_identity_provider**](IdentityProvidersApi.md#delete_identity_provider) | **DELETE** /identity_providers/{name} | Delete a IdentityProvider
[**get_identity_provider**](IdentityProvidersApi.md#get_identity_provider) | **GET** /identity_providers/{name} | Get a IdentityProvider
[**get_identity_provider_action**](IdentityProvidersApi.md#get_identity_provider_action) | **GET** /identity_providers/{name}/actions/{cmd} | List specific action for a identity_providers IdentityProvider
[**get_identity_provider_actions**](IdentityProvidersApi.md#get_identity_provider_actions) | **GET** /identity_providers/{name}/actions | List identity_providers actions IdentityProvider
[**head_identity_provider**](IdentityProvidersApi.md#head_identity_provider) | **HEAD** /identity_providers/{name} | See if a IdentityProvider exists
[**list_identity_providers**](IdentityProvidersApi.md#list_identity_providers) | **GET** /identity_providers | Lists IdentityProviders filtered by some parameters.
[**list_stats_identity_providers**](IdentityProvidersApi.md#list_stats_identity_providers) | **HEAD** /identity_providers | Stats of the List IdentityProviders filtered by some parameters.
[**patch_identity_provider**](IdentityProvidersApi.md#patch_identity_provider) | **PATCH** /identity_providers/{name} | Patch a IdentityProvider
[**post_identity_provider_action**](IdentityProvidersApi.md#post_identity_provider_action) | **POST** /identity_providers/{name}/actions/{cmd} | Call an action on the node.
[**put_identity_provider**](IdentityProvidersApi.md#put_identity_provider) | **PUT** /identity_providers/{name} | Put a IdentityProvider


# **create_identity_provider**
> IdentityProvider create_identity_provider(body)

Create a IdentityProvider

Create a IdentityProvider from the provided object

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
body = drppy_client.IdentityProvider() # IdentityProvider | 

try:
    # Create a IdentityProvider
    api_response = api_instance.create_identity_provider(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->create_identity_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**IdentityProvider**](IdentityProvider.md)|  | 

### Return type

[**IdentityProvider**](IdentityProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_identity_provider**
> IdentityProvider delete_identity_provider(name, force=force, commented=commented, reduced=reduced)

Delete a IdentityProvider

Delete a IdentityProvider specified by {name}

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the IdentityProvider
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a IdentityProvider
    api_response = api_instance.delete_identity_provider(name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->delete_identity_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the IdentityProvider | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**IdentityProvider**](IdentityProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_identity_provider**
> IdentityProvider get_identity_provider(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a IdentityProvider

Get the IdentityProvider specified by {name}  or return NotFound.

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the IdentityProvider
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a IdentityProvider
    api_response = api_instance.get_identity_provider(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->get_identity_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the IdentityProvider | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**IdentityProvider**](IdentityProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_identity_provider_action**
> AvailableAction get_identity_provider_action(name, cmd, plugin=plugin)

List specific action for a identity_providers IdentityProvider

List specific {cmd} action for a IdentityProvider specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the IdentityProvider
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a identity_providers IdentityProvider
    api_response = api_instance.get_identity_provider_action(name, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->get_identity_provider_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the IdentityProvider | 
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

# **get_identity_provider_actions**
> list[AvailableAction] get_identity_provider_actions(name, plugin=plugin)

List identity_providers actions IdentityProvider

List IdentityProvider actions for a IdentityProvider specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the IdentityProvider
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List identity_providers actions IdentityProvider
    api_response = api_instance.get_identity_provider_actions(name, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->get_identity_provider_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the IdentityProvider | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_identity_provider**
> head_identity_provider(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a IdentityProvider exists

Return 200 if the IdentityProvider specifiec by {name} exists, or return NotFound.

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the IdentityProvider
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a IdentityProvider exists
    api_instance.head_identity_provider(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->head_identity_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the IdentityProvider | 
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

# **list_identity_providers**
> list[IdentityProvider] list_identity_providers(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, bundle=bundle, created_at=created_at, created_by=created_by, default_role=default_role, deny_if_no_groups=deny_if_no_groups, description=description, display_name=display_name, documentation=documentation, endpoint=endpoint, errors=errors, group_attribute=group_attribute, group_to_roles=group_to_roles, last_modified_at=last_modified_at, last_modified_by=last_modified_by, logo_path=logo_path, meta=meta, meta_data_blob=meta_data_blob, meta_data_url=meta_data_url, name=name, read_only=read_only, user_attribute=user_attribute, validated=validated)

Lists IdentityProviders filtered by some parameters.

This will show all IdentityProviders by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
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
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
default_role = 'default_role_example' # str | DefaultRole - defines the default role to give these users (optional)
deny_if_no_groups = 'deny_if_no_groups_example' # str | DenyIfNoGroups - defines if the auth should fail if no groups are found in the GroupAttribute (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
display_name = 'display_name_example' # str | DisplayName - The name to display to user (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
group_attribute = 'group_attribute_example' # str | GroupAttribute - specifies the attribute in the Assertions to use as group memberships (optional)
group_to_roles = 'group_to_roles_example' # str | GroupToRoles - defines the group names that map to DRP Roles (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
logo_path = 'logo_path_example' # str | LogoPath - The path on DRP or the URL to the logo icon (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
meta_data_blob = 'meta_data_blob_example' # str | MetaDataBlob - String form of the metadata - instead of MetaDataUrl (optional)
meta_data_url = 'meta_data_url_example' # str | MetaDataUrl - URL to get the metadata for this IdP - instead of MetaDataBlob (optional)
name = 'name_example' # str | Name is the name of this identity provider (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
user_attribute = 'user_attribute_example' # str | UserAttribute - specifies the attribute in the Assertions to use as username (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Lists IdentityProviders filtered by some parameters.
    api_response = api_instance.list_identity_providers(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, bundle=bundle, created_at=created_at, created_by=created_by, default_role=default_role, deny_if_no_groups=deny_if_no_groups, description=description, display_name=display_name, documentation=documentation, endpoint=endpoint, errors=errors, group_attribute=group_attribute, group_to_roles=group_to_roles, last_modified_at=last_modified_at, last_modified_by=last_modified_by, logo_path=logo_path, meta=meta, meta_data_blob=meta_data_blob, meta_data_url=meta_data_url, name=name, read_only=read_only, user_attribute=user_attribute, validated=validated)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->list_identity_providers: %s\n" % e)
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
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **default_role** | **str**| DefaultRole - defines the default role to give these users | [optional] 
 **deny_if_no_groups** | **str**| DenyIfNoGroups - defines if the auth should fail if no groups are found in the GroupAttribute | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **display_name** | **str**| DisplayName - The name to display to user | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **group_attribute** | **str**| GroupAttribute - specifies the attribute in the Assertions to use as group memberships | [optional] 
 **group_to_roles** | **str**| GroupToRoles - defines the group names that map to DRP Roles | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **logo_path** | **str**| LogoPath - The path on DRP or the URL to the logo icon | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **meta_data_blob** | **str**| MetaDataBlob - String form of the metadata - instead of MetaDataUrl | [optional] 
 **meta_data_url** | **str**| MetaDataUrl - URL to get the metadata for this IdP - instead of MetaDataBlob | [optional] 
 **name** | **str**| Name is the name of this identity provider | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **user_attribute** | **str**| UserAttribute - specifies the attribute in the Assertions to use as username | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

[**list[IdentityProvider]**](IdentityProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_stats_identity_providers**
> list_stats_identity_providers(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, bundle=bundle, created_at=created_at, created_by=created_by, default_role=default_role, deny_if_no_groups=deny_if_no_groups, description=description, display_name=display_name, documentation=documentation, endpoint=endpoint, errors=errors, group_attribute=group_attribute, group_to_roles=group_to_roles, last_modified_at=last_modified_at, last_modified_by=last_modified_by, logo_path=logo_path, meta=meta, meta_data_blob=meta_data_blob, meta_data_url=meta_data_url, name=name, read_only=read_only, user_attribute=user_attribute, validated=validated)

Stats of the List IdentityProviders filtered by some parameters.

This will return headers with the stats of the list.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> range-only = returns only counts of the objects in the groups.<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
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
available = 'available_example' # str | Available tracks whether or not the model passed validation. read only: true (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
default_role = 'default_role_example' # str | DefaultRole - defines the default role to give these users (optional)
deny_if_no_groups = 'deny_if_no_groups_example' # str | DenyIfNoGroups - defines if the auth should fail if no groups are found in the GroupAttribute (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
display_name = 'display_name_example' # str | DisplayName - The name to display to user (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
group_attribute = 'group_attribute_example' # str | GroupAttribute - specifies the attribute in the Assertions to use as group memberships (optional)
group_to_roles = 'group_to_roles_example' # str | GroupToRoles - defines the group names that map to DRP Roles (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
logo_path = 'logo_path_example' # str | LogoPath - The path on DRP or the URL to the logo icon (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
meta_data_blob = 'meta_data_blob_example' # str | MetaDataBlob - String form of the metadata - instead of MetaDataUrl (optional)
meta_data_url = 'meta_data_url_example' # str | MetaDataUrl - URL to get the metadata for this IdP - instead of MetaDataBlob (optional)
name = 'name_example' # str | Name is the name of this identity provider (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
user_attribute = 'user_attribute_example' # str | UserAttribute - specifies the attribute in the Assertions to use as username (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Stats of the List IdentityProviders filtered by some parameters.
    api_instance.list_stats_identity_providers(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, bundle=bundle, created_at=created_at, created_by=created_by, default_role=default_role, deny_if_no_groups=deny_if_no_groups, description=description, display_name=display_name, documentation=documentation, endpoint=endpoint, errors=errors, group_attribute=group_attribute, group_to_roles=group_to_roles, last_modified_at=last_modified_at, last_modified_by=last_modified_by, logo_path=logo_path, meta=meta, meta_data_blob=meta_data_blob, meta_data_url=meta_data_url, name=name, read_only=read_only, user_attribute=user_attribute, validated=validated)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->list_stats_identity_providers: %s\n" % e)
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
 **available** | **str**| Available tracks whether or not the model passed validation. read only: true | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **default_role** | **str**| DefaultRole - defines the default role to give these users | [optional] 
 **deny_if_no_groups** | **str**| DenyIfNoGroups - defines if the auth should fail if no groups are found in the GroupAttribute | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **display_name** | **str**| DisplayName - The name to display to user | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **group_attribute** | **str**| GroupAttribute - specifies the attribute in the Assertions to use as group memberships | [optional] 
 **group_to_roles** | **str**| GroupToRoles - defines the group names that map to DRP Roles | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **logo_path** | **str**| LogoPath - The path on DRP or the URL to the logo icon | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **meta_data_blob** | **str**| MetaDataBlob - String form of the metadata - instead of MetaDataUrl | [optional] 
 **meta_data_url** | **str**| MetaDataUrl - URL to get the metadata for this IdP - instead of MetaDataBlob | [optional] 
 **name** | **str**| Name is the name of this identity provider | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **user_attribute** | **str**| UserAttribute - specifies the attribute in the Assertions to use as username | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_identity_provider**
> IdentityProvider patch_identity_provider(body, name, force=force, commented=commented, reduced=reduced)

Patch a IdentityProvider

Update a IdentityProvider specified by {name} using a RFC6902 Patch structure

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
name = 'name_example' # str | Identity key of the IdentityProvider
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a IdentityProvider
    api_response = api_instance.patch_identity_provider(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->patch_identity_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **name** | **str**| Identity key of the IdentityProvider | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**IdentityProvider**](IdentityProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_identity_provider_action**
> object post_identity_provider_action(name, cmd, body, plugin=plugin)

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the IdentityProvider
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_identity_provider_action(name, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->post_identity_provider_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the IdentityProvider | 
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

# **put_identity_provider**
> IdentityProvider put_identity_provider(body, name, force=force, commented=commented, reduced=reduced)

Put a IdentityProvider

Update a IdentityProvider specified by {name} using a JSON IdentityProvider

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
api_instance = drppy_client.IdentityProvidersApi(drppy_client.ApiClient(configuration))
body = drppy_client.IdentityProvider() # IdentityProvider | 
name = 'name_example' # str | Identity key of the IdentityProvider
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a IdentityProvider
    api_response = api_instance.put_identity_provider(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling IdentityProvidersApi->put_identity_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**IdentityProvider**](IdentityProvider.md)|  | 
 **name** | **str**| Identity key of the IdentityProvider | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**IdentityProvider**](IdentityProvider.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

