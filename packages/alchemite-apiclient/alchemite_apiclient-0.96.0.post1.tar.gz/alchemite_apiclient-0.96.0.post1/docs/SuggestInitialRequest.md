# SuggestInitialRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sample_definition** | [**SISampleDefinition**](SISampleDefinition.md) |  | 
**name** | **str** | Optional name to attach to the job. | [optional] 
**tags** | **[str]** | Optional tags to attach to the job. Array should contain unique strings.  | [optional] 
**notes** | **str** | An optional free field for notes about the job. | [optional] 
**project_id** | **str** |  | [optional] 
**num_suggestions** | **int** | The number of suggested measurements to return.  | [optional]  if omitted the server will use the default value of 2
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


