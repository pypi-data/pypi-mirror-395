# CalColExpression

An expression that evaluates to a numerical value. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lit** | **[float]** | A literal numerical value. The first argument must be a valid number  | [optional] 
**const** | **[str]** | A known constant value. The first argument must be one of &#x60;nan&#x60;, &#x60;pi&#x60; or &#x60;e&#x60;  | [optional] 
**ref** | **[str]** | A numeric value referenced by column name. The first argument must be the name of a column in the dataset  | [optional] 
**** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**ln** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**sin** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**cos** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**tan** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**asin** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**acos** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**atan** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**sinh** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**cosh** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**tanh** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**asinh** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**acosh** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**atanh** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**abs** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**sqrt** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**sum** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**product** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**min** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**max** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**avg** | [**[CalColExpression]**](CalColExpression.md) |  | [optional] 
**_if** | [**CalColBooleanExpression**](CalColBooleanExpression.md) |  | [optional] 
**then** | [**CalColExpression**](CalColExpression.md) |  | [optional] 
**_else** | [**CalColExpression**](CalColExpression.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


