# ModelsIdTrainPermittedColumnRelationships


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | the name of the column for which the allow/disallow values are applied. | 
**allow** | **[str]** | array of column names the ML model is able to use to model the column specified by \&quot;name\&quot;. | 
**disallow** | **[str]** | makes the columns present in the array inaccessible to the model for modelling the column specified by \&quot;name\&quot;. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


