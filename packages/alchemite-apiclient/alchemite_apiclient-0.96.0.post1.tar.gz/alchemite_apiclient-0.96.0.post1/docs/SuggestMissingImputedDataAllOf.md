# SuggestMissingImputedDataAllOf


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**imputed_data** | **str** | A CSV string containing a dataset with the columns present in targetColumns or sourceColumns as well as the predictions and uncertainties for missing values in that dataset.  The CSV should contain one column of row headers plus three blocks of equally sized columns:   * The first row contains the column headers   * The first column contains the row headers   * The 1st third of columns after the row headers contains the original incomplete values.   * The 2nd third of columns after the row headers contains the predictions for the missing values.   * The 3rd third of columns after the row headers contains the uncertainties for the predicted values.  The first row of the CSV must contain column headers.  The column header for the row headers is not used. The column headers for the three other blocks of columns should be in one of two formats:   * the first block of column headers are the column headers appearing in the training dataset, the second block has predicted_ as a prefix and the third block has uncertainty_ as a prefix, as shown in the example   * the three blocks column headers will have no prefixes and be identical, for example, &#x60;,w,x,y,z,w,x,y,z,w,x,y,z&#x60;  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


