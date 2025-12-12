# CreateTransactionRequest

Request body for creating a new transaction. At least one amount (sender_amount or receiver_amount) must be provided.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** | Workspace ID | 
**sender_account_id** | **int** | Sender account ID | 
**receiver_account_id** | **int** | Receiver account ID | 
**sender_amount** | **str** | Sender amount. Optional if receiver_amount is provided. | [optional] 
**receiver_amount** | **str** | Receiver amount. Optional if sender_amount is provided. | [optional] 
**dt** | **str** | Transaction date and time | 
**project_id** | **int** | Project ID (HISTORICAL: maps to label_id in DB) | 
**comment** | **str** | Transaction comment | [optional] 
**description** | **str** | Transaction description | [optional] 
**done** | **str** | Transaction status (true/false) | [optional] 
**commission_applied** | **bool** | Whether commission should be applied | [optional] 
**apikey** | **str** | API key for external integrations | [optional] 
**sender_commission** | [**CommissionData**](CommissionData.md) |  | [optional] 
**receiver_commission** | [**CommissionData**](CommissionData.md) |  | [optional] 

## Example

```python
from orbuculum_client.models.create_transaction_request import CreateTransactionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTransactionRequest from a JSON string
create_transaction_request_instance = CreateTransactionRequest.from_json(json)
# print the JSON string representation of the object
print(CreateTransactionRequest.to_json())

# convert the object into a dict
create_transaction_request_dict = create_transaction_request_instance.to_dict()
# create an instance of CreateTransactionRequest from a dict
create_transaction_request_from_dict = CreateTransactionRequest.from_dict(create_transaction_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


