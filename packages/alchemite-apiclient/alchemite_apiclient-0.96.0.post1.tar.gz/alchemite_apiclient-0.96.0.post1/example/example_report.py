import csv
import time
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
dataset_file = "steels.csv"

# Provide a path for the report to be written to
report_file = "model_report.pdf"

# Define names for the dataset and model (they do not have to be unique)
dataset_name = "steels"
model_name = "steels"
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
### Upload a dataset with POST /datasets
############################################################################
with open(dataset_file, "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]

    # Get column headers to pass to POST /datasets
    row_count = len(rows) - 1

    # Get number of rows (excluding the row of column headers) to pass to POST /datasets
    column_headers = rows[0][1:]

# For each column say if it is a descriptor (input only) column.
# In this case there are 6 descriptor columns at the start of the dataset,
# so the list is 6 1's followed by an amount of 0's to get the list the
# same length as the number of column headers
descriptor_columns = [1] * 6 + [0] * (len(column_headers) - 6)

dataset = {
    "name": dataset_name,
    "row_count": row_count,
    "column_headers": column_headers,
    "descriptor_columns": descriptor_columns,
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
model = {
    "name": model_name,
    "training_method": "alchemite",
    "training_dataset_id": dataset_id,
}
model_id = api_models.models_post(model=model)
print("Created model record ID:", model_id)

# Start training the model using hyperparameter optimisation and validation
response = api_models.models_id_train_put(
    model_id,
    train_request={"hyperparameter_optimization": "TPE", "validation": "5-fold"},
)
print("Train response:", response)

# Wait until the model has finished training
await_trained(lambda: api_models.models_id_get(model_id))

# Get the model metadata
model = api_models.models_id_get(model_id)
print("--- model metadata ---")
print(model)

# Print hyperparameters that the model trained with
print("--- Hyperparameters ---")
print(model.training_hyperparameters)

############################################################################
### Generate a model report
############################################################################

# Poll endpoint until report is generated
response = api_models.models_id_report_get(model_id)
while len(response.read()) == 0:
    time.sleep(1)
    response = api_models.models_id_report_get(model_id)

response.seek(0)
with open(report_file, "wb") as f:
    f.write(response.read())
