# OutputToleranceRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sample_definition** | [**OTSampleDefinition**](OTSampleDefinition.md) |  | 
**set_inputs** | [**OTSetInputs**](OTSetInputs.md) |  | 
**num_samples** | **int** | The number of predictions to make during the exploration of the input range space. If using categorical values in the sampleDefinition, numSamples must be at least the length of the largest list of values. This is to ensure all categorical values are samples at least once. If using only categoricals in the sampleDefinition, if all possible combinations of categorical values can be achieved before hitting the value of numSamples, then only this many will be returned. This is to avoid re-sampling combinations that have already been seen as the results will be identical. Neither the sampleDefinition nor the setInputs may contain a calculated column  | [optional]  if omitted the server will use the default value of 500

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


