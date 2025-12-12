# SuggestMissingDatasetID


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** | The ID of a dataset containing at least the columns present in targetColumns or sourceColumns. | 
**source_rows** | **[str]** | A list of row headers which all appear in the dataset corresponding to datasetID.  Suggested measurements will only be returned from these rows.  If not given then the suggestions may come from any row. | [optional] 
**source_columns** | **[str]** | A list of column headers which all appear in the model&#39;s training dataset.  Suggested measurements will only be returned from these columns.  Descriptor columns cannot be in sourceColumns.  If not given then suggestions will come from all non-descriptor columns.  The sourceColumns may or may not be distinct from the targetColumns. | [optional] 
**target_columns** | **[str]** | A list of column headers which all appear in the model&#39;s training dataset.  Suggested measurements will be targeted to best improve predictions for these columns.  Descriptor columns cannot be in targetColumns.  If not given then targetColumns will be treated as being all non-descriptor columns.  The targetColumns may or may not be distinct from the sourceColumns. | [optional] 
**exploration_exploitation** | **float** | The desired tradeoff between &#39;exploration&#39;, at 0, or &#39;exploitation&#39; at 1: * &#39;exploration&#39;: suggesting measurements to improve the model across a wide range of different input and output ranges * &#39;exploitation&#39;: suggesting measurements that the model in its current state thinks will give the highest model improvement; typically results in more localised suggestions than &#39;exploration&#39;  | [optional]  if omitted the server will use the default value of 1
**num_suggestions** | **int** | The maximum number of suggested measurements to return that will best improve predictions for the requested targetColumns. | [optional]  if omitted the server will use the default value of 1
**s_factor** | **float, none_type** | Where data is mostly missing, sFactor should take low values - when data is mostly complete, it should take higher values.  If not given or null then sFactor will be set automatically, which is generally recommended.  Adjusting sFactor can make significant differences to the suggestions returned. | [optional] 
**uncertainty_weight** | **float** | Weighting determining the importance of uncertainties for individual data points compared to inter-column relationships when calculating suggested measurements.  If 0 then only column relationships are used to produce suggestions, while if 1 then uncertainties are treated as more important. Deprecated, this parameter is no longer supported. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


