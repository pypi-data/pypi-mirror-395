# DRClusterDivergence

The divergence for every cluster, for every column in the dataset. Null cluster is ignored. Key is cluster label and the value is an object of column name to divergence.  Divergence computes how dissimilar two data distributions are to each other. The divergence is 0 if the two data distributions are identical and 1 if they differ completely. In this case, the divergence is computed between the data belonging to cluster and data not belonging to that cluster for a combination of every cluster and every column. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **[{str: (float,)}]** | The divergence for every cluster, for every column in the dataset. Null cluster is ignored. Key is cluster label and the value is an object of column name to divergence.  Divergence computes how dissimilar two data distributions are to each other. The divergence is 0 if the two data distributions are identical and 1 if they differ completely. In this case, the divergence is computed between the data belonging to cluster and data not belonging to that cluster for a combination of every cluster and every column.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


