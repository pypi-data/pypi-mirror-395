# SuggestHistoricParameters


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** | The ID of a dataset to search within.  The dataset must have the same column headers as the model&#39;s training dataset. | 
**target_function** | [**HistoricTargetFunction**](HistoricTargetFunction.md) |  | 
**num_suggestions** | **int** | The target number of rows to be returned. May return greater than this number where too many rows meet the criterion without any imputed values, and may return fewer if too few results are meet the provided criteria. If the provided criteria would return more than 500 rows, the sample will be truncated.  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


