import json

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration, await_job

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))

### Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

suggest_initial_args_path = "suggest_initial_args.json"

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(
    f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})"
)
print("------------------------------------------")


############################################################################
### Make a suggest initial request
############################################################################
print("\n--- Suggest-initial ---")

# Get suggest initial input arguments
with open(suggest_initial_args_path, encoding="UTF-8") as f:
    suggest_initial_args = json.load(f)

# Send suggest_initial request
suggest_initial_job_id = api_default.suggest_initial_post(**suggest_initial_args)
print("suggest_initial job ID:", suggest_initial_job_id)


# Wait until the suggest_initial job has finished
def get_suggest_initial_job_metadata():
    return api_default.suggest_initial_job_id_get(suggest_initial_job_id)


suggest_initial_job = await_job(get_suggest_initial_job_metadata)
print(suggest_initial_job)

############################################################################
### Delete suggest_initial job
############################################################################
print("\n--- deleting suggest_initial job ---")
response = api_default.suggest_initial_job_id_delete(suggest_initial_job_id)
if response is None:
    print("deletion suggest_initial job successful")
else:
    print(response)
