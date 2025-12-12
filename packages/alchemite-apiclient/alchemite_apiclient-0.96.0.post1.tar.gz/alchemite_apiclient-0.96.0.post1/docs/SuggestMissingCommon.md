# SuggestMissingCommon


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**num_suggestions** | **int** | The maximum number of suggested measurements to return that will best improve predictions for the requested targetColumns. | [optional]  if omitted the server will use the default value of 1
**s_factor** | **float, none_type** | Where data is mostly missing, sFactor should take low values - when data is mostly complete, it should take higher values.  If not given or null then sFactor will be set automatically, which is generally recommended.  Adjusting sFactor can make significant differences to the suggestions returned. | [optional] 
**uncertainty_weight** | **float** | Weighting determining the importance of uncertainties for individual data points compared to inter-column relationships when calculating suggested measurements.  If 0 then only column relationships are used to produce suggestions, while if 1 then uncertainties are treated as more important. Deprecated, this parameter is no longer supported. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


