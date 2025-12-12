# DRUMAPReductionType


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | **str** | The method of dimensionality reduction to perform on the data. | defaults to "UMAP"
**dimensions** | **int** | The number of dimensions to reduce the data to. | [optional]  if omitted the server will use the default value of 2
**num_neighbours** | **int** | The number of nearest points considered to be related to the target point when evaluating similarities in the high-dimensional space. Selecting a low number will consider local point structure, whereas a high number will consider global point structure. This can help identify local or global trends across the data. | [optional]  if omitted the server will use the default value of 5
**minimum_distance** | **float** | The minimum distance between any two points in the dimensionality-reduced graph plot. | [optional]  if omitted the server will use the default value of 0.5

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


