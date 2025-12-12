# Connection

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**create_time** | **datetime** | CreateTime is when the connection started from the perspective of the DRP Endpoint | [optional] 
**expires_at** | **datetime** | ExpiresAt is when the token/authentication method will expire | [optional] 
**principal** | **str** | Prinicipal is the authenticated entity connecting The string is an method and the identity separated by colon e.g. user:rocketskates or runner:&lt;uuid of machine&gt; | [optional] 
**remote_addr** | **str** | RemoteAddr is the IP:Port pair of the remote connection | [optional] 
**type** | **str** | Type reflects the connection type: websocket or api | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


