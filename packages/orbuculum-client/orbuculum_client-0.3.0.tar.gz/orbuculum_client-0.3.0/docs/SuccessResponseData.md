# SuccessResponseData

Response data

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Success message | [optional] 

## Example

```python
from orbuculum_client.models.success_response_data import SuccessResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of SuccessResponseData from a JSON string
success_response_data_instance = SuccessResponseData.from_json(json)
# print the JSON string representation of the object
print(SuccessResponseData.to_json())

# convert the object into a dict
success_response_data_dict = success_response_data_instance.to_dict()
# create an instance of SuccessResponseData from a dict
success_response_data_from_dict = SuccessResponseData.from_dict(success_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


