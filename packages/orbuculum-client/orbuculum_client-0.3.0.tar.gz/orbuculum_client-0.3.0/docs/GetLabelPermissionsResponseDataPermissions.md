# GetLabelPermissionsResponseDataPermissions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**read** | [**List[LabelPermission]**](LabelPermission.md) | Read permissions | [optional] 
**manage** | [**List[LabelPermission]**](LabelPermission.md) | Manage permissions | [optional] 

## Example

```python
from orbuculum_client.models.get_label_permissions_response_data_permissions import GetLabelPermissionsResponseDataPermissions

# TODO update the JSON string below
json = "{}"
# create an instance of GetLabelPermissionsResponseDataPermissions from a JSON string
get_label_permissions_response_data_permissions_instance = GetLabelPermissionsResponseDataPermissions.from_json(json)
# print the JSON string representation of the object
print(GetLabelPermissionsResponseDataPermissions.to_json())

# convert the object into a dict
get_label_permissions_response_data_permissions_dict = get_label_permissions_response_data_permissions_instance.to_dict()
# create an instance of GetLabelPermissionsResponseDataPermissions from a dict
get_label_permissions_response_data_permissions_from_dict = GetLabelPermissionsResponseDataPermissions.from_dict(get_label_permissions_response_data_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


