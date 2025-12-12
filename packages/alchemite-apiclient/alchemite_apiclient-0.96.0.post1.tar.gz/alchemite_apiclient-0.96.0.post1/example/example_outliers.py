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
dataset_name = "adrenergic"
model_name = "adrenergic"

# Path to write training dataset outliers to
output_outliers_file = "adrenergic_outliers_output.csv"
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
    "training_dataset_id": dataset_id,  # The ID of the dataset we want to train a model with
}
model_id = api_models.models_post(model=model)
print("model ID:", model_id)
response = api_models.models_id_train_put(model_id, train_request={})
model = await_trained(lambda: api_models.models_id_get(model_id))

################################################################################
### Identify outliers in the model's training dataset
################################################################################
outliers_request = {"dataset_id": dataset_id}
response = api_models.models_id_outliers_put(
    model_id, outliers_request=outliers_request
)
with open(output_outliers_file, "w", encoding="UTF-8") as f:
    f.write(response)

### Delete model and dataset
api_models.models_id_delete(model_id)
api_datasets.datasets_id_delete(dataset_id)
