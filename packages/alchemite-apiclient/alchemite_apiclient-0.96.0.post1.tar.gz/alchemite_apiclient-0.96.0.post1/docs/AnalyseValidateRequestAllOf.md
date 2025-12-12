# AnalyseValidateRequestAllOf


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**return_predictions** | **bool** | If true then the predicted values will be included in the response. If false only the analysis of those predictions will be returned | [optional]  if omitted the server will use the default value of True
**return_column_headers** | **bool** | If true then the predicted values, if returned, will include column headers on the first row. | [optional]  if omitted the server will use the default value of False
**virtual_experiment_validation** | **bool** | If true then only the values in descriptor columns will be used to make predictions | [optional]  if omitted the server will use the default value of False
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


