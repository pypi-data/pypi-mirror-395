# ValidationSplit


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_row_ids** | **[str]** | The row IDs from the training dataset to validate the sub-model against. | 
**name** | **str** | The name of this split, used in &#x60;validation-predictions&#x60; to identify which set each prediction came from. If not provided the index of the split will be used. If provided, each split&#39;s name must be distinct  | [optional] 
**train_row_ids** | **[str]** | The row IDs from the training dataset to train the validation model on.  If omitted, is the complement of the testRowIDs in respect to the training dataset.  No elements of the test set may be present in the training set.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


