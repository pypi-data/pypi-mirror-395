# UpdateEntity200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** |  | [optional] 
**data** | [**UpdateEntity200ResponseData**](UpdateEntity200ResponseData.md) |  | [optional] 

## Example

```python
from orbuculum_client.models.update_entity200_response import UpdateEntity200Response

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateEntity200Response from a JSON string
update_entity200_response_instance = UpdateEntity200Response.from_json(json)
# print the JSON string representation of the object
print(UpdateEntity200Response.to_json())

# convert the object into a dict
update_entity200_response_dict = update_entity200_response_instance.to_dict()
# create an instance of UpdateEntity200Response from a dict
update_entity200_response_from_dict = UpdateEntity200Response.from_dict(update_entity200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


