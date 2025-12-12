# ImportanceRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**output_columns** | **[str]** | A list of the training dataset&#39;s column names to include, in the list&#39;s order, as rows in the CSV response.  If not given then all the columns in the training dataset will be included in the order of the model&#39;s &#x60;trainingColumnHeaders&#x60; property. | [optional] 
**input_columns** | **[str]** | A list of the training dataset&#39;s column names to include, in the list&#39;s order, as columns in the CSV response.  If not given then all the columns in the training dataset will be included in the order of the model&#39;s &#x60;trainingColumnHeaders&#x60; property. | [optional] 
**use_only_descriptors** | **bool** | A boolean flag that will return the importance values considering only descriptor-to-target relationships if set to true. Otherwise, target-to-target importance will also be considered. | [optional]  if omitted the server will use the default value of False

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


