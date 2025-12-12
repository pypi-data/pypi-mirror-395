# ErrorResponse409

Conflict error response - resource already exists or conflicts with existing data. May optionally include additional 'message' field with detailed error information for debugging purposes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** | HTTP status code | 
**error** | **str** | Error message indicating conflict | 

## Example

```python
from orbuculum_client.models.error_response409 import ErrorResponse409

# TODO update the JSON string below
json = "{}"
# create an instance of ErrorResponse409 from a JSON string
error_response409_instance = ErrorResponse409.from_json(json)
# print the JSON string representation of the object
print(ErrorResponse409.to_json())

# convert the object into a dict
error_response409_dict = error_response409_instance.to_dict()
# create an instance of ErrorResponse409 from a dict
error_response409_from_dict = ErrorResponse409.from_dict(error_response409_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


