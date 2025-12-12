# QueryRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filters** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Filter on dataset columns. Filtering a column on &#x60;null&#x60;, e.g. &#x60;{\&quot;my_column\&quot;: null}&#x60;, will return rows where the column has no value, i.e. is empty. Note that currently each filter is AND&#39;ed. Currently only &#x60;null&#x60; filtering can be applied on vector columns.  | [optional] 
**column_selection** | **bool, date, datetime, dict, float, int, list, str, none_type** | Select which columns to return. If not given than all columns will be returned.  | [optional] 
**sort** | [**[DatasetQueryRequestSort]**](DatasetQueryRequestSort.md) | Sort result by the dataset column values. This sorts everything by the first column in list first, and then by the subsequent column whenever the previous column has two or  more equal values, i.e. to break ties. If not set, the order is unknown but will be consistent across equal queries. It&#39;s currently not possible to sort on vector columns.  | [optional] 
**row_ids** | [**DatasetQueryRequestRowIDs**](DatasetQueryRequestRowIDs.md) |  | [optional] 
**type** | **str** |  | [optional]  if omitted the server will use the default value of "dataset"
**id** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


