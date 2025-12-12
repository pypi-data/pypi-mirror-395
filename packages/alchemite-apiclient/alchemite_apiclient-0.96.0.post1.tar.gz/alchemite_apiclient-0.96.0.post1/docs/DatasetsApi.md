# alchemite_apiclient.DatasetsApi

All URIs are relative to *https://alchemiteapi.intellegens.ai/v0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**datasets_favourites_id_delete**](DatasetsApi.md#datasets_favourites_id_delete) | **DELETE** /datasets/favourites/{id} | Removes dataset from favourites
[**datasets_favourites_id_get**](DatasetsApi.md#datasets_favourites_id_get) | **GET** /datasets/favourites/{id} | Gets dataset from favourites
[**datasets_favourites_post**](DatasetsApi.md#datasets_favourites_post) | **POST** /datasets/favourites | Creates a favourited dataset
[**datasets_favourites_put**](DatasetsApi.md#datasets_favourites_put) | **PUT** /datasets/favourites | Get all datasets marked as favourited
[**datasets_get**](DatasetsApi.md#datasets_get) | **GET** /datasets | List the metadata for every dataset
[**datasets_id_calculated_columns_get**](DatasetsApi.md#datasets_id_calculated_columns_get) | **GET** /datasets/{id}/calculated-columns | Get all calculated column expressions for a given dataset
[**datasets_id_chunks_chunk_number_delete**](DatasetsApi.md#datasets_id_chunks_chunk_number_delete) | **DELETE** /datasets/{id}/chunks/{chunk_number} | Delete a chunk
[**datasets_id_chunks_chunk_number_get**](DatasetsApi.md#datasets_id_chunks_chunk_number_get) | **GET** /datasets/{id}/chunks/{chunk_number} | Get a chunk&#39;s metadata
[**datasets_id_chunks_chunk_number_put**](DatasetsApi.md#datasets_id_chunks_chunk_number_put) | **PUT** /datasets/{id}/chunks/{chunk_number} | Upload a chunk of a dataset&#39;s rows
[**datasets_id_chunks_delete**](DatasetsApi.md#datasets_id_chunks_delete) | **DELETE** /datasets/{id}/chunks | Restart uploading a dataset
[**datasets_id_chunks_get**](DatasetsApi.md#datasets_id_chunks_get) | **GET** /datasets/{id}/chunks | List the metadata for every chunk of a dataset
[**datasets_id_column_groups_batch_post**](DatasetsApi.md#datasets_id_column_groups_batch_post) | **POST** /datasets/{id}/column-groups/batch | Create multiple new column groups for a dataset
[**datasets_id_column_groups_column_group_id_delete**](DatasetsApi.md#datasets_id_column_groups_column_group_id_delete) | **DELETE** /datasets/{id}/column-groups/{column_group_id} | Delete a column group
[**datasets_id_column_groups_column_group_id_get**](DatasetsApi.md#datasets_id_column_groups_column_group_id_get) | **GET** /datasets/{id}/column-groups/{column_group_id} | Get specific column group for a given dataset
[**datasets_id_column_groups_column_group_id_patch**](DatasetsApi.md#datasets_id_column_groups_column_group_id_patch) | **PATCH** /datasets/{id}/column-groups/{column_group_id} | Update a column group
[**datasets_id_column_groups_get**](DatasetsApi.md#datasets_id_column_groups_get) | **GET** /datasets/{id}/column-groups | Get all column groups for a given dataset
[**datasets_id_column_groups_post**](DatasetsApi.md#datasets_id_column_groups_post) | **POST** /datasets/{id}/column-groups | Create a new column group for a dataset
[**datasets_id_delete**](DatasetsApi.md#datasets_id_delete) | **DELETE** /datasets/{id} | Delete a dataset
[**datasets_id_dimensionality_reduction_put**](DatasetsApi.md#datasets_id_dimensionality_reduction_put) | **PUT** /datasets/{id}/dimensionality-reduction | Reduce the dimensionality of a dataset
[**datasets_id_download_get**](DatasetsApi.md#datasets_id_download_get) | **GET** /datasets/{id}/download | Download a dataset
[**datasets_id_get**](DatasetsApi.md#datasets_id_get) | **GET** /datasets/{id} | Get a dataset&#39;s metadata
[**datasets_id_histogram_put**](DatasetsApi.md#datasets_id_histogram_put) | **PUT** /datasets/{id}/histogram | Returns histograms for provided columns
[**datasets_id_patch**](DatasetsApi.md#datasets_id_patch) | **PATCH** /datasets/{id} | Update a dataset&#39;s metadata
[**datasets_id_share_delete**](DatasetsApi.md#datasets_id_share_delete) | **DELETE** /datasets/{id}/share | Stop sharing dataset with group
[**datasets_id_share_get**](DatasetsApi.md#datasets_id_share_get) | **GET** /datasets/{id}/share | Get groups with which dataset is shared
[**datasets_id_share_put**](DatasetsApi.md#datasets_id_share_put) | **PUT** /datasets/{id}/share | Share dataset with a group
[**datasets_id_uploaded_post**](DatasetsApi.md#datasets_id_uploaded_post) | **POST** /datasets/{id}/uploaded | Finish uploading a dataset
[**datasets_metadata_put**](DatasetsApi.md#datasets_metadata_put) | **PUT** /datasets/metadata | List sorted and filtered dataset metadata
[**datasets_post**](DatasetsApi.md#datasets_post) | **POST** /datasets | Upload or start uploading a dataset


# **datasets_favourites_id_delete**
> datasets_favourites_id_delete(id)

Removes dataset from favourites

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the favourite resource.

    # example passing only required values which don't have defaults set
    try:
        # Removes dataset from favourites
        api_instance.datasets_favourites_id_delete(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_favourites_id_delete: %s\n" % e)
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

# **datasets_favourites_id_get**
> FavouriteDataset datasets_favourites_id_get(id)

Gets dataset from favourites

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.favourite_dataset import FavouriteDataset
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the favourite resource.

    # example passing only required values which don't have defaults set
    try:
        # Gets dataset from favourites
        api_response = api_instance.datasets_favourites_id_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_favourites_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the favourite resource. |

### Return type

[**FavouriteDataset**](FavouriteDataset.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning favourite dataset |  -  |
**400** | Invalid favourite ID |  -  |
**404** | Favourite ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_favourites_post**
> str datasets_favourites_post()

Creates a favourited dataset

Create new reference to a favourite dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.favourite_dataset import FavouriteDataset
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    favourite_dataset = FavouriteDataset(
        dataset_id="dataset_id_example",
        model_id="model_id_example",
    ) # FavouriteDataset |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Creates a favourited dataset
        api_response = api_instance.datasets_favourites_post(favourite_dataset=favourite_dataset)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_favourites_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **favourite_dataset** | [**FavouriteDataset**](FavouriteDataset.md)|  | [optional]

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
**201** | Dataset favourited successfully.  Returning the favourite ID. |  -  |
**400** | Bad request, e.g. invalid dataset ID |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_favourites_put**
> [FavouriteDataset] datasets_favourites_put()

Get all datasets marked as favourited

Returns specified datasets marked as favourited

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.dataset_favourite_query import DatasetFavouriteQuery
from alchemite_apiclient.model.favourite_dataset import FavouriteDataset
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    dataset_favourite_query = DatasetFavouriteQuery(
        filters=DatasetsFavouritesFilters(
            transitive_model_id="00112233-4455-6677-8899-aabbccddeeff",
        ),
    ) # DatasetFavouriteQuery |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all datasets marked as favourited
        api_response = api_instance.datasets_favourites_put(dataset_favourite_query=dataset_favourite_query)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_favourites_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_favourite_query** | [**DatasetFavouriteQuery**](DatasetFavouriteQuery.md)|  | [optional]

### Return type

[**[FavouriteDataset]**](FavouriteDataset.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning favourite datasets matching given query |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_get**
> [Dataset] datasets_get()

List the metadata for every dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.dataset import Dataset
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # List the metadata for every dataset
        api_response = api_instance.datasets_get()
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[Dataset]**](Dataset.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning list of datasets |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_calculated_columns_get**
> [InlineResponse2001] datasets_id_calculated_columns_get(id)

Get all calculated column expressions for a given dataset

Get all calculated column expressions for a given dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.inline_response2001 import InlineResponse2001
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # Get all calculated column expressions for a given dataset
        api_response = api_instance.datasets_id_calculated_columns_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_calculated_columns_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

### Return type

[**[InlineResponse2001]**](InlineResponse2001.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All calculated column expressions for a given dataset ID |  -  |
**400** | Bad Request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_chunks_chunk_number_delete**
> datasets_id_chunks_chunk_number_delete(id, chunk_number)

Delete a chunk

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    chunk_number = 1 # int | An integer which identifies this chunk of data

    # example passing only required values which don't have defaults set
    try:
        # Delete a chunk
        api_instance.datasets_id_chunks_chunk_number_delete(id, chunk_number)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_chunks_chunk_number_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **chunk_number** | **int**| An integer which identifies this chunk of data |

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
**204** | Chunk deleted |  -  |
**400** | Invalid dataset ID |  -  |
**404** | Dataset ID or chunk number not found or the dataset has already been uploaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_chunks_chunk_number_get**
> DatasetChunk datasets_id_chunks_chunk_number_get(id, chunk_number)

Get a chunk's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.dataset_chunk import DatasetChunk
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    chunk_number = 1 # int | An integer which identifies this chunk of data

    # example passing only required values which don't have defaults set
    try:
        # Get a chunk's metadata
        api_response = api_instance.datasets_id_chunks_chunk_number_get(id, chunk_number)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_chunks_chunk_number_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **chunk_number** | **int**| An integer which identifies this chunk of data |

### Return type

[**DatasetChunk**](DatasetChunk.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning chunk metadata |  -  |
**400** | Invalid dataset ID |  -  |
**404** | Dataset ID or chunk number not found or the dataset has already been uploaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_chunks_chunk_number_put**
> datasets_id_chunks_chunk_number_put(id, chunk_number)

Upload a chunk of a dataset's rows

Upload a subset of rows from the full dataset as a CSV file with row and column headers.  If a chunk with this chunkNumber already exists then replace it.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    chunk_number = 1 # int | An integer which identifies this chunk of data
    body = open('/path/to/file', 'rb') # file_type |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Upload a chunk of a dataset's rows
        api_instance.datasets_id_chunks_chunk_number_put(id, chunk_number)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_chunks_chunk_number_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Upload a chunk of a dataset's rows
        api_instance.datasets_id_chunks_chunk_number_put(id, chunk_number, body=body)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_chunks_chunk_number_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **chunk_number** | **int**| An integer which identifies this chunk of data |
 **body** | **file_type**|  | [optional]

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: text/csv
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Chunk uploaded |  -  |
**400** | Bad request, eg. CSV malformed or missing column headers |  -  |
**404** | Dataset ID or chunk number not found or the dataset has already been uploaded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_chunks_delete**
> datasets_id_chunks_delete(id)

Restart uploading a dataset

Delete all the chunks associated with this dataset upload

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # Restart uploading a dataset
        api_instance.datasets_id_chunks_delete(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_chunks_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

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
**204** | Deleted all chunks in this upload |  -  |
**400** | Invalid dataset ID |  -  |
**404** | Dataset ID not found or the dataset has already been uploaded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_chunks_get**
> [DatasetChunk] datasets_id_chunks_get(id)

List the metadata for every chunk of a dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.dataset_chunk import DatasetChunk
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # List the metadata for every chunk of a dataset
        api_response = api_instance.datasets_id_chunks_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_chunks_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

### Return type

[**[DatasetChunk]**](DatasetChunk.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning list of chunk metadata for this upload |  -  |
**400** | Invalid dataset ID |  -  |
**404** | Dataset ID not found or the dataset has already been uploaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_column_groups_batch_post**
> [str] datasets_id_column_groups_batch_post(id, column_group_batch_request)

Create multiple new column groups for a dataset

Create multiple new column groups for a dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.column_group_batch_request import ColumnGroupBatchRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    column_group_batch_request = ColumnGroupBatchRequest(
        column_groups=[
            ColumnGroupRequest(
                name="name_example",
                columns=[
                    "columns_example",
                ],
            ),
        ],
    ) # ColumnGroupBatchRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create multiple new column groups for a dataset
        api_response = api_instance.datasets_id_column_groups_batch_post(id, column_group_batch_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_column_groups_batch_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **column_group_batch_request** | [**ColumnGroupBatchRequest**](ColumnGroupBatchRequest.md)|  |

### Return type

**[str]**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The column groups were created |  -  |
**400** | Bad request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |
**404** | The dataset ID referenced was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_column_groups_column_group_id_delete**
> datasets_id_column_groups_column_group_id_delete(id, column_group_id)

Delete a column group

Delete a column group

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    column_group_id = "column_group_id_example" # str | Unique ID of the column group

    # example passing only required values which don't have defaults set
    try:
        # Delete a column group
        api_instance.datasets_id_column_groups_column_group_id_delete(id, column_group_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_column_groups_column_group_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **column_group_id** | **str**| Unique ID of the column group |

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
**204** | Column group successfully deleted |  -  |
**400** | Invalid column group ID |  -  |
**404** | Column group ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_column_groups_column_group_id_get**
> ColumnGroupResponse datasets_id_column_groups_column_group_id_get(id, column_group_id)

Get specific column group for a given dataset

Get specific column group for a given dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.column_group_response import ColumnGroupResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    column_group_id = "column_group_id_example" # str | Unique ID of the column group

    # example passing only required values which don't have defaults set
    try:
        # Get specific column group for a given dataset
        api_response = api_instance.datasets_id_column_groups_column_group_id_get(id, column_group_id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_column_groups_column_group_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **column_group_id** | **str**| Unique ID of the column group |

### Return type

[**ColumnGroupResponse**](ColumnGroupResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Specific column group belonging to given dataset ID |  -  |
**400** | Bad Request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_column_groups_column_group_id_patch**
> datasets_id_column_groups_column_group_id_patch(id, column_group_id)

Update a column group

Update a column group

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.column_group_patch_request import ColumnGroupPatchRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    column_group_id = "column_group_id_example" # str | Unique ID of the column group
    column_group_patch_request = ColumnGroupPatchRequest(
        name="name_example",
        columns=[
            "columns_example",
        ],
    ) # ColumnGroupPatchRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a column group
        api_instance.datasets_id_column_groups_column_group_id_patch(id, column_group_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_column_groups_column_group_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a column group
        api_instance.datasets_id_column_groups_column_group_id_patch(id, column_group_id, column_group_patch_request=column_group_patch_request)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_column_groups_column_group_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **column_group_id** | **str**| Unique ID of the column group |
 **column_group_patch_request** | [**ColumnGroupPatchRequest**](ColumnGroupPatchRequest.md)|  | [optional]

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
**204** | Column group successfully updated |  -  |
**400** | Invalid column group ID |  -  |
**404** | Column group ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_column_groups_get**
> [ColumnGroupResponse] datasets_id_column_groups_get(id)

Get all column groups for a given dataset

Get all column groups for a given dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.column_group_response import ColumnGroupResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # Get all column groups for a given dataset
        api_response = api_instance.datasets_id_column_groups_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_column_groups_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

### Return type

[**[ColumnGroupResponse]**](ColumnGroupResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All column groups belonging to given dataset ID |  -  |
**400** | Bad Request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_column_groups_post**
> str datasets_id_column_groups_post(id, column_group_request)

Create a new column group for a dataset

Create a new column group for a dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.column_group_request import ColumnGroupRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    column_group_request = ColumnGroupRequest(
        name="name_example",
        columns=[
            "columns_example",
        ],
    ) # ColumnGroupRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create a new column group for a dataset
        api_response = api_instance.datasets_id_column_groups_post(id, column_group_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_column_groups_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **column_group_request** | [**ColumnGroupRequest**](ColumnGroupRequest.md)|  |

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
**201** | The column group was created |  -  |
**400** | Bad request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |
**404** | The dataset ID referenced was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_delete**
> datasets_id_delete(id)

Delete a dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # Delete a dataset
        api_instance.datasets_id_delete(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

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
**204** | Dataset deleted |  -  |
**400** | Invalid dataset ID |  -  |
**404** | Dataset ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_dimensionality_reduction_put**
> DimensionalityReductionResponse datasets_id_dimensionality_reduction_put(id)

Reduce the dimensionality of a dataset

Reduce the dimensionality of a dataset down to a specified number of dimensions through PCA or UMAP. The dataset being reduced must have at least 5 rows and at most 50,000 rows. There must also be fewer than 10,000 columns and fewer than 5,000,000 cells overall. Vector columns are not supported and will be ignored during reduction.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.dimensionality_reduction_request import DimensionalityReductionRequest
from alchemite_apiclient.model.dimensionality_reduction_response import DimensionalityReductionResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    dimensionality_reduction_request = DimensionalityReductionRequest(
        reduction_data=None,
        reduction_method=None,
    ) # DimensionalityReductionRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Reduce the dimensionality of a dataset
        api_response = api_instance.datasets_id_dimensionality_reduction_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_dimensionality_reduction_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Reduce the dimensionality of a dataset
        api_response = api_instance.datasets_id_dimensionality_reduction_put(id, dimensionality_reduction_request=dimensionality_reduction_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_dimensionality_reduction_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **dimensionality_reduction_request** | [**DimensionalityReductionRequest**](DimensionalityReductionRequest.md)|  | [optional]

### Return type

[**DimensionalityReductionResponse**](DimensionalityReductionResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning plotting points for dimension-reduced dataset. |  -  |
**202** | Auto UMAP is being optimized. Try again later |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_download_get**
> file_type datasets_id_download_get(id)

Download a dataset

Download the dataset as a CSV file. The columns may not be in the same  order as they were given at upload. If the dataset uses extensions  then this csv will have all columns that appeared during the extension  (eg if a column was removed and another added, then the CSV will  contain both). 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # Download a dataset
        api_response = api_instance.datasets_id_download_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_download_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

### Return type

**file_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning dataset |  -  |
**400** | Invalid dataset ID |  -  |
**404** | Dataset ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_get**
> Dataset datasets_id_get(id)

Get a dataset's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.dataset import Dataset
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # Get a dataset's metadata
        api_response = api_instance.datasets_id_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

### Return type

[**Dataset**](Dataset.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning dataset metadata |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_histogram_put**
> HistogramResponse datasets_id_histogram_put(id)

Returns histograms for provided columns

Returns histograms for provided columns

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.histogram_request import HistogramRequest
from alchemite_apiclient.model.histogram_response import HistogramResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    histogram_request = HistogramRequest(
        min_bins=1,
        max_bins=30,
        columns=[
            "columns_example",
        ],
    ) # HistogramRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Returns histograms for provided columns
        api_response = api_instance.datasets_id_histogram_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_histogram_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Returns histograms for provided columns
        api_response = api_instance.datasets_id_histogram_put(id, histogram_request=histogram_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_histogram_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **histogram_request** | [**HistogramRequest**](HistogramRequest.md)|  | [optional]

### Return type

[**HistogramResponse**](HistogramResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The data required to generate histograms for provided columns.  If the column is empty, no histogram data will be returned for the column entry is the response.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_patch**
> datasets_id_patch(id)

Update a dataset's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.dataset_patch import DatasetPatch
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    dataset_patch = DatasetPatch(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
    ) # DatasetPatch |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a dataset's metadata
        api_instance.datasets_id_patch(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a dataset's metadata
        api_instance.datasets_id_patch(id, dataset_patch=dataset_patch)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **dataset_patch** | [**DatasetPatch**](DatasetPatch.md)|  | [optional]

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
**204** | Dataset metadata updated |  -  |
**400** | Invalid dataset ID |  -  |
**404** | Dataset ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_share_delete**
> datasets_id_share_delete(id, share_group)

Stop sharing dataset with group

Delete group from dataset's shared groups

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.share_group import ShareGroup
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    share_group = ShareGroup(
        group="/Organization Name/Group Name",
    ) # ShareGroup | 

    # example passing only required values which don't have defaults set
    try:
        # Stop sharing dataset with group
        api_instance.datasets_id_share_delete(id, share_group)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_share_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **share_group** | [**ShareGroup**](ShareGroup.md)|  |

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
**204** | Group deleted from dataset |  -  |
**404** | Dataset ID or group not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_share_get**
> [str] datasets_id_share_get(id)

Get groups with which dataset is shared

Get dataset's shared groups

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # Get groups with which dataset is shared
        api_response = api_instance.datasets_id_share_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_share_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

### Return type

**[str]**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Dataset&#39;s shared groups |  -  |
**404** | Dataset ID or group not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_share_put**
> datasets_id_share_put(id, share_group)

Share dataset with a group

Add a group to a dataset which allows all users belonging to that group to have access to the dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.share_group import ShareGroup
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.
    share_group = ShareGroup(
        group="/Organization Name/Group Name",
    ) # ShareGroup | 

    # example passing only required values which don't have defaults set
    try:
        # Share dataset with a group
        api_instance.datasets_id_share_put(id, share_group)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_share_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |
 **share_group** | [**ShareGroup**](ShareGroup.md)|  |

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
**204** | Dataset is shared with given group. |  -  |
**404** | Dataset ID not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_id_uploaded_post**
> datasets_id_uploaded_post(id)

Finish uploading a dataset

Collate all the uploaded chunks into the final dataset.  This will set the status of the dataset to 'uploaded'.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
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
    api_instance = datasets_api.DatasetsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the dataset.

    # example passing only required values which don't have defaults set
    try:
        # Finish uploading a dataset
        api_instance.datasets_id_uploaded_post(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_id_uploaded_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the dataset. |

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
**200** | Dataset successfully collated |  -  |
**400** | Invalid dataset ID |  -  |
**404** | Dataset ID not found or the dataset has already been uploaded. |  -  |
**409** | The values in one or more chunks conflict or the dataset dimensions do not match those specified at dataset creation. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_metadata_put**
> InlineResponse200 datasets_metadata_put()

List sorted and filtered dataset metadata

Returns all datasets matching the query passed. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.dataset_query import DatasetQuery
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.inline_response200 import InlineResponse200
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    offset = 0 # int | The number of items to skip before starting to collect the result set. (optional) if omitted the server will use the default value of 0
    limit = 20 # int | The number of items to return. (optional) if omitted the server will use the default value of 20
    dataset_query = DatasetQuery(
        sort=[
            DatasetsMetadataSort(
                name="name",
                direction="asc",
            ),
        ],
        filters=DatasetsMetadataFilters(
            name="name_example",
            status="processing",
            tags=[
                "tags_example",
            ],
            row_count=None,
            column_count=None,
            groups=[
                "groups_example",
            ],
            exact_groups=[
                "exact_groups_example",
            ],
            search="search_example",
            dataset_ids=[
                "00112233-4455-6677-8899-aabbccddeeff",
            ],
        ),
    ) # DatasetQuery |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List sorted and filtered dataset metadata
        api_response = api_instance.datasets_metadata_put(offset=offset, limit=limit, dataset_query=dataset_query)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_metadata_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| The number of items to skip before starting to collect the result set. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| The number of items to return. | [optional] if omitted the server will use the default value of 20
 **dataset_query** | [**DatasetQuery**](DatasetQuery.md)|  | [optional]

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of datasets matching given query |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datasets_post**
> str datasets_post()

Upload or start uploading a dataset

Create a dataset for a model to train on and return the dataset ID. If the 'data' parameter is not given in the JSON request body then it will be assumed that the data is to be uploaded later in chunks. In this case the parameter 'status' in the dataset metadata will be set to 'uploading'. If 'data' is provided, the 'status' will be set to 'pending' while the dataset is ingested into the datastore. When finished, the final 'status' the dataset enters will be 'uploaded'. Datasets with more than 10,000 columns are not currently supported and cannot be uploaded. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import datasets_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.dataset import Dataset
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)
    dataset = Dataset(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
        revises_id="00112233-4455-6677-8899-aabbccddeeff",
        row_count=1,
        column_headers=["C","Ni","Si","Young's modulus","Resistivity"],
        categorical_columns=[
            CategoricalColumn(
                name="name_example",
                values=None,
            ),
        ],
        ordinal_columns=[
            OrdinalColumn(
                name="name_example",
                values=[
                    3.14,
                ],
            ),
        ],
        descriptor_columns=[1,1,1,0,0],
        auto_detect_complete_columns=False,
        complete_columns=[1,0,1,0,0],
        calculated_columns=[
            DatasetCalculatedColumns(
                name="name_example",
                expression=CalColExpression(),
            ),
        ],
        measurement_groups=[1,2,3,1,4],
        data=''',C,Ni,Si,Young's modulus,Resistivity
Carbon steel 1,0.105,0,0,209.9,14.4
Carbon steel 2,0.2,,0,,17
Low alloy steel,,0,0.25,206.4,22.40
''',
        vector_pairs=[["time","temperature"],["distance","strength"]],
        extensions=[
            None,
        ],
    ) # Dataset |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Upload or start uploading a dataset
        api_response = api_instance.datasets_post(dataset=dataset)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling DatasetsApi->datasets_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset** | [**Dataset**](Dataset.md)|  | [optional]

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
**201** | Dataset created.  Returning the dataset ID. |  -  |
**400** | Bad request, eg. CSV malformed or JSON with invalid parameters. |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

