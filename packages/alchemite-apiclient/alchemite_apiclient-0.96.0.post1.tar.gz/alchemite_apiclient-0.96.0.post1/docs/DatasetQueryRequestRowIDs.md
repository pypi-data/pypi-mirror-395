# DatasetQueryRequestRowIDs


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | **[str]** | The row IDs to search for in the dataset | 
**strict_search** | **bool** | If true, given row IDs must exactly match those in the dataset to be returned. This search type is also case-sensitive. If false, any row IDs in the dataset containing any of the given values will be returned. | [optional]  if omitted the server will use the default value of False
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


