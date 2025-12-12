# SampleDefCategorical

The key value is a made up variable name by which to identify the constraint. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | [**{str: (SampleDefCategoricalColumnValues,)}**](SampleDefCategoricalColumnValues.md) | Describe the options and accompanying values to choose between. | 
**type** | **str** |  | defaults to "categorical"
**start** | **str** | &#x60;\&quot;start\&quot;&#x60; is used for local optimization only. * &#x60;\&quot;start\&quot;&#x60; specifies the start point of the local optimisation (i.e. the given option). * &#x60;\&quot;start\&quot;&#x60; is **required** when performing local optimization.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


