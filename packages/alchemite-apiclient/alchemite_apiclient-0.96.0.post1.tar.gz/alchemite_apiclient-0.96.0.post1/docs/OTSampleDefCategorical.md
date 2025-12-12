# OTSampleDefCategorical

The key value must be a valid column name. The constraint will be applied to this column. If the sampleDefinition only contains a single column and that column is a categorical, the amount of  results returned will be equal to the number of categories given in values (one sample per value).  If there are multiple columns being sampled then the number of samples requested will be returned. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Values is an array consisting of the categorical values for the column that will be uniformly sampled over.  There cannot be more categories in the list than there are number of samples requested.  | 
**type** | **str** | Sample from a categorical domain specified by the values.  | defaults to "categorical"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


