import csv
from io import StringIO

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration

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
    row_count = len(rows) - 1
    column_headers = rows[0][1:]

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

# Get the metadata about this dataset
dataset_metadata = api_datasets.datasets_id_get(dataset_id)
print("--- dataset metadata ---")
print(dataset_metadata)

############################################################################
### Create column groups for the dataset
############################################################################

column_groups_batch_post_request = {
    "columnGroups": [
        {
            "name": "Element Inputs (incomplete)",
            "columns": [
                "C (carbon)",
                "Cr (chromium)",
                "Mn (manganese)",
                "Mo (molybdenum)",
            ],
        },
        {
            "name": "Strength Targets",
            "columns": [
                "Yield strength (elastic limit)",
                "Tensile strength",
                "Fracture toughness",
            ],
        },
        {
            "name": "Temperature Targets",
            "columns": [
                "Thermal conductivity",
                "Specific heat capacity",
                "Thermal expansion coefficient",
            ],
        },
    ]
}

column_group_ids = api_datasets.datasets_id_column_groups_batch_post(
    dataset_id,
    column_groups_batch_post_request,
)

column_groups = api_datasets.datasets_id_column_groups_get(
    dataset_id,
)

print("--- uploaded column groups ---")
print(column_groups)

############################################################################
### Modify and fetch column group for the dataset
############################################################################

column_group_id = column_group_ids[0]
api_datasets.datasets_id_column_groups_column_group_id_patch(
    dataset_id,
    column_group_id,
    column_group_patch_request={
        "name": "Element Inputs",
        "columns": [
            "C (carbon)",
            "Cr (chromium)",
            "Mn (manganese)",
            "Mo (molybdenum)",
            "Ni (nickel)",
            "Si (silicon)",
        ],
    },
)

modified_column_group = api_datasets.datasets_id_column_groups_column_group_id_get(
    dataset_id,
    column_group_id,
)

print("--- new column group ---")
print(modified_column_group)

# Delete column groups and dataset
# for cg_id in column_group_ids:
#     api_datasets.datasets_id_column_groups_column_group_id_delete(
#         dataset_id,
#         cg_id,
#     )
# api_datasets.datasets_id_delete(dataset_id)
