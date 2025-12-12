# AccountUpdatedResponseData

Updated account data

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Updated account ID | [optional] 
**message** | **str** | Success message | [optional] 

## Example

```python
from orbuculum_client.models.account_updated_response_data import AccountUpdatedResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AccountUpdatedResponseData from a JSON string
account_updated_response_data_instance = AccountUpdatedResponseData.from_json(json)
# print the JSON string representation of the object
print(AccountUpdatedResponseData.to_json())

# convert the object into a dict
account_updated_response_data_dict = account_updated_response_data_instance.to_dict()
# create an instance of AccountUpdatedResponseData from a dict
account_updated_response_data_from_dict = AccountUpdatedResponseData.from_dict(account_updated_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


