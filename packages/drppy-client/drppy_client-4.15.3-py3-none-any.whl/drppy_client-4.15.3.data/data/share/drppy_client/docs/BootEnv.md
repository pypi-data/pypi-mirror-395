# BootEnv

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**available** | **bool** | Available tracks whether or not the model passed validation. | [optional] 
**boot_params** | **str** | A template that will be expanded to create the full list of boot parameters for the environment.  This list will generally be passed as command line arguments to the Kernel as it boots up. | 
**bundle** | **str** | Bundle tracks the name of the store containing this object. This field is read-only, and cannot be changed via the API. | [optional] 
**created_at** | **datetime** | CreatedAt is the time that this object was created. | [optional] 
**created_by** | **str** | CreatedBy stores the value of the user that created this object. Note: This value is stored ONLY if the object was created by a user which means that &#x60;currentUserName&#x60; needs to be populated in the authBlob | [optional] 
**description** | **str** | Description is a string for providing a simple description | [optional] 
**documentation** | **str** | Documentation is a string for providing additional in depth information. | [optional] 
**end_delimiter** | **str** | EndDelimiter is an optional end delimiter. | [optional] 
**endpoint** | **str** | Endpoint tracks the owner of the object among DRP endpoints | [optional] 
**errors** | **list[str]** | If there are any errors in the validation process, they will be available here. | [optional] 
**initrds** | **list[str]** | Partial paths to the initrds that should be loaded for the boot environment. These should be paths that the initrds are located at in the OS ISO or install archive. | 
**kernel** | **str** | The partial path to the kernel for the boot environment.  This should be path that the kernel is located at in the OS ISO or install archive.  Kernel must be non-empty for a BootEnv to be considered net bootable. | 
**last_modified_at** | **datetime** | LastModifiedAt is the time that this object was last modified. | [optional] 
**last_modified_by** | **str** | LastModifiedBy stores the value of the user that last modified this object. NOTE: This value is populated ONLY if the object was modified by a user which means any actions done using machine tokens will not get tracked | [optional] 
**loaders** | **dict(str, str)** | Loaders contains the boot loaders that should be used for various different network boot scenarios.  It consists of a map of machine type -&gt; partial paths to the bootloaders. Valid machine types are:  386-pcbios for x86 devices using the legacy bios.  amd64-uefi for x86 devices operating in UEFI mode  arm64-uefi for arm64 devices operating in UEFI mode  Other machine types will be added as dr-provision gains support for them.  If this map does not contain an entry for the machine type, the DHCP server will fall back to the following entries in this order:  The Loader specified in the ArchInfo struct from this BootEnv, if it exists.  The value specified in the bootloaders param for the machine type specified on the machine, if it exists.  The value specified in the bootloaders param in the global profile, if it exists.  The value specified in the default value for the bootloaders param.  One of the following vaiues:  lpxelinux.0 for 386-pcbios  ipxe.efi for amd64-uefi  ipxe-arm64.efi for arm64-uefi | 
**meta** | [**Meta**](Meta.md) |  | [optional] 
**name** | **str** | Name is the name of the boot environment.  Boot environments that install an operating system must end in &#39;-install&#39;.  All boot environment names must be unique. | 
**os** | [**OsInfo**](OsInfo.md) |  | [optional] 
**only_unknown** | **bool** | OnlyUnknown indicates whether this bootenv can be used without a machine.  Only bootenvs with this flag set to &#x60;true&#x60; be used for the unknownBootEnv preference.  If this flag is set to True, then the Templates provided byt this boot environment must take care to be able to chainload into the appropriate boot environments for other machines if the bootloader that machine is using does not support it natively. The built-in ignore boot environment and the discovery boot environment provided by the community content bundle should be used as references for satisfying that requirement. | 
**optional_params** | **list[str]** | The list of extra optional parameters for this boot environment. They can be present as Machine.Params when the bootenv is applied to the machine.  These are more other consumers of the bootenv to know what parameters could additionally be applied to the bootenv by the renderer based upon the Machine.Params | [optional] 
**read_only** | **bool** | ReadOnly tracks if the store for this object is read-only. This flag is informational, and cannot be changed via the API. | [optional] 
**required_params** | **list[str]** | The list of extra required parameters for this boot environment. They should be present as Machine.Params when the bootenv is applied to the machine. | 
**start_delimiter** | **str** | StartDelimiter is an optional start delimiter. | [optional] 
**templates** | [**list[TemplateInfo]**](TemplateInfo.md) | Templates contains a list of templates that should be expanded into files for the boot environment.  These expanded templates will be available via TFTP and static HTTP from dr-provision.  You should take care that the final paths for the temmplates do not overlap with ones provided by other boot environments. | 
**validated** | **bool** | Validated tracks whether or not the model has been validated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


