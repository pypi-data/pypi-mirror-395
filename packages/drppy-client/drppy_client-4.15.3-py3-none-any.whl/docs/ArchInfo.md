# ArchInfo

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**boot_params** | **str** | A template that will be expanded to create the full list of boot parameters for the environment.  If empty, this will fall back to the top-level BootParams field in the BootEnv | 
**initrds** | **list[str]** | Partial paths to the initrds that should be loaded for the boot environment. These should be paths that the initrds are located at in the OS ISO or install archive.  If empty, this will fall back to the top-level Initrds field in the BootEnv | 
**iso_file** | **str** | IsoFile is the name of the ISO file (or other archive) that contains all the necessary information to be able to boot into this BootEnv for a given arch. At a minimum, it must contain a kernel and initrd that can be booted over the network. | [optional] 
**iso_url** | **str** | IsoUrl is the location that IsoFile can be downloaded from, if any. This must be a full URL, including the filename.  dr-provision does not use this field internally.  drpcli and the UX use this field to provide a default source for downloading the IsoFile. | [optional] 
**kernel** | **str** | The partial path to the kernel for the boot environment.  This should be path that the kernel is located at in the OS ISO or install archive.  If empty, this will fall back to the top-level Kernel field in the BootEnv | 
**loader** | **str** | Loader is the bootloader that should be used for this boot environment.  If left unspecified and not overridden by a subnet or reservation option, the following boot loaders will be used:  lpxelinux.0 on 386-pcbios platforms that are not otherwise using ipxe.  ipxe.pxe on 386-pcbios platforms that already use ipxe.  ipxe.efi on amd64 EFI platforms.  ipxe-arm64.efi on arm64 EFI platforms.  This setting will be overridden by Subnet and Reservation options, and it will also only be in effect when dr-provision is the DHCP server of record.  It will also be overridden by the corresponding entry in the Loaders field of the BootEnv, if present and secure boot is enabled by the license. | [optional] 
**sha256** | **str** | Sha256 should contain the SHA256 checksum for the IsoFile. If it does, the IsoFile will be checked upon upload to make sure it has not been corrupted. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


