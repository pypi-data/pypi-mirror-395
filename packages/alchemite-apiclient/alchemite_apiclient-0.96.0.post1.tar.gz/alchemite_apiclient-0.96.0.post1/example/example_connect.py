import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

api_default = client.DefaultApi(client.ApiClient(configuration))

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(
    f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})"
)
print("------------------------------------------")
