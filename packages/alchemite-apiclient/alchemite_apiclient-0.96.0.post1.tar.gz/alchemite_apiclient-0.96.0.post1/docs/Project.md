# Project

Metadata for a project

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**id** | **str** | Unique identifier for the project. | [optional] [readonly] 
**tags** | **[str]** | Optional tags to attach to the project | [optional] 
**notes** | **str** | An optional free field for notes about the dataset | [optional] 
**created_at** | **int** | The Unix Timestamp in seconds when POST /projects was called. If &#x60;0&#x60; (Unix system time zero) then creation timestamp unavailable. This can happen for older projects.  | [optional] [readonly] 
**model_count** | **int** | The number of models within the project | [optional] [readonly] 
**suggest_initial_count** | **int** | The number of suggest-initial jobs within the project | [optional] [readonly] 
**sharing** | [**ProjectSharing**](ProjectSharing.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


