# Element

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**actual_version** | **str** | ActualVersion is the actual catalog version referenced by this element. This is used for translating tip and stable into a real version. This is the source of the file element.  This can be a relative or absolute path or an URL. | [optional] 
**name** | **str** | Name defines the name of the element.  Normally, this is the name of the the DRP, DRPUX, filename, plugin, ContentPackage, or PluginProvider Name. For Global and Pref, these are the name of the global parameter or preference. | [optional] 
**replace_writable** | **bool** | ReplaceWritable tells whether or not content packs should replace writable content Defaults to false. | [optional] 
**type** | **str** | Type defines the type of element This can be: DRP, DRPUX, File, Global, Plugin, Pref, PluginProvider, ContentPackage | [optional] 
**version** | **str** | Version defines the short or reference version of the element. e.g. tip, stable, v4.3.6 | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


