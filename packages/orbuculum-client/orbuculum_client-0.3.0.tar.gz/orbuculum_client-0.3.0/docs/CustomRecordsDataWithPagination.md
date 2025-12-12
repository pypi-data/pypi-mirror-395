# CustomRecordsDataWithPagination

Data object containing rows and pagination information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rows** | **List[Dict[str, object]]** | Array of records. Each record is a dynamic object with columns from your custom table. Values can be of any type (string, number, boolean, null, object, or array). | 
**total_count** | **int** | Total number of records matching the filter (before pagination) | 
**limit** | **int** | Number of records per page | 
**offset** | **int** | Starting position for pagination | 

## Example

```python
from orbuculum_client.models.custom_records_data_with_pagination import CustomRecordsDataWithPagination

# TODO update the JSON string below
json = "{}"
# create an instance of CustomRecordsDataWithPagination from a JSON string
custom_records_data_with_pagination_instance = CustomRecordsDataWithPagination.from_json(json)
# print the JSON string representation of the object
print(CustomRecordsDataWithPagination.to_json())

# convert the object into a dict
custom_records_data_with_pagination_dict = custom_records_data_with_pagination_instance.to_dict()
# create an instance of CustomRecordsDataWithPagination from a dict
custom_records_data_with_pagination_from_dict = CustomRecordsDataWithPagination.from_dict(custom_records_data_with_pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


