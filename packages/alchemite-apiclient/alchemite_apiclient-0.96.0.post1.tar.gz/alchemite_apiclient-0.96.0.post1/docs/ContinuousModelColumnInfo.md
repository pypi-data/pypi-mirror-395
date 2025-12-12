# ContinuousModelColumnInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The unique name of the column. | 
**max** | **float, none_type** | The maximum value appearing in this column in the dataset. If the column is empty, will be set to null. | 
**min** | **float, none_type** | The minimum value appearing in this column in the dataset. If the column is empty, will be set to null. | 
**mean** | **float, none_type** | The mean average of the values appearing in this column in the dataset. If the column is empty, will be set to null. | 
**data_type** | **str** |  | defaults to "continuous"
**num_samples** | **int** | The number of non-missing values appearing in this column in the dataset. | defaults to 0
**is_descriptor** | **bool** | Whether the column is a descriptor or not | [optional] 
**is_complete** | **bool** | Whether the column is complete or not | [optional] 
**read_only** | **bool** | Whether values can be set for this column in Alchemite operations | [optional]  if omitted the server will use the default value of False
**write_only** | **bool** | If true then this column must be provided for all Alchemite operations but will typically not be returned. | [optional]  if omitted the server will use the default value of False
**extension_source** | **str** | The name of the extension method that created this column | [optional] 
**calculated_column** | **bool** |  | [optional]  if omitted the server will use the default value of False
**std_dev** | **float, none_type** | The population standard deviation of the values appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**min_non_zero** | **float, none_type** | The minimum non-zero value appearing in this column in the dataset. | [optional] 
**coefficient_of_determination** | **float, none_type** | The coefficient of determination for this column in the dataset.  In the case of 5-fold validation this is the mean average for the column across the 5 validation datasets.  Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor or there is no variation in the column&#39;s values. | [optional] 
**rmse** | **float, none_type** | The Root Mean Squared Error (RMSE) for this column in the dataset.  Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor. | [optional] 
**mape** | **float, none_type** | The Mean Absolute Percentage Error (MAPE) for this column in the dataset.  Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60;, if the calculated value was non-finite, or if the column is a descriptor. | [optional] 
**targeted_metric** | **float, none_type** | The value of the targeted metric for this column in the dataset. Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor, and not present if targets were not set for this column during training. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


