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

descriptor_columns = [1] * 6 + [0] * 9

# Define names for the dataset and model (they do not have to be unique)
dataset_name = "steels dataset"
model_name = "steels model"

# File to write the validation request put dataset to
output_validation_request_file = "steels_validation_request.csv"
#######################

# The targeted columns
columns = ["Specific heat capacity", "Electrical resistivity"]
#######################

# Check we can access the API by getting the version number
api_response = api_default.version_get()
print("------ API version -----")
print(api_response)

############################################################################
### Upload the dataset
############################################################################
with open(dataset_file, "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]
    row_count = len(rows) - 1
    column_headers = rows[0][1:]

dataset = client.Dataset(
    name=dataset_name,
    row_count=row_count,
    column_headers=column_headers,
    descriptor_columns=descriptor_columns,
    data=data,
)
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

# Get targeted columns from validation predictions
# For all columns, the "columns" key should be excluded
response = api_models.models_id_validation_predictions_put(
    model_id, training_validation_prediction_request={"columns": columns}
)

with open(output_validation_request_file, "w", encoding="UTF-8") as f:
    f.write(response)
