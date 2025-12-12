# ReadCustomRecordsRequest

Request for reading custom table records with flexible filtering, grouping, pagination and sorting

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** | Workspace ID where the custom table exists | 
**table_name** | **str** | Custom table name (prefix &#39;c_&#39; will be added automatically if not present) | 
**filters** | [**List[CustomTableFilter]**](CustomTableFilter.md) | Array of filter conditions. Each filter can belong to a group. | [optional] 
**groups** | [**List[CustomTableFilterGroup]**](CustomTableFilterGroup.md) | Array of group definitions. Groups allow combining filters with different logic operators (AND/OR). | [optional] 
**root_logic** | **str** | Logic operator to combine groups | [optional] [default to 'AND']
**limit** | **int** | Maximum number of records to return (pagination) | [optional] [default to 100]
**offset** | **int** | Number of records to skip (pagination) | [optional] [default to 0]
**order_by** | [**CustomTableOrderBy**](CustomTableOrderBy.md) |  | [optional] 

## Example

```python
from orbuculum_client.models.read_custom_records_request import ReadCustomRecordsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReadCustomRecordsRequest from a JSON string
read_custom_records_request_instance = ReadCustomRecordsRequest.from_json(json)
# print the JSON string representation of the object
print(ReadCustomRecordsRequest.to_json())

# convert the object into a dict
read_custom_records_request_dict = read_custom_records_request_instance.to_dict()
# create an instance of ReadCustomRecordsRequest from a dict
read_custom_records_request_from_dict = ReadCustomRecordsRequest.from_dict(read_custom_records_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


