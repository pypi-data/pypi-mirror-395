# DRModelReductionData


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_id** | **str** | The ID of the model associated with the dataset. Allows Alchemite to impute missing data and allows the use of any &#x60;optimize&#x60; or &#x60;suggest-additional&#x60; results to be the target of reduction. | 
**reduction_data_type** | **str** | The type of data to be reduced. &#x60;dataset&#x60; means the base dataset will be reduced. &#x60;optimize&#x60; means the optimize results for the dataset will be reduced. &#x60;suggest-additional&#x60; means the suggest-additional results for the dataset will be reduced. | 
**column_type** | **str** | The type of the columns being reduced. Reduction can be done on all descriptor columns, all target columns, or all columns in the data. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


