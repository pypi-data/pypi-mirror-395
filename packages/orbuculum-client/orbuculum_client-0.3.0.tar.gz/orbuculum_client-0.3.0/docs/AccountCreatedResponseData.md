# AccountCreatedResponseData

Created account data

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Created account ID | [optional] 
**message** | **str** | Success message | [optional] 

## Example

```python
from orbuculum_client.models.account_created_response_data import AccountCreatedResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AccountCreatedResponseData from a JSON string
account_created_response_data_instance = AccountCreatedResponseData.from_json(json)
# print the JSON string representation of the object
print(AccountCreatedResponseData.to_json())

# convert the object into a dict
account_created_response_data_dict = account_created_response_data_instance.to_dict()
# create an instance of AccountCreatedResponseData from a dict
account_created_response_data_from_dict = AccountCreatedResponseData.from_dict(account_created_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


