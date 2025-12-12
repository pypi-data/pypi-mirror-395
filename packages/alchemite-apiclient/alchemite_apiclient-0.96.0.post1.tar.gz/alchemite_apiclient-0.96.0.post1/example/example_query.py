import csv

import pandas as pd

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration, await_uploaded, row_chunks

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
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

# Define a name for the dataset (does not have to be unique)
dataset_name = "adrenergic"
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

dataset_id = api_datasets.datasets_post(
    dataset={
        "name": dataset_name,
        "row_count": row_count,
        "column_headers": column_headers,
        "descriptor_columns": descriptor_columns,
        "complete_columns": complete_columns,
    }
)

# Upload the data in chunks of rows at a time
for chunk_number, chunk in enumerate(row_chunks(dataset_file, chunk_size)):
    response = api_datasets.datasets_id_chunks_chunk_number_put(
        dataset_id, chunk_number, body=chunk
    )
    print("Uploaded chunk", chunk_number)

# Say that we've finished uploading the dataset
api_datasets.datasets_id_uploaded_post(dataset_id)

# Wait for dataset to be processed
await_uploaded(lambda: api_datasets.datasets_id_get(dataset_id))
print("Uploaded dataset")

############################################################################
# Query dataset
############################################################################
query_result = api_default.query_v1_put(
    query_request={
        "type": "dataset",
        "id": dataset_id,
        "filters": {
            # Get rows from the dataset where the column LM has no value
            "LM": None,
            # AND where the column D is equal to 0
            "D": 0,
            # AND where the column A is <= 3
            "A": {"max": 3},
            # AND where the column B is > 300
            "B": {"min": 300, "inclusiveMin": False},
        },
        # Only return a subset of the columns in the dataset. An "exclude"
        # option is also available if we wanted to return all column in the
        # dataset except certain ones
        "columnSelection": {"include": ["A", "B", "C", "D", "E", "F", "LM"]},
        # sort by column E in descending order, then A in ascending
        "sort": [
            {"name": "E", "direction": "desc"},
            {"name": "A", "direction": "asc"},
        ],
    },
    # Get only the results 10-30 from the above query (so skip the first 10
    # and limit the number of results returned to 20)
    offset=10,
    limit=20,
)

# query_result is a dictionary
print(query_result)
print("Total number of rows matching filters:", query_result["total"])

# Can convert query_result to a pandas DataFrame if needed
query_df = pd.DataFrame(
    [{e["name"]: e["value"] for e in row.data} for row in query_result.result],
    index=[row.row_id for row in query_result.result],
)
print(query_df)
