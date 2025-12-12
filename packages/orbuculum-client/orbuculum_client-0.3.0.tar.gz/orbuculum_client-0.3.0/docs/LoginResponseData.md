# LoginResponseData

Response data

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** | JWT token for API authentication | 
**user** | [**LoginResponseDataUser**](LoginResponseDataUser.md) |  | 

## Example

```python
from orbuculum_client.models.login_response_data import LoginResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of LoginResponseData from a JSON string
login_response_data_instance = LoginResponseData.from_json(json)
# print the JSON string representation of the object
print(LoginResponseData.to_json())

# convert the object into a dict
login_response_data_dict = login_response_data_instance.to_dict()
# create an instance of LoginResponseData from a dict
login_response_data_from_dict = LoginResponseData.from_dict(login_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


