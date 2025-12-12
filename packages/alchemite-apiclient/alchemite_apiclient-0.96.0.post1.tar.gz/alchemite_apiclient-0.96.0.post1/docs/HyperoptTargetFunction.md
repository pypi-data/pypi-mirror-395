# HyperoptTargetFunction

Dictionary of (potentially multiple) targets to optimize model performance against. Each target aims to match the probability of achieving the specified targets using the model predictions or using the real provided data. Values that are both predicted to be well above/below the target, and whose true values actually are well above/below the target, are downweighted  relative to values where the true and predicted values lie on different sides of the target value (as these indicate the model will be poor at predicting whether a given value will achieve the target or not). For categorical targets this is effectively equivalent to the two-class classification problem using the included/excluded categories in the target function: for continuous targets the target function becomes a mixture between a classification and regression target. Only non-descriptor columns can be included in the target function. If validationTargetColumns are set, the targets set in the targetFunction must be a subset of the validationTargetColumns. Currently the importance factor is ignored, but included for compatability with optimize/suggest-additional/suggest-historic target functions. Currently only single-column targets are supported. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


