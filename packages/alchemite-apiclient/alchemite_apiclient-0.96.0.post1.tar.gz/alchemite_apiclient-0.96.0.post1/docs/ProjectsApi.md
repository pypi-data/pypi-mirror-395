# alchemite_apiclient.ProjectsApi

All URIs are relative to *https://alchemiteapi.intellegens.ai/v0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**projects_get**](ProjectsApi.md#projects_get) | **GET** /projects | List the metadata for every project
[**projects_id_delete**](ProjectsApi.md#projects_id_delete) | **DELETE** /projects/{id} | Delete project
[**projects_id_get**](ProjectsApi.md#projects_id_get) | **GET** /projects/{id} | Get project metadata
[**projects_id_models_batch_put**](ProjectsApi.md#projects_id_models_batch_put) | **PUT** /projects/{id}/models/batch | Move a number of models into or out of a project
[**projects_id_patch**](ProjectsApi.md#projects_id_patch) | **PATCH** /projects/{id} | Update a project&#39;s metadata
[**projects_id_share_delete**](ProjectsApi.md#projects_id_share_delete) | **DELETE** /projects/{id}/share | Stop sharing project with group
[**projects_id_share_get**](ProjectsApi.md#projects_id_share_get) | **GET** /projects/{id}/share | Get groups with which project is shared
[**projects_id_share_put**](ProjectsApi.md#projects_id_share_put) | **PUT** /projects/{id}/share | Share project with a group
[**projects_id_suggest_initial_batch_put**](ProjectsApi.md#projects_id_suggest_initial_batch_put) | **PUT** /projects/{id}/suggest-initial/batch | Move a number of suggest-initial jobs into or out of a project
[**projects_post**](ProjectsApi.md#projects_post) | **POST** /projects | Define a project


# **projects_get**
> [Project] projects_get()

List the metadata for every project

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
from alchemite_apiclient.model.project import Project
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # List the metadata for every project
        api_response = api_instance.projects_get()
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[Project]**](Project.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning list of projects |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_id_delete**
> projects_id_delete(id)

Delete project

Deletes the project. Any associated resources will be removed from the project but continue to exist. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
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
    api_instance = projects_api.ProjectsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the project.

    # example passing only required values which don't have defaults set
    try:
        # Delete project
        api_instance.projects_id_delete(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the project. |

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
**204** | Project deleted |  -  |
**400** | Invalid project ID |  -  |
**404** | Project ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_id_get**
> Project projects_id_get(id)

Get project metadata

Get project data

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.project import Project
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the project.

    # example passing only required values which don't have defaults set
    try:
        # Get project metadata
        api_response = api_instance.projects_id_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the project. |

### Return type

[**Project**](Project.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning project data |  -  |
**400** | Bad request, e.g. invalid project ID |  -  |
**404** | Project ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_id_models_batch_put**
> projects_id_models_batch_put(id, project_bulk_model)

Move a number of models into or out of a project

Move a large number of models into or out of projects. If a model being moved into a project is already in another project, it will first be removed from its current project 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.project_bulk_model import ProjectBulkModel
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the project.
    project_bulk_model = ProjectBulkModel(
        add=[
            "00112233-4455-6677-8899-aabbccddeeff",
        ],
        remove=[
            "00112233-4455-6677-8899-aabbccddeeff",
        ],
    ) # ProjectBulkModel | 

    # example passing only required values which don't have defaults set
    try:
        # Move a number of models into or out of a project
        api_instance.projects_id_models_batch_put(id, project_bulk_model)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_models_batch_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the project. |
 **project_bulk_model** | [**ProjectBulkModel**](ProjectBulkModel.md)|  |

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
**204** | Models are successfully updated with respect to the project. |  -  |
**400** | Bad Request, eg. JSON malformed or invalid model ID |  -  |
**404** | Project ID not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_id_patch**
> projects_id_patch(id)

Update a project's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
from alchemite_apiclient.model.project_patch import ProjectPatch
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
    api_instance = projects_api.ProjectsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the project.
    project_patch = ProjectPatch(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
    ) # ProjectPatch |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update a project's metadata
        api_instance.projects_id_patch(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_patch: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update a project's metadata
        api_instance.projects_id_patch(id, project_patch=project_patch)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the project. |
 **project_patch** | [**ProjectPatch**](ProjectPatch.md)|  | [optional]

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
**204** | Project metadata updated |  -  |
**400** | Invalid project ID |  -  |
**404** | Project ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_id_share_delete**
> projects_id_share_delete(id, share_group)

Stop sharing project with group

Delete group from project's shared groups

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
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
    api_instance = projects_api.ProjectsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the project.
    share_group = ShareGroup(
        group="/Organization Name/Group Name",
    ) # ShareGroup | 

    # example passing only required values which don't have defaults set
    try:
        # Stop sharing project with group
        api_instance.projects_id_share_delete(id, share_group)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_share_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the project. |
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
**204** | Group deleted from project |  -  |
**404** | Project ID or group not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_id_share_get**
> [str] projects_id_share_get(id)

Get groups with which project is shared

Get project's shared groups

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
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
    api_instance = projects_api.ProjectsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the project.

    # example passing only required values which don't have defaults set
    try:
        # Get groups with which project is shared
        api_response = api_instance.projects_id_share_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_share_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the project. |

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
**200** | Project&#39;s shared groups |  -  |
**404** | Project ID or group not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_id_share_put**
> projects_id_share_put(id, share_group)

Share project with a group

Add a group to a project which allows all users belonging to that group to have access to the project

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
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
    api_instance = projects_api.ProjectsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the project.
    share_group = ShareGroup(
        group="/Organization Name/Group Name",
    ) # ShareGroup | 

    # example passing only required values which don't have defaults set
    try:
        # Share project with a group
        api_instance.projects_id_share_put(id, share_group)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_share_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the project. |
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
**204** | Project is shared with given group. |  -  |
**404** | Project ID not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_id_suggest_initial_batch_put**
> projects_id_suggest_initial_batch_put(id, project_bulk_suggest_initial)

Move a number of suggest-initial jobs into or out of a project

Move a large number of suggest-initial jobs into or out of projects. If a suggest-initial jobs being moved into a project is already in another project, it will first be removed from its current project 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.project_bulk_suggest_initial import ProjectBulkSuggestInitial
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the project.
    project_bulk_suggest_initial = ProjectBulkSuggestInitial(
        add=[
            "00112233-4455-6677-8899-aabbccddeeff",
        ],
        remove=[
            "00112233-4455-6677-8899-aabbccddeeff",
        ],
    ) # ProjectBulkSuggestInitial | 

    # example passing only required values which don't have defaults set
    try:
        # Move a number of suggest-initial jobs into or out of a project
        api_instance.projects_id_suggest_initial_batch_put(id, project_bulk_suggest_initial)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_id_suggest_initial_batch_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the project. |
 **project_bulk_suggest_initial** | [**ProjectBulkSuggestInitial**](ProjectBulkSuggestInitial.md)|  |

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
**204** | Suggest-initial jobs are successfully updated with respect to the project. |  -  |
**400** | Bad Request, eg. JSON malformed or invalid job ID |  -  |
**404** | Project ID not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projects_post**
> str projects_post(project)

Define a project

Create new project and return the project ID associated with it.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import projects_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.project import Project
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    project = Project(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
    ) # Project | A JSON object containing the name and metadata for the project.

    # example passing only required values which don't have defaults set
    try:
        # Define a project
        api_response = api_instance.projects_post(project)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ProjectsApi->projects_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project** | [**Project**](Project.md)| A JSON object containing the name and metadata for the project. |

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
**201** | The project was created. Return the project ID. |  -  |
**400** | Bad Request, eg. JSON malformed or with invalid parameters |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

