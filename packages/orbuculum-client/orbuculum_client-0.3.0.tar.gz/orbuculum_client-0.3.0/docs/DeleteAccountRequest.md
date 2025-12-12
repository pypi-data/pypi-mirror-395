# DeleteAccountRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** | Workspace ID | 
**id** | **int** | Account ID to delete | 

## Example

```python
from orbuculum_client.models.delete_account_request import DeleteAccountRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteAccountRequest from a JSON string
delete_account_request_instance = DeleteAccountRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteAccountRequest.to_json())

# convert the object into a dict
delete_account_request_dict = delete_account_request_instance.to_dict()
# create an instance of DeleteAccountRequest from a dict
delete_account_request_from_dict = DeleteAccountRequest.from_dict(delete_account_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


