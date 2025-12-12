# CustomTableFilterGroup

Group definition for combining multiple filters with a specific logic operator

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique identifier for this group. Filters reference this ID to belong to this group. | 
**logic** | **str** | Logic operator to combine filters within this group | 

## Example

```python
from orbuculum_client.models.custom_table_filter_group import CustomTableFilterGroup

# TODO update the JSON string below
json = "{}"
# create an instance of CustomTableFilterGroup from a JSON string
custom_table_filter_group_instance = CustomTableFilterGroup.from_json(json)
# print the JSON string representation of the object
print(CustomTableFilterGroup.to_json())

# convert the object into a dict
custom_table_filter_group_dict = custom_table_filter_group_instance.to_dict()
# create an instance of CustomTableFilterGroup from a dict
custom_table_filter_group_from_dict = CustomTableFilterGroup.from_dict(custom_table_filter_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


