# SensitivityRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_point** | [**[ColumnValue]**](ColumnValue.md) | A single point in your parameter space described by an array of objects with key:value pairs representing the column names and their values. Every column in the model&#39;s training dataset must have a value. | 
**output_columns** | **[str]** | A list of the training dataset&#39;s column names to include, in the list&#39;s order, as rows in the CSV response.   If not given then all continuous target columns in the training dataset will be included in the order of appearance in the model&#39;s &#x60;trainingColumnHeaders&#x60; property.  Categorical and ordinal columns are currently not supported.  | [optional] 
**input_columns** | **[str]** | A list of the training dataset&#39;s column names to include, in the list&#39;s order, as columns in the CSV response.  If not given then all the columns in the training dataset will be included in the order of the model&#39;s &#x60;trainingColumnHeaders&#x60; property. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


