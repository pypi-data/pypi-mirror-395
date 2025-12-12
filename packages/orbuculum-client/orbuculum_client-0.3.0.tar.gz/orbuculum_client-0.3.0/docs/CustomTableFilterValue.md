# CustomTableFilterValue

Value to compare against. Can be string, number, boolean, null, or array (for IN/NOT IN operators). Not required for IS NULL/IS NOT NULL operators.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from orbuculum_client.models.custom_table_filter_value import CustomTableFilterValue

# TODO update the JSON string below
json = "{}"
# create an instance of CustomTableFilterValue from a JSON string
custom_table_filter_value_instance = CustomTableFilterValue.from_json(json)
# print the JSON string representation of the object
print(CustomTableFilterValue.to_json())

# convert the object into a dict
custom_table_filter_value_dict = custom_table_filter_value_instance.to_dict()
# create an instance of CustomTableFilterValue from a dict
custom_table_filter_value_from_dict = CustomTableFilterValue.from_dict(custom_table_filter_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


