# JobsMetadataFilters

Filter jobs based on job and model attributes. Note that currently each filter is AND'ed. If a requested job type doesn't have the required attribute, it will be omitted from the results 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the job. Will return jobs with names containing a subset of this value | [optional] 
**status** | **str** | The status of the job. When asking for optimize jobs, &#x60;running&#x60; will be treated as &#x60;optimizing&#x60; | [optional] 
**tags** | **[str]** | Tags that the job contains | [optional] 
**num_optimization_samples** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**num_suggestions** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**exploration_exploitation** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**project_id** | **str** | The project the job&#39;s model belongs to. | [optional] 
**transitive_model_id** | **str** | A model id. If provided the jobs returned will belong to that model or a previous revision of that model. Cannot be used with jobIds | [optional] 
**exclude_model_id** | **str** | A model id. If provided, none of the jobs returned will belong to that model. Intended for use in combination with transitiveModelId. Cannot be used with jobIds | [optional] 
**model_id** | **str** | A model id. If provided the jobs returned will belong to that model. Cannot be used with jobIds | [optional] 
**search** | **str** | Will search over all valid fields for the job and return any jobs that contain the provided key | [optional] 
**job_ids** | **[str]** | Will filter results by given job ids. Cannot be used with modelId, transitiveModelId or excludeModelId filters. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


