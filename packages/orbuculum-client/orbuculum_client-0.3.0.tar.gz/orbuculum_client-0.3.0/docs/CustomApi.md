# orbuculum_client.CustomApi

All URIs are relative to *https://s1.orbuculum.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_custom_record**](CustomApi.md#create_custom_record) | **POST** /api/custom/create | Create a record in custom table
[**delete_custom_records**](CustomApi.md#delete_custom_records) | **POST** /api/custom/delete | Delete record from custom table by ID
[**get_custom_tables**](CustomApi.md#get_custom_tables) | **GET** /api/custom/tables | Get list of custom tables
[**read_custom_records**](CustomApi.md#read_custom_records) | **POST** /api/custom/read | Read records from custom table with flexible filtering
[**update_custom_records**](CustomApi.md#update_custom_records) | **POST** /api/custom/update | Update record in custom table by ID


# **create_custom_record**
> CreateCustomRecordResponse create_custom_record(create_custom_record_request)

Create a record in custom table

Inserts a new record into a custom table. Custom tables must exist in the project database and have 'c_' prefix (auto-added if not provided). You can specify any columns that exist in the target table. The table structure is not predefined - it depends on your custom table schema.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.create_custom_record_request import CreateCustomRecordRequest
from orbuculum_client.models.create_custom_record_response import CreateCustomRecordResponse
from orbuculum_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://s1.orbuculum.app
# See configuration.py for a list of all supported configuration parameters.
configuration = orbuculum_client.Configuration(
    host = "https://s1.orbuculum.app"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = orbuculum_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with orbuculum_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = orbuculum_client.CustomApi(api_client)
    create_custom_record_request = orbuculum_client.CreateCustomRecordRequest() # CreateCustomRecordRequest | 

    try:
        # Create a record in custom table
        api_response = api_instance.create_custom_record(create_custom_record_request)
        print("The response of CustomApi->create_custom_record:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomApi->create_custom_record: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_custom_record_request** | [**CreateCustomRecordRequest**](CreateCustomRecordRequest.md)|  | 

### Return type

[**CreateCustomRecordResponse**](CreateCustomRecordResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Record created successfully |  -  |
**400** | Bad request - validation failed or table does not exist |  -  |
**401** | Unauthorized |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_custom_records**
> DeleteCustomRecordsResponse delete_custom_records(delete_custom_records_request)

Delete record from custom table by ID

Permanently deletes a single record from a custom table by its ID. The table must have an 'id' column. The 'c_' prefix is added automatically to table name if not present. This action cannot be undone.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.delete_custom_records_request import DeleteCustomRecordsRequest
from orbuculum_client.models.delete_custom_records_response import DeleteCustomRecordsResponse
from orbuculum_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://s1.orbuculum.app
# See configuration.py for a list of all supported configuration parameters.
configuration = orbuculum_client.Configuration(
    host = "https://s1.orbuculum.app"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = orbuculum_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with orbuculum_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = orbuculum_client.CustomApi(api_client)
    delete_custom_records_request = orbuculum_client.DeleteCustomRecordsRequest() # DeleteCustomRecordsRequest | 

    try:
        # Delete record from custom table by ID
        api_response = api_instance.delete_custom_records(delete_custom_records_request)
        print("The response of CustomApi->delete_custom_records:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomApi->delete_custom_records: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delete_custom_records_request** | [**DeleteCustomRecordsRequest**](DeleteCustomRecordsRequest.md)|  | 

### Return type

[**DeleteCustomRecordsResponse**](DeleteCustomRecordsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Record deleted successfully |  -  |
**400** | Bad request - validation failed or table does not exist |  -  |
**401** | Unauthorized - invalid or expired token |  -  |
**404** | Record not found - specified record does not exist in the table |  -  |
**405** | Method not allowed |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_tables**
> GetCustomTablesResponse get_custom_tables(workspace_id)

Get list of custom tables

Returns a list of all custom tables (with 'c_' prefix) in the project database along with their column names and data types. This helps you understand the available tables and their schema before performing CRUD operations.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.get_custom_tables_response import GetCustomTablesResponse
from orbuculum_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://s1.orbuculum.app
# See configuration.py for a list of all supported configuration parameters.
configuration = orbuculum_client.Configuration(
    host = "https://s1.orbuculum.app"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = orbuculum_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with orbuculum_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = orbuculum_client.CustomApi(api_client)
    workspace_id = 1 # int | Workspace ID to get custom tables from

    try:
        # Get list of custom tables
        api_response = api_instance.get_custom_tables(workspace_id)
        print("The response of CustomApi->get_custom_tables:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomApi->get_custom_tables: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| Workspace ID to get custom tables from | 

### Return type

[**GetCustomTablesResponse**](GetCustomTablesResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of custom tables retrieved successfully |  -  |
**400** | Bad request - validation failed |  -  |
**401** | Unauthorized - invalid or expired token |  -  |
**405** | Method not allowed |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_custom_records**
> ReadCustomRecordsResponse read_custom_records(read_custom_records_request)

Read records from custom table with flexible filtering

Retrieves records from a custom table with support for complex filtering including multiple conditions, logical operators (AND/OR), groups, comparison operators, pagination and sorting. The 'c_' prefix is added automatically to table name if not present.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.read_custom_records_request import ReadCustomRecordsRequest
from orbuculum_client.models.read_custom_records_response import ReadCustomRecordsResponse
from orbuculum_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://s1.orbuculum.app
# See configuration.py for a list of all supported configuration parameters.
configuration = orbuculum_client.Configuration(
    host = "https://s1.orbuculum.app"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = orbuculum_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with orbuculum_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = orbuculum_client.CustomApi(api_client)
    read_custom_records_request = orbuculum_client.ReadCustomRecordsRequest() # ReadCustomRecordsRequest | 

    try:
        # Read records from custom table with flexible filtering
        api_response = api_instance.read_custom_records(read_custom_records_request)
        print("The response of CustomApi->read_custom_records:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomApi->read_custom_records: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **read_custom_records_request** | [**ReadCustomRecordsRequest**](ReadCustomRecordsRequest.md)|  | 

### Return type

[**ReadCustomRecordsResponse**](ReadCustomRecordsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Records retrieved successfully |  -  |
**400** | Bad request - validation failed or table does not exist |  -  |
**401** | Unauthorized - invalid or expired token |  -  |
**405** | Method not allowed |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_custom_records**
> UpdateCustomRecordsResponse update_custom_records(update_custom_records_request)

Update record in custom table by ID

Updates an existing record in a custom table by its ID. The table must have an 'id' column. The 'c_' prefix is added automatically to table name if not present. You can update any columns that exist in the target table.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.update_custom_records_request import UpdateCustomRecordsRequest
from orbuculum_client.models.update_custom_records_response import UpdateCustomRecordsResponse
from orbuculum_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://s1.orbuculum.app
# See configuration.py for a list of all supported configuration parameters.
configuration = orbuculum_client.Configuration(
    host = "https://s1.orbuculum.app"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearerAuth
configuration = orbuculum_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with orbuculum_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = orbuculum_client.CustomApi(api_client)
    update_custom_records_request = orbuculum_client.UpdateCustomRecordsRequest() # UpdateCustomRecordsRequest | 

    try:
        # Update record in custom table by ID
        api_response = api_instance.update_custom_records(update_custom_records_request)
        print("The response of CustomApi->update_custom_records:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomApi->update_custom_records: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_custom_records_request** | [**UpdateCustomRecordsRequest**](UpdateCustomRecordsRequest.md)|  | 

### Return type

[**UpdateCustomRecordsResponse**](UpdateCustomRecordsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Record updated successfully |  -  |
**400** | Bad request - validation failed or table does not exist |  -  |
**401** | Unauthorized - invalid or expired token |  -  |
**404** | Record not found - specified record does not exist in the table |  -  |
**405** | Method not allowed |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

