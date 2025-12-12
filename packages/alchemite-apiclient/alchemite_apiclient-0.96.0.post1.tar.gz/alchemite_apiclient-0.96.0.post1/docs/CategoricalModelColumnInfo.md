# CategoricalModelColumnInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The unique name of the column. | 
**categories_present** | **[str]** | The categories that are present for this column in the dataset. If the column is empty, will be empty array. | 
**mode** | **str, none_type** | The mode of the values appearing in this column in the dataset. If the column is empty, will be set to null. | 
**data_type** | **str** |  | defaults to "categorical"
**num_samples** | **int** | The number of non-missing values appearing in this column in the dataset. | defaults to 0
**is_descriptor** | **bool** | Whether the column is a descriptor or not | [optional] 
**is_complete** | **bool** | Whether the column is complete or not | [optional] 
**read_only** | **bool** | Whether values can be set for this column in Alchemite operations | [optional]  if omitted the server will use the default value of False
**write_only** | **bool** | If true then this column must be provided for all Alchemite operations but will typically not be returned. | [optional]  if omitted the server will use the default value of False
**extension_source** | **str** | The name of the extension method that created this column | [optional] 
**mcc** | **float, none_type** | The mean square contingency coefficient for this categorical column in the dataset.  In the case of 5-fold validation this is the mean average for the column across the 5 validation datasets.  Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor or there is no variation in the column&#39;s values. | [optional] 
**coefficient_of_determination** | **float, none_type** | The coefficient of determination for this column in the dataset.  In the case of 5-fold validation this is the mean average for the column across the 5 validation datasets.  Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor or there is no variation in the column&#39;s values. | [optional] 
**f1** | **float, none_type** | The F1 Score for this categorical column in the dataset. Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor. | [optional] 
**ppv** | **float, none_type** | The Positive Predictive Value (PPV/precision) for this categorical column in the dataset. Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor. | [optional] 
**tpr** | **float, none_type** | The True Positive Rate (TPR/recall) for this categorical column in the dataset. Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor. | [optional] 
**acc** | **float, none_type** | The Accuracy (ACC) for this categorical column in the dataset. Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor. | [optional] 
**ckc** | **float, none_type** | The Cohen&#39;s Kappa Coefficient (CKC) for this categorical column in the dataset. Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor. | [optional] 
**targeted_metric** | **float, none_type** | The value of the targeted metric for this column in the dataset. Null if the model was trained with &#x60;validation&#x60; set to &#x60;none&#x60; or if the column is a descriptor, and not present if targets were not set for this column during training. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


