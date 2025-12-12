# ContinuousColumnInfoStats


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**std_dev** | **float, none_type** | The population standard deviation of the values appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**min_non_zero** | **float, none_type** | The minimum non-zero value appearing in this column in the dataset. | [optional] 
**num_samples** | **int** | The number of non-missing values appearing in this column in the dataset. | [optional]  if omitted the server will use the default value of 0
**max** | **float, none_type** | The maximum value appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**min** | **float, none_type** | The minimum value appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**mean** | **float, none_type** | The mean average of the values appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


