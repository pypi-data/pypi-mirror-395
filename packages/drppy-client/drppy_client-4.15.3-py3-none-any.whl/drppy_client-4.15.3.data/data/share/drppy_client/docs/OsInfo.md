# OsInfo

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**codename** | **str** | The codename of the OS, if any. | [optional] 
**family** | **str** | The family of operating system (linux distro lineage, etc) | [optional] 
**iso_file** | **str** | The name of the ISO that the OS should install from.  If non-empty, this is assumed to be for the amd64 hardware architecture. | [optional] 
**iso_sha256** | **str** | The SHA256 of the ISO file.  Used to check for corrupt downloads. If non-empty, this is assumed to be for the amd64 hardware architecture. | [optional] 
**iso_url** | **str** | The URL that the ISO can be downloaded from, if any.  If non-empty, this is assumed to be for the amd64 hardware architecture. | [optional] 
**name** | **str** | The name of the OS this BootEnv has.  It should be formatted as family-version. | 
**supported_architectures** | [**dict(str, ArchInfo)**](ArchInfo.md) | SupportedArchitectures maps from hardware architecture (named according to the distro architecture naming scheme) to the architecture-specific parameters for this OS.  If SupportedArchitectures is left empty, then the system assumes that the BootEnv only supports amd64 platforms. | [optional] 
**version** | **str** | The version of the OS, if any. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


