import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

dataset_id_to_download = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(
    f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})"
)
print("------------------------------------------")

r = api_datasets.datasets_id_download_get(dataset_id_to_download)
with open(dataset_id_to_download + ".csv", "w", encoding="UTF-8") as f:
    f.write(r)
