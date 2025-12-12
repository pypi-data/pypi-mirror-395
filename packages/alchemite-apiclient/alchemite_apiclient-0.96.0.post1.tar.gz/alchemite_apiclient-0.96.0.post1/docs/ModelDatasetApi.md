# alchemite_apiclient.ModelDatasetApi

All URIs are relative to *https://alchemiteapi.intellegens.ai/v0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**models_id_dataset_download_get**](ModelDatasetApi.md#models_id_dataset_download_get) | **GET** /models/{id}/dataset/download | Download a dataset
[**models_id_dataset_get**](ModelDatasetApi.md#models_id_dataset_get) | **GET** /models/{id}/dataset | Get the metadata of a model&#39;s training dataset


# **models_id_dataset_download_get**
> file_type models_id_dataset_download_get(id)

Download a dataset

Download the dataset as a CSV file.  The columns may not be in the same order as they were given at upload.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
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
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Download a dataset
        api_response = api_instance.models_id_dataset_download_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_download_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

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
**400** | Invalid model ID |  -  |
**404** | The model ID or the dataset associated with this model was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_get**
> Dataset models_id_dataset_get(id)

Get the metadata of a model's training dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
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
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get the metadata of a model's training dataset
        api_response = api_instance.models_id_dataset_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

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
**400** | Invalid model ID |  -  |
**404** | Model ID not found or no dataset is associated with this model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

