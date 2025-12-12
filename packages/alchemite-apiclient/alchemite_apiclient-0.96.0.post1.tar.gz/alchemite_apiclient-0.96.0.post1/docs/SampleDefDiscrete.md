# SampleDefDiscrete

The key value must be a valid column name. The constraint will be applied to this column. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**range** | **[float]** | Range is an array consisting of a lower and upper bound where the lower bound is strictly smaller than the upper bound.  | 
**step_size** | **float** | Step size to take within the range | 
**type** | **str** | Pick a value within the discretized &#x60;\&quot;range\&quot;&#x60;, where discretization is done with the &#x60;\&quot;stepSize\&quot;&#x60;.  | defaults to "discrete"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


