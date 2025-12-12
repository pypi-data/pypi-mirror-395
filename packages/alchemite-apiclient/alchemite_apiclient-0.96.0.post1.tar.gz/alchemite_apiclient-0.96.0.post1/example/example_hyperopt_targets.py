import csv
from io import StringIO

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, r2_score
from sklearn.metrics import matthews_corrcoef as mcc

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration, await_trained

configuration = Configuration(offline=True)
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

#### Configuration ####
# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Define names for the dataset and model (they do not have to be unique)
dataset_name = "heteroskedastic dataset"
model_name_targets = "heteroskedastic model with targets"
model_name_no_targets = "heteroskedastic model without targets"

# The objective we will try to minimize below is 0.01
objective = 0.01

#######################

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(
    f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})"
)
print("------------------------------------------")

############################################################################
### Upload the train and test datasets
############################################################################

with open("./heteroskedastic_train.csv", "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]
    row_count = len(rows) - 1
    column_headers = rows[0][1:]

dataset = {
    "name": dataset_name,
    "row_count": row_count,
    "column_headers": column_headers,
    "descriptor_columns": [1, 0],
    "complete_columns": [1, 0],
    "data": data,
}
dataset_train_id = api_datasets.datasets_post(dataset=dataset)
print("Uploaded dataset:", dataset_train_id)


with open("./heteroskedastic_test.csv", "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]
    row_count = len(rows) - 1
    column_headers = rows[0][1:]

dataset = {
    "name": dataset_name,
    "row_count": row_count,
    "column_headers": column_headers,
    "descriptor_columns": [1, 0],
    "complete_columns": [1, 0],
    "data": data,
}
dataset_test_id = api_datasets.datasets_post(dataset=dataset)
print("Uploaded dataset:", dataset_test_id)

# Get the metadata about this dataset
dataset_metadata = api_datasets.datasets_id_get(dataset_train_id)
print("--- dataset metadata ---")
print(dataset_metadata)

############################################################################
### Train the models with hyperparameter optimization
############################################################################
# Create model records that will be trained on this dataset
model_targets = {
    "name": model_name_targets,
    "training_method": "alchemite",
    "training_dataset_id": dataset_train_id,
}
model_id_targets = api_models.models_post(model=model_targets)
print("Created model record for model with targets:", model_id_targets)
model_no_targets = {
    "name": model_name_no_targets,
    "training_method": "alchemite",
    "training_dataset_id": dataset_train_id,
}
model_id_no_targets = api_models.models_post(model=model_no_targets)
print("Created model record for model without targets:", model_id_no_targets)

# Train the optimial model for this dataset
train_request = {
    # Use the TPE optimizer to search the space of training hyperparamters
    # for the model that best suits this dataset
    "hyperparameterOptimization": "TPE",
    # Use 5-fold cross validation to calculate the coefficient of
    # determination (R^2) for the model associated with each set of
    # candidate hyperparameters.  This R^2 contributes to a 'score' that
    # directs the hyperparameter optimiser.
    "validation": "5-fold",
    # Use virtual experiment validation to mimic the scenario where only
    # input values are available at test time
    "virtualTraining": True,
    "virtualExperimentValidation": True,
}
response = api_models.models_id_train_put(
    model_id_no_targets, train_request=train_request
)

train_request_targets = train_request | {
    # Set a target function to be good at predicting when the target value is below the objective
    "targetFunction": {
        "y_target": {"target": "y", "type": "below", "maximum": objective}
    }
}
response = api_models.models_id_train_put(
    model_id_targets, train_request=train_request_targets
)
model_no_targets = await_trained(lambda: api_models.models_id_get(model_id_no_targets))
model_targets = await_trained(lambda: api_models.models_id_get(model_id_targets))

############################################################################
### See how good we are at predicting below the objective value
############################################################################

for model_name, model_id in [
    [model_name_no_targets, model_id_no_targets],
    [model_name_targets, model_id_targets],
]:
    validations = api_models.models_id_validate_put(
        model_id,
        validate_request={
            "datasetID": dataset_test_id,
            "returnRowHeaders": True,
            "returnColumnHeaders": True,
        },
    )
    validation_df = pd.read_csv(StringIO(validations), index_col=0)
    y_true = validation_df.iloc[:, 1]
    y_pred = validation_df.iloc[:, 3]

    y_true_binary = np.where(y_true > objective, 1, 0)
    y_pred_binary = np.where(y_pred > objective, 1, 0)

    print(f"Model: {model_name}")
    print(f"Confusion matrix:\n{confusion_matrix(y_true_binary, y_pred_binary)}")
    print(f"MCC: {mcc(y_true_binary, y_pred_binary)}")
    print(f"R2: {r2_score(y_true, y_pred)}")
    print("")
