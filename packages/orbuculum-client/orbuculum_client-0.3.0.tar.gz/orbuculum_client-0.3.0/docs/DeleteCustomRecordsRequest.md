# DeleteCustomRecordsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** | Workspace ID where the custom table exists | 
**table_name** | **str** | Custom table name (prefix &#39;c_&#39; will be added automatically if not present) | 
**id** | **int** | Record ID to delete. The record must have an &#39;id&#39; column. | 

## Example

```python
from orbuculum_client.models.delete_custom_records_request import DeleteCustomRecordsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteCustomRecordsRequest from a JSON string
delete_custom_records_request_instance = DeleteCustomRecordsRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteCustomRecordsRequest.to_json())

# convert the object into a dict
delete_custom_records_request_dict = delete_custom_records_request_instance.to_dict()
# create an instance of DeleteCustomRecordsRequest from a dict
delete_custom_records_request_from_dict = DeleteCustomRecordsRequest.from_dict(delete_custom_records_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


