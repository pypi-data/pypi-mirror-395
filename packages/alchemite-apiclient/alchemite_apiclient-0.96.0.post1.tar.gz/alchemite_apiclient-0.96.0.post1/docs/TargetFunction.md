# TargetFunction

Dictionary of (potentially multiple) targets to optimize against. The cost function for optimization can be considered to be 1 minus the probability of the given sample to achieve the targets.  The probability function, for each target, accounts for the prediction and the uncertainty in that prediction. Using multiple targets, the overall cost function is 1 minus the probability that all targets are achieved; this is the product of the individual target probabilities. The key value should be a made up name to give the defined target. When importance is specified, the importance factors are included as linear weights on the probabilities in log-probability space. Only certain columns can be included in the targetFunction:   - The target column cannot be empty in the training dataset used to create the model.   - Columns specified as setInputs cannot also be specified as a target column.   - If the target is also a descriptor column, then it must be specified either in the sampleDefinition or as a dependentColumn.   - If the target is a categorical column, then it cannot be also specified in the sampleDefinition. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


