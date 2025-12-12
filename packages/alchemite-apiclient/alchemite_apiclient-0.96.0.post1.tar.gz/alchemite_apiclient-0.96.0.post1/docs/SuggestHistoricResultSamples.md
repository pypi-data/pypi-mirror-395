# SuggestHistoricResultSamples

Object with sample and its probability of success.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**row_id** | **str** | The row IDs of the samples that have been identified. | 
**probability_of_success** | **float** | Confidence metric (in percentage) indicating the likelihood that the result will meet the given targets. | 
**suggested_sample** | [**[HistoricValue]**](HistoricValue.md) | The suggested sample from the dataset.  Name contains the property&#39;s name. Value contains a scalar or list of scalars for vector properties.  | 
**predicted_properties** | [**[HistoricPrediction]**](HistoricPrediction.md) | The predictions for non-descriptor properties, both undefined and target properties. Name contains the property&#39;s name. Value contains a single prediction for scalars or multiple predictions (as a list) for vectors. A prediction consists of a &#39;value&#39; field and an &#39;uncertainty&#39; field.  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


