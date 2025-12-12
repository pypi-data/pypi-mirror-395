# GetEntities200ResponseData

Entity data - array when getting all entities, object when getting by ID

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**type** | **int** |  | [optional] 
**type_name** | **str** |  | [optional] 
**hidden** | **bool** |  | [optional] 

## Example

```python
from orbuculum_client.models.get_entities200_response_data import GetEntities200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetEntities200ResponseData from a JSON string
get_entities200_response_data_instance = GetEntities200ResponseData.from_json(json)
# print the JSON string representation of the object
print(GetEntities200ResponseData.to_json())

# convert the object into a dict
get_entities200_response_data_dict = get_entities200_response_data_instance.to_dict()
# create an instance of GetEntities200ResponseData from a dict
get_entities200_response_data_from_dict = GetEntities200ResponseData.from_dict(get_entities200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


