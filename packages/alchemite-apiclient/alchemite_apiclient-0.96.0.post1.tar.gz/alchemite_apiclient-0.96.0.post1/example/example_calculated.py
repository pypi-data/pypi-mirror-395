import csv
from io import StringIO

import alchemite_apiclient as client

from alchemite_apiclient import calculated_columns as cc
from alchemite_apiclient.extensions import Configuration, await_trained

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

### Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

dataset_file = "steels.csv"
dataset_name = "steels calculated density"
model_name = "steels calculated density"
output_impute_file = "output_impute_categorical.csv"

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(
    f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})"
)
print("------------------------------------------")

############################################################################
### Upload a dataset
############################################################################
with open(dataset_file, "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]
    row_count = len(rows) - 1
    column_headers = rows[0][1:]

calculated_columns = [
    {
        "name": "Fe (iron)",
        # Calculate the remaining percentage of iron, by subtracting the sum of the other elements from 100%
        "expression": cc.literal(100) - cc.col_sum(column_headers[:6]),
    },
    {
        "name": "Average Molecular Mass",
        # Calculate the average molecular mass by multiplying the element percentage
        #    contribution by that element's moleculer mass
        "expression": (
            cc.weighted_sum(
                ["Fe (iron)", *column_headers[:6]],
                [55.845, 12.011, 51.996, 54.938, 95.95, 58.693, 28.085],
            )
            / cc.literal(100)
        ),
    },
]

dataset = {
    "name": dataset_name,
    "row_count": row_count,  # Number of rows (not including column headers)
    "column_headers": column_headers,
    "descriptor_columns": [1] * 6 + [0] * (len(column_headers) - 6),
    "data": data,
    "calculated_columns": calculated_columns,
}
dataset_id = api_datasets.datasets_post(dataset=dataset)
print("dataset ID:", dataset_id)

############################################################################
### Get the metadata about this dataset
############################################################################
dataset_metadata = api_datasets.datasets_id_get(dataset_id)
print("\n--- dataset metadata ---")
print(dataset_metadata)

calculated_dataset = api_datasets.datasets_id_download_get(dataset_id)
print(calculated_dataset)

############################################################################
### Create a model from this dataset
############################################################################
# POST the model
model = {
    "name": model_name,
    "training_method": "alchemite",
    "training_dataset_id": dataset_id,
}
model_id = api_models.models_post(model=model)
print("model ID:", model_id)

############################################################################
### Start training the model
############################################################################
# No hyperparameter optimisation, therefore default hyperparameters used
response = api_models.models_id_train_put(model_id, train_request={})
print(response)
model = await_trained(lambda: api_models.models_id_get(model_id))

############################################################################
### Get the model metadata
############################################################################
model = api_models.models_id_get(model_id)
print("\n--- model metadata ---")
print(model)

training_column_headers = model.training_column_headers

############################################################################
### Print hyperparameters
############################################################################
print("\n--- Hyperparameters ---")
print(model.training_hyperparameters)

# Delete model and dataset
# api_models.models_id_delete(model_id)
# api_datasets.datasets_id_delete(dataset_id)
