# ActivateEntity200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** |  | [optional] 
**data** | [**ActivateEntity200ResponseData**](ActivateEntity200ResponseData.md) |  | [optional] 

## Example

```python
from orbuculum_client.models.activate_entity200_response import ActivateEntity200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ActivateEntity200Response from a JSON string
activate_entity200_response_instance = ActivateEntity200Response.from_json(json)
# print the JSON string representation of the object
print(ActivateEntity200Response.to_json())

# convert the object into a dict
activate_entity200_response_dict = activate_entity200_response_instance.to_dict()
# create an instance of ActivateEntity200Response from a dict
activate_entity200_response_from_dict = ActivateEntity200Response.from_dict(activate_entity200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


