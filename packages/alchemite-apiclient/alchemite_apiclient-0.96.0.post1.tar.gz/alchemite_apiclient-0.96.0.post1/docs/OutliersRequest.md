# OutliersRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** | The ID of a dataset to check for outliers.  The dataset must have the same column headers as the model&#39;s training dataset.  Only one of &#39;datasetID&#39; and &#39;data&#39; should be provided. | [optional] 
**data** | **str** | An array of CSV data with column headers.  Only one of &#39;datasetID&#39; and &#39;data&#39; should be provided. | [optional] 
**outlier_tolerance** | **float** | How many standard deviations from a prediction results in a value being classified as an outlier. | [optional]  if omitted the server will use the default value of 1.0
**return_row_headers** | **bool** | If true then a &#39;Row&#39; column, containing the name of the row the outlier is on, will be included in the response CSV.  If true and the &#39;data&#39; property is given then it is required that the first column of the input CSV contains the row headers. | [optional]  if omitted the server will use the default value of False

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


