# SuggestMissingSpecific


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_columns** | **[str]** | A list of column headers which all appear in the model&#39;s training dataset.  Suggested measurements will only be returned from these columns.  Descriptor columns cannot be in sourceColumns.  If not given then suggestions will come from all non-descriptor columns.  The sourceColumns may or may not be distinct from the targetColumns. | [optional] 
**target_columns** | **[str]** | A list of column headers which all appear in the model&#39;s training dataset.  Suggested measurements will be targeted to best improve predictions for these columns.  Descriptor columns cannot be in targetColumns.  If not given then targetColumns will be treated as being all non-descriptor columns.  The targetColumns may or may not be distinct from the sourceColumns. | [optional] 
**exploration_exploitation** | **float** | The desired tradeoff between &#39;exploration&#39;, at 0, or &#39;exploitation&#39; at 1: * &#39;exploration&#39;: suggesting measurements to improve the model across a wide range of different input and output ranges * &#39;exploitation&#39;: suggesting measurements that the model in its current state thinks will give the highest model improvement; typically results in more localised suggestions than &#39;exploration&#39;  | [optional]  if omitted the server will use the default value of 1
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


