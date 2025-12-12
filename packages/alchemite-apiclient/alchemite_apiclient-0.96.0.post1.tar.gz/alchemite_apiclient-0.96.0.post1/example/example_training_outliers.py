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
training_datset_outliers_file = "adrenergic_outliers.csv"
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

############################################################################
### Train the model with hyperparameter optimization
############################################################################
# Create a model record that will be trained on this dataset
model = {
    "name": model_name,
    "training_method": "alchemite",
    "training_dataset_id": dataset_id,
}
model_id = api_models.models_post(model=model)
print("Created model record:", model_id)

# Train the optimial model for this dataset
train_request = {
    "validation": "5-fold",
    # Setting enable_training_dataset_outliers=True will let us call
    # /models/{id}/training-dataset-outliers once the model is trained
    "enable_training_dataset_outliers": True,
}
response = api_models.models_id_train_put(model_id, train_request=train_request)
model = await_trained(lambda: api_models.models_id_get(model_id))
print("--- model hyperparameters ---")
print(model.training_hyperparameters)

############################################################################
### Get the training dataset outliers
############################################################################
response = api_models.models_id_training_dataset_outliers_put(model_id)
with open(training_datset_outliers_file, "w", encoding="UTF-8") as f:
    f.write(response)
