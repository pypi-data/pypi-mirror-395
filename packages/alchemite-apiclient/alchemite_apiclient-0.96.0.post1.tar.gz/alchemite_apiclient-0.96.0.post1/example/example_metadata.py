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
dataset_file = "steels.csv"

# Provide a path to the dataset to impute using the trained model
impute_input_file = "steels_impute.csv"

# Define names for the dataset and model (they do not have to be unique)
dataset_name = "steels"
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

descriptor_columns = [0] * len(column_headers)

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
### Train some models using the dataset
############################################################################
for model_name in ["Steels Model 1", "Steels Model 2", "Steels Model 3"]:
    model = {
        "name": model_name,
        "training_method": "alchemite",
        "training_dataset_id": dataset_id,
    }
    model_id = api_models.models_post(model=model)
    print("Created model record ID:", model_id)

    # Start training the model using default hyperparameters and no validation
    response = api_models.models_id_train_put(
        model_id, train_request={"validation": "5-fold"}
    )
    print("Train response:", response)

    # Wait until the model has finished training
    await_trained(lambda: api_models.models_id_get(model_id))

############################################################################
### Construct a query to fetch the models
############################################################################
request = {
    "sort": [{"name": "createdAt", "direction": "asc"}],
    "filters": {
        # "search": "steels",
        "name": "Steels Model 1",
        # "status": "trained",
        # "validationMetric": {"min": 0},
        # "validationMethod": "5-fold",
        # "virtualTraining": False,
        # "virtualExperimentValidation": False,
        # "trainingCompletionTime": {"max": 2147483647},
        # "trainingMethodVersion": "20230728",
        # "groups": ["Group 1", "Group 2"],
        # "createdAt": {"max": 2147483647},
        # "tags": ["My Tag"],
    },
}

query_models = api_models.models_metadata_put(
    model_query=request,
    limit=20,
    offset=0,
)
print("--- models ---")
print(query_models)
