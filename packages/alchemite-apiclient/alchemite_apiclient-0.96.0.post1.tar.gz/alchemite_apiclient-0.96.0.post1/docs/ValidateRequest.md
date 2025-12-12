# ValidateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**return_probability_distribution** | **bool** | If true then the full probability distribution for each prediction will be returned, if false then the predicted value and uncertainty derived from that distribution will be returned instead. | [optional]  if omitted the server will use the default value of False
**dataset_id** | **str** | The ID of a dataset to use to make predictions.  The dataset must have the same column headers as the model&#39;s training dataset.  Only one of &#39;datasetID&#39; and &#39;data&#39; should be provided. | [optional] 
**return_row_headers** | **bool** | If true then row headers will be returned in the response csv.  If true and the &#39;data&#39; property is given then it is required that the first column of csv data are row headers. | [optional]  if omitted the server will use the default value of False
**return_column_headers** | **bool** | If true then column headers will be returned in the response csv. | [optional]  if omitted the server will use the default value of False
**data** | **str** | An array of CSV data with column headers.  Only one of &#39;datasetID&#39; and &#39;data&#39; should be provided.  If returnRowHeaders is true then the first column of the CSV should contain the unique row headers which identify each row. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


