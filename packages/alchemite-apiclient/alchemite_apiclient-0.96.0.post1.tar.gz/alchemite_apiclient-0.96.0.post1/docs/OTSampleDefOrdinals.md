# OTSampleDefOrdinals

The key value must be a valid column name. The constraint will be applied to this column. If the sampleDefinition only contains a single column and that column is an ordinal, the amount of  results returned will be equal to the number of ordinals encompassed by the given range (one sample per ordinal value).  If there are multiple columns being sampled then the number of samples requested will be returned. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**range** | **[float]** | Range is an array consisting of a lower and upper bound where the lower bound is strictly smaller than the upper bound. The range must encompass at least one defined ordinal value  | 
**type** | **str** | Sample from a ordinal domain specified by the range.  | defaults to "ordinal"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


