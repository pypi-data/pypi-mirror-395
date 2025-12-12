# InteractionPlotData

Data required to plot interactions for a column with respect to two other columns

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**x** | **[float]** | The x-axis coordinates that contain points from the dataset | 
**y** | **[float]** | The y-axis coordinates that contain points from the dataset | 
**xi** | **[float]** | The x-axis coordinates for each bin | 
**yi** | **[float]** | The y-axis coordinates for each bin | 
**zi** | **[[float]]** | A grid of z-values values for every combination of xi and yi | 
**zi_uncertainties** | **[[float]]** | A grid of z-value uncertainties for every combination of xi and yi | 
**x_name** | **str** | The name of the x-axis column | 
**y_name** | **str** | The name of the y-axis column | 
**z_name** | **str** | The name of the z-axis column | 
**status** | **str** | The status of the interaction job | defaults to "done"

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


