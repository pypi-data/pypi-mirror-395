# LoginResponseDataUser

Authenticated user information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | User ID | 
**email** | **str** | User email | 
**name** | **str** | User display name | [optional] 

## Example

```python
from orbuculum_client.models.login_response_data_user import LoginResponseDataUser

# TODO update the JSON string below
json = "{}"
# create an instance of LoginResponseDataUser from a JSON string
login_response_data_user_instance = LoginResponseDataUser.from_json(json)
# print the JSON string representation of the object
print(LoginResponseDataUser.to_json())

# convert the object into a dict
login_response_data_user_dict = login_response_data_user_instance.to_dict()
# create an instance of LoginResponseDataUser from a dict
login_response_data_user_from_dict = LoginResponseDataUser.from_dict(login_response_data_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


