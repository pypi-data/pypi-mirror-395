# UpdateCustomRecordsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** | Workspace ID where the custom table exists | 
**table_name** | **str** | Custom table name (prefix &#39;c_&#39; will be added automatically if not present) | 
**id** | **int** | Record ID to update. The record must have an &#39;id&#39; column. | 
**record_data** | **Dict[str, object]** | Key-value pairs of columns to update. Keys are column names, values are new data. Values can be of any type (string, number, boolean, null, object, or array). | 

## Example

```python
from orbuculum_client.models.update_custom_records_request import UpdateCustomRecordsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateCustomRecordsRequest from a JSON string
update_custom_records_request_instance = UpdateCustomRecordsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateCustomRecordsRequest.to_json())

# convert the object into a dict
update_custom_records_request_dict = update_custom_records_request_instance.to_dict()
# create an instance of UpdateCustomRecordsRequest from a dict
update_custom_records_request_from_dict = UpdateCustomRecordsRequest.from_dict(update_custom_records_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


