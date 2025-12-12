import csv
from io import StringIO

import alchemite_apiclient as client
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
train_request = {"hyperparameter_optimization": "TPE", "validation": "5-fold"}
response = api_models.models_id_train_put(model_id, train_request=train_request)
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
### Use the model to predict the trendline for two columns
############################################################################
input_column = "Cr (chromium)"
output_column = "Electrical resistivity"
predict_trendline_request = {
    "inputColumn": input_column,
    "outputColumn": output_column,
    "binCount": 5,
}

response = api_models.models_id_predict_trendline_put(
    model_id, predict_trendline_request=predict_trendline_request
)

original_data = pd.read_csv(dataset_file, index_col=0)
plt.scatter(
    original_data[input_column],
    original_data[output_column],
    color="black",
)
plt.xlabel(input_column)
plt.ylabel(output_column)

trendline_x = np.array(response["x"])
trendline_y = np.array(response["y"])
trendline_uncertainties = np.array(response["uncertainties"])


plt.plot(trendline_x, trendline_y, color="blue")
plt.fill_between(
    trendline_x,
    trendline_y - trendline_uncertainties,
    trendline_y + trendline_uncertainties,
    color="gray",
    alpha=0.3,
)
plt.show()
