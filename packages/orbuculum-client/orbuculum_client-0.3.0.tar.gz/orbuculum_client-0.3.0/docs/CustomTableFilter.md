# CustomTableFilter

Single filter condition for custom table queries

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_field** | **str** | Column name to filter by | 
**operator** | **str** | Comparison operator. ILIKE and NOT ILIKE are case-insensitive versions for PostgreSQL. | 
**value** | [**CustomTableFilterValue**](CustomTableFilterValue.md) |  | [optional] 
**group** | **int** | Group ID this filter belongs to. Filters with the same group ID are combined using the group&#39;s logic operator. If not specified, filter is not grouped. | [optional] 

## Example

```python
from orbuculum_client.models.custom_table_filter import CustomTableFilter

# TODO update the JSON string below
json = "{}"
# create an instance of CustomTableFilter from a JSON string
custom_table_filter_instance = CustomTableFilter.from_json(json)
# print the JSON string representation of the object
print(CustomTableFilter.to_json())

# convert the object into a dict
custom_table_filter_dict = custom_table_filter_instance.to_dict()
# create an instance of CustomTableFilter from a dict
custom_table_filter_from_dict = CustomTableFilter.from_dict(custom_table_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


