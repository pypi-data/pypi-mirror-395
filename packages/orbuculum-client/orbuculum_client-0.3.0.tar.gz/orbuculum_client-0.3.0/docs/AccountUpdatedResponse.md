# AccountUpdatedResponse

Response after successfully updating an account

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** | HTTP status code | 
**data** | [**AccountUpdatedResponseData**](AccountUpdatedResponseData.md) |  | 

## Example

```python
from orbuculum_client.models.account_updated_response import AccountUpdatedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccountUpdatedResponse from a JSON string
account_updated_response_instance = AccountUpdatedResponse.from_json(json)
# print the JSON string representation of the object
print(AccountUpdatedResponse.to_json())

# convert the object into a dict
account_updated_response_dict = account_updated_response_instance.to_dict()
# create an instance of AccountUpdatedResponse from a dict
account_updated_response_from_dict = AccountUpdatedResponse.from_dict(account_updated_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


