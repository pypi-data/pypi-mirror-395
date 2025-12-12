# OpaqueColumnInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The unique name of the column. | 
**data_type** | **str** | An opaque column contains more complex data that relies on an extension to be interpreted. It is not used directly to create predictions. | defaults to "opaque"
**is_descriptor** | **bool** | Whether the column is a descriptor or not | [optional] 
**is_complete** | **bool** | Whether the column is complete or not | [optional] 
**read_only** | **bool** | Whether values can be set for this column in Alchemite operations | [optional]  if omitted the server will use the default value of False
**write_only** | **bool** | If true then this column must be provided for all Alchemite operations but will typically not be returned. | [optional]  if omitted the server will use the default value of False
**extension_source** | **str** | The name of the extension method that created this column | [optional] 
**data_subtype** | **str** | An optional subtype describing the type of data held in the opaque column | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


