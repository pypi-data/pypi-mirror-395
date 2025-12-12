import csv
from io import StringIO

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration, await_uploaded

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

#### Configuration ####
# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Provide path to the dataset to train a model from
dataset_file = "steels.csv"

# Define a name for the dataset
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

# Wait for dataset to be processed and get the metadata about this dataset
dataset_metadata = await_uploaded(lambda: api_datasets.datasets_id_get(dataset_id))
print("-------------Dataset Metadata-------------")
print(dataset_metadata)

############################################################################
### Make a histogram request
############################################################################
# Generate a histogram by calling PUT datasets/{id}/histogram with a request
# body.

# Call the histogram endpoint with default parameters, which will return the
# histogram for all columns in the dataset.
response = api_datasets.datasets_id_histogram_put(dataset_id)
print("--------Default Histogram Response--------")
print(response)

# Call Histogram with custom parameters
response = api_datasets.datasets_id_histogram_put(
    dataset_id,
    histogram_request={"minBins": 2, "maxBins": 10, "columns": ["Cr (chromium)"]},
)
print("--------Custom Histogram Response---------")
print(response)

# For a numerical column, here is how to get the same input as given by np.histogram
print("---------Histogram counts for Cr----------")
counts = response["Cr (chromium)"]["counts"]
histogram_min = response["Cr (chromium)"]["min"]
histogram_step = response["Cr (chromium)"]["step"]

bin_edges = [histogram_min + i * histogram_step for i in range(len(counts) + 1)]
for h_lb, h_hb, cnts in zip(bin_edges[:-1], bin_edges[1:], counts):
    print(f"Count for 'Cr (chromium)' between {h_lb} and {h_hb}: {cnts}")
