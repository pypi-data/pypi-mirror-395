# GetAccountPermissionsResponseDataPermissions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**read** | [**List[AccountPermission]**](AccountPermission.md) | Read permissions | [optional] 
**manage** | [**List[AccountPermission]**](AccountPermission.md) | Manage permissions | [optional] 

## Example

```python
from orbuculum_client.models.get_account_permissions_response_data_permissions import GetAccountPermissionsResponseDataPermissions

# TODO update the JSON string below
json = "{}"
# create an instance of GetAccountPermissionsResponseDataPermissions from a JSON string
get_account_permissions_response_data_permissions_instance = GetAccountPermissionsResponseDataPermissions.from_json(json)
# print the JSON string representation of the object
print(GetAccountPermissionsResponseDataPermissions.to_json())

# convert the object into a dict
get_account_permissions_response_data_permissions_dict = get_account_permissions_response_data_permissions_instance.to_dict()
# create an instance of GetAccountPermissionsResponseDataPermissions from a dict
get_account_permissions_response_data_permissions_from_dict = GetAccountPermissionsResponseDataPermissions.from_dict(get_account_permissions_response_data_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


