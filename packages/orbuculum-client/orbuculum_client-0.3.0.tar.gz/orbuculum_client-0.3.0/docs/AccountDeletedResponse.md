# AccountDeletedResponse

Response after successfully deleting an account

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** | HTTP status code | 
**data** | [**AccountDeletedResponseData**](AccountDeletedResponseData.md) |  | 

## Example

```python
from orbuculum_client.models.account_deleted_response import AccountDeletedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccountDeletedResponse from a JSON string
account_deleted_response_instance = AccountDeletedResponse.from_json(json)
# print the JSON string representation of the object
print(AccountDeletedResponse.to_json())

# convert the object into a dict
account_deleted_response_dict = account_deleted_response_instance.to_dict()
# create an instance of AccountDeletedResponse from a dict
account_deleted_response_from_dict = AccountDeletedResponse.from_dict(account_deleted_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


