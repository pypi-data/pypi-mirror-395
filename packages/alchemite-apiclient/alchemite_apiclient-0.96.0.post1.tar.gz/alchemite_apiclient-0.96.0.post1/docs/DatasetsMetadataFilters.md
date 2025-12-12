# DatasetsMetadataFilters

Filter datasets based on their attributes. Note that currently each filter is AND'ed. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the dataset. Will return datasets with names containing a subset of this value | [optional] 
**status** | **str** |  | [optional] 
**tags** | **[str]** | Tags that the dataset contains | [optional] 
**row_count** | **bool, date, datetime, dict, float, int, list, str, none_type** | Number of rows in dataset | [optional] 
**column_count** | **bool, date, datetime, dict, float, int, list, str, none_type** | Number of columns in dataset | [optional] 
**groups** | **[str]** | A list of groups to fuzzy search for within the ones the dataset has been shared with All provided groups will need to match for a dataset to be returned  | [optional] 
**exact_groups** | **[str]** | The full path of groups the dataset has been shared with All provided groups will need to match for a dataset to be returned  | [optional] 
**search** | **str** | Will search over all valid fields for the dataset and return any datasets that contain the provided value | [optional] 
**dataset_ids** | **[str]** | Array of dataset IDs to fetch | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


