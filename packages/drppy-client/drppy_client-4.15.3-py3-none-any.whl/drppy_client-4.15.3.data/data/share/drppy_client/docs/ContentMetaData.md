# ContentMetaData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**author** | **str** | Author should contain the name of the author along with their email address. | [optional] 
**code_source** | **str** | CodeSource should be a URL to the repository that this content was built from, if applicable. | [optional] 
**color** | **str** | Color is the color the Icon should show up as in the UX.  Color names must be one of the ones available from https://react.semantic-ui.com/elements/button/#types-basic-shorthand | [optional] 
**copyright** | **str** | Copyright is the copyright terms for this content. | [optional] 
**description** | **str** | Description is a one or two line description of what the content bundle provides. | [optional] 
**display_name** | **str** | DisplayName is the froiendly name the UX will use by default. | [optional] 
**doc_url** | **str** | DocUrl should contain a link to external documentation for this content, if available. | [optional] 
**documentation** | **str** | Documentation should contain Sphinx RST formatted documentation for the content bundle describing its usage. | [optional] 
**icon** | **str** | Icon is the icon that should be used to represent this content bundle. We use icons from https://react.semantic-ui.com/elements/icon/ | [optional] 
**license** | **str** | License should be the name of the license that governs the terms the content is made available under. | [optional] 
**name** | **str** | Name is the name of the content bundle.  Name must be unique across all content bundles loaded into a given dr-provision instance. | 
**order** | **str** | Order gives a hint about the relaitve importance of this content when the UX is rendering it.  Deprecated, can be left blank. | [optional] 
**overwritable** | **bool** | Overwritable controls whether objects provided by this content store can be overridden by identically identified objects from another content bundle.  This will be false for everything but the BasicStore. This field is read-only, and cannot be changed via the API. | [optional] 
**prerequisites** | **str** | Prerequisites is also a comma-separated list that contains other (possibly version-qualified) content bundles that must be present for this content bundle to load into dr-provision.  Each entry in the Prerequisites list should be in for format of name: version constraints.  The colon and the version constraints may be omitted if there are no version restrictions on the required content bundle.  See ../doc/arch/content-package.rst for more detailed info. | [optional] 
**required_features** | **str** | RequiredFeatures is a comma-separated list of features that dr-provision must provide for the content bundle to operate properly. These correspond to the Features field in the Info struct. | [optional] 
**source** | **str** | Source is mostly deprecated, replaced by Author and CodeSource. It can be left blank. | [optional] 
**tags** | **str** | Tags is used in the UX to categorize content bundles according to various criteria.  It should be a comma-separated list of single words. | [optional] 
**type** | **str** | Type contains what type of content bundle this is.  It is read-only, and cannot be changed voa the API. | [optional] 
**version** | **str** | Version is a Semver-compliant string describing the version of the content as a whole.  If left empty, the version is assumed to be 0.0.0 | [optional] 
**writable** | **bool** | Writable controls whether objects provided by this content can be modified independently via the API. This will be false for everything but the BackingStore.  It is read-only, and cannot be changed via the API. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


