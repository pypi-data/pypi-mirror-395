# GetEntityPermissionsResponseData

Permissions grouped by type

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**GetEntityPermissionsResponseDataPermissions**](GetEntityPermissionsResponseDataPermissions.md) |  | [optional] 

## Example

```python
from orbuculum_client.models.get_entity_permissions_response_data import GetEntityPermissionsResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetEntityPermissionsResponseData from a JSON string
get_entity_permissions_response_data_instance = GetEntityPermissionsResponseData.from_json(json)
# print the JSON string representation of the object
print(GetEntityPermissionsResponseData.to_json())

# convert the object into a dict
get_entity_permissions_response_data_dict = get_entity_permissions_response_data_instance.to_dict()
# create an instance of GetEntityPermissionsResponseData from a dict
get_entity_permissions_response_data_from_dict = GetEntityPermissionsResponseData.from_dict(get_entity_permissions_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


