# DRDatasetReductionMetadata


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | **str** | The method of dimensionality reduction performed on the data. | 
**sources** | [**[DRDatasetReductionMetadataSources]**](DRDatasetReductionMetadataSources.md) | The information necessary to find the corresponding row/result in the reductionData. This can help to identify notable points or clusters. | 
**reduction_data_type** | **str** | The type of data that was reduced. &#x60;dataset&#x60; means the base dataset underwent the reduction. | defaults to "dataset"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


