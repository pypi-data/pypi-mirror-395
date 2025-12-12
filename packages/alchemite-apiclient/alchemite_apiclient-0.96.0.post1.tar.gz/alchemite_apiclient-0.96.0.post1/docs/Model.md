# Model

Metadata for a model

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**training_method** | **str** | The method used to train the model. | defaults to "alchemite"
**id** | **str** | Unique identifier for the model. | [optional] [readonly] 
**tags** | **[str]** | Optional tags to attach to the model | [optional] 
**notes** | **str** | An optional free field for notes about the dataset | [optional] 
**project_id** | **str** | The project this model belongs to. The user must have permission to see the respective project to set this value  | [optional] 
**status** | [**ModelStatus**](ModelStatus.md) |  | [optional] 
**revises_id** | **str** | The UUID of the model this revisesID (its parent). | [optional] 
**revision_ids** | **[str]** | The UUIDs of the models that are revisions of this model (its children). | [optional] [readonly] 
**training_method_version** | **str** | The version of the method used to train the model. | [optional] [readonly] 
**training_dataset_id** | **str** | ID of the dataset used to train the model. | [optional] 
**training_start_time** | **int** | The Unix Timestamp in seconds when the model status switched to &#39;training&#39; upon the last training request. Note that this will be just after hyperparameter optimization finishes, if that was requested.  | [optional] [readonly] 
**training_completion_time** | **int** | The Unix Timestamp in seconds when the model last completed training. | [optional] [readonly] 
**training_progress** | **float** | The percentage completion of the model training process. | [optional] [readonly] 
**hyperparameter_optimization_method** | **str** | The hyperparameter optimization method that was used to find the optimal hyperparameters to train the model on | [optional] [readonly] 
**bespoke_column_hyperparameters** | **bool** | Whether to use bespoke hyperparameters for each target column. If false, hyperparameters are shared between columns. Defaults to true. | [optional] [readonly] 
**hyperparameter_optimization_start_time** | **int** | The Unix Timestamp in seconds when the model last began hyperparameter optimization. | [optional] [readonly] 
**hyperparameter_optimization_completion_time** | **int** | The Unix Timestamp in seconds when the model last completed hyperparameter optimization. | [optional] [readonly] 
**hyperparameter_optimization_progress** | **float** | The percentage completion of the hyperparameter optimization process. | [optional] [readonly] 
**training_real_time** | **int** | The real-world time in seconds that Alchemite took to train the model. | [optional] [readonly] 
**training_cpu_time** | **int** | The CPU time in seconds that Alchemite took to train the model. | [optional] [readonly] 
**training_peak_memory_usage** | **int** | The peak amount of memory (specifically the resident set size) in bytes used while training the model. | [optional] [readonly] 
**training_hyperparameters** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | The hyperparameters in JSON format used to train the model. | [optional] [readonly] 
**training_column_headers** | **[str]** | The list of column headers in the order that the model was trained on (with descriptor columns first). | [optional] [readonly] 
**training_initial_column_headers** | **[str]** | The list of column headers that were initially uploaded, before extensions or calculated columns are applied. | [optional] [readonly] 
**training_column_info** | [**[ModelColumnInfo]**](ModelColumnInfo.md) | Additional information/statistics for each column, listed in the order that model was trained on (with descriptor columns first). | [optional] [readonly] 
**categorical_columns** | [**[CategoricalColumn], none_type**](CategoricalColumn.md) | The possible categorical values for each categorical column in the dataset the model was trained on | [optional] [readonly] 
**ordinal_columns** | [**[OrdinalColumn], none_type**](OrdinalColumn.md) | The possible ordinal values for each ordinal column in the dataset the model was trained on | [optional] [readonly] 
**file_size** | **int** | The size of the model in bytes. | [optional] [readonly] 
**validation_method** | [**ModelValidationMethods**](ModelValidationMethods.md) |  | [optional] 
**validation_metric** | **float, none_type** | The median of validation metrics (whether R^2 for continuous and ordinal columns, MCC for categorical columns, or the targeted metric when using targets during training) across the validation target columns in the validation set. | [optional] [readonly] 
**validation_r_squared** | **float, none_type** | Coefficient of determination, R^2, calculated as the median across the target columns in the validation set. Deprecated, use &#x60;validationMetric&#x60; instead for a measure of the overall fit of the model or the &#x60;trainingColumnInfo&#x60; to find the coefficient of determination for each column with continuous data. | [optional] [readonly] 
**validation_target_columns** | **[str], none_type** | A list of column names specifying the columns to use to calculate the model&#39;s validation metric.  Cannot include descriptor columns. | [optional] [readonly] 
**loaded** | **bool** | If true then the model has been loaded into memory and will be used to respond to impute requests.  If false then the model will only be loaded into memory at request time. | [optional] [readonly] 
**estimated_model_memory** | **int** | The expected memory footprint of the model in bytes. | [optional] [readonly] 
**virtual_training** | **bool** | If true then only the descriptor columns were used as input in the first iteration of training | [optional] [readonly] 
**permitted_column_relationships** | [**[ModelPermittedColumnRelationships], none_type**](ModelPermittedColumnRelationships.md) | An array of objects defining which columns the ML model is able to use or not use as inputs when modelling specific columns.  The \&quot;allow\&quot; and \&quot;disallow\&quot; arrays must contain distinct columns. They do not need to contain all columns in the dataset.  If columns are not allowed in either \&quot;allow\&quot; nor \&quot;disallow\&quot;, the model will use default behaviors:   - use all descriptors for all targets when virtualTraining is true.   - use all descriptors + targets when virtualTraining is false for all targets (except for the same target -&gt; target).  if virtualTraining is false:   This is equivalent to passing \&quot;allow\&quot;: list_of_all_columns for every column in the dataset.   Therefore, passing allow when virtualTraining is false has no effect on the model.   However, columns passed within \&quot;disallow\&quot; will have an effect.  if virtualTraining is true:   This is equivalent to passing \&quot;allow\&quot;: list_of_all_descriptors and passing \&quot;disallow\&quot; for all non descriptors.   Therefore, passing descriptor columns in the \&quot;allow\&quot; list has no effect on the model.   Similarly, passing non descriptor columns in the \&quot;disallow\&quot; list has no effect on the model.   However, columns passed within \&quot;allow\&quot; for non descriptors, and \&quot;disallow\&quot; for descriptors will have an effect.  Interaction with Measurement Groups:   If measurement groups are specified for the training dataset that are incompatible, a 400 response is returned.   This happens when a column defined in \&quot;name\&quot; and one or more columns defined in \&quot;allow\&quot; are part of the same measurement group.  | [optional] [readonly] 
**hyperopt_sample_request** | **int, none_type** | The maximum number of hyperparameter optimization samples used for training the model.  Training may stop before the specified amount of samples if an ideal set of hyperparameters if found early.   | [optional] [readonly] 
**virtual_experiment_validation** | **bool** | If true then only the descriptor columns were used to make predictions when computing the validation metric. | [optional] [readonly] 
**target_function** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] [readonly] 
**exploration_exploitation** | **float** | The exploration exploitation ratio used for training the model | [optional] [readonly]  if omitted the server will use the default value of 1
**training_dataset_outliers_job_id** | **str, none_type** | ID of the training outliers job | [optional] [readonly] 
**training_dataset_outliers_job_status** | **str, none_type** | Status of outliers training job | [optional] [readonly] 
**created_at** | **int** | The Unix Timestamp in seconds when POST /models was called. If &#x60;0&#x60; (Unix system time zero) then creation timestamp unavailable. This can happen for older models.  | [optional] [readonly] 
**shared_through** | **[str]** | If a model has been shared with the user then this will show through which group(s) it has been shared. Won&#39;t be set if the user requesting the resource owns it. Deprecated: Please use &#x60;sharing&#x60; to determine how the access for the model was achieved.  | [optional] [readonly] 
**sharing** | [**ModelSharing**](ModelSharing.md) |  | [optional] 
**detail** | **str** | The error provided by Alchemite for why the model failed to train if  an issue occurs during model creation  | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


