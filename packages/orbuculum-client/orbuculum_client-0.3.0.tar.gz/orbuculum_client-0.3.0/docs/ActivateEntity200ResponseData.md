# ActivateEntity200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**action** | **str** |  | [optional] 
**message** | **str** |  | [optional] 

## Example

```python
from orbuculum_client.models.activate_entity200_response_data import ActivateEntity200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of ActivateEntity200ResponseData from a JSON string
activate_entity200_response_data_instance = ActivateEntity200ResponseData.from_json(json)
# print the JSON string representation of the object
print(ActivateEntity200ResponseData.to_json())

# convert the object into a dict
activate_entity200_response_data_dict = activate_entity200_response_data_instance.to_dict()
# create an instance of ActivateEntity200ResponseData from a dict
activate_entity200_response_data_from_dict = ActivateEntity200ResponseData.from_dict(activate_entity200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


