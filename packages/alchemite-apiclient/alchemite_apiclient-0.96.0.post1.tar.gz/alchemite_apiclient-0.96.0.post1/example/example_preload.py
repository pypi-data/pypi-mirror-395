import csv
import time
from io import StringIO
from statistics import mean

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
dataset_name = "adrenergic"
model_name = "adrenergic"

# Path to dataset to impute
impute_input_file = "adrenergic_row.csv"
#######################

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(
    f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})"
)
print("------------------------------------------")

################################################################################
### Upload the dataset and train a basic model
################################################################################
with open(dataset_file, "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]
    row_count = len(rows) - 1
    column_headers = rows[0][1:]

dataset = {
    "name": dataset_name,
    "row_count": row_count,  # Number of rows (not including column headers)
    "column_headers": column_headers,  # Number of column headers
    "descriptor_columns": descriptor_columns,
    "complete_columns": complete_columns,
    "data": data,
}
dataset_id = api_datasets.datasets_post(dataset=dataset)
print("dataset ID:", dataset_id)
model = {
    "name": model_name,
    "training_method": "alchemite",  # Must always be 'alchemite' right now
    "training_dataset_id": dataset_id,  # The ID of the dataset to train the model pn
}
model_id = api_models.models_post(model=model)
print("model ID:", model_id)
response = api_models.models_id_train_put(model_id, train_request={})
model = await_trained(lambda: api_models.models_id_get(model_id))


################################################################################
### Load the model into memory on the server and impute
################################################################################
print(model)

# Load model into memory
load_request = {
    # If a loaded model is idle for 'timeout' seconds then it will unload itself
    "timeout": 600
}
response = api_models.models_id_load_post(model_id, load_request=load_request)
print(response)

# This impute response will block until the model is loaded
impute_request = {
    "return_probability_distribution": False,
    "return_column_headers": True,
    "data": open(impute_input_file).read(),
}
response = api_models.models_id_impute_put(model_id, impute_request=impute_request)
print(response)


# Time how long the imputation takes
def time_impute():
    ts = []
    for i in range(10):
        t0 = time.time()
        api_models.models_id_impute_put(model_id, impute_request=impute_request)
        t1 = time.time()
        ts.append(t1 - t0)
        print("Run", i, "time (s)", ts[-1])
    print(
        "Time to impute: min",
        min(ts),
        "max",
        max(ts),
        "mean",
        mean(ts),
    )


print("Model loaded:", api_models.models_id_get(model_id).loaded)
time_impute()

################################################################################
### Manually unload model and impute again
################################################################################
api_models.models_id_unload_put(model_id)
print("Model loaded:", api_models.models_id_get(model_id).loaded)
time_impute()

################################################################################
### Delete model and dataset
################################################################################
api_models.models_id_delete(model_id)
api_datasets.datasets_id_delete(dataset_id)
