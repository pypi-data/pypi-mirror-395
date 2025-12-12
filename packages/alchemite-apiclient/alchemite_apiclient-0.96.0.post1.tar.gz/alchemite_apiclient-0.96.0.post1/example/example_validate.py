import csv
import json
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
train_dataset_file = "adrenergic.csv"

# First 320 columns in this dataset are descriptor (input only) columns and are
# complete columns in the training dataset as well as any future datasets we ask
# the model to predict from.  The last 5 are normal columns
descriptor_columns = [1] * 320 + [0] * 5
complete_columns = descriptor_columns

# Define names for the dataset and model (they do not have to be unique)
dataset_name = "adrenergic dataset"
model_name = "adrenergic model"

# File to write the imputed training dataset to
output_validate_file = "adrenergic_validated.csv"

# Dataset to validate the final model against
holdout_dataset_file = "adrenergic_holdout.csv"

# Paths to write the predictions and analysis to
holdout_predictions_file = "adrenergic_holdout_output.csv"
holdout_analysis_file = "adrenergic_holdout_analysis.json"

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
with open(train_dataset_file, "r", encoding="UTF-8") as file:
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

# Get the metadata about this dataset
dataset_metadata = api_datasets.datasets_id_get(dataset_id)
print("--- dataset metadata ---")
print(dataset_metadata)

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
train_request = {"validation": "5-fold"}
response = api_models.models_id_train_put(model_id, train_request=train_request)
model = await_trained(lambda: api_models.models_id_get(model_id))
print("--- model hyperparameters ---")
print(model.training_hyperparameters)

############################################################################
### Get the overall median R^2 from the model metadata
############################################################################
model_dict = api_models.models_id_get(model_id).to_dict()
print("Median R^2 for model = %.4f" % model_dict["validation_r_squared"])

############################################################################
### Get the R^2 for each column via cross validation of the training dataset
############################################################################
# When a model is trained with validation="5-fold" or validation="80/20" the
# R^2 for each column is stored in the model metadata
print(json.dumps(model_dict["training_column_info"], indent=4))

############################################################################
### Use the model to re-predict values in a holdout set
############################################################################

with open(holdout_dataset_file, encoding="UTF-8") as f:
    holdout_data = f.read()

response = api_models.models_id_analyse_validate_put(
    model_id,
    analyse_validate_request={"data": holdout_data, "return_predictions": True},
)

### Write predictions to csv file
# The predictions aren't returned with a header row but we can add it here
header_row = (
    ["Row IDs"]
    + column_headers
    + ["Predicted " + c for c in column_headers]
    + ["Uncertainty " + c for c in column_headers]
)
with open(holdout_predictions_file, "w", encoding="UTF-8") as f:
    f.write(",".join(header_row) + "\n")
    f.write(response.predictions)

### Write analysis to json file
analysis = response.to_dict()
del analysis["predictions"]
with open(holdout_analysis_file, "w", encoding="UTF-8") as f:
    json.dump(analysis, f, indent=4)
