# AccountDeletedResponseData

Deleted account data

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Deleted account ID | [optional] 
**action** | **str** | Action performed | [optional] 
**message** | **str** | Success message | [optional] 

## Example

```python
from orbuculum_client.models.account_deleted_response_data import AccountDeletedResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AccountDeletedResponseData from a JSON string
account_deleted_response_data_instance = AccountDeletedResponseData.from_json(json)
# print the JSON string representation of the object
print(AccountDeletedResponseData.to_json())

# convert the object into a dict
account_deleted_response_data_dict = account_deleted_response_data_instance.to_dict()
# create an instance of AccountDeletedResponseData from a dict
account_deleted_response_data_from_dict = AccountDeletedResponseData.from_dict(account_deleted_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


