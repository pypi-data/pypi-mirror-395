import csv
from io import StringIO

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration, await_trained

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

#### Configuration ####
# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Provide path to the dataset to train a model from
dataset_file = "adrenergic.csv"

# First 320 columns in this dataset are descriptor (input only) columns and are
# complete columns in the training dataset as well as any future datasets we ask
# the model to predict from.  The last 5 are normal columns
descriptor_columns = [1] * 320 + [0] * 5
complete_columns = descriptor_columns

# Define names for the dataset and model (they do not have to be unique)
dataset_name = "adrenergic dataset"
model_name = "adrenergic model"

# File to write the imputed training dataset to
output_impute_file = "adrenergic_imputed.csv"
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
### Upload the dataset
############################################################################
with open(dataset_file, "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]
    row_count = len(rows) - 1
    column_headers = rows[0][1:]

dataset = {
    "name": dataset_name,
    "row_count": row_count,
    "column_headers": column_headers,
    "descriptor_columns": descriptor_columns,
    "complete_columns": complete_columns,
    "data": data,
}
dataset_id = api_datasets.datasets_post(dataset=dataset)
print("Uploaded dataset:", dataset_id)

# Get the metadata about this dataset
dataset_metadata = api_datasets.datasets_id_get(dataset_id)
print("--- dataset metadata ---")
print(dataset_metadata)

############################################################################
### Train the model with hyperparameter optimization
############################################################################
# Create a model record that will be trained on this dataset
model = client.Model(
    name=model_name,
    training_method="alchemite",
    training_dataset_id=dataset_id,
)
model_id = api_models.models_post(model=model)
print("Created model record:", model_id)

# Train the optimial model for this dataset
train_request = client.TrainRequest(
    # Use the TPE optimizer to search the space of training hyperparamters
    # for the model that best suits this dataset
    hyperparameter_optimization="TPE",
    # Use 5-fold cross validation to calculate the coefficient of
    # determination (R^2) for the model associated with each set of
    # candidate hyperparameters.  This R^2 contributes to a 'score' that
    # directs the hyperparameter optimiser.
    validation="5-fold",
)
response = api_models.models_id_train_put(model_id, train_request=train_request)
model = await_trained(lambda: api_models.models_id_get(model_id))

print("--- model hyperparameters ---")
print(model.training_hyperparameters)

############################################################################
### Impute the training dataset and write the output to a file
############################################################################
impute_request = client.ImputeRequest(
    # We can provide the ID of a dataset to be imputed, rather than
    # uploading the dataset itself.
    dataset_id=dataset_id,
    # Set return_row_headers=True so that the first column of the returned
    # CSV with imputed data are actually row headers.
    return_row_headers=True,
    return_column_headers=True,
)
response = api_models.models_id_impute_put(model_id, impute_request=impute_request)
with open(output_impute_file, "w", encoding="UTF-8") as f:
    f.write(response)
