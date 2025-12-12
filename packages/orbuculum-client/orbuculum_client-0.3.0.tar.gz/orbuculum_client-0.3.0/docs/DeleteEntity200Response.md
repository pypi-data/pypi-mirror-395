# DeleteEntity200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** |  | [optional] 
**data** | [**DeleteEntity200ResponseData**](DeleteEntity200ResponseData.md) |  | [optional] 

## Example

```python
from orbuculum_client.models.delete_entity200_response import DeleteEntity200Response

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteEntity200Response from a JSON string
delete_entity200_response_instance = DeleteEntity200Response.from_json(json)
# print the JSON string representation of the object
print(DeleteEntity200Response.to_json())

# convert the object into a dict
delete_entity200_response_dict = delete_entity200_response_instance.to_dict()
# create an instance of DeleteEntity200Response from a dict
delete_entity200_response_from_dict = DeleteEntity200Response.from_dict(delete_entity200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


