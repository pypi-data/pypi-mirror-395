# CreateEntity201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**type** | **int** |  | [optional] 
**type_name** | **str** |  | [optional] 
**message** | **str** |  | [optional] 

## Example

```python
from orbuculum_client.models.create_entity201_response_data import CreateEntity201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of CreateEntity201ResponseData from a JSON string
create_entity201_response_data_instance = CreateEntity201ResponseData.from_json(json)
# print the JSON string representation of the object
print(CreateEntity201ResponseData.to_json())

# convert the object into a dict
create_entity201_response_data_dict = create_entity201_response_data_instance.to_dict()
# create an instance of CreateEntity201ResponseData from a dict
create_entity201_response_data_from_dict = CreateEntity201ResponseData.from_dict(create_entity201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


