# SampleDefCompositionAllOf


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Define the continuous columns and their ranges. Sum of lower bound values must be less than or equal to &#x60;total&#x60;. Sum of upper bound values must be greater than or equal to &#x60;total&#x60;. Columns defined here cannot be defined in another sampleDefinition type.  | 
**type** | **str** | Constrain two or more columns to sum up to &#x60;total&#x60;. Only supported for global optimization methods.  | defaults to "composition"
**total** | **float** | The value the columns defined in &#x60;values&#x60; should sum up to. If not specified, then no total constraint will be applied. Cannot be used in conjunction with totalRange. | [optional] 
**total_range** | **[float]** | The value the columns defined in &#x60;values&#x60; should sum between. If not specified, then no totalRange constraint will be applied. Cannot be used in conjunction with total. | [optional] 
**min** | **int** | The minimum columns defined in &#x60;values&#x60; to be non-zero. | [optional]  if omitted the server will use the default value of 0
**max** | **int** | The maximum columns defined in &#x60;values&#x60; to be non-zero. If not specified, it will default to the number of properties in &#x60;values&#x60; | [optional] 
**hard_limit** | **bool** | Whether min/max are strictly enforced. Unused if no min or max set.  | [optional]  if omitted the server will use the default value of False
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


