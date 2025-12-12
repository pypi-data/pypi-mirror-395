import csv

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration, row_chunks

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

#### Configuration ####
# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Provide path to the dataset to train a model from
dataset_file = "adrenergic.csv"

# The number of rows to upload at once
chunk_size = 500

# First 320 columns in this dataset are descriptor (input only) columns and are
# complete columns in the training dataset as well as any future datasets we ask
# the model to predict from.  The last 5 are normal columns
descriptor_columns = [1] * 320 + [0] * 5
complete_columns = descriptor_columns

# Define names for the dataset (they do not have to be unique)
dataset_name = "chunked adrenergic"
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
### Upload the dataset in chunks
############################################################################
# Call POST /datasets to create the dataset record but don't pass it the
# 'data' argument.  We'll upload the data later.
with open(dataset_file, "r", encoding="UTF-8") as file:
    reader = csv.reader(file, delimiter=",")
    column_headers = next(reader)[1:]
    for row_index, _ in enumerate(reader):
        pass
    row_count = row_index + 1

dataset = {
    "name": dataset_name,
    "row_count": row_count,
    "column_headers": column_headers,
    "descriptor_columns": descriptor_columns,
    "complete_columns": complete_columns,
}

dataset_id = api_datasets.datasets_post(dataset=dataset)
print("Created dataset record:", dataset_id)
print("--- dataset metadata before upload ---")
print(api_datasets.datasets_id_get(dataset_id))

# Upload the data in chunks of rows at a time
for chunk_number, chunk in enumerate(row_chunks(dataset_file, chunk_size)):
    response = api_datasets.datasets_id_chunks_chunk_number_put(
        dataset_id, chunk_number, body=chunk
    )
    print("Uploaded chunk", chunk_number)

# Show all the chunks
response = api_datasets.datasets_id_chunks_get(dataset_id)
print("Chunks:", response)

# Say that we've finished uploading the dataset
api_datasets.datasets_id_uploaded_post(dataset_id)
print("Uploaded dataset")
print("--- dataset metadata after upload ---")
print(api_datasets.datasets_id_get(dataset_id))
