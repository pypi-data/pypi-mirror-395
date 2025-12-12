# MachineFingerprint

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**csn_hash** | **list[int]** | DMI.System.Manufacturer + DMI.System.ProductName + DMI.Chassis[0].SerialNumber, SHA256 hashed Hash must not be zero-length to match. 25 points | [optional] 
**cloud_instance_id** | **str** | Cloud-init file in /run/cloud-init/instance-data.json String from ID of &#39;.v1.cloud_name&#39; + &#39;.v1.instance_id&#39;. 500 point match | [optional] 
**memory_ids** | **list[list[int]]** | MemoryIds is an array of SHA256sums if the following fields in each entry of the DMI.Memory.Devices array concatenated together: Manufacturer PartNumber SerialNumber Each hash must not be zero length Score is % matched. | [optional] 
**ssn_hash** | **list[int]** | DMI.System.Manufacturer + DMI.System.ProductName + DMI.System.SerialNumber, SHA256 hashed Hash must not be zero-length to match. 25 points | [optional] 
**system_uuid** | **str** | DMI.System.UUID, not hashed. Must be non zero length and must be a non-zero UUID. 50 point match | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


