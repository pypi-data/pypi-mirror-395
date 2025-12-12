# GetEntities200ResponseDataOneOfInner


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
from orbuculum_client.models.get_entities200_response_data_one_of_inner import GetEntities200ResponseDataOneOfInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetEntities200ResponseDataOneOfInner from a JSON string
get_entities200_response_data_one_of_inner_instance = GetEntities200ResponseDataOneOfInner.from_json(json)
# print the JSON string representation of the object
print(GetEntities200ResponseDataOneOfInner.to_json())

# convert the object into a dict
get_entities200_response_data_one_of_inner_dict = get_entities200_response_data_one_of_inner_instance.to_dict()
# create an instance of GetEntities200ResponseDataOneOfInner from a dict
get_entities200_response_data_one_of_inner_from_dict = GetEntities200ResponseDataOneOfInner.from_dict(get_entities200_response_data_one_of_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


