# ActivateEntityRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** | Workspace ID | 
**id** | **int** | Entity ID to activate | 

## Example

```python
from orbuculum_client.models.activate_entity_request import ActivateEntityRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ActivateEntityRequest from a JSON string
activate_entity_request_instance = ActivateEntityRequest.from_json(json)
# print the JSON string representation of the object
print(ActivateEntityRequest.to_json())

# convert the object into a dict
activate_entity_request_dict = activate_entity_request_instance.to_dict()
# create an instance of ActivateEntityRequest from a dict
activate_entity_request_from_dict = ActivateEntityRequest.from_dict(activate_entity_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


