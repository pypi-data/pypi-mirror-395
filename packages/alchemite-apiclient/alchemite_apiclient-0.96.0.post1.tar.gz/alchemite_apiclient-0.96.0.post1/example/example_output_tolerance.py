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
# list of zeros of length equal to the number of column headers
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

############################################################################
### Make output tolerance request
############################################################################

# Build the output tolerance request with a mixture of fixed inputs, varied inputs and target outputs (where value is 'None')
# The target outputs for this request are the ones not present in the request:
# - C (carbon)
# - Young's modulus
# - Yield strength (elastic limit)
# - Tensile strength
# - Elongation
# - Fracture toughness
# - Thermal conductivity
output_tolerance_request = {
    "sampleDefinition": {
        "Mo (molybdenum)": {"type": "continuous", "range": [0.2, 0.44]},
        "Thermal expansion coefficient": {
            "type": "continuous",
            "range": [0, 3.76],
        },
        "Electrical resistivity": {"type": "continuous", "range": [4, 4.42]},
    },
    "setInputs": {
        "Cr (chromium)": 0.43,
        "Mn (manganese)": 0.63,
        "Ni (nickel)": 0.45,
        "Si (silicon)": 0.11,
        "Specific heat capacity": 480.72,
    },
    "numSamples": 5,
}

output_tolerance_response = api_models.models_id_output_tolerance_put(
    model_id,
    output_tolerance_request=output_tolerance_request,
)
print(output_tolerance_response)


############################################################################
### Make univariate output tolerance request
############################################################################

# Vary just one column at a time from the sampleDefinition and keep the others
# fixed
output_tolerance_univariate_response = (
    api_models.models_id_output_tolerance_univariate_put(
        model_id, output_tolerance_request=output_tolerance_request
    )
)
print(output_tolerance_univariate_response)
