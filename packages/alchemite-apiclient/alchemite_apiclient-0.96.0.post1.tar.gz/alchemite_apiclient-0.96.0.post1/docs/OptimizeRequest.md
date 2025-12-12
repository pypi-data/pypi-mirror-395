# OptimizeRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sample_definition** | [**SampleDefinition**](SampleDefinition.md) |  | 
**target_function** | [**TargetFunction**](TargetFunction.md) |  | 
**new_columns** | [**NewColumns**](NewColumns.md) |  | [optional] 
**dependent_columns** | [**DependentColumns**](DependentColumns.md) |  | [optional] 
**set_inputs** | [**SetInputs**](SetInputs.md) |  | [optional] 
**num_optimization_samples** | **int** | The number of optimization samples that will be considered. Defaults to &#x60;1000&#x60;. The maximum is set per user and defaults to &#x60;10000&#x60;.  | [optional]  if omitted the server will use the default value of 1000
**optimization_method** | **str** | The following **global optimization** methods are available: * &#x60;\&quot;TPE\&quot;&#x60;: Tree-structured Parzen Estimator * &#x60;\&quot;random\&quot;&#x60;: Random search * &#x60;\&quot;alchemite\&quot;&#x60;: Use Alchemite&#39;s optimize method  &gt; The &#x60;\&quot;alchemite\&quot;&#x60; method only supports the &#x60;\&quot;continuous\&quot;&#x60; sample definition type.  The following **local optimization** methods are available: * &#x60;\&quot;local alchemite\&quot;&#x60;: Use Alchemite&#39;s local optimize method * &#x60;\&quot;powell\&quot;&#x60;: Recommended local optimization method * &#x60;\&quot;nelder-mead\&quot;&#x60;, &#x60;\&quot;l-bfgs-b\&quot;&#x60;, &#x60;\&quot;bfgs\&quot;&#x60;, &#x60;\&quot;conjugate gradient\&quot;&#x60;, &#x60;\&quot;cobyla\&quot;&#x60;, &#x60;\&quot;slsqp\&quot;&#x60;, &#x60;\&quot;tnc\&quot;&#x60;: Other local optimization methods  &gt; Local optimization only supports the following &#x60;\&quot;sample definition\&quot;&#x60; types: &#x60;\&quot;continuous\&quot;&#x60;, &#x60;\&quot;continuous or zero\&quot;&#x60; and &#x60;\&quot;categorical\&quot;&#x60;. The &#x60;\&quot;composition\&quot;&#x60; types can also be used for optimizationMethods &#x60;\&quot;cobyla\&quot;&#x60; and &#x60;\&quot;slsqp\&quot;&#x60;  &gt; The &#x60;\&quot;alchemite\&quot;&#x60; and &#x60;\&quot;local alchemite\&quot;&#x60; methods cannot be used with &#x60;dependentColumns&#x60;; models trained on datasets containing vectors or &#x60;calculatedColumns&#x60;; or &#x60;targetFunctions&#x60; other than &#x60;\&quot;between\&quot;&#x60;, &#x60;\&quot;below\&quot;&#x60; or &#x60;\&quot;above\&quot;&#x60;  | [optional]  if omitted the server will use the default value of "TPE"
**name** | **str** | Optional name to attach to the optimization. | [optional] 
**tags** | **[str]** | Optional tags to attach to the optimization. Array should contain unique strings. | [optional] 
**notes** | **str** | An optional free field for notes about the optimisation job. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


