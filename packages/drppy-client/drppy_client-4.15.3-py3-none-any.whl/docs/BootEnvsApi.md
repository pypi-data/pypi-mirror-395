# drppy_client.BootEnvsApi

All URIs are relative to *https://localhost/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_boot_env**](BootEnvsApi.md#create_boot_env) | **POST** /bootenvs | Create a BootEnv
[**delete_boot_env**](BootEnvsApi.md#delete_boot_env) | **DELETE** /bootenvs/{name} | Delete a BootEnv
[**get_boot_env**](BootEnvsApi.md#get_boot_env) | **GET** /bootenvs/{name} | Get a BootEnv
[**get_boot_env_action**](BootEnvsApi.md#get_boot_env_action) | **GET** /bootenvs/{name}/actions/{cmd} | List specific action for a bootenvs BootEnv
[**get_boot_env_actions**](BootEnvsApi.md#get_boot_env_actions) | **GET** /bootenvs/{name}/actions | List bootenvs actions BootEnv
[**head_boot_env**](BootEnvsApi.md#head_boot_env) | **HEAD** /bootenvs/{name} | See if a BootEnv exists
[**list_boot_envs**](BootEnvsApi.md#list_boot_envs) | **GET** /bootenvs | Lists BootEnvs filtered by some parameters.
[**list_stats_boot_envs**](BootEnvsApi.md#list_stats_boot_envs) | **HEAD** /bootenvs | Stats of the List BootEnvs filtered by some parameters.
[**patch_boot_env**](BootEnvsApi.md#patch_boot_env) | **PATCH** /bootenvs/{name} | Patch a BootEnv
[**post_boot_env_action**](BootEnvsApi.md#post_boot_env_action) | **POST** /bootenvs/{name}/actions/{cmd} | Call an action on the node.
[**purge_local_boot_env**](BootEnvsApi.md#purge_local_boot_env) | **DELETE** /bootenvs/{name}/purgeLocal | Purge local install files (ISOS and install trees) for a bootenv
[**put_boot_env**](BootEnvsApi.md#put_boot_env) | **PUT** /bootenvs/{name} | Put a BootEnv


# **create_boot_env**
> BootEnv create_boot_env(body)

Create a BootEnv

Create a BootEnv from the provided object

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
body = drppy_client.BootEnv() # BootEnv | 

try:
    # Create a BootEnv
    api_response = api_instance.create_boot_env(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->create_boot_env: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BootEnv**](BootEnv.md)|  | 

### Return type

[**BootEnv**](BootEnv.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_boot_env**
> BootEnv delete_boot_env(name, force=force, commented=commented, reduced=reduced)

Delete a BootEnv

Delete a BootEnv specified by {name}

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the BootEnv
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Delete a BootEnv
    api_response = api_instance.delete_boot_env(name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->delete_boot_env: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the BootEnv | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**BootEnv**](BootEnv.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_boot_env**
> BootEnv get_boot_env(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

Get a BootEnv

Get the BootEnv specified by {name}  or return NotFound.

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the BootEnv
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Get a BootEnv
    api_response = api_instance.get_boot_env(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->get_boot_env: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the BootEnv | 
 **aggregate** | **bool**| Should the objects have aggregated parameters used in return and evaluation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **decode** | **bool**| Should Secure Params be decrypted in the result | [optional] 
 **expand** | **bool**| Should the objects have expanded parameters used in return and evaluation | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**BootEnv**](BootEnv.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_boot_env_action**
> AvailableAction get_boot_env_action(name, cmd, plugin=plugin)

List specific action for a bootenvs BootEnv

List specific {cmd} action for a BootEnv specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the BootEnv
cmd = 'cmd_example' # str | The action to run on the plugin
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List specific action for a bootenvs BootEnv
    api_response = api_instance.get_boot_env_action(name, cmd, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->get_boot_env_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the BootEnv | 
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

# **get_boot_env_actions**
> list[AvailableAction] get_boot_env_actions(name, plugin=plugin)

List bootenvs actions BootEnv

List BootEnv actions for a BootEnv specified by {name}  Optionally, a query parameter can be used to limit the scope to a specific plugin. e.g. ?plugin=fred

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the BootEnv
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # List bootenvs actions BootEnv
    api_response = api_instance.get_boot_env_actions(name, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->get_boot_env_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the BootEnv | 
 **plugin** | **str**| Plugin that should be used for this action | [optional] 

### Return type

[**list[AvailableAction]**](AvailableAction.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **head_boot_env**
> head_boot_env(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)

See if a BootEnv exists

Return 200 if the BootEnv specifiec by {name} exists, or return NotFound.

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the BootEnv
aggregate = true # bool | Should the objects have aggregated parameters used in return and evaluation (optional)
commented = true # bool | Should the returned object have comments added (optional)
decode = true # bool | Should Secure Params be decrypted in the result (optional)
expand = true # bool | Should the objects have expanded parameters used in return and evaluation (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # See if a BootEnv exists
    api_instance.head_boot_env(name, aggregate=aggregate, commented=commented, decode=decode, expand=expand, reduced=reduced)
except ApiException as e:
    print("Exception when calling BootEnvsApi->head_boot_env: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the BootEnv | 
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

# **list_boot_envs**
> list[BootEnv] list_boot_envs(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, boot_params=boot_params, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, end_delimiter=end_delimiter, endpoint=endpoint, errors=errors, initrds=initrds, kernel=kernel, last_modified_at=last_modified_at, last_modified_by=last_modified_by, loaders=loaders, meta=meta, name=name, os=os, only_unknown=only_unknown, optional_params=optional_params, read_only=read_only, required_params=required_params, start_delimiter=start_delimiter, templates=templates, validated=validated)

Lists BootEnvs filtered by some parameters.

This will show all BootEnvs by default.  You may specify to control the search:  aggregate = boolean to indicate if the parameters should be aggregated for search and return<br/> expand = boolean to indicate if the parameters should be expanded for search and return<br/> filter = a string that defines a Named filter<br/> raw = a string that is template expanded and then parsed for filter functions<br/>  You may specify to control the output:  decode = boolean to indicate that the returned object have the secure parameters decoded.<br/> group-by = can be specified multiple times. An array of objects (nested) grouped by the value is returned.<br/> limit = integer, number of items to return<br/> offset = integer, 0-based inclusive starting point in filter data.<br/> params = a comma separated list of parameters, or list functions to allow for inclusion in the returned object (if appropriate)<br/> range-only = returns only counts of the objects in the groups.<br/> reverse = boolean to indicate to reverse the returned list<br/> slim = A comma separated list of fields to exclude (meta, params, or other field names)<br/> sort = A list of strings defining the fields or parameters to sort by<br/> reduced = boolean to indicate that the objects should not have read-only fields<br/> commented = boolean to indicate that field comments should be included in object<br/>  Functions:  Eq(value) = Return items that are equal to value<br/> Lt(value) = Return items that are less than value<br/> Lte(value) = Return items that less than or equal to value<br/> Gt(value) = Return items that are greater than value<br/> Gte(value) = Return items that greater than or equal to value<br/> Between(lower,upper) = Return items that are inclusively between lower and upper<br/> Except(lower,upper) = Return items that are not inclusively between lower and upper<br/>  Functions can be applied against fields of the object.  Example:  Name=fred - returns items named fred<br/> Name=Lt(fred) - returns items that alphabetically less than fred.<br/> Name=Lt(fred)&Available=true - returns items with Name less than fred and Available is true<br/>

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
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
boot_params = 'boot_params_example' # str | A template that will be expanded to create the full list of boot parameters for the environment.  This list will generally be passed as command line arguments to the Kernel as it boots up. (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
end_delimiter = 'end_delimiter_example' # str | EndDelimiter is an optional end delimiter. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
initrds = 'initrds_example' # str | Partial paths to the initrds that should be loaded for the boot environment. These should be paths that the initrds are located at in the OS ISO or install archive. (optional)
kernel = 'kernel_example' # str | The partial path to the kernel for the boot environment.  This should be path that the kernel is located at in the OS ISO or install archive.  Kernel must be non-empty for a BootEnv to be considered net bootable. (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
loaders = 'loaders_example' # str | Loaders contains the boot loaders that should be used for various different network boot scenarios.  It consists of a map of machine type -> partial paths to the bootloaders. Valid machine types are:  386-pcbios for x86 devices using the legacy bios.  amd64-uefi for x86 devices operating in UEFI mode  arm64-uefi for arm64 devices operating in UEFI mode  Other machine types will be added as dr-provision gains support for them.  If this map does not contain an entry for the machine type, the DHCP server will fall back to the following entries in this order:  The Loader specified in the ArchInfo struct from this BootEnv, if it exists.  The value specified in the bootloaders param for the machine type specified on the machine, if it exists.  The value specified in the bootloaders param in the global profile, if it exists.  The value specified in the default value for the bootloaders param.  One of the following vaiues:  lpxelinux.0 for 386-pcbios  ipxe.efi for amd64-uefi  ipxe-arm64.efi for arm64-uefi (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | Name is the name of the boot environment.  Boot environments that install an operating system must end in '-install'.  All boot environment names must be unique. (optional)
os = 'os_example' # str | OS is the operating system specific information for the boot environment. (optional)
only_unknown = 'only_unknown_example' # str | OnlyUnknown indicates whether this bootenv can be used without a machine.  Only bootenvs with this flag set to `true` be used for the unknownBootEnv preference.  If this flag is set to True, then the Templates provided byt this boot environment must take care to be able to chainload into the appropriate boot environments for other machines if the bootloader that machine is using does not support it natively. The built-in ignore boot environment and the discovery boot environment provided by the community content bundle should be used as references for satisfying that requirement. (optional)
optional_params = 'optional_params_example' # str | The list of extra optional parameters for this boot environment. They can be present as Machine.Params when the bootenv is applied to the machine.  These are more other consumers of the bootenv to know what parameters could additionally be applied to the bootenv by the renderer based upon the Machine.Params (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
required_params = 'required_params_example' # str | The list of extra required parameters for this boot environment. They should be present as Machine.Params when the bootenv is applied to the machine. (optional)
start_delimiter = 'start_delimiter_example' # str | StartDelimiter is an optional start delimiter. (optional)
templates = 'templates_example' # str | Templates contains a list of templates that should be expanded into files for the boot environment.  These expanded templates will be available via TFTP and static HTTP from dr-provision.  You should take care that the final paths for the temmplates do not overlap with ones provided by other boot environments. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Lists BootEnvs filtered by some parameters.
    api_response = api_instance.list_boot_envs(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, boot_params=boot_params, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, end_delimiter=end_delimiter, endpoint=endpoint, errors=errors, initrds=initrds, kernel=kernel, last_modified_at=last_modified_at, last_modified_by=last_modified_by, loaders=loaders, meta=meta, name=name, os=os, only_unknown=only_unknown, optional_params=optional_params, read_only=read_only, required_params=required_params, start_delimiter=start_delimiter, templates=templates, validated=validated)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->list_boot_envs: %s\n" % e)
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
 **boot_params** | **str**| A template that will be expanded to create the full list of boot parameters for the environment.  This list will generally be passed as command line arguments to the Kernel as it boots up. | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **end_delimiter** | **str**| EndDelimiter is an optional end delimiter. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **initrds** | **str**| Partial paths to the initrds that should be loaded for the boot environment. These should be paths that the initrds are located at in the OS ISO or install archive. | [optional] 
 **kernel** | **str**| The partial path to the kernel for the boot environment.  This should be path that the kernel is located at in the OS ISO or install archive.  Kernel must be non-empty for a BootEnv to be considered net bootable. | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **loaders** | **str**| Loaders contains the boot loaders that should be used for various different network boot scenarios.  It consists of a map of machine type -&gt; partial paths to the bootloaders. Valid machine types are:  386-pcbios for x86 devices using the legacy bios.  amd64-uefi for x86 devices operating in UEFI mode  arm64-uefi for arm64 devices operating in UEFI mode  Other machine types will be added as dr-provision gains support for them.  If this map does not contain an entry for the machine type, the DHCP server will fall back to the following entries in this order:  The Loader specified in the ArchInfo struct from this BootEnv, if it exists.  The value specified in the bootloaders param for the machine type specified on the machine, if it exists.  The value specified in the bootloaders param in the global profile, if it exists.  The value specified in the default value for the bootloaders param.  One of the following vaiues:  lpxelinux.0 for 386-pcbios  ipxe.efi for amd64-uefi  ipxe-arm64.efi for arm64-uefi | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| Name is the name of the boot environment.  Boot environments that install an operating system must end in &#39;-install&#39;.  All boot environment names must be unique. | [optional] 
 **os** | **str**| OS is the operating system specific information for the boot environment. | [optional] 
 **only_unknown** | **str**| OnlyUnknown indicates whether this bootenv can be used without a machine.  Only bootenvs with this flag set to &#x60;true&#x60; be used for the unknownBootEnv preference.  If this flag is set to True, then the Templates provided byt this boot environment must take care to be able to chainload into the appropriate boot environments for other machines if the bootloader that machine is using does not support it natively. The built-in ignore boot environment and the discovery boot environment provided by the community content bundle should be used as references for satisfying that requirement. | [optional] 
 **optional_params** | **str**| The list of extra optional parameters for this boot environment. They can be present as Machine.Params when the bootenv is applied to the machine.  These are more other consumers of the bootenv to know what parameters could additionally be applied to the bootenv by the renderer based upon the Machine.Params | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **required_params** | **str**| The list of extra required parameters for this boot environment. They should be present as Machine.Params when the bootenv is applied to the machine. | [optional] 
 **start_delimiter** | **str**| StartDelimiter is an optional start delimiter. | [optional] 
 **templates** | **str**| Templates contains a list of templates that should be expanded into files for the boot environment.  These expanded templates will be available via TFTP and static HTTP from dr-provision.  You should take care that the final paths for the temmplates do not overlap with ones provided by other boot environments. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

[**list[BootEnv]**](BootEnv.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_stats_boot_envs**
> list_stats_boot_envs(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, boot_params=boot_params, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, end_delimiter=end_delimiter, endpoint=endpoint, errors=errors, initrds=initrds, kernel=kernel, last_modified_at=last_modified_at, last_modified_by=last_modified_by, loaders=loaders, meta=meta, name=name, os=os, only_unknown=only_unknown, optional_params=optional_params, read_only=read_only, required_params=required_params, start_delimiter=start_delimiter, templates=templates, validated=validated)

Stats of the List BootEnvs filtered by some parameters.

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
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
boot_params = 'boot_params_example' # str | A template that will be expanded to create the full list of boot parameters for the environment.  This list will generally be passed as command line arguments to the Kernel as it boots up. (optional)
bundle = 'bundle_example' # str | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true (optional)
created_at = 'created_at_example' # str | CreatedAt is the time that this object was created. (optional)
created_by = 'created_by_example' # str | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that `currentUserName` needs to be populated in the authBlob (optional)
description = 'description_example' # str | Description is a string for providing a simple description (optional)
documentation = 'documentation_example' # str | Documentation is a string for providing additional in depth information. (optional)
end_delimiter = 'end_delimiter_example' # str | EndDelimiter is an optional end delimiter. (optional)
endpoint = 'endpoint_example' # str | Endpoint tracks the owner of the object among DRP endpoints read only: true (optional)
errors = 'errors_example' # str | If there are any errors in the validation process, they will be available here. read only: true (optional)
initrds = 'initrds_example' # str | Partial paths to the initrds that should be loaded for the boot environment. These should be paths that the initrds are located at in the OS ISO or install archive. (optional)
kernel = 'kernel_example' # str | The partial path to the kernel for the boot environment.  This should be path that the kernel is located at in the OS ISO or install archive.  Kernel must be non-empty for a BootEnv to be considered net bootable. (optional)
last_modified_at = 'last_modified_at_example' # str | LastModifiedAt is the time that this object was last modified. (optional)
last_modified_by = 'last_modified_by_example' # str | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked (optional)
loaders = 'loaders_example' # str | Loaders contains the boot loaders that should be used for various different network boot scenarios.  It consists of a map of machine type -> partial paths to the bootloaders. Valid machine types are:  386-pcbios for x86 devices using the legacy bios.  amd64-uefi for x86 devices operating in UEFI mode  arm64-uefi for arm64 devices operating in UEFI mode  Other machine types will be added as dr-provision gains support for them.  If this map does not contain an entry for the machine type, the DHCP server will fall back to the following entries in this order:  The Loader specified in the ArchInfo struct from this BootEnv, if it exists.  The value specified in the bootloaders param for the machine type specified on the machine, if it exists.  The value specified in the bootloaders param in the global profile, if it exists.  The value specified in the default value for the bootloaders param.  One of the following vaiues:  lpxelinux.0 for 386-pcbios  ipxe.efi for amd64-uefi  ipxe-arm64.efi for arm64-uefi (optional)
meta = 'meta_example' # str | Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref=rs_object_metadata (optional)
name = 'name_example' # str | Name is the name of the boot environment.  Boot environments that install an operating system must end in '-install'.  All boot environment names must be unique. (optional)
os = 'os_example' # str | OS is the operating system specific information for the boot environment. (optional)
only_unknown = 'only_unknown_example' # str | OnlyUnknown indicates whether this bootenv can be used without a machine.  Only bootenvs with this flag set to `true` be used for the unknownBootEnv preference.  If this flag is set to True, then the Templates provided byt this boot environment must take care to be able to chainload into the appropriate boot environments for other machines if the bootloader that machine is using does not support it natively. The built-in ignore boot environment and the discovery boot environment provided by the community content bundle should be used as references for satisfying that requirement. (optional)
optional_params = 'optional_params_example' # str | The list of extra optional parameters for this boot environment. They can be present as Machine.Params when the bootenv is applied to the machine.  These are more other consumers of the bootenv to know what parameters could additionally be applied to the bootenv by the renderer based upon the Machine.Params (optional)
read_only = 'read_only_example' # str | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true (optional)
required_params = 'required_params_example' # str | The list of extra required parameters for this boot environment. They should be present as Machine.Params when the bootenv is applied to the machine. (optional)
start_delimiter = 'start_delimiter_example' # str | StartDelimiter is an optional start delimiter. (optional)
templates = 'templates_example' # str | Templates contains a list of templates that should be expanded into files for the boot environment.  These expanded templates will be available via TFTP and static HTTP from dr-provision.  You should take care that the final paths for the temmplates do not overlap with ones provided by other boot environments. (optional)
validated = 'validated_example' # str | Validated tracks whether or not the model has been validated. read only: true (optional)

try:
    # Stats of the List BootEnvs filtered by some parameters.
    api_instance.list_stats_boot_envs(offset=offset, limit=limit, filter=filter, raw=raw, decode=decode, group_by=group_by, params=params, range_only=range_only, reverse=reverse, slim=slim, sort=sort, aggregate=aggregate, expand=expand, commented=commented, reduced=reduced, available=available, boot_params=boot_params, bundle=bundle, created_at=created_at, created_by=created_by, description=description, documentation=documentation, end_delimiter=end_delimiter, endpoint=endpoint, errors=errors, initrds=initrds, kernel=kernel, last_modified_at=last_modified_at, last_modified_by=last_modified_by, loaders=loaders, meta=meta, name=name, os=os, only_unknown=only_unknown, optional_params=optional_params, read_only=read_only, required_params=required_params, start_delimiter=start_delimiter, templates=templates, validated=validated)
except ApiException as e:
    print("Exception when calling BootEnvsApi->list_stats_boot_envs: %s\n" % e)
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
 **boot_params** | **str**| A template that will be expanded to create the full list of boot parameters for the environment.  This list will generally be passed as command line arguments to the Kernel as it boots up. | [optional] 
 **bundle** | **str**| Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API.  read only: true | [optional] 
 **created_at** | **str**| CreatedAt is the time that this object was created. | [optional] 
 **created_by** | **str**| CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
 **description** | **str**| Description is a string for providing a simple description | [optional] 
 **documentation** | **str**| Documentation is a string for providing additional in depth information. | [optional] 
 **end_delimiter** | **str**| EndDelimiter is an optional end delimiter. | [optional] 
 **endpoint** | **str**| Endpoint tracks the owner of the object among DRP endpoints read only: true | [optional] 
 **errors** | **str**| If there are any errors in the validation process, they will be available here. read only: true | [optional] 
 **initrds** | **str**| Partial paths to the initrds that should be loaded for the boot environment. These should be paths that the initrds are located at in the OS ISO or install archive. | [optional] 
 **kernel** | **str**| The partial path to the kernel for the boot environment.  This should be path that the kernel is located at in the OS ISO or install archive.  Kernel must be non-empty for a BootEnv to be considered net bootable. | [optional] 
 **last_modified_at** | **str**| LastModifiedAt is the time that this object was last modified. | [optional] 
 **last_modified_by** | **str**| LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
 **loaders** | **str**| Loaders contains the boot loaders that should be used for various different network boot scenarios.  It consists of a map of machine type -&gt; partial paths to the bootloaders. Valid machine types are:  386-pcbios for x86 devices using the legacy bios.  amd64-uefi for x86 devices operating in UEFI mode  arm64-uefi for arm64 devices operating in UEFI mode  Other machine types will be added as dr-provision gains support for them.  If this map does not contain an entry for the machine type, the DHCP server will fall back to the following entries in this order:  The Loader specified in the ArchInfo struct from this BootEnv, if it exists.  The value specified in the bootloaders param for the machine type specified on the machine, if it exists.  The value specified in the bootloaders param in the global profile, if it exists.  The value specified in the default value for the bootloaders param.  One of the following vaiues:  lpxelinux.0 for 386-pcbios  ipxe.efi for amd64-uefi  ipxe-arm64.efi for arm64-uefi | [optional] 
 **meta** | **str**| Meta contains the meta data of the object.  The type of this field is a key / value map/dictionary. The key type is string. The value type is also string.  The general content of the field is undefined and can be an arbritary store. There are some common known keys:  color - The color the UX uses when displaying icon - The icon the UX uses when displaying title - The UX uses this for additional display information.  Often the source of the object.  Specific Object types use additional meta data fields.  These are described at: https://docs.rackn.io/stable/redirect/?ref&#x3D;rs_object_metadata | [optional] 
 **name** | **str**| Name is the name of the boot environment.  Boot environments that install an operating system must end in &#39;-install&#39;.  All boot environment names must be unique. | [optional] 
 **os** | **str**| OS is the operating system specific information for the boot environment. | [optional] 
 **only_unknown** | **str**| OnlyUnknown indicates whether this bootenv can be used without a machine.  Only bootenvs with this flag set to &#x60;true&#x60; be used for the unknownBootEnv preference.  If this flag is set to True, then the Templates provided byt this boot environment must take care to be able to chainload into the appropriate boot environments for other machines if the bootloader that machine is using does not support it natively. The built-in ignore boot environment and the discovery boot environment provided by the community content bundle should be used as references for satisfying that requirement. | [optional] 
 **optional_params** | **str**| The list of extra optional parameters for this boot environment. They can be present as Machine.Params when the bootenv is applied to the machine.  These are more other consumers of the bootenv to know what parameters could additionally be applied to the bootenv by the renderer based upon the Machine.Params | [optional] 
 **read_only** | **str**| ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API.  read only: true | [optional] 
 **required_params** | **str**| The list of extra required parameters for this boot environment. They should be present as Machine.Params when the bootenv is applied to the machine. | [optional] 
 **start_delimiter** | **str**| StartDelimiter is an optional start delimiter. | [optional] 
 **templates** | **str**| Templates contains a list of templates that should be expanded into files for the boot environment.  These expanded templates will be available via TFTP and static HTTP from dr-provision.  You should take care that the final paths for the temmplates do not overlap with ones provided by other boot environments. | [optional] 
 **validated** | **str**| Validated tracks whether or not the model has been validated. read only: true | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_boot_env**
> BootEnv patch_boot_env(body, name, force=force, commented=commented, reduced=reduced)

Patch a BootEnv

Update a BootEnv specified by {name} using a RFC6902 Patch structure

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
body = drppy_client.Patch() # Patch | 
name = 'name_example' # str | Identity key of the BootEnv
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Patch a BootEnv
    api_response = api_instance.patch_boot_env(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->patch_boot_env: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Patch**](Patch.md)|  | 
 **name** | **str**| Identity key of the BootEnv | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**BootEnv**](BootEnv.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_boot_env_action**
> object post_boot_env_action(name, cmd, body, plugin=plugin)

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
name = 'name_example' # str | Identity key of the BootEnv
cmd = 'cmd_example' # str | The action to run on the plugin
body = NULL # object | Additional parameter data for the action.  At a minimum, an empty object must be provided e.g. {}
plugin = 'plugin_example' # str | Plugin that should be used for this action (optional)

try:
    # Call an action on the node.
    api_response = api_instance.post_boot_env_action(name, cmd, body, plugin=plugin)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->post_boot_env_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Identity key of the BootEnv | 
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

# **purge_local_boot_env**
> purge_local_boot_env(body, reexplode_isos=reexplode_isos)

Purge local install files (ISOS and install trees) for a bootenv

Purges ISO files and local install files for a bootenv on an arch by arch basis.

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
body = [drppy_client.list[str]()] # list[str] | 
reexplode_isos = true # bool |  (optional)

try:
    # Purge local install files (ISOS and install trees) for a bootenv
    api_instance.purge_local_boot_env(body, reexplode_isos=reexplode_isos)
except ApiException as e:
    print("Exception when calling BootEnvsApi->purge_local_boot_env: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **list[str]**|  | 
 **reexplode_isos** | **bool**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_boot_env**
> BootEnv put_boot_env(body, name, force=force, commented=commented, reduced=reduced)

Put a BootEnv

Update a BootEnv specified by {name} using a JSON BootEnv

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
api_instance = drppy_client.BootEnvsApi(drppy_client.ApiClient(configuration))
body = drppy_client.BootEnv() # BootEnv | 
name = 'name_example' # str | Identity key of the BootEnv
force = true # bool | Attempt force the action with less validation (optional)
commented = true # bool | Should the returned object have comments added (optional)
reduced = true # bool | Should the returned object have only read/write fields (optional)

try:
    # Put a BootEnv
    api_response = api_instance.put_boot_env(body, name, force=force, commented=commented, reduced=reduced)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BootEnvsApi->put_boot_env: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BootEnv**](BootEnv.md)|  | 
 **name** | **str**| Identity key of the BootEnv | 
 **force** | **bool**| Attempt force the action with less validation | [optional] 
 **commented** | **bool**| Should the returned object have comments added | [optional] 
 **reduced** | **bool**| Should the returned object have only read/write fields | [optional] 

### Return type

[**BootEnv**](BootEnv.md)

### Authorization

[Bearer](../README.md#Bearer), [basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

