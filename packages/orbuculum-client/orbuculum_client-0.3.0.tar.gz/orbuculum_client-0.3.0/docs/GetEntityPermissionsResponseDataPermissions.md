# GetEntityPermissionsResponseDataPermissions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**read** | [**List[EntityPermission]**](EntityPermission.md) | Read permissions | [optional] 
**manage** | [**List[EntityPermission]**](EntityPermission.md) | Manage permissions | [optional] 
**create** | [**List[EntityPermission]**](EntityPermission.md) | Create account permissions | [optional] 

## Example

```python
from orbuculum_client.models.get_entity_permissions_response_data_permissions import GetEntityPermissionsResponseDataPermissions

# TODO update the JSON string below
json = "{}"
# create an instance of GetEntityPermissionsResponseDataPermissions from a JSON string
get_entity_permissions_response_data_permissions_instance = GetEntityPermissionsResponseDataPermissions.from_json(json)
# print the JSON string representation of the object
print(GetEntityPermissionsResponseDataPermissions.to_json())

# convert the object into a dict
get_entity_permissions_response_data_permissions_dict = get_entity_permissions_response_data_permissions_instance.to_dict()
# create an instance of GetEntityPermissionsResponseDataPermissions from a dict
get_entity_permissions_response_data_permissions_from_dict = GetEntityPermissionsResponseDataPermissions.from_dict(get_entity_permissions_response_data_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


