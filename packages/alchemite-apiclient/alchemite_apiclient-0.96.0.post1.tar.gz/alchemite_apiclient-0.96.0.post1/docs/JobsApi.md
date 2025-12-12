# alchemite_apiclient.JobsApi

All URIs are relative to *https://alchemiteapi.intellegens.ai/v0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**jobs_favourites_id_delete**](JobsApi.md#jobs_favourites_id_delete) | **DELETE** /jobs/favourites/{id} | Removes job from favourites
[**jobs_favourites_id_get**](JobsApi.md#jobs_favourites_id_get) | **GET** /jobs/favourites/{id} | Gets job from favourites
[**jobs_favourites_id_patch**](JobsApi.md#jobs_favourites_id_patch) | **PATCH** /jobs/favourites/{id} | Updates job in favourites
[**jobs_favourites_post**](JobsApi.md#jobs_favourites_post) | **POST** /jobs/favourites | Creates a favourited job
[**jobs_favourites_put**](JobsApi.md#jobs_favourites_put) | **PUT** /jobs/favourites | Get all jobs marked as favourited
[**jobs_metadata_put**](JobsApi.md#jobs_metadata_put) | **PUT** /jobs/metadata | Sort and filter suggest-additional, suggest-historic &amp; optimize metadata


# **jobs_favourites_id_delete**
> jobs_favourites_id_delete(id)

Removes job from favourites

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import jobs_api
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
    api_instance = jobs_api.JobsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the favourite resource.

    # example passing only required values which don't have defaults set
    try:
        # Removes job from favourites
        api_instance.jobs_favourites_id_delete(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling JobsApi->jobs_favourites_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the favourite resource. |

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
**204** | Removed from favourites |  -  |
**400** | Invalid favourite ID |  -  |
**404** | Favourite ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_favourites_id_get**
> FavouriteJob jobs_favourites_id_get(id)

Gets job from favourites

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import jobs_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.favourite_job import FavouriteJob
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jobs_api.JobsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the favourite resource.

    # example passing only required values which don't have defaults set
    try:
        # Gets job from favourites
        api_response = api_instance.jobs_favourites_id_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling JobsApi->jobs_favourites_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the favourite resource. |

### Return type

[**FavouriteJob**](FavouriteJob.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning favourite job |  -  |
**400** | Invalid favourite ID |  -  |
**404** | Favourite ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_favourites_id_patch**
> jobs_favourites_id_patch(id)

Updates job in favourites

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import jobs_api
from alchemite_apiclient.model.favourite_patch import FavouritePatch
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
    api_instance = jobs_api.JobsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the favourite resource.
    favourite_patch = FavouritePatch(
        result_indices=[
            1,
        ],
    ) # FavouritePatch |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Updates job in favourites
        api_instance.jobs_favourites_id_patch(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling JobsApi->jobs_favourites_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Updates job in favourites
        api_instance.jobs_favourites_id_patch(id, favourite_patch=favourite_patch)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling JobsApi->jobs_favourites_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the favourite resource. |
 **favourite_patch** | [**FavouritePatch**](FavouritePatch.md)|  | [optional]

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
**204** | Favourite metadata updated |  -  |
**400** | Invalid favourite ID |  -  |
**404** | Favourite ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_favourites_post**
> str jobs_favourites_post()

Creates a favourited job

Create new reference to a favourite job and optionally favourite result within the job

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import jobs_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.favourite_job import FavouriteJob
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jobs_api.JobsApi(api_client)
    favourite_job = FavouriteJob(
        job_id="job_id_example",
        result_indices=[
            1,
        ],
    ) # FavouriteJob |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Creates a favourited job
        api_response = api_instance.jobs_favourites_post(favourite_job=favourite_job)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling JobsApi->jobs_favourites_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **favourite_job** | [**FavouriteJob**](FavouriteJob.md)|  | [optional]

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
**201** | Job favourited successfully.  Returning the favourite ID. |  -  |
**400** | Bad request, e.g. invalid job ID |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_favourites_put**
> [FavouriteJob] jobs_favourites_put()

Get all jobs marked as favourited

Returns specified jobs marked as favourited

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import jobs_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.favourite_job import FavouriteJob
from alchemite_apiclient.model.job_favourite_query import JobFavouriteQuery
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jobs_api.JobsApi(api_client)
    job_favourite_query = JobFavouriteQuery(
        filters=JobsFavouritesFilters(
            transitive_model_id="00112233-4455-6677-8899-aabbccddeeff",
        ),
    ) # JobFavouriteQuery |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all jobs marked as favourited
        api_response = api_instance.jobs_favourites_put(job_favourite_query=job_favourite_query)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling JobsApi->jobs_favourites_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_favourite_query** | [**JobFavouriteQuery**](JobFavouriteQuery.md)|  | [optional]

### Return type

[**[FavouriteJob]**](FavouriteJob.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning favourite jobs matching given query |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jobs_metadata_put**
> InlineResponse2006 jobs_metadata_put()

Sort and filter suggest-additional, suggest-historic & optimize metadata

Returns all suggest-additional, suggest-historic and optimize jobs matching the query passed. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import jobs_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.inline_response2006 import InlineResponse2006
from alchemite_apiclient.model.job_query import JobQuery
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jobs_api.JobsApi(api_client)
    offset = 0 # int | The number of items to skip before starting to collect the result set. (optional) if omitted the server will use the default value of 0
    limit = 20 # int | The number of items to return. (optional) if omitted the server will use the default value of 20
    job_query = JobQuery(
        types=[
            "optimize",
        ],
        sort=[
            JobsMetadataSort(
                name="name",
                direction="asc",
            ),
        ],
        filters=JobsMetadataFilters(
            name="name_example",
            status="pending",
            tags=[
                "tags_example",
            ],
            num_optimization_samples=NumericalFilter(None),
            num_suggestions=NumericalFilter(None),
            exploration_exploitation=NumericalFilter(None),
            project_id="00112233-4455-6677-8899-aabbccddeeff",
            transitive_model_id="00112233-4455-6677-8899-aabbccddeeff",
            exclude_model_id="00112233-4455-6677-8899-aabbccddeeff",
            model_id="00112233-4455-6677-8899-aabbccddeeff",
            search="search_example",
            job_ids=[
                "00112233-4455-6677-8899-aabbccddeeff",
            ],
        ),
    ) # JobQuery |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Sort and filter suggest-additional, suggest-historic & optimize metadata
        api_response = api_instance.jobs_metadata_put(offset=offset, limit=limit, job_query=job_query)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling JobsApi->jobs_metadata_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| The number of items to skip before starting to collect the result set. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| The number of items to return. | [optional] if omitted the server will use the default value of 20
 **job_query** | [**JobQuery**](JobQuery.md)|  | [optional]

### Return type

[**InlineResponse2006**](InlineResponse2006.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of jobs matching given query |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

