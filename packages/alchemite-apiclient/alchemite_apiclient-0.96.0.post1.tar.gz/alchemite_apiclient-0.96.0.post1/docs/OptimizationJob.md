# OptimizationJob

The metadata and, if available, results for the job

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enqueue_time** | **int** | The Unix Timestamp in seconds when the optimize job enqueued. | [optional] [readonly] 
**start_time** | **int** | The Unix Timestamp in seconds when the optimize job started. | [optional] [readonly] 
**end_time** | **int** | The Unix Timestamp in seconds when the optimize job ended. | [optional] [readonly] 
**sharing** | [**PartGetOptimizeSharing**](PartGetOptimizeSharing.md) |  | [optional] 
**progress** | **float** |  | [optional] 
**id** | **str** |  | [optional] 
**parameters** | [**OptimizeRequest**](OptimizeRequest.md) |  | [optional] 
**status** | **str** |  | [optional]  if omitted the server will use the default value of "failed"
**result** | [**PartGetOptimizeDoneResultArray**](PartGetOptimizeDoneResultArray.md) |  | [optional] 
**detail** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


