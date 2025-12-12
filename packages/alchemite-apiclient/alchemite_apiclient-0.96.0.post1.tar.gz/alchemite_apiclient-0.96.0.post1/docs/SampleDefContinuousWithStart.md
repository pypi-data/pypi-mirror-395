# SampleDefContinuousWithStart

The key value must be a valid column name. The constraint will be applied to this column. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | * &#x60;\&quot;continuous\&quot;&#x60;: Search a continuous domain within the &#x60;\&quot;range\&quot;&#x60; specified with uniform prior. * &#x60;\&quot;continuous or zero\&quot;&#x60;: Either search a continuous domain within the &#x60;\&quot;range\&quot;&#x60; specified, or return 0.  | 
**range** | **[float]** | Range is an array consisting of a lower and upper bound where the lower bound is strictly smaller than the upper bound.  | 
**start** | **float** | &#x60;\&quot;start\&quot;&#x60; is used for local optimization only. * &#x60;\&quot;start\&quot;&#x60; specifies the start point of the local optimisation. * If it is not specified the mean value of the &#x60;\&quot;range\&quot;&#x60; will be taken as the starting point.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


