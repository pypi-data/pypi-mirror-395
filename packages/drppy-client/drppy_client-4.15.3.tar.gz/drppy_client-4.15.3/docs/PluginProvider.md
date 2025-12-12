# PluginProvider

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auto_start** | **bool** | If AutoStart is true, a Plugin will be created for this Provider at provider definition time, if one is not already present. | [optional] 
**available_actions** | [**list[AvailableAction]**](AvailableAction.md) | AvailableActions lists the actions that this PluginProvider can take. | [optional] 
**content** | **str** | Content Bundle Yaml string - can be optional or empty | [optional] 
**documentation** | **str** | Documentation of this plugin provider.  This should tell what the plugin provider is for, any special considerations that should be taken into account when using it, etc. in rich structured text (rst). | [optional] 
**has_publish** | **bool** | HasPlugin is deprecated, plugin provider binaries should use a websocket event stream instead. | [optional] 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**name** | **str** | Name is the unique name of the PluginProvider. Each Plugin provider must have a unique Name. | [optional] 
**optional_params** | **list[str]** | OptionalParams are Params that can be present on a Plugin for the Provider to operate.  This is used to ensure default parameters are available. | [optional] 
**plugin_version** | **int** | This is used to indicate what version the plugin is built for This is effectively the API version of the protocol that plugin providers use to communicate with dr-provision. Right now, all plugin providers must set this to version 4, which is the only supported protocol version. | [optional] 
**required_params** | **list[str]** | RequiredParams are Params that must be present on a Plugin for the Provider to operate. | [optional] 
**store_objects** | **dict(str, object)** | Object prefixes that can be accessed by this plugin. The interface can be empty struct{} or a JSONSchema draft v4 This allows PluginProviders to define custom Object types that dr-provision will store and check the validity of. | [optional] 
**version** | **str** | The version of the PluginProvider.  This is a semver compatible string. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


