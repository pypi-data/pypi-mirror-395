# ReadCustomRecordsResponse

Response containing custom table records with pagination info

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** | HTTP status code | 
**data** | [**CustomRecordsDataWithPagination**](CustomRecordsDataWithPagination.md) |  | 

## Example

```python
from orbuculum_client.models.read_custom_records_response import ReadCustomRecordsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReadCustomRecordsResponse from a JSON string
read_custom_records_response_instance = ReadCustomRecordsResponse.from_json(json)
# print the JSON string representation of the object
print(ReadCustomRecordsResponse.to_json())

# convert the object into a dict
read_custom_records_response_dict = read_custom_records_response_instance.to_dict()
# create an instance of ReadCustomRecordsResponse from a dict
read_custom_records_response_from_dict = ReadCustomRecordsResponse.from_dict(read_custom_records_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


