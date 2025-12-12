# DatasetChunk

Metadata for a chunk of an upload

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**chunk_number** | **int** |  | 
**column_count** | **int** | The number of columns in the chunk array, not including row headers. | 
**row_count** | **int** | The number of rows in the chunk array, not including column headers. | [optional] 
**created_at** | **int** | The Unix Timestamp in seconds when PUT /datasets/{id}/chunks/{chunk_number} was called. If &#x60;0&#x60; (Unix system time zero) then creation timestamp unavailable. This can happen for older dataset chunks.  | [optional] [readonly] 
**status** | **str** | Status of the dataset chunk during different stages of ingestion.  The chunk is set to &#39;uploading&#39; directly after chunk call and is awaiting to be processed.  The chunk is set to &#39;processing&#39; during ingestion into the datastore.  The chunk is set to &#39;uploaded&#39; once all processing tasks are finished.  If the chunk cannot be processed for any reason, status is set to failed.  | [optional] [readonly] 
**detail** | **str** | The error provided for why the dataset chunk failed to upload if an error occured during dataset chunk ingestion  | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


