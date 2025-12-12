# PredictTrendlineRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input_column** | **str** | Name of the input column for the trendline calculation. This column can be either a model descriptor or non-descriptor | [optional] 
**output_column** | **str** | Name of the output column for the trendline calculation. This column must be a model non-descriptor | [optional] 
**bin_count** | **int** | The number of splits in the trendline to calculate between the two columns | [optional]  if omitted the server will use the default value of 10

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


