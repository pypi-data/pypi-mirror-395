# DependentColumns

Define any dependent columns that exist in the dataset. Categorical columns cannot be dependant on other columns, nor can they have columns depending on them. The dependent column cannot also appear in the sampleDefinition nor setInputs, although this is not true for the 'zero if zero' case. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Define any dependent columns that exist in the dataset. Categorical columns cannot be dependant on other columns, nor can they have columns depending on them. The dependent column cannot also appear in the sampleDefinition nor setInputs, although this is not true for the &#39;zero if zero&#39; case.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


