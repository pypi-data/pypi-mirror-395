# alchemite_apiclient.DefaultApi

All URIs are relative to *https://alchemiteapi.intellegens.ai/v0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query_v1_put**](DefaultApi.md#query_v1_put) | **PUT** /query/v1 | Query the datastore
[**suggest_initial_get**](DefaultApi.md#suggest_initial_get) | **GET** /suggest-initial | Get all suggest-initial jobs
[**suggest_initial_job_id_delete**](DefaultApi.md#suggest_initial_job_id_delete) | **DELETE** /suggest-initial/{job_id} | Delete suggest-initial job
[**suggest_initial_job_id_get**](DefaultApi.md#suggest_initial_job_id_get) | **GET** /suggest-initial/{job_id} | Get suggest-initial job data
[**suggest_initial_job_id_patch**](DefaultApi.md#suggest_initial_job_id_patch) | **PATCH** /suggest-initial/{job_id} | Update a suggest initial jobs&#39;s metadata
[**suggest_initial_post**](DefaultApi.md#suggest_initial_post) | **POST** /suggest-initial | Suggest initial DoE experiments without a trained model
[**version_get**](DefaultApi.md#version_get) | **GET** /version | Get API and application versions


# **query_v1_put**
> QueryResponse query_v1_put(query_request)

Query the datastore

Returns all rows matching the query passed. Will only return results on datasets that are in the 'uploaded' state. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import default_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.query_response import QueryResponse
from alchemite_apiclient.model.query_request import QueryRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    query_request = QueryRequest(None) # QueryRequest | 
    offset = 0 # int | The number of items to skip before starting to collect the result set. (optional) if omitted the server will use the default value of 0
    limit = 20 # int | The number of items to return. (optional) if omitted the server will use the default value of 20

    # example passing only required values which don't have defaults set
    try:
        # Query the datastore
        api_response = api_instance.query_v1_put(query_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->query_v1_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Query the datastore
        api_response = api_instance.query_v1_put(query_request, offset=offset, limit=limit)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->query_v1_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_request** | [**QueryRequest**](QueryRequest.md)|  |
 **offset** | **int**| The number of items to skip before starting to collect the result set. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| The number of items to return. | [optional] if omitted the server will use the default value of 20

### Return type

[**QueryResponse**](QueryResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query Response |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **suggest_initial_get**
> [SuggestInitialResponse] suggest_initial_get()

Get all suggest-initial jobs

Get all suggest-initial jobs

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import default_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_initial_response import SuggestInitialResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all suggest-initial jobs
        api_response = api_instance.suggest_initial_get()
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->suggest_initial_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[SuggestInitialResponse]**](SuggestInitialResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All suggest-initial jobs |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **suggest_initial_job_id_delete**
> suggest_initial_job_id_delete(job_id)

Delete suggest-initial job

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import default_api
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    job_id = "job_id_example" # str | Unique ID of the job

    # example passing only required values which don't have defaults set
    try:
        # Delete suggest-initial job
        api_instance.suggest_initial_job_id_delete(job_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->suggest_initial_job_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique ID of the job |

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Job deleted |  -  |
**400** | Invalid job ID |  -  |
**404** | Job ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **suggest_initial_job_id_get**
> SuggestInitialResponse suggest_initial_job_id_get(job_id)

Get suggest-initial job data

Get suggest-initial job data

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import default_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_initial_response import SuggestInitialResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    job_id = "job_id_example" # str | Unique ID of the job

    # example passing only required values which don't have defaults set
    try:
        # Get suggest-initial job data
        api_response = api_instance.suggest_initial_job_id_get(job_id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->suggest_initial_job_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique ID of the job |

### Return type

[**SuggestInitialResponse**](SuggestInitialResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning suggest-initial job data |  -  |
**400** | Bad request, e.g. invalid job ID |  -  |
**404** | Job ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **suggest_initial_job_id_patch**
> suggest_initial_job_id_patch(job_id)

Update a suggest initial jobs's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import default_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_initial_job_patch import SuggestInitialJobPatch
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    job_id = "job_id_example" # str | Unique ID of the job
    suggest_initial_job_patch = SuggestInitialJobPatch(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
        project_id="00112233-4455-6677-8899-aabbccddeeff",
    ) # SuggestInitialJobPatch |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a suggest initial jobs's metadata
        api_instance.suggest_initial_job_id_patch(job_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->suggest_initial_job_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a suggest initial jobs's metadata
        api_instance.suggest_initial_job_id_patch(job_id, suggest_initial_job_patch=suggest_initial_job_patch)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->suggest_initial_job_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique ID of the job |
 **suggest_initial_job_patch** | [**SuggestInitialJobPatch**](SuggestInitialJobPatch.md)|  | [optional]

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Job metadata updated |  -  |
**400** | Invalid job ID |  -  |
**404** | Job ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **suggest_initial_post**
> str suggest_initial_post(suggest_initial_request)

Suggest initial DoE experiments without a trained model

Suggest initial DoE experiments without a trained model Performing the suggested experiments could serve as the basis for an initial dataset to train a model with. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import default_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_initial_request import SuggestInitialRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    suggest_initial_request = SuggestInitialRequest(None) # SuggestInitialRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Suggest initial DoE experiments without a trained model
        api_response = api_instance.suggest_initial_post(suggest_initial_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->suggest_initial_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **suggest_initial_request** | [**SuggestInitialRequest**](SuggestInitialRequest.md)|  |

### Return type

**str**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The job was created, returning the job ID |  -  |
**400** | Bad request, eg. JSON malformed or with invalid parameters  |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **version_get**
> VersionResponse version_get()

Get API and application versions

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import default_api
from alchemite_apiclient.model.version_response import VersionResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get API and application versions
        api_response = api_instance.version_get()
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DefaultApi->version_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**VersionResponse**](VersionResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning API version |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

