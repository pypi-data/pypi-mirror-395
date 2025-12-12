# SuggestHistoricResult

The set of returned results from a run of suggest historic

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**truncated** | **bool** | When true, this indicates that the result set was shortened to 500 due to too many records being selected by the provided function. This should be reported to the user as a soft error.  | 
**samples** | [**[SuggestHistoricResultSamples]**](SuggestHistoricResultSamples.md) | Array with the samples from the dataset most likely to meet the specified targetFunction | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


