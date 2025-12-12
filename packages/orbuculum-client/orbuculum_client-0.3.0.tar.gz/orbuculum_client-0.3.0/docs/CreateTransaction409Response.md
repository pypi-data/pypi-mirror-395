# CreateTransaction409Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** |  | [optional] 
**error** | **str** |  | [optional] 

## Example

```python
from orbuculum_client.models.create_transaction409_response import CreateTransaction409Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTransaction409Response from a JSON string
create_transaction409_response_instance = CreateTransaction409Response.from_json(json)
# print the JSON string representation of the object
print(CreateTransaction409Response.to_json())

# convert the object into a dict
create_transaction409_response_dict = create_transaction409_response_instance.to_dict()
# create an instance of CreateTransaction409Response from a dict
create_transaction409_response_from_dict = CreateTransaction409Response.from_dict(create_transaction409_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


