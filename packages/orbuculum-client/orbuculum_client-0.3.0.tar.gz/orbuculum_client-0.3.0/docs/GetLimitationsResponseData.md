# GetLimitationsResponseData

Limitations grouped by type

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_limitations** | [**List[Limitation]**](Limitation.md) | Direct account limitations | [optional] 
**account_to_entity_limitations** | [**List[Limitation]**](Limitation.md) | Account to entity limitations | [optional] 

## Example

```python
from orbuculum_client.models.get_limitations_response_data import GetLimitationsResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetLimitationsResponseData from a JSON string
get_limitations_response_data_instance = GetLimitationsResponseData.from_json(json)
# print the JSON string representation of the object
print(GetLimitationsResponseData.to_json())

# convert the object into a dict
get_limitations_response_data_dict = get_limitations_response_data_instance.to_dict()
# create an instance of GetLimitationsResponseData from a dict
get_limitations_response_data_from_dict = GetLimitationsResponseData.from_dict(get_limitations_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


