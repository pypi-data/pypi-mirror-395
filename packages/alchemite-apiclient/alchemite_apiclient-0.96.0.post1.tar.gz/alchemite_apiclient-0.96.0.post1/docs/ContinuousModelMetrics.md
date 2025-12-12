# ContinuousModelMetrics


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**coefficient_of_determination** | **float, none_type** | The coefficient of determination for this column in the dataset.  In the case of 5-fold validation this is the mean average for the column across the 5 validation datasets.  Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor or there is no variation in the column&#39;s values. | [optional] 
**rmse** | **float, none_type** | The Root Mean Squared Error (RMSE) for this column in the dataset.  Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor. | [optional] 
**mape** | **float, none_type** | The Mean Absolute Percentage Error (MAPE) for this column in the dataset.  Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60;, if the calculated value was non-finite, or if the column is a descriptor. | [optional] 
**targeted_metric** | **float, none_type** | The value of the targeted metric for this column in the dataset. Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor, and not present if targets were not set for this column during training. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


