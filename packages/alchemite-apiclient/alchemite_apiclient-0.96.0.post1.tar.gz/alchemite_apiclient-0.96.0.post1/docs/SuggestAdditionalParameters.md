# SuggestAdditionalParameters


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sample_definition** | [**SampleDefinition**](SampleDefinition.md) |  | 
**target_function** | [**TargetFunction**](TargetFunction.md) |  | 
**new_columns** | [**NewColumns**](NewColumns.md) |  | [optional] 
**dependent_columns** | [**DependentColumns**](DependentColumns.md) |  | [optional] 
**set_inputs** | [**SetInputs**](SetInputs.md) |  | [optional] 
**num_optimization_samples** | **int** | The number of optimization samples that will be considered. Defaults to &#x60;1000&#x60;. The maximum is set per user and defaults to &#x60;10000&#x60;.  | [optional]  if omitted the server will use the default value of 1000
**optimization_method** | **str** | The following **global optimization** methods are available: * &#x60;\&quot;TPE\&quot;&#x60;: Tree-structured Parzen Estimator * &#x60;\&quot;random\&quot;&#x60;: Random search  The following **local optimization** methods are available: * &#x60;\&quot;powell\&quot;&#x60;: Recommended local optimization method * &#x60;\&quot;nelder-mead\&quot;&#x60;, &#x60;\&quot;l-bfgs-b\&quot;&#x60;, &#x60;\&quot;bfgs\&quot;&#x60;, &#x60;\&quot;conjugate gradient\&quot;&#x60;, &#x60;\&quot;cobyla\&quot;&#x60;, &#x60;\&quot;slsqp\&quot;&#x60;, &#x60;\&quot;tnc\&quot;&#x60;: Other local optimization methods  &gt; NOTE: local optimization only supports the following &#x60;\&quot;sample definition\&quot;&#x60; types: &#x60;\&quot;continuous\&quot;&#x60;, &#x60;\&quot;continuous or zero\&quot;&#x60; and &#x60;\&quot;categorical\&quot;&#x60;  Defaults to &#x60;\&quot;TPE\&quot;&#x60;.  | [optional]  if omitted the server will use the default value of "TPE"
**unique_samples** | **bool** | If true only return one suggested measurement for each sample. If false then multiple suggestions may appear for the same sample. | [optional]  if omitted the server will use the default value of True
**exploration_exploitation** | **float** | The desired tradeoff between &#39;exploration&#39;, at 0, or &#39;exploitation&#39; at 1: * &#39;exploration&#39;: suggesting measurements to improve the model so that future suggestions may better meet the target parameters * &#39;exploitation&#39;: suggesting measurements that the model in its current state thinks will best meet the target parameters  | [optional]  if omitted the server will use the default value of 0.8
**source_columns** | **[str], none_type** | A list of column headers which all appear in the model&#39;s training dataset.  Suggested measurements will only be returned from these columns.  Descriptor columns cannot be in sourceColumns.  By default an empty array, in which case the sourceColumns will be same as targetColumns.  If null then all the non-descriptor columns will be treated as the sourceColumns. | [optional]  if omitted the server will use the default value of []
**target_columns** | **[str], none_type** | A list of column headers which all appear in the model&#39;s training dataset.  Suggested measurements will be targeted to best improve predictions for these columns.  Descriptor columns cannot be in targetColumns.  The targetColumns may or may not be distinct from the sourceColumns.  By default an empty array, in which case the targetColumns will be those columns that appear in the targetFunction.  If null then all the non-descriptor columns will be treated as the targetColumns. | [optional]  if omitted the server will use the default value of []
**num_suggestions** | **int** | The maximum number of suggested measurements to return that will best improve predictions for the requested targetColumns. | [optional]  if omitted the server will use the default value of 1
**s_factor** | **float, none_type** | Where data is mostly missing, sFactor should take low values - when data is mostly complete, it should take higher values.  If not given or null then sFactor will be set automatically, which is generally recommended.  Adjusting sFactor can make significant differences to the suggestions returned. | [optional] 
**uncertainty_weight** | **float** | Weighting determining the importance of uncertainties for individual data points compared to inter-column relationships when calculating suggested measurements.  If 0 then only column relationships are used to produce suggestions, while if 1 then uncertainties are treated as more important. Deprecated, this parameter is no longer supported. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


