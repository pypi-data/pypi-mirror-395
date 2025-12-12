# AdditiveSensitivityRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_point** | [**[ColumnValueNullable]**](ColumnValueNullable.md) | A single point in your parameter space described by an array of objects with key:value pairs representing the column names and their values. | 
**output_columns** | **[str]** | A list of the training dataset&#39;s column names to include, in the list&#39;s order, as rows in the CSV response.   If not given then all continuous target columns in the training dataset will be included in the order of appearance in the model&#39;s &#x60;trainingColumnHeaders&#x60; property.  Categorical and ordinal columns are currently not supported.  | [optional] 
**input_columns** | **[str]** | A list of the training dataset&#39;s column names to include, in the list&#39;s order, as columns in the CSV response.  If not given then all the columns in the training dataset will be included in the order of the model&#39;s &#x60;trainingColumnHeaders&#x60; property. | [optional] 
**origin** | [**[ModelsIdAdditiveSensitivityOrigin]**](ModelsIdAdditiveSensitivityOrigin.md) | An optional single point in your parameter space described by an array of objects with key:value pairs representing the column names and their values. It is used to set a baseline value for each column, which the additive sensitivity of the provided data point is calculated with respect to. For instance, the &#39;current best&#39; entry could be provided as a reference point to compare differences to a new data point. If no specific point is given, the mean/mode of the dataset will be used. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


