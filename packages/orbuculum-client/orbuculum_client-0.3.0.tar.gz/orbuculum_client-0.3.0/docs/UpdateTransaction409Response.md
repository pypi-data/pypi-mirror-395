# UpdateTransaction409Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** |  | [optional] 
**error** | **str** |  | [optional] 

## Example

```python
from orbuculum_client.models.update_transaction409_response import UpdateTransaction409Response

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateTransaction409Response from a JSON string
update_transaction409_response_instance = UpdateTransaction409Response.from_json(json)
# print the JSON string representation of the object
print(UpdateTransaction409Response.to_json())

# convert the object into a dict
update_transaction409_response_dict = update_transaction409_response_instance.to_dict()
# create an instance of UpdateTransaction409Response from a dict
update_transaction409_response_from_dict = UpdateTransaction409Response.from_dict(update_transaction409_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


