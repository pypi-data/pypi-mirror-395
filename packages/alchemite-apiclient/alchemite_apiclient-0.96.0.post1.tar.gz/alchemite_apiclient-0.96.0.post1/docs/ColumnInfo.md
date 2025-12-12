# ColumnInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_descriptor** | **bool** | Whether the column is a descriptor or not | [optional] 
**is_complete** | **bool** | Whether the column is complete or not | [optional] 
**read_only** | **bool** | Whether values can be set for this column in Alchemite operations | [optional]  if omitted the server will use the default value of False
**write_only** | **bool** | If true then this column must be provided for all Alchemite operations but will typically not be returned. | [optional]  if omitted the server will use the default value of False
**extension_source** | **str** | The name of the extension method that created this column | [optional] 
**calculated_column** | **bool** |  | [optional]  if omitted the server will use the default value of False
**std_dev** | **float, none_type** | The population standard deviation of the values appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**min_non_zero** | **float, none_type** | The minimum non-zero value appearing in this column in the dataset. | [optional] 
**data_subtype** | **str** | An optional subtype describing the type of data held in the opaque column | [optional] 
**name** | **str** | The unique name of the column. | [optional] 
**data_type** | **str** |  | [optional]  if omitted the server will use the default value of "ordinal"
**num_samples** | **int** | The number of non-missing values appearing in this column in the dataset. | [optional]  if omitted the server will use the default value of 0
**categories_present** | **[str]** | The categories that are present for this column in the dataset. If the column is empty, will be empty array. | [optional] 
**mode** | **float, none_type** | The mode of the values appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**max** | **float, none_type** | The maximum value appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**min** | **float, none_type** | The minimum value appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**mean** | **float, none_type** | The mean average of the values appearing in this column in the dataset. If the column is empty, will be set to null. | [optional] 
**ordinals_present** | **[float]** | The ordinals that are present for this column in the dataset. If the column is empty, will be empty array. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


