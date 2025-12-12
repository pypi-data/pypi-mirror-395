# SuggestAdditionalJob

The metadata and, if available, results for the job

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The job&#39;s name | [optional] 
**tags** | **[str]** | The tags attached to the job | [optional] 
**notes** | **str** | An optional free field for notes about the job. | [optional] 
**enqueue_time** | **int** | The Unix Timestamp in seconds when the job enqueued. | [optional] [readonly] 
**start_time** | **int** | The Unix Timestamp in seconds when the job started. | [optional] [readonly] 
**end_time** | **int** | The Unix Timestamp in seconds when the job ended. | [optional] [readonly] 
**sharing** | [**PartGetOptimizeSharing**](PartGetOptimizeSharing.md) |  | [optional] 
**progress** | **float** |  | [optional] 
**id** | **str** |  | [optional] 
**parameters** | [**SuggestAdditionalParameters**](SuggestAdditionalParameters.md) |  | [optional] 
**status** | **str** |  | [optional]  if omitted the server will use the default value of "failed"
**result** | [**SuggestAdditionalResult**](SuggestAdditionalResult.md) |  | [optional] 
**detail** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


