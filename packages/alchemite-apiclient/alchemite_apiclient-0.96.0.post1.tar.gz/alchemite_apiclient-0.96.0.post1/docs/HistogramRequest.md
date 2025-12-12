# HistogramRequest

A Customisable Histogram Request.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**min_bins** | **int** | The mininum number of bins to return. Must be equal to or below &#39;max_bins&#39;. | [optional]  if omitted the server will use the default value of 1
**max_bins** | **int** | The maxinum number of bins to return. Must be equal to or above &#39;min_bins&#39;. | [optional]  if omitted the server will use the default value of 30
**columns** | **[str]** | The columns to return the histogram for. If not given, will return the histogram for all columns. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


