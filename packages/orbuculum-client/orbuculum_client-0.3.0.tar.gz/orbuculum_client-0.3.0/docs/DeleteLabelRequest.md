# DeleteLabelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** | Workspace ID | 
**id** | **int** | Label ID to delete | 

## Example

```python
from orbuculum_client.models.delete_label_request import DeleteLabelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteLabelRequest from a JSON string
delete_label_request_instance = DeleteLabelRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteLabelRequest.to_json())

# convert the object into a dict
delete_label_request_dict = delete_label_request_instance.to_dict()
# create an instance of DeleteLabelRequest from a dict
delete_label_request_from_dict = DeleteLabelRequest.from_dict(delete_label_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


