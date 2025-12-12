# alchemite_apiclient.ModelsApi

All URIs are relative to *https://alchemiteapi.intellegens.ai/v0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**models_get**](ModelsApi.md#models_get) | **GET** /models | List the metadata for every model
[**models_id_additive_sensitivity_put**](ModelsApi.md#models_id_additive_sensitivity_put) | **PUT** /models/{id}/additive-sensitivity | Get model additive sensitivity at a point
[**models_id_analyse_validate_put**](ModelsApi.md#models_id_analyse_validate_put) | **PUT** /models/{id}/analyse-validate | Analyse predictions against given data
[**models_id_copy_post**](ModelsApi.md#models_id_copy_post) | **POST** /models/{id}/copy | Copy a model
[**models_id_delete**](ModelsApi.md#models_id_delete) | **DELETE** /models/{id} | Delete a model
[**models_id_export_get**](ModelsApi.md#models_id_export_get) | **GET** /models/{id}/export | Export a model
[**models_id_get**](ModelsApi.md#models_id_get) | **GET** /models/{id} | Get a model&#39;s metadata
[**models_id_importance_put**](ModelsApi.md#models_id_importance_put) | **PUT** /models/{id}/importance | Importance of each column to each other column
[**models_id_impute_put**](ModelsApi.md#models_id_impute_put) | **PUT** /models/{id}/impute | Impute missing data
[**models_id_influence_put**](ModelsApi.md#models_id_influence_put) | **PUT** /models/{id}/influence | Request the influence model inputs have on a given output
[**models_id_load_post**](ModelsApi.md#models_id_load_post) | **POST** /models/{id}/load | Load model into memory
[**models_id_optimize_get**](ModelsApi.md#models_id_optimize_get) | **GET** /models/{id}/optimize | Get all optimize jobs for given model ID
[**models_id_optimize_job_id_delete**](ModelsApi.md#models_id_optimize_job_id_delete) | **DELETE** /models/{id}/optimize/{job_id} | Delete optimize job
[**models_id_optimize_job_id_get**](ModelsApi.md#models_id_optimize_job_id_get) | **GET** /models/{id}/optimize/{job_id} | Get optimize job data
[**models_id_optimize_job_id_patch**](ModelsApi.md#models_id_optimize_job_id_patch) | **PATCH** /models/{id}/optimize/{job_id} | Update an optimize jobs&#39;s metadata
[**models_id_optimize_post**](ModelsApi.md#models_id_optimize_post) | **POST** /models/{id}/optimize | Optimize for specified targets using set of constraints
[**models_id_outliers_put**](ModelsApi.md#models_id_outliers_put) | **PUT** /models/{id}/outliers | Find the outlying values in a dataset
[**models_id_output_tolerance_put**](ModelsApi.md#models_id_output_tolerance_put) | **PUT** /models/{id}/output-tolerance | Get tolerance of predicted outputs from variations in inputs
[**models_id_output_tolerance_univariate_put**](ModelsApi.md#models_id_output_tolerance_univariate_put) | **PUT** /models/{id}/output-tolerance-univariate | Get the univariate tolerances of predicted outputs from variations in inputs
[**models_id_patch**](ModelsApi.md#models_id_patch) | **PATCH** /models/{id} | Update a model&#39;s metadata
[**models_id_predict_interaction_job_id_get**](ModelsApi.md#models_id_predict_interaction_job_id_get) | **GET** /models/{id}/predict/interaction/{job_id} | Get the result of an interaction request from a given job ID
[**models_id_predict_interaction_post**](ModelsApi.md#models_id_predict_interaction_post) | **POST** /models/{id}/predict/interaction | Calculate the interaction between two columns with respect to an output column
[**models_id_predict_put**](ModelsApi.md#models_id_predict_put) | **PUT** /models/{id}/predict | Predict given and missing data
[**models_id_predict_trendline_put**](ModelsApi.md#models_id_predict_trendline_put) | **PUT** /models/{id}/predict/trendline | Calculate the trendline between two columns
[**models_id_report_get**](ModelsApi.md#models_id_report_get) | **GET** /models/{id}/report | Get a PDF report for the model
[**models_id_sensitivity_put**](ModelsApi.md#models_id_sensitivity_put) | **PUT** /models/{id}/sensitivity | Get model sensitivity at a point
[**models_id_share_delete**](ModelsApi.md#models_id_share_delete) | **DELETE** /models/{id}/share | Stop sharing model with group
[**models_id_share_get**](ModelsApi.md#models_id_share_get) | **GET** /models/{id}/share | Get groups with which model is shared
[**models_id_share_put**](ModelsApi.md#models_id_share_put) | **PUT** /models/{id}/share | Share model with a group
[**models_id_suggest_additional_get**](ModelsApi.md#models_id_suggest_additional_get) | **GET** /models/{id}/suggest-additional | Get all suggest-additional jobs for a model
[**models_id_suggest_additional_job_id_delete**](ModelsApi.md#models_id_suggest_additional_job_id_delete) | **DELETE** /models/{id}/suggest-additional/{job_id} | Delete suggest-additional job
[**models_id_suggest_additional_job_id_get**](ModelsApi.md#models_id_suggest_additional_job_id_get) | **GET** /models/{id}/suggest-additional/{job_id} | Get suggest-additional job data
[**models_id_suggest_additional_job_id_patch**](ModelsApi.md#models_id_suggest_additional_job_id_patch) | **PATCH** /models/{id}/suggest-additional/{job_id} | Update a suggest additional jobs&#39;s metadata
[**models_id_suggest_additional_post**](ModelsApi.md#models_id_suggest_additional_post) | **POST** /models/{id}/suggest-additional | Suggest additional measurements
[**models_id_suggest_historic_get**](ModelsApi.md#models_id_suggest_historic_get) | **GET** /models/{id}/suggest-historic | Get all suggest-historic jobs for a model
[**models_id_suggest_historic_job_id_delete**](ModelsApi.md#models_id_suggest_historic_job_id_delete) | **DELETE** /models/{id}/suggest-historic/{job_id} | Delete suggest-historic job
[**models_id_suggest_historic_job_id_get**](ModelsApi.md#models_id_suggest_historic_job_id_get) | **GET** /models/{id}/suggest-historic/{job_id} | Get suggest-historic job data
[**models_id_suggest_historic_job_id_patch**](ModelsApi.md#models_id_suggest_historic_job_id_patch) | **PATCH** /models/{id}/suggest-historic/{job_id} | Update a suggest historic jobs&#39;s metadata
[**models_id_suggest_historic_post**](ModelsApi.md#models_id_suggest_historic_post) | **POST** /models/{id}/suggest-historic | Suggest historic measurements
[**models_id_suggest_missing_put**](ModelsApi.md#models_id_suggest_missing_put) | **PUT** /models/{id}/suggest-missing | Suggest which missing values to measure next
[**models_id_synergy_put**](ModelsApi.md#models_id_synergy_put) | **PUT** /models/{id}/synergy | Request the synergy - the input-input interaction, for a given output
[**models_id_train_put**](ModelsApi.md#models_id_train_put) | **PUT** /models/{id}/train | Train a model
[**models_id_training_dataset_outliers_put**](ModelsApi.md#models_id_training_dataset_outliers_put) | **PUT** /models/{id}/training-dataset-outliers | Find the outlying values in the model&#39;s training dataset
[**models_id_unload_put**](ModelsApi.md#models_id_unload_put) | **PUT** /models/{id}/unload | Unload model from memory
[**models_id_validate_put**](ModelsApi.md#models_id_validate_put) | **PUT** /models/{id}/validate | Validate given data
[**models_id_validation_predictions_get**](ModelsApi.md#models_id_validation_predictions_get) | **GET** /models/{id}/validation-predictions | Get the predictions used to calculate the model&#39;s quality during training
[**models_id_validation_predictions_put**](ModelsApi.md#models_id_validation_predictions_put) | **PUT** /models/{id}/validation-predictions | Get the predictions used to calculate the model&#39;s quality during training
[**models_id_validation_splits_get**](ModelsApi.md#models_id_validation_splits_get) | **GET** /models/{id}/validation-splits | Get a model&#39;s validation splits.
[**models_import_post**](ModelsApi.md#models_import_post) | **POST** /models/import | Import a model
[**models_metadata_put**](ModelsApi.md#models_metadata_put) | **PUT** /models/metadata | List sorted and filtered model metadata
[**models_post**](ModelsApi.md#models_post) | **POST** /models | Define a model to be trained


# **models_get**
> [Model] models_get()

List the metadata for every model

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.model import Model
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # List the metadata for every model
        api_response = api_instance.models_get()
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[Model]**](Model.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning list of models |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_additive_sensitivity_put**
> file_type models_id_additive_sensitivity_put(id)

Get model additive sensitivity at a point

Generate an additive sensitivity analysis around a point. This reports the additive contributions of input columns to each output column around a datapoint, similar to coefficients in a local linear regression.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.additive_sensitivity_request import AdditiveSensitivityRequest
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    additive_sensitivity_request = AdditiveSensitivityRequest(
        data_point=[
            ColumnValueNullable(
                name="name_example",
                value=None,
            ),
        ],
        output_columns=["x1","x2","y1"],
        input_columns=["x1","x2","y1","y2"],
        origin=[
            ModelsIdAdditiveSensitivityOrigin(
                name="name_example",
                value=None,
            ),
        ],
    ) # AdditiveSensitivityRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get model additive sensitivity at a point
        api_response = api_instance.models_id_additive_sensitivity_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_additive_sensitivity_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get model additive sensitivity at a point
        api_response = api_instance.models_id_additive_sensitivity_put(id, additive_sensitivity_request=additive_sensitivity_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_additive_sensitivity_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **additive_sensitivity_request** | [**AdditiveSensitivityRequest**](AdditiveSensitivityRequest.md)|  | [optional]

### Return type

**file_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning additive sensitivity matrix |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_analyse_validate_put**
> AnalyseValidateResponse models_id_analyse_validate_put(id)

Analyse predictions against given data

Analyse the model's predictions against a given dataset and, optionally, return the predictions themselves

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.analyse_validate_response import AnalyseValidateResponse
from alchemite_apiclient.model.analyse_validate_request import AnalyseValidateRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    analyse_validate_request = AnalyseValidateRequest() # AnalyseValidateRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Analyse predictions against given data
        api_response = api_instance.models_id_analyse_validate_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_analyse_validate_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Analyse predictions against given data
        api_response = api_instance.models_id_analyse_validate_put(id, analyse_validate_request=analyse_validate_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_analyse_validate_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **analyse_validate_request** | [**AnalyseValidateRequest**](AnalyseValidateRequest.md)|  | [optional]

### Return type

[**AnalyseValidateResponse**](AnalyseValidateResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning predictions |  -  |
**400** | Bad request, eg. CSV malformed or missing column headers |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_copy_post**
> str models_id_copy_post(id)

Copy a model

Create a copy of the model which is identical except for having a new model ID.  The model ID of the copy will be returned in the response.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Copy a model
        api_response = api_instance.models_id_copy_post(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_copy_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

**str**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | A copy of the model was created.  Returning the model ID of the copy. |  -  |
**400** | Invalid model ID |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_delete**
> models_id_delete(id)

Delete a model

Delete the model and stop any in progress training

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Delete a model
        api_instance.models_id_delete(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

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
**204** | Model successfully deleted |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_export_get**
> file_type models_id_export_get(id)

Export a model

Download the model data and metadata as a zip file  > Not enabled by default. Please contact Intellegens if required 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Export a model
        api_response = api_instance.models_id_export_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_export_get: %s\n" % e)
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
 - **Accept**: application/zip, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning model data as a .zip file. |  -  |
**400** | Bad request, eg. invalid model ID |  -  |
**404** | The model ID was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_get**
> Model models_id_get(id)

Get a model's metadata

Get the metadata for the model.  This includes, for example, ID, name, status and percentage training completion.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.model import Model
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get a model's metadata
        api_response = api_instance.models_id_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

[**Model**](Model.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning model metadata |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_importance_put**
> file_type models_id_importance_put(id)

Importance of each column to each other column

Generate a global analysis of how important each input is for predicting each output.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.importance_request import ImportanceRequest
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    importance_request = ImportanceRequest(
        output_columns=["w","y","z"],
        input_columns=["w","x","y","z"],
        use_only_descriptors=False,
    ) # ImportanceRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Importance of each column to each other column
        api_response = api_instance.models_id_importance_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_importance_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Importance of each column to each other column
        api_response = api_instance.models_id_importance_put(id, importance_request=importance_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_importance_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **importance_request** | [**ImportanceRequest**](ImportanceRequest.md)|  | [optional]

### Return type

**file_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning analysis |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_impute_put**
> bool, date, datetime, dict, float, int, list, str, none_type models_id_impute_put(id)

Impute missing data

Given an incomplete dataset return the predictions for the missing values together with the corresponding uncertainties or full probability distribution for each prediction.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.impute_request import ImputeRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    impute_request = ImputeRequest(
        return_probability_distribution=False,
        dataset_id="dataset_id_example",
        return_row_headers=False,
        return_column_headers=False,
        data='''x,y,x+y,x-y
1,0.2,,0.8
0.5,0.3,,
''',
    ) # ImputeRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Impute missing data
        api_response = api_instance.models_id_impute_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_impute_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Impute missing data
        api_response = api_instance.models_id_impute_put(id, impute_request=impute_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_impute_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **impute_request** | [**ImputeRequest**](ImputeRequest.md)|  | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning predictions |  -  |
**400** | Bad request, eg. CSV malformed or missing column headers |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_influence_put**
> InlineResponse2003 models_id_influence_put(id)

Request the influence model inputs have on a given output

Request the influence model inputs have on a given output.  These influence values are calculated using the rows of the training dataset,  representing how much of the output each input is responsible for. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.inline_object import InlineObject
from alchemite_apiclient.model.inline_response2003 import InlineResponse2003
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    inline_object = InlineObject(
        output_column="output_column_example",
    ) # InlineObject |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Request the influence model inputs have on a given output
        api_response = api_instance.models_id_influence_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_influence_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Request the influence model inputs have on a given output
        api_response = api_instance.models_id_influence_put(id, inline_object=inline_object)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_influence_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **inline_object** | [**InlineObject**](InlineObject.md)|  | [optional]

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The influence for the requested column |  -  |
**202** | Influence is being generated |  -  |
**400** | Bad Request, e.g. Invalid model ID or outputColumn |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_load_post**
> models_id_load_post(id)

Load model into memory

Load the model into memory so that future \"/models/{id}/impute\" requests will be faster.  The \"loaded\" property in the model metadata shows whether the model is currently loaded or not.  The model will be removed from memory if \"timeout\" seconds have passed since the model was loaded into memory and the model has not been used for \"timeout\" seconds.  Calling the \"/models/{id}/load\" endpoint for an already loaded model will reset the timeout.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.load_request import LoadRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    load_request = LoadRequest(
        timeout=60,
    ) # LoadRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Load model into memory
        api_instance.models_id_load_post(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_load_post: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Load model into memory
        api_instance.models_id_load_post(id, load_request=load_request)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_load_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **load_request** | [**LoadRequest**](LoadRequest.md)|  | [optional]

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
**200** | Model is loaded. |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_optimize_get**
> GetAllOptJobs models_id_optimize_get(id)

Get all optimize jobs for given model ID

Get all optimize jobs for given model ID

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.get_all_opt_jobs import GetAllOptJobs
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    n_samples = 1 # int | Set number of samples to return (i.e. top N samples). Only applies when the optimization status is `done` and the result is returned. Defaults to 1  (optional) if omitted the server will use the default value of 1

    # example passing only required values which don't have defaults set
    try:
        # Get all optimize jobs for given model ID
        api_response = api_instance.models_id_optimize_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_optimize_get: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all optimize jobs for given model ID
        api_response = api_instance.models_id_optimize_get(id, n_samples=n_samples)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_optimize_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **n_samples** | **int**| Set number of samples to return (i.e. top N samples). Only applies when the optimization status is &#x60;done&#x60; and the result is returned. Defaults to 1  | [optional] if omitted the server will use the default value of 1

### Return type

[**GetAllOptJobs**](GetAllOptJobs.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All optimize jobs for given model ID |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | The model ID or the dataset used to train the model was not found or the model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_optimize_job_id_delete**
> models_id_optimize_job_id_delete(id, job_id)

Delete optimize job

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job

    # example passing only required values which don't have defaults set
    try:
        # Delete optimize job
        api_instance.models_id_optimize_job_id_delete(id, job_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_optimize_job_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
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
**204** | Optimize job deleted |  -  |
**400** | Invalid optimize job ID |  -  |
**404** | Optimize job ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_optimize_job_id_get**
> OptimizationJob models_id_optimize_job_id_get(id, job_id)

Get optimize job data

Request information about an optimize job. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.optimization_job import OptimizationJob
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job
    n_samples = 1 # int | Set number of samples to return (i.e. top N samples). Only applies when the optimization status is `done` and the result is returned. Defaults to 1  (optional) if omitted the server will use the default value of 1

    # example passing only required values which don't have defaults set
    try:
        # Get optimize job data
        api_response = api_instance.models_id_optimize_job_id_get(id, job_id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_optimize_job_id_get: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get optimize job data
        api_response = api_instance.models_id_optimize_job_id_get(id, job_id, n_samples=n_samples)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_optimize_job_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **job_id** | **str**| Unique ID of the job |
 **n_samples** | **int**| Set number of samples to return (i.e. top N samples). Only applies when the optimization status is &#x60;done&#x60; and the result is returned. Defaults to 1  | [optional] if omitted the server will use the default value of 1

### Return type

[**OptimizationJob**](OptimizationJob.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning optimize job data |  -  |
**400** | Bad request, eg. invalid model ID or optimize Job ID |  -  |
**404** | The model ID or optimize job ID was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_optimize_job_id_patch**
> models_id_optimize_job_id_patch(id, job_id)

Update an optimize jobs's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.job_patch import JobPatch
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job
    job_patch = JobPatch(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
    ) # JobPatch |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update an optimize jobs's metadata
        api_instance.models_id_optimize_job_id_patch(id, job_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_optimize_job_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update an optimize jobs's metadata
        api_instance.models_id_optimize_job_id_patch(id, job_id, job_patch=job_patch)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_optimize_job_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **job_id** | **str**| Unique ID of the job |
 **job_patch** | [**JobPatch**](JobPatch.md)|  | [optional]

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

# **models_id_optimize_post**
> str models_id_optimize_post(id, optimize_request)

Optimize for specified targets using set of constraints

Specify sample definition and target function to optimize for.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.optimize_request import OptimizeRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    optimize_request = OptimizeRequest(None) # OptimizeRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Optimize for specified targets using set of constraints
        api_response = api_instance.models_id_optimize_post(id, optimize_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_optimize_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **optimize_request** | [**OptimizeRequest**](OptimizeRequest.md)|  |

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
**201** | The optimize job was created.  Return the optimize job ID. |  -  |
**400** | Bad request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |
**404** | The model ID or the dataset used to train the model was not found or the model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_outliers_put**
> bool, date, datetime, dict, float, int, list, str, none_type models_id_outliers_put(id)

Find the outlying values in a dataset

Compares a given array of data (complete or incomplete) with the corresponding predicted values.  If a given value lies outside of the error bounds of the corresponding predicted value then it is deemed an outlier.  Returns the given value of all outliers along with the corresponding predicted values, the number of standard deviations between the given and predicted values and the row and column indices of the outlier.  If the outlier is part of a vector then the \"Component Index\" indicates which component of the vector is an outlier.  If the outlier is not a vector then the \"Component Index\" will be 1.  > If the outliers in the model's own training dataset are required then consider using `/models/{id}/training-dataset-outliers` instead 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.outliers_request import OutliersRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    outliers_request = OutliersRequest(
        dataset_id="dataset_id_example",
        data='''x,x^2,x^3,x^4
3,9,72,81
2,4,8,16
''',
        outlier_tolerance=1.0,
        return_row_headers=False,
    ) # OutliersRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Find the outlying values in a dataset
        api_response = api_instance.models_id_outliers_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_outliers_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Find the outlying values in a dataset
        api_response = api_instance.models_id_outliers_put(id, outliers_request=outliers_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_outliers_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **outliers_request** | [**OutliersRequest**](OutliersRequest.md)|  | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning comparison between predicted and measured values |  -  |
**400** | Bad request, eg. CSV malformed or missing column headers |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_output_tolerance_put**
> OutputToleranceResponse models_id_output_tolerance_put(id)

Get tolerance of predicted outputs from variations in inputs

Explore over an input space and make imputations based on sampled values from provided input ranges. These resultant outputs can then be evaluated to judge how much the output changes in relation to these variable inputs. The tolerance of the output can then be evaluated based on how sensitive it is to changing inputs.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.output_tolerance_request import OutputToleranceRequest
from alchemite_apiclient.model.output_tolerance_response import OutputToleranceResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    output_tolerance_request = OutputToleranceRequest(
        sample_definition=OTSampleDefinition(
            key=None,
        ),
        set_inputs=OTSetInputs(
            key=None,
        ),
        num_samples=500,
    ) # OutputToleranceRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get tolerance of predicted outputs from variations in inputs
        api_response = api_instance.models_id_output_tolerance_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_output_tolerance_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get tolerance of predicted outputs from variations in inputs
        api_response = api_instance.models_id_output_tolerance_put(id, output_tolerance_request=output_tolerance_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_output_tolerance_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **output_tolerance_request** | [**OutputToleranceRequest**](OutputToleranceRequest.md)|  | [optional]

### Return type

[**OutputToleranceResponse**](OutputToleranceResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning output tolerance results from exploring the sample space. |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_output_tolerance_univariate_put**
> OutputToleranceUnivariateResponse models_id_output_tolerance_univariate_put(id)

Get the univariate tolerances of predicted outputs from variations in inputs

For each specified column, explore over a single input space and make imputations based on sampled values from provided input ranges. These resultant outputs can then be evaluated to judge how much the output changes in relation to these variable inputs. The tolerance of each output can then be evaluated based on how sensitive they are to changing inputs.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.output_tolerance_request import OutputToleranceRequest
from alchemite_apiclient.model.output_tolerance_univariate_response import OutputToleranceUnivariateResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    output_tolerance_request = OutputToleranceRequest(
        sample_definition=OTSampleDefinition(
            key=None,
        ),
        set_inputs=OTSetInputs(
            key=None,
        ),
        num_samples=500,
    ) # OutputToleranceRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get the univariate tolerances of predicted outputs from variations in inputs
        api_response = api_instance.models_id_output_tolerance_univariate_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_output_tolerance_univariate_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get the univariate tolerances of predicted outputs from variations in inputs
        api_response = api_instance.models_id_output_tolerance_univariate_put(id, output_tolerance_request=output_tolerance_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_output_tolerance_univariate_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **output_tolerance_request** | [**OutputToleranceRequest**](OutputToleranceRequest.md)|  | [optional]

### Return type

[**OutputToleranceUnivariateResponse**](OutputToleranceUnivariateResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning univariate output tolerance results from exploring the sample spaces. |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_patch**
> models_id_patch(id)

Update a model's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.model_patch import ModelPatch
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    model_patch = ModelPatch(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
        project_id="00112233-4455-6677-8899-aabbccddeeff",
    ) # ModelPatch |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a model's metadata
        api_instance.models_id_patch(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a model's metadata
        api_instance.models_id_patch(id, model_patch=model_patch)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **model_patch** | [**ModelPatch**](ModelPatch.md)|  | [optional]

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
**204** | Model successfully updated |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_predict_interaction_job_id_get**
> bool, date, datetime, dict, float, int, list, str, none_type models_id_predict_interaction_job_id_get(id, job_id)

Get the result of an interaction request from a given job ID

Gets the result of an interaction request from a given job ID, where the request was made using post /models/{id}/prediction/interaction. If the job was successful, the interaction between two columns and a target output column will be returned 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.interaction_plot_data import InteractionPlotData
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job

    # example passing only required values which don't have defaults set
    try:
        # Get the result of an interaction request from a given job ID
        api_response = api_instance.models_id_predict_interaction_job_id_get(id, job_id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_predict_interaction_job_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **job_id** | **str**| Unique ID of the job |

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Will always return an object with the status key. If status is done, will also return the required data to plot interactions between columns  |  -  |
**400** | Bad request, e.g. invalid model ID or job ID |  -  |
**404** | The model ID or job ID was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_predict_interaction_post**
> str models_id_predict_interaction_post(id)

Calculate the interaction between two columns with respect to an output column

Given two columns and an output column from the model, an interaction for a specified amount of bins will be calculated When a calculated or extension column is used as input(s), the underlying calculations do not alter the source columns  and may not fully reflect the actual trend 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.predict_interaction_request import PredictInteractionRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    predict_interaction_request = PredictInteractionRequest(
        input_columns=[
            "input_columns_example",
        ],
        output_column="output_column_example",
        bin_count=10,
    ) # PredictInteractionRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Calculate the interaction between two columns with respect to an output column
        api_response = api_instance.models_id_predict_interaction_post(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_predict_interaction_post: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Calculate the interaction between two columns with respect to an output column
        api_response = api_instance.models_id_predict_interaction_post(id, predict_interaction_request=predict_interaction_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_predict_interaction_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **predict_interaction_request** | [**PredictInteractionRequest**](PredictInteractionRequest.md)|  | [optional]

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
**201** | Returns the ID of the interaction job |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_predict_put**
> bool, date, datetime, dict, float, int, list, str, none_type models_id_predict_put(id)

Predict given and missing data

Given a dataset return the predictions for all given and missing values in the dataset with the uncertainties or full probability distribution for each prediction.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.predict_request import PredictRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    predict_request = PredictRequest(
        return_probability_distribution=False,
        dataset_id="dataset_id_example",
        return_row_headers=False,
        return_column_headers=False,
        data='''x,y,x+y,x-y
1,0.2,,0.8
0.5,0.3,,
''',
    ) # PredictRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Predict given and missing data
        api_response = api_instance.models_id_predict_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_predict_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Predict given and missing data
        api_response = api_instance.models_id_predict_put(id, predict_request=predict_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_predict_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **predict_request** | [**PredictRequest**](PredictRequest.md)|  | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning predictions |  -  |
**400** | Bad request, eg. CSV malformed or missing column headers |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_predict_trendline_put**
> InlineResponse2005 models_id_predict_trendline_put(id)

Calculate the trendline between two columns

Given an input column and an output column from the model, a trendline of a specified amount of bins will be calculated. When a calculated or extension column is used as input, the underlying calculations do not alter the source columns  and may not fully reflect the actual trend 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.inline_response2005 import InlineResponse2005
from alchemite_apiclient.model.predict_trendline_request import PredictTrendlineRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    predict_trendline_request = PredictTrendlineRequest(
        input_column="input_column_example",
        output_column="output_column_example",
        bin_count=10,
    ) # PredictTrendlineRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Calculate the trendline between two columns
        api_response = api_instance.models_id_predict_trendline_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_predict_trendline_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Calculate the trendline between two columns
        api_response = api_instance.models_id_predict_trendline_put(id, predict_trendline_request=predict_trendline_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_predict_trendline_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **predict_trendline_request** | [**PredictTrendlineRequest**](PredictTrendlineRequest.md)|  | [optional]

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | An array of points containing the x and y axis values to plot the trendline, as well as the calculated uncertainties |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_report_get**
> file_type models_id_report_get(id)

Get a PDF report for the model

Generate a PDF report for the chosen model. This report will contain statistical information on the training dataset, notable features of the model, and multiple plots explaining trends in the data.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get a PDF report for the model
        api_response = api_instance.models_id_report_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_report_get: %s\n" % e)
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
 - **Accept**: application/pdf, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning model report |  -  |
**202** | Report is being generated |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_sensitivity_put**
> file_type models_id_sensitivity_put(id)

Get model sensitivity at a point

Generate a sensitivity analysis around a point. This reports how strongly each column depends on each other column at that point.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.sensitivity_request import SensitivityRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    sensitivity_request = SensitivityRequest(
        data_point=[
            ColumnValue(
                name="name_example",
                value=None,
            ),
        ],
        output_columns=["w","y","z"],
        input_columns=["w","x","y","z"],
    ) # SensitivityRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get model sensitivity at a point
        api_response = api_instance.models_id_sensitivity_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_sensitivity_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get model sensitivity at a point
        api_response = api_instance.models_id_sensitivity_put(id, sensitivity_request=sensitivity_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_sensitivity_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **sensitivity_request** | [**SensitivityRequest**](SensitivityRequest.md)|  | [optional]

### Return type

**file_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning sensitivity matrix |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_share_delete**
> models_id_share_delete(id, share_group)

Stop sharing model with group

Delete group from model's shared groups

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    share_group = ShareGroup(
        group="/Organization Name/Group Name",
    ) # ShareGroup | 

    # example passing only required values which don't have defaults set
    try:
        # Stop sharing model with group
        api_instance.models_id_share_delete(id, share_group)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_share_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
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
**204** | Group deleted from model |  -  |
**404** | Model ID or group not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_share_get**
> [str] models_id_share_get(id)

Get groups with which model is shared

Get model's shared groups

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get groups with which model is shared
        api_response = api_instance.models_id_share_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_share_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

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
**200** | Model&#39;s shared groups |  -  |
**404** | Model ID or group not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_share_put**
> models_id_share_put(id, share_group)

Share model with a group

Add a group to a model which allows all users belonging to that group to have access to the model

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    share_group = ShareGroup(
        group="/Organization Name/Group Name",
    ) # ShareGroup | 

    # example passing only required values which don't have defaults set
    try:
        # Share model with a group
        api_instance.models_id_share_put(id, share_group)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_share_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
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
**204** | Model is shared with given group. |  -  |
**404** | Model ID not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_suggest_additional_get**
> [SuggestAdditionalJob] models_id_suggest_additional_get(id)

Get all suggest-additional jobs for a model

Get all suggest-additional jobs for a given model

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_additional_job import SuggestAdditionalJob
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get all suggest-additional jobs for a model
        api_response = api_instance.models_id_suggest_additional_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_additional_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

[**[SuggestAdditionalJob]**](SuggestAdditionalJob.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All suggest-additional jobs for given model ID |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | The model ID or the dataset used to train the model was not found or the model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_suggest_additional_job_id_delete**
> models_id_suggest_additional_job_id_delete(id, job_id)

Delete suggest-additional job

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job

    # example passing only required values which don't have defaults set
    try:
        # Delete suggest-additional job
        api_instance.models_id_suggest_additional_job_id_delete(id, job_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_additional_job_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
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

# **models_id_suggest_additional_job_id_get**
> SuggestAdditionalJob models_id_suggest_additional_job_id_get(id, job_id)

Get suggest-additional job data

Get job metadata and, if available, the suggestions

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_additional_job import SuggestAdditionalJob
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job

    # example passing only required values which don't have defaults set
    try:
        # Get suggest-additional job data
        api_response = api_instance.models_id_suggest_additional_job_id_get(id, job_id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_additional_job_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **job_id** | **str**| Unique ID of the job |

### Return type

[**SuggestAdditionalJob**](SuggestAdditionalJob.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning suggest-additional job data |  -  |
**400** | Bad request, e.g. invalid model ID or job ID |  -  |
**404** | The model ID or job ID was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_suggest_additional_job_id_patch**
> models_id_suggest_additional_job_id_patch(id, job_id)

Update a suggest additional jobs's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.job_patch import JobPatch
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job
    job_patch = JobPatch(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
    ) # JobPatch |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a suggest additional jobs's metadata
        api_instance.models_id_suggest_additional_job_id_patch(id, job_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_additional_job_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a suggest additional jobs's metadata
        api_instance.models_id_suggest_additional_job_id_patch(id, job_id, job_patch=job_patch)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_additional_job_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **job_id** | **str**| Unique ID of the job |
 **job_patch** | [**JobPatch**](JobPatch.md)|  | [optional]

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

# **models_id_suggest_additional_post**
> str models_id_suggest_additional_post(id, suggest_additional_request)

Suggest additional measurements

Suggest additional measurements in the form of new rows that could be added to the training dataset to improve future models

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_additional_request import SuggestAdditionalRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    suggest_additional_request = SuggestAdditionalRequest(None) # SuggestAdditionalRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Suggest additional measurements
        api_response = api_instance.models_id_suggest_additional_post(id, suggest_additional_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_additional_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **suggest_additional_request** | [**SuggestAdditionalRequest**](SuggestAdditionalRequest.md)|  |

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
**400** | Bad request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |
**404** | The model ID or the dataset used to train the model was not found or the model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_suggest_historic_get**
> [SuggestHistoricJob] models_id_suggest_historic_get(id)

Get all suggest-historic jobs for a model

Get all suggest-historic jobs for a given model

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_historic_job import SuggestHistoricJob
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get all suggest-historic jobs for a model
        api_response = api_instance.models_id_suggest_historic_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_historic_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

[**[SuggestHistoricJob]**](SuggestHistoricJob.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All suggest-historic jobs for given model ID |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | The model ID or the dataset used to train the model was not found or the model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_suggest_historic_job_id_delete**
> models_id_suggest_historic_job_id_delete(id, job_id)

Delete suggest-historic job

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job

    # example passing only required values which don't have defaults set
    try:
        # Delete suggest-historic job
        api_instance.models_id_suggest_historic_job_id_delete(id, job_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_historic_job_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
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

# **models_id_suggest_historic_job_id_get**
> bool, date, datetime, dict, float, int, list, str, none_type models_id_suggest_historic_job_id_get(id, job_id)

Get suggest-historic job data

Get job metadata and, if available, the results

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.get_suggest_historic_running import GetSuggestHistoricRunning
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.get_suggest_historic_pending import GetSuggestHistoricPending
from alchemite_apiclient.model.get_suggest_historic_failed import GetSuggestHistoricFailed
from alchemite_apiclient.model.get_suggest_historic_done import GetSuggestHistoricDone
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job

    # example passing only required values which don't have defaults set
    try:
        # Get suggest-historic job data
        api_response = api_instance.models_id_suggest_historic_job_id_get(id, job_id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_historic_job_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **job_id** | **str**| Unique ID of the job |

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning suggest-historic job data |  -  |
**400** | Bad request, e.g. invalid model ID or job ID |  -  |
**404** | The model ID or job ID was not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_suggest_historic_job_id_patch**
> models_id_suggest_historic_job_id_patch(id, job_id)

Update a suggest historic jobs's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.job_patch import JobPatch
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    job_id = "job_id_example" # str | Unique ID of the job
    job_patch = JobPatch(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
    ) # JobPatch |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a suggest historic jobs's metadata
        api_instance.models_id_suggest_historic_job_id_patch(id, job_id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_historic_job_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a suggest historic jobs's metadata
        api_instance.models_id_suggest_historic_job_id_patch(id, job_id, job_patch=job_patch)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_historic_job_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **job_id** | **str**| Unique ID of the job |
 **job_patch** | [**JobPatch**](JobPatch.md)|  | [optional]

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

# **models_id_suggest_historic_post**
> str models_id_suggest_historic_post(id, suggest_historic_request)

Suggest historic measurements

Suggest historic measurements from an existing dataset that are likely to meet user-specified target criteria. Predictions and uncertainties for missing values in the dataset are used to compute the probability that each historic measurement has of meeting the target criteria.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_historic_request import SuggestHistoricRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    suggest_historic_request = SuggestHistoricRequest(None) # SuggestHistoricRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Suggest historic measurements
        api_response = api_instance.models_id_suggest_historic_post(id, suggest_historic_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_historic_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **suggest_historic_request** | [**SuggestHistoricRequest**](SuggestHistoricRequest.md)|  |

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
**400** | Bad request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |
**404** | The model ID or the dataset used to train the model was not found or the model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_suggest_missing_put**
> [SuggestMissingResponse] models_id_suggest_missing_put(id, suggest_missing_request)

Suggest which missing values to measure next

Get suggestions for which missing values to measure next from a given subset of rows and columns in a dataset in order to best improve subsequent predictions for a given set of target columns. > Part of the underlying algorithm uses the imputed values so a quicker response will be obtained if the `imputedData` is provided as part of the request body. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.suggest_missing_request import SuggestMissingRequest
from alchemite_apiclient.model.suggest_missing_response import SuggestMissingResponse
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    suggest_missing_request = SuggestMissingRequest(None) # SuggestMissingRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Suggest which missing values to measure next
        api_response = api_instance.models_id_suggest_missing_put(id, suggest_missing_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_suggest_missing_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **suggest_missing_request** | [**SuggestMissingRequest**](SuggestMissingRequest.md)|  |

### Return type

[**[SuggestMissingResponse]**](SuggestMissingResponse.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning suggested measurements as an ordered array with the first element being the most recommended suggestion.  The length of the array will be less than or equal to numSuggestions. |  -  |
**400** | Bad request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |
**404** | The model ID or dataset ID (if provided) was not found or the model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_synergy_put**
> InlineResponse2004 models_id_synergy_put(id)

Request the synergy - the input-input interaction, for a given output

Request the pairwise interaction (synergy) between model inputs for a given output.  Synergy values are computed using second-order (input-input) sensitivity analysis,  quantifying the interaction effects—how much each pair of inputs jointly contributes to the output. The synergy values are normalised to the range [0, 1], where 0 indicates no interaction and 1 indicates maximum interaction. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.inline_response2004 import InlineResponse2004
from alchemite_apiclient.model.inline_object1 import InlineObject1
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    inline_object1 = InlineObject1(
        output_column="output_column_example",
    ) # InlineObject1 |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Request the synergy - the input-input interaction, for a given output
        api_response = api_instance.models_id_synergy_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_synergy_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Request the synergy - the input-input interaction, for a given output
        api_response = api_instance.models_id_synergy_put(id, inline_object1=inline_object1)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_synergy_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **inline_object1** | [**InlineObject1**](InlineObject1.md)|  | [optional]

### Return type

[**InlineResponse2004**](InlineResponse2004.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The synergy for the requested column |  -  |
**202** | Synergy is being generated |  -  |
**400** | Bad Request, e.g. Invalid model ID or outputColumn |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_train_put**
> models_id_train_put(id)

Train a model

Train the model on the dataset corresponding to the 'trainingDatasetId' parameter in the model metadata.  The dataset must have the status 'processing' or 'uploaded' to begin to have a model trained on it.  If `hyperparameterOptimization` is 'none' then the model 'status' will be first set to 'pending' and then 'training' once the model has started training.  Otherwise the model 'status' will be first set to 'optimizing hyperparameters' and then once the optimal hyperparameters have been found set to 'pending' and then 'training'.  The model status will be set to 'trained' once it has finished training and is ready to use.  Use GET /model/{id} to get model status as well as percentage training and hyperparameter optimization completion. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.train_request import TrainRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    train_request = TrainRequest(
        validation="none",
        validation_target_columns=["Resistivity","Tensile Strength"],
        validation_splits=[
            ValidationSplit(
                name="name_example",
                test_row_ids=[
                    "test_row_ids_example",
                ],
                train_row_ids=[
                    "train_row_ids_example",
                ],
            ),
        ],
        hyperparameter_optimization="none",
        bespoke_column_hyperparameters=True,
        hyperparameters={},
        fraction_data_present=[
            0,
        ],
        virtual_experiment_validation=False,
        virtual_training=False,
        permitted_column_relationships=[
            ModelsIdTrainPermittedColumnRelationships(
                name="name_example",
                allow=[
                    "allow_example",
                ],
                disallow=[
                    "disallow_example",
                ],
            ),
        ],
        enable_training_dataset_outliers=True,
        max_number_samples=200,
        target_function=HyperoptTargetFunction(
            key=None,
        ),
        exploration_exploitation=1,
    ) # TrainRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Train a model
        api_instance.models_id_train_put(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_train_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Train a model
        api_instance.models_id_train_put(id, train_request=train_request)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_train_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **train_request** | [**TrainRequest**](TrainRequest.md)|  | [optional]

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
**202** | Began training. |  -  |
**400** | Bad request, eg. invalid model ID. |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or training unavailable because the model is training or has already been trained on this dataset. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_training_dataset_outliers_put**
> file_type models_id_training_dataset_outliers_put(id)

Find the outlying values in the model's training dataset

> Requires that the model was trained with `enableTrainingDatasetOutliers` set to true.  Compares the training dataset with the corresponding predicted values using the requested validation splits.  If the model's `validationMethod` is '5-fold', each will be trained on 80% of the full dataset to identify the outliers in the remaining 20%. If the model's `validationMethod` is 'custom', each row in a test set will be checked against a model trained on the matching train set. Please note, if `validationMethod` is '80/20', only the validation 20% will report outliers, and is thus not recommended.  If a given value lies outside of the error bounds of the corresponding predicted value then it is deemed an outlier.  Returns the given value of all outliers along with the corresponding predicted values, the number of standard deviations between the given and predicted values and the row and column indices of the outlier.  If the outlier is part of a vector then the \"Component Index\" indicates which component of the vector is an outlier.  If the outlier is not a vector then the \"Component Index\" will be 1. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.training_dataset_outliers_request import TrainingDatasetOutliersRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    training_dataset_outliers_request = TrainingDatasetOutliersRequest(
        row_ids=[
            "row_ids_example",
        ],
    ) # TrainingDatasetOutliersRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Find the outlying values in the model's training dataset
        api_response = api_instance.models_id_training_dataset_outliers_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_training_dataset_outliers_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Find the outlying values in the model's training dataset
        api_response = api_instance.models_id_training_dataset_outliers_put(id, training_dataset_outliers_request=training_dataset_outliers_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_training_dataset_outliers_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **training_dataset_outliers_request** | [**TrainingDatasetOutliersRequest**](TrainingDatasetOutliersRequest.md)|  | [optional]

### Return type

**file_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning comparison between predicted and measured values |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_unload_put**
> models_id_unload_put(id)

Unload model from memory

Remove a loaded model from memory.  Impute requests can still be sent but the model will be loaded into memory at request time.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Unload model from memory
        api_instance.models_id_unload_put(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_unload_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

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
**200** | Model is unloaded. |  -  |
**404** | Model ID not found or is not preloaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_validate_put**
> bool, date, datetime, dict, float, int, list, str, none_type models_id_validate_put(id)

Validate given data

Given a dataset return the predictions for the given values in the dataset with the uncertainties or full probability distribution for each prediction.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.validate_request import ValidateRequest
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    validate_request = ValidateRequest(
        return_probability_distribution=False,
        dataset_id="dataset_id_example",
        return_row_headers=False,
        return_column_headers=False,
        data='''x,y,x+y,x-y
1,0.2,,0.8
0.5,0.3,,
''',
    ) # ValidateRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Validate given data
        api_response = api_instance.models_id_validate_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_validate_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Validate given data
        api_response = api_instance.models_id_validate_put(id, validate_request=validate_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_validate_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **validate_request** | [**ValidateRequest**](ValidateRequest.md)|  | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning predictions |  -  |
**400** | Bad request, eg. CSV malformed or missing column headers |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_validation_predictions_get**
> file_type models_id_validation_predictions_get(id)

Get the predictions used to calculate the model's quality during training

> Requires that the model was trained with `validation` set to `80/20` or `5-fold`.  Returns the validation predictions generated for assessing model performance during training.  For 5-fold validation, this is the result of training 5 sub-models on 80% and predicting on the remaining 20%, such that the each row in dataset is represented in exactly one validation set. For 80/20 validation, 20% of the dataset is selected at random to form the validation set. This endpoint has been deprecated, please use PUT /models/{id}/validation-predictions instead. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get the predictions used to calculate the model's quality during training
        api_response = api_instance.models_id_validation_predictions_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_validation_predictions_get: %s\n" % e)
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
**200** | Returning comparison between predicted and measured values |  -  |
**400** | Bad request |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_validation_predictions_put**
> file_type models_id_validation_predictions_put(id)

Get the predictions used to calculate the model's quality during training

> Requires that the model was trained with `validation` set to `80/20` or `5-fold`.  Returns validation predictions for given columns so that the model training performance can be evaluated. For 5-fold validation, this is the result of training 5 sub-models on 80% and predicting on the remaining 20%, such that the each row in dataset is represented in exactly one validation set. For 80/20 validation, 20% of the dataset is selected at random to form the validation set. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.training_validation_prediction_request import TrainingValidationPredictionRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    training_validation_prediction_request = TrainingValidationPredictionRequest(
        columns=["x1","x2","y1","y2"],
    ) # TrainingValidationPredictionRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get the predictions used to calculate the model's quality during training
        api_response = api_instance.models_id_validation_predictions_put(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_validation_predictions_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get the predictions used to calculate the model's quality during training
        api_response = api_instance.models_id_validation_predictions_put(id, training_validation_prediction_request=training_validation_prediction_request)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_validation_predictions_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **training_validation_prediction_request** | [**TrainingValidationPredictionRequest**](TrainingValidationPredictionRequest.md)|  | [optional]

### Return type

**file_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning comparison between predicted and measured values |  -  |
**400** | Bad request |  -  |
**404** | Model ID not found or model is not trained or has not been trained on the dataset attached to it. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_validation_splits_get**
> bool, date, datetime, dict, float, int, list, str, none_type models_id_validation_splits_get(id)

Get a model's validation splits.

Get the validation splits used for a model. Requires that the model has been trained, and was not trained with `validation` set to 'none'.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get a model's validation splits.
        api_response = api_instance.models_id_validation_splits_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_id_validation_splits_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning model validation splits |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_import_post**
> str models_import_post()

Import a model

Upload a zip file, as provided by GET /models/{id}/download, which will set the data and metadata of a new model.  If the model ID included in the provided metadata is not already assigned to another model then it will be used as the ID for the new model, otherwise a new unique ID will be created for the new model.  In either case a successful response will return the model ID of the new model.  > Not enabled by default. Please contact Intellegens if required 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
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
    api_instance = models_api.ModelsApi(api_client)
    body = open('/path/to/file', 'rb') # file_type |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Import a model
        api_response = api_instance.models_import_post(body=body)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_import_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **file_type**|  | [optional]

### Return type

**str**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/zip
 - **Accept**: text/plain, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The model was created.  Return the model ID. |  -  |
**400** | Bad request, eg. required files missing from .zip file. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_metadata_put**
> InlineResponse2002 models_metadata_put()

List sorted and filtered model metadata

Returns all models matching the query passed.  

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.model_query import ModelQuery
from alchemite_apiclient.model.inline_response2002 import InlineResponse2002
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = models_api.ModelsApi(api_client)
    offset = 0 # int | The number of items to skip before starting to collect the result set. (optional) if omitted the server will use the default value of 0
    limit = 20 # int | The number of items to return. (optional) if omitted the server will use the default value of 20
    model_query = ModelQuery(
        sort=[
            ModelsMetadataSort(
                name="name",
                direction="asc",
            ),
        ],
        filters=ModelsMetadataFilters(
            name="name_example",
            status=ModelStatus("new"),
            validation_metric=NumericalFilter(None),
            validation_method=ModelValidationMethods("none"),
            virtual_training=True,
            virtual_experiment_validation=True,
            training_completion_time=NumericalFilter(None),
            training_method_version="training_method_version_example",
            groups=[
                "groups_example",
            ],
            owner=True,
            created_at=NumericalFilter(None),
            tags=[
                "tags_example",
            ],
            project_id="00112233-4455-6677-8899-aabbccddeeff",
            unrevised=False,
            transitive_model_id="00112233-4455-6677-8899-aabbccddeeff",
            exclude_model_id="00112233-4455-6677-8899-aabbccddeeff",
            search="search_example",
        ),
    ) # ModelQuery |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List sorted and filtered model metadata
        api_response = api_instance.models_metadata_put(offset=offset, limit=limit, model_query=model_query)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_metadata_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**| The number of items to skip before starting to collect the result set. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| The number of items to return. | [optional] if omitted the server will use the default value of 20
 **model_query** | [**ModelQuery**](ModelQuery.md)|  | [optional]

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of models matching given query |  -  |
**400** | Bad request |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_post**
> str models_post(model)

Define a model to be trained

Create new model and return the model ID associated with it.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import models_api
from alchemite_apiclient.model.model import Model
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
    api_instance = models_api.ModelsApi(api_client)
    model = Model(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
        project_id="00112233-4455-6677-8899-aabbccddeeff",
        status=ModelStatus("new"),
        revises_id="00112233-4455-6677-8899-aabbccddeeff",
        training_method="alchemite",
        training_dataset_id="00112233-4455-6677-8899-aabbccddeeff",
        validation_method=ModelValidationMethods("none"),
    ) # Model | A JSON object containing the name and training method for the model.  The dataset ID of the dataset that will be used to train the model must be provided under the key `trainingDatasetId`.

    # example passing only required values which don't have defaults set
    try:
        # Define a model to be trained
        api_response = api_instance.models_post(model)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelsApi->models_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model** | [**Model**](Model.md)| A JSON object containing the name and training method for the model.  The dataset ID of the dataset that will be used to train the model must be provided under the key &#x60;trainingDatasetId&#x60;. |

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
**201** | The model was created.  Return the model ID. |  -  |
**400** | Bad Request, eg. JSON malformed or with invalid parameters |  -  |
**401** | Licence expired |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

