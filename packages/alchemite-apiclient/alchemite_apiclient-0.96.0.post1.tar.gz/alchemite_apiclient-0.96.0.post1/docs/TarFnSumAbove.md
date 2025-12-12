# TarFnSumAbove


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**minimum** | **float** |  | 
**targets** | **[str]** | Array of columns names to sum | 
**type** | **str** | Find a solution where the sum of the given columns is above &#x60;\&quot;minimum\&quot;&#x60;. | defaults to "sum above"
**importance** | **float** | The higher the value the higher the importance of this target.  If the importance values all equal 1 then the &#x60;probabilityOfSuccess&#x60; is a true probability (the probability of all the targets being satisfied, assuming that the probability of any individual target being satisfied is independent of the others).  Note, having many targets or importance numbers &gt; 1 can make the &#x60;probabilityOfSuccess&#x60; very small, even if most of the targets are individually likely to be met. If there are many targets it may be helpful to make the importance values all add up to 1. This will make the &#x60;probabilityOfSuccess&#x60; scale with the number of columns so that it becomes a more natural-looking \&quot;score\&quot; of how likely the targets are to be met. For example, the reported &#x60;probabilityOfSuccess&#x60; of achieving one target with probability 50% is the same as achieving two targets, each with probability 50% and importance 0.5.  | [optional]  if omitted the server will use the default value of 1
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


