# DRJobReductionMetadata


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reduction_data_type** | **str** | The type of data that was reduced. &#x60;optimize&#x60; means the optimize results for the dataset were reduced. &#x60;suggest-additional&#x60; means the suggest-additional results for the dataset were reduced. | 
**method** | **str** | The method of dimensionality reduction performed on the data. | 
**sources** | [**[DRJobReductionMetadataSources]**](DRJobReductionMetadataSources.md) | The information necessary to find the corresponding row/result in the reductionData. This can help to identify notable points or clusters. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


