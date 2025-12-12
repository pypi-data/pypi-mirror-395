# CustomTableOrderBy

Sorting configuration for custom table queries

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_field** | **str** | Column name to sort by | 
**direction** | **str** | Sort direction | [default to 'ASC']

## Example

```python
from orbuculum_client.models.custom_table_order_by import CustomTableOrderBy

# TODO update the JSON string below
json = "{}"
# create an instance of CustomTableOrderBy from a JSON string
custom_table_order_by_instance = CustomTableOrderBy.from_json(json)
# print the JSON string representation of the object
print(CustomTableOrderBy.to_json())

# convert the object into a dict
custom_table_order_by_dict = custom_table_order_by_instance.to_dict()
# create an instance of CustomTableOrderBy from a dict
custom_table_order_by_from_dict = CustomTableOrderBy.from_dict(custom_table_order_by_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


