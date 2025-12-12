# GetAccountPermissionsResponseData

Permissions grouped by type

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**GetAccountPermissionsResponseDataPermissions**](GetAccountPermissionsResponseDataPermissions.md) |  | [optional] 

## Example

```python
from orbuculum_client.models.get_account_permissions_response_data import GetAccountPermissionsResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetAccountPermissionsResponseData from a JSON string
get_account_permissions_response_data_instance = GetAccountPermissionsResponseData.from_json(json)
# print the JSON string representation of the object
print(GetAccountPermissionsResponseData.to_json())

# convert the object into a dict
get_account_permissions_response_data_dict = get_account_permissions_response_data_instance.to_dict()
# create an instance of GetAccountPermissionsResponseData from a dict
get_account_permissions_response_data_from_dict = GetAccountPermissionsResponseData.from_dict(get_account_permissions_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


