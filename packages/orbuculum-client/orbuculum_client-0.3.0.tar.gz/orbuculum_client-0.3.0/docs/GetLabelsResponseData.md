# GetLabelsResponseData

Label data - array when getting all labels, object when getting by ID

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Label ID | [optional] 
**name** | **str** | Label name | [optional] 
**color** | **int** | Label color code | [optional] 
**icon** | **int** | Label icon code | [optional] 
**is_default** | **bool** | Whether this is a default label | [optional] 

## Example

```python
from orbuculum_client.models.get_labels_response_data import GetLabelsResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetLabelsResponseData from a JSON string
get_labels_response_data_instance = GetLabelsResponseData.from_json(json)
# print the JSON string representation of the object
print(GetLabelsResponseData.to_json())

# convert the object into a dict
get_labels_response_data_dict = get_labels_response_data_instance.to_dict()
# create an instance of GetLabelsResponseData from a dict
get_labels_response_data_from_dict = GetLabelsResponseData.from_dict(get_labels_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


