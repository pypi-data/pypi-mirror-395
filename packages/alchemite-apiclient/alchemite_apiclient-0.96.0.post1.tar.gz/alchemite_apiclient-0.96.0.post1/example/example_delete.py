import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

model_id_to_delete = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(
    f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})"
)
print("------------------------------------------")

# Can iterate through all models and delete a model with a particular ID.
# IDs are unique to each model and dataset so this guarantees we only delete
# the one model we want.
for model in api_models.models_get():
    if model.id == model_id_to_delete:
        print("deleting", model.id, model.name)
        api_models.models_id_delete(model.id)

# Datasets can also be deleted in a similar way
dataset_id_to_delete = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
for dataset in api_datasets.datasets_get():
    if dataset.id == dataset_id_to_delete:
        print("deleting", dataset.id, dataset.name)
        api_datasets.datasets_id_delete(dataset.id)
