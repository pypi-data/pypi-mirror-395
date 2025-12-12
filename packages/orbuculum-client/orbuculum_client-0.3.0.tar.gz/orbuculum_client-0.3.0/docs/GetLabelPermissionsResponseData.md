# GetLabelPermissionsResponseData

Permissions grouped by type

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**GetLabelPermissionsResponseDataPermissions**](GetLabelPermissionsResponseDataPermissions.md) |  | [optional] 

## Example

```python
from orbuculum_client.models.get_label_permissions_response_data import GetLabelPermissionsResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetLabelPermissionsResponseData from a JSON string
get_label_permissions_response_data_instance = GetLabelPermissionsResponseData.from_json(json)
# print the JSON string representation of the object
print(GetLabelPermissionsResponseData.to_json())

# convert the object into a dict
get_label_permissions_response_data_dict = get_label_permissions_response_data_instance.to_dict()
# create an instance of GetLabelPermissionsResponseData from a dict
get_label_permissions_response_data_from_dict = GetLabelPermissionsResponseData.from_dict(get_label_permissions_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


