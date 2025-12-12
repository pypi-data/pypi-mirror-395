# orbuculum_client.EntityApi

All URIs are relative to *https://s1.orbuculum.app*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate_entity**](EntityApi.md#activate_entity) | **POST** /api/entity/activate | Activate entity
[**create_entity**](EntityApi.md#create_entity) | **POST** /api/entity/create | Create entity
[**delete_entity**](EntityApi.md#delete_entity) | **POST** /api/entity/delete | Delete entity
[**get_entities**](EntityApi.md#get_entities) | **GET** /api/entity/get | Get entities
[**update_entity**](EntityApi.md#update_entity) | **POST** /api/entity/update | Update entity


# **activate_entity**
> ActivateEntity200Response activate_entity(activate_entity_request)

Activate entity

Activates an archived entity. All accounts within this entity will also be activated.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.activate_entity200_response import ActivateEntity200Response
from orbuculum_client.models.activate_entity_request import ActivateEntityRequest
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
    api_instance = orbuculum_client.EntityApi(api_client)
    activate_entity_request = orbuculum_client.ActivateEntityRequest() # ActivateEntityRequest | 

    try:
        # Activate entity
        api_response = api_instance.activate_entity(activate_entity_request)
        print("The response of EntityApi->activate_entity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EntityApi->activate_entity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activate_entity_request** | [**ActivateEntityRequest**](ActivateEntityRequest.md)|  | 

### Return type

[**ActivateEntity200Response**](ActivateEntity200Response.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Entity activated successfully |  -  |
**401** | Unauthorized - invalid or expired token |  -  |
**403** | Forbidden - no manage permission for this entity |  -  |
**404** | Entity not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity**
> CreateEntity201Response create_entity(create_entity_request)

Create entity

Creates a new entity with automatic permission setup. The creator and all users with full access will automatically get read, manage, and account creation permissions for this entity.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.create_entity201_response import CreateEntity201Response
from orbuculum_client.models.create_entity_request import CreateEntityRequest
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
    api_instance = orbuculum_client.EntityApi(api_client)
    create_entity_request = orbuculum_client.CreateEntityRequest() # CreateEntityRequest | 

    try:
        # Create entity
        api_response = api_instance.create_entity(create_entity_request)
        print("The response of EntityApi->create_entity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EntityApi->create_entity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_entity_request** | [**CreateEntityRequest**](CreateEntityRequest.md)|  | 

### Return type

[**CreateEntity201Response**](CreateEntity201Response.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Entity created successfully |  -  |
**400** | Bad request - validation failed |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden - no permission to create entities |  -  |
**409** | Conflict - entity name already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity**
> DeleteEntity200Response delete_entity(delete_entity_request)

Delete entity

Deletes or archives an entity. If entity has dependent data (accounts, transactions), it will be archived instead of permanently deleted. All accounts in archived entity will also be archived.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.delete_entity200_response import DeleteEntity200Response
from orbuculum_client.models.delete_entity_request import DeleteEntityRequest
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
    api_instance = orbuculum_client.EntityApi(api_client)
    delete_entity_request = orbuculum_client.DeleteEntityRequest() # DeleteEntityRequest | 

    try:
        # Delete entity
        api_response = api_instance.delete_entity(delete_entity_request)
        print("The response of EntityApi->delete_entity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EntityApi->delete_entity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delete_entity_request** | [**DeleteEntityRequest**](DeleteEntityRequest.md)|  | 

### Return type

[**DeleteEntity200Response**](DeleteEntity200Response.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Entity deleted or archived successfully |  -  |
**401** | Unauthorized - invalid or expired token |  -  |
**403** | Forbidden - no manage permission for this entity |  -  |
**404** | Entity not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entities**
> GetEntities200Response get_entities(workspace_id, id=id)

Get entities

Retrieve list of all entities or specific entity by ID. Returns only entities the user has permission to access.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.get_entities200_response import GetEntities200Response
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
    api_instance = orbuculum_client.EntityApi(api_client)
    workspace_id = 1 # int | Workspace ID
    id = 1 # int | Entity ID (optional, returns all if not specified) (optional)

    try:
        # Get entities
        api_response = api_instance.get_entities(workspace_id, id=id)
        print("The response of EntityApi->get_entities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EntityApi->get_entities: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| Workspace ID | 
 **id** | **int**| Entity ID (optional, returns all if not specified) | [optional] 

### Return type

[**GetEntities200Response**](GetEntities200Response.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Entities retrieved successfully (array of entities or single entity object) |  -  |
**401** | Unauthorized - invalid or expired token |  -  |
**403** | Forbidden - insufficient permissions |  -  |
**404** | Entity not found or workspace not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity**
> UpdateEntity200Response update_entity(update_entity_request)

Update entity

Updates an existing entity. Requires manage permission. If entity type is changed, all accounts within this entity will also have their type updated.

### Example

* Bearer (JWT) Authentication (bearerAuth):

```python
import orbuculum_client
from orbuculum_client.models.update_entity200_response import UpdateEntity200Response
from orbuculum_client.models.update_entity_request import UpdateEntityRequest
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
    api_instance = orbuculum_client.EntityApi(api_client)
    update_entity_request = orbuculum_client.UpdateEntityRequest() # UpdateEntityRequest | 

    try:
        # Update entity
        api_response = api_instance.update_entity(update_entity_request)
        print("The response of EntityApi->update_entity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EntityApi->update_entity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_entity_request** | [**UpdateEntityRequest**](UpdateEntityRequest.md)|  | 

### Return type

[**UpdateEntity200Response**](UpdateEntity200Response.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Entity updated successfully |  -  |
**401** | Unauthorized - invalid or expired token |  -  |
**403** | Forbidden - no manage permission for this entity |  -  |
**404** | Entity not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

