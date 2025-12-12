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

# Provide a path to the dataset to output sensitivity using the trained model
sensitivity_output_file = "steels_sensitivity.csv"

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
# In this case there are no descriptor columns so descriptor_columns is a
# list of zeros of length equal to the number of column headers
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

############################################################################
### Train a basic model without validaiton or hyperparameter optimization
############################################################################
# Create a model record from this dataset with POST /models.  Note that this
# doesn't train the model, we still need to call PUT /models/{model_id}/train
# to do that.
model = {
    "name": model_name,
    "training_method": "alchemite",  # Must always be 'alchemite' right now
    "training_dataset_id": dataset_id,  # The ID of the dataset to train the model pn
}
model_id = api_models.models_post(model=model)
print("Created model record ID:", model_id)

# Start training the model using default hyperparameters and no validation
response = api_models.models_id_train_put(model_id, train_request={})
print("Train response:", response)

# Wait until the model has finished training
model = await_trained(lambda: api_models.models_id_get(model_id))

# build the sensitivity request (we use mean of each col as an example)
sensitivity_request = {
    "dataPoint": [
        {"name": "C (carbon)", "value": 0.57},
        {"name": "Cr (chromium)", "value": 0.43},
        {"name": "Mn (manganese)", "value": 0.63},
        {"name": "Mo (molybdenum)", "value": 0.08},
        {"name": "Ni (nickel)", "value": 0.45},
        {"name": "Si (silicon)", "value": 0.11},
        {"name": "Young's modulus", "value": 208.57},
        {"name": "Yield strength (elastic limit)", "value": 368.61},
        {"name": "Tensile strength", "value": 494.52},
        {"name": "Elongation", "value": 28.9},
        {"name": "Fracture toughness", "value": 75.42},
        {"name": "Thermal conductivity", "value": 48.86},
        {"name": "Specific heat capacity", "value": 480.72},
        {"name": "Thermal expansion coefficient", "value": 11.89},
        {"name": "Electrical resistivity", "value": 19.21},
    ]
}

############################################################################
### Get the sensitivity matrix of each column based on our input data point
############################################################################
r = api_models.models_id_sensitivity_put(
    model_id, sensitivity_request=sensitivity_request
)
with open(sensitivity_output_file, "w", encoding="UTF-8") as f:
    f.write(r)
