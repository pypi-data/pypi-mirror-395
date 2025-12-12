# MetadataOptimizationJob


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_id** | **str** | The ID of the model associated with the job. | 
**id** | **str** |  | 
**parameters** | **bool, date, datetime, dict, float, int, list, str, none_type** | The parameters as they were given to the optimize request. | [readonly] 
**result** | [**PartGetOptimizeDoneResultArray**](PartGetOptimizeDoneResultArray.md) |  | 
**detail** | **str** |  | 
**status** | **str** |  | defaults to "failed"
**type** | **str** |  | defaults to "optimize"
**name** | **str** | The job&#39;s name | [optional] 
**tags** | **[str]** | The tags attached to the job | [optional] 
**notes** | **str** | An optional free field for notes about the job. | [optional] 
**enqueue_time** | **int** | The Unix Timestamp in seconds when the optimize job enqueued. | [optional] [readonly] 
**start_time** | **int** | The Unix Timestamp in seconds when the optimize job started. | [optional] [readonly] 
**end_time** | **int** | The Unix Timestamp in seconds when the optimize job ended. | [optional] [readonly] 
**sharing** | [**PartGetOptimizeSharing**](PartGetOptimizeSharing.md) |  | [optional] 
**progress** | **float** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


