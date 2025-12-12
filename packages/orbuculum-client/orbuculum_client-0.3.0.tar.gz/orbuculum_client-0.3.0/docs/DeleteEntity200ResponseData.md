# DeleteEntity200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**action** | **str** |  | [optional] 
**message** | **str** |  | [optional] 

## Example

```python
from orbuculum_client.models.delete_entity200_response_data import DeleteEntity200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteEntity200ResponseData from a JSON string
delete_entity200_response_data_instance = DeleteEntity200ResponseData.from_json(json)
# print the JSON string representation of the object
print(DeleteEntity200ResponseData.to_json())

# convert the object into a dict
delete_entity200_response_data_dict = delete_entity200_response_data_instance.to_dict()
# create an instance of DeleteEntity200ResponseData from a dict
delete_entity200_response_data_from_dict = DeleteEntity200ResponseData.from_dict(delete_entity200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


